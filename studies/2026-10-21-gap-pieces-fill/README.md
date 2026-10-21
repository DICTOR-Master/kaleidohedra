# Gap pieces: which fill space alone, in pairs, in threes (DICTO, 2026-10-21)

DICTO: "how many pieces such as CLEO are space filling as pairs etc, just in our tile kit" (the gap pieces, new test).

Step 1 done, dihedral angle screen (`angle_screen.py`, `angle_screen_360.py`, logs): every edge must close to 360 deg (or 180 deg
across a face). Necessary only.
- Fail (proved): AXE alone, CLEO alone, FUJI alone (its 41.81 deg edge), AXE + CLEO.
- Pass (still possible): AXE + FUJI, CLEO + FUJI (63.43 + 79.19 + 37.38 = 180), AXE + CLEO + FUJI; Bodhi B1-B5 alone and in any
  pair/three (all angles multiples of 6 deg, the golden rhombohedra's angles).
- Known: AXE, CLEO = Mosseri-Sadoc tiles t6, t4 at 1/tau; check the library whether they alone fill space.

2026-10-21 resumed: Theaetetus pieces (#29: Aetos, Sphen, Sphenion, Atraktos) added (`angle_screen_theaetetus.py`, log): each fails alone, and
every pair with one of them fails (with each other, AXE, CLEO, FUJI, B1-B5). Kion not in the data yet.
Next: face-to-face growth test on the node, order B1, Bodhi pairs, AXE + FUJI,
CLEO + FUJI.

DICTO · dictospheres.com
