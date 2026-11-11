# The OG's margin (#43 Conjecture 1): study 2026-11-09

**Conclusion: #43 Conjecture 1, t_min(D_k) ≤ 3/φ² for every k, is now proved exactly for k = 0 to 11 (three more levels than
Table 7) and reduced, for every larger k, to one stated lemma about the inradius of the downward family; float runs to k = 28 back the
lemma with a 13 % margin.**
**Status: REDUCED** (exact for k ≤ 11; the tail rests on the Inradius Lemma below, unproved; no counterexample, and none expected).

DICTO chose this gap on 9 November 2026.

## 1. Setting

#43 (DICTO Kyushindo Cores, Version 2) notation: for a convex polytope S with O inside, faces n_i·x ≤ h_i (unit normals), R(S) the
largest corner distance, r(S) the smallest face distance, H(S) the largest face distance, P(S) = hull of the foot points h_i n_i,
t_min(S) the least t with S ⊂ t·P(S). The OG's downward family: D_0 = OG, D_k = P(D_{k−1}).
Conjecture 1: t_min(D_k) ≤ 3/φ² = (9 − 3√5)/2 ≈ 1.145898 for every k (equality at k = 3).

Ledger: none of the 51 Concordance ledger entries touches Conjecture 1 (the one #43 entry is the 2026-11-08 proof of Conjecture 2), so
nothing here is a retry.

## 2. What is proved for every convex polytope (general)

Let θ(S) be the covering radius of S's unit face normals on the sphere (the largest angle from any direction to the nearest normal;
it equals arccos of the smallest face distance of the hull of the normals).

**Lemma A (the step in support functions).** For every direction u, h_{P(S)}(u) = max_i h_i (n_i·u), and
t_min(S) = max_u h_S(u)/h_{P(S)}(u).
Proof: P(S) is the hull of the points h_i n_i, so its support is the largest of their projections; S ⊂ t·P(S) exactly when
h_S ≤ t·h_{P(S)} in every direction. ∎

In logarithms, log h_{P(S)}(u) = max_i [log h_i + log cos∠(n_i, u)]: one step of the downward family is a max-plus convolution of the
log-support with the kernel log cos, taken over the current normals only.

**Lemma B (two step inequalities).**
(F1) R(P(S)) = H(S) ≤ R(S).
(F2) r(P(S)) ≥ r(S)·cos θ(S).
(F3) t_min(S) ≤ R(S)/r(P(S)) ≤ (R(S)/r(S))/cos θ(S).
Proof. (F1) The farthest point of a hull of finitely many points is one of them; the foot point h_i n_i has length h_i ≤ R(S).
(F2) For a direction u take the normal n_i nearest to u (angle ≤ θ); by Lemma A, h_{P(S)}(u) ≥ h_i cos θ ≥ r(S) cos θ; the inradius
of P(S) is its smallest support. (F3) First inequality is #43 Theorem 1; the second is (F2). ∎

**Proposition C (tail criterion).** For K ≤ k: t_min(D_k) ≤ R(D_K)/r(D_{k+1}), and r(D_{k+1}) ≥ r(D_K)·∏_{j=K}^{k} cos θ(D_j).
Proof: (F3) and R(D_k) ≤ R(D_K) by (F1) repeated; (F2) repeated. ∎

**Remark (polar form).** By #43 Lemma 3, polar(D_k) = X_k := T^k(polar OG) (the UP steps from the Hecatodihedron), and
S ⊂ t·S′ ⟺ polar(S′) ⊂ t·polar(S). So Conjecture 1 is the same statement as X_{k+1} ⊂ (3/φ²)·X_k for every k.

## 3. The reduction

**Inradius Lemma (unproved).** r(D_j) ≥ (φ²/3)·R(D_11) ≈ 1.084154 for every j ≥ 12.

**Theorem R.** Conjecture 1 holds for k ≤ 11 (exact, §4); and the Inradius Lemma implies it for every k ≥ 11.
Proof of the second part: for k ≥ 11, t_min(D_k) ≤ R(D_k)/r(D_{k+1}) ≤ R(D_11)/r(D_{k+1}) ≤ 3/φ² by Proposition C. ∎

So, given the exact cases, Conjecture 1 follows from a statement about inradii only. By Proposition C the lemma in turn follows from
the mesh statement ∏_{j≥11} cos θ(D_j) ≥ (φ²/3)·R(D_11)/r(D_11) = 1.084154/1.165269 ≈ 0.9304: the normals of D_j must keep filling
the sphere finely enough. This crude route is too lossy from K = 11: the float product over j = 11..27 is already 0.9090 < 0.9304,
because it ignores that r recovers (r falls at j = 9 and then climbs back). From K = 20 it has room: the need is
(φ²/3)·R(D_20)/r(D_20) = 0.8836 and the product over j = 20..28 is 0.9879; what is missing is a bound on θ(D_j) for every later j.

What the float runs show (§5): R(D_j) falls monotonically (as it must, F1) from 1.687 to 1.18974 at k = 28; r(D_j) stays between
1.1767 and 1.1889 for 14 ≤ j ≤ 28; the smallest r seen for j ≥ 12 is 1.176699, 8.5 % above what the lemma needs, and 13.4 % above the
need for K = 27.

## 4. Exact results (Q(√5))

exact_family.py builds D_0 … D_12 exactly: the float hull only proposes faces; each face is proved by an exact supporting plane (every
listed point on the inner side, members exactly on it), carried round its orbit by the 60 exact rotations, and the proved faces are
shown to close up (every polygon edge in exactly two faces; a closed sub-collection of the faces of a convex polytope is all of them).
t_min(D_k) is the exact maximum of m·v/d over all listed points v of D_k and face representatives (m, d) of D_{k+1}, confirmed by exact
sign tests against every pair.

| k | listed points | faces | t_min(D_k) | 3/φ² − t_min | digits |
|---|---|---|---|---|---|
| 0 | 102 | 80 | (445 − 16√5)/361 = 1.133581 | +0.012317 | 6 |
| 1 | 80 | 132 | 1.117382 | +0.028516 | 8 |
| 2 | 132 | 140 | 1.103147 | +0.042751 | 11 |
| 3 | 140 | 162 | (9 − 3√5)/2 = 3/φ² | 0 (equality) | 2 |
| 4 | 162 | 200 | (21 − √5)/18 = 1.042441 | +0.103457 | 3 |
| 5 | 200 | 252 | 1.086902 | +0.058996 | 44 |
| 6 | 252 | 320 | 1.025657 | +0.120241 | 49 |
| 7 | 320 | 402 | 1.059516 | +0.086383 | 108 |
| 8 | 402 | 500 | 1.138077 | +0.007821 | 375 |
| **9** | 500 | 732 | **1.076770** | +0.069128 | 792 |
| **10** | 732 | 662 | **1.008772** | +0.137126 | 3096 |
| **11** | 662 | 672 | **1.018734** | +0.127164 | 7572 |

(k = 9, 10, 11 are new; Table 7 stopped at 8. "digits": the longest numerator or denominator in the exact value. The heights of the
coordinates triple per level, 17 829 digits at D_12, which is what stops the exact run.)

## 5. Float run to k = 28 (evidence for the lemma)

float_family.py: double precision, symmetry re-imposed every step (orbit closure under the 60 rotations), coplanar hull triangles merged
by adjacency within 1e-9. It reproduces every exact count (corners and faces, k ≤ 11) and t_min of Table 7 to 1e-9.

| k | corners | faces | t_min | R/r(next) | θ (deg) | r | R |
|---|---|---|---|---|---|---|---|
| 12 | 540 | 902 | 1.020352 | 1.046076 | 8.603 | 1.179355 | 1.237154 |
| 14 | 900 | 1262 | 1.024833 | 1.025236 | 9.080 | 1.185352 | 1.218931 |
| 16 | 1392 | 2360 | 1.011525 | 1.018867 | 6.611 | 1.176986 | 1.202115 |
| 18 | 2072 | 3780 | 1.008139 | 1.015901 | 5.155 | 1.179561 | 1.196909 |
| 20 | 4200 | 7952 | 1.005365 | 1.012678 | 4.190 | 1.178037 | 1.192726 |
| 22 | 8082 | 15500 | 1.003051 | 1.013594 | 3.398 | 1.176754 | 1.192696 |
| 24 | 18132 | 33980 | 1.002565 | 1.011487 | 3.051 | 1.176946 | 1.190595 |
| 26 | 34860 | 66482 | 1.000652 | 1.010807 | 1.888 | 1.177328 | 1.190013 |
| 28 | 57000 | 110672 | 1.000769 | — | 2.028 | 1.177489 | 1.189741 |

Every row k = 0..27 satisfies (F1), (F2) and (F3) (tail_criteria.py). The largest t_min over k = 0..28 is still t_min(D_3) = 3/φ²;
after k = 9 no value exceeds 1.0276. The per-step criterion (R/r)/cos θ ≤ 3/φ² holds for every k from 10 to 27 (it fails at k = 0, 3
and 9, where Theorem 1 is not enough and the exact values are needed).

**Does D_k converge in shape?** It rounds out: r/R rises from 0.8957 (k = 9) to 0.98970 (k = 28), still rising by about 2·10⁻⁴ per
step, and t_min falls to 1.0007. The limit, if it is the ball, has t_min = 1. The covering radius θ falls from 20° to about 2° and then
stalls (1.89°, 1.96°, 2.03° at k = 26, 27, 28), so a proof by Σθ² alone would need more care than the numbers suggest; the Inradius
Lemma is the cleaner target. Lemma A explains the rounding: each step is a max-plus convolution (sup-convolution) of the log-support
with log cos, which flattens bumps toward the maximum, while the finite set of normals costs a factor cos θ.

## 6. Checks, with numbers

| check | result | script, log |
|---|---|---|
| sanity: Table 7 exact values k = 0..8 reproduced digit for digit from the 2026-10-21 log | identical | sanity_table7.py, data/sanity-table7.log |
| exact t_min(D_k) ≤ 3/φ², k = 0..11, by exact sign; each an exact maximum | all true; equality only at k = 3 | exact_family.py, data/exact-family.log/json |
| float counts and Table 7 values | all match (k ≤ 11 counts, k ≤ 8 values, to 2e−6 or better) | float_family.py, data/float-family.log/json |
| float symmetry error | ≤ 3.2e−15 at every k | float_family.py |
| step inequalities F1–F3 on 28 steps | all hold | tail_criteria.py, data/tail-criteria.log |
| Inradius Lemma margin, K = 11 | need 1.084154, smallest r seen (12 ≤ j ≤ 28) 1.176699 (+8.5 %) | tail_criteria.py |

All runs on the large machine (scripts end with a conditional FINAL line; all printed FINAL ok).

## 7. On #43

Nothing inconsistent: the nine Table 7 values reproduce exactly, the counts 102/80 … 312(402)/500 and the named solids down 9–11
(732, 662, 672 faces: TQD-732, TQHD-662, TQP-672) match the float and exact builds. Two small points for a later version:
(i) §2 says "By Theorem 1 below, S_{k−1} ⊂ S_k … holds exactly when t_min(D_{k−1}) ≤ φ"; this equivalence is the definition of t_min
plus Corollary 1's S_k = φ^k D_k, not Theorem 1. (ii) At k = 0, 3 and 8 Theorem 1's upper bound R/r(P) is attained (t_min = R/r(P)
exactly), i.e. the farthest corner points straight at the nearest face of the next solid; Table 7 could say so, since this is why the
k = 3 equality has the clean value 3/φ².

## 8. LEADS

