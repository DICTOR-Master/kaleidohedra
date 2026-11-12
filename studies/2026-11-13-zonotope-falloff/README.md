# Zonotope fall-off law (13 Nov 2026; lead 1 of studies/2026-11-13-amplitude-at-distance)

**Conclusion (13 Nov 2026): the law holds, but it is KNOWN. Far from a d-polytope P, Omega_P falls off like r^-(d+e), with 1 <= e <= d, and e = d (decay r^-2d) exactly for zonotopes. In 3D the only orders are r^-4, r^-5, r^-6, decided by the faces. All of this is in Baumbach, Freyer, Weigert and Winter (2025), where the "degree drop" of the adjoint is e - 1. The refined hypothesis in the brief is FALSE: central symmetry does not give r^-(d+2) in 3D (octahedron, icosahedron: r^-4), and 4D zonotopes fall off like r^-8, not r^-7. New here, as far as we checked: a Laplace-transform proof that gives every coefficient as c_k = ((-1)^k/k!) L[h_P^k], and an explicit, always nonzero formula for the zonotope's leading coefficient.**

## Setting
Omega_P(x) is the canonical rational function of a full-dimensional polytope P = {n_F.x <= b_F} in R^d. Inside P it equals
d! vol((P - x)°) (Arkani-Hamed, Bai and Lam). Outside P it is the same rational function, with poles on the facet planes. Along a
generic direction u, Omega_P(t u) = sum_{k>=1} c_k(u) t^-(d+k). The term c_0 vanishes for every P (complete-fan identity). Write
**e(P)** for the first k with c_k != 0; the fall-off is then r^-(d+e). In the language of Baumbach-Freyer-Weigert-Winter (BFWW),
e - 1 = drop(P), the degree drop of the adjoint, and c_{s+1} = their valuation Omega_s.

## Results

| statement | status | where |
|---|---|---|
| 1 <= e(P) <= d; e = d iff P is a zonotope (decay r^-2d) | KNOWN: BFWW Thm 3.5(3), Cor 3.8, Thm 4.5 | checked exactly: 15 zonotopes in 3D, 4D, 5D |
| centrally symmetric P: c_k = 0 whenever d + k is odd | KNOWN: BFWW Thm 3.5(7) (parity of the drop) | checked: 25 solids |
| 3D: e = 1 unless opposite facets match; e = 2 if they do but P is not a zonotope; e = 3 iff zonotope | KNOWN: BFWW Thm 6.4 (stated through P + (-P)) | checked: 28 solids, all as predicted |
| products: e(P x Q) = e(P) + e(Q) | KNOWN: BFWW Thm 3.5(1) | checked: 8 products |
| P = Q_1 + ... + Q_m: c_k = 0 for k < r, r = the least number of summands whose spans add up to R^d | a BFWW-type bound (their Thm 3.5(6) is a different inequality); proof below | checked: 3 sums |
| c_k = ((-1)^k / k!) L[h_P^k](-u) (Theorem 1 below) | NEW as far as checked | M5-M7, T3 |
| zonotope leading coefficient: c_d(u) = (-1)^d 2^d sum_S \|det G_S\|^(2d-1) / prod_{i in S} det(G_S, g_i -> u)^2 | NEW as far as checked | T3: exact at 45 directions |

