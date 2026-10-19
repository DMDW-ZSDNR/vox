# MILESTONE Z state — OpenMontage Kilo (space / astronomy niche)

**Branch:** factory/business-documentary-pilot  
**HEAD:** 8e96cda (Milestone K complete; K4 close)  
**Started:** 2026-10-19  
**Disk at start:** /workspaces 7.3 GB free; /tmp 39 GB free (STOP whole run if free disk < 800 MB)  
**Rules:** zero-cost only (unknown/unpriced route = BLOCKED, never free), curl -L for downloads, max 60 network requests per phase, no paid routes, no AI upscaling, no publishing/upload, no secrets printed or committed, never touch `youtube-niche-finder/` or the owner's `.env.example`/`AGENTS.md`. Roles inline, not independent. Venv + weights live outside the repo (/tmp/kilo/*) and are never committed.

## Phase status

| Phase | Status | Evidence | Commit |
|-------|--------|----------|--------|
| Z1 VOICE ENV | DONE | docs/openmontage/Z1_VOICE_ENV.md; venv /tmp/kilo/z1_venv (python3.12.3), kokoro==0.2.2, misaki==0.7.17, torch==2.6.0+cpu, weights in /tmp/kilo/hf_cache; 14.625 s sample synthesized, finish_audio PASS, qc.py decode/loudness/silence/freeze PASS (ffprobe_streams FAILED expected: audio-only) | 580d1d9 |
| Z2 ARTEMIS DRAFT (3-4 min) | DONE | docs/openmontage/slice/artifacts/* (qa_report PASS, 13 checks: 11 PASS, 1 REVIEW freezedetect=static_by_design cards, 1 NOT_RUN n/a); video projects/slice_artemis_v0/renders/final_artemis_draft.mp4 1920x1080p30 h264/aac 185.43s (gitignored media); NOT_PUBLISHABLE per credits.txt | a7ca003 |
| Z3 ONE-COMMAND PIPELINE | DONE (code+tests), BLOCKED (smoke) | scripts/run_episode.py + z3_kokoro_narrate.py + z3_subtitles.py + tests/test_run_episode.py; 6/6 orchestration tests pass with fake stages (resume, mid-chain failure, unknown claim_id, rights unknown, hash mismatch, disk threshold). Real smoke test on artemis BLOCKED: Kokoro-82M weights unreachable — HF xet CAS server (cas-server.xethub.hf.co) and CDN (us.aws.cdn.hf.co) both unreachable from this network; /tmp/kilo venv + weights wiped, HF_HUB_DISABLE_XET=1 regular HTTP stuck at 0 bytes. Owner action: restore Kokoro weights cache on a network with HF access. | 554ab91 |
| Z4 CHAPTER MODE | DONE (code+tests+spec), BLOCKED (dry-run) | scripts/run_episode.py --chapters (split <=6min chapters, per-chapter checkpoint+resume, disk budget before each chapter, xfade concat, final loudness pass); 5/5 chapter tests pass; docs/openmontage/LONGFORM_SPEC.md written (40-50 min targets, added-value gate, step ladder, no invented thresholds). Dry-run on Artemis into 2 chapters BLOCKED: Kokoro-82M weights unreachable (same HF network block as Z3). | cd445a0 + LONGFORM_SPEC.md |
| Z5 SERIES PLAN | DONE | docs/openmontage/SERIES_PLAN.md — 12 topics ranked (space niche); per topic: HD clip count, rights_basis, primary docs reachable, est. usable minutes, max feasible length; demand from T1 (5/300 breakouts, weak signal), footage from T5/T12, primary docs from T15; no demand claims beyond measured data; SpaceX Tier C excluded (no PD footage) | ee3db4a |
| Z6 SCRIPTS | DONE | docs/openmontage/slice/{APOLLO_TEST_FLIGHTS,ISS,JWST}_FULL_SCRIPT_v0.md (3–5 min each), docs/openmontage/evidence/*_CLAIM_LEDGER.md, docs/openmontage/slice/*_SHORTS_PLAN.md (45 s each); claim_ids resolve check ALL OK (all claim_ids resolve to ledger, all SINGLE/UNVERIFIED claims flagged); Apollo 4 TWO_SOURCE + 9 flagged; ISS/JWST all UNVERIFIED pending NASA primary page verification | dbd0276 |
| Z7 PACKAGING | DONE | docs/openmontage/slice/artifacts/ARTEMIS_PACKAGING.md (3 truthful titles, 3 thumbnail text options, 1280x720 PNG thumbnails in gitignored projects/ from own graphics+NASA still, no emblem/people, description with chapters+credits, synthetic-voice disclosure checklist citing support.google.com/youtube/answer/14328491 with owner action items) | a798db6 |
| Z8 INDEPENDENT REVIEW PACK | NOT_DONE | — | — |
| Z9 CLOSE | NOT_DONE | — | -- |

## Notes
- No `docs/openmontage/Z_STATE.md` existed at session start → resuming at Z1 (first phase not DONE).
- Pre-existing uncommitted modifications to `docs/openmontage/slice/*` and `docs/openmontage/slice/artifacts/*` are not mine; I do not commit or claim them.
- KokoroTTSTool (`tools/audio/tts_kaggle.py`) is the existing integration point: Kokoro-82M CPU via `kokoro.KPipeline`, finish_audio, QC on the finished wav.