1. Prove the Inradius Lemma. Two routes: (a) a mesh bound from a later start (∏_{j≥20} cos θ_j ≥ 0.8836 suffices, with the exact table
   or a certified computation carried to k = 20; from j = 11 the mesh route fails, §3);
   (b) a direct lower bound on the max-plus convolution of Lemma A when the normal set is a union of orbits of a fixed list of axis
   types (Table 6's axis rhythm).
2. Push the exact table to k = 12 (one more level, about 50 000 digits, longer than 20 min): useful only to shrink the lemma's K.
3. Shape limit: decide whether D_k/R(D_k) tends to the ball (r/R → 1) or to a slightly non-round limit (r/R near 0.990); a float run to
   k ≈ 35 needs chunked hulls.
4. The polar form (Remark): X_{k+1} ⊂ (3/φ²)X_k for the UP steps from the Hecatodihedron; the same reduction applies to any start, so the
   question "which icosahedral starts keep t_min ≤ 3/φ² for ever" is the natural general version.
5. Destination: the Version-3 line of #43 (Table 7 extended to k = 11; Conjecture 1 stated as reduced to the Inradius Lemma). Where to
   place: DICTO's choice.

## 9. Concordance ledger line (ready)

```json
{"question": "", "method": "exact Q(sqrt5) builds of the OG downward family D_0..D_12 (float-guessed faces proved exactly, orbit-closed, closure check); max-plus form of the step h_P(u) = max h_i n_i.u; step inequalities R(P S) = H(S) <= R(S), r(P S) >= r(S) cos theta(S); float family to k = 28", "status": "REDUCED", "result": "t_min(D_k) <= 3/phi^2 proved exactly for k = 0..11 (new: 1.076770, 1.008772, 1.018734 for k = 9, 10, 11); for k >= 11 it follows from the Inradius Lemma r(D_j) >= (phi^2/3) R(D_11) = 1.084154 for all j >= 12 (float: smallest r 1.176699 up to j = 28, margin 8.5%); D_k rounds out (r/R 0.9897 at k = 28, t_min 1.0008)", "retry": "prove the Inradius Lemma (mesh bound on theta(D_j) or axis-type bound on the max-plus step); exact k = 12 only to shrink K", "study": "studies/2026-11-09-og-margin", "date": "2026-11-09", "target": "#43 Conjecture 1 (the OG's margin)"}
```

DICTO · dictospheres.com

## 6. Exact run to D_14 (og-exact-13, the compute machine, finished 9 Nov 15:38, FINAL ok, 14 183 s)

Log: data/exact-family-13.log. D_0 … D_14 built exactly in Q(√5) (D_13: 1092 faces, D_14: 1262 faces; max 90 928 digits).
New exact cases: t_min(D_12) = 1.020352, t_min(D_13) = 1.027602, both ≤ 3/φ² exactly (match the float run).
So Conjecture 1 is now exact for k ≤ 13, and Theorem R moves to K = 13:
the Inradius Lemma needed is r(D_j) ≥ (φ²/3)·R(D_13) ≈ 1.078315 for j ≥ 14 (was 1.084154); float margin 9.1 % (smallest r 1.176699).
From K = 13 the crude mesh route has room on the float data: need ∏ cos θ ≥ 0.91177, product over j = 13..27 is 0.93176
(from K = 11 it failed: 0.9090 < 0.9304). What remains is a bound on θ(D_j) for all later j.

## 7. Coincidence pilot (DICTO "yes", 9 Nov): can intervals replace exact arithmetic beyond D_13?

scripts/coincidence_pilot.py, data/coincidence-pilot-12.log (watched job, FINAL ok). Intervals prove strict inequalities, never equalities,
so every exact coincidence of D_0..D_12 was classified. With rotations only, 1484 coplanar faces looked unforced; with the mirrors of
I_h added (two mirror pairs of corners are always coplanar), **every coplanar face of D_5 … D_12 is forced by symmetry** (unforced:
20, 30, 20 hexagon-type faces at D_2–D_4 only, inside the exact range). No listed point lies on a face without being a corner: the
non-corner points are all strictly inside (60–252 per level). Smallest float gap face-plane to non-member: 7.7e-8 (D_9), else ≥ 2e-5.
Consequence: an interval (ball) run is rigorous if points are stored as orbit representatives and generated by the exact symmetry
(forced coplanarity then holds by construction) and every remaining gap is certified non-zero; it checks the pattern level by level.

## 8. CERTIFIED run (ball arithmetic), k = 10 … 22: FINAL ok (9 Nov, watched job og-certified-22, 38 s)

scripts/certified_family.py (method in its header), data/certified-family-22.json, .log. Exact Q(√5) to D_10, then Arb balls
(600 bits) with the exact I_h action on labels; every face certified (non-members strictly inside, every coplanarity forced by
symmetry, closure); certified upper bounds. Validation: the certified t_min(D_10 … D_13) agree with the exact values to 12 digits.
**Result: t_min(D_k) < 3/φ² certified for every k ≤ 22** (k = 14 … 22: 1.024833, 1.021610, 1.011525, 1.011068, 1.008139,
1.006896, 1.005365, 1.003401, 1.003051). Ball radii stay ≤ 1e−141.
Theorem R now runs from K = 22: the Inradius Lemma needed is r(D_j) ≥ (φ²/3)·R(D_22) ≈ 1.040839 for j ≥ 23 (float min r 1.176699:
margin 13.1 %). Extension to k = 30 running (og-certified-30).

## 9. New-Face Lemma: the dips do not add up (DICTO "proceed", 9 Nov; scripts/newface_float.py, data/newface-30.*, float k ≤ 30)

Exact chain (Lemma G + one plane bound): a surviving face never moves in; a new face spanned by foot points of radius ≥ r(D_k)
within angular radius γ lies at distance ≥ r(D_k) cos γ. Hence **r(D_{k+1}) ≥ r(D_k)·cos γ_{k+1}**, γ_{k+1} = largest angular radius
of a new face of D_{k+1}, and r(D_j) ≥ r(D_K) ∏_{K<k≤j} cos γ_k (checked: bound slack ≥ 0 at every k).
Monotone routes fail: one-step and m-step ratios ν_new(D_{j+m})/r(D_j) dip below 1 for m = 1…4 (worst 0.990 at j = 15).
But γ_k shrinks steadily: 9.30° (k = 16) … 7.28 (22), 6.43, 5.95, 5.41, 5.29, 5.01, 4.59, 4.60, 4.28° (k = 30), about −7 % per level.
∏ cos γ_k over 22 < k ≤ 30 = 0.967. With r(D_30) ≈ 1.177483 the lemma (need 1.040839, from the certified K = 22) holds for all
later j as soon as **∏_{k>30} cos γ_k ≥ 0.884**, i.e. Σ_{k>30} γ_k² ≲ 0.247 rad². Even constant γ = 4.28° would last 44 more levels;
geometric decay at the observed rate uses only 0.041. **Reduction: Conjecture 1 ⇐ certified k ≤ 30 + Decay Lemma (Σ γ_k² < 0.247
for k > 30, the new faces keep getting finer).** Open: a proof of the Decay Lemma (mesh refinement of the pedal iteration).

## 10. Is 3/φ² a Hopscotch turn value? (DICTO "make it so", 9 Nov; scripts/d3_turn.py, data/d3-turn.log, exact Q(√5))

Hopscotch link (exact): polar(D_{k+1}) = D_k^∨ (the antipol), so each step is one hop, and t_min(D_k) is the Hopscotch pairing
max x·y over D_k × D_k^∨ (form B). DICTO proposed the link.
No D_k (k ≤ 5) has all faces on one sphere, so none is a turn solid in the Turn Theorem's global sense. But the equality case is a
**local turn on one axis**: t_min(D_3) is attained with the corner of D_3 and the face of D_4 on the SAME axis (angle 0), and exactly
  t_min(D_3) = (R/H)²(D_3) = (R/r)²(D_4) = 3/φ² = (9 − 3√5)/2,   with   R(D_3)·r(D_4) = H(D_3)².
On that axis the farthest corner of D_3 (R), its farthest face (H) and the nearest face of D_4 (r) are in geometric progression: the
inversion d ↦ H²/d of the hop turns about H there, which is the Turn Theorem's (R/r)² shape of value. (Not a general bound:
(R/H)²(D_4) = 1.0347 < t_min(D_4) = 1.0424.)

## 11. Where is the largest new face? (DICTO: "faces getting smaller ~ whole getting bigger"; data/newface-axes-30.log)
Angles are scale-free, so in the turned-out family S_k = φ^k D_k the Decay Lemma reads: the whole grows by φ per step, its faces
grow more slowly. Average angular radius 2/√F falls ≈ 0.88 per level (0.91° at k = 22 → 0.26° at k = 30); the largest new face only
≈ 0.93 (7.28° → 4.28°). Expected: the laggards sit on the symmetry axes. **Found: they do NOT** (k ≥ 13): the largest new face is
always off-axis, 3°–18° from the nearest axis (mostly nearest a 2-fold axis), and equals the off-axis maximum. Since γ measures a
face's angular RADIUS, the laggards are likely long thin faces (slivers). Route 3 (axis model) dropped; next: shape (aspect ratio)
of the largest faces, and whether slivers split within a bounded number of steps.

## 12. The lagging faces, and a 4-step contraction (DICTO "continue", 9 Nov; scripts/sliver_track.py, data/sliver-30.*)
The largest face (by angular radius γ) is a TRIANGLE at every level k ≥ 15, aspect mostly 1.2–3.8 (6.5 at k = 22, 10.3 at k = 30;
some of the top five reach 20–56): moderately long triangles, γ 3–10× their equal-area radius. Not extreme slivers in general.
Tracking the largest face of level k in its own direction: after m steps the face there has γ ratio m1 0.53–0.97, m2 0.35–0.93,
m3 0.30–0.76, **m4 0.19–0.66** (k = 12…26): every largest face is cut down within 4 steps. New large faces appear elsewhere, so the
global maximum falls more slowly: γ_max(D_{k+4})/γ_max(D_k) = 0.73, 0.78, 0.77, 0.85, 0.81 (k = 22…26).
Sufficient for Conjecture 1 (with certified k ≤ 30, r(D_30) ≈ 1.17748, need ∏_{k>30} cos γ_k ≥ 0.884 ⇔ Σ γ_k² ≲ 0.247 rad²):
a **4-step contraction γ_max(D_{k+4}) ≤ 0.95·γ_max(D_k) for k ≥ 30** gives Σ ≤ 4γ_30²/(1 − 0.95²) = 0.229 rad² (observed ≤ 0.85 → 0.080).
So the open statement is now: **the pedal iteration contracts the largest face by a fixed factor over 4 steps.**

## 13. The 3-fold-axis faces are truncated triangles (DICTO "truncated triangles?", 9 Nov; scripts/hexagons.py, data/hexagons.log)
Face on a 3-fold axis, float, reliable to k ≈ 20 (the plain float iteration drifts later; the symmetrised gnomon/certified data show
axis hexagons again at k = 22, 23, 30): k = 0, 2, 4 REGULAR hexagon; odd k mostly a corner (the hop swaps corner ↔ face); k = 6, 8, 12,
14 an equilateral TRIANGLE; k = 10 a TRUNCATED TRIANGLE, sides alternating, all angles 120°, long/short 4.516518; k = 16 a truncated
triangle, long/short 2.356103; k = 17, 19, 20 triangles. So the 3-fold face moves along the truncated-triangle line between the
triangle (short side 0) and the regular hexagon (ratio 1), the same line as a Kaleidohedra slider. Exact ratios: to do.

## 14. The axis walk, certified to k = 27 (DICTO "yes please", 9 Nov; scripts/axis_walk.py, data/axis-walk-26.log)
Ball arithmetic (as §8, every face certified). Faces on the axes, long/short side ratio to 30 digits:
- 3-fold axis: triangle (k = 6, 8, 12, 14, 17, 19, 20, 24, 26) or TRUNCATED TRIANGLE: k = 10 4.516518, 16 2.356103, 22 1.751818,
  23 1.838215 (period 6 at 10, 16, 22, then 23); odd levels otherwise a corner.
- 5-fold axis: pentagon, or a 10-gon = TRUNCATED PENTAGON: k = 9 29.887, 10 31.056, 13 8.020, 17 1.615005 (near, not equal to, φ),
  19 19.092.
