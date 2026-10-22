# DICTO solids: exact coordinates (math-data dataset)

Created by DICTO · [dictospheres.com](https://dictospheres.com) · Licence CC BY-SA 4.0 · 2026-10-22

Exact geometry of named convex and non-convex polyhedra found or named by DICTO (artist, Osaka), taken from his published papers
and the Kaleidohedra findings archive, with lattice packings where a published result says the solid tiles space. Every number is
exact in a real quadratic field (here always ℚ(√5)) and is re-proved by `check.py` from the data files alone.

## Contents

| path | what |
|---|---|
| `solids/<slug>.json` | one solid: exact corners, faces, f-vector, symmetry, exact volume, edge lengths, normalisation, source, published values, checks |
| `solids/<slug>.off` | the same solid in standard OFF (15-decimal coordinates; same corner order and faces as the JSON) |
| `packings/<slug>.json` | a published space-filling: lattice vectors and the cell's pieces (solid + exact rotation + exact translation) |
| `index.csv` | inventory of every named shape (also the ones not in this dataset), with status, finding, DICTO DOI, whether it is in the dataset and in Polyhedraverse |
| `check.py` | standalone verifier (python3 + sympy) |
| `build/` | the scripts that generated the files (`exactlib.py`, `build_og.py`, `build_pv.py`, `make_index.py`), their logs, and copied source data |
| `published/records.json` | the Zenodo records (latest versions) whose PDFs were used to check the published values |

## File format (solids)

- `field`: `"Q(sqrt(5))"`. Every coordinate is given twice: `exact`, a sympy-parsable string `a + b*sqrt(5)` with rationals `a`, `b`, and
  `decimal`, the same number rounded to 15 decimal places.
- `faces`: lists of 0-based corner indices, counter-clockwise seen from outside (right-hand normal points out).
- `f_vector`, `faces_by_sides`, `squared_edge_lengths` (exact, with counts), `volume` (exact and decimal).
- `symmetry`: Schoenflies symbol, group order, number of rotations, whether it contains the inversion. The group is the full group of
  orthogonal maps taking the corner set to itself about its centroid.
- `scale_note`: the normalisation (each solid is given in the frame of the paper it comes from, so published values can be compared
  directly); `source`: where the geometry was taken from (`Polyhedraverse` id, a Kaleidohedra study, or the paper's closed form);
  `published_values`: values stated in the published paper or archive at this scale, each re-checked by `check.py`.
- `credit` "DICTO", `licence` "CC BY-SA 4.0".

## File format (packings)

`lattice_vectors` (exact), `cell_volume`, and `pieces`: each piece is a solid of `solids/` mapped by `x -> R x + t` with exact `R`
(orthogonal) and `t`. The pieces of one cell, repeated by the lattice, fill space.

## Normalisation

Each solid is in its source paper's frame (stated in `scale_note`), for example: the OG family of #38/#39 in the frame where the
icosidodecahedron has circumradius φ; the DICTO Hecatodihedron in the #28 frame (truncated icosahedron of edge 1/φ); the DICTO
Ogdoecontahedron in the #31 frame (the Hecatodihedron's polar in the unit sphere); the DBT and OTT in the #37 frame (rhombic
triacontahedron of inradius 2/3); the parallelohedra with edge 1.

## How to verify

```
pip install sympy
python3 check.py        # prints a PASS/FAIL table; exit code 0 only if every check passes (add -v for every single check)
```

For each solid it checks: the exact strings parse into ℚ(√5) and the decimals agree; the faces form a closed 2-manifold (each
directed edge once, its reverse once, every vertex link a single cycle), consistently wound; V − E + F = 2; every face exactly
planar; the exact volume is positive (so the winding is outward) and equals the stated value; for convex solids, every face is a
strictly convex polygon wound counter-clockwise from outside and every other corner lies strictly inside its plane; f-vector, face
counts, squared edge lengths; symmetry order, rotations, inversion and the Schoenflies symbol; and every recorded published value.
For each packing: the cell volume, exact orthogonality of the rotations, the sum of piece volumes equals the cell volume exactly, and
no two pieces overlap among all lattice translates that could meet (an exact separating plane for each such pair). Equal volume and
no overlap prove that the pieces tile space. The OFF files are checked against the JSON.

Limits: for the non-convex DICTO Jewel the checks prove a closed, consistently outward-wound polyhedral surface with exact planar
faces and the stated exact volume; freedom from self-intersection is not separately tested. The checker was also run on corrupted
copies (a reversed face, a moved corner, a wrong group order, an extra overlapping piece) and failed each as it should.

## Contents at a glance

| solid | finding | paper | V, E, F | symmetry (order) | convex | volume (exact) | file |
|---|---|---|---|---|---|---|---|
| DICTO Belted Triacontahedron (DBT) | F37a | #37a (V3 for the OTT) | 30, 60, 32 | D3d (12) | yes | -872/81 + (440/81)*sqrt(5) | `dicto-dbt` |
| DICTO Dodeca-13 Needle | F13 | #13 The DICTO Dodeca-13 | 4, 6, 4 | C3v (6) | yes | 3/40 + (-19/600)*sqrt(5) | `dicto-dodeca-13-needle` |
| DICTO Dodeca-13 Wedge | F13 | #13 The DICTO Dodeca-13 | 8, 12, 6 | C2v (4) | yes | 1/10 + (1/20)*sqrt(5) | `dicto-dodeca-13-wedge` |
| DICTO DPHP (Decagon-Pentagon-Hexagon Polyhedron) | #39 (paper; no F number) | #39 The DICTO OG Family | 270, 420, 152 | Ih (120) | yes | -14900661388229463716320/1064860352965629261 + (741665577198656722816/118317816996181029)*sqrt(5) | `dicto-dphp` |
| DICTO FPD (flat pentakis dodecahedron) | F38 | #38 Universal PiTet | 32, 90, 60 | Ih (120) | yes | 130000/9 + (-58000/9)*sqrt(5) | `dicto-fpd` |
| DICTO GTI (golden truncated icosahedron) | F38 | #38 Universal PiTet | 60, 90, 32 | Ih (120) | yes | 85/2 + (-15/2)*sqrt(5) | `dicto-gti` |
| DICTO Truncated-Icosahedral Hecatodihedron (DICTO Hecatodihedron, TIH) | F28 | #28 | 80, 180, 102 | Ih (120) | yes | -365/4 + (189/4)*sqrt(5) | `dicto-hecatodihedron` |
| DICTO Jewel (EKP windows; first called Dragon Jewel) | F10 | #41 The DICTO Jewel | 38, 96, 60 | Th (24) | no | 3 + (3/2)*sqrt(5) | `dicto-jewel` |
| DICTO KRE (Kite-Rhombic Enneacontahedron) | #39 (paper; no F number) | #39 The DICTO OG Family | 92, 180, 90 | Ih (120) | yes | 920/57 + (20/19)*sqrt(5) | `dicto-kre` |
| DICTO Metaxyhexecontahedron | F35 (paper #35a) | #35a | 32, 90, 60 | Ih (120) | yes | 410/27 + (550/81)*sqrt(5) | `dicto-metaxyhexecontahedron` |
| DICTO Ogdoecontahedron (OG) | F31 | #31 | 102, 180, 80 | Ih (120) | yes | -1000/1539 + (1240/1539)*sqrt(5) | `dicto-ogdoecontahedron` |
| DICTO OTT (Octahedrally Truncated Triacontahedron) | F37a | #37a (V3 for the OTT) | 24, 60, 38 | Th (24) | yes | -608/81 + (320/81)*sqrt(5) | `dicto-ott` |
| DICTO Palintriacontahedron | F35 (paper #35b) | #35b | 32, 90, 60 | Ih (120) | yes | 50/3 + (50/9)*sqrt(5) | `dicto-palintriacontahedron` |
| DICTO PHE (Pentagon-Hexagon Enneacontadihedron) | #39 (paper; no F number) | #39 The DICTO OG Family | 180, 270, 92 | Ih (120) | yes | 95875/4617 + (-520/1539)*sqrt(5) | `dicto-phe` |
| DICTO skewed elongated dodecahedron (ED F16) | F7 | Kaleidohedra findings archive | 18, 28, 12 | C2h (4) | yes | 7/2 + (1/2)*sqrt(5) | `dicto-skewed-ed-16` |
| DICTO skewed elongated dodecahedron (ED F18) | F7 | Kaleidohedra findings archive | 18, 28, 12 | C2h (4) | yes | 5/2 + sqrt(5) | `dicto-skewed-ed-18` |
| DICTO skewed rhombic dodecahedron | F1 | Kaleidohedra findings archive | 14, 24, 12 | C2h (4) | yes | 3/2 + (1/2)*sqrt(5) | `dicto-skewed-rhombic-dodecahedron` |
| DICTO TPH | #39 (paper; no F number) | #39 The DICTO OG Family | 80, 210, 132 | Ih (120) | yes | 10437930/1295029 + (3959694/1295029)*sqrt(5) | `dicto-tph` |
| DICTO TPP (Triangle-Pentagon Polyhedron) | #39 (paper; no F number) | #39 The DICTO OG Family | 212, 390, 180 | Ih (120) | yes | -1142247902494640/32258276241813 + (10284735282640/398250323973)*sqrt(5) | `dicto-tpp` |
| DICTO TQH | #39 (paper; no F number) | #39 The DICTO OG Family | 132, 270, 140 | Ih (120) | yes | 770805045/120198224 + (337172409/120198224)*sqrt(5) | `dicto-tqh` |
| DICTO TQHD | #39 (paper; no F number) | #39 The DICTO OG Family | 162, 360, 200 | Ih (120) | yes | 270305422263352121003895663/51860885574873804704126416 + (120804282361507036859626617/51860885574873804704126416)*sqrt(5) | `dicto-tqhd` |
| DICTO TQP | #39 (paper; no F number) | #39 The DICTO OG Family | 140, 300, 162 | Ih (120) | yes | 120305817389620301905755/20607697986465930772682 + (53586855308159545924323/20607697986465930772682)*sqrt(5) | `dicto-tqp` |
Packings: `dicto-skewed-rhombic-dodecahedron-lattice` (F1, DICTO FCC), `dicto-skewed-ed-16-lattice`, `dicto-skewed-ed-18-lattice` (F7):
each solid tiles space by translation.

## How to cite

Cite this dataset and the source papers, each by its DICTO DOI (concept DOI, always the newest version):

- DICTO, *Kaleidohedra by DICTO* (findings archive; F1, F7, F10, F13 entries): DICTO DOI: 10.5281/zenodo.23173809
- DICTO, *The DICTO Dodeca-13*: DICTO DOI: 10.5281/zenodo.23284281
- DICTO, *The DICTO Truncated-Icosahedral Hecatodihedron* (#28): DICTO DOI: 10.5281/zenodo.23360857
- DICTO, *The DICTO Ogdoecontahedron* (#31): DICTO DOI: 10.5281/zenodo.23404688
- DICTO, *The DICTO Metaxyhexecontahedron* (#35a): DICTO DOI: 10.5281/zenodo.23430864
- DICTO, *The DICTO Palintriacontahedron* (#35b): DICTO DOI: 10.5281/zenodo.23430866
- DICTO, *The DICTO Ogdoecontahedron on the Gyrated Octet* (#37a; DBT, OTT): DICTO DOI: 10.5281/zenodo.23484012
- DICTO, *Universal PiTet: The DICTO PiTet Proposition* (#38; GTI, FPD): DICTO DOI: 10.5281/zenodo.23463305
- DICTO, *The DICTO OG Family: Four Steps Up and Four Down* (#39): DICTO DOI: 10.5281/zenodo.23488944
- DICTO, *The DICTO Jewel* (#41): DICTO DOI: 10.5281/zenodo.23496353

Shapes, names and ideas are DICTO's; the exact computations were made with Claude (Anthropic).
Created by DICTO · dictospheres.com · CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
