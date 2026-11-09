# The OG's margin by a gnomon (#43 Conjecture 1): study 2026-11-09

**Conclusion: the gnomon route does not close Conjecture 1, but it finds the exact mechanism behind the inradius recovery: the next
solid always reaches every face plane of the last one (Lemma G), so a face that survives a step never moves inward, the inradius can
fall only on new faces, and the reduction sharpens from the Inradius Lemma to a New-Face Lemma; no step or run of steps is a classical
gnomon, and r(D_j) is not monotone, so "r(D_12) plus monotonicity" is false.**
**Status: PARTIAL** (Lemma G, its corollaries, the gnomon criterion and the axis rhythm are proved exactly for every convex polytope /
every icosahedral one; the per-level facts are float to k = 28; Conjecture 1 stays REDUCED as in studies/2026-11-09-og-margin).

DICTO proposed a gnomon argument (9 November 2026): read the family by the shell between consecutive solids, as in #54 One Turn Is a
Gnomon.

Ledger: one entry touches Conjecture 1 (2026-11-09, og-margin, UNDECIDED, retry "only a proof of the Inradius Lemma, e.g. via the
max-plus convolution form of lemma A, or the shape limit r/R → 1"). This study is that retry along the max-plus / support-function
route, with the gnomon as the organising idea; it does not repeat the exact builds.

## 1. Setting

Notation of #43 and og-margin: D_0 = OG, D_k = P(D_{k−1}) (hull of the foot points h_i n_i of the face planes n_i·x = h_i);
h_k = support function of D_k, f_k(n) = h_k(n) at a face normal n of D_k; R, r, H = largest corner distance, smallest and largest face
distance; t_k = t_min(D_k) = max_u h_k(u)/h_{k+1}(u) (D_k ⊂ t_k D_{k+1}). Conjecture 1: t_k ≤ 3/φ² for every k.

Two shells sit between consecutive solids, and each has its own normalisation:
- the scaled shell c^{k+1}D_{k+1} \ c^k D_k. With c = φ it has non-negative thickness for every k (#43 Corollary 1, the OG turned out
  S_k = φ^k D_k). With c = 3/φ² non-negative thickness at every k is exactly Conjecture 1, and c = 3/φ² is the smallest constant that
  can work (equality at k = 3). So the natural gnomon normalisation is the conjecture itself;
- the unscaled shell between D_k and D_{k+1}, which has both signs (§3) and carries the mechanism.

## 2. Exact results (general)

**Lemma G (the next solid reaches every face plane).** For every convex polytope S with O inside and every face normal n_i of S,
h_{P(S)}(n_i) ≥ h_i, with equality exactly when P(S) lies in that face's half-space. Hence P(S) ⊂ S exactly when every foot point lies
in S.
Proof: the foot point h_i n_i is a point of P(S), and its projection on n_i is h_i. ∎

**Corollaries.**
(G1) *A surviving face never moves in.* If n is a face normal of both S and P(S), its distance in P(S) is ≥ its distance in S.
(G2) *Both shell ratios are ≥ 1.* s(S) := max_u h_{P(S)}/h_S ≥ 1 (take u = n_i), and t(S) ≥ R(S)/R(P(S)) ≥ 1 (the farthest corner v of
S needs t ≥ |v|/ρ_{P(S)}(v̂) ≥ R(S)/R(P(S)), and R(P(S)) = H(S) ≤ R(S), og-margin F1).
(G3) *Where the inradius can fall.* Let ν(P(S)) be the smallest distance of a face of P(S) whose normal is not a face normal of S
("new faces"). Then r(P(S)) ≥ min(r(S), ν(P(S))): a face of P(S) is either new, or survives and then lies at ≥ its old distance ≥ r(S).
By induction, r(D_j) ≥ min(r(D_K), ν(D_{K+1}), …, ν(D_j)) for all j > K.

**Gnomon criterion.** Put δ(S) = log(s(S)·t(S)) ≥ 0. It is scale-free: δ = 0 exactly when P(S) = c·S for some c > 0, i.e. when the step
from S to P(S) is a classical gnomon about O (Heron's definition, as in #54). By (G2), log t(S) ≤ δ(S). Hence
Conjecture 1 ⟸ δ(D_k) ≤ log(3/φ²) = 0.136189 for every k,
and this is sharp: at k = 3, s = 1 (D_4 ⊂ D_3) and δ(D_3) = log(3/φ²). Each step must stay within the conjecture's margin of being a
classical gnomon.

**Theorem N (the New-Face reduction).** Conjecture 1 holds for every k ≥ 11 provided r(D_12) ≥ 1.084154 and every new face of D_j,
j ≥ 13, lies at distance ≥ 1.084154 = (φ²/3)·R(D_11).
Proof: (G3) with K = 12 gives the Inradius Lemma of og-margin, and og-margin Theorem R finishes. ∎
This is the old reduction with the faces that cannot cause trouble removed: the surviving faces are already controlled exactly.

**The axis rhythm (icosahedral S, exact).** A 5-fold or 3-fold axis a meets the boundary of S in the interior of a face perpendicular to
a, or at a corner (a rotation of order ≥ 3 about a cannot map an edge through a to itself unless it fixes it, so the smallest face
containing the boundary point is a corner or a face whose plane is perpendicular to a). Corners of P(S) are foot points, and a foot
point on a comes only from a face with normal a. So, along the family:
(R1) a corner on a at D_k is preceded by a face on a at D_{k−1} (any axis), and followed by a face on a at D_{k+1} (5- and 3-fold axes);
(R2) if D_k has a face on a, then h_{k+1}(a) ≥ h_k(a) (Lemma G), with equality h_{k+1}(a) = f_k(a) when D_{k+1} has a corner there;
(R3) the support on a can fall only at a step that starts from a corner, and then by at most the Thales factor: the foot points of the
faces at a corner v lie on the sphere with diameter Ov, so h_{k+1}(a) ≥ |v| cos²β, β the smallest angle between a and a face normal
at v. At each 5-fold and 3-fold axis at most every other step can lose support.

## 3. What the gnomon route tested (float, k ≤ 28)

Scripts: gnomon_float.py (shell ratios s, t, δ, Lemma G, face orbits, polygon sizes, axis rhythm), gnomon_axes.py (surviving faces,
new-face minimum, the face carrying r, axis supports), gnomon_checks.py (the tests below). Double precision, symmetry re-imposed every
step as in og-margin; the counts and t_min reproduce og-margin to all printed digits.

**(1) Classical gnomon: none.** The face counts of D_0 … D_28 are all different (80, 132, 140, 162, 200, 252, 320, 402, 500, 732, 662,
672, 902, 1092, 1262, 1392, 2360, 2882, 3780, 5612, 7952, 11322, 15500, 25262, 33980, 47052, 66482, 89742, 110672; exact for k ≤ 11), so
no D_j is similar to any D_k: no step and no run of steps is a classical gnomon. This is the opposite of DICTO's golden cycle (#54
Theorem A), where one whole turn is one.

**(2) Unscaled shell: both signs; δ shrinks.** s_k ≥ 1 and t_k ≥ R_k/R_{k+1} ≥ 1 at every k (as G2 says). D_{k+1} ⊂ D_k (s = 1) only at
k = 0, 1, 3; from k = 9 on D_{k+1} crosses most of D_k's face planes (80 142 of 89 742 at k = 27). The gnomon defect δ_k:

| k | 0 | 3 | 8 | 9 | 10 | 13 | 16 | 20 | 24 | 27 |
|---|---|---|---|---|---|---|---|---|---|---|
| δ_k | 0.1254 | **0.1362** | 0.1293 | 0.0764 | 0.0195 | 0.0371 | 0.0163 | 0.0078 | 0.0039 | 0.0019 |

δ_k ≤ log(3/φ²) at every k ≤ 27, equality only at k = 3; max over k ≥ 10 is 0.0371, over k ≥ 20 it is 0.0078. The steps approach a
classical gnomon about O but never reach one (point 1).

**(3) Monotone inradius: false.** r(D_j) falls at 8 of the steps j ≥ 12; the largest fall is r(D_15) = 1.188927 → r(D_16) = 1.176986
(−1.0 %). So the hoped-for reduction "r(D_12) ≥ 1.084154 plus monotonicity" cannot be used. The oscillation log(R/r) of the log-support
also rises at 6 steps (2→3, 5→6, 8→9, 15→16, 20→21, 21→22): no one-step contraction of the max-plus form either.

**(4) The recovery is the gnomon mechanism.** From D_9 to D_15 the only surviving faces are the 12 faces on the 5-fold axes, and the
inradius of D_10 … D_14 sits exactly on them; by (G1) their distance cannot fall:

| j | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|
| 5-fold face distance | 1.155919 | 1.156886 | 1.165269 | 1.179355 | 1.182661 | 1.185352 | 1.189746 | corner |
| r(D_j) | 1.155919 | 1.156886 | 1.165269 | 1.179355 | 1.182661 | 1.185352 | 1.188927 | 1.176986 |

At D_15 a new face (60-orbit) undercuts the axis face; at D_16 the axis face has become a corner (R1, R2: h on the axis stays
1.189746) and r drops on a new face. From then on r is carried by new 60-orbit faces about 7–8° from a 3-fold axis, and it stays in
[1.176699, 1.180] for 16 ≤ j ≤ 28. Each lowest new face is spanned by foot points barely above the old inradius (their shortest is
1.00005–1.005 r(D_{j−1})) and has angular radius 0.9°–8.4° (j ≥ 16); the step-to-step change ν(D_{j+1})/r(D_j) lies between 0.98996
(j = 15) and 1.0024 (j = 16).

**(5) Self-similarity: none found.** Face counts grow by 1.23–1.63 per step without a period; the faces become almost all triangles
(107 360 of 110 672 at k = 28, plus 3300 quadrilaterals and the 12 axis pentagons); the 5-fold axis rhythm c f c f f f, c f c f f f
(k = 16–27) breaks at k = 28 (f), and the 3-fold rhythm has no period. Every rule R1, R2 held at every k.

## 4. Checks, with numbers

| check | result | script, log |
|---|---|---|
| Lemma G at every face normal, k ≤ 28 | min of h_{k+1}(n) − f_k(n) ≥ −5.8e−13 (float zero) | gnomon_float.py, data/gnomon-float.log |
| G1 on surviving faces | min gain ≥ +6.7e−6 at every k with surviving faces | gnomon_axes.py, data/gnomon-axes.log |
| G3: r_{k+1} = min(surviving min, new min) ≥ min(r_k, new min) | holds k ≤ 27 | gnomon_checks.py, data/gnomon-checks.log |
| s ≥ 1, t ≥ R_k/R_{k+1} ≥ 1, log t ≤ δ ≤ log(3/φ²) | all k ≤ 27; equality δ = log(3/φ²) only k = 3 | gnomon_checks.py |
| face orbits sum to the face count; t_k ≤ 3/φ² | all k ≤ 28 | gnomon_float.py |
| axis rules R1, R2 (5-, 3-, 2-fold) | every k ≤ 27 | gnomon_axes.py |
| face counts distinct | D_0 … D_28 | gnomon_checks.py |
| reproduces og-margin (t_min, counts, r, R, θ) | identical to printed digits | gnomon-float.log vs og-margin float-family.log |

Pilots: data/gnomon-pilot.log (k ≤ 16), data/axes-pilot.log (k ≤ 14). All runs on the large machine, foreground, each ≤ 6 min; every
script printed FINAL ok.

## 5. What would finish it

The open statement is now the **New-Face Lemma**: every new face of D_j (j ≥ 13) lies at distance ≥ 1.084154 (float: ≥ 1.176699, an
8.5 % margin), with r(D_12) ≥ 1.084154 (float 1.179355). A new face F of D_{j+1} is spanned by ≥ 3 foot points p = f_j(n) n and lies at
distance ≥ min|p|·cos γ_F (γ_F its angular radius about its normal). The float data show the mechanism that must be proved: the lowest
new face is spanned by foot points of faces that are themselves above the minimum, so the cos γ loss is not compounded. A proof needs a
bound that does not multiply over steps, e.g. a trapping region of icosahedral polytopes (r ≥ a, R ≤ b, plus a local condition on how
foot points sit in their faces) mapped into itself by P.

## 6. LEADS

1. **New-Face Lemma** (§5): look for a two-step inequality ν(D_{j+2}) ≥ min(r(D_j), …) using (R1)–(R3) at the 3-fold axes, where the
   late minimum lives.
2. **Exact recovery, cheap:** from the exact builds of og-margin read off the 5-fold face distances of D_9 … D_12 in Q(√5); this makes
   r(D_9) < r(D_10) < r(D_11) < r(D_12) exact and gives r(D_12) exactly, the base value in Theorem N.
3. **Shape limit as gnomon limit:** δ_k → 0 is the statement that the family becomes asymptotically a classical gnomon about O; any proof
   that δ_k ≤ 0.136 for k ≥ K gives Conjecture 1 for k ≥ K by the gnomon criterion.
4. **Note for #43:** Lemma G sharpens Proposition 1: D_{k+1} ⊂ D_k exactly when every foot point lies in D_k, and D_{k+1} is never
   strictly inside D_k. Destination: the Version-3 line of #43 together with og-margin. Where to place: DICTO's choice.

## 7. Concordance ledger line (ready)

```json
{"question": "#43 Conjecture 1 (OG margin) by a gnomon: shell between D_k and D_{k+1}", "method": "Lemma G (h_{P S}(n_i) >= h_i at every face normal); corollaries: surviving faces never move in, r(P S) >= min(r(S), new-face minimum), s,t >= 1 and gnomon criterion log t <= delta = log(s t); axis rhythm for icosahedral solids; float k <= 28 (gnomon_float.py, gnomon_axes.py)", "status": "UNDECIDED", "result": "PARTIAL: no step or run of steps is a classical gnomon (face counts D_0..D_28 distinct); r(D_j) NOT monotone (r_15 1.188927 > r_16 1.176986), so monotonicity cannot be used; recovery D_9..D_15 is carried by the 12 surviving 5-fold faces (exact mechanism, G1); reduction sharpened to the New-Face Lemma: new faces of D_j (j >= 13) at distance >= 1.084154 (float min 1.176699); delta_k <= log(3/phi^2) for k <= 27, equality only k = 3", "retry": "only a proof of the New-Face Lemma (e.g. a P-invariant trapping region or a two-step bound at the 3-fold axes); never retry monotonicity of r", "study": "studies/2026-11-09-og-gnomon", "date": "2026-11-09", "target": "#43 Conjecture 1 (the OG's margin)"}
```

DICTO · dictospheres.com
