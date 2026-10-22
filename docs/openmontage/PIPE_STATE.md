# PIPE STATE — queued factory prompts (Kilo lane)

**Created:** 2026-10-22
**Branch:** `kilo/mega-100`
**Source of truth:** `FACTORY_100_SPEC.md` (root, never edited) + `docs/openmontage/MEGA_STATE.md`
  + `docs/openmontage/RUN_RULES.md` (operating rules for this lane).
**Roles:** all work in this run is **inline, not independent**.

## Prompt queue

The prompt bodies for P2–P14 are **not stored in this repository** (searched: `docs/`,
`.kilo/`, `PROMPT_GALLERY.md`, `.codex/prompts/`, `.github/prompts/` — no `P2`…`P14`
prompt series found). Only the identifiers below are known, so every one of those rows
stays `PENDING` until its prompt text is supplied by the owner. No work is started on a
prompt whose body is unknown.

P0 and P1 were executed from the prompt bodies the owner delivered in the session on
2026-10-22 (recorded in the session log below); their evidence and commits are in the
table.

| Prompt | Status | Evidence | Commit |
|---|---|---|---|
| P0 | DONE | admin preflight: branch `kilo/mega-100` pushed non-force (`a502d69..1da2524`, exit 0); `RUN_RULES.md` + `PIPE_STATE.md` created; stray untracked files listed, not added | `0276b8d` |
| P1 | DONE | image model locked as CONFIG: `config/image_engine.json` (klein, OWNER_GATED, SDXL-Lightning FAST_FALLBACK) + model-adapter interface (`tools/illustration/model_registry.py`) + CLI (`scripts/image_engine.py`); 40 new tests pass; CI fast suite 12/12 exit 0 | (this commit) |
| P2 | DONE | style kit for 4 niches (`style.json` + finalized `STYLE_BIBLE.md` each) + consistency kit (canonical front/side/3-4 sheets, seed + card-supported reference policy) + LoRA feasibility note; 30 new tests; 4-image smoke job on Kaggle | (this commit) |
| P3 | PENDING | — | — |
| P4 | PENDING | — | — |
| P5 | PENDING | — | — |
| P6 | PENDING | — | — |
| P7 | PENDING | — | — |
| P8 | PENDING | — | — |
| P9 | PENDING | — | — |
| P10 | PENDING | — | — |
| P11 | PENDING | — | — |
| P12 | PENDING | — | — |
| P13 | PENDING | — | — |
| P14 | PENDING | — | — |

Statuses used here: `PENDING` (queued, not started), `IN_PROGRESS`, `DONE`,
`BLOCKED` (evidence recorded), `OWNER_GATED` (safe default applied, not waited on).

## Rules that apply to every prompt in this queue

- Scope and git discipline: `docs/openmontage/RUN_RULES.md`.
- Never edit `FACTORY_100_SPEC.md`, `AGENTS.md`, `.env*`.
- Never commit media or secrets; commit own paths only; `git pull --rebase`; push non-force.
- Test-first (red → green) with recorded commands and exit codes.
- $0 only; unpriced route = `BLOCKED`. Fail-closed QC; no silent threshold changes.
- Kaggle: submit, record state, one status call between phases — never loop/sleep.
- Persistence: ≤4 attempts per blocker, a concrete change per attempt, 90 min cap, then `BLOCKED`.
- Owner-gated items: safest default, marked `OWNER_GATED`, never waited on.
- Stop the run if free disk < 800 MB after deleting caches this run created.
- Final report ≤12 lines: Status, Commit, Done, Failed/NOT_CHECKED, Owner decision, Next action.

## Session log

### 2026-10-22 — admin preflight (before the P0–P14 queue starts)

- Branch `kilo/mega-100` pushed non-force to `origin`: `a502d69..1da2524` (exit 0);
  remote confirmed at `1da2524`, no divergence (behind 0 / ahead 0 before the push).
