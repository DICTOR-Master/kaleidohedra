# Waiting list triage, 7 November 2026

Source: `concordance.json` → `gaps.waiting` (60 items). Read only: nothing in the Concordance or in any paper was changed.

Method: each item's key numbers and phrases were searched in the current HTML of every paper and book folder (`papers/*/*.html`, book chapter files included, plus `book-centre-pyramids/drafts/`). The Concordance, status boards, destination notes, plans and the gallery were left out, because they are indexes and not homes. Publication state comes from each folder's `zenodo-state.json`. Study completeness comes from `studies/<study>/README.md` and the data listings.

Paper numbers to folders: #47 = `2026-10-22-platonic-mixes` (v3 published 6 Nov) · #92 = `2026-11-04-pyramid-tilings` (v2) · #93 = `2026-11-04-cubic-pairings` (v1) · #94 = `2026-11-04-harmonic-fingerprint` (v1) · #95 = `2026-11-05-og-pentagons` · #96 = `2026-11-05-reading-the-voids` · #97 Narcissus Keyed = `2026-11-05-keyed-narcissus` · #98 Narcissus and Covenant = `2026-11-04-hexoct-narcissus` · #99 Plato's Five in the Octet = `2026-11-06-five-in-octet` (v2, 7 Nov) · HexOct volume = `book-laws-of-stacking` (v8) · The Golden Ladder = `book-golden-ladder` (v5) · Alicia (Queens) = `book-queens` (v3) · DICTONIC Bonds = `book-bonds` · Centre Pyramids = `book-centre-pyramids` (drafts only, not published) · "Space-Fillers and Lattice Moves" and "OG volume": **no folder yet**.

Totals: **LANDED 15 · PENDING 38 · STALE 7**.

## Table

