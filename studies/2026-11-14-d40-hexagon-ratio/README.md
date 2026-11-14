VERDICT: D40 (DICTO GTI) has hexagon sides √5 − 1 and 5 − 2√5 in turn, so long : short = 1 + 3√5/5 ≈ 2.3416, exactly as the Golden Ladder census says. Paper #38's "hexagon sides 1 : φ" (and "icosahedron cut at 1/(2 + φ)") is wrong; it describes the Lesser Golden Cut Icosahedron, a different solid.

# D40 hexagon ratio (2026-11-14)

Question: paper #38 gives the GTI's hexagon sides as 1 : φ; the Golden Ladder census gives 1 + 3√5/5. Which is right?

## Exact construction (d40_hex.py, every number a + b√5 with rational a, b)

Definition (#38, DICTO PiTet Proposition): ID = icosidodecahedron of circumradius φ, corners (±φ, 0, 0) cyclic and (±1/2, ±φ/2, ±φ²/2) cyclic; T(S) = {x : v·x ≤ v·v for every corner v of S}; RT = T(ID), GTI = T(RT).

- T(ID): 32 corners (RT). T(RT): 60 corners, all at radius² 15 − 5√5 (radius √10/φ ≈ 1.954, as #38 says); faces 12 pentagons + 20 hexagons; V − E + F = 2.
- Every hexagon has alternating sides:
  - short side² = 45 − 20√5, short side = 5 − 2√5 ≈ 0.5279 (the side shared with a pentagon; the pentagons are regular with this side);
  - long side² = 6 − 2√5, long side = √5 − 1 ≈ 1.2361 (the side shared with another hexagon).
- long/short: (long/short)² = (14 + 6√5)/5 = (1 + 3√5/5)², so long/short = 1 + 3√5/5 ≈ 2.341641. It is not φ (tested exactly).
- As a cut icosahedron (edge 1, cut at x from every corner, hexagon sides x and 1 − 2x): the GTI is the cut at x = 5/(15 + 3√5) = (5 − √5)/12 ≈ 0.2303 (same edge ratio, script check), not at 1/(2 + φ) ≈ 0.2764.
- The DICTO Solids dataset file dicto-gti.json is the same solid: its corners are T(T(ID))'s corners after the coordinate swap (x, y, z) → (−z, −y, −x) (the mirror orientation of the ID), with identical edge lengths and ratio.

Controls: icosahedron cut at 1/3 gives regular hexagons (ratio 1, Archimedean); cut at 1/(2 + φ) gives ratio exactly φ; cut at 5/(15 + 3√5) gives exactly 1 + 3√5/5 and matches the GTI. Log: d40_hex.log (FINAL ok line).

## What each source claims

"Ratio" means long side over short side of the alternating hexagon in every source below; only the value differs.

| Source | Claim (quoted) | Right? |
|---|---|---|
| Paper #38 Universal PiTet (v1 paper.html and v2 paper-v2.html; published, 10.5281/zenodo.23463306) | Table 1: "DICTO GTI · 12 regular pentagons, 20 hexagons, sides 1 : φ · … the icosahedron cut at 1/(2+φ) of each edge, not 1/3"; abstract: "DICTO GTI (Golden Truncated Icosahedron: hexagon sides 1 : φ)"; §Duals: "the DICTO GTI is the member whose hexagon sides are in the ratio 1 : φ" | **Wrong.** 1 : φ and the cut 1/(2 + φ) give the Lesser Golden Cut Icosahedron. The GTI's two hexagon sides are 5 − 2√5 and √5 − 1, ratio 1 : (1 + 3√5/5); cut (5 − √5)/12. The rest of #38's GTI row (12 regular pentagons, 20 hexagons, 60 corners on one sphere of radius √10/φ) is right. |
| The Golden Ladder (book, v6, 10.5281/zenodo.24091238), §2 + Table 4.1 + Table 4.2 note | "Its ratio is long side over short side"; Table 4.1: "DICTO GTI · 20 · 1 + 3√5/5"; Table 4.2 note: "DICTO's GTI, despite its name, is not one of the ten: its ratio is 1 + 3√5/5"; Table 4.3: cut 5/(15 + 3√5) ≈ 0.2303 | **Right.** |
| Census study (papers/golden-truncated-triangles/fet-exact.md, 11-02, sympy from the dataset) | "2.341641 = (5 + 3√5)/5: gti" | **Right** ((5 + 3√5)/5 = 1 + 3√5/5). |
| Memory open-work 11-02 "GOLDEN TRUNCATED TRIANGLES: EXACT PROOF … GTI 20 1+3√5/5" | 20 faces, ratio 1 + 3√5/5 | **Right.** |
| DICTOnary of Atoms: Quanta of Space II (v1.3, 10.5281/zenodo.24037771), PiTet section table, and its ja/zh/ar/fa editions | "DICTO GTI · 12 regular pentagons, 20 hexagons, sides 1 : φ (icosahedron cut at 1/(2 + φ) of each edge)"; the D40 catalogue entry itself gives no ratio | **Wrong** (copied from #38). |
| concordance.json names, D40 | desc "…whose hexagons alternate sides in ratio 1 : φ", flagged desc_unsure | **Wrong**; corrected in this commit to 1 + 3√5/5. |

The two values are not two conventions for one number: neither φ nor 1/φ nor any ratio of the GTI's two edge lengths equals φ. #38 defines the right solid (T(RT), the same as the dataset file) but its one-line description of the hexagons was wrong.

## Records

- Erratum appended to concordance.json "errata" for #38 and for the DICTOnary (next version, DICTO decides). No book or paper text edited.
- Files: d40_hex.py (script), d40_hex.log (run log), dataset-gti-vertices.json (dataset corners, input).

Run notes: the first run stopped at the Archimedean control (a regular hexagon has one side length; the script expected two) and printed the dataset as "not equal" before testing orientation. Both were script faults, fixed; the second run ended FINAL ok (about 15 min, under 1 GB).
