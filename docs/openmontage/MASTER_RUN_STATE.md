# MASTER RUN State — OpenMontage (2026-10-17)

**HEAD at start:** 21903ee (factory/business-documentary-pilot)
**Preflight:** git clean-ish (AGENTS.md modified by user — preserved), disk 3.4 GB free, KAGGLE_API_TOKEN set (length 37), kaggle auth OK (exit 0)

## Phase status
| Phase | Status | Evidence | Commit hash |
|---|---|---|---|
| P1 Voice license evidence | DONE | docs/openmontage/VOICE_BAKEOFF_LICENSES.md (Chatterbox MIT/MIT, Maya1 Apache2/Apache2, Kokoro-82M Apache2/Apache2 all PASS; ASR faster-whisper MIT + openai-whisper MIT; weights not separately licensed) | 94c789d |
| P2 Evidence ledger + script | DONE | docs/openmontage/evidence/CID_CLAIM_LEDGER.md (16 claims), docs/openmontage/slice/CID_SLICE_SCRIPT_v0.md (8 sentences, DRAFT/NOT_PUBLISHABLE, S8 BLOCKED), docs/openmontage/slice/CID_SLICE_CLAIM_IDS.json; QC claim_ids check PASS (9/9 with claim_id); NASA Facts PDF fetched -> FS claims AGENT_VERIFIED_TEXT | 9bf1605 |
| P3 Kaggle voice bake-off | BLOCKED | Kaggle GPU job forts845/of-bridge-runner pushed OK (enable_gpu=true, enable_internet=true) but stayed KernelWorkerStatus.QUEUED for 15+ min poll window, never reached RUNNING/COMPLETE => total-timeout BLOCKED. Blocker: GPU/internet provisioning (GPU quota exhausted or enable_internet requires phone verification). Owner action: verify phone number in Kaggle settings / check GPU quota; 1 retry attempt remains (max 2). | — |
| P4 TTS integration | DONE | tools/audio/tts_kaggle.py (KokoroTTSTool: license gate blocks piper, bridge+BLOCKED→local Kokoro fallback, finish_audio+QC verify), config/voice.json, tests/tools/test_tts_kaggle.py (5 pass); P3 BLOCKED so Kokoro CPU fallback used; py_compile OK | fafc238 |
| P5 Footage source registry | DONE | docs/openmontage/footage/SOURCE_REGISTRY.md (probe results for NASA/IA/Wikimedia/LoC/NARA/DVIDS; MISSING adapters: NASA SVS, DVIDS, Open Beelden, Europeana, Smithsonian, NPS, CDC, Vimeo CC, Videezy); all 16 existing adapters verified via auto-discovery (12 available, 4 key-required unavailable) | 7c41da6 |
| P6 Technical slice ~50s | DONE | 4 CID clips from archive.org NIX (all source_policy_us_gov, no third-party credit per RIGHTS_MODEL.md); final slice 48.93s at 1920x1080 30fps h264/aac in projects/slice_cid_v0/ (gitignored); QC qa_report.json ALL PASS (12/12 checks); EDL with per-cut rationale; credits.txt; subtitles.srt; contact_sheet.jpg; NOT_PUBLISHABLE (unreviewed flags, single-source claims, voice owner sign-off, S8 blocked) | 501585b |
| P7 Global check | DONE | docs/openmontage/GLOBAL_CHECK_2026-10-17.md (all phases, tests, QC summary, repo hygiene, open gates); docs/openmontage/OWNER_ACTIONS.md (numbered owner steps); 32 tests passed | — |
| P7 Global check | PENDING | — | — |

## Rules observed
- KAGGLE_API_TOKEN: never printed/logged/committed/passed on CLI; env check yes/no only
- Network: kaggle CLI/bridge, images-api.nasa.gov, nasa.gov, archive.org (curl -L), official license pages, HF/GitHub/PyPI LICENSE pages. NTRS blocked — do not retry
- Downloads only into gitignored projects/ or /tmp, never committed; delete temp files
- Disk < 800 MB free → write state and STOP whole run
- ERROR/HTTP/EMPTY separate states; fail-closed; unmeasured = BLOCKED or NOT_RUN
- Code test-first (red then green); run new + existing tests; report exact commands/exit codes
- Roles inline; never claim unobserved work

