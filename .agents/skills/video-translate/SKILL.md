---
name: video-translate
description: |
  [RETIRED 2026-10-31] Legacy HeyGen v2 video translation skill. Use `heygen-translate` (v3 `POST /v3/video-translations`).
---

# video-translate (retired)

HeyGen shut down every v1/v2 endpoint on 2026-10-31 (`Sunset: Sat, 31 Oct 2026`, see https://developers.heygen.com/endpoint-version-comparison). The instructions this skill used to carry no longer work: do not call `api.heygen.com/v1/...`, `api.heygen.com/v2/...` or `upload.heygen.com/v1/asset`.

Use instead:

- `heygen-translate` — translation, dubbing and proofreads through v3 and the `heygen` CLI.
- Field-level doubts: `heygen <noun> <verb> --request-schema` or https://developers.heygen.com/llms.txt.
