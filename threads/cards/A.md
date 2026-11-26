# A · Vacuus–Resonus Lean entry (Palomar)
## Goal
DICTO 26 Nov, "yes to all": formalize #120 Theorems 1, 2, 4 (any dimension) and 3 (i)-(ii); lattice webs (Theorem 0) as a bonus
(into #120's next version); blueprint paper #123 released with the entry; repo vacuus-resonus-lean.
## Pass
Entry preflight FINAL ok; blueprint #123 read ok; DICTO submits; registered.
## State
- Done: Theorem 4 (a) (M1), Theorem 2 pencil lemma + Theorem 4 (b) any dimension (M5, 26 Nov, FINAL ok).
- Lattice webs (M4) done; fins (M2) and factor 3 (M3) belong to other papers.
- Theorem 1 (<=) done (M6a, IsRidge = nonempty exposed face of dim finrank-2; heart_of_symm). Left: (=>), needs every corner of a polytope on a ridge.
## Next
- DONE 26 Nov: Theorem 3 (i) (M7, span_permFlat, FINAL ok). (1) Theorem 3 (ii): layer 1 DONE (M8a: plateOf u <= plateOf v iff v = l u + m). Layer 2 next: weight w = c(a+b) on B1, a(b+c) on B3, 0 on B2 (all >= 0, min 0 exactly on B2); affine map with l>0 keeps levels -> B2 equal, then a!=c: same or reverse ridge, a=c: pair case; l<0 -> only the a=c pair swap {B1+B3, B2}; 3-level vs 2-level counts by cards. Was: permutohedron facet planes in centred coordinates, sum over S of y <= m(n-m)/2 (m = |S|);
  ridge (B1,B2,B3) = facets S1 = B1 (h1 = a(b+c)/2), S2 = B1+B2 (h2 = (a+b)c/2); pencil lemma in V0 = {sum y = 0} gives
  c(a+b) sum_B1 y + a(b+c) sum_B3 y = 0 (checked by hand 26 Nov). Then (ii) the equality criterion.
- (2) Theorem 1 (=>) groundwork in the master library: every extreme point of a full-dimensional polytope (d >= 2) lies on a ridge
  (faces through a vertex; graded face lattice). Multi-step; reusable for later 3D/4D entries. Then heart => X = -X via Krein-Milman
  (convex hull of extreme points).
- If (2) runs long: entry v1 states Theorem 1 (<=) only, exactly; v2 adds (=>).
- Theorem 1 (=>): prove every extreme point of a full-dimensional polytope (hull of a finite set, dim >= 2) lies on a ridge (face lattice: facets through a vertex, two adjacent facets meet in a ridge); then symmetric ridges => symmetric corners => X = -X.
## Files
studies/2026-11-25-lean-vacuus-resonus (VacuusResonus/*.lean, check.sh, logs); build on dicto-big-brother ~/lean/vacuus-resonus;
master copy ~/dicto-geometry-lean/lib/VacuusResonus; paper papers/2026-11-24-vacuus-resonus.