- Created `docs/openmontage/RUN_RULES.md` (this lane's operating rules) and
  `docs/openmontage/PIPE_STATE.md` (this queue file).
- Stray untracked files were listed and left unadded (`.opencode/`, `opencode.json`,
  `apollo_11.json`, `artemis_sls.json`, `cassini_saturn.json`, `dart_asteroid.json`,
  `hubble_space_telescope.json`, `hubble_test.mp4`, `james_webb_space_telescope.json`,
  `mars_rover_perseverance.json`, `osiris_rex.json`, `parker_solar_probe.json`,
  `perseverance_test.mp4`, `voyager.json`, `tools/illustration/s1_qc.py`,
  `youtube-niche-finder/`).
- Not done: no prompt body was executed; no QC run; no Kaggle job touched.
- Next action: owner supplies the P0–P14 prompt texts; P0 is then executed under
  `RUN_RULES.md` and this table is updated with evidence and commit hash.

### 2026-10-22 — P1: image model locked as CONFIG

- **Decision (agent advisory, OWNER_GATED):** `klein`. The owner's blind CSV is not
  filled (`projects/s7_blind/results.csv` 0/10, `projects/s8_blind/results.csv` 0/10),
  so no owner winner exists and the model is not waited on. `sdxl-lightning` is
  recorded as the declared `FAST_FALLBACK` for drafts.
- **Files:** `config/image_engine.json` (the lock + one entry per model),
  `tools/illustration/model_registry.py` (adapter interface, fail-closed loader,
  owner decision via `scripts/s7_tally.py`, GPU-minute projection, `FakeGenerator`),
  `scripts/image_engine.py` (CLI: status / project / select --write),
  `docs/openmontage/image_gen/IMAGE_ENGINE_CONFIG.md` (measured speeds + projections).
- **Wiring:** `tools/illustration/episode_batch.py` and `scripts/run_illustrations.py`
  now read the config (prompt target, prompt variant, steps, guidance, model id,
  pipeline class, VAE, distilled-UNet checkpoint, scheduler, install ladder, measured
  timings). The Kaggle-side runner accepts the job's `model_config` block
  (`resolve_model_plan()`), so a model it never saw still runs.
- **Measured (S7/S8 manifests):** klein 24.691 s/img, sdxl-lightning 3.943 s/img,
  dreamshaper-xl-lightning 5.112 s/img, sdxl 41.400 s/img, zimage BLOCKED (0 usable
  images). 100 images: 43.4 / 7.8 / 9.2 / 70.4 GPU minutes (incl. one model load).
- **Tests (red then green):** `tests/illustration/test_image_engine_config.py` (28),
  `tests/illustration/test_image_engine_runner.py` (7),
  `tests/illustration/test_image_engine_cli.py` (5) — 40 new tests, all pass;
  `tests/illustration tests/test_run_illustrations.py tests/test_s7_* tests/test_s8_*`
  → 161 passed / 1 skipped, exit 0; `python scripts/ci_fast_suite.py` → 12/12, exit 0
  (300 s, 4124 MB free after).
- **Not done / NOT_CHECKED:** no Kaggle job was submitted (the kernel-side change is
  unit-tested locally only, `NOT_RUN` on Kaggle for the Lightning models); the owner's
  blind scoring is still open; `zimage` stays BLOCKED.
- **Owner decision:** fill `projects/s8_blind/results.csv` (or the S7 pack) and run
  `python scripts/image_engine.py select --write` to re-lock the model as
  `OWNER_CONFIRMED`.
- **Next action:** owner blind-scoring; then the pilot episode (G8) can use the locked
  engine.

### 2026-10-22 — P2: niche styles + consistency kit (LOCKED model)

- **Style files (machine-readable):** `docs/openmontage/niches/<niche>/style.json` for
  `space_iss`, `art_history`, `speculative_science`, `speculative_evolution` — palette,
  line style, camera vocabulary, constraints (positive AND negative forms), label rule,
  anatomy rule, seed policy, aspect, provenance. Each niche also has a finalized
  `STYLE_BIBLE.md` (Status: FINAL).
- **Positive wording:** the locked model (klein) has no negative prompt, so every
  constraint is written positively into the prompt; the SDXL family gets the negative
  forms instead (same style file drives both).
- **Consistency kit:** `tools/illustration/style_kit.py` + `tools/illustration/creature_sheet.py`
  + driver `scripts/creature_sheet.py` (plan / submit / status / fetch). Canonical sheet
  = front + side + three-quarter view per creature from OpenCode's YAML (read only),
  anatomy counts ALWAYS in the prompt, one fixed seed per creature+view (range 3000-3999),
  deterministic job file (byte-identical across runs).
- **Reference workflow:** only for the locked model, because its official card documents
  multi-reference image-to-image editing (https://huggingface.co/black-forest-labs/FLUX.2-klein-4B,
  accessed 2026-10-22). Every other model falls back to seed + prompt anchoring.
- **LoRA feasibility (read-only, nothing trained):** `docs/openmontage/image_gen/LORA_FEASIBILITY.md`
  — a LoRA run for this family needs ~24 GB VRAM (BFL/HF article, 2026-06-04) and ~1 h on
  an RTX 4090 at ~$0.50/run; a Kaggle T4 has 16 GB -> NOT feasible as documented, and the
  rented-GPU path is a paid route -> BLOCKED. Inference fits (measured peak 7995 MB,
  `s7-klein-1`). 81 community adapters exist for the model; the examples are Apache-2.0.
- **Tests (red then green):** `tests/illustration/test_style_kit.py` (23),
  `tests/illustration/test_reference_workflow.py` (4), `tests/test_runner_static.py` (3)
  -> 30 new tests pass; `tests/illustration tests/test_run_illustrations.py tests/test_s7_runner.py
  tests/test_s8_bakeoff.py tests/test_s7_push_bakeoff.py` -> 166 passed / 1 skipped, exit 0;
  `python scripts/ci_fast_suite.py` -> 12/12, exit 0 (293 s, 4112 MB free after).
- **Smoke job (the only generation in this milestone):** `smoke_sheet_klein_4img_2`,
  4 images (vent grazer front/side/3-4 + ice burrower front), klein, 1024x1024, ~4 min of
  T4 time. Attempt 1 FAILED with `NameError: name 'guidance' is not defined` (the manifest
  block referenced a variable that the P1 refactor had moved into the call builder);
  fixed in the runner and covered by the new static check; attempt 2 submitted.
- **Not done / NOT_CHECKED:** no LoRA trained (nothing installed, no dataset, no paid GPU);
  the I2I quality at the locked guidance 1.0 is NOT judged yet (owner); the seed range
  diverges from the S7 (4000) and episode (7000) seeds - new work uses the reserved
  3000-3999 range, recorded in `docs/openmontage/image_gen/CONSISTENCY_KIT.md`.
- **Owner decision:** (a) blind-score the models to unlock the model lock (P1);
  (b) approve or reject the LoRA route (it needs either a community adapter or a GPU
  budget - no training happens on a T4).
- **Next action:** fetch + verify + QC the smoke job output, then the owner judges the
  four images (front/side/3-4 consistency).
