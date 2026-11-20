# Prior art for E1 and E2 (searched 20 November 2026)

A quick search, as asked. It reuses the full Dehn prior-art record of 19 November (studies/2026-11-19-dehn-prior-art), which already covered Lean (Mathlib, FormalBook ch. 10, atlas-lean, proof_in_the_book, lean-genius), Isabelle AFP, Coq/Rocq, HOL Light, Metamath, Mizar and Naproche for Dehn invariants and Hilbert's third problem. Below is what was searched again today and what was seen.

## Formalizations

| Searched | Where | What was seen |
|---|---|---|
| Sydler's theorem, formal proof | web search "formalization Sydler theorem scissors congruence Lean OR Isabelle OR Coq OR HOL Light"; GitHub code search "Sydler" | No formal proof. Expository papers only (Schwartz's notes on Jessen's proof, Brown; Welsh, UChicago REU 2016; Zakharevich, arXiv:2210.08082). GitHub hits are a Python script and research summaries in a "math-superagent" repository (markdown, no proofs). |
| Scissors congruence / equidecomposability in Lean | GitHub code search "scissors congruent language:Lean", "Dehn invariant language:Lean"; web search on Mathlib | Only the ATLAS edge-list Dehn invariant (facebookresearch/atlas-lean and its copy in math-proof/lemma), already in the 19 Nov record; nothing on explicit dissections of solids. FormalBook ch. 10 (19 Nov record) has `GeomEquidecomposable` on sets and non-equidecomposability; no explicit dissection into a cube was found there. |
| Wallace–Bolyai–Gerwien, formal proof | GitHub code search "Bolyai Gerwien" (Lean, Isabelle); web search | Not found in any system. (Needed for the box-to-cube step of E1, so E1 would build it.) |
| Equidecomposability in Isabelle | GitHub code search "equidecomposable language:Isabelle" | Only AFP Banach_Tarski (paradoxical decompositions), not polyhedral dissections. |
| Dehn invariant in Coq | GitHub code search "Dehn invariant language:Coq" | Nothing. |
| 4D Dehn invariant (any system) | web searches above; 19 Nov record | Nothing. No formalization of Jessen's 4D theorem, of Hadwiger invariants, or of any Dehn invariant beyond dimension 3. |

## Mathematics

| Source | What was seen |
|---|---|
| Lagarias, Moews, "Polytopes that fill ℝⁿ and scissors congruence", DCG 13 (1995) 573–583, doi:10.1007/BF02574064 (search snippets of the Springer PDF) | In dimension ≤ 4 a polytope that tiles by congruent copies is scissors congruent to a cube (Corollary 2a for dimension 4); Jessen: in dimension 4 volume and the Dehn invariant are sufficient. |
| Encyclopedia of Mathematics, "Dehn invariant" and "Sydler theorem"; Wikipedia "Hilbert's third problem" | Classical statements: Dehn 1901, Sydler 1965, Jessen; Dehn–Hadwiger invariants in higher dimensions. |
| Zakharevich (par.nsf.gov, survey) | Dehn–Sydler–Jessen complete in dimensions 3 and 4. |
| Search "Dehn invariant" with 24-cell / 120-cell / 600-cell / 5-cell | No source discussing the Dehn invariants of the regular 4-polytopes. Not found either: the relation θ₆₀₀ ≡ −θ₅ (mod ℚπ). Both follow at once from the classical dihedral angles, so they are not claimed as discoveries. |
| Wikipedia pages (wikitext read): "5-cell" (dichoral angle arccos 1/4 ≈ 75.52°), "Tesseract" (90°), "16-cell" (120°, Coxeter Table I(ii)), "120-cell" (144°), "600-cell" (π/3 + arccos(−1/4) ≈ 164.4775°), "Regular 4-polytope" (only mirror dihedrals, no polytope dihedrals) | The six dihedral angles. 24-cell: the characteristic table did not show the value in the lines read; its 2π/3 rests on our coordinate check and Coxeter Table I(ii) as cited. |
| Frederickson, web updates to *Dissections: Plane & Fancy* ch. 20 (Purdue page, seen via search) | Truncated octahedron to a cube: Hanegraaf; Theobald 12 pieces; Theobald 11 pieces (Oct 2007). |
| Wolfram Demonstrations (titles and abstracts via search) | Rhombic dodecahedron into two cubes (cube + six pyramids; Hafner, hinged version after Frederickson 2002); two truncated octahedra into a cube (six pieces, Paterson 1988, Hanegraaf); truncated octahedron to a rectangular solid; cube into a golden acute rhombohedron and three rectangular solids; rhombic dodecahedra of the second kind into cubes. |

## Our checks

- `checks/dihedral4d.py` (log `checks/dihedral4d.log`): the six dihedral angles from coordinates (π minus the nearest-neighbour angle of the dual's vertices; the 120-cell's vertices built as the 600 tetrahedron centres of the 600-cell). All six match. FINAL ok.
- `checks/rational_pi.py` (log): 2 cos θ is 1/2 (5-cell) and a root of the primitive non-monic 4x² + 2x − 11 (600-cell), so neither angle is in ℚπ. FINAL ok.
- `checks/relation_600_5.py` (log): θ₆₀₀ = 4π/3 − θ₅ exactly (cos(π/3 + arccos(−1/4)) = −(1+3√5)/8). FINAL ok.

## Conclusion

No formal explicit polyhedral dissection into a cube, no formal Sydler or Wallace–Bolyai–Gerwien theorem, and no formal Dehn invariant in dimension 4 were found. The mathematics of both candidates is classical. E1's individual dissections are in the recreational literature for at least the rhombic dodecahedron and the truncated octahedron.
