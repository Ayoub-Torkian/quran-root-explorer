# Contributing

Thank you for wanting to help. This project is meant to be a shared, global effort — and it stays
trustworthy because contributions are **proposed openly and reviewed before they're accepted.**
Nothing you submit changes the project until a maintainer reviews and merges it, so you can
experiment freely.

## The ground rules (what keeps this project honest)

1. **Evidence-first, no overclaiming.** Every analytical claim must come with its statistic, a
   null/baseline, an equal-sized comparison, and an honest verdict. Null and "no different from
   ordinary" results are welcome and reported as first-class findings. No "miracle" framing.
2. **Credit others.** If you bring in any text, data, or code that isn't your own, add it to
   `SOURCES.md` with its origin and license. Do not add copyrighted text to the public repository.
3. **Respect the subject.** This studies a scripture sacred to many. Keep contributions scholarly,
   measured, and free of polemic in any direction.
4. **Reproducible.** Analysis code should run from the data in `data/` (or a documented source) so
   others can re-check your result.

## How to propose a change

1. **Fork** this repository (your own copy — the original is untouched).
2. Make your change in your fork.
3. Open a **pull request** describing what you changed and why. If it's an analysis, include the
   method, the null, and the comparison.
4. A maintainer reviews it. Automated checks (tests, security and secret scanning) run first.
5. On approval, it's merged. If a finding changes, the matching documents in `research/` are updated
   in the same change, so the record always stays consistent.

## What not to submit
- Secrets, tokens, API keys, or passwords (the repo blocks these automatically — keep them out).
- Copyrighted text or data you don't have the right to release.
- Large binary files without discussing first (use the data conventions in `data/`).

## Not a programmer? You can still help
Open an **issue** to report a mistake, suggest a new "lens"/idea to test, point out an unclear
explanation, or offer a translation. Ideas and corrections are as valuable as code.

## Becoming a maintainer
This is a community project. Trusted, consistent contributors can be invited to help review. Only
maintainers can merge — see [SECURITY.md](SECURITY.md) for why that gate matters.
