---
name: ai-video-gen
description: |
  Generate AI videos from text prompts using multiple provider gateways. Use when: (1) Generating videos from text descriptions, (2) Creating AI-generated video clips for content production, (3) Image-to-video generation with a reference image, (4) Choosing between video generation providers (VEO, Kling, Sora, Runway, Seedance, MiniMax, Gemini Omni). Supports gateways: fal.ai API, Kling official direct API, and the Gemini API (Gemini Omni Flash).
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env_any:
        - FAL_KEY
        - KLING_API_KEY
        - GEMINI_API_KEY
        - GOOGLE_API_KEY
---

# Video Generation (Multi-Gateway)

Generate AI videos from text prompts. Supports multiple providers via three API paths:

| Gateway | Env Variable | Providers | Tool |
|---------|-------------|-----------|------|
| **fal.ai** | `FAL_KEY` | **Seedance 2.0** (standard + fast), Kling v3/v2.1, MiniMax, VEO | `seedance_video`, `kling_video`, `minimax_video`, `veo_video` |
| **Kling Official** | `KLING_API_KEY` | Kling official Classic, Turbo, and basic Omni video | `kling_official_video` |
| **Gemini API** | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Gemini Omni Flash (generation + conversational editing) | `gemini_omni_video` |

**Iterative editing — Gemini Omni.** When the brief calls for *refining an existing clip* (add/remove objects, restyle, change lighting or on-screen text) rather than regenerating, Gemini Omni Flash is the only provider in the fleet with stateful multi-turn editing. See Layer 3 `gemini-omni` for the authoritative prompting guide (reference-image tags, timecode syntax, edit-prompt rules) before writing any prompt for it.

**Preferred premium default — Seedance 2.0.** When any premium gateway is configured (`FAL_KEY` → `seedance_video`), Seedance 2.0 is the preferred default for cinematic, trailer, and high-fidelity clip work. It is the only model in the fleet with **single-pass native synchronized audio, multi-shot generation, director-level camera control, and lip-sync from quoted dialogue**, and it ranks #1 on Artificial Analysis Elo as of early 2026. Switch off it only when the user has a specific reason (budget, provider preference, stylistic fit like VEO for photoreal landscape or Kling for specific anime look). See Layer 3 `seedance-2-0` for the authoritative prompting and parameter guide.

**IMPORTANT:** Always use `video_selector` instead of calling provider tools directly. The selector handles availability checks, cost comparison, and automatic fallback, and its scoring engine already biases toward Seedance 2.0 for cinematic intent.

## Authentication

Use whichever configured gateway best matches the user's available providers and cost/quality goals.

- **fal.ai:** Set `FAL_KEY` to access Kling, MiniMax, and Veo through fal.ai.
- **Kling Official:** Set `KLING_API_KEY` to access Kling's official direct API via `provider="kling_official"`.
- **Gemini API:** Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to access Gemini Omni video generation and conversational editing.

Do not describe any gateway as the default or top choice without checking the registry and current task fit first.

fal.ai Kling (`kling_video`, `provider="kling"`) and Kling Official (`kling_official_video`, `provider="kling_official"`) are different paths. Do not reuse fal.ai queue URLs, `FAL_KEY`, or image upload behavior when the official provider is selected.

## HeyGen gateway (retired)

The HeyGen multi-model gateway (`POST /v1/workflows/executions`, `GenerateVideoNode`) was removed on 2026-10-31 with no v3 replacement, so the `heygen_video` tool reports itself unavailable. Reach Veo, Kling, Sora, Runway and Seedance through their own tools via `video_selector`. HeyGen presenter videos live in `heygen-video` (v3).

## Best Practices

1. **Be descriptive in prompts** — include camera movement, lighting, style, and mood details
2. **Default to Seedance 2.0 (via `seedance_video`) for cinematic and motion-led work** when `FAL_KEY` is set — single-pass synced audio, multi-shot, lip-sync, director-level camera. Use VEO 3.1 / Sora V2 Pro when the user specifically wants Google or OpenAI motion character; use `ltx_distilled` or `veo3_fast` only when speed is the hard constraint
3. **Use reference images** for image-to-video generation — great for animating product photos or still images
4. **Video generation is the slowest workflow** — allow up to 5 minutes, poll every 10 seconds
5. **Aspect ratio matters** — use `9:16` for social media stories/reels, `16:9` for landscape, `1:1` for square
6. **Output URLs are temporary** — download or save generated videos promptly
