# Evaluation set

Repeat the same tasks before and after any meaningful agent-rule/Skill/MCP change. Record only observed facts. These 5 fixed tasks replace the generic E1-E5 placeholders; record baseline and new result per run.

| ID | Task | Pass criteria | Baseline | New result | Regression? | Notes |
|---|---|---|---|---|---|---|
| E1 | Run `tools/qa/qc.py` on a known-bad MP4 (e.g. truncated/corrupt) | qc.py exits non-zero or emits at least one FAILED/BLOCKED check; never PASS on a corrupt file | | | | Fail-closed: unable to run => BLOCKED |
| E2 | Run `finish_audio` on clipped audio | Output reaches target loudness (~-14 LUFS integrated) and true peak (>= -1.5 dBTP, no clipping) per QA_SPEC `ebur128` thresholds | | | | `finish_audio` must not normalize clipped audio above true-peak max |
| E3 | Run TTS tool with Piper `lessac` voice | TTS tool must refuse Piper `lessac` (license gate blocks Piper); falls back to Kokoro or errors, never emits Piper lessac audio | | | | KokoroTTSTool license gate blocks piper (P4 TTS integration) |
| E4 | Run qc.py `claim_ids` check with an unknown claim_id | Check fails: every factual sentence must have a resolvable claim_id; unknown claim_id => FAILED/BLOCKED, 100% not met | | | | `claim_ids` requires resolvable claim_id per factual sentence |
| E5 | Classify a clip with third-party credit | footage classifier must return `rights_basis == unknown` / REJECT (third-party credit blocks `source_policy_us_gov`); clip NOT USABLE | | | | Fail-closed: any third-party credit => unknown => REJECT |