## M1 — selective merge of KILO_CODE_YOUTUBE_FACTORY_MASTER.md (2026-10-18)
- **Status:** COMPLETE (docs + project-level skills only)
- **HEAD:** `8bc5f7b` (factory/business-documentary-pilot)
- **Master file:** located in git commit `36e6595` (1782 lines), not in working tree; treated as reference only — no bootstrap, no install scripts, no vertical slice.
- **Skills:** all 9 master skills already installed in `.kilo/skills/` with matching name/description; `kilo-self-improvement` adapted to reference `docs/agent-improvement/EVALS.md` (project-level only, no global writes); remaining 8 SKIP (duplicates); `youtube-publishing-analytics` stub-only in `docs/openmontage/` (no OAuth).
- **Rules audit:** `docs/openmontage/MERGE_AUDIT.md` written (Table A skills + Table B rules). 4 conflicts flagged: Remotion vs HyperFrames (HyperFrames wins); extra MCPs vs max-3-runtime+zero-secrets (none installed); global AGENTS/skill paths vs project-level (none written); master `NOT_CHECKED` vs QA_SPEC `PASS\|REVIEW\|BLOCKED\|FAILED` (mapped, our statuses kept).
- **Templates:** `docs/agent-improvement/LESSONS.md` seeded with 6 entries; `EVALS.md` seeded with 5 fixed tasks; `BACKLOG.md`/`CHANGELOG.md` preserved (merge, never overwrite); CHANGELOG M1 entry added.
- **Verification:** `tests/tools/test_qc_tool.py` 6/6 exit 0; `test_finish_audio.py` 5/5 exit 0; `test_piper_tts.py` 9/9 exit 0; `test_tts_kaggle.py` 5/5 exit 0; `kilo --help` has no `skills` subcommand → discovery NOT_CHECKED.
- **AGENTS.md:** owner's uncommitted modification preserved exactly (backed up to `/tmp/AGENTS.md.bak-20261018-013214`); proposed additive rules block in `docs/openmontage/AGENTS_PROPOSED_DIFF.md` (not applied).
- **Rollback:** `git revert` of the M1 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews MERGE_AUDIT.md Table B conflicts and AGENTS_PROPOSED_DIFF.md; decides on MCP/tool and global-path conflicts.

## F1 — fix slice footage quality (2026-10-18)
- **Status:** SUPERSEDED by F2. Media in gitignored projects/, never committed.

## F2 — improve slice footage quality (2026-10-18)
- **Status:** PARTIAL (docs/code only; media in gitignored projects/, never committed; temp files deleted)
- **Diagnosis:** ffprobe 4 clips — all 1920x1080 upscaled from 320x240 archive.org sources. clip01→NIX-EM-0004-01, clip02→NIX-LV-1998-00090, clip03→NIX-LV-1998-00092, clip04→NIX-LV-1998-00098 (per edit_decisions.json). Owner confirmed real footage; clip01 NOT treated as placeholder.
- **Layout fix:** each 320x240 source scaled 2x integer to 640x480 (lanczos), centered on dark solid background (1920x1080), thin white frame, on-screen source card (asset id + center + rights_basis). No stretch. crf 18, 30fps, h264/aac. Audio chain kept (PCM/WAV per source; archive.org AAC malformed).
- **Step 2:** re-read archive.org metadata for all 4 items (4 requests, curl -L). Best = h.264 mp4, all only 320x240, no higher-res → keep all 4, none replaced. Recorded name/size/res/sha256 per clip.
- **Step 3 (higher-quality probe):** archive.org advancedsearch found additional CID items (NIX-ECN-*, NIX-EC84-*, NIX-EM-0004-02) but EC84/ECN are photos only and NIX-EM-0004-02 is 320x240. NASA images API returned web-app HTML (no JSON candidates). No higher-resolution (>640x480) CID video source available. Max 3 test downloads not needed (none downloaded for probe). ~7.6MB total downloads.
- **QC investigation (freeze):** frame-compare of EM-0004-01.mp4 showed source still (static NASA logo + title card) 0-6s, real motion from ~t=6s. Per task "if source still, trim/cut around it": clip01 rebuilt from motion segment t=6.0-10.5s (4.5s), frozen 0-6s cut; clip kept, not rejected. freezedetect now PASS (max freeze 0.00s <= 2.0s).
- **Thresholds:** NOT changed in qc.py. Proposed ebur128 narration-only band (-16 +/- 2 LUFS) in docs only: docs/openmontage/EBUR128_THRESHOLD_PROPOSAL.md (reason: narration-only, no music, -17.1 LUFS marginal ~1 LU below -16 band; QA_SPEC docstring already notes -16..-14 may be acceptable for narration-first).
- **QC result (final_f2.mp4):** ffprobe_streams PASS, full_decode PASS, blackdetect PASS, freezedetect PASS (0.00s), silencedetect FAILED (silence ratio 0.1006 > 0.10, borderline; clip01 silent), ebur128 FAILED (I=-17.1 LUFS, target -14+/-2, marginal); credits_complete PASS, rights_basis PASS (4/4), added_value PASS; duration_vs_script/subtitle_sync/claim_ids NOT_RUN. Overall FAILED.
- **Before/after bitrate:** clip01 480k→724k, clip02 1.94M→4.45M, clip03 1.62M→3.76M, clip04 1.87M→4.17M (all 1920x1080).
- **Records:** rights_records.json updated (clip01 used_segment 6.0-10.5s + freeze-trim note); credits.txt updated (layout + QC + probe notes); qa_report.json recorded. Media NOT committed (gitignored).
- **Network/download budget:** ~11 requests (<25), ~7.6MB downloads (<600MB), curl -L. No new installs, no paid routes, no secrets. Temp files (/tmp/f2, rebuild3) deleted after commit.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the F2 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner decides on ebur128 narration-only threshold proposal and borderline silencedetect; then proceed to next milestone.