The ratios lie in Q(√5) (all coordinates do) but are not simple: no integer polynomial of degree ≤ 4 with coefficients < 10^15 fits
ratio² (exact coordinates carry hundreds to thousands of digits by k = 10). So the walk along the truncation lines is not a simple
hop rule; the 3-fold truncated triangles do settle (4.52 → 2.36 → 1.75, 1.84).

## 15. Decagons both ways (DICTO: "decagons started appearing, even 13-gons on 400+ faces in earlier cycles", 9 Nov)
Down (this family): the 5-fold axis faces at k = 9, 10, 13, 17 (19) are TRUNCATED PENTAGONS: sides alternate, all angles 144°
(scripts/decagons.py). Up (#43 / og-family-both-ways, Table 1): the DICTO DPHP (Decagon-Pentagon-Hexagon Polyhedron, 270 corners,
152 faces, 420 edges) has 12 decagons with ten EQUAL sides and two alternating angles. These are the two dual kinds of 5-fold decagon
(sides alternate & angles equal ↔ sides equal & angles alternate), as polarity predicts (polar(D_k) = X_k, faces ↔ corners).
13-gons: found only in studies/2026-10-13-fused-shells (Spheres of Dharma, non-convex partial builds, stages 47/49: 4–5 13-gons on
56–71 faces), not in the OG family; DICTO: "probably ones you found" (settled: the fused-shells partial builds).

## 16. CERTIFIED to k = 30: FINAL ok (watched job og-certified-30, 1981 s, D_31 built: 265 050 faces, 2305 orbits)
**t_min(D_k) < 3/φ² certified for every k ≤ 30** (k = 23 … 30: 1.002128, 1.002565, 1.001215, 1.000652, 1.000671, 1.000769, 1.000677,
1.001014); validation k = 10 … 13 MATCH the exact values. Conjecture 1 for all k now needs only the 4-step contraction (§12) from k = 30.

## 17. Ring lemma data (DICTO "proceed", cheapest safe option; scripts/ring_lemma.py, data/ring-lemma-30.log; plain float, face
counts drift slightly from the certified ones after k ≈ 20)
Ratio of angular radii γ across every shared edge: median 1.10–1.20, 99th percentile ≤ 4.1 (k ≥ 20), but the MAXIMUM is unbounded in
the data (up to 93 at k = 21, 37 at k = 28): tiny faces sit next to ordinary ones, so the classical all-faces ring lemma FAILS.
The LARGEST face is never far above its neighbours: at most 5.59 (k = 22), ≤ 2.7 at k ≥ 24. Usable form: a ring lemma for the
largest face only (it is at most a fixed multiple of each neighbour), which is what the 4-step contraction needs.

## §17 Exact reformulation (10 Nov 2026): the growth rule is a Voronoi step
T(S) = {x : v·x ≤ v·v for every corner v of S}. The plane v·x = |v|² is the perpendicular bisector of 0 and 2v
(|x|² = |x − 2v|² ⇔ v·x = |v|²). Hence, exactly: **T(S) = the Voronoi cell of the origin among the points {2v : v a corner of S}**,
and the corners of T(S) are circumcentres of the Delaunay simplices at the origin. The #43 chain D_{k+1} = T(D_k) is therefore iterated
"double the corners, take the origin's Voronoi cell". Conjecture 1 (t_min → 1) becomes: the corner DIRECTIONS spread ever more evenly;
the Decay Lemma (4-step contraction of the largest new face angle γ) becomes: the covering radius (largest empty cap) of the corner
directions shrinks under the map points → their cell's corners. Leads: Delaunay refinement theory (Chew 1989, Ruppert 1995,
Shewchuk 2002: inserting circumcentres bounds circumradius / shortest edge) for the contraction; the prior-art reading of 10 Nov
(Demyanov–Ryabova, Buffon) found both processes different (study 2026-11-10-arxiv-scan).

## §18 The linearised hop (route 2, 10 Nov 2026): no built-in contraction; what the rule must be
In the Voronoi form (§17) the step near the sphere is, to first order in a small patch, the planar map
points → their Voronoi vertices (circumcentres of the Delaunay triangles). That map does NOT contract gaps: on the triangular
lattice it gives the honeycomb (circumcentres) and then the triangular lattice again (period 2), with the same covering radius
a/√3 at every step. So a spectral-gap / linear-operator proof (Buffon-type) cannot give a universal contraction; route 2 is closed.
The decrease of γ in #43 comes from global effects: the face count grows (F: 116 949 → 152 912 → 198 458 at k = 28–30, ≈ 1.3 per
level, so the AVERAGE spacing shrinks ≈ 0.88 per level) and curvature; the LARGEST gap lags (γ_new_max 4.590°, 4.599°, 4.282° at
k = 28–30; ≈ 0.94 per level over k = 22–30; not monotone).
Target (Proposition C + New-Face chain): Conjecture 1 for all k ⇐ Σ_{k>30} γ_k² < 0.247 rad². From γ_30 = 0.0747 rad a geometric
decay q per level suffices when γ_30² q²/(1 − q²) < 0.247, i.e. q ≤ ≈ 0.985 (q = 0.98 gives 0.135; q = 0.99 gives 0.275). Observed
≈ 0.94: a fourfold margin in the rate.
Rule to prove (route 1): (A) growth: F_{k+1} ≥ λ F_k with λ > 1 (Euler counting + the degeneracy pattern); (B) lag: the largest new
face is at most C times its neighbours (ring lemma; measured C ≤ 5.6, ≤ 2.7 from k = 24), so the largest gap follows the average
spacing up to a bounded factor per step. (A) + (B) ⇒ γ_k ≤ γ_30 q^{k−30} with q < 1.

## §19 Step (A), growth of the face count: exact identity and the two lemmas (10 Nov 2026)
With X = polar(D): faces of X_{k+1} = T(X_k) are the ACTIVE corners of X_k; corners of X_{k+1} are the faces of D_{k+1}. Euler
(V = 2f − 4 − e, e = Σ(deg − 3)) gives exactly **F_k = 2(F_{k−1} − c_k) − 4 − e_k**, c_k = candidate corners cut off, e_k = excess
at corners where more than three faces meet. Checked at every level k = 1..25 (float-family-45.log; listed corners = F_{k−1}).
Data: k ≤ 16 irregular (excess up to 0.86 F; growth 0.904 at k = 10); k ≥ 17: growth 1.22–1.63, cut fraction c_k/F_{k−1} 0.15–0.29,
excess e_k/F_k 0.03–0.07 and falling.
(A) for the tail ⇐ (A1) cut lemma c_k ≤ (1/2 − δ) F_{k−1}, and (A2) excess e_k = o(F_k) (degenerate corners only on mirror planes and
axes). Route to (A1): a candidate v is cut only if some corner w has w·v > |w|², which forces |w| < |v| (a smaller cutter beside it);
if cutters are never cut and each cuts a bounded number, c_k < F_{k−1}/2. Next: instrument the family run (who cuts whom) on the
compute machine to test 'cutters survive' and the cut multiplicity.

## §20 Santaló route (10 Nov 2026, DICTO: "start the Santaló volume test")
Idea: P = vol(D_k) vol(D_k°)/(4π/3)² ≤ 1 (Blaschke–Santaló; = 1 only for ellipsoids, here the ball by symmetry). If P rises along
the family, quantitative Santaló stability bounds the distance to the ball, hence t_min. santalo.py pilot (k ≤ 18, float): P = 0.94562
(k = 0), 0.95022, 0.95008 (k = 3, falls), …, 0.95197 (k = 6, falls), …, 0.95559 (k = 9, falls), then rises at every step k = 9..18 to
0.99521. Not monotone from the start: the falls sit at k = 3, 6, 9 (the period-3 rhythm of the early family). Full run k ≤ 32 on the
compute machine (santalo-32.log). Next: monotone from k = 9? a rise lemma for the hop; the stability constant needed.

**Full run (k ≤ 31; k = 32 ran out of memory, exit 137).** P rises at every step from k = 9 to 31: 0.99521 (18), 0.99713 (20), 0.99808
(22), 0.99860 (24), 0.99889 (26), 0.99906 (28), 0.99914 (30), 0.99916 (31). The rises shrink fast (7.5e-5, 9.8e-5, 5.0e-5, 3.4e-5,
1.2e-5 for k = 27..31): P may tend to about 0.9992, below 1, which matches the open shape question (limit slightly non-round, r/R ≈ 0.990).
Consequence: monotone from k = 9 (to 31) holds; but if the limit is not the ball, stability alone cannot reach t_min → 1; it still
suffices if the Santaló-stability distance at P ≥ 0.9991 keeps t_min ≤ 3/φ² (margin 0.145). Next: that stability constant (Böröczky
2010; Ivaki 2015), and a rise lemma for one hop.

## §21 Santaló route: closed for a proof (10 Nov 2026, literature check; DICTO "go ahead with both")
Stability theorem (K. J. Böröczky, Stability of the Blaschke–Santaló and the affine isoperimetric inequality, Adv. Math. 2010,
arXiv 0901.3340; K. Ball and K. J. Böröczky, arXiv 0909.3742): in dimension n ≥ 3, vol(K)vol(K°) ≥ (1 − ε)ω_n² gives a Banach–Mazur
distance to an ellipsoid of at most 1 + γ ε^{1/(6n)} |log ε|^{…}, and the paper states that γ was not made explicit (the exponent
1/(6n) being likely far from optimal). For n = 3 the exponent is 1/18. Our family: ε = 1 − 0.99916 = 8.4·10⁻⁴ at k = 31, so
ε^{1/18} ≈ 0.675: even with γ = 1 the bound allows distance ≈ 1.67, far above the 1.146 needed. Two further facts close it: the
product levels off near 0.9992 (ε does not tend to 0), and the planar or symmetric-difference results (Ivaki, arXiv 1405.5384;
arXiv 1411.3842; arXiv 2602.20325, origin-symmetric, symmetric difference) do not give the sup-norm closeness t_min needs.
**Verdict: the Santaló route cannot prove Conjecture 1 with known theorems.** The monotone rise of P from k = 9 to 31 stays a
recorded observation. Sources checked: arXiv 0901.3340, 0909.3742, 1405.5384, 1411.3842, 2602.20325; users.renyi.hu/~carlos
(zonoid stability, Böröczky–Hug), renyi.hu/~carlos/prekopaleindlerhigh.pdf.

## §22 Cut lemma, the counting step (A1): data k ≤ 22 (10 Nov 2026, cut_lemma.py, data/cut-lemma-22.log, FINAL ok)
Polar picture: candidate v of X_k is cut iff its foot point is not a corner of D_{k+1}; a cutter is a corner w with w·v > |w|².
- Every cut candidate has a cutter, and its cutters always include an ACTIVE corner (all levels).
- Cut fraction at most 0.437 (k = 14); 0.15–0.29 for k ≥ 16; never above a half. So growth (A) holds at every computed level.
- The matching proofs FAIL: a one-to-one matching of cut candidates to distinct active cutters misses at k = 9, 12, 14, 16, 17,
  19–22 (e.g. 1920/2300 at k = 22); even letting each active cutter take two fails at k = 14 (420/552), 19 (1292/1412), 20 (1692/1872).
  Some active corners cut three or more candidates, so "c ≤ active" cannot come from local one-to-one or two-to-one charging.
Verdict: (A1) holds in the data with margin (≤ 0.44 < 0.5) but needs a global argument (area or angle weighting of the active faces of
X_{k+1}, or the degeneracy pattern of the icosahedral orbits), not a local matching. Next idea to test: charge each cut candidate to
the active face of X_{k+1} whose angular cell contains it, weighted by that cell's solid angle.
**Ray charge (10 Nov, same script, k ≤ 18):** charging each cut candidate to the active face of X_{k+1} its own ray meets first
also fails to be one-to-one: up to 3 cut candidates per face at k = 7, 9, 12, and 5 at k = 14 and 16. The cut candidates come in
clusters under single active faces (near-coincident candidates of one icosahedral orbit), which is why no local charge works.
So step (A1) is true in all data (cut ≤ 0.437) but needs a cluster-aware global count: e.g. count clusters (orbit classes of
near-coincident candidates) instead of candidates, together with the excess e of §19. Logged as the next idea; no further runs now.

