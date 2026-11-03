# Tilings by the cubic pairings (DICTO, 2026-11-04; paper #93)

DICTO's idea: carry the method of #92 (edge lengths, face shapes, dihedral angles) over to the cubic pairings.

## Results (proofs in ../../papers/2026-11-04-cubic-pairings/paper.src.html)
- CsCl walk (#90 Prop. 6), P = C n muC*, Q = C n (3-mu)C*: for every mu in (1,3) every tiling (face to face or not) is the
  CsCl tiling. Includes Kelvin (bcc only), CO + O (rectified cubic only), truncated cubes + O, Golden Cut Cubes, Icosaxes/Unborn Axes.
- Delian walk (#51) T(t), O(t): rigid for t in (0,1/3) and (1/3,1); RD alone (t = 0) tiles only as fcc.
- RD centre pyramid R12: face-to-face tilings = one diagonal choice on every square of the cube lattice (B = 2 C6 = 2 R12);
  whole RDs only round corners whose 12 squares all choose them. #77's law fails for the RD.
- Cube pyramid C6: f2f only cubes (#77); lateral edges shared end to end by three; cube tilings give no finite list.
- OPEN: reversed C6 neighbour; non-f2f R12 tilings; mixed sizes; TRD centre pyramids.

## Files
- pairing_checks.py -> data/pairing-checks.log (67 PASS, 0 FAIL), data/pairing-checks.json.
- figs.py -> figures/ (matplotlib; float copies).
Run on dicto-big-brother: ~/geom/bin/python <script>.

## Prior art
#90, #48, #51-#53, #44 Lemma 1, #77, #92; Gabbrielli-Jiao-Torquato 2012 (angle sums); Wikipedia RD / RD honeycomb /
convex uniform honeycomb (Johnson, Grunbaum lists). Library: 4 queries 2026-11-04.
