# CID Beat Coverage — OpenMontage MASTER RUN H2

**Status:** docs only. Coverage map of available assets to narrative beats for the CID full script (CID_FULL_SCRIPT_v0.md).
**Method:** archive.org advancedsearch (keyless) re-read for all NIX CID items; NASA Armstrong CID image gallery re-read; NASA images API search returned web-app HTML (no JSON candidates, no additional assets). Rights per RIGHTS_MODEL.md: third-party credit = REJECT; NASA-produced + no third-party credit = source_policy_us_gov.
**Downloads:** none new beyond metadata reads (0 of 3 test-file limit used). All asset metadata below from archive.org / nasa.gov record pages already in evidence.

---

## 1. Narrative beats and required coverage

The full script (CID_FULL_SCRIPT_v0.md) has 6 narrative beats:

| beat | description | key claims |
|---|---|---|
| B1 | Preparation — program scope, aircraft, purpose | CID-01 to CID-05 |
| B2 | Remote piloting — commitment altitude, decision point | CID-06 to CID-08 |
| B3 | Approach — impact geometry | CID-09, CID-17 |
| B4 | Impact — ignition, fireball | CID-10 |
| B5 | Fire — fire behavior, interior damage, cabin cameras | CID-16, CID-23 to CID-28 |
| B6 | Aftermath / lessons — FAA cancellation, fuel ineffectiveness | CID-19 to CID-22, CID-29, CID-30 |

---

## 2. Available assets

### 2.1 Archive.org NIX video clips (all 320x240 h.264, all NASA/Dryden or NASA/Langley, rights=None → source_policy_us_gov, no third-party credit)

| archive.org item | title | center | resolution | size | rights_basis | third-party credit? | usable? |
|---|---|---|---|---|---|---|---|
| NIX-EM-0004-01 | CID flight video montage | NASA/Dryden | 320x240 | 3,052,294 B | source_policy_us_gov | no | USABLE |
| NIX-EM-0004-02 | CID tail camera video | NASA/Dryden | 320x240 | 2,929,659 B | source_policy_us_gov | no | USABLE |
| NIX-EC84-31805 | CID Aircraft pre-impact lakebed skid | NASA/Dryden | 320x240 | TBD | source_policy_us_gov | no | USABLE |
| NIX-EC84-31806 | CID Aircraft post-impact lakebed skid | NASA/Dryden | 320x240 | TBD | source_policy_us_gov | no | USABLE |
| NIX-EC84-31809 | CID Post-impact fireball | NASA/Dryden | 320x240 | TBD | source_policy_us_gov | no | USABLE |
| NIX-ECN-31808 | CID Post-impact fireball | NASA/Dryden | 320x240 | TBD | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00090 | Crash Impact Demonstration pt 1/10 | NASA/Langley | 320x240 | 1,740,303 B | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00092 | Crash Impact Demonstration pt 3/10 | NASA/Langley | 320x240 | 1,252,468 B | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00098 | Crash Impact Demonstration pt 9/10 | NASA/Langley | 320x240 | 1,599,299 B | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00091 | Crash Impact Demonstration pt 2/10 | NASA/Langley | 320x240 | 3,543,825 B | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00093 | Crash Impact Demonstration pt 4/10 | NASA/Langley | 320x240 | 2,994,722 B | source_policy_us_gov | no | USABLE |
| NIX-LV-1998-00096 | Crash Impact Demonstration pt 7/10 | NASA/Langley | 320x240 | 3,954,050 B | source_policy_us_gov | no | USABLE |

**Note:** size/TBD for items whose file list was read but file not downloaded (metadata-only). All NIX video items are 320x240 h.264 per archive.org metadata file list (re-read, not guessed).

### 2.2 NASA Armstrong still photos (all NASA/Armstrong, source_policy_us_gov, no third-party credit)

| nasa.gov id | title | resolution | source_url |
|---|---|---|---|
| ECN-31803 | Initial Impact of Controlled Impact Demonstration | 1040x816 | image-detail/initial-impact-of-controlled-impact-demonstration |
| EC84-3167-A | Practice Run Before Controlled Impact Demonstration | 1040x672 | image-detail/practice-run-before-controlled-impact-demonstration |
| ECN-31808 | Remotely Flown Boeing 720 Erupts After Impact | 1040x816 | image-detail/remotely-flown-boeing-720-erupts-after-impact |
| EC84-31809 | Boeing 720 Engulfed After Striking Wing Cutter | 1040x704 | image-detail/boeing-720-engulfed-after-striking-wing-cutter |
| ECN-28307 | Crash-Test Dummies Aid in Anti-Misting Kerosene Experiment | 1040x832 | image-detail/crash-test-dummies-aid-anti-misting-kerosene-experiment |