## §23 The #104 sweep applied to the hop (11 Nov 2026; DICTO: "could we not use anything from permutahedron studies" → "yes start the pilot"; scripts/og_sweep.py, data/og-sweep-22.*, watched jobs og-sweep-16 and og-sweep-22, FINAL ok)
Slider T_λ = {y : X_j·y ≤ |X_j|² + λ} over the candidates X_j (corners of X_k): stacked over λ it is ONE convex 4D polyhedron (as the
power cells of #104); each facet's λ-range is [λ_i, ∞), so faces only die going down, exactly once, and cut ⇔ λ_i > 0 (one LP per
orbit). Controls at every k ≤ 22: sweep cut set = hull cut set; mass conserved; no orphans. Deaths are mostly generic (dies among 3),
with symmetric clusters up to 15 at one point.
Note: the sweep's h-vector relation (Dehn–Sommerville on the capped 4D polytope) gives only deaths = F_top − F_bottom, i.e. Euler again
(same as the g-theorem in 3D); the content has to come from geometry, hence the flow tests.
- Equal-split mass flow (dying face → faces it dies among that outlive it): max active mass < 2 FAILS (3.2–3.7 at k = 11–13, 7.56 at
  k = 14, 6.92 at k = 21); mean ≤ 1.78 at every k (= the cut fraction ≤ 0.437).
- BEST flow (max-flow, least possible max active load c*): c* = 1, 1, 1, 1, 1, 1.5, 1.5, 1.5, 1, 1.75, 1.73, **3.20**, 2.29, 3.20, 3.20,
  1, 3.00, 2.58, 2.00, 2.33, 2.00, **4.50**, 2.45 (k = 0…22). c* ≥ 2 at k = 11–14, 16–22: some sets of active faces are the only outlet
  for more than twice their number (Hall violations, e.g. 16 into 5 at c* = 16/5, 9 into 2 at k = 21).
**Verdict: no charging along the sweep's own neighbour relation proves cut < active; step (A1) is a global (average) fact, as §22
found for the hull's cutters.** Sweep route closed for a local proof. What stays: the exact one-death-per-face structure and the
λ-ordering (usable for an averaging argument: e.g. a solid-angle or area-weighted count of the 4D facets).

## §24 Births and deaths exchanged between hops (11 Nov 2026; DICTO: "or the number of births to deaths being exchanged"; scripts/og_born_die.py, data/og-born-die-14.json, local, FINAL ok)
Faces of D_k classed as BORN at hop k−1 (normal not a face normal of D_{k−1}) or SURVIVING; CUT at hop k = foot point not a corner of D_{k+1}.
Result k ≤ 14: the hop renews EVERY face except, from k = 10, the 12 faces on the 5-fold axes (k ≤ 9: all faces born). So births and
deaths are exchanged completely at each hop (corners ↔ faces, the polarity), cut ≤ born holds trivially (born ≈ all), and the 12
survivors are exactly 'cut' in the polar sense (their foot point lies inside the surviving face, Lemma G). The count reduces to the
step-(A) identity F_k = 2(F_{k−1} − c_k) − 4 − e_k: no new inequality from this reading.

## §25 A balancing 4D shadow? plane speeds (11 Nov 2026; DICTO: "is it possibly a different 4D shadow", "a balancing one"; scripts/og_sweep_speeds.py, data/og-speeds-22.*, watched job og-speeds-22, FINAL ok)
Same hop, plane j moving at speed s_j = |X_j|^q: every valid q has the same top (all faces) and bottom (X_{k+1}) but a different 4D shape.
Valid: q ∈ [0, 1] at every level; q = 1.5 and 1.8 lose faces at the top from k = 5–6 (not valid shapes; q < 0 also invalid, local pilot).
Result: best-flow c* is IDENTICAL for q = 0, 0.5, 1 at every k ≤ 22 (worst 4.50 at k = 21). The overload does not depend on the speeds:
it is fixed at the bottom (groups of active faces that are the only possible outlet for many cut faces whatever the order of deaths).
Verdict: no balancing speed exists in this family; next form of the idea (if pursued): per-orbit speeds cannot help either where the
outlet set is forced by tightness at λ = 0 itself, so a balancing argument must weight faces (solid angle / area), not reorder deaths.

## §25a Wall spacing in the sweep (11 Nov 2026; DICTO: "what is the distance between walls if they are cell walls"; scripts/og_walls.py, local, k ≤ 14)
Walls = slider heights λ where cut faces die (scutoid reading: faces = cells between the top slice and X_{k+1}), in units of R(X_k)²
(scale-free). One wall per orbit class of dying faces: 1 (k = 5, 6), 2 (7), 4 (9), 3 (10, 11), 4 (12, 13), 9 (14). Heights k = 14:
0.0066, 0.0132, 0.0559, 0.2144, 0.5402, 0.7356, 0.8341, 0.8585, 0.9348. Gaps irregular (0.0065 … 0.4626), no constant spacing or
ratio. Walls very near the bottom (0.0066–0.0089 at k = 9, 14) = faces that only just die; k = 14 has both the most walls and the
largest cut fraction (0.437).

## §25b Shell thickness (11 Nov 2026; DICTO: "measure the shell thickness too"; scripts/og_shell.py, data/og-shell-16.json, local, FINAL ok)
Along 20 000 rays + the axes, ρ_k = distance O→boundary of D_k. Gnomon shell of the grown family (φ^{k+1}ρ_{k+1} − φ^kρ_k, relative
to φ^kρ_k = φρ_{k+1}/ρ_k − 1): never negative (Cor. 1 control); range 0.43–0.62 at 0→1, narrowing to 0.600–0.626 (mean 0.614) at
16→17: the shell tends to an EVEN layer of relative thickness 1/φ = 0.618. Exactly 0.6180 on many axes at many levels (ρ unchanged:
Lemma G equality). Unscaled shell: D_{k+1} inside D_k on 55–100 % of rays; out at most 1.8 %, in at most 13 % of the mean radius;
from k = 10 within ±2.6 %, mean −0.2 … −0.5 %: the two surfaces interleave almost on top of each other.

## §28 The Galois twins (11 Nov 2026; DICTO: "maybe a 5D penrose type", "yes run the twin test", "maybe there is a scutoid type exchange between twins"; scripts/og_twin.py, data/og-twin-10.json, exact Q(√5), the compute machine, FINAL ok)
Penrose = cut-and-project from 5D; icosahedral = 6D, and the twin (√5 → −√5) is the perpendicular-space coordinate. Exact corners of
D_0 … D_10, twin computed without cancellation as (a² − 5b²)/(a + b√5). Coordinates' digits 4, 6, 7, 14, 18, 25, 44, 78, 231, 567, 1780:
no fixed lattice (unbounded denominators), so no model set in the usual sense. But the twins COLLAPSE to the centre: largest twin radius
0.628, 0.544, 0.471, 0.218, 0.078, 0.068, 0.028, 2.1e−3, 3.3e−4, 7.1e−5, 1.8e−5 (k = 0 … 10; about ×0.35 per level, irregular), while the
real radius settles near 1.2. Why: Galois conjugation commutes with the foot-point formula p = (n·a / n·n) n, so the twin family is the
SAME hop on the twin points with the faces chosen by the real hull; in twin space those member sets are not convex faces (twin hull
has only 12–180 of 80–500 points as corners), their planes pass near the centre, and the pedal step contracts.
Exchange between the twins: real neighbour pairs (hull edges) that are also twin hull edges: 20 % (k = 0, 1), then 0–5 %, 0.2–0.8 % at
k = 9, 10: the twins exchange almost ALL neighbours (scutoid-type exchange is nearly complete).
Reading: one real direction neutral (radius settles), the conjugate direction contracting (like a Pisot unit); the 'window' shrinks
to a point. Not a proof route yet; lead: does the contraction rate tie to the cut fraction (both come from how far the faces are from
convex in twin space)?
**§28a Vacuus and non-convex sheets (DICTO: "its a vacuus", "non convex sheets", "like a prism"; same script, FINAL ok).**
Vacuus ratio = distance of each face's TWIN plane from O ÷ twin size of that face (0 = a sheet through the centre, as the fins of a
Vacuus). Real faces: median 0.93–0.99. Twin faces: median 0.87 (k = 0), 0.32–0.40 (k = 1–5), then 0.009, 0.11, 0.12, 0.08, 0.12 (k = 6–10),
max up to 0.7: the twin faces lie far nearer to sheets through the centre than the real ones (about a tenth of their size off-centre
from k = 6), but do not tend to 0: nearly a Vacuus, not exactly.
Sheet shapes (each face's corners in their REAL order, drawn in twin coordinates): NO face is merely non-convex; every non-convex twin
face is SELF-CROSSING (a star): 12 at k = 1, 3, 5 (the five-fold faces: pentagon → pentagram, the classical Galois swap of
icosahedral solids ↔ Kepler–Poinsot stars), 72, 60, 72, 32 at k = 7–10; all others convex. So the twin family is a Kepler–Poinsot-type
star family of sheets packed close round the centre. Lead: DICTO's Kepler–Poinsot papers (#? 2026-10-19-kepler-poinsot-*).

## §26 Balance laws (DICTO 11 Nov) — DRAFT, not yet in the README
DICTO: "can you check all the different balance laws for all the 4D polytopes and figure out if this may be an expression of a new law".
Scripts: scripts/balance_weights.py (data/balance-weights-14.*, FINAL ok), scripts/generic_hop.py (data/generic-hop-s1.*, -s2.*,
FINAL ok both), scripts/hop_counterexample.py (data/hop-counterexample.log, data/hop-counterexample-small.log, FINAL ok both). All local, float.

**Conclusion: "cut < half" is NOT a law of the hop. It fails for generic convex polytopes (origin off centre: up to 0.90 cut; a
10-face polytope with 6 cut), and even for near-round, icosahedrally symmetric starts (0.628). Every known balance law holds for those
counterexamples, so no combination of known laws can prove step A1; the proof must use what is special to the OG family.**
**Status: A1 stays open (true in OG data ≤ 0.437); the "new law" reading is REFUTED; a weaker limit law (≈ 0.30 for fine near-round
polytopes with the origin central) is a candidate observation only.**

### 26.1 The laws, one line each
(a) one solid D_k; (b) the swept 4D polytope of §23; (c) the pair D_k → D_{k+1}. "Ineq.?" = can it bound the cut fraction?

| Law | Statement | (a) | (b) | (c) | Ineq.? |
|---|---|---|---|---|---|
| Euler–Poincaré | Σ(−1)^i f_i = 1 − (−1)^d (3D: V − E + F = 2) | yes | yes | gives F_{k+1} = 2(F_k − c) − 4 − e (§19) | no: an identity; c stays free |
| Dehn–Sommerville | h_i = h_{d−i} (simplicial/simple) | only if simple | yes (capped sweep, §23) | no | no: gives Euler again (§23) |
| Bayer–Billera / cd-index | all linear relations on flag f-vectors; cd-index coefficients ≥ 0 (Stanley, polytopes) | yes | yes | no | nonnegativity is an inequality but on one polytope's flags, not on c |
| g-theorem, UBT, LBT | g-vector conditions; f_i ≤ cyclic polytope; f ≥ stacked | yes | yes | no | bounds F against V of ONE polytope; c compares two polytopes |
| Minkowski balance | Σ A_i n_i = 0; facet data determine P up to translation | yes | (4D) yes | no | metric but symmetric (OG: = 0 trivially); measured below |
| Gram / Brianchon–Gram | Σ(−1)^i Σ_faces interior angle = 0 | yes | yes | no | metric terms; measured below (τ) |
| Sommerville, Perles–Shephard | angle sums of simplicial polytopes, DS-type; with Gram they are all linear relations on angle sums (Höhn) | if simplicial | yes | no | linear: same obstacle |
| Descartes / Gauss–Bonnet | Σ corner defects = 4π | yes (X_k) | 4D analogue | no | metric; measured below (ω) |
| Steiner / quermassintegrals, Alexandrov–Fenchel | V(K + tB) polynomial; V(K,L,…)² ≥ … | yes | yes | pair as K, L possible | inequalities, but on volumes, not on counts |
| Blaschke–Santaló | vol K · vol K° ≤ ω_n² | done §20–21 | – | – | closed |
| Dehn invariant | Σ ℓ_e ⊗ θ_e ∈ ℝ ⊗ ℝ/πℚ (scissors class) | yes | yes | no | not order-valued: no inequality possible |

Why the linear combinatorial laws cannot bound c: c = F(D_k) − V(D_{k+1}) mixes two polytopes. Each law constrains one polytope
(or one 4D sweep). Decisive form (§26.3): there are honest convex polytopes with c > F/2. They obey every law in the table, so no
combination of these laws implies c ≤ F/2.

### 26.2 Weighted laws split cut vs active on the OG family (k ≤ 14; checks Σω = 4π, Minkowski, cone volumes = volume, Gram ≈ 1e-12, all pass)
Share of each weight carried by the CUT candidates (faces of D_k). Weights: area A (Minkowski), ω = solid angle the face subtends = Descartes
defect of X_k at the polar corner, τ = interior solid angle of X_k at that corner (Gram term), cone volume.
k: count | A | ω | τ | vol | mean d cut/active
5: 0.238 | 0.355 | 0.359 | 0.229 | 0.352 | 0.985 · 6: 0.188 | **0.710** | **0.719** | 0.162 | 0.706 | 0.973 · 7: 0.224 | 0.121 | 0.126 | 0.232 | 0.119 | 0.986
9: 0.344 | **0.685** | **0.697** | 0.339 | 0.678 | 0.992 · 10: 0.290 | 0.554 | 0.561 | 0.276 | 0.552 | 0.986 · 11: 0.196 | 0.333 | 0.341 | 0.190 | 0.325 | 0.957
12: 0.279 | 0.351 | 0.356 | 0.276 | 0.348 | 0.986 · 13: 0.176 | 0.226 | 0.230 | 0.175 | 0.224 | 0.986 · 14: 0.437 | 0.506 | 0.510 | 0.438 | 0.503 | 0.989
(k = 0–4, 8: nothing cut.)
- Cut faces are not the small ones. They are LARGER on average (area/ω share above the count share at every level except k = 7), so
  "Σ_cut A ≤ Σ_active A" and "Σ_cut ω ≤ 2π" FAIL (k = 6, 9, 10, 14).
- τ (Gram) share ≈ count share (τ ≈ 2π for these nearly flat corners): it repeats the count and adds nothing.
- Best surviving weighted statement: **cut faces sit nearer the origin on average**: mean d(cut) / mean d(active) = 0.957–0.992 at every
  level with cuts. But no threshold: max d(cut) > min d(active) at k = 9, 10, 12 (and a tie at k = 5).
  The general fact behind it: the face of largest d is always active.
  No weighted form found that holds with margin at every level.

### 26.3 New-law test: generic starts (48 runs, 5–8 hops each; Euler identity, no duplicate foot points; every over-half hop with
F ≤ 1000 re-checked candidate by candidate by LP, 24 hops, all agree)
| start class | max cut fraction | max mean load | last-hop fraction |
|---|---|---|---|
| S near-sphere points, noise 1–20 %, origin central | 0.308 | 1.45 | 0.24–0.31 |
| H random half-spaces, offsets in [1−s, 1] | 0.344 | 1.53 | 0.23–0.33 |
| I icosahedral (60 rotations), noise 1–20 % | **0.628** (n = 100, 20 %, hop 5: 540 of 860; LP-verified) | 2.69 | 0.11–0.41 |
| E ellipsoid, origin off centre | **0.901** | 10.06 | 0.22–0.44 |
Smallest counterexample found (random search, 80 000 trials): a flat polytope with 7 corners and 10 faces, origin near two of its faces;
the hop cuts 6 of 10 faces (LP-verified, depth 4.6e-2; corners in data/hop-counterexample.log). Since P(D) has ≥ 4 corners, F ≥ 9 is needed
for c > F/2, so 9 faces may be possible; not found.
**Verdict: no general law.** Off-centre origins break it at once. Symmetry alone does not save it: whole 60-orbits are cut together, so the
fraction jumps. What is left as a candidate observation: after many hops, starts that are fine and near-round with the origin central
settle near 0.30 cut (mean load ≈ 1.43). The hop rounds even the E starts back toward this (0.9 → 0.3 in 8 hops). The OG family
(≤ 0.437, period-3 spikes) behaves like the I class.
So step A1 for the OG needs OG-specific input: the near-roundness from #43 (t_min ≤ 3/φ² keeps the origin central) together with the orbit
structure, e.g. "if D is within factor t of round, then c ≤ g(t)·F", with g(3/φ²) < 1/2. The E runs give the right shape of test for g.

