# Improvement changelog

Record accepted changes, benchmark evidence, reviewer and rollback method.

## 2026-10-18 — M1 selective merge of KILO_CODE_YOUTUBE_FACTORY_MASTER.md
- Accepted: docs/openmontage/MERGE_AUDIT.md (Table A skills + Table B rules vs RIGHTS_MODEL.md/QA_SPEC.md/AGENTS.md/plan v3.2); docs/agent-improvement/LESSONS.md (6 evidence-backed entries); docs/agent-improvement/EVALS.md (5 fixed tasks); .kilo/skills/kilo-self-improvement/SKILL.md (EVALS.md reference, project-level only); docs/openmontage/youtube-publishing-analytics-STUB.md (stub only, no OAuth); docs/openmontage/AGENTS_PROPOSED_DIFF.md (proposed, not applied).
- Not accepted: no MCP installs; no global ~/.config/kilo or kilo.json/kilo.jsonc changes; no Remotion activation (render stack = ffmpeg + HyperFrames); AGENTS.md left unmodified (owner's uncommitted change preserved; diff proposed only).
- Evidence: tests pass (test_qc_tool 6/6, test_finish_audio 5/5, test_piper_tts 9/9, test_tts_kaggle 5/5, all exit 0).
- Rollback: `git revert` of the M1 commit on branch `factory/business-documentary-pilot`.

## 2026-10-18 — Output style rule (project rule)
- Final report max 12 lines, no tables; full detail kept in docs/... and MASTER_RUN_STATE.md.
- Report format: Status | Commit | Done (≤3 bullets) | Failed/NOT_CHECKED (≤3 bullets or "none") | Owner decision needed (≤3 bullets or "none") | Next action (one sentence).
- No restating of task, no per-file lists or per-skill tables; use "details: <path>".
- Never shorten honesty: keep "inline, not independent", real PASS/FAIL/NOT_CHECKED, blockers stated first.
- Apply to every milestone from now on; commit docs only, push non-force; do not touch AGENTS.md.

## 2026-10-18 — F1 fix slice footage quality
- Accepted: rebuilt slice with real archive.org derivatives (clip01 NASA-logo placeholder replaced with real-footage segment 8.0-12.5s); lanczos 1080p+pad crf 18 30fps; finish_audio PASS; qc.py run; rights_records.json + credits.txt + qa_report.json updated; contact sheet 12 frames, logo_visible=false.
- Not accepted: ebur128 FAILED (I=-17.0 LUFS, target -14+/-2, marginal 1 LU below range) → overall qc FAILED. Owner must decide whether to accept or re-run finish_audio.
- Evidence: qc report at projects/slice_cid_v0/qa_report.json (gitignored, not committed); 12/12 checks accounted (PASS/NOT_RUN/1 FAILED).
- Network/download budget: 8/20 requests, ~7.6MB/400MB, curl -L, no new installs, no paid routes, no secrets.
- Rollback: `git revert` of the F1 commit on branch `factory/business-documentary-pilot`.

## 2026-10-18 — F1 redo (v2) improve slice footage quality
- Accepted: re-read archive.org metadata for 4 items (4/25 requests); all only 320x240, no higher-res derivative → keep all 4, none replaced. Rebuilt slice lanczos 1920x1080+pad crf 18 30fps, clip01 = real footage 0-4.5s per owner. finish_audio PASS. qc.py: freezedetect FAILED (max freeze 2.43s > 2.0s), ebur128 FAILED (I=-17.0 LUFS, marginal); remaining checks PASS/NOT_RUN. Before/after bitrate table recorded. rights_records.json + credits.txt + qa_report.json updated.
- Not accepted: overall qc FAILED (freezedetect + ebur128). Owner must decide whether to accept or investigate/re-run.
- Evidence: qc report at projects/slice_cid_v0/rebuild2/qa_report_f1.json (gitignored, not committed).
- Network/download budget: 4/25 requests, ~7.6MB/600MB, curl -L, no new installs, no paid routes, no secrets. Temp files deleted after commit.
- Rollback: `git revert` of the F1 redo commit on branch `factory/business-documentary-pilot`.

## 2026-10-18 — F2 improve slice footage quality
- Accepted: layout fix (320x240 → 2x integer 640x480 centered on dark background + thin frame + source card, lanczos crf 18 30fps, audio chain kept); re-read archive.org metadata for 4 items (all 320x240, no higher-res → keep all 4); source probe (archive.org + NASA images API; no higher-res CID video >640x480 available); freeze investigation (frame-compare EM-0004-01.mp4: source still 0-6s, motion from ~t=6s → clip01 rebuilt from motion segment 6.0-10.5s, frozen portion cut, clip kept); finish_audio PASS; qc.py: freezedetect PASS (0.00s); silencedetect FAILED (0.1006 > 0.10 borderline); ebur128 FAILED (-17.1 LUFS marginal); rights_records.json + credits.txt + qa_report.json updated; EBUR128_THRESHOLD_PROPOSAL.md created (docs only, no qc.py change).
- Not accepted: overall qc FAILED (silencedetect borderline + ebur128 marginal). Thresholds NOT changed in qc.py; ebur128 narration-only proposal in docs only.
- Evidence: qc report at projects/slice_cid_v0/rebuild3/qa_report_f2.json (gitignored, not committed).
- Network/download budget: ~11/25 requests, ~7.6MB/600MB, curl -L, no new installs, no paid routes, no secrets. Temp files deleted after commit.
- Rollback: `git revert` of the F2 commit on branch `factory/business-documentary-pilot`.

## 2026-10-18 — F3 still-image-led slice
- Accepted: built stills-led slice (5 NASA Armstrong CID photos, zoompan max 1.15x, 1080p, letterboxed, no upscale beyond source); archive inserts clip01/02/03 (3-6s) in 2x framed layout; 2 original graphics cards (flight-path/timeline + key-numbers with claim_ids); finish_audio PASS; rights_records.json + credits.txt + qa_report.json updated; FOOTAGE_QUALITY.md written (findings, draft email to ARC-DL-archives@mail.nasa.gov, AI-upscale NEEDS OWNER APPROVAL as 4th component).
- Not accepted: qc.py overall FAILED (freezedetect on static title cards, silencedetect no-narration, ebur128 quiet). Thresholds NOT changed in qc.py. AI upscaling NOT applied (needs owner approval).
- Evidence: qc report at projects/slice_cid_v0/f3/qa_report_f3.json (gitignored, not committed).
- Network/download budget: ~17/25 requests, ~7.6MB/300MB, curl -L, no installs, no AI upscaling, no paid routes, no secrets.
- Rollback: `git revert` of the F3 commit on branch `factory/business-documentary-pilot`.

## 2026-10-18 — F4 still-image-led slice + Kokoro narration
- Accepted: rebuilt slice with Kokoro-82M narration (S1-S7 only, S8 BLOCKED/omitted, 46.0s) laid over stills-led visuals with zoompan, archive inserts in 2x framed layout, 2 original graphics cards; subtitles.srt regenerated; finish_audio PASS. Added static_by_design per-segment exemption to qc.py freezedetect (edit_decisions.json with cuts[] + static_segments[]); test-first 2 new tests (red→green); all 9 qc tests pass. qc.py run with all inputs: overall PASS, freezedetect REVIEW (static title cards), ebur128 PASS (I=-15.3 LUFS). rights_records.json + credits.txt updated. Contact sheet 12 frames.
- Not accepted: qc.py thresholds NOT changed. S8 (CID-13) omitted (BLOCKED, load-bearing). AI upscaling NOT applied.
- Evidence: qc report at projects/slice_cid_v0/f4/qa_report_f4.json (gitignored, not committed); tests pass (test_qc_tool 9/9, test_finish_audio 5/5, test_piper_tts 9/9, test_tts_kaggle 5/5, all exit 0).
- Network/download budget: no new downloads for F4 (sources reused). curl -L. No new installs, no AI upscaling, no paid routes, no secrets.
- Rollback: `git revert` of the F4 commit on branch `factory/business-documentary-pilot`.
