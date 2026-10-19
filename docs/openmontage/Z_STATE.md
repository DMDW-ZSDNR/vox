# MILESTONE Z state — OpenMontage Kilo (space / astronomy niche)

**Branch:** factory/business-documentary-pilot  
**HEAD:** 8e96cda (Milestone K complete; K4 close)  
**Started:** 2026-10-19  
**Disk at start:** /workspaces 7.3 GB free; /tmp 39 GB free (STOP whole run if free disk < 800 MB)  
**Rules:** zero-cost only (unknown/unpriced route = BLOCKED, never free), curl -L for downloads, max 60 network requests per phase, no paid routes, no AI upscaling, no publishing/upload, no secrets printed or committed, never touch `youtube-niche-finder/` or the owner's `.env.example`/`AGENTS.md`. Roles inline, not independent. Venv + weights live outside the repo (/tmp/kilo/*) and are never committed.

## Phase status

| Phase | Status | Evidence | Commit |
|-------|--------|----------|--------|
| Z1 VOICE ENV | DONE | docs/openmontage/Z1_VOICE_ENV.md; venv /tmp/kilo/z1_venv (python3.12.3), kokoro==0.2.2, misaki==0.7.17, torch==2.6.0+cpu, weights in /tmp/kilo/hf_cache; 14.625 s sample synthesized, finish_audio PASS, qc.py decode/loudness/silence/freeze PASS (ffprobe_streams FAILED expected: audio-only) | pending |
| Z2 ARTEMIS DRAFT (3-4 min) | DONE | docs/openmontage/slice/artifacts/* (qa_report PASS, 13 checks: 11 PASS, 1 REVIEW freezedetect=static_by_design cards, 1 NOT_RUN n/a); video projects/slice_artemis_v0/renders/final_artemis_draft.mp4 1920x1080p30 h264/aac 185.43s (gitignored media); NOT_PUBLISHABLE per credits.txt | a7ca003 |
| Z3 ONE-COMMAND PIPELINE | NOT_DONE | — | — |
| Z4 CHAPTER MODE | NOT_DONE | — | — |
| Z5 SERIES PLAN | NOT_DONE | — | — |
| Z6 SCRIPTS | NOT_DONE | — | — |
| Z7 PACKAGING | NOT_DONE | — | — |
| Z8 INDEPENDENT REVIEW PACK | NOT_DONE | — | — |
| Z9 CLOSE | NOT_DONE | — | -- |

## Notes
- No `docs/openmontage/Z_STATE.md` existed at session start → resuming at Z1 (first phase not DONE).
- Pre-existing uncommitted modifications to `docs/openmontage/slice/*` and `docs/openmontage/slice/artifacts/*` are not mine; I do not commit or claim them.
- KokoroTTSTool (`tools/audio/tts_kaggle.py`) is the existing integration point: Kokoro-82M CPU via `kokoro.KPipeline`, finish_audio, QC on the finished wav.
