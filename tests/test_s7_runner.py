"""Static guards for tools/kaggle_bridge/s7_bakeoff_run.py (S7-2).

The kernel copy is only exercised on Kaggle, so these tests catch the cheap
mistakes locally before burning a GPU run:
  * the module compiles;
  * `global X` is declared before the first use of X in that function
    (the S5 SDXL run 1 died on exactly this: a SyntaxError);
  * no bitsandbytes / CPU fallback; fp16 only;
  * the install ladder has at most 4 rungs and starts with a RELEASED
    diffusers (git-main diffusers is only a later rung);
  * klein probes Flux2KleinPipeline first (the S5 klein run died because the
    job used the FLUX.2-dev class and left the text encoder on meta);
  * the manifest carries every measurement S7 requires.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNNER = REPO / "tools/kaggle_bridge/s7_bakeoff_run.py"
SRC = RUNNER.read_text(encoding="utf-8")
TREE = ast.parse(SRC)


def _load():
    spec = importlib.util.spec_from_file_location("s7_runner_mod", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["s7_runner_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


def _funcs(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def test_runner_compiles():
    compile(SRC, str(RUNNER), "exec")


def test_global_declared_before_use():
    for fn in _funcs(TREE):
        names = set()
        decl_line = {}
        for node in ast.walk(fn):
            if isinstance(node, ast.Global):
                for n in node.names:
                    names.add(n)
                    decl_line[n] = node.lineno
        if not names:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id in names:
                    assert node.lineno > decl_line[node.id], (
                        f"{fn.name}: '{node.id}' used at line {node.lineno} "
                        f"before 'global {node.id}' at line {decl_line[node.id]}")


def test_no_forbidden_routes():
    low = SRC.lower()
    assert "import bitsandbytes" not in low, "no bitsandbytes in the S7 runner"
    assert "bitsandbytesconfig" not in low, "no 4-bit quantisation in the S7 runner"
    assert "torch.float16" in SRC or "float16" in SRC, "fp16 only"
    assert "cpu_fallback" in SRC
    assert "no cpu fallback" in low


def test_install_ladder_shape():
    mod = _load()
    for model, ladder in mod.DEFAULT_LADDERS.items():
        assert 1 <= len(ladder) <= 4, f"{model}: ladder must hold at most 4 rungs"
        first = mod.RELEASED_STACKS[ladder[0]]["pip_args"]
        assert not any(a.startswith("git+") for a in first), \
            f"{model}: rung 1 must be a RELEASED diffusers"
    assert set(mod.RELEASED_STACKS) >= {
        "released_041_x4", "released_041_x5", "released_036_x4",
        "git_main_x4", "git_main_x5"}


def test_probe_classes_per_model():
    mod = _load()
    assert mod.PIPELINE_CANDIDATES["zimage"] == ["ZImagePipeline"]
    assert mod.PIPELINE_CANDIDATES["klein"][0] == "Flux2KleinPipeline"
    assert mod.PIPELINE_CANDIDATES["sdxl"] == ["StableDiffusionXLPipeline"]


def test_measurement_fields_present():
    for token in ("black_count", "nan_count", "oom_count", "peak_vram_mb",
                  "steady_state_sec_per_image", "load_seconds",
                  "usable_images_per_minute", "versions", "install_log",
                  "max_wall_seconds"):
        assert token in SRC, f"manifest field {token} missing"


def test_wall_cap_is_ninety_minutes():
    mod = _load()
    assert mod.MAX_WALL_SECONDS == 5400
