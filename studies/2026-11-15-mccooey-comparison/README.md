# DICTO's solids against McCooey's Visual Polyhedra (15 Nov 2026) - DICTO · dictospheres.com

**Verdict (15 Nov 2026): NOT DONE. McCooey's site refuses scripted access, so no DICTO solid has been compared with his catalogue yet, and no claim of "new" can be confirmed or withdrawn by this study.** David McCooey's *Visual Polyhedra* (dmccooey.com/polyhedra) answered the polite fetcher (plain Python client with its own default user agent, robots.txt read first, 2 s between requests) with HTTP 465 "Access Denied - Sorry, you have been blocked ... please reach out to the site owner". As instructed, the crawl stopped at once. The site was not worked around: no other client, no changed user agent, no bot-check bypass.

Every other part of the comparison is built and tested, so it can run as soon as the catalogue files are at hand (see "What DICTO decides").

## Status
- DICTO noted on 15 Nov 2026 that much of the McCooey material "seems to be what we now have". That stays an open question until the comparison has run.
- Until then the existing claims stand exactly as the earlier studies worded them. One example: studies/2026-11-12-permutohedron-equal-edges, PRIOR-ART.md, "339 H3 atoms were not found in the sources checked". Those sources did not include McCooey's catalogue, so that wording must keep "in the sources checked".
- Also called / changes to "new": **none can be listed yet**. No book, Concordance name or paper is to be changed on the strength of this study.

## What DICTO decides (one of these, then one job finishes the comparison)
1. **Ask McCooey** for the coordinate files, or for permission to fetch them, citing the block's request ID (below). This is the cleanest route, and it credits him directly.
2. **DICTO downloads the catalogue in his own browser** (each polyhedron page links its "Name.txt" coordinate file) into one folder. Then match.py runs on that folder unchanged.
3. Approve a different client explicitly. Three single requests made by hand with curl before the block were answered. Using it now would be a way round a block the site chose, so this study does not do it without DICTO's say.

Block request ID (for McCooey): d4307556-99c6-4ee7-af7a-cb8a9caa3f7a (15 Nov 2026).

## What is ready (all tested on the compute host, job mccooey-offline, FINAL ok, 42/42 checks)
**DICTO's solids, 4963 in one file** (scripts/export_dicto.py; corners as 40-digit decimals from the exact builds):

| group | solids | source | precision |
|---|---|---|---|
| permutohedron cones A3 / B3 / H3: every equal-edged solid (incl. the 369 distinct new atoms, 371 rows since A3-10/16 = B3-19/36, and the 54 sums of atoms) | 4547 | study 2026-11-12-permutohedron-equal-edges, rebuilt from its 0/1 wall labels with its own exact coxeter.py | exact Q(√2), Q(√5) |
| DICTO silent zonohedron, signed permutations of (a, a+1, a+2), a = −1 + √(1 + √(5/6)) = 0.383065771818 | 1 | study 2026-11-14-forced-fixed-points | exact |
| Lesser and Greater Golden OG (#91), 102 corners, 80 faces each | 2 | study 2026-11-03-dual-pairs-dimensions (dp_lib) | exact Q(√2, √5) |
| OG family: OG, KRE, PHE, TPP, DPHP, TPH, TQH, TQP, TQHD (#39); Hamlet, Ophelia (#80); pedal steps 5-11 (#43); Universal PiTet golden truncated icosahedron and Q (#38) | 20 | five-fold-octet float file + recomputed steps | double |
| app registry used by the books (the disc-ranking study's 389) | 389 | studies/2026-11-13-platonic-disc-ranking | double |
| hybrid kit: cap, roof plate Z, roof R, Admiral Cap | 4 | study 2026-11-14-platonic-hybrid (golden.py) | exact Q(√5) |

Export checks: cone counts 4547 / 371 / 54; Golden OGs 102 corners and 80 faces; the nine OG-family corner counts; T¹⁻⁴(OG) and P¹⁻⁴(OG) recomputed agree with the float file within 1e-7; Hamlet 452 corners / 270 faces, Ophelia 642 / 440; pedal steps 5-11 have 252, 320, 402, 500, 732, 662, 672 faces as the Concordance says; the PiTet cycle runs 30 → 32 → 60 → 32 → 30 corners; Z's ridge lies on the plate's top face.

**The matcher** (scripts/match.py):
- IDENTICAL means congruent up to similarity and mirror. Both corner sets are centred and scaled to mean squared radius 1. An orthogonal map (det ±1) is then fitted to three independent corners, and it must carry every corner onto a corner (tolerance 1e-8). The fit is re-checked in 40 digits against McCooey's 30-digit constants when the DICTO solid is an exact build. Faces are compared as well for non-convex entries.
- SIMILAR means the same combinatorics (isomorphic vertex-face incidence of the merged hull faces) with a different metric. The distinct edge lengths of both are recorded.
- NOT IN THE CATALOGUE means neither of the above.

Controls run against the one McCooey file at hand (TruncatedOctahedron.txt, fetched by hand before the block; used only as a test fixture and not redistributed). All seven passed:
- the TO turned, mirrored, scaled and moved is IDENTICAL, 40-digit residual 5.7e-41;
- the registry TO is IDENTICAL, and so is the A3 cone's TO;
- the TO stretched 1.3 along an axis is SIMILAR and not IDENTICAL;
- the cube is NOT IN THE CATALOGUE;
- the silent zonohedron is not IDENTICAL.

The verdict counts in that fixture run test the tool only. They say nothing about the catalogue.

## Files
- scripts/fetch_mccooey.py: the polite crawler. Since 15 Nov it stops on any refusal (HTTP 4xx other than 404, "Access Denied", a refused robots.txt).
- scripts/export_dicto.py, scripts/match.py: as above. Run: `export_dicto.py <repo root> data/dicto-solids.json`, then `match.py data/dicto-solids.json <folder of McCooey .txt files> <manifest.json> data/matches.json`.
- data/mccooey-fetch-pilot.log (the refusal), data/mccooey-offline.log (export + matcher controls). data/dicto-solids.json (26 MB) is regenerated by the export and is not committed. Downloaded McCooey files stay in data/cache/ and are not committed: they are his work.

Credit: the catalogue, its coordinates and its names are David McCooey's (Visual Polyhedra, dmccooey.com/polyhedra).
