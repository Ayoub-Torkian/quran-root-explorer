# re-deploy 1779771131
"""Admin: Usage dashboard — anonymous visit counts and country distribution.

Password-gated via env var ADMIN_PASSWORD.
"""
from __future__ import annotations

import os
import datetime as _dt

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import analytics

st.set_page_config(page_title="Usage", page_icon="📊", layout="wide")

# ── Password gate ─────────────────────────────────────────────────────
EXPECTED = (os.environ.get("ADMIN_PASSWORD") or "").strip()

if not EXPECTED:
    st.error(
        "🔒 Usage dashboard is disabled.  Set the `ADMIN_PASSWORD` secret "
        "in your hosting environment (Hugging Face Space → Settings → "
        "Variables and secrets) to enable this page."
    )
    st.stop()

if not st.session_state.get("_admin_ok"):
    st.markdown("### 🔒 Admin access required")
    pwd = st.text_input("Password", type="password", key="admin_pwd")
    if st.button("Unlock"):
        if pwd == EXPECTED:
            st.session_state["_admin_ok"] = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()

# ── Dashboard ────────────────────────────────────────────────────────
st.markdown("## 📊 Usage dashboard")
st.caption("Anonymous visit counts and country distribution.  No personal "
           "data is collected — only an opaque per-browser UUID and a "
           "two-letter country code.")

df = analytics.events_dataframe()
if df.empty:
    st.info("No events recorded yet.  Once visitors arrive, this dashboard "
            "will populate automatically.")
    st.stop()

now = _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc)
df = df.sort_values("dt")

# Auto-refresh every 60 s
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

# ── Self-diagnostic strip ────────────────────────────────────────────
total_events = len(df)
with_cc      = int((df["country"] != "??").sum())
pct_cc       = (with_cc / total_events * 100) if total_events else 0
span_hours   = max(0.01, (df["dt"].max() - df["dt"].min()).total_seconds() / 3600)

def _badge(ok, label, detail):
    bg = "#1D9E75" if ok else "#E63946"
    icon = "✓" if ok else "✗"
    return (f'<span style="background:{bg};color:#fff;padding:4px 10px;'
            f'border-radius:6px;font-size:13px;font-weight:600;'
            f'margin-right:8px;display:inline-block;">{icon} {label}</span>'
            f'<span style="font-size:12px;color:#3D4757;margin-right:18px;">{detail}</span>')

db_ok    = total_events > 0
ipapi_ok = pct_cc > 0
mirror_on = bool(os.environ.get("ANALYTICS_DATASET_REPO", "").strip())

st.markdown(
    '<div style="background:#EEF3FB;border-left:4px solid #1D3557;'
    'padding:10px 14px;border-radius:6px;margin:8px 0 14px;">'
    + _badge(db_ok, "DB live", f"{total_events} events · {span_hours:.1f}h span")
    + _badge(ipapi_ok, "Country tracking", f"{with_cc}/{total_events} have country ({pct_cc:.0f}%)")
    + _badge(mirror_on, "HF mirror",
             "persistent across restarts" if mirror_on
             else "ANALYTICS_DATASET_REPO not set — data lost on each restart")
    + '</div>',
    unsafe_allow_html=True,
)

# ── Time-period selector ─────────────────────────────────────────────
data_span_days = (df["dt"].max() - df["dt"].min()).total_seconds() / 86400
if data_span_days > 30:
    _default_idx = 2
elif data_span_days > 7:
    _default_idx = 1
else:
    _default_idx = 0
window = st.radio("Time window",
                  ["Last 7 days", "Last 30 days", "All time"],
                  horizontal=True, index=_default_idx, key="usage_window")

if window == "Last 7 days":
    since = now - _dt.timedelta(days=7)
    prev_since = since - _dt.timedelta(days=7)
elif window == "Last 30 days":
    since = now - _dt.timedelta(days=30)
    prev_since = since - _dt.timedelta(days=30)
else:
    since = df["dt"].min()
    prev_since = since

cur = df[df["dt"] >= since]
prev = df[(df["dt"] >= prev_since) & (df["dt"] < since)] if window != "All time" else cur.iloc[0:0]

unique_visitors  = cur["user_id"].nunique()
unique_countries = (cur[cur["country"] != "??"])["country"].nunique()
page_views = (cur[cur["event"] == "page_view"]).shape[0]
searches   = (cur[cur["event"] == "search"]).shape[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Unique visitors", f"{unique_visitors:,}",
          delta=f"{unique_visitors - prev['user_id'].nunique():+d}" if not prev.empty else None)
c2.metric("Countries", unique_countries)
c3.metric("Page views", f"{page_views:,}")
c4.metric("Searches", f"{searches:,}")

st.divider()

# ── World map ────────────────────────────────────────────────────────
st.markdown("### 🗺️ Visitors by country")
by_country = (cur[cur["country"] != "??"]
              .groupby("country")["user_id"].nunique()
              .reset_index(name="visitors"))
