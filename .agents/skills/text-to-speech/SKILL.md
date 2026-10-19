---
name: text-to-speech
description: |
  [RETIRED 2026-10-31] Legacy HeyGen v1 Starfish TTS skill. HeyGen TTS is now `heygen voice speech` (v3 `POST /v3/voices/speech`, voices from `GET /v3/voices?engine=starfish`). Other TTS providers keep their own skills.
---

# text-to-speech (retired)

HeyGen shut down every v1/v2 endpoint on 2026-10-31 (`Sunset: Sat, 31 Oct 2026`, see https://developers.heygen.com/endpoint-version-comparison). The instructions this skill used to carry no longer work: do not call `api.heygen.com/v1/...`, `api.heygen.com/v2/...` or `upload.heygen.com/v1/asset`.

Use instead:

- HeyGen Starfish TTS: `heygen voice speech` / `POST /v3/voices/speech`; voices from `heygen voice list` (`GET /v3/voices?engine=starfish`). Ready-made script: `.agents/skills/hyperframes-media/scripts/heygen-tts.mjs`.
- Other providers: `elevenlabs`, `azure-text-to-speech`, `fish-audio-tts`, `doubao-tts`, `dashscope`, `minimax-h3` and the `tts_selector` tool.
- Field-level doubts: `heygen <noun> <verb> --request-schema` or https://developers.heygen.com/llms.txt.
