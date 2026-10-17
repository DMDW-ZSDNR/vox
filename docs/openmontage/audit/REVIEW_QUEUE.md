# Review Queue — OpenMontage Milestone C2 (v2)

**Status:** docs/report only. Media artifacts under `projects/c2_review/` are gitignored and NOT committed.
**Rule source:** `docs/openmontage/RIGHTS_MODEL.md` (applied as written, not loosened).
**Subagent note:** executed inline (orchestrator). The `task` tool exposes only `explore`/`general`; no separate `.kilo/agents` subagent process was available. Footage-scout/evidence-checker/qa-reviewer rules applied inline and attributed by domain.

---

## Per-clip review queue

Each row: `nasa_id`, URL, evidence fields observed, `rights_basis`, verdict, and what a human must check (identifiable persons, logos/insignia, third-party material). Preview/thumbnail paths listed where available; downloaded variants live under `projects/c2_review/previews/` (gitignored, not committed, total ~20K).

### Boeing 720 Controlled Impact Demonstration 1984

| # | nasa_id / asset | URL | Evidence fields | rights_basis | Verdict | Human must check |
|---|---|---|---|---|---|---|
| B-1 | File:Controlled Impact Demonstration.webm | https://commons.wikimedia.org/wiki/File:Controlled_Impact_Demonstration.webm | uploader=Askeuhd (2022-05-23); license tag "Public domain" per prior probe; extmetadata fetch returned no usable JSON (fetch limitation) | explicit_license | NEEDS_REVIEW | identifiable_persons (crash-test footage may show crew/dummies), logo_visible (NASA insignia on vehicle), third-party credit (uploader Askeuhd — third-party uploader, not NASA) |
| B-2 | NIX-EM-0004-02 | https://archive.org/details/NIX-EM-0004-02 | creator=NASA/Dryden Flight Research Center; date 1988-12-02; duration 36s; **no** `license`/`rights`/`licenseurl` field | unknown | REJECT | n/a (rejected) |
| B-3 | NIX-EM-0004-01 | https://archive.org/details/NIX-EM-0004-01 | creator=NASA/Dryden Flight Research Center; date 1988-12-02; duration 38s; **no** `license`/`rights`/`licenseurl` field | unknown | REJECT | n/a |
| B-4..12 | NIX-LV-1998-00090 … 00098 (9 items) | https://archive.org/details/NIX-LV-1998-00090 … | creator=NASA/Langley Research Center; date 1988-12-02; duration 11–39s each; **no** `license`/`rights`/`licenseurl` field | unknown | REJECT x9 | n/a |
| B-13 | youtube-Jpc32JQXT_0 | https://archive.org/details/youtube-Jpc32JQXT_0 | creator="The Federal File" (third-party re-upload); date 2017-03-17; duration 275s; **no** license statement | unknown | REJECT | n/a |

### Space Shuttle landing tests at Edwards (ALT-era specificity unverified)

| # | nasa_id / asset | URL | Evidence fields | rights_basis | Verdict | Human must check |
|---|---|---|---|---|---|---|
| S-1 | RSS_294545main_edw_113008_sts126_landing_pod | https://archive.org/details/RSS_294545main_edw_113008_sts126_landing_pod | title="Landing of Space Shuttle Endeavour"; creator=NASA; date=11/30/2008; description="…smooth touchdown at Edwards Air Force Base"; rights="Public Domain"; licenseurl=None; uploader=bonnie@archive.org; collections nasa/nasacastvideo; preview `__ia_thumb.jpg` (fetch returned 0 bytes — blocked) | explicit_license | NEEDS_REVIEW | identifiable_persons (crew on landing), logo_visible (NASA insignia on orbiter/pad), third-party credit (none in metadata) |
| S-2 | STS1FirstFlight | https://archive.org/details/STS1FirstFlight | title="STS-1 Space Shuttle First Manned Orbital Flight"; creator=**Department of Defense** (NOT NASA); date=1981-04-12; description includes "Provided by Fight for Space / Paul Hildebrandt" + fightforspace.com (**third-party credit**); licenseurl=Public Domain Mark 1.0; rights=None; uploader=eventidevisuals@gmail.com; preview __ia_thumb.jpg available | explicit_license | NEEDS_REVIEW | identifiable_persons (crew John Young/Robert Crippen named), logo_visible, third-party credit (DoD + Fight for Space — not NASA-produced despite NASA content) |
| S-3 | nasa-space-shuttle-discovery-sts-26-1988-tape-02 | https://archive.org/details/nasa-space-shuttle-discovery-sts-26-1988-tape-02 | title="NASA Space Shuttle Discovery STS 26 1988 TAPE 02"; creator=NASA; date=1988-09-29; description="via NASA TV / Multnomah Cable Access, CNN & NBC" + "Bernard Shaw … on CNN" (**third-party credits**); licenseurl=CC-BY 4.0; rights=None; uploader=drnormal@gmail.com; preview __ia_thumb.jpg available | explicit_license | NEEDS_REVIEW | identifiable_persons (Bonnie Dunbar named), logo_visible, third-party credit (CNN/NASA TV/Multnomah Cable Access) |
| S-4 | nasa_tv-STS-128_Landing | https://archive.org/details/nasa_tv-STS-128_Landing | creator=NASA TV; date 2009-09-11; duration 335s; rights="none stated" | unknown | REJECT | n/a |
| S-5..7 | 59094…, 59104…, 59084… (3 IA compilations) | https://archive.org/details/59094SpaceShuttleAmericasSpaceTransportationSystem … | creator=none (unknown provenance); rights="none stated"; third_party_credit=YES | unknown | REJECT x3 | n/a |
| S-8 | File:Approach and Landing Tests Film Documentary.webm | https://commons.wikimedia.org/wiki/File:Approach_and_Landing_Tests_Film_Documentary.webm | uploader=Askeuhd (2022-07-25); Public domain tag per prior probe; extmetadata fetch returned no usable JSON | explicit_license | NEEDS_REVIEW | identifiable_persons (ALT pilots), logo_visible (NASA insignia), third-party credit (uploader Askeuhd) |
| S-9 | File:NASA Report - Space Shuttle Enterprise Rollout.webm | https://commons.wikimedia.org/wiki/File:NASA_Report_-_Space_Shuttle_Enterprise_Rollout.webm | uploader=Askeuhd (2022-07-25); Public domain tag per prior probe; extmetadata fetch returned no usable JSON | explicit_license | NEEDS_REVIEW | identifiable_persons, logo_visible (NASA insignia on Enterprise), third-party credit (uploader Askeuhd) |
| S-10..22 | NASA-API 13 KSC clips (e.g. edw_052409_sts125_land, ksc_082505_114landing) | images-assets.nasa.gov/video/<nasa_id>/… | center=KSC; rights="none stated"; **no** license/rights/duration field exposed by NASA Image/Video Library API | unknown | REJECT x13 | n/a |

