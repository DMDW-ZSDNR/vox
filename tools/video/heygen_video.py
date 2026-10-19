"""HeyGen-backed cloud video generation (retired).

HeyGen removed the v1 Workflows API (`POST /v1/workflows/executions`,
`GenerateVideoNode`) on 2026-10-31 and v3 has no replacement, so this tool
always reports itself unavailable. HeyGen avatar videos live in
`tools/avatar/heygen_avatar.py` (v3).
"""

from __future__ import annotations

from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)
from tools.video._shared import HEYGEN_PROVIDERS, estimate_quality_cost, estimate_speed_runtime


class HeyGenVideo(BaseTool):
    name = "heygen_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "heygen"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    install_instructions = (
        "Retired: HeyGen shut down the v1 Workflows API on 2026-10-31 with no v3 "
        "replacement. Use video_selector with another provider."
    )
    fallback = "wan_video"
    fallback_tools = ["wan_video", "hunyuan_video", "ltx_video_local", "cogvideo_video", "ltx_video_modal", "image_selector"]
    agent_skills = ["ai-video-gen", "create-video"]

    capabilities = ["text_to_video", "image_to_video", "provider_selection"]
    supports = {
        "reference_image": True,
        "offline": False,
        "native_audio": False,
        "cloud_generation": True,
    }
    best_for = [
        "premium cloud video generation without local GPU setup",
        "fast access to VEO, Sora, Kling, Runway, and Seedance providers",
    ]
    not_good_for = [
        "offline or privacy-constrained rendering",
        "free local-first production",
    ]
    provider_matrix = {
        key: {"tool": "heygen_video", **value, "mode": "api"} for key, value in HEYGEN_PROVIDERS.items()
    }

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video"],
                "default": "text_to_video",
            },
            "provider_variant": {
                "type": "string",
                "enum": sorted(HEYGEN_PROVIDERS),
                "default": "veo_3_1",
            },
            "reference_image_url": {"type": "string"},
            "reference_image_path": {"type": "string"},
            "aspect_ratio": {
                "type": "string",
                "enum": ["16:9", "9:16", "1:1"],
                "default": "16:9",
            },
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True)
    retry_policy = RetryPolicy(max_retries=2, backoff_seconds=10.0, retryable_errors=["rate_limit", "timeout", "server_error"])
    idempotency_key_fields = ["prompt", "provider_variant", "aspect_ratio"]
    side_effects = ["writes video file to output_path", "calls HeyGen API"]
    user_visible_verification = ["Watch generated clip for motion quality and prompt adherence"]

    def get_status(self) -> ToolStatus:
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        meta = HEYGEN_PROVIDERS.get(inputs.get("provider_variant", "veo_3_1"), HEYGEN_PROVIDERS["veo_3_1"])
        return estimate_quality_cost(meta["quality"])

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        meta = HEYGEN_PROVIDERS.get(inputs.get("provider_variant", "veo_3_1"), HEYGEN_PROVIDERS["veo_3_1"])
        return estimate_speed_runtime(meta["speed"])

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(success=False, error=self.install_instructions)
