# Improvement changelog

Record accepted changes, benchmark evidence, reviewer and rollback method.

## 2026-10-18 — M1 selective merge of KILO_CODE_YOUTUBE_FACTORY_MASTER.md
- Accepted: docs/openmontage/MERGE_AUDIT.md (Table A skills + Table B rules vs RIGHTS_MODEL.md/QA_SPEC.md/AGENTS.md/plan v3.2); docs/agent-improvement/LESSONS.md (6 evidence-backed entries); docs/agent-improvement/EVALS.md (5 fixed tasks); .kilo/skills/kilo-self-improvement/SKILL.md (EVALS.md reference, project-level only); docs/openmontage/youtube-publishing-analytics-STUB.md (stub only, no OAuth); docs/openmontage/AGENTS_PROPOSED_DIFF.md (proposed, not applied).
- Not accepted: no MCP installs; no global ~/.config/kilo or kilo.json/kilo.jsonc changes; no Remotion activation (render stack = ffmpeg + HyperFrames); AGENTS.md left unmodified (owner's uncommitted change preserved; diff proposed only).
- Evidence: tests pass (test_qc_tool 6/6, test_finish_audio 5/5, test_piper_tts 9/9, test_tts_kaggle 5/5, all exit 0).
- Rollback: `git revert` of the M1 commit on branch `factory/business-documentary-pilot`.
