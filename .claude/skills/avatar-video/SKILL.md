---
name: avatar-video
description: |
  [RETIRED 2026-10-31] Legacy HeyGen v2 avatar-video skill. For HeyGen avatar videos use `heygen-video` (v3); to create an avatar identity use `heygen-avatar`; inside OpenMontage pipelines use the `heygen_avatar` tool. Non-HeyGen avatar tools (Kling) keep their own skills.
---

# avatar-video (retired)

HeyGen shut down every v1/v2 endpoint on 2026-10-31 (`Sunset: Sat, 31 Oct 2026`, see https://developers.heygen.com/endpoint-version-comparison). The instructions this skill used to carry no longer work: do not call `api.heygen.com/v1/...`, `api.heygen.com/v2/...` or `upload.heygen.com/v1/asset`.

Use instead:

- `heygen-video` — presenter videos through the v3 Video Agent and the `heygen` CLI.
- `heygen-avatar` — create or reuse an avatar identity (digital twin, photo avatar).
- `heygen_avatar` tool (`tools/avatar/heygen_avatar.py`) — Avatar V through `POST /v3/videos`
  inside OpenMontage pipelines.
- Kling avatar / lip-sync: `kling-official`.
- Field-level doubts: `heygen <noun> <verb> --request-schema` or https://developers.heygen.com/llms.txt.
