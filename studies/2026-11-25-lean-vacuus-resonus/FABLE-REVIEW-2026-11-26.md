# Independent review of the withdrawn Vacuus Lean entry (Fable, 26 Nov 2026), judged
Scope: attack the 6 entry theorems, restructure, milestones, verdict. Mathlib names checked against the pinned revision's sources
(not compiled). My judgement of each point follows the point.

## Attack (agreed with the Palomar reviewer on all six)
- resonusPlane_eq_orthogonal, span_ridgeFlat, vacuusPlate_polar: linear algebra; P, facets, polar never enter (the polar defined in
  PolarLink is unused in Challenge). AGREED.
- heart_of_symm: holds for any set. AGREED. Extra: IsHeart is vacuous without ridges, and Mathlib's IsExposed allows l = 0, so the
  converse needs "polytope, full-dimensional, dim >= 2". AGREED (Lean definitions; the paper's statement is for polytopes).
- span_permFlat: facet equations assumed in the definition; Equiv.Perm / convexHull never appear. AGREED. Sign remark: our permFlat
  follows the facet heights a(b+c)/2 of the study's convention; harmless.
- web_iff: Lambda any AddSubgroup, no tiling. AGREED.
- Theorem 3 (ii)-(v) and the plate count (A402191) not formalized: these are the paper's real content. AGREED.

## Restructure (accepted as the plan; lead only, no promise)
M1 permutohedron = convexHull of permutations; easy half of Rado; extreme points = the n! permutations (rearrangement inequality).
M2 Rado 1952 H = V (separation + sorting). M1+M2 = credible entry (a named classical theorem on Mathlib's convexHull/Equiv.Perm).
M3 facets and ridges as exposed faces with dimensions. M4 Theorem 3 (i) and the 2^(n-1)-1 Resonus planes on the real polytope.
M5 plate coincidence classification and count (Theorem 3 (ii)-(iii), A402191): the new theorem; M1-M5 = strongest entry.
M6 one-sided polar bipolar + heart iff for polytopes (optional). M7 face duality (library investment only).
Verdict: Theorems 2/4, heart <=, web_iff will not clear the bar in any wording (framing, not theorems). Best value: M1+M2.
Before starting: search for an existing permutohedron/Rado formalization outside Mathlib (related_formalizations).

## Prior-formalisation search (26 Nov 2026, before starting M1-M2)
Sources checked: Mathlib (GitHub code search: no "permutohedron", "permutahedron", vector majorization; "Rado" hits unrelated);
all public Lean code on GitHub for permutohedron / permutahedron / majorization; web searches (Lean, Isabelle, Coq, Mathlib + Rado,
majorization, permutahedron facets); Coq-Polyhedra (general faces, not permutohedra).
**Found: Rado's theorem is already formalized** in TauCeti (TauCetiProject/TauCeti, Apache-2.0, downstream of Mathlib),
TauCeti/Analysis/Convex/PermutationOrbit.lean: `mem_convexHull_range_comp_perm_iff` (x in the convex hull of the rearrangements of an
antitone w iff majorized by w), with the rearrangement-inequality direction and Robin Hood transfer closure (TauCeti/Analysis/Convex/
Majorization.lean). Also Schur-Horn there. So M1-M2 are NOT new; credit TauCeti (related_formalizations) and build M3-M5 on it.
Other hits (majorization only, not Rado): physlib QuantumInfo/ForMathlib/Majorization.lean, QuAIR/Lean-QIT, LeanPool DavisKahan.
