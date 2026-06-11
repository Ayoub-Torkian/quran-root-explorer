# PROJECT ORGANIZATION PLAN — one public home for everything

*Status: PROPOSAL v0.1 (brewing). Critical review + staged operationalization of the idea:
"put everything in one organized, public GitHub directory that everybody can access for free;
the app lives there too; every revision is reflected; fold in the Google Drive material without
clutter or redundancy." Nothing destructive happens until each stage is approved.*

---

## 0. The idea, in one line
A single **public GitHub repository** becomes the canonical home for the *whole* project —
the app, the research papers, the evidence, the method, the course, and the data — organized so a
newcomer can find what they want in seconds, with the live app deploying *from* that same repo so
code and app never drift apart.

---

## 1. Critical review (where the idea is strong, where it needs care)

**What's right about it.** One source of truth ends the current fragmentation: today the same files
exist in the working folder, in a 6.5 MB `.deploy_workdir` clone, on a Hugging Face Space, and across
a separate Google Drive. That is four partial copies and no canonical one. Git is purpose-built for
exactly this: it gives you history (every revision reflected automatically), public read access for
free, and a deploy hook so the app stays in lockstep. Making it public also fits the project's spirit —
the work is meant to be read, probed, and challenged by anyone.

**Where it needs care — five real risks, each with a fix:**

1. **Secrets leak (highest priority).** The folder contains `.hf_token`, a live Hugging Face write
   token, and `.git` LFS material. A public repo would expose it instantly, and Git history is
   forever — deleting a file later does *not* remove it from history. *Fix:* a hard secret-scrub gate
   before the first public push, a `.gitignore` that excludes all token/credential files, and **rotate
   the current token now** since it has been sitting in a folder slated to go public.

