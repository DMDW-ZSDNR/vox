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