### 26.4 Prior art
Planar pedal polygons and iterated pedal triangles are studied (chaotic, a full shift on four symbols: J. C. Alexander, Math. Mag. 66 (1993) 147–158;
A. Manning, Bull. LMS 42 (2010) 673–679; arXiv 1312.0281; arXiv 2108.08293 "Topics on pedal polygons"). These keep every foot point
and take no hull, so they say nothing about redundancy. No source found on the 3D "hull of the foot points" map, its iteration, or a
"half the facets are redundant" bound. Random Voronoi-cell f-vector work (arXiv 1909.13335, 2506.02607, 1612.03029) gives expected facet
counts but no redundancy fraction for this map.
Queries run: "pedal polytope foot points of facet hyperplanes convex hull iterated pedal body"; "iterated pedal polygon convergence";
"fraction of redundant constraints Voronoi cell of origin random points expected number of facets half"; "pedal convex body polar
Voronoi cell map iteration polytope sphere convergence circumcentres Delaunay"; "Perles Shephard angle sums … Gram relation …
complete"; "Manning pedal triangle ergodic full shift".
Laws sources: Ziegler, Lectures on Polytopes, ch. 8 (f-vectors, Dehn–Sommerville, UBT, g-theorem). Grünbaum, Convex Polytopes,
ch. 8 (Euler), 9 (Dehn–Sommerville), 10 (UBT/LBT), 14 (angle sums: Gram, Sommerville, Perles–Shephard). Bayer–Billera, Invent. Math. 79
(1985) (generalized DS). Bayer–Klapper, Discrete Comput. Geom. 6 (1991) (cd-index). Stanley 1980 and Billera–Lee 1981 (g-theorem).
Barnette 1973 (LBT). Schneider, Convex Bodies: The Brunn–Minkowski Theory (2nd ed. 2014): ch. 5 (mixed volumes), §7.3
(Alexandrov–Fenchel), §8.2 (Minkowski existence/uniqueness). Perles–Shephard, Math. Scand. 21 (1967); Shephard, Canad. J. Math.
19 (1967); Camenga, arXiv math/0607469 (Höhn: Gram + Perles are all linear angle-sum relations). Sydler 1965 (Dehn invariant).
The books and papers are cited from standard knowledge and were NOT re-opened this session. Section numbers should be checked
before publication. The web sources above were opened through search results.

**Judged (11 Nov, main session):** accepted. One correction: the icosahedral counterexample (0.628 at hop 6) started from 20 % radial noise (generic-hop-s1.log, class I, s = 0.20), so 'near-round' overstates it; its roundness at that hop was not measured. Conclusion stands: cut < 1/2 is not a general law of the hop; a proof needs the OG's own roundness (t_min ≤ 3/φ²) and orbit structure, e.g. c ≤ g(t)·F with g(3/φ²) < 1/2. Next test for that form: cut fraction against t_min over the generic runs.

## §29 Leaning Vacuus pyramids? (11 Nov 2026; DICTO: "we did vacuus survey earlier of all the shapes"; scripts/og_vacuus_lean.py, data/og-vacuus-lean-14.json, local, FINAL ok)
In D_k's Vacuus (#87) each face has its centre pyramid; the foot point d n lies inside its own face (upright) or outside (leaning).
Test cut ⇔ leaning, k ≤ 14: FALSE. Cut but upright at every level with cuts (60, 60, 30, 72, 72, 132, 72, 192, 192 for k = 5 … 14,
including the 12 five-fold faces whose foot point is the face centre: lean −0.8090 = −cos 36°, cut in the polar sense of §24);
survive though leaning: 60 … 720. Lean of cut faces from −0.85 to positive; of survivors up to +1.93. The Vacuus lean does not
decide the cut (the cut is a property of the foot points together, not of one pyramid).

## §30 Cut fraction vs roundness (11 Nov 2026; DICTO: "run the cut fraction vs roundness test"; scripts/roundness_hop.py, data/og-roundness.*, watched job og-roundness, 40 seeds × 4 start kinds × 8 hops = 1280 hops, FINAL ok)
#43's t (D inside t·P(D)) is NOT a roundness measure: t ≤ 3/φ² still allows cut 0.718 (pilot: t 1.143 with cut 0.853 at R/r 5.4).
Roundness R/r (from O): non-icosahedral starts never exceed cut 0.405 for R/r < 1.5 and 0.412 for R/r < 2; over 1/2 only when
R/r ≥ 2. ALL 8 round over-half hops (R/r 1.03–1.08, cut 0.508–0.718) are ICOSAHEDRAL starts: whole 60-orbits cut together.
Verdict: for generic shapes the data show a roundness law (cut ≤ 0.41 for R/r < 2); icosahedral symmetry is what breaks it, so
step A1 for the OG must use the OG's own orbit structure, not roundness alone. DICTO (11 Nov): "most likely a 4D Vacuus that is
very sophisticated but that should narrow it down".

## §27 Scutoid exchanges in the hop (DICTO 11 Nov; "nothing from exchange of communication of scutoids helps?", then "shape of cells how many walls" and "a or c, the sheets are continuous"; scripts/og_exchanges.py, data/og-exchanges-5-16.*, data/og-exchanges-17-18.*, local, both runs FINAL ok)

**Conclusion: exchanges do not bound the cut.** c ≤ s holds at every level k = 5 … 18, with equality at k = 7, but s is not a
fixed number of the hop (it changes with the tie-break), and s reaches 1.16 n (k = 5), so no inequality in s gives c < n/2. What the
scutoid view does give exactly: cut < active ⇔ the dying cells start with fewer sides than the survivors, in the precise amount
below (Euler at the top of the sweep, checked at every level). Cut cells have fewer walls on average than active cells at every
level, but the two ranges overlap.

**Method.** Same hop and slider as §23: P = {(y, λ) : X_j·y − λ ≤ |X_j|², 0 ≤ λ ≤ Λ}, Λ = 4 max|X_j|² (checked: every event lies
below Λ/4; all n candidates are faces of the top slice). Vertices of P by halfspace intersection in 4D; facets tight within 10⁻⁹
(the gap to the next facet is ≥ 2.8·10⁻⁷ at every level). A vertex with 4 facets has 4 edges; going down in λ, 3 up + 1 down = a
triangle dies, 2 + 2 = an exchange (two faces lose a side, two gain one), 1 + 3 = a birth (none found). Symmetric clusters
(5 to 15 facets at one point) and degenerate slice corners (axis corners, persistent over λ) are resolved by a symbolic random
perturbation in three orders: offsets δε_j, then a tilt ηξ_j of the plane normals, then the cross term δη; each cluster is resolved
locally from its tight facets only, so no precision is lost. The tilt is needed because some faces die along a horizontal edge
(a four-sided face collapsing to a segment: the 30-orbit at k = 7), which an offset perturbation cannot break. Each run uses two
random tie-breaks. Cells and walls are read from the unperturbed slices between consecutive event levels.