### X-15 research flights

| # | nasa_id / asset | URL | Evidence fields | rights_basis | Verdict | Human must check |
|---|---|---|---|---|---|---|
| X-1 | NDTV001077-X-15_Documentary_Revised | https://images-assets.nasa.gov/video/NDTV001077-X-15_Documentary_Revised/collection.json | center=AFRC; date_created=2021-02-01; description="X-15 Documentary… Early test footage, engineers in mission control room, in-flight footage from B-52 and chase aircraft, on-board the X-15, accidents, audio, maintenance, and pilots"; keywords X-15/NASA/AFRC/filmstock; **no** third-party credit/restriction in metadata | source_policy_us_gov candidate | NEEDS_REVIEW | identifiable_persons (pilots/engineers), logo_visible (NASA insignia on aircraft/control room), third-party credit (none in metadata) |
| X-2 | ksc_121704_b52_retires | https://images-assets.nasa.gov/video/ksc_121704_b52_retires/collection.json | center=KSC; date_created=2004-12-21; description="NASA retired its esteemed B-52B… carried aloft the first X-15 hypersonic rocket planes… last X-43A scramjet"; photographer="NASA or National Aeronautics and Space Administration"; **no** third-party credit/restriction in metadata | source_policy_us_gov candidate | NEEDS_REVIEW | identifiable_persons, logo_visible (NASA insignia on B-52), third-party credit (none in metadata) |

---

## Preview / contact-sheet evidence (downloaded, gitignored, not committed)

| File | Path | Size | Notes |
|---|---|---|---|
| X-15 NASA thumb | `projects/c2_review/previews/x15_nasa_thumb.jpg` | 5,877 B | From NASA Image/Video Library ~thumb.jpg |
| KSC B-52 thumb | `projects/c2_review/previews/ksc_b52_thumb.jpg` | 7,056 B | From NASA Image/Video Library ~thumb.jpg |
| IA thumb (RSS_294545main) | `projects/c2_review/previews/ia_rss_thumb.jpg` | 0 B | **Fetch returned 0 bytes — blocked** (archive.org thumbnail not reachable) |
| Contact sheet | `projects/c2_review/previews/contact_sheet_previews.jpg` | 6,686 B | ffmpeg `tile=2x1` of the two successful thumbnails |

**Total downloaded:** ~20K (well under the 200 MB cap). Nothing committed (projects/ is gitignored).

**Preview availability per clip:**
- NASA-API clips (X-1, X-2): `~thumb.jpg` / `~small.jpg` variants exist in `collection.json` links — downloadable.
- IA clips (S-1, S-2, S-3): `__ia_thumb.jpg` and `.thumbs/*.jpg` derivatives exist — S-1 thumb fetch blocked (0 bytes); S-2/S-3 thumbnails not fetched.
- Commons clips (B-1, S-8, S-9): thumbnail via Commons `Special:FilePath` / API (extmetadata fetch returned no usable JSON — fetch limitation).
- NASA-API Shuttle REJECT clips (S-10..22): `~thumb.jpg` variants exist but clips are REJECT, so no preview needed.

**Contact-sheet method:** ffmpeg `tile=2x1:margin=5:padding=10` over the two downloaded thumbnails → `contact_sheet_previews.jpg`. Per-clip 12-frame video contact sheets were not generated because (a) most NEEDS_REVIEW clips are still images/thumbnails, not readily downloadable video within time-box, and (b) the milestone is docs/reports-only. Defer video contact sheets to the next milestone.

---

## Human review checklist (matches NASA exceptions)

For each NEEDS_REVIEW clip, the human reviewer must confirm:
1. **Identifiable persons** — NASA guideline: commercial use of media including an identifiable person may infringe privacy/publicity rights; permission from the person required. Current NASA employees' names/likenesses/position titles barred on commercial products.
2. **Logos/insignia** — NASA Insignia ("meatball"), Logotype ("worm"), identifiers and imagery are NOT public domain; use protected by law.
3. **Third-party material** — NASA occasionally uses third-party copyrighted material with permission; marked with the copyright holder's name; NASA's use conveys no rights; contact the copyright holder directly.

Reviewer signs off with: reviewer name, date, notes. Only after sign-off does a NEEDS_REVIEW clip become eligible for the gate (see proposed gate wording in C2 report).
