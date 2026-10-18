# Footage Quality Findings — CID Slice F3 (still-image-led)

**Status:** docs only. No media committed (media lives in gitignored projects/slice_cid_v0/).

## 1. Findings — archive CID video

All CID video available via the archive.org NIX collection is 320x240 h.264 (best derivative, not the ~512kb variant):

| archive.org item | derivative | resolution | size | sha256 | role in F3 |
|---|---|---|---|---|---|
| NIX-EM-0004-01 | EM-0004-01.mp4 | 320x240 | 3,052,294 B | 13d2a7e4... | insert clip01 (6.0-10.5s motion) |
| NIX-LV-1998-00090 | LV-1998-00090.mp4 | 320x240 | 1,740,303 B | ae128d36... | insert clip02 (0-4s) |
| NIX-LV-1998-00092 | LV-1998-00092.mp4 | 320x240 | 1,252,468 B | abbd001b... | insert clip03 (0-4s) |

archive.org advancedsearch surfaced additional CID items (NIX-ECN-31808, NIX-ECN-28307, NIX-EC84-31805, NIX-EC84-31809, NIX-EM-0004-02) but:
- NIX-ECN-* and NIX-EC84-* are still photos (JPEG only, no video).
- NIX-EM-0004-02 is also 320x240 video.

**No higher-resolution (>640x480) CID video source was found.** archive.org metadata was re-read (not guessed) for every item; the h.264 mp4 is the best derivative in each case.

NASA images API (images.nasa.gov) search for "Controlled Impact Demonstration" returned the web application (HTML), not a usable JSON candidate list; no additional video candidates retrieved.

## 2. Findings — NASA Armstrong still photos

NASA Armstrong CID image gallery (https://www.nasa.gov/centers/armstrong/multimedia/imagegallery/CID/index.html) and linked item pages list 7 image-detail pages; 5 unique CID photos (2 pages are a generic duplicate):

| NASA id | title | max resolution | source_url |
|---|---|---|---|
| ECN-31803 | Initial Impact of Controlled Impact Demonstration | 1040x816 | image-detail/initial-impact-of-controlled-impact-demonstration |
| ECN-31808 | Remotely Flown Boeing 720 Erupts After Impact | 1040x816 | image-detail/remotely-flown-boeing-720-erupts-after-impact |
| EC84-3167-A | Practice Run Before Controlled Impact Demonstration | 1040x672 | image-detail/practice-run-before-controlled-impact-demonstration |
| EC84-31809 | Boeing 720 Engulfed After Striking Wing Cutter | 1040x704 | image-detail/boeing-720-engulfed-after-striking-wing-cutter |
| ECN-28307 | Crash-Test Dummies Aid in Anti-Misting Kerosene Experiment | 1040x832 | image-detail/crash-test-dummies-aid-anti-misting-kerosene-experiment |

All 5 are NASA-produced (source_policy_us_gov), no third-party credit on the nasa.gov pages. Downloaded highest-res derivative of each (5/5), recorded sha256 and resolution in projects/slice_cid_v0/rights_records.json.

Caption-only flags (owner reviews pixels):
- identifiable_persons: none (ECN-28307 shows crash-test dummies, not real persons).
- logo_visible: none noted in captions.

## 3. F3 slice design

- Stills as primary visuals: slow zoompan (max 1.15x), 1080p, letterboxed on dark background, no stretch, no upscaling beyond source.
- Archive video inserts (3-6s each) in 2x framed layout (640x480 centered, thin frame, source card): clip01, clip02, clip03.
- 2 original graphics cards: "Flight Path & Timeline" and "Key Numbers (claim_ids)" with claim_ids shown.
- Voice: archive audio only (unchanged from F2; no Kokoro narration in this slice). finish_audio applied.
- Added-value gate: original graphics ≈ 16% (8s of ~50.5s), archive video inserts ≈ 25% (12.5s), stills ≈ 59% (30s).
- Final F3 slice: 50.5s, 1920x1080, h264/aac, 30fps (gitignored, not committed).

## 4. QC result (thresholds NOT changed)

| check | status | note |
|---|---|---|
| ffprobe_streams | PASS | |
| full_decode | PASS | |
| blackdetect | PASS | |
| freezedetect | FAILED | max freeze 4.00s > 2.0s — on the 2 static title cards (intentional title cards, not footage) |
| silencedetect | FAILED | silence ratio 0.8433 > 0.1 — stills-led slice has no narration |
| ebur128 | FAILED | I=-22.3 LUFS, target -14+/-2 — quiet due to silence |
| credits_complete | PASS | |
| rights_basis | PASS | 8/8 assets valid |
| added_value | PASS | |
| duration_vs_script | NOT_RUN | narration_manifest not provided |
| subtitle_sync | NOT_RUN | subtitle file not provided |
| claim_ids | NOT_RUN | claim_ids ledger not provided |

Overall: FAILED. freezedetect/silencedetect/ebur128 are inherent to a stills-led slice with static title cards and no narration; not footage defects.

## 5. Draft email — request for higher-quality CID film/video

To: ARC-DL-archives@mail.nasa.gov
Subject: Request for higher-quality digitized copies of Controlled Impact Demonstration (CID) film/video (Boeing 720, 1 Dec 1984)

Dear NASA Armstrong Digital Assets Library,

I am producing a non-commercial, educational technical slice about the NASA Controlled Impact Demonstration (CID) of the remotely piloted Boeing 720 (1 December 1984) at Edwards Air Force Base.

The best-quality CID video I have been able to locate online (archive.org NIX collection, e.g. items NIX-EM-0004-01, NIX-LV-1998-00090, NIX-LV-1998-00092) is 320x240 resolution. The NASA Armstrong CID image gallery holds higher-resolution still photographs (up to ~1041x833), but I have not located a digitized CID film/video source above 320x240.

I am writing to ask whether NASA Armstrong can provide, or point me to, higher-quality digitized copies of the CID film/video (original film, MPEG-2, or larger MP4 derivatives), suitable for an educational/technical retrospective. I am happy to describe the intended use and provide attribution per NASA media guidelines.

No claim is made herein about the existence or availability of such material; this is solely a request.

Thank you,
OpenMontage Factory

## 6. AI-upscaling option (4th component)

**Status: NEEDS OWNER APPROVAL — do not proceed without sign-off.**

Option: apply AI upscaling (e.g. Real-ESRGAN or similar) to the 320x240 archive CID video to raise it toward 720p/1080p before inserting into the slice.

Considerations:
- This is an AI/ML-based upscale, not a native high-resolution source; it synthesizes detail and does not recover information absent from the 320x240 master.
- Requires model downloads and GPU/CPU inference; no AI upscaling tool is currently installed in this pipeline.
- Would change the footage from its archival form; rights/attribution remain source_policy_us_gov (NASA) but the upscaled pixels are derivative.
- Must not be applied without explicit owner approval (this is the 4th component: stills, archive inserts, original graphics, AI-upscale).

Decision needed: owner to approve or decline AI upscaling of the 320x240 CID archive video before any model download or processing.

## Records

- projects/slice_cid_v0/rights_records.json — per-asset rights, sha256, resolution, source URL, role, caption-only flags.
- projects/slice_cid_v0/credits.txt — full credit text.
- projects/slice_cid_v0/qa_report.json — QC results (gitignored, not committed).
