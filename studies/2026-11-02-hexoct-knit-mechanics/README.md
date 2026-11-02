# Knitted HexOct: is the c/h stacking a design dial? (2 November 2026)

DICTO proposed the Knitted HexOct (spec: studies/2026-11-02-knitted-hexoct). This study tests in idealised lattice
models whether the c/h stacking sequence changes mechanical and airflow properties enough to use as a design dial.

**Conclusion:** c/h is a strong dial for straight see-through area (2H 34.7 %, 4H 9.9 %, 3C 3.25 % at rod radius
0.05 a; 10.7×; at 0.1 a: 14.3 % against 0) at identical porosity. It is also a strong dial for free transverse shear
when the sheets are soft in-plane (links-only frame: 3C/2H = 0.057, 17.5×). It is no dial at all for through-thickness
compression, buckling onset or rigidity: identical to 4 digits in every sequence. With stiff sheets the shear dial drops
to 3C/2H = 0.900.
**Status:** done. Typeset `results/hexoct-knit-mechanics.pdf`, copy in ~/Documents/papers-to-read, awaiting DICTO's read.
Not published.

## Findings (all at equal geometry and equal relative density, because every sequence has the same members)
- **Check:** 3C with in-sheet members and pin joints is the octet truss. Its computed E[100] = ρ̄/9 exactly (Deshpande,
  Fleck & Ashby 2001), ratio 1.0000000000 (`data/check_octet.out`).
- **Through-thickness:** C33 (bonded platens), E3 (lubricated, laterally free) and first-buckling strain and stress are
  the same in all 7 sequences, for both joint types and all 3 sheet variants. Ratio 1.000.
- **Transverse shear, bonded platens:** same in all sequences. **Free (1/S55):** 3C/2H = 0.900 (pin, links + in-sheet
  members; periodic), 0.908 (12-sheet block). The cause is the trigonal shear-stretch coupling C14 = 1.31e-3 E_s of 3C.
  It is zero in 2H, 4H and 6H (hexagonal symmetry). Links-only frame: 0.193 against 3.378 (1e-3 E_s), ratio 0.057.
  Graded stacks (5 c + 5 h, either way round) give 0.927, in between.
- **Governing number:** the mean Hägg symbol of the stack (its net c twist), not the share of c sheets. Each h reverses
  the twist sense, so c runs split by an h cancel: ccccchcccc behaves like 2H (3.24), cccccchhhh does not (0.52).
  Fibonacci and 6H behave like 2H.
- **Sheet-stiffness sweep:** the shear dial 3C/2H goes from 0.05 (rigid joints) or 0.001 (pin joints) when the sheets are
  10⁴× softer than the links, to 0.47–0.50 at 0.1×, 0.90 at 1× and 0.999 at 100×.
- **Rigidity (pin joints):** links only gives bars = 3N per periodic cell (Maxwell isostatic count), but every sequence
  has 3 zero-energy macro strains. These are in-plane strains with ε_zz = −(ε_xx+ε_yy)/2, mixed with transverse shear in
  3C. The 6×6×12 cell also has periodic mechanisms (3C 33, 4H 37, 2H 39, 6H 51), each with as many self-stress states
  + 3. This is consistent with Guest & Hutchinson 2003. The finite 12-sheet block has 105 mechanisms in every sequence.
  With in-sheet members every sequence is rigid (0 mechanisms): the h stack (hcp truss) is as rigid as the octet.
- **Energy proxy:** struts buckle at the pinned Euler load and then hold it. Work to 5 % strain: compression
  identical in all sequences. Shear xz: 3C 3.50 against 3.28 (1e-6 E_s), +7 %. Shear yz: identical.
- **Airflow:** porosity is identical (0.9406 at r = 0.05 a). The see-through area depends only on which of the three
  link plan pairs (AB, BC, CA) occur: 2H has one, 4H two, and 3C, 6H, Fibonacci and graded stacks have all three.
  Mean shortest-path tortuosity stays close to 1: 3C 1.0031, 2H 1.0011 (r = 0.05); 3C 1.039, 2H 1.008 (r = 0.1).

