# A · Vacuus–Resonus Lean entry (Palomar)
## Goal
DICTO 26 Nov, "yes to all": formalize #120 Theorems 1, 2, 4 (any dimension) and 3 (i)-(ii); lattice webs (Theorem 0) as a bonus
(into #120's next version); blueprint paper #123 released with the entry; repo vacuus-resonus-lean.
## Pass
Entry preflight FINAL ok; blueprint #123 read ok; DICTO submits; registered.
## State
- 26 Nov: preflight 1 failed on intake only (request_id must be 12 chars); fixed to vacresonlean, commit 8f12f7e4, rerun 45761289408 in progress. #120 v2 draft in reading folder (WAITING 6).
- 26 Nov: public repo DICTOR-Master/vacuus-resonus-lean (main, f31a43fc) created (DICTO yes); preflight run 45760814867 started.
- 26 Nov: ENTRY ASSEMBLED vacuus-resonus-lean (local git bd004e5+README): 6 theorems (T4a, T2, T4b, T1 <=, T3 (i), web_iff), Challenge/Solution, comparator.json, formalization.yaml (plain tone; source #120 formalizes, Ziegler background). Full lake build on the compute host OK. Local comparator script clashes with hard-linked packages: use the GitHub preflight.
- Release plan changed: no separate blueprint #123; #120 v2 (adds lattice webs + Lean names) is released with the entry (fewer papers, less self-promotion).
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
studies/2026-11-25-lean-vacuus-resonus (VacuusResonus/*.lean, check.sh, logs); build on the compute host;
master copy dicto-geometry-lean/lib/VacuusResonus; paper papers/2026-11-24-vacuus-resonus.
- 26 Nov: SUBMITTED to Palomar by DICTO (repo vacuus-resonus-lean, commit 8f12f7e4, preflight passed). Next: review result, then registration; #120 v2 release still waits on his read ok.
- 26 Nov: PALOMAR REVIEW: registration NOT offered (selected statements elementary: Resonus/pencil/polar-edge = inner-product identities without polytope/polarity; heart routine; permutohedron equations not proved to be facets; lattice web without lattice tiling). Recommended to DICTO: withdraw; no cosmetic resubmission; stronger entry only as real milestones (Rado: permutohedron facets from conv of permutations; Resonus/Vacuus for a polytope and its polar via Mathlib polar; lattice web under a lattice tiling). #120 v2 drops any mention of a Palomar entry. Awaiting his numbers.
- 26 Nov: DICTO WITHDREW the Palomar submission (vacuus-resonus-lean). Repo stays public as a record. Stronger entry = lead only (Rado facets, polar via Mathlib, lattice tiling). #120 v2: no Palomar mention.
- 26 Nov: Fable review done (studies/2026-11-25-lean-vacuus-resonus/FABLE-REVIEW-2026-11-26.md): permutohedron line M1-M5 (Rado H=V, faces, plates, count A402191) is the only route likely to clear the bar; best value M1+M2. Awaiting DICTO.
- 26 Nov: prior-formalisation search: Rado ALREADY in TauCeti (PermutationOrbit.lean, mem_convexHull_range_comp_perm_iff, Apache-2.0). M1-M2 not new; new value = M3-M5 on top (faces/ridges, plates, A402191 count). Awaiting DICTO.
