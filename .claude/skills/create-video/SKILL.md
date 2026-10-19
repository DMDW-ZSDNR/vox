---
name: create-video
description: |
  [RETIRED 2026-10-31] Legacy HeyGen v1 Video Agent skill. Prompt-to-video with HeyGen now lives in `heygen-video` (v3 `POST /v3/video-agents`). For generic AI video clips use `ai-video-gen` + `video_selector`.
---

# create-video (retired)

HeyGen shut down every v1/v2 endpoint on 2026-10-31 (`Sunset: Sat, 31 Oct 2026`, see https://developers.heygen.com/endpoint-version-comparison). The instructions this skill used to carry no longer work: do not call `api.heygen.com/v1/...`, `api.heygen.com/v2/...` or `upload.heygen.com/v1/asset`.

Use instead:

- `heygen-video` — prompt-to-video with the v3 Video Agent (`heygen video-agent create`).
- `ai-video-gen` + `video_selector` — generic AI clips (Seedance, Veo, Kling, MiniMax...).
- Field-level doubts: `heygen <noun> <verb> --request-schema` or https://developers.heygen.com/llms.txt.
