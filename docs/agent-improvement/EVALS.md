# Evaluation set

Repeat the same tasks before and after any meaningful agent-rule/Skill/MCP change. Record only observed facts. These 5 fixed tasks replace the generic E1-E5 placeholders; record baseline and new result per run.

| ID | Task | Pass criteria | Baseline | New result | Regression? | Notes |
|---|---|---|---|---|---|---|
| E1 | Run `tools/qa/qc.py` on a known-bad MP4 (e.g. truncated/corrupt) | qc.py exits non-zero or emits at least one FAILED/BLOCKED check; never PASS on a corrupt file | — | PASS | No | test_corrupt_file: corrupt MP4 full_decode FAILED/BLOCKED; fail-closed |
| E2 | Run `finish_audio` on clipped audio | Output reaches target loudness (~-14 LUFS integrated) and true peak (>= -1.5 dBTP, no clipping) per QA_SPEC `ebur128` thresholds | — | PASS | No | test_finish_audio: all 5 tests pass |
| E3 | Run TTS tool with Piper `lessac` voice | TTS tool must refuse Piper `lessac` (license gate blocks Piper); falls back to Kokoro or errors, never emits Piper lessac audio | — | PASS | No | test_piper_tts: all 9 tests pass; KokoroTTSTool license gate blocks piper |
| E4 | Run qc.py `claim_ids` check with an unknown claim_id | Check fails: every factual sentence must have a resolvable claim_id; unknown claim_id => FAILED/BLOCKED, 100% not met | — | PASS | No | test_claim_ids_rejects_missing_claim_id: missing/empty claim_id => FAILED |
| E5 | Classify a clip with third-party credit | footage classifier must return `rights_basis == unknown` / REJECT (third-party credit blocks `source_policy_us_gov`); clip NOT USABLE | — | NOT_CHECKED | — | No direct footage-classifier test in fast suite; TTS license-gate analog PASS via test_tts_kaggle |
