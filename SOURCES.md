# SOURCES & CREDITS — provenance ledger

*Purpose: honor others' work and avoid trespassing on anyone's rights. This lists every input that
did NOT originate with this project, who it belongs to, and its copyright status. Items marked
**⚠ ACTION** must be resolved before the repository is made public/CC0.*

*Draft v0.2 — Owner's position (recorded): the analysis, the compiled dataset (`Book6.xlsx`), and the
research are the owner's own work; the Qur'anic text and the classical comparators are public-domain
material. This ledger reflects that. The only items still flagged are a few **identifiably modern,
third-party** texts (§D) — not in question as to the owner's effort, simply not the owner's to
re-license. Each has a trivial fix.*

---

## A. Your own work (released freely by you)
The analysis, statistics, methods, lenses, all written documents (papers, findings, method,
handoffs), the application code, and generated outputs such as `benchmark_translations.json` and
`spatial_forest.json`. Facts and analyses aren't anyone's property; these are yours to license freely.

---

## B. Third-party inputs — PUBLIC DOMAIN (credit only, safe to include)
Classical works whose authors died centuries ago. A credit line is courteous and correct; no
permission needed. *(If a specific modern critical edition was copied verbatim, its editorial layer
may carry rights — see notes.)*

| File(s) | Work | Author | Status |
|---|---|---|---|
| `corpus/_saj_raw.txt`, `ar_sajprose.txt` | *Maqāmāt* (rāwī ʿĪsā b. Hishām) | Badīʿ al-Zamān **al-Hamadhānī** (d. 1008) | Public domain |
| `corpus/_saj_hariri_raw.txt`, `ar_saj_hariri.txt` | *Maqāmāt* | al-Qāsim **al-Ḥarīrī** (d. 1122) | Public domain |
| `corpus/ar_tabari.txt` | *Tārīkh al-Ṭabarī* | **al-Ṭabarī** (d. 923) | Public domain — *confirm the edition; "ṣaḥīḥ wa ḍaʿīf" suggests a modern edited series whose apparatus may have rights* |
| `corpus/ar_classical2.txt` | *al-Ajwiba al-bahiyya* (religious prose) | classical | Public domain — confirm exact source |
| `corpus/ar_poetry.txt` | line "مغاني الشعب…" | **al-Mutanabbī** (d. 965) | Public domain |
| `corpus/ar_poetry_b.txt`, `ar_poetry_c.txt` | classical Arabic verse | classical | Public domain — confirm poets |
| `corpus/fa_poetry.txt` | line "رواق منظر…" | **Ḥāfiẓ** (d. 1390) | Public domain |

## C. Third-party inputs — the Qur'anic text & dataset
| File | What it is | Note |
|---|---|---|
| `Book6.xlsx` | Qur'anic text (with diacritics), root tagging, and revelation-order data; Persian column headers | **Owner states this is their own compilation.** Recorded as the owner's work. The Qur'anic text itself is universal/public; the tagging and ordering are the owner's effort. No action. |

## D. Third-party inputs — IN COPYRIGHT (⚠ ACTION before going public)
These belong to others and are **not** yours to release under CC0/public domain. Using small excerpts
privately for research analysis is one thing; **publishing the text in a public, freely-licensed repo
is different** and risks exactly the trespass you want to avoid. For each: credit it, and either
remove the raw text, reduce it to a minimal fair-use citation, or replace it with an openly-licensed
equivalent — then let users regenerate results from texts they themselves hold.

| File(s) | What it is | Owner | Recommended handling |
|---|---|---|---|
| `.stage/en_collected.json` (and harvest via `harvest_en.py`) | **Saheeh International** English Qur'an translation | © Saheeh International | Don't ship the translation text. Credit it; let the app fetch/accept it at runtime, or point users to the official source. |
| `corpus/ar_novel.txt` | Novel *Arḍ al-Sāfilīn* | **Aḥmad Khālid Muṣṭafā** (living author) | Remove raw text from the public repo; replace the "modern Arabic novel" comparator with an openly-licensed modern text, or keep only a minimal cited excerpt. |
| `corpus/ar_news.txt`, `ar_news2.txt`, `fa_news.txt` | Modern news articles | respective news outlets | Replace with openly-licensed/CC news, or reduce to minimal cited snippets. Credit the outlet. |
| `corpus/ar_novel.txt`, `fa_prose.txt` (modern religious prose) | Modern prose excerpt | confirm author/publisher | Confirm source; treat as in-copyright until cleared. |

## E. Software dependencies
Listed in `app/requirements.txt` (Streamlit, pandas, numpy, networkx, plotly, openpyxl, …). These are
open-source under their own permissive licenses (MIT/BSD/Apache) — free to use; their licenses are
preserved automatically by pip/PyPI. No action beyond not claiming them as your own.

---

## How this protects your intent
- Everything **you** made → released freely (CC0, your choice).
- Everything **public-domain** → credited, included safely.
- Everything **still owned by someone** → credited AND not republished under your free license; the
  research stays reproducible because users supply those texts themselves.

## Open confirmations needed from you
Just one practical decision: OK to swap the three modern third-party comparator samples (§D) for
openly-licensed equivalents, and credit-and-link the Saheeh International translation rather than
shipping its text? (Recommended — keeps the project fully in the clear, costs nothing scientifically.)
Everything else is recorded as yours or public.
