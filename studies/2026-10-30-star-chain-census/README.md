# Star Chain Census (DICTO, 2026-10-30), first pass

**Idea (DICTO):** run the TI Star steps on all newly discovered and identified solids.

**One-line conclusion (first pass).** The star step (hull of the spike tips at t × the feet of the face perpendiculars) is the inverse of DICTO's growth rule T of Universal PiTet (#38), so the census is a census of T-orbits: it reproduces DICTO's own families (OG → TPH → TQH → TQP → TQHD, #39; GTI → RT → ID → FPD → GTI, #38; TPP → PHE → KRE) and finds period four for TI (#78), GTI/FPD/Palintriacontahedron, DBT and OTT (which feed into the GTI orbit), Icosaxes, Unborn Axes, Tweedledum, Metaxyhexecontahedron, Lahdeli and the Triskelion Tetrahedron, period two for the tetrahedron and the octahedron.
**Status:** first pass, screening only. Fill checks (corner pyramids + edge tetrahedra) hold only where the star lies inside the hull of its tips; many steps fail that (e.g. the octahedron: its spikes stick out of their hull), and the pass/fail flag per chain in the log is per whole chain (too strict). Solids without a centre of symmetry were centred at the mean of their corners (flagged NOSYM); their results are not meaningful yet.

**Found on the way:** the dataset's DICTO FPD (#38) and DICTO Palintriacontahedron have the same shape (corner radii and edge lengths agree to 6 digits after scaling) — a one-name-per-shape question for DICTO.

Files: scripts/census.py; data/census-v1.json, census-v1.log (dataset v5 solids dir, t = φ and 2, 8 steps).
Next: per-step validity, exact T-orbits (gains in Q(√5)) for the period-4 solids, comparison of their gains (the 'new series' idea: TI's gain (17745 − 7712√5)/361 vs ID's 10/φ⁴).
