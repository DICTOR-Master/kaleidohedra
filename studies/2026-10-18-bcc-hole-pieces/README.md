# Resin hole pieces for the OCD double network — DICTO 2026-10-18

DICTO · dictospheres.com

**DICTO 10-18:** "if you have the double network packing of the OCD, five double T bars crossing covers the shape of each unit to fill the remainder of space" — "as they are in the app Golden Bodhi Pyrochlore network, yellow and blue OCDs" — "they represent the individual shapes the resin fill spaces around the network could be cut into" — "five double T bars crossing is the shape between 6 OCDs" — "a central double T bar in the gap between two widely and narrowly spaced OCDs, and when an OCD is placed above and below the other pairs of double Ts space is formed; you can also visualise the double Ts as double crescents".

## Construction (`scripts/hole_piece.py` on dicto-node → `data/hole-piece.json`)
- OCD frame: bcc cube edge a = 4R/3 = 8φ/9; OCD sites (a/2)(i, j, k) all even or all odd (the yellow and blue networks together). The holes between 6 OCDs (bcc octahedral holes) are (a/2)(i, j, k) with one or two odd entries — 3 per OCD; each has a narrow pair of OCDs at a/2 (across a slab) and a wide ring of four at a/√2.
- **Hole piece = the Voronoi cell of a hole among all holes (10 corners), minus the OCDs.** Every point of resin goes to its nearest hole, the holes are all alike under the OCD frame's symmetry, so **one piece shape fills all the resin**.
- Results: exactly 6 OCDs bite (2 at 0.7191, 4 at 1.0170); **volume 0.111898 = (gap per OCD)/3 exactly** (exact: (cell − OCD)/3 with cell (512 + 256√5)/729, OCD (−1000 + 1240√5)/1539); **one solid, genus 0**; sphericity 0.515; centrosymmetric with a mirror plane (no left/right).
- 3D page (`scripts/hole_page.py` → `renders/bcc-hole-pieces.html`): the piece, with its 6 OCDs (yellow/blue by network), the network with all pieces, resin only.
- Open: does the piece read as DICTO's "five double T bars / double crescents"? exact face analysis; Fable check only if wanted.
