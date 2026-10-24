# DICTO solids: exact coordinates (math-data dataset)

Created by DICTO · [dictospheres.com](https://dictospheres.com) · Licence CC BY-SA 4.0 · 2026-10-22 · **Version 2: 2026-10-24**

Exact geometry of named convex and non-convex polyhedra found or named by DICTO (artist, Osaka), taken from his published papers
and the Kaleidohedra findings archive, with lattice packings where a published result says the solid tiles space, and the published
packings that do not fill space. Every number is exact in a real number field stated in each file (ℚ(√5) for all solids but two; ℚ(∛2)
for Samson and Delilah, version 2) and is re-proved by `check.py` from the data files alone; the only exception is the unit-volume copy
of each solid, whose scale is a cube root (stored exactly as a symbolic expression, with decimal corners).

## What is new in version 2 (2026-10-24)

- **Six solids**, the six DICTONIC SOLIDS of DICTO's papers #48 *The Golden Split* and #51 *The Delian Bond*: the Icosaxes and the Unborn
  Axes (convex truncated octahedra), the Lotus Jewel Axes and the Dodecaxes (non-convex: the Icosaxes with 8 Tricap dents, the Unborn Axes
  with 8 Tricap keys), and Samson and Delilah (the octet's two pieces at the Delian bond, in ℚ(∛2)).
- **Three fills**, the three DICTONIC BONDS: the golden bond (Icosaxes + Unborn Axes), the keyed bond (Lotus Jewel Axes + Dodecaxes, one
  fixed keying) and the Delian bond (8 Samsons + 4 Delilahs per cube).
- **A second number field**: the `field` key now names the field of each file, `"Q(sqrt(5))"` or `"Q(2**(1/3))"`; `check.py` reads both
  exactly (every version 1 check is unchanged and passes as before).
- **Non-convex solids as convex ∓ Tricaps**: a `decomposition` key, re-proved by `check.py`; the keyed bond is proved from the golden bond.
- **`universal_number` column in `index.csv`**: catalogue numbers given by earlier creators (see below); **`proposed-t-numbers.md`**: the
  DICTO T-numbers that could be given next, for DICTO to approve (none is used yet).
- The symmetry group is now the group of the solid (corners **and** faces); for every convex solid, and for the DICTO Jewel, it is the same
  group as before.

## Contents

| path | what |
|---|---|
| `solids/<slug>.json` | one solid: exact corners, faces, f-vector, symmetry, exact volume, edge lengths, normalisation, source, published values, checks |
| `solids/<slug>.off` | the same solid in standard OFF (15-decimal coordinates; same corner order and faces as the JSON) |
| `solids/<slug>-unit-volume.off` | the same solid scaled to volume 1 (see Normalisation) |
| `packings/<slug>.json` | a published space-filling: lattice vectors and the cell's pieces (solid + exact rotation + exact translation) |
| `packings-nonfilling/<slug>.json` | a published packing that does not fill space: the same format, with `"kind": "packing, not a fill"` and the exact density |
| `index.csv` | inventory of every named shape (also the ones not in this dataset), with its universal number (if any), status, finding, DICTO DOI, whether it is in the dataset and in Polyhedraverse |
| `proposed-t-numbers.md` | proposed DICTO T-numbers for the shapes with no earlier number (a proposal for DICTO; not used anywhere yet) |
| `check.py` | standalone verifier (python3 + sympy) |
| `build/` | the scripts that generated the files (`exactlib.py`, `build_og.py`, `build_pv.py`, `build_extra.py`, `build_v2.py`, `make_index.py`), their logs, and copied source data (version 2: the three exact study scripts of #48 and #51 in `build/sources/`) |
| `published/records.json` | the Zenodo records (latest versions) whose PDFs were used to check the published values |

## File format (solids)

- `field`: `"Q(sqrt(5))"` or (version 2, Samson and Delilah) `"Q(2**(1/3))"`. Every coordinate is given twice: `exact`, a sympy-parsable
  string in that field, `a + b*sqrt(5)` or `a + b*2**(1/3) + c*2**(2/3)` with rationals `a`, `b`, `c`, and `decimal`, the same number
  rounded to 15 decimal places. (Exact signs in ℚ(∛2) are decided by the norm a³ + 2b³ + 4c³ − 6abc, which has the sign of the number.)
- `faces`: lists of 0-based corner indices, counter-clockwise seen from outside (right-hand normal points out).
- `f_vector`, `faces_by_sides`, `squared_edge_lengths` (exact, with counts), `volume` (exact and decimal).
- `symmetry`: Schoenflies symbol, group order, number of rotations, whether it contains the inversion. The group is the full group of
  orthogonal maps taking the solid to itself about its centroid: corners to corners and faces to faces (version 2; for a convex solid this
  is the symmetry of the corner set, as in version 1; the dented and keyed solids have corner sets with more symmetry than the solids).
- `decomposition` (version 2, non-convex solids only): `base_solid` (a convex solid of this dataset), `operation` (`minus`: dents,
  `plus`: keys), `tricap_volume`, and the 8 `tricaps`, each with the centre of the Unborn it belongs to (`unborn_centre`), its `apex` and
  its three `base` corners (exact).
- `version_added`: 2 for the solids added in version 2.
- `scale_note`: the normalisation (each solid is given in the frame of the paper it comes from, so published values can be compared
  directly); `source`: where the geometry was taken from (`Polyhedraverse` id, a Kaleidohedra study, or the paper's closed form);
  `published_values`: values stated in the published paper or archive at this scale, each re-checked by `check.py`.
- `unit_volume`: the solid scaled to volume 1 (see Normalisation): `scale_exact` (sympy-parsable, `(V)**(-1/3)` with V the exact
  volume), `scale_decimal`, `centre` (exact and decimal, with its kind), `vertices_decimal` (15 decimal places; same corner order and
  faces as the solid).
- `credit` "DICTO", `licence` "CC BY-SA 4.0".

## File format (packings)

`lattice_vectors` (exact), `cell_volume`, and `pieces`: each piece is a solid of `solids/` mapped by `x -> R x + t` with exact `R`
(orthogonal) and `t`. The pieces of one cell, repeated by the lattice, fill space.

Version 2: `field` may be `"Q(2**(1/3))"` (the Delian bond). A fill by non-convex pieces (the keyed bond) has `"proof": "decomposition"`,
`base_packing` (a convex fill of this dataset with the same lattice and placements), `keying` (which side each Tricap is on) and the same
`pieces` list; it is proved from the base fill and the pieces' `decomposition` (see How to verify).

`packings-nonfilling/<slug>.json` has the same fields plus `kind` "packing, not a fill", `paper`, and `density`: `exact` (the published
closed form), `decimal`, `published_percent` (as printed in the paper) and `published_in`. The pieces of one cell, repeated by the
lattice, do not overlap; the rest of space is empty.

## Normalisation

Each solid is in its source paper's frame (stated in `scale_note`), for example: the OG family of #38/#39 in the frame where the
icosidodecahedron has circumradius φ; the DICTO Hecatodihedron in the #28 frame (truncated icosahedron of edge 1/φ); the DICTO
Ogdoecontahedron in the #31 frame (the Hecatodihedron's polar in the unit sphere); the DBT and OTT in the #37 frame (rhombic
triacontahedron of inradius 2/3); the parallelohedra with edge 1. The DICTO OCD Stella is in the OG's #31 frame, cut by the Voronoi
cell of the OG's body-centred cubic packing whose joint hexagons point along (±1, ±1, ±1).

Second common size, unit volume (DICTO 2026-10-23): every solid also carries a copy of volume 1, scaled by s = V^(-1/3) about its
centre. The centre is the exact corner centroid: for 21 of the 23 solids this is the origin of the paper frame; the Dodeca-13 Wedge
and Needle do not sit at the origin, so they are scaled about their corner centroid (stated in `unit_volume.centre.kind`). Cube roots
leave ℚ(√5), so s is stored as an exact symbolic expression and the scaled corners as decimals (15 places, as everywhere else).

Version 2 frames: the Icosaxes, Unborn Axes, Lotus Jewel Axes and Dodecaxes are in the #48 frame (regular icosahedron of edge 1, lattice
spacing φ); the Icosaxes and the Lotus Jewel Axes are centred at the icosahedron's centre, the Unborn Axes and the Dodecaxes at their own
centre (the cube centre (φ/2)(1, 1, 1) of #48 moved to the origin). Samson and Delilah are in the frame of the #51 study
(`octet_special_exact.py`): the octet in a cube of side 2, so the octet edge is √2 (#51 states its values at octet edge 1: divide lengths by
√2 and volumes by 2√2; there Samson and Delilah have volume √2/6, here 2/3); each is moved so that its centre is at the origin. √2 is not
in ℚ(∛2), so this frame keeps everything in one field. All six sit at the origin, which is their corner centroid.

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
Version 2: the same checks in ℚ(∛2) for Samson and Delilah. For the non-convex Lotus Jewel Axes and Dodecaxes, besides the checks above
(as for the DICTO Jewel), the `decomposition` is re-proved: each of the 8 Tricaps is #48's, in its cyclic orientation (its three base corners
are corners of the Unborn at the stated centre, the cyclic permutations of (±φ/2, ±1/(2φ), 0), and its apex is a corner of that Unborn's
dodecahedron cube; the mirrored Tricap fails this test), of volume (3 − √5)/24; its base corners are corners of the convex solid on one of
its faces, the apex strictly inside the convex solid (a dent) or strictly outside that face (a key); the Tricaps are pairwise
interior-disjoint (exact separating planes); the corners are the convex solid's corners plus the 8 apices; every face lies in a face plane of
the convex solid or of a Tricap; and the exact volume equals the convex volume minus (plus) 8 Tricaps (√5 = 1 + 2√5/3 − 8(3 − √5)/24;
2 = 1 + √5/3 + 8(3 − √5)/24).

For each packing: the cell volume, exact orthogonality of the rotations, the sum of piece volumes equals the cell volume exactly, and
no two pieces overlap among all lattice translates that could meet (an exact separating plane for each such pair). Equal volume and
no overlap prove that the pieces tile space. For the keyed bond (non-convex pieces, version 2): its base fill, the golden bond, passes
all its checks (a tiling by convex pieces); the keyed bond has the same lattice and the same placements, each keyed piece being the
base fill's piece with its Tricaps removed or added; the piece volumes sum to the cell volume; and every dent equals exactly one key moved by
a lattice vector, and vice versa. Each Tricap removed from an Icosaxes is therefore added to exactly one Unborn Axes: only the owner of each
Tricap changes, so the keyed pieces tile space too (any keying would; this file fixes the one with every Tricap on the dodecahedron side).
For each non-filling packing: the kind, exact lattice vectors (decimals agree, nonzero
cell), the cell volume, orthogonal rotations and convex pieces, density = sum of the piece volumes / cell volume exactly equal to the
stated published closed form, its decimal (below 1), the published percentage equal to that decimal at the paper's precision, and no
overlaps (the same separating-plane test). For each unit-volume copy: the scale is exactly (stated volume)^(-1/3) (checked to 50
digits), the centre is the exact corner centroid, every decimal corner is centre + s (corner − centre) to 1e-14, and the decimal solid
has volume 1 to 1e-12. The OFF files, plain and unit-volume, are checked against the JSON.

Limits: for the non-convex DICTO Jewel, Lotus Jewel Axes and Dodecaxes the checks prove a closed, consistently outward-wound polyhedral
surface with exact planar faces and the stated exact volume; freedom from self-intersection is not separately tested (for the Lotus Jewel
Axes and the Dodecaxes the decomposition checks above give the same solid as convex ∓ disjoint Tricaps by volume, corners and face planes,
but not a separate surface-intersection test). The checker was also run on corrupted
copies (a reversed face, a moved corner, a wrong group order, an extra overlapping piece; for the second pass, a shrunken
non-filling lattice, a wrong published percentage and a moved unit-volume corner; for version 2, a moved corner of Samson (ℚ(∛2)) and of
the Lotus Jewel Axes, mirrored Tricaps, and a keyed bond with a moved piece) and failed each as it should.

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
| DICTO OCD Stella | F31a | #31a The DICTO OCD Stella | 48, 96, 50 | Th (24) | yes | -4064/729 + (2240/729)*sqrt(5) | `dicto-ocd-stella` |
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
Version 2 (the six DICTONIC SOLIDS):

| solid | finding | paper | V, E, F | symmetry (order) | convex | volume (exact) | field | file |
|---|---|---|---|---|---|---|---|---|
| Icosaxes | – | #48 The Golden Split | 24, 36, 14 | Oh (48) | yes | 1 + (2/3)*sqrt(5) | ℚ(√5) | `dicto-icosaxes` |
| Unborn Axes | – | #48 The Golden Split | 24, 36, 14 | Oh (48) | yes | 1 + (1/3)*sqrt(5) | ℚ(√5) | `dicto-unborn-axes` |
| Lotus Jewel Axes | – | #48 The Golden Split | 32, 84, 54 | Th (24) | no | sqrt(5) | ℚ(√5) | `dicto-lotus-jewel-axes` |
| Dodecaxes | – | #48 The Golden Split | 32, 84, 54 | Th (24) | no | 2 | ℚ(√5) | `dicto-dodecaxes` |
| Samson | – | #51 The Delian Bond | 16, 24, 10 | Td (24) | yes | 2/3 (= √2/6 at octet edge 1) | ℚ(∛2) | `dicto-samson` |
| Delilah | – | #51 The Delian Bond | 6, 12, 8 | Oh (48) | yes | 2/3 (= √2/6 at octet edge 1) | ℚ(∛2) | `dicto-delilah` |

Packings: `dicto-skewed-rhombic-dodecahedron-lattice` (F1, DICTO FCC), `dicto-skewed-ed-16-lattice`, `dicto-skewed-ed-18-lattice` (F7):
each solid tiles space by translation. Version 2, the three DICTONIC BONDS: `dicto-golden-bond` (Icosaxes at φℤ³, Unborn Axes at
φℤ³ + (φ/2)(1, 1, 1), #48 Main theorem), `dicto-keyed-bond` (Lotus Jewel Axes and Dodecaxes at the same places, every Tricap on the
dodecahedron side, #48 Theorem 3), `dicto-delian-bond` (8 Samsons and 4 Delilahs per cube of side 2, #51, in ℚ(∛2)).

Packings that do not fill space (`packings-nonfilling/`), each with its exact density as published:

| packing | paper | lattice, pieces per cell | density (exact) | published |
|---|---|---|---|---|
| `dicto-ogdoecontahedron-bcc-packing` | #31 | body-centred cubic, 1 OG | (9225 − 3915√5)/608 | 77.43% |
| `dicto-ocd-stella-bcc-packing` | #31a | the same body-centred cubic lattice, 1 OCD Stella | 151/2 − 267√5/8 | 87.12% |
| `dicto-dbt-gyrated-octet-packing` | #37a | gyrated octet, 2 DBTs (a layer and its mirror-twin layer) | 493/6 − 73√5/2 | 55.02% |
| `dicto-ott-octet-packing` | #37a | octet (face-centred cubic), 1 OTT | 176/3 − 26√5 | 52.89% |

## Universal numbers (index.csv)

`universal_number` gives the number a shape already has in an established catalogue, numbers given by earlier creators first (DICTO
2026-10-23): Johnson solids J1–J92 (Johnson 1966), the uniform index U of R. E. Maeder's list of the uniform
polyhedra (U5 = regular octahedron), Wenninger's model numbers W1–W119 (*Polyhedron Models*, 1971), George W. Hart's stellation lists (1996), and the
Mosseri–Sadoc tiles t1–t6 (numbering as tabulated by Koca et al. 2020, arXiv:2009.07048; DICTO's pieces are these scaled by 1/τ). Several
numbers are separated by "; ". Only numbers we are sure of are given; the cell is empty where a shape has no such number. DICTO T-numbers
(his universal piece numbers) are not used in any published paper yet; `proposed-t-numbers.md` proposes them for DICTO to approve.

## How to cite

Cite this dataset and the source papers, each by its DICTO DOI (concept DOI, always the newest version):

- DICTO, *Kaleidohedra by DICTO* (findings archive; F1, F7, F10, F13 entries): DICTO DOI: 10.5281/zenodo.23173809
- DICTO, *The DICTO Dodeca-13*: DICTO DOI: 10.5281/zenodo.23284281
- DICTO, *The DICTO Truncated-Icosahedral Hecatodihedron* (#28): DICTO DOI: 10.5281/zenodo.23360857
- DICTO, *The DICTO Ogdoecontahedron* (#31): DICTO DOI: 10.5281/zenodo.23404688
- DICTO, *The DICTO OCD Stella* (#31a): DICTO DOI: 10.5281/zenodo.23430870
- DICTO, *The DICTO Metaxyhexecontahedron* (#35a): DICTO DOI: 10.5281/zenodo.23430864
- DICTO, *The DICTO Palintriacontahedron* (#35b): DICTO DOI: 10.5281/zenodo.23430866
- DICTO, *The DICTO Ogdoecontahedron on the Gyrated Octet* (#37a; DBT, OTT): DICTO DOI: 10.5281/zenodo.23484012
- DICTO, *Universal PiTet: The DICTO PiTet Proposition* (#38; GTI, FPD): DICTO DOI: 10.5281/zenodo.23463305
- DICTO, *The DICTO OG Family: Four Steps Up and Four Down* (#39): DICTO DOI: 10.5281/zenodo.23488944
- DICTO, *The DICTO Jewel* (#41): DICTO DOI: 10.5281/zenodo.23496353
- DICTO, *The Golden Split: Icosahedra, Unborns and AXE Become Two Convex Space-Fillers* (#48; Icosaxes, Unborn Axes, Lotus Jewel Axes,
  Dodecaxes): DICTO DOI: 10.5281/zenodo.23596362
- DICTO, *The Delian Bond: Samson, Delilah and the Octet Between Kepler's Rhombic Dodecahedron and the Cube* (#51; Samson, Delilah):
  DICTO DOI: 10.5281/zenodo.23606828

Shapes, names and ideas are DICTO's; the exact computations were made with Claude (Anthropic).
Created by DICTO · dictospheres.com · CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
