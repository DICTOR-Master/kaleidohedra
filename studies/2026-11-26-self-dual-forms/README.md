# The Vacuus, Resonus and Tacitus of McCooey's self-dual polyhedra (26 November 2026)

DICTO · study, V SF A project. The idea is **DICTO's** (26 Nov): "self-duals may be interesting to explore for vacuus, resonus and
tacitus studies"; "browse his self duals for candidates"; "check all his forms as all unusual". Naming rule (DICTO, FIRM): the solids
keep their finders' names and credit and get no new names; their Vacuus, Resonus and Tacitus forms are DICTO's constructions.

> **Status box.** Study note, not published. Census in floating point from McCooey's 30-digit coordinates; every flagged silence
> rechecked at 40 digits. Resume: everything committed; nothing running.

## The solids and their credit

| what | credit | source checked |
|---|---|---|
| the 162 polyhedra, their canonical coordinates and names | **David McCooey**, Visual Polyhedra (dmccooey.com/polyhedra), pages "Greater Self-Dual Solids", "Improper Self-Dual Polyhedra", "Symmetries of Canonical Self-Dual Polyhedra"; data files <name>.txt | the three pages and all 162 data files, fetched 26 Nov 2026 (source/) |
| the graphs of the self-duals up to 16 faces | generated with **plantri**, G. Brinkmann and B. D. McKay, "Fast generation of planar graphs", MATCH 58(2) (2007) 323–357 (cited by McCooey) | McCooey's page; the paper not opened |
| construction and classification of all self-dual spherical polyhedra | **D. Archdeacon and R. B. Richter**, J. Combin. Theory Ser. B (1992) (via their radial graphs) | cited in arXiv:2108.01058 (read: abstract and introduction); the paper not opened |
| existence of the canonical form (every edge tangent to one sphere) | the Koebe–Andreev–Thurston midsphere theorem (cited by McCooey through MathWorld, "Canonical Polyhedron") | MathWorld page named on McCooey's page; not opened |
| the eleven "Greater Self-Dual Solids" (28, 40, 76 faces, tetrahedral symmetry) | **McCooey**; no earlier source found | web search 26 Nov 2026 (no source on these face counts); McCooey's page gives none |
| the pyramids among them | classical | |

## Results (scripts/forms.py, scripts/part2.py; data-forms.json, data-part2.json; logs-*.txt; both FINAL ok)

1. **All 162 are geometrically self-dual.** For each, the canonical dual (poles of the face planes; same size, since every edge is
   tangent to the unit sphere) is carried onto the solid by an orthogonal map: a rotation for 123, a map with a reflection for 39
   (the dual is the mirror image; McCooey's improper self-duals).
2. **The polar link, read in the solid itself (all 162).** Through that map, the Resonus is exactly the set of planes perpendicular
   to the solid's own corner directions, and the Vacuus exactly the set of planes perpendicular to its own edge directions. (Lean M1:
   the Resonus plane of a facet is perpendicular to the polar corner; the Vacuus plate of an edge is perpendicular to the polar edge.)
3. **Resonus and Vacuus never share a plane** in any of the 162, and no Resonus plane is a mirror; Vacuus plates on mirrors occur
   only where the solid has mirrors (e.g. pyramids: Self-Dual Hexadecahedron #2, 30 plates, 15 on mirrors).
4. **Tacitus: no silence beyond symmetry**, with unit weights or with area weights. Two candidates were settled at 40 digits as
   near misses: Self-Dual Tetracontahedron #2, degree 4 with area weights, energy 6.27·10⁻¹³ (nonzero; the double-precision pass
   had flagged it); Self-Dual Hexadecahedron #8, degree 2 with area weights, energy 3.98·10⁻⁹ (nonzero).
5. **Partial Vacuus:** no self-dual has a special pit depth at which every pit wall lies on a face plane of its own dual.

## Faults met and fixed (for the record of the run)
- McCooey's files repeat a constant as a formula on a later line ("C0 = 2 + sqrt(5) - ..."); the first reader took the formula's
  leading number and misread 5 solids. Fixed: the first, numeric value is kept. All results above are from the fixed runs.
- A first high-precision pass refined the constants with a root finder that could jump to another root of the same polynomial;
  replaced by McCooey's 30-digit values as given.

## LEADS
1. Exact (algebraic) proof of the two near misses' nonzero energies (resultants over his minimal polynomials).
2. The self-duality map as a symmetry of the combined Vacuus + Resonus (it swaps "own corners" and "own edges" data): its order and
   whether it is an involution (Archdeacon–Richter's strongly involutive self-duals, arXiv:2005.03866).
3. Why no Resonus plane is a mirror in any self-dual here: study 2026-11-25-quality-overlaps proved that a Resonus lying in the
   mirrors forces central symmetry; check whether a self-dual polyhedron can be centrally symmetric (if not, this is a theorem).
4. The smaller tables (419 378 canonical self-duals up to 16 faces) only through McCooey's representatives here; no bulk download.
