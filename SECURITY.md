# Security policy

This project is public and open to contributions, but it is protected so that **no one can change
the official copy without maintainer review**, and so that mistakes or malicious changes are caught
before they reach anyone.

## Reporting a vulnerability or safety concern
If you find a security hole, a leaked secret, or a safety problem, **please report it privately** —
do not open a public issue that could tip off bad actors. Use GitHub's **"Report a vulnerability"**
(Security → Advisories) on the repository, or contact a maintainer directly. We'll acknowledge it and
work with you on a fix and disclosure timeline.

## How the project is protected
- **Owner-only write.** No outside account can change the official repository. Outsiders may fork and
  open pull requests, but a maintainer must review and merge.
- **Protected main branch.** Direct pushes are blocked; changes require a reviewed pull request and
  passing automated checks.
- **Automated scanning on every change** (free on public repos): secret scanning (blocks tokens and
  keys), dependency vulnerability alerts (Dependabot), and code scanning (CodeQL).
- **No secrets in the repository, ever.** Deploy credentials live in the hosting platform's secret
  store, not in the code. The `.gitignore` blocks token/credential files.
- **The public live app runs from vetted, tagged releases** — not from in-progress work — so an
  un-reviewed change cannot reach users.
- **No blind merges.** Maintainers do not merge changes they don't understand; sensitive changes need
  a second reviewer.

## For maintainers
- Keep the maintainer team small and trusted; add reviewers deliberately.
- Review dependency additions skeptically (supply-chain risk).
- Never expose deploy secrets to pull-request checks coming from forks.
- Rotate any credential the moment it may have been exposed.
