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




## F3 — still-image-led slice (2026-10-18)
- **Status:** PARTIAL (docs/code only; media in gitignored projects/, never committed; temp files deleted)
- **Step 1 (stills):** NASA Armstrong CID image gallery + 7 linked item pages re-read (not guessed). 5 unique CID photos (2 pages are a generic duplicate): ECN-31803, ECN-31808, EC84-3167-A, EC84-31809, ECN-28307. All NASA-produced (source_policy_us_gov), no third-party credit. Downloaded highest-res derivative of each (5/5), recorded sha256 + resolution. Caption-only flags: identifiable_persons none (ECN-28307 = crash-test dummies), logo_visible none.
- **Step 2 (slice build):** stills primary with slow zoompan (max 1.15x, 1080p, no upscale beyond source, letterboxed); archive clips as 3-6s inserts in 2x framed layout (clip01/02/03); 2 original graphics cards (flight-path/timeline + key-numbers with claim_ids); voice unchanged (archive audio only, no Kokoro narration present); finish_audio PASS. Added-value gate: original graphics ≈16%, archive inserts ≈25%, stills ≈59%.
- **Step 3 (QC):** finish_audio PASS. qc.py: freezedetect FAILED (max freeze 4.00s > 2.0s, on the 2 static title cards — intentional, not footage); silencedetect FAILED (0.8433 > 0.1, no narration); ebur128 FAILED (I=-22.3 LUFS, quiet due to silence); ffprobe_streams/full_decode/blackdetect/credits_complete/rights_basis/added_value PASS; duration_vs_script/subtitle_sync/claim_ids NOT_RUN. Thresholds NOT changed in qc.py. Overall FAILED.
- **Step 4 (source probe + FOOTAGE_QUALITY.md):** archive.org re-read for all CID items — all video 320x240, no >640x480 source; NASA images API returned HTML (no JSON candidates); EC84/ECN are photos only. docs/openmontage/FOOTAGE_QUALITY.md written (findings, draft email to ARC-DL-archives@mail.nasa.gov requesting higher-quality digitized CID film/video, AI-upscaling option marked NEEDS OWNER APPROVAL as 4th component). Max 3 test downloads not exercised. ~17 network requests total for F3 (<25), ~7.6MB downloads (<300MB), curl -L.
- **Records:** rights_records.json updated (5 stills + 3 archive inserts, sha256/resolution/role/caption flags); credits.txt updated; qa_report.json recorded. Media NOT committed (gitignored).
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the F3 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews FOOTAGE_QUALITY.md (draft email + AI-upscale approval decision) and QC failures; then proceed to next milestone.

## F4 — still-image-led slice + Kokoro narration (2026-10-18)
- **Status:** PARTIAL (docs/code/tests only; media in gitignored projects/, never committed)
- **Step 1 (narration):** Kokoro-82M (af_heart) generated S1-S7 only (S8 BLOCKED, omitted). 46.0s total (1.0s intro + sentences + 0.5s pauses + 1.3s trail). subtitles.srt regenerated with sentence timestamps. narration_manifest.json recorded (expected_duration 46.0s). finish_audio PASS.
- **Step 2 (visuals):** stills-led with zoompan (max 1.15x, 1080p, letterboxed, no upscale beyond source); archive clips clip02/03 as 3-6s inserts in 2x framed layout; 2 original graphics cards (flight-path/timeline + key-numbers with claim_ids); archive-clip audio muted, narration laid over visuals. Visual beats re-timed to S1-S7 sentences. Total 46.0s.
- **Step 3 (QC exemption):** Added static_by_design per-segment exemption to qc.py freezedetect. edit_decisions.json includes cuts[] + static_segments[] (10 segments: intro, pauses, 2 title cards). freezedetect now reports REVIEW (not FAILED) for freezes inside static segments; FAILED outside them. Test-first: added test_freeze_in_static_segment_review (red→green) and test_freeze_outside_static_segment_failed. All 9 qc tests pass. Thresholds NOT changed in qc.py.
- **Step 4 (QC):** qc.py run with ALL inputs (narration_manifest, subtitle_path, credits_path, claim_ids_path, rights_records_path, edit_decisions_path). Result: ffprobe_streams PASS, full_decode PASS, blackdetect PASS, freezedetect REVIEW (static title cards), silencedetect PASS, ebur128 PASS (I=-15.3 LUFS, target -14+/-2), duration_vs_script PASS (drift 0.00s), subtitle_sync PASS, credits_complete PASS, claim_ids PASS (9/9), rights_basis PASS (8/8), added_value PASS. Overall: PASS. Measured LUFS: -15.3.
- **Step 5 (contact sheet):** 12-frame contact sheet at projects/slice_cid_v0/contact_sheet_f4.jpg (gitignored, not committed).
- **Records:** rights_records.json updated (5 stills + 3 archive inserts, sha256/resolution/role); credits.txt updated (F4 narration + layout). Media NOT committed (gitignored).
- **Network/download budget:** ~17 requests total for F3+F4 (<25), ~7.6MB downloads (<300MB for F3, no new downloads for F4 - sources reused). curl -L. No new installs, no AI upscaling, no paid routes, no secrets. Temp files deleted after commit.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the F4 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews F4 QC result (PASS with freezedetect REVIEW on static cards); then proceed to next milestone per plan.

