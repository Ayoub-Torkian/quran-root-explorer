"""feedback.py — v1.4 user-signal layer for the Qur'an Explorer app.

The app is the MAIN INSTRUMENT (see APP_PLAN.md): users READ, TEST lenses, give FEEDBACK on
novel ideas, and report BUGS. This module is the smallest piece of that: it captures feedback,
bug reports, and proposed lenses to local JSONL files, and renders the widgets.

Self-contained: depends only on streamlit + stdlib. Storage is append-only JSONL under
<app>/feedback/, so nothing is ever overwritten and the files are trivial to read/export.
"""
from __future__ import annotations
import json, datetime, platform
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
FB_DIR = HERE / "feedback"
FB_FILE = FB_DIR / "feedback.jsonl"
BUG_FILE = FB_DIR / "bugs.jsonl"
IDEA_FILE = FB_DIR / "ideas.jsonl"

# For now feedback is OFFLINE: forms keep a local copy when the app is run
# locally. (Online persistence can be added later.)

# The 12 gate-validated lenses (kept in sync with SIX_LENSES_PAPER.md / COVERAGE_MAP.html)
LENSES = [
    "1 · Lexical–statistical repetition",
    "2 · Architecture (ring/refrain)",
    "3 · Rhyme / fāṣila",
    "4 · Phonosemantics",
    "5 · Fusion cell",
    "6 · Prosodic rhythm",
    "7 · Morpho-syntax / iltifāt",
    "8 · Wazn templates",
    "9 · Intratextual recurrence",
    "10 · Discourse macrostructure",
    "11 · Syntactic complexity",
    "12 · Lexical-semantic field dynamics",
    "(general / whole app)",
]


def _append(path: Path, record: dict) -> bool:
    try:
        FB_DIR.mkdir(parents=True, exist_ok=True)
        record = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **record}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except Exception as e:  # never let logging break the app
        st.warning(f"Could not save (kept in session only): {e}")
        return False


def _read(path: Path, limit: int = 200) -> list[dict]:
    if not path.exists():
        return []
    out = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
    except Exception:
        pass
    return out[-limit:][::-1]


# ---------------------------------------------------------------- sidebar widget
def render_sidebar_widgets(page: str = "unknown") -> None:
    """Compact, always-visible bug + quick-feedback controls. Call inside the sidebar."""
    try:
        with st.expander("🐞 Report a bug", expanded=False):
            with st.form(f"bug_{page}", clear_on_submit=True):
                txt = st.text_area("What went wrong?", height=80,
                                   placeholder="What did you do, what did you expect, what happened?")
                sev = st.select_slider("Severity", ["minor", "annoying", "blocking"], value="annoying")
                if st.form_submit_button("Send bug report") and txt.strip():
                    if _append(BUG_FILE, {"page": page, "severity": sev, "text": txt.strip(),
                                          "platform": platform.platform()}):
                        st.success("Thanks — bug logged.")
        with st.expander("💬 Quick feedback", expanded=False):
            with st.form(f"fb_{page}", clear_on_submit=True):
                rating = st.radio("This view is…", ["👍 useful", "👎 not useful"], horizontal=True)
                note = st.text_input("Note (optional)")
                if st.form_submit_button("Send feedback"):
                    if _append(FB_FILE, {"page": page, "rating": rating, "note": note.strip()}):
                        st.success("Thanks — feedback logged.")
    except Exception:
        pass  # a widget failure must never break navigation


# ---------------------------------------------------------------- full page
def render_feedback_page() -> None:
    st.title("💬 Feedback, Bugs & Ideas")
    st.caption("The app is meant to be tested and challenged. Tell us what's useful, what's broken, "
               "and what new lens we should try.")

    tab_fb, tab_bug, tab_idea, tab_view = st.tabs(
        ["💬 Lens feedback", "🐞 Bug report", "💡 Propose a lens", "📜 Recent entries"])

    with tab_fb:
        with st.form("page_fb", clear_on_submit=True):
            lens = st.selectbox("Which lens / view?", LENSES, index=len(LENSES) - 1)
            rating = st.radio("Verdict", ["👍 useful", "👎 not useful", "🤔 unclear"], horizontal=True)
            note = st.text_area("What worked or didn't? Did the null/gate make sense?", height=120)
            if st.form_submit_button("Submit feedback"):
                _append(FB_FILE, {"page": "feedback_page", "lens": lens, "rating": rating,
                                  "note": note.strip()})
                st.success("Logged. Thank you.")

    with tab_bug:
        with st.form("page_bug", clear_on_submit=True):
            where = st.text_input("Where? (page / lens)")
            sev = st.select_slider("Severity", ["minor", "annoying", "blocking"], value="annoying")
            txt = st.text_area("Steps, expected vs actual", height=140)
            if st.form_submit_button("Submit bug") and txt.strip():
                _append(BUG_FILE, {"page": where or "feedback_page", "severity": sev,
                                   "text": txt.strip(), "platform": platform.platform()})
                st.success("Bug logged. Thank you.")

    with tab_idea:
        st.caption("A lens is a feature + a null + a gate. Even a rough hunch helps — we'll "
                   "operationalize and gate it (see IDEA_SIGNALS_GEOMETRY.md for the toolkit).")
        with st.form("page_idea", clear_on_submit=True):
            title = st.text_input("One-line idea")
            body = st.text_area("What signal/pattern should we look for, and against what baseline?",
                                height=140)
            if st.form_submit_button("Submit idea") and title.strip():
                _append(IDEA_FILE, {"title": title.strip(), "body": body.strip()})
                st.success("Idea logged. Thank you.")

    with tab_view:
        for label, path in [("💬 Feedback", FB_FILE), ("🐞 Bugs", BUG_FILE), ("💡 Ideas", IDEA_FILE)]:
            rows = _read(path)
            st.subheader(f"{label} ({len(rows)})")
            if rows:
                st.dataframe(rows, use_container_width=True, hide_index=True)
                st.download_button(f"Download {path.name}", path.read_text(encoding="utf-8"),
                                   file_name=path.name, key=f"dl_{path.name}")
            else:
                st.caption("No entries yet.")