if by_country.empty:
    st.info("No country data yet — open the 'Inbound HTTP headers' expander at the "
            "bottom to see which headers HF is passing through.")
else:
    fig = px.choropleth(by_country, locations="country", locationmode="ISO-2",
                        color="visitors", color_continuous_scale="Plasma",
                        hover_name="country", labels={"visitors": "Unique visitors"})
    fig.update_geos(showcountries=True, countrycolor="#B4B2A9",
                    showcoastlines=True, coastlinecolor="#B4B2A9",
                    projection_type="natural earth")
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=10, b=0),
                      coloraxis_colorbar=dict(title="Visitors"))
    st.plotly_chart(fig, use_container_width=True)

if window != "All time" and not prev.empty:
    st.markdown(f"### 📈 Delta vs previous {window.lower()}")
    cur_c = (cur[cur["country"] != "??"].groupby("country")["user_id"].nunique()
             .reset_index(name="cur"))
    prev_c = (prev[prev["country"] != "??"].groupby("country")["user_id"].nunique()
              .reset_index(name="prev"))
    delta = pd.merge(cur_c, prev_c, on="country", how="outer").fillna(0)
    delta["change"] = delta["cur"] - delta["prev"]
    fig2 = px.choropleth(delta, locations="country", locationmode="ISO-2",
                         color="change", color_continuous_scale="RdBu",
                         color_continuous_midpoint=0, hover_data=["cur", "prev"])
    fig2.update_geos(showcountries=True, countrycolor="#B4B2A9", projection_type="natural earth")
    fig2.update_layout(height=440, margin=dict(l=0, r=0, t=10, b=0),
                       coloraxis_colorbar=dict(title="Δ visitors"))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Daily active users sparkline ─────────────────────────────────────
st.markdown("### 📅 Daily active users")
dau = (df.assign(day=df["dt"].dt.tz_convert("UTC").dt.date)
         .groupby("day")["user_id"].nunique().reset_index(name="dau"))
if not dau.empty:
    line = go.Figure()
    line.add_trace(go.Scatter(x=dau["day"], y=dau["dau"],
        mode="lines+markers", fill="tozeroy",
        line=dict(color="#1D9E75", width=2), marker=dict(size=6)))
    line.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10),
                       yaxis_title="Unique visitors", xaxis_title="",
                       showlegend=False, plot_bgcolor="white")
    line.update_xaxes(showgrid=False)
    line.update_yaxes(showgrid=True, gridcolor="#E2E8F1")
    st.plotly_chart(line, use_container_width=True)

# ── Top searched roots ───────────────────────────────────────────────
st.markdown("### 🔍 Top searched roots")
search_df = cur[cur["event"] == "search"].copy()
if not search_df.empty:
    import json as _json
    rows = []
    for _, r in search_df.iterrows():
        try:
            d = _json.loads(r["payload"])
            for rt in d.get("roots", []):
                rows.append({"root": rt, "user_id": r["user_id"]})
        except Exception:
            pass
    if rows:
        top = pd.DataFrame(rows)
        agg = (top.groupby("root")
                  .agg(searches=("root", "count"),
                       unique_visitors=("user_id", "nunique"))
                  .reset_index().sort_values("searches", ascending=False).head(25))
        st.dataframe(agg, use_container_width=True, hide_index=True)
    else:
        st.info("No searches recorded in this window yet.")
else:
    st.info("No searches recorded in this window yet.")

# ── Raw counts ───────────────────────────────────────────────────────
with st.expander("🛠️ Raw counts", expanded=False):
    st.write({
        "total_events": total_events,
        "unique_visitors_all_time": int(df["user_id"].nunique()),
        "events_by_type": df["event"].value_counts().to_dict(),
        "events_by_country": df["country"].value_counts().to_dict(),
        "first_event_utc": str(df["dt"].min()),
        "last_event_utc":  str(df["dt"].max()),
    })

# ── Inbound HTTP headers — diagnostic for country header ─────────────
with st.expander("🛰️ Inbound HTTP headers (server-side)", expanded=False):
    _hdrs = {}
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        _hdrs = dict(_get_websocket_headers() or {})
    except Exception:
        try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            _ctx = get_script_run_ctx()
            if _ctx is not None:
                _hdrs = dict(getattr(_ctx, "session_client", None).request.headers)
        except Exception as e:
            st.warning(f"Could not read headers: {type(e).__name__}: {e}")
    if _hdrs:
        _hide = {"cookie", "authorization", "x-forwarded-authorization"}
        st.write({k: v for k, v in _hdrs.items() if str(k).lower() not in _hide})
        # Show what get_visitor_country() would pick
        st.markdown("**`get_visitor_country()` returns:** "
                    f"`{analytics.get_visitor_country()}`")
    else:
        st.info("No HTTP headers accessible — this version of Streamlit may not expose them.")

st.divider()
st.caption("Privacy: only an anonymous per-browser UUID and ISO country code are stored.")
