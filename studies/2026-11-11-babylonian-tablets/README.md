# Babylonian clay tablets: the geometry of the tablets themselves (DICTO 11 Nov 2026)
DICTO: "are there any special geometric properties of ancient Babylonian clay tablets that may not have been noticed of the tablets
themselves"; "pilot for babylonian"; "maybe stacking friendly shapes".
Data: HeiCuBeDa Hilprecht (H. Mara, B. Bogacz, P. V. Bayer; heiDATA doi:10.11588/data/IE8CCN, CC BY-SA 4.0): 1,977 tablets of the
Hilprecht Collection (Jena), 3D-scanned; the catalogue gives each tablet's measured box, area, volume and its CDLI period and genre.
## Pilot 1: shape numbers from the catalogue (scripts/tablet_shapes.py; 1,854 whole tablets)
- Typical tablet: length/width 1.24 (quartiles 1.11-1.45), thickness/width 0.50, fill V/(LWT) 0.59 (between an ellipsoid 0.524 and a box).
- Length/width shows NO preference for simple ratios (no peaks at 3:2, 4:3 or the golden ratio): a smooth spread peaking near-square
  (1.05-1.15) with a long tail. A clean negative.
- Fill by period: Ur III 0.641 (quartiles 0.598-0.668, the most standardised), Middle Babylonian 0.640, Old Babylonian 0.608, ED IIIb
  0.564; by genre: Legal 0.656 fullest, Administrative 0.619, Lexical 0.535 roundest.
- SIZE LAW: thickness ~ width^0.678 (bootstrap 95%: 0.647-0.709), while length ~ width^0.99: bigger tablets keep their outline but get
  relatively thinner; the exponent sits at 2/3 (Ur III 0.70, Old Babylonian 0.74, Middle Babylonian 0.64), except ED IIIb (0.26: thickness
  nearly fixed). Lead: is this the hand (a palm-sized pat of clay pressed out) or drying (thickness limited by cracking)? Not yet
  explained; a known-or-not check in the literature is due.
## Next (DICTO's lead: "maybe stacking friendly shapes")
From the 3D meshes: the flatness and curvature of obverse and reverse separately, how each tablet rests on a table (stable resting face,
contact area), and whether tablets of one archive and type would stack or nest. Needs the PLY meshes (dataset part 02, 5.6 GB, first).
## Stacking, first block of meshes (scripts/tablet_stacking.py, stacking_summary.py; part 02, 100 tablets, HS 0239-0661; FINAL ok)
Controls: a box rests stably on its 6 sides, an ellipsoid on its 2 faces only. Stable resting positions = hull faces holding the centre
of mass at least 0.5 mm inside; drops = rolling from random orientations.
- Every tablet has a flatter face (sag 0.195 of the thickness, median) and a rounder one (0.243): obverse and reverse differ.
- Median 4 stable positions; dropped at random a tablet lands on a face 91 % of the time, about half on each; 39 of 100 can also rest
  on an edge, but only from 9 % of drops: standing on edge is possible for many, comfortable for few.
- Old Babylonian mathematical tablets (13): rounder (sag 0.25 / 0.31), yet more of them rest on an edge (8 of 13, 18 % of drops).
This block is mostly of unknown genre; the archive genres (Ur III administrative, legal) are needed to test DICTO's stacking idea.
NEXT: a block rich in Ur III administrative tablets (choose by HS numbers from the catalogue).
## Correction and leads (11 Nov)
The "13 mathematical tablets" of part 02 are about 7 tablets: HS 270b-f are fragments of one (TMH 8, 76), HS 271a-d of another
(TMH 8, 17); the catalogue join ignored letter suffixes. Exclude fragments in the next stacking pass.
LATER (DICTO: "note them for later"): (1) read their CDLI transliterations and check the arithmetic (errors show how tables were
computed); (2) look in the 3D scans for wiped and rewritten areas (working tablets vs archive copies).
