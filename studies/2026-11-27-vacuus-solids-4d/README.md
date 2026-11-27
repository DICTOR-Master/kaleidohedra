# Vacuus-Solids as shadows of 4D polytopes (27 November 2026)

DICTO · study. The observation is **DICTO's** (27 Nov): "Vacuus solids having a copy of the solid in the centre makes them seem like
polytopes in appearance"; then "so those that nest the solid are 4D shapes, but those that have their dual aren't?!"; "Yes run the test".
With Claude (Anthropic).

**Question.** Is a Vacuus-Solid (solid P, core at the centre, every face dug in as a pit whose apex is a core corner) the Schlegel
diagram of a 4D polytope, (a) with a scaled copy of P as core, (b) with the scaled dual P* as core (the Vacuus-Solids of 26 Nov)?

**Construction.** Q = conv(P x {0} u K x {1}), K = mu P (copy) or mu P* (dual); seen from (O, -h), beyond the facet P x {0} only.

**Result (scripts/cayley4d.py, logs/cayley4d.log, FINAL ok; exact in Q(sqrt 5) with sympy).** For all five Platonic solids, both cores:
- (a) copy core: Q is the prism P x I; facets P, the core, one frustum per face (2 + F). Cube: the tesseract.
- (b) dual core: Q has exactly 2 + V + E + F facets: P, the core, and one join per face of P with its dual face of the core:
  face * dual corner = **the pit over that face**; edge * dual edge = a tetrahedron (the wedge of material along the edge);
  corner * dual face = a pyramid from the corner onto a core face. Cube 28, octahedron 28, tetrahedron 16, dodecahedron 64, icosahedron 64.
- Every predicted facet is exact (its points span one hyperplane, all other points strictly on one side); the float hull has exactly the
  predicted number of facets; the view from (O, -1) lies beyond P x {0} only (exact sign check against every other facet).
- Core sizes mu = 1/20, 1/2, 9/10 tested for cube and dodecahedron: all hold (the facet structure does not depend on mu).
- Negative control: the cube's octahedral core turned by a generic rotation (cos 3/5) is NOT such a shadow (the joins stop being flat).
So DICTO's observation holds for both: the copy core gives the 4D prism, the dual core gives the 4D polytope conv(P u P*) stacked in
4D; the pits are cells of it in both readings, and t -> 0 gives the 4D pyramid over P (the Vacuus itself). In the dual case the 4D reading
also cuts the material between the pits into the core, one wedge per edge and one pyramid per corner.

**Credit.** Schlegel diagrams: V. Schlegel (1886). Stacking two polytopes in parallel levels and taking the hull is the Cayley trick
(Huber, Rambau, Santos 2000). Whether conv(P x {0} u P* x {1}) has a name in the literature: prior-art search still open.

**Leads.** (1) Prove the dual-core statement for every convex P with O inside (conditions: each face, edge and corner of P meets the
relative interior of the matching normal cone; true for the five here); (2) test the Archimedean, Catalan and McCooey self-dual sets;
(3) prior-art search on the name; (4) DICTO: observation only for now, nothing into a paper without his word.

**Exact completeness (27 Nov; DICTO: "make the completeness check exact").** cayley4d.py, exact_complete(): every listed facet is a
true facet (checked exactly); the 2-faces of each listed facet F are found as the 2-dimensional intersections of F with the other listed
facets (two facets of a polytope meet in a face), and they must close F's boundary exactly: every edge of each 2-face shared with exactly
one other found 2-face, and Euler V - E + F = 2. Then every 2-face of a listed facet lies in another listed facet; the facets of a
polytope are connected across 2-faces, so the list is complete. All 14 cases pass (rank computations exact in Q(sqrt5), Q(sqrt2)).
Control: the cube's dual-core list with one edge wedge left out FAILS (a 2-face of a neighbouring facet is not closed). FINAL ok.