2. **Publishing work-in-progress.** The research is explicitly mid-sweep ("nothing is final;
   re-evaluate every verdict"). Public readers may quote a tentative finding as settled. *Fix:* this is
   a presentation problem, not a reason to stay private — surface the `DESIGN_STANCE` voice (data-driven,
   no overclaim, honest nulls as first-class) in the README, and clearly separate `findings/` (current
   verdicts, dated) from `experiments/` (raw, in-flight).

3. **Religious-text sensitivity.** A public repository making measurable claims about the Qur'an will
   be read closely by a wide audience. *Fix:* the project's own locked methodology already handles this —
   no miracle-tone, every claim shown with its null and comparator. Lead with method and license.

4. **Large/binary data + reproducibility.** `Book6.xlsx`, `spatial_forest.json`, `.npy`, `.db` files
   bloat a Git repo and don't diff well. *Fix:* keep small reference data in `data/`; route anything
   large or regenerable through Git LFS or a documented regeneration script, so clones stay light.

5. **Two moving parts can still drift.** "App lives in the repo" only helps if the deploy *reads* from
   the repo. *Fix:* wire Hugging Face to auto-deploy from GitHub (below), so a push is the single action
   that updates everything.

**Verdict:** the concept is sound and worth doing. The right shape is **public, but staged** — scrub
and structure first, push second, automate deploy third, fold in Drive fourth. Public from day one of
the *push*, never private-forever; the staging is about safety and tidiness, not secrecy.

---

## 2. Target structure (discoverable by a stranger)

```
quran-root-explorer/                 ← repo root (the one public home)
├── README.md                        ← what this is · live-app link · how to read the findings · how to contribute
├── LICENSE                          ← so "free for everybody" is legally real (see §6)
├── CONTRIBUTING.md                  ← how revisions flow in (see §4)
├── .gitignore                       ← excludes secrets, caches, the deploy clone
│
├── app/                             ← THE APP (exactly what deploys to Hugging Face)
│   ├── app.py · state.py
│   ├── pages/                       ← the ~25 Streamlit pages
│   ├── lib/                         ← analysis.py, plotly_charts.py, stats_*.py, topics.py, interpret.py, …
│   ├── feedback/                    ← feedback + bug widgets (data-store paths documented)
│   ├── requirements.txt · Dockerfile
│   └── README.md                    ← run-locally + deploy notes
│
├── research/
│   ├── papers/                      ← SIX_LENSES_PAPER.md, FINDINGS_FINAL.md, MASTERY_REPORT.md
│   ├── findings/                    ← FINDINGS_SYNTHESIS.md, EVIDENCE.md, RESULTS_comparative.md (the verdicts)
│   ├── method/                      ← DESIGN_STANCE.md, DESIGN_OF_EXPERIMENTS.md, DISCOVERY_CRITERIA.md, CROSS_IMPACT.md, REFLECTIONS_…
│   ├── handoffs/                    ← HANDOFF_MASTERY.md, DEEP_DIVE_HANDOFF.md, ROADMAP_TwoBooks.md, SEQUENCE_SCALE_PLAN.md, IDEA_SIGNALS_GEOMETRY.md
│   ├── experiments/                 ← sequence_tests/, fusion_*.py, synergy_*.py, ideas_batch*.py, *_test.py … (raw, in-flight)
│   └── coverage/                    ← COVERAGE_MAP.html
│
├── data/                            ← Book6.xlsx, spatial_forest.json, *.npy (large → Git LFS or regen script)
├── course/                          ← RootCourse lectures (the 10-Minute Nuance set) + handouts (.docx)
├── docs/                            ← CHANGELOGs, APP_PLAN.md, UI_REORG_NOTES.md (dev/project docs)
└── deploy/                          ← deploy scripts ONLY — never tokens (creds via env/secret store)
```

Five top-level folders a stranger understands at a glance: **app** (use it), **research** (read the
evidence), **data** (the inputs), **course** (learn), **docs** (project meta). The Drive material
(§5) folds into these same five — it does not get its own dumping ground.

---

## 3. App hosting — GitHub-centric, with a safe transition (user decision)

**Transition decision (user):** *Leave the live app on Hugging Face running and untouched for now.*
Stand up GitHub as the full **mirror + source of truth** in parallel. Only once everything is mature
and proven on the GitHub side do we **retire Hugging Face**. This guarantees nothing live can break
during the move. End-state is still GitHub-centric, public and free; getting there is staged, not
a flip-the-switch cutover.

The end-state below works for *everything except the running app*, with one honest constraint and a
clean fix.

- **Static material — GitHub hosts it outright.** Papers, findings, method, data, course, docs, code,
  and `COVERAGE_MAP.html` are all files: viewable, cloneable, downloadable from GitHub for free, no
  account needed. For all of this, **GitHub is literally the whole host.**
- **The running app — GitHub cannot execute it.** `app.py` is a *Streamlit* (server-side Python) app.
  GitHub serves static files only; GitHub Pages cannot run a Python server. So the live, interactive
  app needs a runtime that runs Python.
- **Recommended runtime: Streamlit Community Cloud.** Free, public, and it deploys **directly from the
  public GitHub repo** — no separate clone, no token in the repo, auto-redeploys on every push. This
  lets us **retire Hugging Face entirely** and makes GitHub the single source in the practical sense.
  Bonus: the HF token then becomes irrelevant and can simply be **revoked**.
- **If you want it on GitHub's own servers later:** `stlite` runs Streamlit in-browser via WebAssembly
  and can be served from GitHub Pages — the only way to *literally* host the app on GitHub. But this
  app is heavy (pandas/networkx/plotly + sizable data), so it's a real engineering effort with
  performance/compat risk. Park it as a future option, not the starting point.

## 3a. Access model — public read, owner-only write (user requirement)

"Users can take anything, change nothing" is the **default** behavior of a public repo, hardened:
- Anyone may view / clone / download / **fork** every file — no account needed to read or download.
- **Write access is owner-only.** No outside account can alter the canonical repo unless added as a
  collaborator (we add none). Enable **branch protection on `main`**.
- Outsiders *can* fork (their own separate copy — yours untouched) and open pull requests/issues
  (*proposals/comments* that change nothing until you approve; Issues can be disabled). This is the
  desired "take and reuse, but can't edit the original" model — no compromise needed.

---

## 4. "Every revision reflected" — the discipline that makes it true

Git gives you this almost for free, with light rules:

- **One commit per meaningful revision**, message describing what changed (a finding landed, a lens
  retired, an app page added). Git history then *is* the permanent, browsable record of every revision.
- **Findings stay in lockstep** exactly as the project already practices: when a verdict changes,
  the same commit updates `FINDINGS_SYNTHESIS.md`, `EVIDENCE.md`, the paper, and `COVERAGE_MAP.html`.
  `CONTRIBUTING.md` encodes this so it survives across sessions and contributors.
- **Releases as checkpoints.** Tag stable points (`v1.4`, `v2.0`) so readers can cite a fixed state
  while `main` keeps moving.
- **Working cadence:** I prepare each change here and explain it; pushing to the public repo is a
  publishing action, so it happens only with your go-ahead (per-session, not blanket).

---

## 5. Local mirror — your explicit question, answered

**Yes, and you essentially get it automatically.** With Git, a *clone* of the repo on your computer
**is** a full local mirror — every file and the entire history. So the recommended setup is:

- The public GitHub repo = canonical home.
- A local clone on your machine (via GitHub Desktop, which you already have installed) = your live
  mirror. `git pull` to refresh it with anything we revise, `git push` to publish your local changes.
- The current `Downloads\Quran_Root_Explorer_Web_v1.2` folder becomes (after the cleanup) that clone,
  or we make a fresh clone and retire the old folder to avoid two divergent copies.

So you don't need to maintain a *separate* mirror by hand — the clone is the mirror, and Git keeps it
in sync in one command. The one rule: **edit in the clone, not in scattered copies**, so there's only
ever one thing to sync.

---

## 6. License — "public domain / everything free" (user direction)
"Public" lets people *see* it; a **license** lets people *use* it. Without one, default copyright law
forbids reuse — so a license is required to make "free for everybody" real.

- **What you own (your code + your writing): full public domain via CC0** (or the Unlicense for code).
  No rights reserved — anyone can take, modify, and redistribute with no conditions. This is the
  maximally-free option and matches your intent.
- **What you don't own (Qur'anic source text, third-party datasets): cannot be relicensed by us.**
  These keep whatever terms their source carries; we credit them in a `NOTICE`/`SOURCES.md`. Dedicating
  them to the public domain isn't ours to do — flagged honestly so the repo's licensing is clean.
