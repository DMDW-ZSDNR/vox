"""Section cards: the EDL must carry own-graphics chapter cards.

Spec L6 requires original graphics (chapter cards, source/credit cards) in
every episode; QC `added_value` requires >= 1 original graphic per 90 s, an
all-illustration episode has zero unless the EDL adds them.
"""
from __future__ import annotations

import json

import pytest

from tools.illustration.pilot_edl import build_illustration_edl


def _images(n):
    return [{"file": f"/img/ill_{i:02d}.png", "sha256": "a" * 64,
             "scene_id": f"s{i}"} for i in range(1, n + 1)]


def _sections(n_sections=3, sentences_per=2):
    out = []
    for s in range(n_sections):
        out.append({
            "title": f"Chapter {s + 1} — title {s + 1}",
            "sentences": [
                {"sentence": f"chapter {s} sentence {k} with a number of words",
                 "claim_id": "SE-01"}
                for k in range(sentences_per)
            ],
        })
    return out


def _cards(n):
    return [f"/cards/card_{i}.png" for i in range(n)]


def test_section_cards_are_own_graphics_cuts():
    edl = build_illustration_edl(
        _images(12), None, total_duration=60.0, topic="t", episode="e",
        sections=_sections(3), card_paths=_cards(3), card_duration=3.0)
    cards = [c for c in edl["cuts"] if c["role"] == "graphics_card"]
    assert len(cards) == 3
    for c in cards:
        assert c["kind"] == "graphics"
        assert c["static_by_design"] is True
        assert c["rights_basis"] == "explicit_license"
        assert "original" in c["credit"].lower()
        assert c["duration"] == pytest.approx(3.0, abs=0.01)
        assert c["source"].endswith(".png")
    # Illustrations are still all used exactly once.
    ill = [c for c in edl["cuts"] if c["role"] == "illustration"]
    assert len(ill) == 12


def test_section_card_timeline_stays_contiguous_and_exact():
    edl = build_illustration_edl(
        _images(12), None, total_duration=60.0, topic="t", episode="e",
        sections=_sections(3), card_paths=_cards(3), card_duration=3.0)
    cuts = edl["cuts"]
    assert cuts[0]["start"] == 0.0
    assert cuts[-1]["end"] == 60.0
    for a, b in zip(cuts, cuts[1:]):
        assert b["start"] == pytest.approx(a["end"], abs=1e-6)
    assert all(c["duration"] > 0 for c in cuts)
    assert sum(c["duration"] for c in cuts) == pytest.approx(60.0, abs=0.01)


def test_cards_open_each_section():
    edl = build_illustration_edl(
        _images(12), None, total_duration=60.0, topic="t", episode="e",
        sections=_sections(3), card_paths=_cards(3), card_duration=3.0)
    cuts = edl["cuts"]
    positions = [i for i, c in enumerate(cuts) if c["role"] == "graphics_card"]
    assert len(positions) == 3
    # The first cut is a card, and no two cards are adjacent.
    assert positions[0] == 0
    assert all(b - a > 1 for a, b in zip(positions, positions[1:]))


def test_no_cards_keeps_legacy_behaviour():
    edl = build_illustration_edl(_images(4), _sections(2, 2)[0]["sentences"],
                                 total_duration=20.0, topic="t", episode="e")
    assert all(c["role"] == "illustration" for c in edl["cuts"])
    assert edl["cuts"][-1]["end"] == 20.0


def test_section_cards_must_match_sections():
    with pytest.raises(ValueError):
        build_illustration_edl(_images(6), None, total_duration=30.0,
                               topic="t", episode="e",
                               sections=_sections(3), card_paths=_cards(2))
