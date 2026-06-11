# research/neural_coding

The pivot from the (closed) text↔genome program to the one direction with a real mechanism and a
**non-flat target**: language ↔ neural code. Scoping rationale: `../two_books_genome/NEURAL_CODING_SCOPING.md`.

Principle carried over from the genome work: **validate the instrument with a planted positive
control before interpreting any null or any real-data result.**

- `FIRST_STEP.md` — what's done and the concrete next step (one real open dataset).
- `scripts/encoding_sim.py` — encoding-model harness, validated on a simulation with a known
  feature→response mapping; the positive control (double dissociation) fires.
- `scripts/encoding_sim_result.json` — the run output.
- `figures/N1_double_dissociation.png` — the validated positive control.
- `scripts/fetch_narratives.py` — downloads one Pieman subject (BOLD + word onsets) from the public
  OpenNeuro S3 mirror via botocore (no AWS CLI / no credentials); prints the exact next command.
- `scripts/encoding_real.py` — real-data adapter (BOLD→ROIs, word-onset features, HRF), same
  control stack as the simulation.

Run locally (data is multi-GB):
    python scripts/fetch_narratives.py        # downloads + prints the encoding_real.py command
    # then run the printed command (optionally add --glove glove.6B.300d.txt)

- `scripts/encoding_multi.py` — multi-subject stability run (step 1); `figures/N2,N3`.
- `scripts/encoding_semantic.py` — step 2: semantic arm via variance partitioning (Whisper word
  timings + GloVe); does meaning add held-out variance beyond low-level features.
- `scripts/encoding_real.py` + `STEP3.md` — step 3: auditory-vs-language dissociation (engine ready;
  needs preprocessed/MNI data — DataLad derivatives or fMRIPrep).

- `NEURAL_PILOT.md` — the consolidated, publication-shaped pilot write-up (companion to the genome
  paper); figures N1–N3 embedded.

Status:
- step 1 (acoustic envelope) — DONE: replicated positive across 5 subjects (Fig. N3), ~25% of ceiling.
- step 2 (semantic) — DONE: honest null (unique semantic below floor) on raw single-subject data.
- step 3 (anatomical dissociation) — DONE: INCONCLUSIVE across 3 iterations; caught a false positive;
  needs fMRIPrep + multiple subjects (engine ready). See FIRST_STEP.md / STEP3.md.
- Consolidated in NEURAL_PILOT.md.
