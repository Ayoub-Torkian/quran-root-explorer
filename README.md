---
title: Quran Root Explorer
emoji: 📖
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: true
license: mit
short_description: Explore the Quran by roots, networks, and 18 lenses
tags:
  - quran
  - quran-analysis
  - arabic
  - arabic-nlp
  - quran-roots
  - corpus-linguistics
  - digital-humanities
  - religious-text-analysis
  - muqattaat
  - text-mining
---

# Qur'an Root Explorer — an open, evidence-first study of the Qur'an's structure

A free, open project with two halves: an **interactive app** for reading the Qur'an and probing its
structure, and a **research record** documenting what has — and has *not* — been found to be
measurably distinctive about the text. Everything the author created here is free to use, copy, and
build on (see [LICENSE](LICENSE)). Contributions are welcome (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## What this is — and what it isn't

This is an **evidence instrument, not a claims engine.** Every analysis is reported with its
statistic, a null/baseline, equal-sized comparisons, and an honest verdict. Most things tested turn
out to be *register-level or null* — and that is shown as a first-class result, not hidden. The voice
is deliberately data-driven: no overclaiming, no "miracle" framing. The aim is to let anyone read,
test, and challenge the findings for themselves.

The current working thesis, stated carefully: the text's measurable distinctiveness concentrates in
**structured recurrence at long range** — locally it is *less* continuous than ordinary prose, while
across the whole it *returns* to itself more. This remains under active review; nothing is final.

## How it's organized

| Folder | What's in it |
|---|---|
| `app/` | The interactive application (reader, lens lab, feedback) — what gets deployed live. |
| `research/` | The findings, evidence, method, and experiment scripts. |
| `data/` | Reference datasets the analysis and app use. |
| `course/` | Teaching material — short lectures and handouts. |
| `docs/` | Project/development notes, changelogs, plans. |

*(The repository is being reorganized into this layout from years of accumulated working files; see
`docs/PROJECT_ORGANIZATION_PLAN.md` and `docs/REORG_MANIFEST.md` for the migration in progress.)*

## The live app

The app runs on free public hosting and deploys directly from this repository. *(Link added once the
public deployment is live.)* You can also run it locally — see `app/README.md`.

## Using and contributing

- **Use it freely.** Anyone may view, download, clone, or fork everything here — no account needed.
- **Propose changes** via pull requests; report problems via issues. Nothing changes in this
  canonical copy without a maintainer's review. See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Found a security or safety concern?** See [SECURITY.md](SECURITY.md).
- **Be respectful.** See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## C