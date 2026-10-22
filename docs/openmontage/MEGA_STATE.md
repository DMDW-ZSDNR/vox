# MEGA STATE — factory build toward FACTORY_100_SPEC.md (single resumable run)

**Source of truth:** `FACTORY_100_SPEC.md` (root; never edited) + this file.
**Branch:** `kilo/mega-100` (working branch; never `main`).
**Started:** 2026-10-22.
**Roles:** all work in this run is **inline, not independent** (one agent).

## Resume rule

Resume at the first phase whose status is not in {DONE, OWNER_GATED, BLOCKED}.
After each phase: update this table (status, evidence, commit), commit only the
paths this agent owns, then `git pull --rebase` + non-force push.

## Phase status

| Phase | Status | Evidence | Commit |
|---|---|---|---|
| G0 PREFLIGHT | DONE | ci_fast_suite 10/10 exit 0 (2247->2239 MB); 19 episode/EDL tests pass; 2515 tests collected exit 0; audit appendix A in FACTORY_GAP_AUDIT.md | (this commit) |
| G1 QC + CONTRACTS | DONE | qc.py: added_value start/end fix + narration/graphics/still gates, motion_variety, speculative_label, strict rights flags/provenance; qc_report schema test; release_gate (SINGLE_SOURCE blocks publish); run_evals.py 6/6 PASS; fast suite 12/12 exit 0 | (this commit) |
| G2 EPISODE PIPELINE | PENDING | — | — |
| G3 IMAGE ENGINE | PENDING | — | — |
| G4 VISUAL SOURCES | PENDING | — | — |
| G5 AUDIO + VOICE | PENDING | — | — |
| G6 EDITING + RENDER | PENDING | — | — |
| G7 NICHE + TOPIC | PENDING | — | — |
| G8 PILOT A (speculative evolution) | PENDING | — | — |
| G9 PILOT B (ISS real footage) | PENDING | — | — |
| G10 PACKAGING + SHORTS | PENDING | — | — |
| G11 REVIEW + VERIFICATION | PENDING | — | — |
| G12 OPERATIONS + PORTABILITY | PENDING | — | — |
| G13 SCORECARD | PENDING | — | — |

## Hard rules carried into every phase

- $0 only; no paid routes. Unknown price = BLOCKED.
- No secrets printed. `KAGGLE_API_TOKEN` reported yes/no only.
- Rights fail closed. AI illustrations always labelled, never as real footage.
- No AI upscaling of footage, no voice cloning, no music without stored licence.
- Manual publishing only; no OAuth to YouTube.
- QC fail-closed: cannot run => BLOCKED/NOT_RUN, never PASS.
- Code test-first (red then green); record exact commands + exit codes.
- Never claim a command/test/commit/push/Kaggle run that was not observed.
- Stop the whole run only if free disk < 800 MB after deleting caches this run created.

## Owner decisions (never waited on)

| Decision | Safest default used | Where to change |
|---|---|---|
| Image model (blind scores) | `klein` advisory (S7 report), marked OWNER_GATED | `config/illustration.json` → `model` |
| Voice acceptance | Kokoro-82M (licence gate PASS), owner sign-off OWNER_GATED | `config/voice.json` |
| Speculative illustration share | 0.15 of runtime, labelled | `docs/openmontage/niches/*/profile.yaml` |
| Emblem policy | reject emblem-as-main-picture; incidental emblem flagged REVIEW | `config/qc_thresholds.json` |
| Disclosure wording | checklist citing official YouTube help page, owner confirms | `docs/openmontage/package/<ep>/DISCLOSURE.md` |
| Publication / Studio metrics | NOT_PUBLISHABLE drafts only | owner action |

## Blockers

(none yet)
