# re-deploy 1779771065604001220
"""Anonymous visit-tracking — never blocks the app, never stores PII.

What it captures
  • Anonymous visitor UUID (generated browser-side in localStorage)
  • ISO country code (derived browser-side from ipapi.co, never an IP)
  • Event type: page_view | search | export | session_start
  • Optional small payload (e.g. searched roots, export format)
  • UTC timestamp

What it does NOT capture
  • Raw IP addresses, email, real name, precise location
  • Any user-typed content beyond the searched roots themselves

Storage
  • Local SQLite at $ANALYTICS_DATA_DIR (default /data/analytics.db)
  • Background thread mirrors new rows to a private HF Dataset every
    5 minutes so data survives container restarts on the free tier.

Privacy compliance
  • Country-only granularity → no GDPR consent banner needed
  • No cookies (localStorage is exempt under most regulations
    when used for non-tracking purposes; the UUID is opaque)
  • Visit-counter banner shown once per visitor to be transparent
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

import streamlit as st

# ─── Config (all overridable via HF Spaces "Secrets") ────────────────────
DATA_DIR = Path(os.environ.get("ANALYTICS_DATA_DIR", "/data"))
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    # Fall back to a relative path if /data isn't writable (e.g. local dev)
    DATA_DIR = Path("./.analytics")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "analytics.db"

# Optional HF Dataset mirror (events survive container restarts)
HF_DATASET_REPO = os.environ.get("ANALYTICS_DATASET_REPO", "").strip()  # e.g. "youruser/quran-roots-analytics"
HF_TOKEN = os.environ.get("HF_TOKEN", "").strip()
MIRROR_INTERVAL_SEC = int(os.environ.get("ANALYTICS_MIRROR_INTERVAL", "300"))

_DB_LOCK = threading.Lock()
_MIRROR_LOCK = threading.Lock()
_LAST_MIRROR_TS = 0.0
_MIRROR_STARTED = False


# ─── SQLite plumbing ─────────────────────────────────────────────────────
def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(str(DB_PATH), isolation_level=None,
                        check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS events (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts        REAL NOT NULL,
                    event     TEXT NOT NULL,
                    user_id   TEXT,
                    country   TEXT,
                    payload   TEXT
                  )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id)")
    return c


# ─── Visitor identity (set by JS via query params; see state.py) ─────────
def _qp_get(key: str) -> str | None:
    """Read a query-string value across Streamlit versions."""
    try:
        # 1.30+
        v = st.query_params.get(key, None)
        if isinstance(v, list):
            return v[0] if v else None
        return v
    except Exception:
        pass
    try:
        # Legacy
        return st.experimental_get_query_params().get(key, [None])[0]
    except Exception:
        return None


def get_visitor_id() -> str:
    """Stable per-browser id, sourced from URL query param `vid` (set by
    the JS shim in state.py).  Only cache a REAL id from the URL — never
    cache the server-side fallback, otherwise the JS-set id is masked on
    later reruns and every session counts as a fresh visitor."""
    vid_qp = _qp_get("vid")
    if vid_qp and 8 <= len(vid_qp) <= 64:
        st.session_state["_visitor_id"] = vid_qp
        return vid_qp
    if "_visitor_id" in st.session_state:
        return st.session_state["_visitor_id"]
    # First-render fallback — used only until the JS sets the URL param
    return uuid.uuid4().hex[:16]


def _country_from_headers() -> str | None:
    """Server-side country lookup from HTTP headers.  HF Spaces sits behind
    CloudFlare which usually injects CF-IPCountry; some setups also provide
    X-Country-Code or similar.  This bypasses all JS / iframe headaches."""
    try:
        # Streamlit's private API — try multiple import paths across versions
        try:
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers() or {}
        except Exception:
            try:
                from streamlit.runtime.scriptrunner import get_script_run_ctx
                ctx = get_script_run_ctx()
                headers = dict(ctx.session_client.request.headers) if ctx else {}
            except Exception:
                headers = {}
        # Headers are case-insensitive — normalize keys to lowercase
        h = {str(k).lower(): str(v) for k, v in dict(headers).items()}
        for key in ("cf-ipcountry", "x-country-code",
                    "x-vercel-ip-country", "x-appengine-country"):
            v = (h.get(key) or "").strip().upper()
            if len(v) == 2 and v.isalpha() and v not in ("XX", "T1"):
                return v
    except Exception:
        pass
    return None


def get_visitor_country() -> str:
    """Two-letter ISO code, e.g. 'US', 'EG', 'DE'.  '??' if unknown.

    Lookup order:
      1. HTTP header (CloudFlare CF-IPCountry, etc.) — most reliable, zero JS
      2. URL query param `cc` set by the JS shim (fallback for hosts
         that don't pass country headers through)
      3. session_state cache from a prior successful lookup
    """
    # 1. Server-side header lookup
    cc_h = _country_from_headers()
    if cc_h:
        st.session_state["_visitor_country"] = cc_h
        return cc_h
    # 2. JS-set query param
    cc_qp = (_qp_get("cc") or "").strip().upper()
    if len(cc_qp) == 2 and cc_qp.isalpha():
        st.session_state["_visitor_country"] = cc_qp
        return cc_qp
    # 3. Cache from previous successful render
    return st.session_state.get("_visitor_country", "??")


# ─── Public API ──────────────────────────────────────────────────────────
def track(event: str, payload: dict[str, Any] | None = None) -> None:
    """Log one event.  Safe to call on every render — fast and non-blocking.

    Never raises: tracking failures must not break the app.
    """
    try:
        if not _MIRROR_STARTED:
            _start_mirror_thread()
        vid = get_visitor_id()
        cc = get_visitor_country()
        body = json.dumps(payload or {}, ensure_ascii=False, default=str)[:1000]
        with _DB_LOCK:
            c = _conn()
            c.execute(
                "INSERT INTO events (ts, event, user_id, country, payload) "
                "VALUES (?,?,?,?,?)",
                (time.time(), event[:32], vid, cc, body),
            )
    except Exception:
        pass  # never break the app on a logging failure


def track_once_per_session(event: str, payload: dict[str, Any] | None = None) -> None:
    """Log an event only the first time it is seen in this session."""
    flag = f"_track_once::{event}"
    if st.session_state.get(flag):
        return
    st.session_state[flag] = True
    track(event, payload)


def events_dataframe(since_ts: float | None = None):
    """Pull events as a pandas DataFrame for the Usage dashboard."""
    import pandas as pd
    try:
        with _DB_LOCK:
            c = _conn()
            if since_ts is None:
                df = pd.read_sql_query(
                    "SELECT ts, event, user_id, country, payload FROM events",
                    c)
            else:
                df = pd.read_sql_query(
                    "SELECT ts, event, user_id, country, payload FROM events "
                    "WHERE ts >= ?",
                    c, params=(since_ts,))
    except Exception:
        import pandas as pd
        df = pd.DataFrame(columns=["ts", "event", "user_id", "country", "payload"])
    df["dt"] = pd.to_datetime(df["ts"], unit="s", utc=True)
    return df


# ─── HF Dataset mirror (background thread) ───────────────────────────────
def _start_mirror_thread() -> None:
    global _MIRROR_STARTED
    if _MIRROR_STARTED:
        return
    _MIRROR_STARTED = True
    if not HF_DATASET_REPO or not HF_TOKEN:
        # Mirror disabled — data lives only in the local SQLite (ephemeral
        # on free-tier hosts).  This is fine for local dev.
        return
    t = threading.Thread(target=_mirror_loop, daemon=True, name="analytics-mirror")
    t.start()


def _mirror_loop() -> None:
    global _LAST_MIRROR_TS
    # Initial pull on startup so we don't lose history from previous runs
    try:
        _pull_from_hf()
    except Exception:
        pass
    while True:
        try:
            time.sleep(MIRROR_INTERVAL_SEC)
            _push_to_hf()
        except Exception:
            pass


def _push_to_hf() -> None:
    """Append new events to a CSV in the private HF Dataset."""
    global _LAST_MIRROR_TS
    with _MIRROR_LOCK:
        import pandas as pd
        from huggingface_hub import HfApi
        with _DB_LOCK:
            c = _conn()
            df = pd.read_sql_query(
                "SELECT ts, event, user_id, country, payload FROM events "
                "WHERE ts > ? ORDER BY ts",
                c, params=(_LAST_MIRROR_TS,))
        if df.empty:
            return
        # Stream-append a daily CSV (one file per UTC date)
        import datetime as _dt
        today = _dt.datetime.utcnow().strftime("%Y-%m-%d")
        local_path = DATA_DIR / f"events-{today}.csv"
        if local_path.exists():
            df.to_csv(local_path, mode="a", header=False, index=False)
        else:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(local_path, index=False)

        # Push the day's CSV to the HF Dataset (best-effort).
        try:
            api = HfApi(token=HF_TOKEN)
            api.upload_file(
                path_or_fileobj=str(local_path),
                path_in_repo=f"events/{local_path.name}",
                repo_id=HF_DATASET_REPO,
                repo_type="dataset",
            )
        except Exception:
            pass

        # Advance watermark so next push only sees new rows.
        try:
            _LAST_MIRROR_TS = float(df["ts"].max())
        except Exception:
            pass


def _pull_from_hf() -> None:
    """Pull existing day-CSVs from the HF Dataset into local SQLite on startup."""
    global _LAST_MIRROR_TS
    if not HF_DATASET_REPO or not HF_TOKEN:
        return
    with _MIRROR_LOCK:
        import pandas as pd
        from huggingface_hub import HfApi, hf_hub_download

        api = HfApi(token=HF_TOKEN)
        try:
            files = api.list_repo_files(
                repo_id=HF_DATASET_REPO, repo_type="dataset")
        except Exception:
            return

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        max_ts = _LAST_MIRROR_TS
        for remote in files:
            if not remote.startswith("events/") or not remote.endswith(".csv"):
                continue
            try:
                local = hf_hub_download(
                    repo_id=HF_DATASET_REPO,
                    repo_type="dataset",
                    filename=remote,
                    token=HF_TOKEN,
                    local_dir=str(DATA_DIR),
                )
                df = pd.read_csv(local)
            except Exception:
                continue
            if df.empty:
                continue
            with _DB_LOCK:
                c = _conn()
                rows = df[["ts", "event", "user_id", "country", "payload"]].itertuples(
                    index=False, name=None)
                c.executemany(
                    "INSERT OR IGNORE INTO events"
                    " (ts, event, user_id, country, payload)"
                    " VALUES (?,?,?,?,?)", rows)
                c.commit()
            try:
                file_max = float(df["ts"].max())
                if file_max > max_ts:
                    max_ts = file_max
            except Exception:
                pass
        _LAST_MIRROR_TS = max_ts