Controls, every level k = 5 … 18, both tie-breaks: deaths = cut set of the hull (§22); tracked side counts = resolved slices at
the bottom and at up to 6 well-separated levels; every face dies as a triangle; Σ(top sides − 3) over dying faces = lost to
exchanges + lost to neighbour deaths − gained in exchanges; Σ sides = 2E, V − E + F = 2, 3V = 2E in every resolved slice (Σ = 6n − 12
at the top, 6a − 12 at the bottom); unperturbed slices: Euler, all faces present at the top, faces just above λ = 0 = active set;
every wall is a single λ-interval; cells of one orbit agree.

**Per level** (s = exchanges, tie-breaks 1 and 2; s_min = net side gains / 2 between unperturbed event levels, a lower bound for
any tie-break; m_c, m_a = mean top sides of dying and active faces; cl = exchanges at cluster points / at generic points):

| k | n | c | a | s | s_min | c/s | s/n | m_c | m_a | cl / gen | deaths in clusters |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 252 | 60 | 192 | 291, 284 | 150 | 0.21 | 1.155 | 4.20 | 6.50 | 291 / 0 | 60 |
| 6 | 320 | 60 | 260 | 270, 270 | 180 | 0.22 | 0.844 | 5.00 | 6.18 | 210 / 60 | 60 |
| 7 | 402 | 90 | 312 | 90, 90 | 0 | **1.00** | 0.224 | 4.67 | 6.35 | 60 / 30 | 60 |
| 8 | 500 | 0 | 500 | 300, 300 | 180 | 0 | 0.600 | – | 5.98 | 300 / 0 | 0 |
| 9 | 732 | 252 | 480 | 474, 474 | 360 | 0.53 | 0.648 | 5.00 | 6.50 | 174 / 300 | 12 |
| 10 | 662 | 192 | 470 | 444, 444 | 180 | 0.43 | 0.671 | 5.31 | 6.26 | 444 / 0 | 132 |
| 11 | 672 | 132 | 540 | 204, 204 | 120 | 0.65 | 0.304 | 5.45 | 6.11 | 24 / 180 | 12 |
| 12 | 902 | 252 | 650 | 511, 510 | 360 | 0.49 | 0.567 | 5.00 | 6.37 | 151 / 360 | 72 |
| 13 | 1092 | 192 | 900 | 384, 384 | 240 | 0.50 | 0.352 | 5.63 | 6.07 | 144 / 240 | 72 |
| 14 | 1262 | 552 | 710 | 934, 940 | 660 | 0.59 | 0.740 | 5.65 | 6.25 | 274 / 660 | 252 |
| 15 | 1392 | 0 | 1392 | 120, 120 | 120 | 0 | 0.086 | – | 5.99 | 0 / 120 | 0 |
| 16 | 2360 | 560 | 1800 | 1602, 1598 | 780 | 0.35 | 0.679 | 5.44 | 6.17 | 1122 / 480 | 360 |
| 17 | 2882 | 810 | 2072 | 1950, 1950 | 1560 | 0.42 | 0.677 | 5.19 | 6.31 | 720 / 1230 | 180 |
| 18 | 3780 | 720 | 3060 | 1158, 1168 | 900 | 0.62 | 0.306 | 4.32 | 6.39 | 198 / 960 | 120 |

Sides lost by the dying faces (tie-break 1), Σ(top sides − 3) = via exchanges + via neighbour deaths − gained:
k = 5: 72 = 88 + 25 − 41; 6: 120 = 99 + 21 − 0; 7: 150 = 120 + 30 − 0; 9: 504 = 444 + 180 − 120; 10: 444 = 444 + 60 − 60;
11: 324 = 204 + 180 − 60; 12: 504 = 520 + 195 − 211; 13: 504 = 324 + 240 − 60; 14: 1464 = 1388 + 836 − 760;
16: 1368 = 1294 + 716 − 642; 17: 1770 = 1890 + 900 − 1020; 18: 948 = 811 + 251 − 114. Exchanges carry 63–122 % of the net loss.
Top sides of dying faces: 3 to 9 (k = 9: 20 for the twelve 5-fold faces); the dying face is a triangle only at the end.

**Laws tested.**
- c ≤ s/2: FAILS at k = 7, 9, 11, 13, 14, 18.
- c ≤ s: holds at every level, equality at k = 7 (no margin). Not usable: s depends on the tie-break (291 vs 284 at k = 5, 934 vs
  940 at k = 14), the tie-break-free bound s_min gives c ≤ s_min FALSE at k = 7 (90 > 0), 10 (192 > 180) and 11 (132 > 120), and
  s/n reaches 1.155, so c ≤ s cannot give c < n/2. Exchanges are not bounded relative to the cut in either direction (k = 8, 15:
  300 and 120 exchanges with no cut at all).
- **Exact (Euler at the top, a simple slice with Σ sides = 6n − 12):** c/a = (m_a − 6 + 12/a)/(6 − m_c), equal to the data at every
  level. So cut < active ⇔ m_a − 6 + 12/a < 6 − m_c: the survivors' excess over six sides is smaller than the dying faces' deficit.
  Excess vs deficit: 0.56 vs 1.80 (k = 5), 0.23 vs 1.00, 0.38 vs 1.33, –, 0.53 vs 1.00, 0.28 vs 0.69, 0.13 vs 0.55, 0.39 vs 1.00,
  0.08 vs 0.38, **0.27 vs 0.35 (k = 14, least margin)**, –, 0.17 vs 0.56, 0.32 vs 0.82, 0.40 vs 1.68 (k = 18). This is the
  growth identity of §19 seen from the top of the sweep, not a new inequality, but it moves the question to the top slice alone.
- Clusters: at k = 11–14, where the flow tests of §23 failed, exchanges sit mostly at GENERIC points (24 of 204, 151 of 511, 144 of
  384, 274 of 934 at clusters); what concentrates there is deaths (k = 14: 252 of 552 deaths in clusters). Exchanges dominate the
  clusters at k = 5, 6, 8, 10, 16 instead.

**Cells (DICTO "shape of cells how many walls").** Each candidate's facet of P is a 3D cell: walls = distinct neighbours over the
sweep + top cap + bottom cap if active; corners = vertices of P on it; edges = walls + corners − 2. Kinds: PRISM (same walls top to
bottom), TRUNCATED PRISM (walls lost only to dying neighbours), SCUTOID (an exchange changes its walls), PYRAMID (cut; "exchanged" if an
exchange touched it before death). Counts per orbit class: the orbit lines in the logs (5 to 63 orbits per level). Mean walls,
active vs cut: 8.88 / 4.0 (k = 5), 8.23 / 5.0, 8.15 / 5.67, 7.64 / –, 8.75 / 6.48, 8.64 / 6.0, 8.11 / 6.91, 8.83 / 6.24, 7.6 / 6.62,
9.61 / 7.52 (k = 14), 7.56 / –, 8.53 / 6.36, 9.27 / 7.22, 8.75 / 5.25 (k = 18). **Cut cells have fewer walls on average at every
level**, but not cell by cell: active cells have 5–23 walls, cut cells 4–21 (k = 14: cut up to 10, active down to 5). Kinds at
k = 14: 470 scutoids, 240 prisms, 540 pyramids after exchanges, 12 plain pyramids; at k = 18: 1740 scutoids, 1080 prisms, 240 truncated
prisms, 540 + 180 pyramids. The commonest cut cell is a 5-walled pyramid (a four-sided top, 6 corners: one exchange, then the
death point); the smallest is the tetrahedron (4 walls, 4 corners).

**Walls as sheets (DICTO "a or c, the sheets are continuous").** Every wall between cells i and j is one λ-interval at every level
(control passed: convexity of P). Per level, walls full height / start partway (born at an exchange) / end partway (at an exchange
or a death) / both: k = 5: 330/180/240/0 of 750 (44 % full); 6: 480/180/270/0 (52 %); 7: 780/30/360/0 (67 %); 8: 1050/180/180/0
(74 %); 9: 840/300/1110/60 (36 %); 10: 960/180/900/0 (47 %); 11: 1320/120/540/60 (65 %); 12: 1500/240/1020/120 (52 %);
13: 1920/240/840/60 (63 %); 14: 1740/360/2040/360 (39 %); 15: 3630/120/120/0 (94 %); 16: 4020/660/2550/150 (54 %);
17: 4860/990/3600/600 (48 %); 18: 7770/900/3120/60 (66 %). The cut cells are exactly the cells none of whose walls reaches λ = 0
(every level; this is the definition of cut seen from the walls, a control rather than a law). Parallel pairs: the two caps of an
active cell are parallel by construction; parallel SIDE walls (normals ±parallel inside the cell) occur only once: one 60-orbit
of active scutoids at k = 9, one pair each. So the cells are not prisms with parallel ends in the side walls; the sheets are flat
and continuous but tilted.

**Verdict.** The scutoid exchanges do not prove step (A1): their number is not intrinsic and is not bounded by, nor bounds, the cut
with any margin. The usable exact form is the top-slice identity: cut < active ⇔ dying faces' side deficit > survivors' excess
(least margin 0.35 vs 0.27 at k = 14).

**LEADS.**
1. The top slice is fixed by X_k alone: at large λ, T_λ/λ → {X_j·y ≤ 1} = polar of X_k, with ties broken by the offsets |X_j|², i.e.
   a regular (lifted) triangulation of the non-triangular faces of X_k. So top sides of j = number of edges at corner X_j of X_k
   after that triangulation (expected; to check). The law to prove becomes: corners of X_k that get cut have few edges (mean
   ≤ 5.65) and survivors have mean below 6 + deficit − 12/a. A degree lemma on X_k, not a sweep lemma.
2. Test whether "cut ⇒ top sides ≤ 5" holds per orbit (k = 9 has twelve 20-sided cut faces on the 5-fold axes, so it needs the
   axis exception of §24).
3. If pursued: the area-weighted version (§25 verdict) on the top slice only.

Concordance ledger line (ready): 2026-11-11 · #43 Conj. 1 step (A1) · scutoid exchanges in the hop sweep, k = 5–18 · c ≤ s holds
(equality k = 7) but s is tie-break dependent and up to 1.16 n; c ≤ s/2 and c ≤ s_min fail · exact top identity
c/a = (m_a − 6 + 12/a)/(6 − m_c) · cut cells fewer walls on average, ranges overlap · route closed for a counting proof; lead: degree lemma on X_k.

## §30a The census solids as starts (11 Nov 2026; DICTO: "yes add the census shapes"; scripts/census_hop.py, census-list.txt, data/og-census-hop.*, watched job, FINAL ok)
The 100 solids of the #87 Vacuus census (classical + DICTO solids), 8 hops each: 98 run (Dodeca-13 Needle and Wedge: origin not
inside), 784 hops (770 robust). NO hop cuts more than half. The maximum is EXACTLY 1/2 (Icosaxes Hexa, hop 1, R/r 1.3–1.5); next
0.482 (Unicorn), 0.444, 0.429 (White Rabbit), 0.411 (Jabberwock); means 0.02–0.21. So random icosahedral starts break the bound
(§30) but none of the real (crafted) solids does, and Icosaxes Hexa attains it: a candidate EQUALITY case for 'cut ≤ F/2'.
Lead: what do the census solids share that the random icosahedral sets lack (rational/Q(√5) coordinates? few orbits?).

## §31 4D Vacuus of the sweep — pilot (11 Nov 2026; DICTO: "c the permutahedron 4D vacuus", "yes go ahead"; scripts/og_vacuus4d.py, local, k = 5–7, FINAL ok)
Central slice through c = (O, lc) containing wall (i, j): normal (lc + b_j)(X_i, −1) − (lc + b_i)(X_j, −1), linear in lc; special
heights = exact common roots of the 2×2 minors. Walls 750, 930, 1170; generic slice counts 465, 615, 1035 (same at three generic
heights). The biggest drops sit at lc = −b_i (−1 = −max b): there the centre lies on cell i's own hyperplane and all walls of the
outermost cells fall into that hyperplane — a TRIVIAL coincidence. Non-trivial drop: k = 7, lc = −0.896234 (2237 coinciding pairs,
1035 → 943 slices). Rounding of the slice key (1e-8) splits near-coincidences at some special heights (counts above generic):
counting must use exact or interval comparison. NEXT: exclude lc = −b_i, count by exact parallelism (Q(√5) for k ≤ 10), then the
slice-type test (cut vs surviving cells).

