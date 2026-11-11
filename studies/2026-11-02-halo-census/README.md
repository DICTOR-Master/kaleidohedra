# 2026-11-02 Stars and halos census (DICTO: "are all hulls recorded / prior art as shapes?!")

Conclusion: of the 110 halos of the 58 Star Cores book solids, 84 are new (42 centre halos, 42 polar halos), 22 are known solids (mostly
other DICTO Solids: the halo map links them, e.g. OG -> TPH, TPH -> TQH -> TQP -> TQHD) and 4 repeat another census halo. 114 of the
116 stars are new; the stars of the FPD and the Palintriacontahedron coincide, because DICTO Solids v7 holds these two as two entries of
ONE shape up to similarity (flag for DICTO). No star equals a stellation in the registry, and no base solid is classical. The
operations themselves are classical (Kleetope / kis, polar reciprocation); the new objects are the halos and stars of DICTO's new
solids. Status: study note (stars-and-halos-census.pdf in DICTO's reading folder); not in a paper.

Run on compute-host (~/work/halo-census, python3), DICTO Solids v7. census.py ran as background processes, 8 at a
time via xargs, one per shape, then collect.py as one process; all finished and nothing is left running.
- data/slugs.txt: the 58 card solids (star-cores.json of 2026-10-30-star-cores + star-cores-new4.json of 2026-11-01-star-cores-book).
  The notch cards Maedate and Kuwagata are pieces, not solids with a star treatment: not included.
- scripts/census.py <dataset> <slug> <out>: centre halo (hull of t x the feet of the perpendiculars from O; shape independent of t),
  polar halo (convex solids with O inside every face plane: the polar reciprocal; independent of rho), stars t = 2 and phi (solid
  + face pyramids as a surface, coplanar neighbours merged). Exact in Q(sqrt5) / Q (210 of 226 objects: every hull facet checked
  exactly; star faces merged only when exactly coplanar); the 4 solids in Q(t), Q(2^(1/3)), Q(sqrt3) float64 (16 objects).
  Per-shape output data/shapes/<slug>.json stays on compute-host (47 MB, not in git).
- scripts/collect.py <dataset> <data>: matches (same corner count and, for halos, faces by sides; same sorted scaled squared distances
  1e-6; explicit orthogonal map of the corner sets 1e-6; mirror images count as the same) against DICTO Solids v7, the classical
  families (data/classical-krp.json, exported from krp-core's POLYHEDRA registry: 5 Platonic, 13 Archimedean, 13 Catalan, 92 Johnson,
  72 stellations; plus uniform prisms / antiprisms n = 3..40 and their duals generated in the script) and each other. Output
  data/census.json, data/collect.log, data/thumbs/*.png (the 84 new halos, solid faces, dark edges).
- scripts/typeset_census.py: the PDF page (two tables + thumbnails), printed with papers/print.mjs.
- Placeholder names (rule: at once): "<solid> Halo", "<solid> Polar Halo", "<solid> Star" (t = 2), "Golden <solid> Star" (t = phi).
- Prior art, sources checked 2026-11-02:
  - Library (ask-library, top 5 each): five queries, on the pedal hull, polar reciprocal, Kleetope, Conway kis, and the hull of pyramid
    apexes. They returned Hynd 2023, Cesaroni-Novaga 2026, Richter-Gebert 2026, Montejano et al. 2019, Wikipedia Goldberg polyhedron,
    Koca et al. 2010, Wikipedia Rhombic dodecahedron, McMullen-Schulte 2005, Matteo 2014, Leppmeier 2019, O'Rourke 2010, Devadoss et
    al. 2026, Antiprism "conway", Kabai 2010, Gosain-Grimmer 2025, Johnson 1966, He-Guest 2025, Hepworth 2022, Erdahl 1999 and
    Magazinov 2015, and the pages Pacioli 1509 p. 107, Firsching 2015 p. 10, Dutour Sikiric et al. 2008 p. 31 and Betke-Henk 2000
    p. 35.
  - Web (3 searches): Wikipedia Kleetope (citing Grunbaum, Convex Polytopes 1967, pp. 217, 227), arXiv:1509.08218, 2004.08429; arXiv:
    2108.08293, 1003.2153 ("face pedal polyhedron" as an open problem), Grace 1927, Robinson 1939 (pedal tetrahedra); G. W. Hart,
    Conway Notation for Polyhedra, Wikipedia Conway notation, Antiprism conway.
  - None names any of the new halos or stars.
- Limits: classical coordinates are float64 closed forms (the matches are to 1e-6 with an explicit corner map); symmetry is that of the
  corner set (1e-7); stars are compared by their corner sets; the stellation registry holds the first four stellations of the Platonic
  and Catalan solids (and a few others), not all 59 icosahedron stellations.
