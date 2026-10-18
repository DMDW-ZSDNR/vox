"""Tests for local_diffusion's pipeline loading: AutoPipeline (SD 1.x/2.x and SDXL),
fp16 variant with fallback on CUDA, CPU offload, and the per-model pipeline cache.
diffusers/torch are faked, so no weights are downloaded and no GPU is needed."""

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.graphics import local_diffusion
from tools.graphics.local_diffusion import LocalDiffusion


def _fake_torch(cuda: bool):
    torch = types.ModuleType("torch")
    torch.cuda = types.SimpleNamespace(is_available=lambda: cuda)
    torch.float16 = "float16"
    torch.float32 = "float32"
    torch.Generator = MagicMock()
    return torch


def _fake_pipe(tmp_path: Path):
    pipe = MagicMock(name="pipe")
    image = MagicMock(name="image")
    image.save.side_effect = lambda p: Path(p).write_bytes(b"\x89PNG")
    pipe.return_value.images = [image]
    pipe.to.return_value = pipe
    return pipe


@pytest.fixture
def fakes(monkeypatch, tmp_path):
    """Install fake torch/diffusers modules; returns (auto_pipeline_class, pipe)."""
    local_diffusion._PIPELINE_CACHE.clear()
    pipe = _fake_pipe(tmp_path)
    auto = MagicMock(name="AutoPipelineForText2Image")
    auto.from_pretrained.return_value = pipe
    diffusers = types.ModuleType("diffusers")
    diffusers.AutoPipelineForText2Image = auto
    monkeypatch.setitem(sys.modules, "diffusers", diffusers)

    def use_cuda(flag: bool):
        monkeypatch.setitem(sys.modules, "torch", _fake_torch(flag))

    use_cuda(False)
    yield types.SimpleNamespace(auto=auto, pipe=pipe, use_cuda=use_cuda, out=tmp_path)
    local_diffusion._PIPELINE_CACHE.clear()


def _run(fakes, **over):
    inputs = {"prompt": "a red fox", "output_path": str(fakes.out / "img.png"),
              "model": "stabilityai/stable-diffusion-xl-base-1.0", **over}
    return LocalDiffusion().execute(inputs)


def test_cpu_loads_fp32_moves_to_cpu_and_writes_image(fakes):
    res = _run(fakes, seed=7)
    assert res.success, res.error
    fakes.auto.from_pretrained.assert_called_once_with(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype="float32")
    fakes.pipe.to.assert_called_once_with("cpu")
    fakes.pipe.enable_model_cpu_offload.assert_not_called()
    assert Path(res.data["output"]).is_file()
    assert res.model == "stabilityai/stable-diffusion-xl-base-1.0"
    assert res.seed == 7


def test_pipeline_is_cached_per_model(fakes):
    assert _run(fakes).success
    assert _run(fakes).success
    assert fakes.auto.from_pretrained.call_count == 1
    assert _run(fakes, model="runwayml/stable-diffusion-v1-5").success
    assert fakes.auto.from_pretrained.call_count == 2
    assert set(local_diffusion._PIPELINE_CACHE) == {
        "stabilityai/stable-diffusion-xl-base-1.0", "runwayml/stable-diffusion-v1-5"}


def test_cuda_loads_fp16_variant_with_cpu_offload(fakes):
    fakes.use_cuda(True)
    assert _run(fakes).success
    fakes.auto.from_pretrained.assert_called_once_with(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype="float16", variant="fp16")
    fakes.pipe.enable_model_cpu_offload.assert_called_once_with()
    fakes.pipe.to.assert_not_called()


def test_cuda_falls_back_when_repo_has_no_fp16_variant(fakes):
    fakes.use_cuda(True)
    fakes.auto.from_pretrained.side_effect = [OSError("no fp16 variant"), fakes.pipe]
    assert _run(fakes).success
    calls = fakes.auto.from_pretrained.call_args_list
    assert calls[0].kwargs == {"torch_dtype": "float16", "variant": "fp16"}
    assert calls[1].kwargs == {"torch_dtype": "float16"}
    assert fakes.pipe.enable_model_cpu_offload.called


def test_generation_error_is_reported_not_raised(fakes):
    fakes.pipe.side_effect = RuntimeError("CUDA out of memory")
    res = _run(fakes)
    assert res.success is False
    assert "CUDA out of memory" in res.error