## §32 Against the 600-cell (11 Nov 2026; DICTO: "I thought every 4D was identified" → "yes test it against the 600-cell"; scripts/og_600cell.py, data/og-600cell.json, FINAL ok)
Only regular and uniform 4D polytopes are catalogued; the hop's sweep is an irregular icosahedral 4D polytope, new at each level. Test:
600-cell vertex axis along the slider, its H3 matched to our icosahedral orientation (exact, Kabsch on the 5-fold axes); one slider
scale s per level for ALL cells (scanned + every s that makes one orbit exact); count orbit classes of cell normals along the 600-cell's
120 vertex or 600 cell-normal directions (1e-6). Baseline: same directions, random radii per orbit (50 draws).
Result k = 5 … 12: at most 1 orbit class of 5–17 matches at any single scale, exactly as many as the random baseline (mean 1.00,
max 1). The one match is an axis orbit fitted by the free scale. Verdict: the sweep is NOT a 600-cell slice or shadow in this sense.
**§32a Remaining 600-cell direction families (DICTO "try it").** The icosahedral group sits in H4 only as the stabiliser of a 600-cell
vertex (= 120-cell cell centre), so the slider axis is forced; tested also the 600-cell's 720 edge midpoints and 1200 triangle centres
(= 120-cell edge directions), k = 5 … 12: again at most 1 orbit class per level, equal to the random baseline. No 600-cell/120-cell structure.

## §33 Listening for silences (11 Nov 2026; DICTO: "can we use resonance or spherical wave tech", "og family has icosahedral so listen for silences"; scripts/og_silences.py, data/og-silences-14.json, the compute machine, FINAL ok)
log ρ_k expanded in spherical harmonics to degree 40 (30 000 rays). Degrees allowed by the rotation group I: 6, 10, 12, 15, 16, 18, 20,
21, 22, 24–28, 30 (×2), 31–35, 36 (×2), 37–39, 40 (×2); forbidden energy ≤ 8e−7 of the total (control).
SILENT at every level k = 0 … 14: exactly the ODD allowed degrees 15, 21, 25, 27, 31, 33, 35, 37, 39 (energy 2e−5 … 4e−4 of the median,
the quadrature floor). Explained: the OG family is centrally symmetric (full I_h ∋ −1), and a centrally symmetric shape has no odd
waves. Every EVEN allowed degree sounds at every level: no unexplained silence up to degree 40.
Sign flips between hops (the corner ↔ face swap heard as waves): 4–13 even degrees flip at each hop (13 at hop 7→8), degree 6 at hops
1→2, 3→4, 8→9, 13→14 — no fixed period; no single resonant mode.
Verdict: the spectrum holds no hidden silence beyond central symmetry; leads: (1) a silence may appear for the TWIN family (§28) or in
the sweep's 4D waves; (2) look for silences in the hop's change f_{k+1} − f_k rather than in f_k.

## §31a 4D Vacuus, EXACT — centred and centre-free (11 Nov 2026; DICTO: "do the exact 4D vacuus count next", "a sheets without a centre", "so look for either"; scripts/og_vacuus4d_exact.py, og_vacuus4d_free.py, data/og-vacuus4d*.{json,log}, watched jobs, both FINAL ok)
Exact coordinates (Q(√5) → 60 digits); every coincidence and non-coincidence decided with a printed gap (≥ 1.3e−3 against 1e−40).
CENTRED (centre on the slider axis, k = 5 … 11): generic slice counts 465, 615, 1035, 1095, 1875, 1635, 1695 for 750 … 2310 walls;
hundreds of special heights (138 … 1088 non-trivial; trivial ones with the centre on a cell's hyperplane excluded); each merges whole
orbits (48 or 60 slices). At the strongest heights no slice ever mixes a survivor–cut wall with another wall type.
CENTRE-FREE: walls of different cells share a 3D sheet ⇔ their four cells' candidate points lie on ONE CIRCLE (h_m = (X_m, −1, −|X_m|²)
dependent ⇔ the paraboloid lifts are affinely dependent). k = 5 … 11: 3857, 5375, 5983, 8975, 14203, 12343, 11231 sheets; all float
hits confirmed exactly (0 rejected). Sheets meet the slider axis at 45 … 215 different heights (one height per orbit class): NO common
centre. In every level exactly 15 VERTICAL sheets (they contain the slider direction, 45 at k = 5) = the 15 MIRROR PLANES of I_h ×
the slider; they carry the most walls (14, 22, 10, 22, 30, 28, 24). Every cell, cut or surviving, lies on some sheet.
SEPARATION (both versions, every level): a sheet carrying a SURVIVOR–CUT wall carries only survivor–cut walls; the only mixed sheets
are the 15 mirror sheets at k = 6, 9, 10 combining cut–cut with survivor–survivor walls. The border between cut and surviving cells
lives on sheets of its own. Lead for step A1: count border sheets (circles through two survivor and two cut candidates).

## §34 Certified run toward 40 (11 Nov 2026; DICTO "yes take it to 40"; scripts/certified_orbit.py, data/og-certified-40*.{json,log}, watched job og-certified-40)
Orbit storage + float with a proved error bound (1e−12) + balls for close calls (2–15 per level from D_35) + exact point labels.
Validation: every t_min(D_k), k = 10 … 30, MATCHES certified-30 to 1e−9. **Certified t_min(D_k) < 3/φ² for every k ≤ 38** (t_min(D_38) ≤ 1.000098; D_39: 2 533 472 faces; first written as k ≤ 37)
(D_38: 1 873 742 faces, 15 844 orbits; t_min(D_37) ≤ 1.000083). Stops on the way: D_27 (normal match tolerance), D_29 (distinct
normals 1.4e−7 apart: faces now labelled by exact point keys) — both tooling, fixed. D_39: one face orbit with ≥ 4 coplanar members
not forced by symmetry → refused (balls cannot prove an equality); diagnosis job og-diag-39 decides: float merge vs genuine.

## §35 Derive and reduce (11 Nov 2026; DICTO: "derive and reduce possibilities")
What remains of #43 Conjecture 1 for all k: certified k ≤ 37 (§34, run to 40 resumed); for k > 37 the 4-step contraction (§12), whose
step (A) is "cut < half" (step A1) at every hop.
ELIMINATED today (ledger entries 139 on): local charges of every kind (matching, ray, sweep flow, any plane speeds, exchange budgets);
single-face tests (lean of the Vacuus pyramid, area, solid angle, distance); all linear balance laws (only Euler survives); roundness
alone (icosahedral sets break it); the 600-cell / 120-cell (no alignment); hidden silences (only the odd waves, = central symmetry).
REDUCED (exact, Euler at the top of the sweep, a simple slice with Σ sides = 6n − 12): c(6 − m_c) = a(m_a − 6) + 12, so
   step A1 (c < a)  ⇔  6 − m_c  >  m_a − 6 + 12/a,
m_c, m_a = mean sides at the top of the sweep of the faces that die / survive. The total deficit of the dying faces always exceeds the
total excess of the survivors by exactly 12; A1 asks that it is spread over FEWER faces. Data: deficit 0.35–1.80 vs excess 0.08–0.56
(least margin k = 14: 0.35 vs 0.27). The top slice depends on X_k alone (D_k with its corners split by the weights |X_j|²), so the whole
question is now a statement about ONE polytope per level.
POSSIBILITIES LEFT (three, in order of promise):
 (P1) TOP-SLICE RULE: survivors are nearly hexagonal at the top (m_a ≤ 6.5 seen) and the dying faces are pentagons/quadrilaterals
      (m_c ≤ 5.65); find the rule that decides death from the top slice (sides in D_k + extra sides from corner splits).
 (P2) BORDER SHEETS (§31a): every survivor–cut wall lies on a concyclic sheet of its own; bound cut cells by border circles.
 (P3) ORBITS: whole orbits die together; with orbit sizes 12, 20, 30, 60 and the census bound (≤ 1/2, equality Icosaxes Hexa), a
      count by orbit types.
NEXT: (P1) per orbit at the top slice: sides in D_k, extra sides from splits, die/survive; look for the exact rule.

