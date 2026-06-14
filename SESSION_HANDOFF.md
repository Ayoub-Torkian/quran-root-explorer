# Session handoff — Qur'ān Root Explorer (paste this into a new task to continue)

## What this project is
A **Streamlit multi-page research app** that studies the Qur'ān's intrinsic structure on the
**rasm** (consonantal skeleton). Local repo (this is the working folder):
`C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2`.
Deployed to **two git remotes**: `origin` (GitHub: Ayoub-Torkian/quran-root-explorer) and
`hf` (Hugging Face Space: **QuranProject/quran-root-explorer**, live at
https://quranproject-quran-root-explorer.hf.space/).

## FIRST STEP every session
**Read `CLAUDE.md`** in the repo root — it holds the locked, non-negotiable rules (response
style, reasoning-calibration protocol, research discipline, base-truth axiom, arrangement
legitimacy, two-tier recording, and the UI/typography rules). Honor it exactly.

## Locked conventions (do not violate)
- **UI:** no font smaller than **12px**; **no grey text — use ink `#10243A`**. Enforced in
  `closeup.py` via `MUTE == INK`. Grey is allowed only for non-text gridlines/borders.
- **Always give a ranked recommendation** (#1 = explicit pick, one line why). Never list flat
  options with "which do you want?".
- **Tag claims `[MEASURED]` vs `[INFERRED]`**; attach a confidence % + "what would flip it".
- **Substrate** = rasm-WORD (has grammar/fāṣila) vs ROOT (content only). Diacritics are a human
  artifact — corroborative only.
- **Close-up standard (8-section anatomy):** Problem → Hypothesis → Method → Results → Gating
  chain → Interpretation → Caveats → Verdict, then Reflection · Summary · Lessons · Takeaway ·
  full **Persian + Arabic abstracts**. Each opens with a `C.onpage([...])` nav strip; each
  *claims-reviewed* page ends with a probability-ranked **"Path forward"** section.

## Key files
- `CLAUDE.md` — the rulebook (read first).
- `state.py` — `NAV_SECTIONS` (sidebar), `render_grouped_nav()`, `inject_css()`. The sidebar
  has a 🔎 **CLOSE-UP** tab with buckets *Units & arrangement* + *Claims reviewed*, plus a
  native `st.link_button` footer → resources (Google Drive).
- `closeup.py` — the close-up component library. Public API: `ar · inject · hero · story ·
  onpage · kpis · section · note · callout · para · table · vbars · hist · verdict · cascade ·
  scale · bars`. All components are ink/≥12px compliant; `vbars` label gutter is 212px (fixed a
  truncation bug).
- Close-up pages: `27_Closeup_Index.py` (Map), `28` Āyah (DEFINED 78), `29` Inter-Sūra
  (REFUTED-ARTIFACT 30), `30` Sūra (CANDIDATE 62), `31` Code 19 (REFUTED-ARTIFACT 22),
  `32_Closeup_Nuzul.py` chronology (CANDIDATE 70), `33_Closeup_Adadi.py` word-count miracle
  (REFUTED-ARTIFACT 35).
- `pages/0_Help.py` — tabbed help; page-tour mirrors the sidebar; Glossary includes close-up
  vocabulary. `COURSE_UPDATE_v1.4.md` documents the close-up module for instructors.

## Data
Real corpus = **`.deploy_workdir/Book6.xlsx`** (~1.2 MB). NOTE: the file at repo-root
`Book6.xlsx` reads as 132 bytes in the sandbox — corrupted by the mount; always use
`.deploy_workdir/Book6.xlsx`. Columns (0-indexed): 5 = sūra#, 6 = āyah#, 7 = name, 8 = roots,
9 = root tokens, **10 = tokenized rasm (no diacritics)**, 11 = with diacritics, **12 = revelation
order**. Persian-form characters (ی, ک). Totals: 135,366 tokens · 7,236 types · 114 sūras.
Useful measured constants: verse-length↔revelation r = 0.66 (R² 0.44); Meccan 14 vs Medinan 30
words/āyah; within-sūra σ 8.4 ≈ between σ 11.1.

## CRITICAL gotchas (these cost time if forgotten)
1. **The sandbox mount intermittently serves stale/truncated copies of files you just edited.**
   So `python -m py_compile` *inside the sandbox* often fails with a SyntaxError at a line far
   below your edit (mid-string/mid-call) — that is **truncation, not a real error**. Verify edits
   with the **Read/Grep tools (host-reliable)** instead, and have the **user compile + push
   locally**. A brand-new file usually compiles fine once (before the mount goes stale).
2. **Deploy is manual, by the user, in PowerShell.** Always hand off a one-line command. PowerShell
   uses `;` not `&&`, and they must `cd` into the repo first:
   ```powershell
   cd C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2; python -m py_compile <files>; git add <files>; git commit -m "..."; git push origin main; git push hf main
   ```
3. **Streamlit's HTML sanitizer strips inline `style` attributes containing `!important`.** For
   forced colors use a `<style>` block (where `!important` survives) or a native widget
   (`st.link_button`, `st.page_link`). Plain inline colors are fine.
4. **Usage page** (`pages/9_Usage.py`) is gated by the **`ADMIN_PASSWORD`** env secret — set it on
   the HF Space (Settings → Variables and secrets, or `huggingface_hub.add_space_secret`). Not in
   code by design.

## Where things stand
All close-ups are built, standard-compliant, cross-referenced, and carry "Path forward" sections.
Help + course docs updated. The no-grey/min-12 color sweep was applied to the close-up module and
the heavy ledger pages; a full app-wide sweep of remaining legacy pages is the open follow-up
(use the corrected grep: `#(56|5B|41|47|7A|8F|34|46|6A|5A)[0-9A-Fa-f]{4}` and bump any
`font-size` < 12). Nothing is blocking.

## How to start the new task
Tell the assistant: "Read `CLAUDE.md` and `SESSION_HANDOFF.md` in
`C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2`, then [your next request]." It will have
full context to continue seamlessly.
