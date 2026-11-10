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