## §36 Possibility 1: a top-slice rule? (11 Nov 2026; DICTO: "yes run possibility 1"; scripts/og_topslice.py, data/og-topslice.json, the compute machine, FINAL ok)
Per orbit class, k = 5 … 14: sides in D_k, sides at the top of the sweep, extra sides from corner splits, dies or survives.
NO side rule decides death. Same (D_k → top) types both die and survive (3→5, 3→7, 4→4, 4→6 at k = 7, 9, 11, 12, 14). Tested rules:
"top sides ≤ 5" (right 1206, wrongly flagged 2642, missed 576), "no extra sides" (606 / 722 / 1176), "fewer top than D_k sides"
(12 / 0 / 1770: only the five-fold faces), "triangle in D_k" (960 / 3980 / 822).
Note: without a random tie-break the symmetric corners stay degenerate, so the top slice is simple only at k = 14 (where the §27 margin
0.348 vs 0.270 is reproduced); the identity of §35 needs the perturbed slice.
What does separate (partly): the RADIUS |X_i| = 1/(distance of face i of D_k). Dying faces are the faces NEAREST the centre at
k = 5–8 (|X| = max), and dying and surviving radii are fully separated at k = 11 (dying ≥ 0.9995 > 0.9824), 13 (≥ 0.9873 > 0.9869),
14 (≥ 0.9943 > 0.9921), but overlap at k = 9, 10, 12. The 12 five-fold faces die at every level 9–14 (foot point at the face centre).
Verdict (P1): no combinatorial rule; the radial order is the strongest single signal but not a rule. P1 joins P2/P3 as a tool, not a
proof. Next: (P3) orbit counting, or (P1') radial threshold per level against the census and generic sets.

## §37 Possibility 3: counting by symmetry classes (11 Nov 2026; DICTO: "run possibility 3"; scripts/og_orbits.py, data/og-orbits.json, FINAL ok)
Classes under I_h (120): size 12 / 20 / 30 (five-, three-, two-fold axes), 60 (on a mirror plane), 120 (generic). Every class dies or
survives whole (checked). k = 0 … 24:
- GENERIC classes (120): at most 1/3 die at any level (max 0.333 at k = 10; 0.25–0.27 from k = 19).
- MIRROR classes (60): up to 0.611 die (k = 23), 0.58 at k = 14: the faces on the 15 mirror planes are the vulnerable ones.
- Axis classes: the five-fold class dies at k = 9–14, 19, 20; at most 62 faces in all.
- Shares of the faces: mirror + axis faces fall from 0.62 (k = 14) to about 0.11 (k = 24); generic faces rise to about 0.89.
REDUCTION: c/n ≤ g·(1 − μ) + μ, with g = dying share of generic classes, μ = share of faces on mirror planes or axes. With g ≤ 1/3,
step A1 holds whenever μ < 1/4 — true from k = 19 on in the data (μ = 0.209, 0.170, 0.152, 0.102, 0.088, 0.114 for k = 19 … 24). So A1 for the tail ⇐ (G) generic classes: at most a third die, and
(M) mirror faces become a vanishing share (they lie along the 15 mirror great circles, a one-dimensional family, so about √n of n:
the 15 vertical sheets of the 4D Vacuus, §31a). (M) is geometric and looks provable; (G) is the remaining core, now only for generic
classes (where the generic-shape roundness law of §30 also gave ≤ 0.41).

## §38 Proving (M): mirror faces (11 Nov 2026; DICTO: "yes prove M"; scripts/og_mirror_bound.py, data/og-mirror-bound.json, FINAL ok)
LEMMA (exact). Let P be one of the 15 mirror planes. A face F of D_k with normal in P satisfies σF = F, so F ∩ P is an edge of the
section polygon D_k ∩ P, and F's cap of directions meets the great circle of P. Caps of distinct faces are disjoint. Hence the mirror
faces of P fill at most the band of half-width 2γ_M (γ_M = largest cap radius of a mirror face), and
   μ_k ≤ 15 · sin(2γ_M) · (mean solid angle of all faces / mean solid angle of mirror faces) + 62/n_k.
Edges of D_k ∩ P = the mirror faces of P plus the edges of D_k lying in P (the σ-pairs of faces meet P only there).
DATA k = 0 … 20: the bound holds at every level (control) but is far too weak: 14.9 … 1.28 against the needed 1/4 (actual μ 0.17 at
k = 20). Reasons: γ_M (largest mirror cap, 5.2° at k = 20) is about twice the mean cap (2.7°), and mirror faces are LARGER than average
(size ratio 0.47–0.8 from k = 18): the vulnerable faces of §37 are the big ones on the mirror circles.
REDUCTION: (M) ⇐ the mirror faces shrink: γ_M ≲ 0.5° (with size ratio ≈ 0.5–1) makes the bound < 1/4. Since the mirror faces of P are
the edges of the section polygon D_k ∩ P, this is a 2D question: do the edges of the 15 section polygons keep getting finer?
Next: track γ_M and the section polygon's edge count/lengths to k = 37 (certified checkpoints), and the 2D dynamics of D_k ∩ P.
**§38a Mirror growth to k = 27 (og_orbits.py, watched job og-orbits-30; stopped by memory at k = 28, exit 137, levels ≤ 27 in data/og-orbits-30.log).**
Mirror faces M (k = 20 … 27): 1320, 1680, 1560, 2160, 3840, 3000, 4500, 4740 against n = 7952 … 89 742; fit M ∝ n^0.56 (k = 20 … 27), M/√n
between 12.5 and 20.8: the √n law expected from 15 mirror circles holds in the data. μ (mirror + axis) = 0.053 at k = 27.
CORRECTION to §37: the generic death share g reaches 0.355 at k = 27 (0.283 at k = 26), so "g ≤ 1/3" is false; the reduction needs
μ < (1/2 − g)/(1 − g) (= 0.225 for g = 0.355), still true with a wide margin at k = 27 (μ = 0.053). (G) must be stated with a bound
below 1/2, not 1/3. Cut shares 0.259, 0.303, 0.365 at k = 25–27.

## §38b Mirror faces and death shares to k = 37 (11 Nov 2026; DICTO: "track the mirror faces to level 37", "why is the generic share rising"; scripts/mirror_track.py, data/og-mirror-37.{json,log}, watched job og-mirror-37, FINAL ok)
Float companion of certified_orbit.py (foot points pinned to their stabiliser after a first run stopped at D_34 on float drift). Face
counts agree with the certified run to within 240 faces at k = 32, 35 (near-degenerate merges; the certified counts stand).
(M): μ = 0.0332, 0.0279, 0.0240, 0.0189, 0.0179, 0.0155 (k = 32 … 37); mirror faces M/√n = 16–19 (√n law to k = 37). The §38 bound proves
μ < 1/4 by itself only at k = 37 (0.182): the largest mirror cap does NOT shrink steadily (1.18° at k = 33, 3.19° at 34, 2.03° at 37) and
the mean mirror cap stays ≈ 0.5° while the mean cap falls (0.45° → 0.21°): mirror faces are long thin faces across the mirror circles
(spacing along the circle ≈ 0.25°). So (M) holds by COUNT (~18√n), not by size; the right lemma counts edges of the section polygons.
(G) and the identity cut share = 1 − growth/2 − (4 + e)/(2F) (§19): growth ratios 1.42 (k ≈ 20) → 1.23 (dips at hops 27, 32) → 1.25,
1.39, 1.40, 1.37 (hops 33–36). Generic death share g = 0.37, 0.36 (hops 32, 33) then 0.293, 0.285, 0.304, 0.327 (hops 34–37); cut share
0.297, 0.292, 0.310, 0.331. The rise to 0.37 was two growth dips plus the vanishing excess term (gap 0.068 → 0.010 from hop 18 to 32:
degenerate corners disappear); g returns to ≈ 0.30 — the generic near-round equilibrium of §26 (≈ 0.30), not a drift to 1/2.
Equivalent form of A1 (from the identity): c < F/2 ⇔ F_{k+1} > F_k − 4 − e_k: step A1 says only that the face count does not shrink.

## §38c Section polygons to k = 37 and the 2D derivation (11 Nov 2026; DICTO: "count the section polygon edges", "derive the 2D bound for the section polygons"; scripts/section_track.py, data/og-section-37*, watched job og-section-37, FINAL ok)
COUNT: e(S_k) = edges of D_k ∩ P (one mirror plane) = mirror-face edges + edges of D_k in P (control exact at every level): 32 (k = 10),
126 (20), 652 (30), 1716 (37); e/√n between 1.12 and 1.53 for k = 10 … 37 (1.44 at k = 37). Median edge angle 6.8° → 0.15°, longest
3.6° at k = 37, shortest down to 1e−3°: the polygon refines on average, unevenly.
DERIVATION (exact): (1) an edge of D crossing P meets P in one point and σ maps it to an edge through the same point, so it is its own
mirror image [v, σv]; hence the vertices of S_k are the corners of D_k in P plus the symmetric edges: e(S_k) = c_P(D_k) + x_P(D_k).
(2) A foot point d·n lies in P iff n lies in P, so c_P(D_{k+1}) ≤ (mirror faces of D_k in P) ≤ e(S_k). Hence
   e(S_{k+1}) ≤ e(S_k) + x_P(D_{k+1}).
(3) Crofton: averaged over planes through O, the section edge count = (1/π)·Σ_F (mean angular width of F) ≤ (2/√π)·√(average aspect)·√n.
PILOT of the recursion (k = 10 … 16): corners in P ≤ mirror faces of the previous level at every hop (true); but x_P(D_{k+1}) is 0.27 –
1.09 × e(S_k), so the crude recursion allows doubling per hop: too weak against face growth ≈ 1.3. (M) needs a bound on the symmetric
edges x_P of the kind x_P(D_{k+1}) ≤ (λ − 1 − ε)·e(S_k) on average over a few hops, or a direct √n bound. Full ratios to k = 37 running.

**Remark (§38d, the mirror sections of the up and down families are polar polygons).** Let P be a mirror plane of I_h and σ its
reflection. (a) For a convex body K with σK = K, the orthogonal projection of K onto P equals the section K ∩ P: if (p, h) ∈ K then
(p, −h) = σ(p, h) ∈ K, so the midpoint (p, 0) ∈ K. (b) Projection–section duality: for a convex body K with the origin in its interior
and a linear subspace E, the polar within E of K ∩ E is the orthogonal projection of K° onto E. Applied to D_k (σ-symmetric) and
X_k = polar(D_k) (#43 Lemma 3): X_k ∩ P = proj_P(X_k) = (D_k ∩ P)°, the polar within P of the down section. A polygon and its polar
have equally many edges, so the mirror sections of the up and down families have the same edge count at every level (observed:
32 = 32, 44 = 44, …, 126 = 126 for k = 10 … 20, up_track.py). Not a new result: (a) is elementary, (b) is classical; only its use for
the OG family is ours. Consequence: the √n question for (M) is one 2D problem, not two.
Sources checked (11 Nov 2026):
- S. Arya, D. M. Mount, "Cauchy's Surface Area Formula in the Funk Geometry", arXiv:2601.16468v2 — Lemma 2.1 (Projection–Section
  Duality), stated exactly as (b): "(K ∩ E)°_E = K°|E" (opened, read).
- A. C. Thompson, Minkowski Geometry, Encyclopedia of Mathematics and its Applications 63, Cambridge University Press, 1996,
  Theorem 2.2.9 and Corollary 2.2.10 — the source Arya–Mount cite for the proof (their ref. [35]); not opened here.
- A. Jensen, "Self-polar polytopes", arXiv:1902.00784v1 (2019), Lemma 5.3: for a polytope P and a subspace H, (proj_H P)° = P° ∩ H
  (polar in H), with proof (opened, read).
- R. J. Gardner, Geometric Tomography (2nd ed., Cambridge University Press, 2006), Section 0.8, relation (0.38), used to convert
  projection results to central-section results "or vice versa" (from the publisher's chapter page via search; book not opened).
- Library check: neither ~/kaleidohedra-references nor ~/Documents/reference-library holds Gardner, Schneider or Thompson.
Queries: "polar body section projection duality Gardner Geometric Tomography"; "polar of a section equals projection of the polar
convex body subspace lemma".
**§38e Recursion ratios to k = 37 (section_track.py, og-section-37 second run, FINAL ok).** Hops 27–36: corners of D_{k+1} in P are
0.41–0.53 of the mirror faces of D_k (the mirror foot points that survive: 1 − mirror death share), symmetric edges 0.71–0.87 × e(S_k),
section growth e(S_{k+1})/e(S_k) = 1.04–1.26 (faces grow 1.23–1.41). Sharper recursion: e(S_{k+1}) = c_P + x_P with c_P ≤ (1 − mirror
death share)·m_P(D_k); the open term is still x_P (symmetric edges), steady near 0.8 × e(S_k).

## §38f The up family counted to k = 37 (11 Nov 2026; DICTO: "yes run the up family counts"; scripts/up_track.py, data/og-up-37.*, watched job og-up-37, FINAL ok)
Up shells X_k = polar(D_k): faces = corners of D_k. Up faces / down faces → 0.505 (k = 37; 0.51–0.73 earlier): D_k is almost all triangles,
so the up shells have about HALF as many faces. Up mirror share μ_up 0.047 (k = 24) → 0.0104 (k = 37), the same order as μ_down (0.0155).
Up section edges = down section edges at EVERY level 10 … 37 (Remark §38d: projection = section for mirror-symmetric bodies, plus
projection–section duality); e_up/√(up faces) = 1.8–2.15, i.e. e ≈ 1.44 √(down faces) ≈ 2.0 √(up faces), the same √n law on both sides.
Classes of up faces: mirror (60) classes grow 14 → 124, generic (120) classes 144 → 5893; axis classes occasional.

## §39 (G): the hop has an equilibrium cut share ≈ 0.32 (11 Nov 2026; DICTO: "yes go ahead with G"; scripts/g_equilibrium.py, data/og-g-equilibrium.*, watched job, FINAL ok)
Long runs of the hop on starts with NO symmetry, 16 hops each, up to 1.3 M faces: uniform random (U) and Fibonacci-spread (F) points on
the sphere, radial noise 0.1 % and 5 %, and the OG's level 18 with its symmetry broken by a 1e−7 nudge. The identity c = F − (F′ + 4)/2
(generic sets: no corner excess) holds exactly at every hop (control).
Cut share rises from 0.13–0.17 (hop 0) and SETTLES: hops 10–15 give 0.316–0.321 (U, 0.1 %), 0.306–0.321 (F, 0.1 %), 0.312–0.319 (U, 5 %),
0.317–0.326 (F, 5 %); growth settles at 1.35–1.37. The nudged OG wanders 0.31–0.36 (mean 0.336) and comes down to 0.313 at hop 15.
Late hops (k ≥ 4, F > 5000): mean 0.310, range 0.245–0.359, growth mean 1.380. Roundness keeps improving (R/r → 1.002–1.025).
Verdict: the cut share of the hop on fine near-round polytopes tends to an equilibrium near 0.32 (growth ≈ 1.36) whatever the start;
it does not creep toward 1/2. The OG's generic classes (§38b, g ≈ 0.29–0.33 at hops 34–37) sit at the same equilibrium. (G) is thus a
statement about ONE map: prove that the hop's cut share on fine near-round polytopes stays below 1/2 (observed ≈ 0.32, max 0.36).
