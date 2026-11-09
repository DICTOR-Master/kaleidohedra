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