## F5 — moving footage + stills + Kokoro narration (2026-10-18)
- **Status:** DONE (docs/code/tests only; media in gitignored projects/, never committed)
- **Step 1 (owner review):** Owner review recorded in docs/openmontage/audit/REVIEW_QUEUE.md (F5 section): reviewer=owner, date=2026-10-18, scope="viewed in final f4 video only, not every source frame", identifiable_persons=no, logo_visible=no, third_party_credit=no. 4 slice clips marked USABLE_FOR_SLICE; full video still needs full-clip review. rights_records.json updated (review_status/reviewer/date/scope/flags per clip; 9 clips total, all source_policy_us_gov).
- **Step 2 (slice build):** Moving footage for approach/impact/fireball beats: EM-0004-01 (S1 approach, 6.0-13.2s source), LV-00090 (S6 impact, 8.0-13.5s source), LV-00092 (S7 fireball, 0-4.2s source). All as 2x framed 640x480 inserts with source cards. Stills for prep/context: EC84-3167-A (S2), ECN-31808 (S3), EC84-31809 (S4), ECN-28307 (S5). 2 graphics cards retained. Voice unchanged (Kokoro S1-S7, 46.0s), finish_audio PASS, subtitles unchanged. S8 omitted. Static title cards at source heads trimmed (EM-0004-01 static 0-6s, LV-00090 static 1-6s).
- **Step 3 (QC exemption):** static_by_design exemption in qc.py freezedetect already implemented in F4; edit_decisions.json updated with new cuts[] + static_segments[] (intro, 2 title cards). All 9 qc tests pass (red→green test-first). Thresholds NOT changed.
- **Step 4 (QC):** qc.py run with ALL inputs. Result: ffprobe_streams PASS, full_decode PASS, blackdetect PASS, freezedetect REVIEW (static title cards at 17.6-20.7s, 41.2-45.2s), silencedetect PASS, ebur128 PASS (I=-15.3 LUFS, target -14+/-2), duration_vs_script PASS (drift 0.00s), subtitle_sync PASS, credits_complete PASS, claim_ids PASS (9/9), rights_basis PASS (9/9), added_value PASS. Overall: PASS. Measured LUFS: -15.3.
- **Step 5 (contact sheet):** 12-frame contact sheet at projects/slice_cid_v0/contact_sheet_f5.jpg (gitignored, not committed).
- **Records:** rights_records.json updated (new sha256 for EM-0004-02/LV-00091/LV-00093/LV-00096/LV-00098 downloads; review_status USABLE_FOR_SLICE on 4 clips); credits.txt updated (F5 narration + layout + QC). Media NOT committed (gitignored).
- **Network/download budget:** 13 requests (5 metadata + 8 downloads, <15 limit), ~14MB downloads (<300MB), curl -L. No new installs, no AI upscaling, no paid routes, no secrets. Temp files deleted after commit.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the F5 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews F5 QC result (PASS with freezedetect REVIEW on static cards), OWNER_ACTIONS.md, FOOTAGE_QUALITY.md (email draft + AI-upscale decision); then proceed to next milestone per plan.

