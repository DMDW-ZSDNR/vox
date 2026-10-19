# MILESTONE Z state — OpenMontage Kilo (space / astronomy niche)

**Branch:** factory/business-documentary-pilot  
**HEAD:** K complete (8e96cda); Z1-Z9 this session  
**Started / updated:** 2026-10-19  
**Disk:** ~6.1 GB free /workspaces, ~29 GB free /tmp (above 800 MB stop threshold)  
**Rules:** zero-cost only (unknown/unpriced route = BLOCKED), curl -L for downloads, max 60 requests/phase, no paid routes, no AI upscaling, no publishing/upload, no secrets printed/committed, never touch `youtube-niche-finder/` or owner's `.env.example`/`AGENTS.md`. Roles inline, not independent. Venv + weights live outside the repo (/tmp/kilo/*) and are never committed.

## Phase status

| Phase | Status | Evidence | Commit |
|-------|--------|----------|--------|
| Z1 VOICE ENV | DONE | Isolated python3.12 venv at /tmp/kilo/z1_venv. Kokoro-82M via kokoro-onnx 0.6.1 (PyPI, MIT) + ONNX weights from GitHub Releases (thewh1teagle/kokoro-onnx model-files-v1.1, model Apache-2.0). kokoro-onnx==0.6.1, onnxruntime==1.20.1, espeakng-loader==0.2.4, phonemizer==3.4.0. Weights: kokoro-v1.0.onnx (310MB) + voices-v1.0.bin (27MB) in /tmp/kilo/kokoro_onnx_weights/ (gitignored). 10s sample synthesized (15.46s, RTF 1.0), finish_audio PASS, qc.py PASS (ebur128 I=-15.8 LUFS). NOTE: HF xet/CDN blocked — kokoro-onnx route used instead; HF Kokoro weights NOT re-downloaded. | 580d1d9 + z1-onnx |
| Z2 ARTEMIS DRAFT | DONE | 3:05 video, qc.py PASS (11 PASS + 1 REVIEW static_by_design), NOT_PUBLISHABLE. Media under projects/ (gitignored, not committed). | e0739ed |
| Z3 PIPELINE | DONE (smoke OK) | scripts/run_episode.py (10-stage chain, per-stage checkpoint+resume+idempotency via output hash, fail-closed, 800MB disk budget, wall-time/disk logging, STAGE_REGISTRY pluggable). scripts/z3_kokoro_narrate.py (kokoro-onnx route). 6/6 orchestration tests pass. Smoke test on artemis: VERDICT OK (all stages incl. qc PASS, duration drift 0.00s). qc.py claim_ids_resolve generalized to comma-separated IDs (regression test added). | 554ab91 + run_episode edits |
| Z4 CHAPTER MODE | DONE code+tests, dry-run limited | run_episode.py --chapters (per-chapter checkpoint+resume, per-chapter disk budget, xfade concat, final loudness). 5/5 chapter tests pass. docs/openmontage/LONGFORM_SPEC.md (40-50 min, added-value gate, step ladder, owner's YouTube Studio metrics go/no-go). End-to-end render dry-run NOT completed: render EDL is Artemis-hardcoded (fixed 12-cut plan), not chapter-subset; per-chapter render would produce wrong/duplicated content. Documented as known gap. | adfbb9e + run_episode edits |
| Z5 SERIES PLAN | DONE | docs/openmontage/SERIES_PLAN.md — 12 ranked space topics; per topic HD clips, rights_basis, primary docs, usable minutes, max feasible length; T1 demand measured (weak signal); SpaceX Tier C excluded. | ee3db4a |
| Z6 SCRIPTS | DONE | Apollo test flights, ISS, JWST scripts + claim ledgers + Shorts plans; claim_ids resolve ALL OK. | dbd0276 |
| Z7 PACKAGING | DONE | docs/openmontage/slice/artifacts/ARTEMIS_PACKAGING.md (3 titles, thumbnails, description+chapters+credits, synthetic-voice disclosure citing support.google.com/youtube/answer/14328491). | a798db6 |
| Z8 REVIEW PACK | DONE | docs/openmontage/REVIEW_PACK.md (files to read, paste-ready reviewer prompt, verification commands w/ exit codes). 29 fast tests pass exit 0; py_compile OK. | 3476815 |
| Z9 CLOSE | DONE | OWNER_ACTIONS.md, MASTER_RUN_STATE.md, CHANGELOG.md, LESSONS.md updated; stop Codespace commands printed. | a660c5c + 579ba4c |
| APOLLO 9 (in-session) | PARTIAL (build blocked) | Claim ledger APOLLO9_CLAIM_LEDGER.md (42 claims, all TWO_SOURCES). Script table APOLLO9_FULL_SCRIPT_v0.md (13 sentences, B1-B8). claim_ids resolve: ALL OK (13/13 resolve, all TWO_SOURCES). Narration synthesized via kokoro-onnx (421s, 13 sentences). finish_audio PASS. Subtitles via stable-ts (1005 words, 134 cues). BUILD+QC BLOCKED: no Apollo 9 HD footage downloaded; render stage is Artemis-specific (hardcoded EDL + Artemis footage path) — rendering now would produce a wrong video. Owner action: download Apollo 9 HD footage (NASA/archive.org via curl -L), create Apollo 9 EDL, then run build + qc.py with all inputs. | pending |

## Blocker carried (Z1/Z3/Z4 + Apollo 9 build)
Kokoro-82M HF weights unreachable (cas-server.xethub.hf.co + us.aws.cdn.hf.co blocked; HF_HUB_DISABLE_XET=1 HTTP stuck at 0 bytes). Resolved for narration via kokoro-onnx GitHub Releases route (weights in /tmp/kilo/kokoro_onnx_weights/). Apollo 9 video build additionally blocked by missing Apollo 9 HD footage.

## Rules observed
- KAGGLE_API_TOKEN never printed/logged/committed.
- Network: NASA images-api, archive.org (curl -L), YouTube help page (read-only), GitHub/PyPI for kokoro-onnx. NTRS blocked — do not retry.
- Downloads into gitignored /tmp or projects/, never committed; delete temp files.
- Disk < 800 MB free -> write state and STOP whole run.
- Code test-first (red then green); report exact commands/exit codes; never claim unobserved work.

## Stop Codespace commands (owner)
- `gh codespace stop -c <codespace-name>`
- `gh codespace list`
- Or VS Code Codespaces panel: stop active codespace

## Rollback
`git revert` of the session's commits on branch `factory/business-documentary-pilot`.