## Model
12 sheets, 6 × 6 nodes per sheet, in-plane periodic rectangular cell. a = 1, sheet spacing √(2/3). Rods have
r = 0.05 a, E_s = 1 and ν = 0.3. Pin joints use bars. Rigid joints use 3D Euler–Bernoulli frame members. Sheet variants:
links only; links + in-sheet members 100× stiffer ("stiff" sheets); links + in-sheet members of the same rod ("full").
Tests on the block: bonded and lubricated compression, bonded and free transverse shear (x and y), and in-plane E1, E2
and G12 of the free plate. Volume = cell area × 12 d. A 3D-periodic homogenisation (6×6 Voigt C) is run for 3C, 2H, 4H
and 6H. Fibonacci labels: abaababaab with a → c, b → h. Graded: 5 h at the bottom and 5 c at the top, or the reverse.
Airflow: members are capsules (rods with rounded ends). The open fraction is exact from the plan projection. Tortuosity
uses a 26-neighbour voxel graph (h = 0.02 a; at h = 0.0125 a: 3C 1.0030, 2H 1.0011), with multi-source Dijkstra from the
bottom plane.
Limits: idealised straight rods, no yarn mechanics (no loops, friction, compaction or yarn buckling in tension). The
model is linear-elastic except for the strut-buckling plateau. No Stokes or Darcy permeability solve.

## Files (run on dicto-big-brother, ~/geom/bin/python: numpy 2.5.4, scipy 1.18.1)
- `scripts/lattice.py`: geometry, word from c/h labels, check of 3 + 3 links and 6 in-sheet members per node.
- `scripts/mech.py`: pin and frame models, block tests, periodic C, rigidity ranks, buckling-event energy proxy.
- `scripts/check_octet.py` → `data/check_octet.out`: frame-element rigid-rotation check and octet E[100] = ρ̄/9.
- `scripts/run_all.sh` → `data/mech/*.json` (264 tasks in parallel, ~20 s).
- `scripts/flow.py`, `scripts/run_flow.sh` → `data/flow/*.json` and `*_openmask.npy` (16 runs).
- `scripts/summarize.py` → `data/summary.json`, `data/tables.txt`, `figs/fig1-line-of-sight.png`,
  `figs/fig2-sheet-sweep.png`, `figs/fig3-hagg.png`.
- `results/paper.html` → `results/hexoct-knit-mechanics.pdf` (printed on dicto-big-brother with playwright; footer
  "study, not published").

## Sources checked (2026-11-02)
Library (`~/bin/ask-library`). Queries: "octet truss lattice stiffness stretch-dominated Deshpande Ashby Fleck",
"spacer fabric compression mechanics", "3D woven knitted textile composite preform", "hcp fcc stacking elastic constants
polytypes", "Maxwell rigidity isostatic periodic lattice mechanisms Guest Hutchinson".
Hits, with what was read:
- Keller et al. 2023, hexagonal Si/Ge polytypes (arXiv 2302.10822): p. 1 and p. 11 read. Elastic constants of atomic
  polytypes vary almost linearly with hexagonality. Relevant.
- Lalvani 1990, NASA TM-102635, layered octahedral–tetrahedral truss part count: pp. 1–3 read. Geometry and part counts
  only, no mechanics.
- Goyal & Lakes 2026, micromorphic effects in an octet truss lattice: catalogue entry only.
- Korshunova et al. 2020 and 2021, octet-truss tension and bending: catalogue entries only.
- Krishnamurthy, Akleman et al. 2020 and 2022, woven tiles: page snippets only, not relevant.
- Rodriguez-Horta et al. 2017, close-packed layer interactions: catalogue entries only.
Web (WebSearch, standard). What was opened or seen:
- Deshpande, Fleck & Ashby 2001, JMPS 49, 1747–1769: record and DTIC preprint listing (apps.dtic.mil ADA411734).
- Guest & Hutchinson 2003, JMPS 51, 383–391: record (groups.seas.harvard.edu/hutchinson/papers/guest.pdf listed).
- Liu, Hu, Zhao & Long 2012, Textile Res. J. 82, 11–20 (warp-knitted spacer fabrics for cushioning): abstract and record
  (research.polyu.edu.hk). Liu & Hu 2016, TRJ 86, 3–12: record.
- Pham, Liu, Todd & Lertthanasarn 2019, Nature 565, 305–311 (crystal-inspired "meta-grain" lattices): records only.
- Mouritz et al. 1999, review of 3D fibre textile composite applications: abstract seen, journal record not confirmed in
  the search. Tong, Mouritz & Bannister 2002, *3D Fibre Reinforced Polymer Composites*: book listing.
- Search "hcp truss lattice vs fcc octet truss lattice stiffness stacking sequence": no head-to-head mechanical
  comparison of hcp and fcc truss lattices or of mixed c/h stackings found in the results seen. This is not a
  literature review.