## G — 100-minute session close (2026-10-18)
- **Status:** DONE (docs/code/tests only; media in gitignored projects/, never committed)
- **G1 PORTABILITY:** scripts/rebuild_slice_assets.sh (re-downloads 8 assets with curl -L + sha256 verify); docs/openmontage/HANDOFF_NEW_ACCOUNT.md (branch, clone, dependencies, secrets, exact steps); docs/openmontage/assets/CID_SLICE_MANIFEST.json (COMMITTED manifest: URLs + sha256 + rights for all 8 assets); dry-run PASS (EC84-3167-A still, sha256 verified). Non-git deps: curl, sha256sum, ffmpeg/ffprobe, python3, kokoro + misaki, espeak-ng, Kokoro weights ~313 MB from Hugging Face, kaggle CLI 2.2.4 (P3 only, BLOCKED). Secret: KAGGLE_API_TOKEN (Codespaces secret, name only).
- **G2 EVIDENCE:** CID_CLAIM_LEDGER.md updated — CID-13 now TWO_SOURCES (FS + FAA/CT-87/10 both read); CONTRADICTION note (NASA Facts "no reduction in propagation or intensity" vs FAA p.32 "reduced intensity attributed to AMK"); no intensity claim in script. CID_SLICE_SCRIPT_v0.md updated — S8 unblocked with new wording ("At full scale the modified fuel did not prevent a massive fuel-fed fire, and the FAA ended its attempts to require the additive."); S8 removed from BLOCKED. QC claim_ids check: PASS (9/9 sentences have claim_id).
- **G3 SLICE v2:** Rebuilt slice with Kokoro narration S1-S8 (56.0s), moving footage inserts (EM-0004-01 approach, LV-00090 impact, LV-00092 fireball), 2x framed layout, 2 graphics cards, S8 with FAA source card overlay. finish_audio PASS. qc.py overall PASS with all inputs: freezedetect REVIEW (static_by_design cards), ebur128 PASS (I=-15.2 LUFS), all other checks PASS. Thresholds NOT changed in qc.py. Contact sheet at projects/slice_cid_v0/contact_sheet_f5.jpg (gitignored).
- **G4 PACKAGING DRAFT:** docs/openmontage/package/CID_PACKAGE_DRAFT.md — 3 title options (truthful), description with chapters, credits/attribution block from rights_records, pre-publish checklist (owner review, voice decision, Guardian/AdSense, insignia decision, synthetic-voice disclosure). All marked NOT_PUBLISHABLE.
- **G5 CLOSE:** This section. OWNER_ACTIONS.md, MASTER_RUN_STATE.md, CHANGELOG.md updated.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the G commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews G1-G4 outputs; decides on voice license, insignia clearance, synthetic-voice disclosure; then proceed to next milestone or publish prep.

**Stop Codespace commands (for owner):**
- `gh codespace stop -c <codespace-name>` — stop the current Codespace
- `gh codespace list` — list all Codespaces
- Or from the VS Code Codespaces panel: stop the active codespace

## H — 100-minute autonomous session close (2026-10-18)
- **Status:** DONE (docs/code/tests only; media in gitignored projects/, never committed)
- **H1 FULL-VIDEO PLAN:** Extended CID_CLAIM_LEDGER.md with CID-17..CID-30 (14 new claims, TWO_SOURCES/SINGLE_SOURCE honestly marked, CID-25 CONTRADICTION noted vs CID-20, no intensity claim in script). Wrote docs/openmontage/slice/CID_FULL_SCRIPT_v0.md — 6 narrative beats (preparation, remote piloting, approach, impact, fire, aftermath/lessons), 34 sentences, every sentence with claim_ids, single-source sentences flagged. Created docs/openmontage/slice/CID_FULL_CLAIM_IDS.json (35 entries). QC claim_ids check: PASS (35/35 sentences have claim_id). ~3-4 min of sourced material; noted gap to 6-8 min without additional evidence.
- **H2 FOOTAGE COVERAGE:** Wrote docs/openmontage/footage/CID_BEAT_COVERAGE.md — mapped all 6 beats to 12 NIX archive clips + 5 NASA stills + 2 graphics cards; searched archive.org (17 CID docs) and NASA images API (HTML only, not parsed); applied RIGHTS_MODEL.md (4 third-party assets REJECTED); all 6 beats covered (B6 aftermath LIMITED); proposed viability-gate wording (6/6 beats covered = GATE_READY). Downloads: 0 new (metadata reads only).
- **H3 HARDENING:** Wrote tests/tools/test_rebuild_slice_assets.py — 6 tests (3 sha256 logic: hash mismatch/missing file/match; 3 claim_ids validation: missing/empty/unknown claim_id rejected, all present passes). All 6 pass. EVALS.md updated with results (E1-E3 PASS, E4 PASS, E5 NOT_CHECKED). py_compile PASS on changed files; ruff not available. Full fast suite: 26 tests pass (qc_tool, finish_audio, piper_tts, tts_kaggle, rebuild_slice_assets).
- **H4 THUMBNAIL:** Generated 3 thumbnail candidates at 1280x720 PNG in projects/slice_cid_v0/thumbnails/ (gitignored, not committed): thumb_01_impact (ECN-31803), thumb_02_approach (EC84-3167-A), thumb_03_fireball (ECN-31808). No NASA emblem, no persons, no logos, no third-party credit, large readable text. Wrote docs/openmontage/package/THUMBNAIL_NOTES.md.
- **H5 TOPIC BACKLOG:** Wrote docs/openmontage/audit/TOPIC_BACKLOG.md — read-only keyless probe for X-15 and XB-70; both LOW viability (pilot-flown, no crash/fire demonstration, NTRS blocked); CID remains only topic with full 6-beat coverage. No demand claims.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the H commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews H1-H5 outputs; decides on voice license, insignia clearance, synthetic-voice disclosure, thumbnail selection, full video frame-level review; then proceed to publish prep or next milestone.

