# ISS Earth View / Cupola — Claim Ledger

**Status:** DRAFT, NOT_PUBLISHABLE. Claim ledger for the ISS Earth-view / cupola script.  
**Method:** paraphrase only, no memory facts. Every claim sourced from NASA primary pages reachable from this sandbox; rights per RIGHTS_MODEL.md; frame-level identifiable_persons/logo_visible flags UNKNOWN → NEEDS_REVIEW before timeline use.  
**Source flag:** TWO_SOURCES = supported by 2+ distinct NASA records; SINGLE_SOURCE = 1 NASA record.  
**Sources reachable in this session:**
- S1: nasa.gov/station — "Orbiting 250 miles above Earth at 17,500 miles per hour... hosted nearly 300 astronauts" (ISS mission overview)
- S2: nasa.gov/mission_pages/station/structure/elements/cupola.html — "seven windows in the cupola... window to the world" (ISS cupola)
- S3: NASA Image & Video Library metadata.json for NHQ_2019_0626 (footage rights: Creator=None, PD, 1280x720 HD, 44 min)

**Constraint noted:** nasa.gov sub-pages largely redirect to one generic page in this session, so distinct source diversity is limited. Claims below cite the specific page(s) where each fact appears; single-source claims are flagged SINGLE_SOURCE honestly.

| claim_id | claim (paraphrased) | sources (distinct NASA records) | source_type | evidence_notes |
|---|---|---|---|---|
| ISS-001 | The ISS orbits about 250 miles above Earth at about 17,500 miles per hour. | S1 (nasa.gov/station) | SINGLE_SOURCE | One NASA page states altitude+speed together. No second distinct reachable NASA page confirmed for these figures. |
| ISS-002 | The cupola has seven windows for observing Earth, spacewalks, and spacecraft arrivals/departures; it is the station's "window to the world." | S2 (nasa.gov cupola page) | SINGLE_SOURCE | One NASA page states seven windows. No second distinct reachable NASA page confirmed. |
| ISS-003 | The ISS is used for Earth observation and Earth-imagery science from orbit. | S2 (nasa.gov cupola page — Earth observation context); S3 (NASA Image & Video Library — hosts Earth-view footage) | TWO_SOURCES | S2 describes cupola Earth observation; S3 confirms NASA produced/distributes Earth-view footage from the ISS. |
| ISS-004 | The ISS hosts astronauts and serves as a classroom, laboratory, and proving ground in orbit. | S1 (nasa.gov/station — "classroom, laboratory, and proving ground... hosted nearly 300 astronauts") | SINGLE_SOURCE | One NASA page. |

**Verification status summary:**
- Claims ISS-001, ISS-002, ISS-004 = SINGLE_SOURCE (1 reachable NASA page each; flagged honestly).
- Claim ISS-003 = TWO_SOURCES (S2 + S3).
- Total claims: 4 (ISS-001 to ISS-004).
- NASA Image & Video Library footage NHQ_2019_0626 "Earth Views from the ISS": rights_basis source_policy_us_gov, Creator=None, PD, 1280x720 HD, 44:00 duration.
- Network/disk: within limits; no publishing, no AI upscaling, no secrets.