- Confirm **CC0 (no attribution required)** vs **CC-BY (attribution required)** for your own material
  and I'll add the files. CC0 = closest to "public domain."

---

## 7. Folding in the Google Drive material (no clutter, no redundancy)
Once the Drive connector is authorized, the merge runs as:
1. **Enumerate** every subfolder and file of the shared Drive link; build a catalog (path, type, size,
   modified date).
2. **Classify** each item into the five top-level folders above (app / research / data / course / docs).
3. **De-duplicate** against what's already in the repo — same content under different names, older
   copies, and superseded drafts are flagged, not blindly copied. Newest/canonical wins; older versions
   are noted in the catalog rather than cluttering the tree.
4. **Report before moving.** You get the catalog + proposed placement + the dedupe decisions to approve,
   *then* files move in. Nothing is deleted from your Drive — this is a copy-and-organize, not a cut.

---

## 8. Staged roadmap (gradual — "brew, then move")

- **Stage 0 — Decide & prepare (now).** This plan; license = **CC0** ✅; GitHub = **new self-contained
  org** (owner to create); Google Drive connector authorized ✅. **Keep the HF token for now** (HF stays
  live during transition; revoke only at the final HF retirement). *No pushing yet.*
- **Stage 1 — Clean & restructure locally.** Remove caches/backups/the deploy clone from the tree,
  reorganize into the five-folder layout, add `.gitignore`, `README.md`, `LICENSE`/`CC0`, `NOTICE`,
  `CONTRIBUTING.md`. Verify the app still runs from the new `app/` layout. *Reversible; nothing public.*
- **Stage 2 — Create the public repo & first push.** After a secret-scrub gate passes, create the
  public GitHub repo, push the cleaned tree, and set **branch protection on `main`** (public read,
  owner-only write). The project is now public, free to read, and read-only to the world.
- **Stage 3 — Stand up the live app on Streamlit Community Cloud (in parallel; HF stays live).**
  Connect it to the public repo; confirm a push auto-redeploys. Hugging Face keeps running untouched
  until the GitHub-hosted app is proven mature — *then* retire HF and revoke its token.
- **Stage 4 — Fold in Google Drive.** Run the catalog → classify → dedupe → approve → merge flow (§7).
- **Stage 5 — Steady state.** Local clone as your mirror; every revision committed; releases tagged;
  research continues on its own track and lands in `research/` as it always has.

---

## 9. Research continuation (the parallel track, unaffected)
The research sweep continues independently of this reorg. Per the handoff, the top next candidate is
**extending the muqaṭṭaʿāt / rasm positional thread, network-first** (dynamic communities, bipartite
sūra×letter graph, letter-transition graph), under the LOCKED controls (equal-N · null · comparator ·
positive-control; divine-rootedness; rearrangement built in; no overclaim). New findings land in
`research/findings/` and stay in lockstep with the paper and coverage map, exactly as the structure
above is designed to support.

---

## 10. Open items needing your input
- **License choice** (§6) — CC0 (true public domain, no attribution) vs CC-BY (attribution required)
  for your own code + writing; confirm.
- **Revoke the HF token** — since we're leaving Hugging Face, the token can simply be deleted/revoked
  (credential action, only you can do it).
- **GitHub account/org** — confirm the account (or org `QuranProject`) the public repo lives under.
- **Google Drive** — connector authorized ✅; say the word and I'll catalog all subfolders for the merge.