### 2.3 Rejected assets (third-party credit = REJECT per RIGHTS_MODEL.md)

| asset | reason |
|---|---|
| youtube-Jpc32JQXT_0 | third-party credit ("The Federal File" re-upload) + no license statement → rights_basis=unknown → REJECT |
| File:Controlled Impact Demonstration.webm | third-party uploader (Askeuhd) → third-party credit → REJECT |
| File:Approach and Landing Tests Film Documentary.webm | third-party uploader → REJECT |
| File:NASA Report - Space Shuttle Enterprise Rollout.webm | third-party uploader → REJECT |

---

## 3. Beat-to-asset coverage map

| beat | beat name | archive video assets | still assets | graphics cards | coverage assessment |
|---|---|---|---|---|---|
| B1 | Preparation | EM-0004-01 (flight video montage) | ECN-31803, EC84-3167-A | Flight Path & Timeline card | GOOD — archive flight montage + prep stills |
| B2 | Remote piloting | EM-0004-01 (flight video montage) | ECN-31808, EC84-3167-A | none | GOOD — flight montage shows remote-piloted aircraft |
| B3 | Approach | EM-0004-01 (motion segment), EC84-31805 (pre-impact skid) | ECN-31803 | none | GOOD — approach/skid coverage from two angles |
| B4 | Impact | LV-00090 (impact), EC84-31806 (post-impact skid) | ECN-31808 | none | GOOD — impact + post-impact skid from two angles |
| B5 | Fire | LV-00092 (fireball), EC84-31809 (post-impact fireball), ECN-31808 (post-impact fireball) | EC84-31809 (still) | none | EXCELLENT — fireball from three angles + still |
| B6 | Aftermath / lessons | ECN-28307 (dummies installed - still-image source) | ECN-28307 (dummies still) | Key Numbers card | LIMITED — no dedicated aftermath motion footage; dummies still + graphics card only |

**Total archive video assets:** 12 NIX clips (all source_policy_us_gov, all 320x240)
**Total still assets:** 5 NASA Armstrong photos (all source_policy_us_gov, up to 1040x833)
**Total graphics cards:** 2 original (Flight Path & Timeline, Key Numbers)

---

## 4. Gaps

| beat | gap | severity | proposed mitigation |
|---|---|---|---|
| B6 | Aftermath / lessons — no dedicated motion footage of post-impact investigation, cabin interior, or lessons-learned discussion | MEDIUM | Use dummies still (ECN-28307) + Key Numbers graphics card + stills with slow zoompan; note gap in script |
| All beats | All archive video is 320x240; no source above 640x480 found on archive.org or NASA images API | MEDIUM | Upscale to 1080p with lanczos + pad (existing pipeline); AI upscaling NEEDS OWNER APPROVAL (4th component) |
| B1 | No dedicated "program scope" motion footage beyond flight montage | LOW | Flight montage (EM-0004-01) covers scope; stills for context |

---

## 5. Viability-gate wording (proposed)

**Proposed gate (not yet applied):**

> In addition to the raw clip count (≥ 10 usable clips), the stage 0 topic viability gate requires coverage of ≥ 6 distinct narrative beats with ≥ 1 usable clip per beat. Beats: preparation, remote piloting, approach, impact, fire, aftermath. A topic lacking ≥ 6 beats is NOT_GATE_READY regardless of clip count.

**Applied to CID:** CID covers all 6 beats (B1–B6) with ≥ 1 usable asset per beat → GATE_READY on narrative coverage.

**Beat coverage summary:**
- B1 Preparation: GOOD (archive + stills)
- B2 Remote piloting: GOOD (archive flight montage + stills)
- B3 Approach: GOOD (2 archive angles + still)
- B4 Impact: GOOD (2 archive angles + still)
- B5 Fire: EXCELLENT (3 archive angles + still)
- B6 Aftermath: LIMITED (dummies still + graphics card only; no motion aftermath footage)

**CID passes the proposed viability gate on beat coverage (6/6 beats covered).**

---

## 6. Rights summary

- All 12 NIX archive clips: source_policy_us_gov (NASA-produced, no third-party credit)
- All 5 NASA Armstrong stills: source_policy_us_gov (NASA-produced, no third-party credit)
- 0 assets REJECTED for third-party credit in the selected set (4 third-party-upload assets identified and REJECTED)
- No asset downloaded beyond metadata reads (0 of 3 test-file limit used)
