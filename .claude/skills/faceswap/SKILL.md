---
name: faceswap
description: |
  [RETIRED 2026-10-31] Retired HeyGen face swap skill. It ran on the v1 Workflows API, which HeyGen removed on 2026-10-31 with no v3 replacement. HeyGen face swap is not available through the API.
---

# faceswap (retired)

HeyGen shut down every v1/v2 endpoint on 2026-10-31 (`Sunset: Sat, 31 Oct 2026`, see https://developers.heygen.com/endpoint-version-comparison). The instructions this skill used to carry no longer work: do not call `api.heygen.com/v1/...`, `api.heygen.com/v2/...` or `upload.heygen.com/v1/asset`.

Use instead:

- No HeyGen v3 replacement exists. Pick another provider explicitly with the user.
- Field-level doubts: `heygen <noun> <verb> --request-schema` or https://developers.heygen.com/llms.txt.
