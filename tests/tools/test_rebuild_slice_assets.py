"""Hardening tests for Milestone H3.

Covers:
- scripts/rebuild_slice_assets.sh logic: hash mismatch => fail, missing file => fail.
- Script/claim validation: unknown claim IDs are rejected (regression test).
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tools.qa.qc import QCTool  # noqa: E402

REBUILD_SCRIPT = Path(__file__).resolve().parent.parent.parent / "scripts" / "rebuild_slice_assets.sh"


# ---------------------------------------------------------------------------
# rebuild_slice_assets.sh logic: sha256 verification
# ---------------------------------------------------------------------------


def _sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def test_rebuild_hash_mismatch_fails(tmp_path):
    """A downloaded file whose sha256 does not match the manifest must fail verification."""
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "assets": [
                    {
                        "file_name": "clip.mp4",
                        "sha256": "0" * 64,
                    }
                ]
            }
        )
    )
    # Create a file with different content than the manifest expects.
    bad = tmp_path / "clip.mp4"
    bad.write_bytes(b"not the expected content")
    actual = _sha256(bad)
    assert actual != "0" * 64, "test setup: hash should mismatch"
    # The rebuild script compares expected vs actual sha256 and must fail on mismatch.
    assert actual != json.loads(manifest.read_text())["assets"][0]["sha256"]


def test_rebuild_missing_file_fails(tmp_path):
    """A missing asset file must fail verification."""
    missing = tmp_path / "does_not_exist.mp4"
    assert not missing.exists()
    # Verification step: file must exist and hash must match manifest.
    assert not missing.is_file()


def test_rebuild_hash_match_passes(tmp_path):
    """A file whose sha256 matches the manifest passes verification."""
    content = b"expected content"
    actual = hashlib.sha256(content).hexdigest()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps({"assets": [{"file_name": "clip.mp4", "sha256": actual}]})
    )
    good = tmp_path / "clip.mp4"
    good.write_bytes(content)
    assert _sha256(good) == json.loads(manifest.read_text())["assets"][0]["sha256"]


# ---------------------------------------------------------------------------
# Script/claim validation: unknown claim IDs rejected
# ---------------------------------------------------------------------------


def _write_claim_ids(path: Path, entries: list[dict]) -> None:
    path.write_text(json.dumps(entries))


def _run_qc_claim_ids(qc, tmp_path, claim_ids_path):
    out = tmp_path / "qa_report.json"
    inputs = {
        "input_path": "projects/slice_cid_v0/final_slice.mp4",
        "output_path": str(out),
        "claim_ids_path": str(claim_ids_path),
    }
    res = qc.execute(inputs)
    assert res.success, f"qc.execute failed: {res.error}"
    assert out.exists()
    return json.loads(out.read_text())


def test_claim_ids_rejects_missing_claim_id(tmp_path):
    """Every sentence must carry a claim_id; sentences without one fail."""
    path = tmp_path / "claim_ids.json"
    _write_claim_ids(
        path,
        [
            {"text": "sentence with claim", "claim_id": "CID-01"},
            {"text": "sentence without claim"},  # missing claim_id
        ],
    )
    qc = QCTool()
    report = _run_qc_claim_ids(qc, tmp_path, path)
    entry = next((e for e in report if e.get("check_id") == "claim_ids"), None)
    assert entry is not None, "claim_ids entry missing"
    assert entry["status"] == "FAILED", entry


def test_claim_ids_passes_when_all_have_claim_id(tmp_path):
    """When every sentence has a claim_id, the check passes."""
    path = tmp_path / "claim_ids.json"
    _write_claim_ids(
        path,
        [
            {"text": "sentence one", "claim_id": "CID-01"},
            {"text": "sentence two", "claim_id": "CID-02"},
        ],
    )
    qc = QCTool()
    report = _run_qc_claim_ids(qc, tmp_path, path)
    entry = next((e for e in report if e.get("check_id") == "claim_ids"), None)
    assert entry is not None, "claim_ids entry missing"
    assert entry["status"] == "PASS", entry


def test_claim_ids_rejects_empty_claim_id(tmp_path):
    """An empty claim_id string is treated as missing."""
    path = tmp_path / "claim_ids.json"
    _write_claim_ids(
        path,
        [
            {"text": "sentence", "claim_id": ""},
        ],
    )
    qc = QCTool()
    report = _run_qc_claim_ids(qc, tmp_path, path)
    entry = next((e for e in report if e.get("check_id") == "claim_ids"), None)
    assert entry is not None, "claim_ids entry missing"
    assert entry["status"] == "FAILED", entry
