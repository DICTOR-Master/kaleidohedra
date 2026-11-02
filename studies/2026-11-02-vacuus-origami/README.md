# 2026-11-02 DICTO Vacuus origami (DICTO proposed 2026-11-02)

Conclusion: every DICTO Vacuus with its centre strictly inside all face planes folds as modular origami, one flat fan per face (the open centre
pyramid, no base). Nested at the centre, the fans make every fin a double wall. The 7 solids here need 1 to 3 distinct nets each (fan angles
88.77°–330°, all < 360°). Folded by the exact dihedrals, every net returns to its true pyramid to within 3e-15 of the longest strut. Fold the
cube first: 6 copies of one net, every fold 120°. Status: study note (vacuus-origami.pdf + 7 nets PDFs in DICTO's reading folder), not published.

Principle: one sheet cannot fold the whole Vacuus, because 3 or more fins meet along each strut O–v. The open pyramid of one face is a fan of triangles
O–v_k–v_(k+1) that folds from one flat net. The two pyramids on either side of an edge meet back to back along its fin.

Solids: cube, cuboctahedron (two face types: 8 triangle fans + 6 square fans; all 24 fins lie in the 4 central hexagons), David, Kagemusha (D86,
3 net types × 10; the central pentagon disc of five 72° fins is shown in its assembly guide), Cube Pearl, Golden Clasp and TI Star core (One-Strut Vacuus).

Run on dicto-big-brother (~/kres-tmp/vacuus-origami, ~/geom/bin/python). Each step ran as parallel processes (xargs -P 7 or shell jobs), all
waited for; nothing is left running.
- scripts/qf.py: exact Q(√d) arithmetic (copy of the census file).
- scripts/fan.py <solid json> <out>: per face, the strut lengths, rim edges and fan angles θ (cos²θ exact), and the fold dihedrals ψ (cos²ψ exact
  + sign). It also finds the fin letters, the net types (cyclic sequences of strut class, fin and neighbour type, refined until stable; mirror
  test) and the central-disc fins. Closure check: the flat net is folded by ψ and compared with the true corners of every face of its type.
  Output: data/<solid>.json. Inputs: data/inputs.txt (classical census coordinates; DICTO Solids v7).
- scripts/render.py: assembled + exploded views (own z-buffer rasteriser, paper white, ≥ 2 px edges, wall gap 0.8 % R) → renders/*.png.
- scripts/nets.py: the A4 nets PDF per solid. Page 1 is the assembly guide; then every copy. One true scale per solid (the largest net fills
  186 × 249 mm; longest strut rounded down to whole mm). Lines: cut solid, valley dashed, mountain dash-dot (seen from the printed side = the
  inside of the pyramid). Tab rule: each triangle O–A–B (A→B counter-clockwise on the printed side) carries a rim half-tab on the half of AB next
  to B; the neighbour runs B→A, so every rim gets two half-tabs, one per pyramid of the fin pair, each folded 180° onto the neighbour. One seam tab
  per fan is glued under triangle 1. Overlaps are checked with shapely. Writes data/vacuus-origami-nets-<solid>.json (scale, pages).
- scripts/typeset.py: paper.html, printed with print.mjs (A4) in ~/kres-tmp/vacuus/print/vacuus-origami → vacuus-origami.pdf (8 pages).

Checks: fold error ≤ 1.9e-15, closure ≤ 3.1e-15, rim-edge error ≤ 3e-15 (relative to the longest strut); fan angles < 360°; Σ sides = 2E;
no overlapping pieces; every net in one piece and on its page. Every page (overview 8 + nets 137) was looked at.

| Solid | Net types | Longest strut | Pages |
|---|---|---|---|
| Cube | N1 square ×6 | 96 mm | 7 |
| Cuboctahedron | N1 triangle ×8, N2 square ×6 | 114 mm | 15 |
| David | N1 triangle ×4 (fan 330°) | 114 mm | 5 |
| Kagemusha | N1, N2, N3 triangle ×10 each | 153 mm | 31 |
| Cube Pearl | N1 square ×6, N2 hexagon ×12 | 120 mm | 19 |
| Golden Clasp | N1 quadrilateral ×12, N2 hexagon ×8, N3 octagon ×6 | 124 mm | 27 |
| TI Star core | N1 pentagon ×12, N2 hexagon ×20 | 142 mm | 33 |

Prior art (all sources are listed in the PDF): 8 library queries (ask-library) and 8 web searches. Known: unit/modular origami (Sonobe; Fuse 1990
and later; Riskin 2007; Hartl–Kwickert 2012), paper nets with tabs (Wenninger 1971; Stella), paper dissections into the centre pyramids (Walser 2020,
the cube, from 1:√2 rectangles; Constantino–de Souza 1998, the tetrahedron, as an sp³ model; Wheeler models), Leonardo/Hart vacuus frames, and
computational origami (Mitani, Lang, Benbernou–Demaine–Demaine–Ovadya, O'Rourke). New within these checks: open centre pyramids nested so that every
fin is a double wall (the Vacuus itself as the folded object), the two-half-tab orientation rule, the exact fold dihedrals with the closure check, and
the nets for DICTO's solids.

Nets PDFs are kept only in ~/Documents/papers-to-read (not in git); regenerate them with nets.py.