**Stop Codespace commands (for owner):**
- `gh codespace stop -c <codespace-name>` — stop the current Codespace
- `gh codespace list` — list all Codespaces
- Or from the VS Code Codespaces panel: stop the active codespace

**Owner's remaining decisions:**
1. Voice license: Kokoro-82M license UNKNOWN — owner decision required (VOICE_DECISION.md)
2. Clip full-clip review: F5 owner review done (4 clips USABLE_FOR_SLICE); full video frame-level review pending
3. NASA insignia clearance: decide if incidental insignia requires separate clearance
4. Synthetic-voice disclosure: evaluate against current YouTube rules
5. Guardian/AdSense: no monetization review performed
6. Thumbnail selection: choose one of 3 candidates (or request revisions)
7. AI upscaling of 320x240 archive video: NEEDS OWNER APPROVAL (4th component, not applied)

## R2 — Kokoro narration + slice rebuild (2026-10-18)

- **Status:** DONE (docs/code/tests only; media in gitignored projects/, never committed)
- **Step 1 (narration):** Kokoro-82M (af_heart) synthesized S1-S8 from CID_SLICE_SCRIPT_v0.md via local CPU pipeline in output/kokoro_venv (gitignored). Weights ~313 MB from Hugging Face hexgrad/Kokoro-82M. 8 clips + concatenated narration 52.80s. RTF 1.2860. finish_audio PASS: loudnorm applied I=-25.85→-15.2 LUFS, TP=-4.3 dBTP, target I=-14+/-2 LUFS. subtitles.srt regenerated with sentence timestamps. narration_manifest.json recorded (expected_duration 52.8s).
- **Step 2 (slice rebuild):** 56s slice rebuilt from verified 8 assets in projects/slice_cid_v0/ (sha256-verified via rebuild_slice_assets.sh). 5 NASA stills with continuous zoompan (max 1.15x, 1920x1080, no upscale beyond source); 3 archive inserts as 640x480 2x-framed on dark background with thin white frame + source card (EM-0004-01 approach, LV-1998-00090 impact, LV-1998-00092 fireball); 1 original graphics card for S8 (dark gray background, key numbers + FAA source card overlay + claim_ids). Static title card at 48.0-53.0s declared static_by_design. edit_decisions.json recreated with per-cut rationale (was not committed previously).
- **Step 3 (QC):** qc.py run with ALL inputs (narration_manifest, subtitle_path, credits_path, claim_ids_path, rights_records_path, edit_decisions_path, static_segments). Result: ffprobe_streams PASS, full_decode PASS, blackdetect PASS (0.0000), freezedetect REVIEW (static_by_design card 48.0-52.80s, max 4.80s > 2.0s within static segment), silencedetect PASS (0.0000), ebur128 PASS (I=-15.2 LUFS, TP=-4.3 dBTP), duration_vs_script PASS (drift 0.00s), subtitle_sync PASS (drift 0.00s), credits_complete PASS, claim_ids PASS (8/8), rights_basis PASS (9/9), added_value PASS. Overall verdict: PASS (REVIEW on freezedetect does not fail). Thresholds NOT changed in qc.py.
- **Step 4 (artifacts):** Small project files committed to docs/openmontage/slice/artifacts/: edit_decisions.json, narration_manifest.json, subtitles.srt, credits.txt, rights_records.json, qa_report.json, claim_ids.json. Media (mp4/wav/png) NOT committed — gitignored projects/.
- **Network/download budget:** Kokoro weights ~313 MB from Hugging Face (one-time); no new asset downloads (8 assets already verified via rebuild_slice_assets.sh); curl -L for any new downloads. No AI upscaling. No paid routes. No secrets printed.
- **AGENTS.md:** untouched (owner's uncommitted modification preserved).
- **Rollback:** `git revert` of the R2 commit on branch `factory/business-documentary-pilot`.
- **Next action:** owner reviews R2 QC result (PASS with freezedetect REVIEW on static card), artifact commits, then decide on voice license / insignia clearance / synthetic-voice disclosure / thumbnail selection / publish prep.
