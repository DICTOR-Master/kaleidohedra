# 2026-11-01 Star Cores book (Cycles of Growth, Part II): cards, plates and the four new solids

Conclusion: the book draft is assembled (papers/book-star-cores, DRAFT PDF in DICTO's reading folder, not published). Every card
picture and plate was rendered here; the four solids DICTO named on 31 October 2026 got the star core treatment with the scripts of
#79 and #81 unchanged: all four are group B (centre-rule star fills its halo); polar spikes fill (layer volumes to 3e-15; 0 overlaps
for D106-D108, test not run on Ophelia's 1722 pieces); exact cores period two (D106, D107 from turn 1, scale t^2/3; D108, D109 from
turn 2, scale t^2(5 + 2 sqrt5)/15); valley rule over steps 2-3: Cube Pearl x1.72 (phi) x1.91 (2), Golden Clasp x1.71 (phi) x1.45 (2);
sharpest dihedral angles 120 (exactly), 125.264, 160.151, 161.095 degrees. Status: in the book draft for DICTO's reading; not in a paper.

Run on dicto-big-brother (~/kres-tmp/star-cores-book, ~/geom/bin/python, float64 unless stated), DICTO Solids v7 (~/kres-tmp/dataset-v7).
- scripts/cards.py: the 60 card pictures (2 x 2 panels; convex: solid, centre-rule star t = phi, polar star rho^2 = phi R^2, polar
  halo; non-convex: solid, centre-rule stars at phi and 2, solid from below; Maedate and Kuwagata: one piece, Kagemusha with five, star
  step one at t = 2 and phi). Imports figs_paper_a.py, star_core.py (study 2026-10-30-star-cores). Piece volumes check against
  kagemusha-variants.json (0.2218; 2 x 0.0752). PNGs reduced to 256 colours for the repo (no dithering).
- scripts/plates.py: six plates (GTI, OG, OCD Stella, Golden Clasp polar stars; Lahdeli valley rule t = 2 after three steps;
  Kagemusha with Kuwagata, step one, t = 2).
- scripts/meta.py -> data/meta-v7.json (name, D-number, symmetry, f-vector, volume, edges, paper, inventory note per solid).
- scripts/new4.py, run_new4.sh -> data/star-cores-new4.json (treatment), polar-spikes-new4.json + polar-new4.log (polar fill with
  overlap test), study2b-new4.json/.log (exact core turns, study2b.py of 2026-10-30-star-cores-exact), valley-new4/star-valley.json
  + valley-new4.log (valley rule, star_valley.py).
- scripts/polar_quick.py -> data/polar-quick-new4.json (halo and layer volumes without the overlap test, for the cards).
- scripts/dihedral_new4.py -> data/dihedral-new4.log (sharpest dihedral angle of D106-D109).
- scripts/typeset.sh: prints the book with papers/print.mjs (playwright from ~/kaleidohedra-check/node_modules).
