# Face to face (#77), 2026-10-30

**One-line conclusion.** Face-to-face tilings by the five Platonic face pyramids are exactly whole Platonic-solid tilings cut
from their centres (cubic tiling, or tetrahedra + octahedra with 2 + 2 round every edge); D and the Cleo-Icos never occur.
The six-piece gluing search of DICTO's pieces (5,143,972 clusters) finds only the tetrahedron (4 Q) and the pentagonal
bipyramid J13 (4 M-S t1 + 2 Hound Tooth, at both tile scales) = two Koca et al. 2020 pentagonal pyramids t1+t2+t1: nothing new.

**Status:** done; paper #77 drafted (papers/face-to-face, DRAFT-77-face-to-face.pdf in papers-to-read).

- scripts/enum_glue.py: the five-pyramids search with evaluation in the workers (run on dicto-big-brother as
  ~/kres-tmp/pyramids/scripts/enum_glue_f2f.py, `DEEP=1 ... 6 12`, 4165 s). Counts 191, 1834, 25683, 363319, 5143972.
- scripts/render_j13.py: Figure 2. data/f2f-deep-L4/L6-results.json: results with positions and merged faces.
- J13 check: equator coplanar, edges 1 to 2e-16, volume (5+√5)/12; each piece on one side of the equator.