The facet test in 3D: group each facet with its parallel opposite facet, if there is one. For a facet polygon F, let A_F be the sum of
its edge vectors on each line, going round F the same way as seen from one fixed side. A_F = 0 exactly when F is centrally symmetric.
Then **c_1 = 0 iff A_F = A_F' for every parallel pair and A_F = 0 for every facet without a partner**. This is the same as BFWW's
"F + (-F') centrally symmetric", because A_{F + (-F')} = A_F - A_F'. For example, the TRD and every prism over a polygon pass this
test, so they fall off like r^-5. The octahedron fails it: its opposite faces are F and -F, so A_{-F} = -A_F.

The brief's hypothesis, tested: "r^-(d+1) generically; r^-(d+2) when centrally symmetric; r^-(d+3) when every 2-face is". **Refuted
twice.** (i) In 3D, centrally symmetric non-zonotopes fall off like r^-4: octahedron, cuboctahedron, icosahedron, dodecahedron,
rhombicuboctahedron and a cube with its corners cut. Central symmetry kills c_k only when d + k is odd, which in 3D is c_2, not c_1.
(ii) 4D zonotopes (tesseract, a generic 5-zonotope, the A4 permutohedron) fall off like r^-8 = r^-2d, not r^-7.
The guess is right in one place: in 3D a zonotope gives r^-6 = r^-(d+3).

## Proofs (all d)
**Theorem 1 (every coefficient).** For x inside P, Omega_P(x) = INT_{R^d} exp(x.y - h_P(y)) dy, where h_P is the support function.
This is the classical identity INT e^{-h_K} = d! vol(K°) applied to K = P - x. Split R^d into the normal cones N_v; on N_v,
h_P = v.y. Each cone integral is a rational function (Brion; Lawrence), so Omega_P(x) = sum_v I_v(v - x) with
I_v(z) = INT_{N_v} e^{-z.y} dy as rational functions everywhere. Each I_v is homogeneous of degree -d. A Taylor expansion of
I_v(-t u + v) in v/t then gives c_k(u) = ((-1)^k/k!) L[h_P^k](-u), where L[f](z) := sum_v INT_{N_v} f e^{-z.y} dy (the cone integrals
of a piecewise polynomial f on a complete fan, rationally continued).
**Lemma (lineality).** If f is piecewise polynomial on a complete fan whose cones all contain a common line, then L[f] = 0.
The reason is that the exponential integral of a polyhedral cone containing a line is 0 as a rational function, and polynomial
weights are derivatives in z (Lawrence 1991; Khovanskii and Pukhlikov 1992; Barvinok's book). In particular L[1] = 0, which is c_0 = 0.
**Theorem 2 (zonotopes).** For Z = sum [-g_i, g_i], h_Z = sum |g_i.y|. Each monomial of h_Z^k uses at most k generators, and for
k < d these leave a line in every cone, so c_k = 0 for k < d. For k = d, only monomials with d independent generators survive. On
their 2^d orthants the integral factorises after the change of variables eta = G_S y, which gives the formula above. Every term is
positive at a generic u, so c_d != 0 and e = d exactly. Translating Z changes only coefficients after c_d.
**Proposition (Minkowski sums).** If P = Q_1 + ... + Q_m, each h_{Q_i} is a linear function plus a function of the projection onto
span(Q_i - Q_i). A monomial of (sum h_{Q_i})^k that uses fewer than r summands lives on a fan with a common lineality space, so the
Lemma gives c_k = 0 for k < r.
**Central symmetry.** h_P is even, so L[h_P^k] is even. It is also homogeneous of degree -(d+k), so it vanishes when d + k is odd.
**Residue mechanism (all d; the facet test).** The poles of c_1 lie only on the hyperplanes n_F.u = 0. Take facets F and F' with
n_F' = -n_F. Their two pole planes meet at infinity, on the residual flat where the adjoint vanishes (Warren; Kohn and Ranestad). So
the poles are simple, with residue c_1(F') - c_1(F) (the residue of Omega on a facet is Omega_F). A rational function with no poles
and negative degree is 0, so c_1 = 0 iff every pair has c_1(F) = c_1(F') and every facet without a partner has c_1(F) = 0. At the
next order, if c_1(P) = 0 then c_2 has a double pole on n_F.u = 0 with coefficient -(b_F + b_F') c_1(F), and b_F + b_F' is the
width, which is never 0. So c_2 = 0 forces c_1(F) = 0 on every facet. In 3D, c_1(polygon) = 0 iff the polygon is centrally
symmetric (the same argument one dimension down, where a segment has c_1 = -length != 0). A 3-polytope with all faces centrally
symmetric is a zonotope (Alexandrov; Bolker; McMullen). This gives the 3D trichotomy. BFWW prove the same statements by other means.
The local check T4 tests this mechanism at 171 facet lines: w c_1 -> 0 and w^2 c_2 -> 0 where predicted, and a true double pole
for the e = 2 solids.

## Data (exact; data/zono.log, data/zono.json)
| solid | d | e | decay | | solid | d | e | decay |
|---|---|---|---|---|---|---|---|---|
| cube, RD, TO, hexagonal prism, generic parallelepiped, generic 4- and 5-zonotopes, truncated cuboctahedron, RT, rhombic icosahedron | 3 | 3 | r^-6 | | tesseract, generic 5-zonotope, A4 permutohedron | 4 | 4 | r^-8 |
| TRD, triangular prism, irregular pentagonal prism, oblique triangular prism, triangle + generic zonotope | 3 | 2 | r^-5 | | triangle x square, TRD x segment, triangle + generic 4-zonotope | 4 | 3 | r^-7 |
| tetrahedron, octahedron, cuboctahedron, icosahedron, dodecahedron, truncated tetrahedron, cut-corner cube (truncated-cube type), rhombicuboctahedron, triangular frustum, square antiprism, tetrahedron + cube, corner-cut cube, random hull | 3 | 1 | r^-4 | | 16-cell, 24-cell, triangle x triangle, tetrahedron x segment, octahedron x segment | 4 | 2 | r^-6 |
| 5-cube, generic 6-zonotope | 5 | 5 | r^-10 | | 4-simplex | 4 | 1 | r^-5 |
| triangle x triangle x segment | 5 | 3 | r^-8 | | 5-simplex, 5-cross-polytope | 5 | 1 | r^-6 |

These agree with BFWW: the 16-cell and 5-cross-polytope have drops 1 and 0 (their Lemma 3.7), and the 24-cell has drop 1.

## Running
`scripts/zono_falloff.py` ran on the compute host through the job gate: pilot `zonofall-pilot` (13 solids, FINAL ok,
data/zono-pilot.log) and full run `zonofall` (45 solids, 12 workers, 20 GB cage, 20 checks, 0 failed, FINAL ok). Arithmetic is exact
over Q, and over Q(sqrt5) for the golden solids (field class of studies/2026-11-02-dicto-vacuus/scripts/qf.py, executed from its file).
A float hull (scipy) gives only the facet combinatorics; every facet plane is recomputed and verified exactly. Each solid uses three
generic rational directions. The pilot had two faults, both in the script and neither affecting a value: Qhull's triangulated
simplices were degenerate on non-simplicial facets (fixed by reading facets from the plane equations), and integer division in the
determinant gave floats (fixed with a Fraction guard plus an assertion that no float coordinate enters).
Controls: Omega_cube(0) = 64; the cube's product formula holds exactly; Omega_{PxQ} = Omega_P Omega_Q exactly at 14 random points
(an independent test of the triangulation in 4D and 5D); Omega(x0) = d! vol((P - x0)°) holds to 1e-9 against a float hull of the
polar at 41 solids; the series c_0..c_K agrees with exact Omega(10^6 u) to 1e-12. NEGATIVE: centrally symmetric non-zonotopes and
the frustum stay at r^-4, and the e = 2 solids have a true double pole of c_2.
"Exact" means exact at the three directions computed. The vanishing of c_k as a rational function is covered by the proofs (and by
BFWW), not by the sampling.

## Credits and what is known
Known and used: canonical forms of positive geometries (Arkani-Hamed, Bai and Lam 2017); Warren's adjoint (1996) and its vanishing
on the residual arrangement (Kohn and Ranestad 2020); Brion's theorem (1988); Lawrence's volume formula and rational-function
valuations (1991); Khovanskii and Pukhlikov (1992); Barvinok, Integer Points in Polyhedra (2008); INT e^{-h_K} = d! vol(K°) (classical);
zonotopes are exactly the polytopes with all 2-faces centrally symmetric (Bolker 1969; McMullen 1970/71; in 3D Alexandrov 1933).
**The main law is a theorem of T. Baumbach, A. Freyer, J. Weigert and M. Winter, "The canonical form, scissors congruence and
adjoint degrees of polytopes", arXiv:2508.04275 (2025):** the degree drop (= e - 1) is at most d - 1, with equality iff P is a
zonotope; the 3D classification (Thm 6.4); parity for centrally symmetric P; products; and the valuations Omega_s (= our c_{s+1}).
So the r^-6 "law" of the amplitude study is their Theorem 4.5 for d = 3. It is neither new nor a tiling law.
New here as far as checked: the Laplace-transform formula c_k = ((-1)^k/k!) L[h_P^k] with the lineality proof; the explicit,
positive leading coefficient of a zonotope; the Minkowski lineality bound in the form above; and the local residue check.

## Sources checked
studies/2026-11-13-amplitude-at-distance (README, amp_dist.py: TRD neighbours, decay census); 2026-11-13-near-but-never-on (job-gate
pattern); 2026-11-02-dicto-vacuus/scripts/qf.py. Reference library (search tool, 4 queries: canonical form decay, zonotope 2-face
characterisation, Laplace transform of support function, valuations on cones with lines). Hits read by title. The decisive hit was
the BFWW catalogue entry (no PDF in the library); its arXiv abstract and HTML text (sections 3-7) were read on the web. Other hits
(Adnan-Hasan zonohedra graphs, Taylor 1992, Khovanskii-Kiritchenko-Timorin 2026 polygon valuations) were not needed.
Concordance ledger: the 2026-11-13 amplitude entry.

## LEADS
1. Check BFWW Section 7 in full for an explicit top coefficient of Omega_{d-1}(Z). If it is absent, our zonotope formula is a short
   note-sized addition (tell them, credit theirs).
2. BFWW Question 3.3 (characterise polytopes of a given drop): the Minkowski lineality bound gives e >= r. When is it sharp?
3. 24-cell: e = 2, though all its facets are centrally symmetric octahedra. Is it the smallest regular example of BFWW's Remark 4.10
   (the drop is not a translation scissors invariant for d >= 4)?
4. Correct the amplitude-at-distance README and its ledger entry: "proof open (LEAD 1)" -> known, BFWW Thm 4.5.

DICTO · dictospheres.com
