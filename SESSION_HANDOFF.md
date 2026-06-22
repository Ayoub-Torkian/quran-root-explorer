# SESSION HANDOFF — Quran Root Explorer

**One file to resume from.** Read this, then `CLAUDE.md` (locked working rules), then the file map below.
Last updated: 2026‑06‑21.

> **Latest session (2026‑06‑21) in one breath:** (1) Built an **on‑corpus semantic engine**
> (`semantic_features.py`: PPMI co‑occurrence → truncated SVD, pure‑numpy, cached) powering **meaning‑based
> related‑verses + concept navigation** — wired into Search (design‑profile table, radial concept‑map,
> meaning chips, all with a stated data‑driven criterion), Read (📎 related verses), Cross‑References.
> (2) **Graph‑theoretic program** (verses/roots → concept network): **#1 bridges** (degree‑NORMALISED
> betweenness vs degree‑preserving null — e.g. ظلم is a true connector) and **#2 dcSBM families + within‑family
> hubs** are **banked into the product** via a precomputed `concept_graph_features.json` (built offline by
> `research/intrinsic/scripts/precompute_concept_graph.py`; the app only READS it — no graph deps at runtime)
> → two new rows on the Search profile ("Network role", "Concept family"). **#3 higher‑order (3‑way) — REFUTED**
> (curveball null gave 6.6×/z+25.8 but the **Kirkwood** test shows it reduces to pairwise; grade ~25). **#4
> temporal/multiplex — modest real residual** (finer‑than‑Meccan/Medinan timing‑homophily survives the
> attribution control, z+4.1; multiplex degenerate in‑sandbox — semantic layer is PPMI‑derived; grade ~52).
> All recorded in `GRADED_FINDINGS_LEDGER.md` + `JOURNEY_LOG.md`. (3) **Excel‑ready copy:** `copy_table()` TSV
> helper in `state.py` → Cross‑refs copies *āyah + its whole layer* as columns; Deep‑Dive seed too.
> (4) **Export catalogue reaudit:** new single‑root charts (revelation profile, network‑role scatter,
> meaning‑neighbors), pairwise charts gated on single‑root, frequency‑baseline decluttered. (5) **IA reaudit:**
> admin **Usage gated** out of public nav; **Concept Deep‑Dive de‑duplicated** (dropped morphology +
> distribution‑bar, kept its unique fusion/null/senses/report); **Home Export tab slimmed to a pointer**
> (kills an eager Excel/PDF/zip rebuild that ran every rerun); nav labels differentiated; **`deploy_git.py`
> guarded** as stale. Calibration + `9_`/`8x` filename numbering checked and **left alone** (harmless).
> **Bug fixes:** Visualize‑tab staleness (safety‑net recompute in `needs_recompute()` when selection drifts
> from results), removed a figure‑cache that caused DuplicateElementId + stale gallery, restored a truncated
> `36_Cross_References.py`, key‑collision hotfix. Staleness + de‑dup + gallery fixes **confirmed live**;
> Export‑tab pointer deployed (deterministically fixed, live eyeball pending the Space's slow cold‑boot).

> **⚙️ OPERATIONAL GOTCHAS (cost real time — read before deploying/verifying):**
> - **Deploy = direct `git push origin main && git push hf main`** (the USER runs it; the sandbox is proxy‑blocked
>   from huggingface.co and has no GitHub creds). **`deploy_git.py` is STALE/guarded — do NOT use it** (its
>   rename map would break the nav).
> - **HF Space sleeps → every push = a slow cold‑boot (~1‑2 min)**; live verification is flaky during boot
>   (tabs die, theme‑chips register as hover). **BATCH several changes into one push** to cut rebuilds.
> - **The bash mount serves STALE/truncated content for recently‑edited files.** The **Read tool is the source
>   of truth.** Validate edits by reconstructing from a fresh `git clone` in `/tmp` (`/tmp/dep`) + `compile()`,
>   NOT by reading the mount. (A truncated mount view once got committed → broke a page.)
> - **`state.py` and `app.py` have a leading BOM** → `compile()` falsely errors unless you read with
>   `encoding="utf-8-sig"`. Python's importer handles the BOM fine; it's a false alarm.
> - **Streamlit `st.tabs` renders ALL tab bodies every run** (hidden too) — never put expensive work in a tab
>   body (the old Home Export tab rebuilt Excel/PDF/zip on every rerun). **Widget keys must be globally unique**
>   (a reused `key="inputbar"` crashed the whole home page).
> - **Per‑concept graph features** live in `concept_graph_features.json` (top‑300 concepts). To refresh:
>   `python research/intrinsic/scripts/precompute_concept_graph.py` (needs networkx + sklearn, offline).

---

## 0. What this project is
A Streamlit multi‑page app deployed to the Hugging Face Space **`QuranProject/quran-root-explorer`**.
It has **two faces**:
1. **Research / discovery program** — the original purpose (latent‑feature discovery on the Qur'ān's
   consonantal skeleton / **rasm**). See `CLAUDE.md`, `research/intrinsic/JOURNEY_LOG.md`,
   `LATENT_FEATURES.md`, `GRADED_FINDINGS_LEDGER.md`, `DISCOVERY_CRITERIA.md`. Governed by the locked
   reasoning/substrate rules (MEASURED‑vs‑INFERRED, rasm‑WORD vs ROOT, arrangement legitimacy, BASE‑TRUTH).
2. **Consumer reading app** — the recent work track: a polished, **mobile‑first** Qur'ān reader
   (>90 % of use is on phones) with translations and **audio recitation**. This handoff focuses on (2).

> The user drives via rapid screenshots + short directives, values **conciseness**, and (per `CLAUDE.md`)
> always wants a **ranked recommendation with an explicit #1 pick**, MEASURED‑vs‑INFERRED honesty, and
> insight‑per‑effort. **Mobile is the priority surface — never neglect it.**

---

## 1. Deploy + environment (IMPORTANT)
- **Two git remotes**: `origin` (backup) and `hf` (the live Space). Deploy = push to both.
- Standard deploy (run on the user's Windows machine, NOT the sandbox):
  ```powershell
  cd "C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2"
  del .git\index
  git reset
  git add <files...>
  git commit -m "..."
  git push origin main
  git push hf main
  ```
- After deploy the **HF Space rebuilds** and **browsers cache aggressively** → tell the user to test in
  **Incognito / clear cache**, especially on phone.
- **The assistant cannot run the deploy** (no git creds) — always hand the user the command block and let
  them run + confirm.

## 2. Gotchas that WILL bite you (learned the hard way)
- **Stale bash mount.** The Linux sandbox mount serves **stale/truncated** copies of files edited via the
  Edit/Write tools → `ast.parse` reports **false** SyntaxErrors and `grep`/`wc` show old content.
  **The Read tool is the source of truth.** Validate logic with standalone `/tmp` scripts or by inspection,
  not by compiling the mounted file. (This recurs constantly — don't be fooled.)
- **`st.markdown(unsafe_allow_html=True)` strips `<script>`/`onclick`.** Anything interactive (audio,
  clipboard, localStorage, toggles) must go through **`st.components.v1.html`** (a sandboxed iframe).
- **components.html iframes can reach the parent DOM only best‑effort** — `window.parent.document...` is
  often blocked, so wrap in `try{}catch{}` and treat parent access as optional (used for "highlight the
  playing āyah" + scroll → degrades gracefully).
- **iOS autoplay**: audio must START from a user tap. After a Streamlit **rerun** the iframe is rebuilt, so
  resuming playback programmatically may be blocked on iOS (position is restored; user taps Play once).
- **`position:fixed`/sticky on component containers is unreliable across devices** — a bottom‑docked player
  built with a `:has(.anchor)+container` selector **broke on the user's laptop** (hidden). Reverted to
  in‑flow. If you re‑attempt sticky, it must degrade safely to in‑flow‑visible.
- **`<details>` on iOS**: setting `display:block` on `<summary>` **breaks the native tap‑toggle** on iOS
  Safari (works on desktop). Hide the marker via `::-webkit-details-marker{display:none}` instead.
- **Renderer/preview keeps crashing** during live browser testing → most changes verified by **inspection +
  the verified data/source**, not live. Ask the user to confirm on device after deploy.

## 3. The reading app — current state (BUILT)
- **`pages/40_Read.py`** — primary Read surface: sticky sūra nav (Prev / picker / "Jump to āyah" / Next),
  position in the **URL `?s=&a=`** (shareable/resumable), translation + reading‑settings in two compact
  columns, a **bookmarks/resume/share tools bar** (localStorage), the **recitation player (top of page)**,
  the inline reader, bottom nav.
- **`surah_reader.py`** — reader engine: `inline_html()` (page‑scroll reader), `build_html()` (iframe
  pop‑out "peek"), `peek()`, `render()`. Each āyah is a `<details>` (tap reveals/collapses translation, works
  in any mode incl. Off→reveals English), a **Bismillah header** (except sūra 1 & 9), a **⌄ chevron**
  affordance, a unique id **`qa{surah}_{ayah}`** on every āyah (so the player can highlight/scroll it), and a
  `.playing` highlight class.
- **`meaning.py`** — 4‑language translations keyed `"S:A"` from `meaning.json` (EN Qarai, AR Jalālayn,
  UR Jawadi, FA Makarem). `translation_control()` = single‑select Off/EN/AR/UR/FA/All, **default Off**,
  persists (session key `tr_lang`).
- **`mobile.py`** — mobile‑first CSS (webfonts, type scale, landscape full‑flow, big tap targets),
  `inject()`, `settings_controls()` (text size A−/A/A+/A++, line spacing). Arabic is the hero font.
- **`pages/38_Search.py`** — root + phrase search; verse rows reuse tap‑to‑toggle; `nword2roots` full‑word→
  root index; `peek()` reader for single‑sūra results.
- **`state.py`** — `NAV_SECTIONS` grouped nav (4 intent areas), corpus loader.
- **`.streamlit/config.toml`** — pins **light theme** (fixes iOS dark‑mode invisible‑text). Do not remove.
- **`Book6.xlsx`** — corpus (Git‑LFS). Cols: `ش  سوره`(surah) `ش  آیه`(ayah) `اسم سوره`(name)
  `ریشه نحوی`(roots) surface/segmented `متن آیه با حرکت`(diacritized display) `ترتیب نزول`(revelation).
  6236 rows + a `جمع` footer row (filter it). 9 truncated display cells repaired (`BOOK6_TRUNCATION.md`);
  roots were NEVER truncated (verified).

## 3a. Reader ↔ research bridge — structural‑context panel [2026‑06‑20]
Connects the app's two faces inside the reading experience. All on `pages/40_Read.py`, powered by
**`structure_scales.read_context(corpus)`** (pure‑python, deployable, NO sklearn).
- **`read_context` return**: `{refs:{(s,a):i}, vroots:[set], drop:set, npmi:{frozenset(a,b):v},
  vt:{i:[{roots,n_suras,support,verses}]}, dist:{root:{arch,n_suras,cov}}, sura_theme:{s:{roots,lo,hi}}}`.
  Reuses `template_families`, `distribution_profiles`, `quran_themes`. **First call is heavy
  (NPMI + templates + distribution + NMF, a few seconds) → ALWAYS cache** (`@st.cache_data` keyed `id(corpus)`).
- **Panel** = expander "📐 What this āyah is part of" after `_read_tools(...)`. Lazy: computes only on first
  open, instant after. Shows, with actual data + analogies + ink ≥12px: concept‑bonds (NPMI · "chord"),
  recurring template/mathānī (roots·#chapters·#verses · "chorus"), chapter theme (NMF · "library section"),
  distribution character (🏛️ Distributed core vs 📍 Concentrated pocket). Honest fallbacks, no overclaim.
- **Jump‑links** (`_jump_btns`): each template row + the strongest bond render `s:a` buttons. Click stashes
  `st.session_state["_jump_to"]` + `st.rerun()`; a handler at the TOP of `40_Read.py` applies it to
  `read_s`/`read_a` BEFORE the nav widgets instantiate (you CANNOT mutate a widget‑bound key after its widget
  is built — that's the whole reason for the top‑of‑page handler). Hover a button → verse Arabic preview
  (cached `_vtext_map`).
- **Fingerprint chip**: always‑visible one‑liner above the panel. Renders only after the panel has been
  opened once (`st.session_state["_struct_ready"]`), then reuses the cached `read_context` — never a fresh
  compute. This is the trick that keeps the reader fast while still giving an at‑a‑glance summary.

## 4. The audio system — `audio_player.py`
- **Source [VERIFIED LIVE]**: `https://cdn.islamic.network/quran/audio/{bitrate}/{edition}/{N}.mp3`,
  **N = global āyah 1..6236** (standard Ḥafṣ). **Streamed → requires internet.**
- **Global‑index mapping [MEASURED]**: `_offsets()` computes it from Book6; verified 1:1→1, 2:1→8, 2:255→262,
  114:6→6236; Book6 counts == standard Ḥafṣ.
- **Bitrate is PER edition** (a hardcoded 128 made some voices 404 = "absent voices"). Verified:
  - **@128**: `ar.alafasy`, `ar.husary`, `ar.minshawi`, `ar.mahermuaiqly`, `ar.ahmedajamy`
  - **@64 only**: `ar.abdulbasitmurattal`, `ar.abdurrahmaansudais`
  - `RECITERS` = `(edition, label, bitrate)` triples — never assume one bitrate for all.
- **Player [REDESIGNED 2026‑06‑19]** — one components.html iframe, a permanently SLIM strip:
  `⏮ ▶/⏸ ⏭ · ref · progress · ⋯ ✕`. Behind **⋯** is a rerun‑free **options sheet** (reciter, speed
  **−/+** over [0.75,1,1.25,1.5,1.75,2], repeat off·āyah·sūra, **follow text** on/off). The iframe
  **self‑grows via `window.frameElement`** so the sheet is never clipped (fixed iframe height was the old
  trap). Continuous **auto‑advance** preserved.
- **Follow [2026‑06‑19]**: `hi(a)` runs on **`au.onplay`** (every play start: tap‑play, prev/next, resume,
  reciter‑change, advance) → highlights `.rdr details.playing` and `scrollIntoView({block:center})` the
  reciting āyah. Gated by the follow toggle. Reaches the reader (MAIN doc) via `window.parent` — best‑effort.
- **Tap‑to‑play [2026‑06‑19]**: each āyah in `surah_reader.inline_html` has a green **▶** (`.vp[data-a]`).
  A bridge in `40_Read.py` (components.html, height 0) delegates the click on the parent doc and
  postMessages every iframe `{qre_cmd:'play', a:N}`; the player loads N and auto‑continues. Best‑effort
  (no‑op if parent access blocked; tap‑to‑reveal still works).
- **Exit [2026‑06‑19]**: **✕** stops, clears the highlight, collapses to a slim **🎧 Recite** launcher
  (reading unobstructed); persists `qre_exited` (no auto‑resume while exited). Launcher or any āyah ▶ re‑enters.
- **Persistence (localStorage)**: `qre_reciter`, `qre_spd` (now a speed VALUE, snapped to the nearest step),
  `qre_rep`, `qre_follow`, `qre_exited`, plus **`qre_surah`/`qre_pos`/`qre_play`** so a rerun doesn't stop
  recitation (resumes position + playback unless exited). `jumped=True` cues the Jump box āyah (don't resume).
- **Placement**: **sticky TOP BAR** in `40_Read.py` — sūra nav (◀ picker · jump · ▶) + the player share one
  keyed container (`.st-key-topbar`, `position:sticky;top:0`) that **degrades to in‑flow‑visible** if a
  browser ignores sticky. (Replaced both the in‑flow‑top AND the fixed bottom‑dock — the dock could hide on
  laptops.)

## 5. Pending / backlog (ranked)
1. **Offline recitation** (open ask — Maher Al‑Muaiqly complete, offline). **Hard for Streamlit/HF**: the app
   needs the server to run, and one full reciter set is ~roughly 1 GB (impractical to bundle in the Space).
   Viable paths: (a) **per‑sūra browser caching** (Cache API + service worker — partial offline replay),
   (b) **downloadable audio pack** the user keeps on device, (c) a future **PWA/native shell**. **Decide
   approach before building.** Maher per‑āyah is confirmed at 128 kbps.
2. **Sticky mini‑player redux** — ✅ DONE 2026‑06‑19 (sticky top bar, nav+player in one keyed container).
3. **Tap‑an‑āyah‑to‑play‑from‑here** — ✅ DONE 2026‑06‑19 (▶ per āyah + postMessage bridge; best‑effort).
4. **Memorization / range loop** — inside the ⋯ sheet: loop āyahs X→Y, repeat each N× (ḥifẓ). Cheap now the
   sheet exists; all in‑iframe. NOT yet built.
5. **Continuous play across sūras** — pass the sūra‑offset map into the player so recitation flows past a
   sūra's end with ref/highlight staying correct. NOT yet built.
6. **Tafsīr (parked)** — al‑Mizan, 4 languages; blocked on a clean per‑āyah Shia source (almizan.org not
   freely available as clean data). Translations already shipped.

### Next moves after the structural panel (ranked, 2026‑06‑20)
1. **Structure‑fingerprint chip on Search results** — same one‑liner next to each hit, so structure is
   visible before reaching Read. Reuses the cached engine. _#1: highest insight‑per‑effort, reader‑facing._
2. **Grade the template families** (clique filter + proper null) — from provisional ~60–65 toward the ≥90
   ledger bar. _Research‑side, slower._
3. **Perf pass on `read_context`** — precompute a small per‑verse fingerprint JSON shipped with the app so
   the chip/panel load instantly cold. _Blocked this session by the stale mount; do in a clean checkout._

### IA status [2026‑06‑20]
4 areas (EXPLORE · DISCOVER · METHODS·LAB · TOOLS). **43 pages, 0 orphans, 0 broken links.** DISCOVER top =
🧭 Discovery Map (start here) · 🗺️ Concept Atlas (concepts) · 🪜 Structure Map (scales), with a signpost on
`37_Discovery_Map.py`. Residual (monitor): Motif (EXPLORE) vs Mathānī/Structure (DISCOVER) split across areas
— mitigated by cross‑links.

## 6. Verification discipline
- Validate corpus logic against Book6 before wiring; re‑check after. Tag **[MEASURED]** vs **[INFERRED]**.
- A usability feature is usability, **not** a discovery — never present it as a new latent feature.
- Always end with a **ranked numbered recommendation (#1 = explicit pick)**.

## 7. File map
```
pages/40_Read.py        primary reader (nav, URL pos, audio, tools, inline reader)
pages/38_Search.py      root/phrase search + verse rows + peek reader
surah_reader.py         reader engine (inline_html / build_html / peek)
audio_player.py         recitation player (CDN, reciters+bitrate, speed, localStorage resume)
structure_scales.py     structure engines + read_context() powering the Read structural-context panel
pages/41_Structure_Map.py  multi-scale structure hub (āyah→Qur'ān + distribution + synthesis)
pages/35_Mathani_Lab.py    recurrence hub (cross-verse template families = the real higher-order layer)
meaning.py              4-lang translations + translation control
mobile.py               mobile-first CSS + reading settings
state.py                grouped nav (NAV_SECTIONS), corpus loader
.streamlit/config.toml  pinned light theme (do not remove)
Book6.xlsx              corpus (Git-LFS)  ·  BOOK6_TRUNCATION.md (repair notes)
meaning.json            translations data  ·  arabic.json (legacy; reader now uses Book6)
CLAUDE.md               LOCKED working rules (read every session)
research/intrinsic/...  the discovery program (JOURNEY_LOG, ledgers, criteria)
```