| n | Result (short) | Verdict | Destination | Evidence / missing |
|---|---|---|---|---|
| 1 | No reversed neighbour for T and C6: whole tetrahedra and whole cubes | PENDING | #92 v3 + #93 v2 | #92 §6 still says "Open… (1) whether… a reversed neighbour… can occur"; #93 open point (1) still open. Study complete (search proof, overlap margin 0.2) |
| 2 | #92 Table 2 complete: the 3 undecided rows have odd nT | PENDING | #92 v3 | #92 Table 2 still has the "not decided" rows. Study complete |
| 3 | R12 not face to face: planes x+y=k slide, uncountably many | PENDING | #93 v2 | #93 open point (2) still open. Study complete (384 pieces checked) |
| 4 | Admiral Cap network frustrated (≤ 8/12); ground states one free bit per layer; twin-boundary node | PENDING | Space-Fillers vol. | Not in any paper. Data complete; ground-state completeness not proved (stated in the README) |
| 5 | Galois twins of the golden cuts: cube only; dodecahedron self-twin + φ³ cut; φ³ cut not a cycle station | PENDING (partly landed) | Golden Ladder | GL has only the cube twins (from #90, "Theorem 1 (Galois twins)"). Dodecahedron self-twin and φ³ cut are missing. Study complete (sympy, exact) |
| 6 | Golden Ladder ch. 1, One Triangle, Three Numbers | LANDED | book-golden-ladder | Contents: "Chapter 1 · One Triangle, Three Numbers" |
| 7 | The Turned Twin: TRD, turned node, ring cells (read ok) | PENDING | HexOct vol. (next version) | `study-note-trd/paper.html` is written and read ok, but has no Zenodo record. HexOct v8 has the RD/TRD halves but not the turned node (J27 ties). Ready to release |
| 8 | Harmonic fingerprint: CO–RD sweep, tetrahedron sweep, network c/h; Fig. 1 labels | LANDED | #94 v1 | #94 (D) "CO ∩ μRD… Q4 = 0 at exactly one point", (E) "T ∩ μ(−T)", §4 "Networks: every node by its own sound" |
| 9 | PET-ring RD cells: tetrapod of 4 RDs; build sheet 1/4/6/14 | PENDING | HexOct vol. or Quanta | Not in any paper. README is short; the brief from DICTO's photos still has "[confirm]" items, so DICTO must confirm them first |
| 10 | Consolidation: one living volume per thread | STALE | — | Plan note (`2026-11-04-consolidation/PLAN.md`), not a result |
| 11 | O pyramids: reversed neighbours do occur; conjecture (octahedron or cube corner) | PENDING (open, not writable) | #92 v3 (as an open point) | Conjecture only; needs an argument for sliding edges ("not a queue job yet") |
| 12 | Mahler product on the cube–octahedron sweep: exact; max at 2μ³ − 9μ + 6 = 0 | PENDING | #94 v2 | No "Mahler" in #94 or GL. `mahler-sweep` README is complete and exact |
| 13 | Parallel tests: IQ max at μ = √3; table of special points | PENDING | #94 v2 | Not in any paper. Complete, but must be reworded per item 34 (Lindelöf, not a coincidence) |
| 14 | 4D harmonics: 600-cell 11-design; #91 sweep Q4=0 only at the 24-cell, Q6=0 at √2, 1+√3 | PENDING | #94 v2 (sweep) / Queens (calibration) | No "11-design" in any paper. `harmonic-4d` README complete |
| 15 | 600-cell slices: corner-first Q6 silent at 0.128/0.396/0.638; cell-first never Q4 and Q8 together | PENDING | Queens vol. | Not in a paper. Float only (heights ≈ 0.002); exact heights open, so it is only a minor section |
| 16 | CO–RD sweep: Mahler 40/3 at both ends, max at 12μ³ − 36μ² + 43 = 0; IQ max ≈ 1.523 | PENDING | #94 v2 (with 12–13) | Not in a paper. Complete. The "√3 coincidence" wording also needs the item 34 fix |
| 17 | Delian walk: O(t) cubic-silent exactly at t = 1/9, never together with Q8 | PENDING | #94 v2 | Not in #94 or Bonds. `harmonic-fingerprint` README §Delian walk is complete (exact factor) |
| 18 | Foam test on CsCl pairs: wall area symmetric, max at Kelvin, min (3+2√3)/4 | PENDING | #93 v2 | Not in a paper. `mahler-sweep` README §Foam test is complete |
| 19 | OG family fingerprint: W6 sign split; KRE quietest | PENDING | OG vol. (new) / OG family paper next version | Not in a paper. Float; the cycle stations Cleo star, rTI, H, jtI, M are still to do |
| 20 | Red Queen 11-design; Queens path: 1440 points form a 19-design at μ ≈ 0.92417 (classical, credited) | PENDING | Queens vol. | Not in a paper. Credit is checked; exact μ* is still to compute |
| 21 | Fibonacci stacking spectrum: word pure point with exact amplitudes; crystal non-Bragg at l = 1/2, cos 72° | PENDING | HexOct vol. (stackings) | Not in a paper. The pure-point part is complete. "Probably singular continuous" is unconfirmed (scaling exponent and literature to do) |
| 22 | J27 + octahedra tile hcp; with COs on mixed stackings; twisted twin of the rectified cubic | PENDING | #92 v3 (Thm 10 sequel) | #92 Thm 10(b) has only the local J27 vertex; the tiling is new. IP feasible on 5 stackings; prior art not yet checked |
| 23 | Sweep = SU(4)/SO(7) weight shapes; Fibonacci and Pell ladders | LANDED | book-golden-ladder ch. 2 | Table "SO(7) Pell 112, 4 928, 905 520…; truncated cube, 1 + √2" |
| 24 | Tuning: half the sweep is one octave; golden interval 833 cents | LANDED | book-golden-ladder ch. 2 | Table "golden interval φ 833 limit: Icosaxes 0" (the tuning-app idea is not a paper item) |
| 25 | 4D sweep = SO(9) weight shapes; All-Golden limits 1650, 27027… | LANDED | book-golden-ladder ch. 2 | "SO(9) Fibonacci 1 650, 27 027, 1 527 552" |
| 26 | Golden Ladder ch. 2, Silence Is Golden (read ok) | LANDED | book-golden-ladder | Contents: "Chapter 2 · Silence Is Golden" |
| 27 | Dehn test: exactly cube, RD, RT have Dehn-zero centre pyramids; RT open | PENDING | Centre Pyramids vol. | Not in the drafts. The Dehn part is complete. The RT tiling is UNDECIDED: the overnight result is not recorded in the README or the ledger |
| 28 | Dehn on sweeps: zero only at Kelvin and the cube; CO–RD only at μ = 5/3 (B3 permutohedron), which cannot tile | PENDING (one mention) | Space-Fillers vol. | HexOct v8 ch. 16 mentions only "the turned B3 permutohedron… Dehn-zero but fails that count". The sweep result is not in any paper. Complete (settled) |
| 29 | Hopf rings of the White Queen: 12 decagons / 20 hexagons / 30 squares (classical) | PENDING | Queens vol. (+ app view) | No "Hopf" in any paper. Complete; classical, credit Coxeter, Sadoc–Mosseri |
| 30 | Octet (111) slab: octahedra locked, tetrahedra free | PENDING | Space-Fillers vol. | No "Dyskin" in any paper. Complete |
| 31 | #47 Admiral slab interlocks (slides and twists), apart from 4 surface pyramids | PENDING | Space-Fillers vol. (#47 chapter) | Not in #47 v3. Complete (first-order test, calibrated) |
| 32 | HexOct c- and h-tile layers interlock (λ = 1/10), with both controls | PENDING | HexOct vol. | Not in HexOct v8 (its "interlock" means the layers' geometric reach, not Dyskin locking). Complete |
| 33 | Tetrahedron sweep: IQ max at the octahedron; Mahler (11−√33)/4; Dehn zero only at μ = 2, which tiles (known: β-tin) | PENDING | Space-Fillers vol. (Dehn calibration) | Not in a paper. Complete, prior art credited |
| 34 | Roundness max at μ = √n is Lindelöf's theorem (CORRECTION) | PENDING | #94 v2 | #94 v1 has no √3 wording; the wrong wording is only in the Concordance waiting items 13 and 16 and the README. Complete |
| 35 | Dehn screen: all nine OG-family solids nonzero | PENDING (partly landed) | OG vol. (new) | OG itself is exact in #96 (Thm 1) and the cut OG in #95 (Thm 2). The other eight are float only (exact angles needed) |
| 36 | HexOct Dehn: h-pieces zero from 5/24; fixed 10-corner piece for λ ≥ 3/8 tiles alone | LANDED | #98 / HexOct v8 ch. 16 | "s = 0 for the h pieces with λ ≥ 5/24"; Narcissus "fills space alone"; Mahler 34/3. The 5/24–3/8 tiling lead stays open |
| 37 | Admiral network: Q′, I, A each Dehn nonzero | PENDING | Space-Fillers vol. | Not in a paper. Complete (float screen) |
| 38 | Delian walk O(t): Dehn nonzero for t > 0 (144.74°), zero only at the RD | PENDING | #93 v2 (or Bonds next version) | Not in a paper. Complete |
| 39 | Seven golden Dehn-zero truncated tetrahedra (exact in Z[φ]); none silent; approximants under test | PENDING | Space-Fillers vol. (with 41) | Not in a paper. NOT complete: the README has no golden section (only `golden-cuts.json` and `golden-harmonic.json`), and the census runs timed out |
| 40 | Aperiodic-monotile clue checklist | STALE | — | Watch list, no claim |
| 41 | All 6/6 Dehn-zero truncated tetrahedra tile (piece + inverse); conjecture Dehn zero ⇔ tiles | PENDING | Space-Fillers vol. | Not in a paper. Enough for a conjecture section. Still open: the real-cut verification (`verify_real.py`) and wider prior art |
| 42 | White Queen icosians = Poincaré dodecahedral space group; mode counts match ALS to k = 120 | PENDING | Queens vol. | No "Poincaré" in any paper. Complete (cross-check, no cosmology claim) |
| 43 | Narcissus alone stacks any word; 17 keyed copies force a non-periodic word | LANDED | #97 (`2026-11-05-keyed-narcissus`) | "a set of seventeen keyed copies of Narcissus (fourteen carrying Kari's… three relays)" |
| 44 | Narcissus = Goldberg 10-XII (1982), formula 1036-64 | LANDED | #98 + #97 + HexOct v8 | "Its combinatorial type is Goldberg's space-filler 10-XII (1982)… formula 1036-64" |
| 45 | All-equal-edge rectified TI: arrangement known, this form not found (Wikipedia, McCooey) | PENDING | #95 next version (table row) | #95 row still reads "Arrangement known among near-misses; this solid to be checked". A one-row edit; sources are listed |
| 46 | Narcissus halves = two mirror heptahedra √2/8; 7-XXIX needs Goldberg 1978 | LANDED | #98 | "cut on any of its three mirror planes, it splits into two mirror-image heptahedra, each of volume √2/8… needs the 1978 paper" |
| 47 | Golden OGs: face pattern known (Rossiter/McCooey), golden metric forms not found | PENDING | Golden Ladder (ch. 8 = #91) prior-art line | GL/#91 name the Golden OGs but have no prior-art statement for them. Prior-art line only |
| 48 | Route (a) count: one keyed Narcissus ≤ 6 placements per site; pairs need 30 states | PENDING (interim) | One-piece paper (new; `plan-one-piece-narcissus`) | Not in #97. Interim step; the SAT search for a key pattern is next, so not yet writable |
| 49 | PUBLISHED The Golden Ladder v2 | STALE | — | Admin note (the book is now at v5) |
| 50 | #47 v3: octet and cube slabs stack with no connector, never face to face | LANDED | #47 v3 | "Version 3 answers open question 1… Theorem 2"; "200 000 random points each lie in exactly one tile" |
| 51 | Zenodo 24005568 (#97), site tile | STALE | — | Record and deploy note |
| 52 | Zenodo 24005562: #47 Thm 2, Fig. 5 | STALE | — | Marked "done" |
| 53 | Zenodo 24005930 (#98), site tile | STALE | — | Record and deploy note; #98 is already in HexOct v8 ch. 16 |
| 54 | Five in the octet: O > I > D > C > T in every octahedron; 12 inscriptions, 14 (18) chains | LANDED | #99 v2 | "Theorem 1 (Five in the octet)…"; "fourteen chains through all five (eighteen with the truncated tetrahedron)" |
| 55 | Gap pieces: Admiral Caps; 12 pentagonal caps + 30 wedges; Euclid roofs; centre pyramids ×2/3 | LANDED | #99 v2 | "12 Sheriffs… 30 Lone-stars… D − C Euclid's six roofs; C − T four copies of O's centre pyramid at 2/3" |
| 56 | Nested Dodeca-13, 600-cell corner 14.1%, UNITY heart 2/√5; Dodeca-13 fits at ×1/3 | LANDED | #99 v2 | "leave 14.1% of their hull open"; "edge exactly 2/√5 at UNITY's heart"; "fits inside its own central dodecahedron at exactly 1/3" |
| 57 | Cut-and-project rungs; seats; spacing 4.5346; diffraction 0.916 → quasilattice | LANDED | #99 v2 | Table "754 + 466 = 1220"; "√3 φ² = 4.5346". The paper has 0.9969 at 8/5 and 0.9974 at 13/8, not "0.9974 (8/5)" as the waiting item says. The paper is newer |
| 58 | Rock-salt pieces: cubes/truncated cubes + regular octahedra 2(3/8−λ); freedom in 2 deformed pieces | PENDING | HexOct vol. (and #47 pointer) | Not in a paper. Float only; still to do: exact forms, DICTO's names for the deformed pieces, prior art |
| 59 | Football layer at 79.19°, two orientations; chains only | PENDING | Scutoid paper (new) | Not in a paper. Study in progress (step 3 on 7 Nov), so not complete |
| 60 | Zenodo 24012440 (#99 v1), site tile; Sheriff and Lone-star named | STALE | — | Admin note; the names are already in #99 v2 |

## PENDING by destination (38), suggested order

Order: largest coherent group first. Where a paper already exists, a new version is cheaper than a new volume, and that is noted.

1. **Space-Fillers and Lattice Moves (new volume, no folder yet): 8.** Items 4, 28, 30, 31, 33, 37, 39, 41. These hold together: a Dehn screen, the edge-angle count, interlocking, and the Admiral network. 4, 28, 30, 31, 33 and 37 are complete. 41 can go in as a conjecture. 39 first needs its README section and the census result. Per the publish-rhythm rule a new volume needs DICTO's yes (ask before any new record).
2. **#94 v2 (`2026-11-04-harmonic-fingerprint`): 6.** Items 12, 13, 16, 17, 34, 14 (the sweep part). All complete. Item 34 is a correction (√3 = Lindelöf), so the wording of 13 and 16 changes with it. This is the quickest group: a new version of a published paper.
3. **HexOct volume (`book-laws-of-stacking`, v9): 5.** Items 7, 32, 21, 58, 9. 7 is written and read ok; release it first, standalone or as a chapter. 32 is complete. 21 is complete except the "singular continuous" claim. 58 needs exact forms and names. 9 needs DICTO to confirm the build brief.
4. **#92 v3 (`2026-11-04-pyramid-tilings`): 4.** Items 1, 2, 22, 11. 1 and 2 are complete and close open points 1–2. 22 needs a prior-art check. 11 stays as a stated open point. Item 1 also closes #93 open point (1), so it is best done in the same batch as group 5.
5. **Alicia, Queens volume (`book-queens`, v4): 4.** Items 29, 42, 20, 15. 29 and 42 are complete and classical (credit lines ready). 20 needs exact μ*. 15 is float only.
6. **#93 v2 (`2026-11-04-cubic-pairings`): 3.** Items 3, 18, 38, plus the C6 half of item 1. All complete.
7. **OG volume (new) or the OG family paper's next version: 2.** Items 19, 35. Both are float. 35 is partly landed (#95, #96 exact).
8. **The Golden Ladder (`book-golden-ladder`, v6): 2.** Items 5, 47. Short additions to the cuts chapter (#88/#90 rung) and the #91 rung.
9. **Centre Pyramids volume (`book-centre-pyramids`, drafts): 1.** Item 27, which waits on the RT overnight outcome. Items 1–3 also belong here as a chapter, once they are in #92 and #93.
10. **#95 next version (`2026-11-05-og-pentagons`): 1.** Item 45, a one-row table edit. It could ride with the batched one-line pointers already planned for the OG papers.
11. **One-piece paper (new; `plan-one-piece-narcissus`): 1.** Item 48, interim; wait for the SAT step.
12. **Scutoid paper (new): 1.** Item 59, study still running.

## Notes for the Concordance (not applied)

- Seven STALE items (10, 40, 49, 51, 52, 53, 60) and fifteen LANDED items could leave `gaps.waiting`.
- Item 57's diffraction numbers in the waiting list do not match #99 v2. The paper should be treated as correct.
- Item 34's correction affects only the Concordance wording of items 13 and 16 and the `mahler-sweep` README. Published #94 v1 has no √3 claim.
- Item 27: the RT overnight result is not in the study README or the ledger ("UNDECIDED"). Fetch it from dicto-big-brother before writing.
