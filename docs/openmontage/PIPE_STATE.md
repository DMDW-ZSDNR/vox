# PIPE STATE — queued factory prompts (Kilo lane)

**Created:** 2026-10-22
**Branch:** `kilo/mega-100`
**Source of truth:** `FACTORY_100_SPEC.md` (root, never edited) + `docs/openmontage/MEGA_STATE.md`
  + `docs/openmontage/RUN_RULES.md` (operating rules for this lane).
**Roles:** all work in this run is **inline, not independent**.

## Prompt queue

The prompt bodies for P0–P14 are **not stored in this repository** (searched: `docs/`,
`.kilo/`, `PROMPT_GALLERY.md`, `.codex/prompts/`, `.github/prompts/` — no `P1`…`P14`
prompt series found). Only the identifiers below are known, so every row stays `PENDING`
until its prompt text is supplied by the owner. No work is started on a prompt whose body
is unknown.

| Prompt | Status | Evidence | Commit |
|---|---|---|---|
| P0 | PENDING | — | — |
| P1 | PENDING | — | — |
| P2 | PENDING | — | — |
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
