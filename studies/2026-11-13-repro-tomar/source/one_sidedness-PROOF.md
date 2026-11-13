# One-sidedness of the right-hand sides of the certificate: proofs

Notation: R = sqrt2. For unit vectors w1, w2, w3 in R^4 with Gram matrix G = [[1,u,v],[u,1,w],[v,w,1]]:

- S0 = vol{|x| < R, <x,w1> > 1}
- Pi0(u) = vol{|x| < R, <x,w1> > 1, <x,w2> > 1}
- Theta0(u,v,w) = vol{|x| < R, <x,wk> > 1 for k = 1,2,3}

These depend only on G. Write q = 4uvw - (u+v+w-1)^2 and det G = 1 + 2uvw - u^2 - v^2 - w^2. Piece II is
the set of points of A = {G PSD, u,v,w <= 1/2} with q >= 0.

The objective file objS_deg16.txt (certificate/data/) uses these right-hand sides:
- -S0r on 1-sets;
- p2+ on pairs with u in [0, 1/2], and 0 for u in [-1, 0];
- -p3+ on triples in piece II, and 0 on the rest of A.

The value V(23) is a valid lower bound up to the following one-sidedness errors:

1. S0r >= S0;
2. Pi0 = 0 on [-1, 0];
3. p2+ <= Pi0 + eps2 on [0, 1/2];
4. Theta0 = 0 on A \ piece II;
5. p3+ >= Theta0 - eps3 on piece II.

A configuration with N <= 23 has at most 253 pairs and 1771 triples, so
T3* >= V(23) - 253 eps2 - 1771 eps3.

Items 2 and 4 are proved below. Items 1, 3 and 5 are machine-verified: exact rationals for every polynomial
quantity, and Arb ball arithmetic (python-flint 0.9.0) for every transcendental one.

## Lemma P (pairs and S0)

(a) Pi0(u) = 0 for u <= 0, and Theta0 = 0 for every triple with an entry <= 0.

(b) For 0 <= u < 1, Pi0(u) = (pi/2)[pi - 8/3 - 2 arccos u + 3t - t^3/3] with t = sqrt((1-u)/(1+u)).
Moreover Pi0'(u) = pi u^2 / ((1+u)^2 sqrt(1-u^2)).

(c) S0 = pi^2/2 - 4pi/3.

*Proof.*

(a) If u = -1 then w2 = -w1 and K2 = {<p,w1> >= 1, <p,w2> >= 1} is empty. If -1 < u <= 0, the closed convex
set K2 has point of least norm (w1 + w2)/(1+u): both KKT multipliers equal 1/(1+u) > 0, and the squared norm is
2/(1+u) >= 2. So K2 misses the open ball |x| < R. The same holds for any pair of the three caps, so a triple with
an entry <= 0 has Theta0 = 0, since the triple region lies inside that pair's region.

(b) Write x = p + y with p in the plane P = span(w1, w2) and y orthogonal to P. Then
Pi0 = int_D pi (R^2 - |p|^2) dp, where D = {p in P : |p| < R, <p,w1> > 1, <p,w2> > 1}.
Use polar coordinates (rho, phi) in P, with w1 at angle 0 and w2 at angle g = arccos u. The region is
symmetric about phi = g/2, and for phi in [g/2, pi/4] the lower limit is rho = sec(phi); the upper limit pi/4 is
where sec(phi) = R. Hence

  Pi0 = 2 (pi/4) int_{g/2}^{pi/4} (2 - sec^2 phi)^2 dphi = (pi/2)[F(pi/4) - F(g/2)],

with F(x) = 4x - 3 tan x + tan^3 x / 3. Finally F(pi/4) = pi - 8/3 and tan(g/2) = t; this uses g/2 <= pi/4,
i.e. u >= 0.

Differentiating, with dt/du = -1/((1+u) sqrt(1-u^2)) and 3 - t^2 = (2+4u)/(1+u), gives Pi0'.

(c) S0 = int_1^R (4pi/3)(R^2 - h^2)^{3/2} dh = pi^2/2 - 4pi/3.

Checks: (b) agrees with a separate numerical quadrature of Pi0 to 3e-16, and the formula for Pi0' agrees with finite differences.

## Lemma 0 (where Theta0 vanishes)

Let (u,v,w) be in [-1, 1/2]^3 with G positive semidefinite (G is the Gram matrix of three unit vectors; det G = 0
is allowed). Then:

(i) If det G > 0: Theta0 > 0 if and only if q > 0.

(ii) q >= 0 implies (u,v,w) is in [0, 1/2]^3, and det G >= 1/4 on [0, 1/2]^3. In particular piece II lies in
[0, 1/2]^3 and contains no degenerate (det G = 0) triple.

(iii) If det G = 0, then some entry is negative, Theta0 = 0 and q < 0.

(iv) Consequently Theta0 = 0 on all of A \ piece II, degenerate triples included, and on the boundary q = 0 of
piece II. On the rest of the boundary of piece II, det G >= 1/4: the faces u, v or w = 1/2 (where q > 0) lie in the
domain (0, 1/2]^3 of Lemma 1, and the only points of piece II with a zero entry are the permutations of (1/2, 1/2, 0),
where q = 0, det G = 1/2 and Theta0 = 0 (by (i)).

*Proof.*

(i) Work in E = span(w_k). Let K = {p in E : <p,w_k> >= 1 for all k}. Then Theta0 > 0 if and only if
dist(0, K) < R: if a point of K lies at distance less than R, it is a limit of interior points of K x E^perp
inside the ball, which has positive volume, and otherwise the region is empty.

The minimiser of |p| over K is unique. It is one of the following.
- The vertex p0. Here |p0|^2 = 1^T G^{-1} 1, and 2 det G - (3 - sum u^2 + 2 sum uv - 2 sum u) = q.
  So |p0|^2 < 2 if and only if q > 0.
- A point (w_i + w_j)/(1 + u_ij) on an edge. It lies in K only if u_ik + u_jk >= 1 + u_ij. When u_ij >= 0 this is
  impossible, because both left terms are at most 1/2 (the one exception is equality at u_ij = 0 with
  u_ik = u_jk = 1/2, and there the squared norm is exactly 2, not less); when u_ij < 0 the squared norm
  2/(1 + u_ij) exceeds 2.
- The point w_k on a facet. It lies in K only if u_ik, u_jk >= 1, which is impossible.

So dist(0,K) < R forces the minimiser to be p0 with q > 0. Conversely, q > 0 gives p0 in K with |p0| < R.

(ii) If one or three of the entries are negative and none is 0, then uvw < 0, so q < 0.

If exactly two are negative, say u = -a and v = -b with a, b > 0 and w <= 1/2, then
(u+v+w-1)^2 = (1 + a + b - w)^2 >= (a+b)^2 >= 4ab > 4abw = 4uvw,
so q < 0.

If one entry is 0, then q = -(sum - 1)^2 <= 0, with equality only at permutations of (1/2, 1/2, 0).

On [0, 1/2]^3 we have 2uvw >= 0 and u^2 + v^2 + w^2 <= 3/4, so det G >= 1/4.

(iii) Suppose det G = 0, so w1, w2, w3 are linearly dependent. If they span a line, two of them are equal or
opposite; equal vectors have inner product 1 > 1/2, which is excluded, so some inner product is -1. Otherwise they
lie in a 2-plane. No two coincide (inner product 1 is excluded), so their directions cut the unit circle into three
arcs a, b, c > 0 with a + b + c = 2pi. The two vectors bounding an arc of length a have inner product cos a.
If all three inner products were >= 0, every arc would lie in (0, pi/2] or in [3pi/2, 2pi), and at most one arc
can be >= 3pi/2. If none is, a + b + c <= 3pi/2 < 2pi; if one is, say a, then b + c <= pi/2, but cos b,
cos c <= 1/2 force b, c >= pi/3, so b + c >= 2pi/3. Either way this is a contradiction, so some inner product is
negative.

In both cases Lemma P(a) gives Theta0 = 0, and (ii) gives q < 0 (an entry is negative).

(iv) Points of A \ piece II have q < 0, and Theta0 = 0 there by (i) when det G > 0 and by (iii) when det G = 0.
On the boundary q = 0 of piece II, det G >= 1/4 by (ii), so Theta0 = 0 by (i). The rest of (iv) follows from (ii),
its proof and direct substitution.

## Lemma 1 (gradient of Theta0)

On (0, 1/2]^3,

  dTheta0/du = (8/3) u^2 (1+u)^{-2} (1-u^2)^{-1/2} Q(phi),

where Q(phi) = int_0^phi sin^4 s ds = 3phi/8 - sin(2phi)/4 + sin(4phi)/32. The angle phi in [0, pi/2] is given by
sin^2 phi = z := q(1+u)/(2u det G) when q > 0, and by phi = 0 when q <= 0.

The partial derivatives in v and w follow by symmetry. Theta0 is C^1 on (0, 1/2]^3 and nondecreasing in each
variable.

*Proof.*

Fix w2 and w3. Let n be the unit vector in E orthogonal to w1 and w3 with <n,w2> > 0 (it exists since det G > 0),
and set w1(s) = cos(s) w1 + sin(s) n. Then <w1(s), w3> = v cos s, whose derivative vanishes at s = 0, and
<w1(s), w2> has derivative <n,w2> at s = 0.

Let K' = {|x| < R, <x,w2> > 1, <x,w3> > 1} and F(s) = vol(K' ∩ {<x, w1(s)> > 1}).

By the coarea (Reynolds transport) formula, the hyperplane H1(s) moves with normal speed <x, n> at s = 0, and
the boundary of K' meets H1 in a sigma-null set. So F'(0) = int_{F1} <x,n> dsigma, where F1 = K' ∩ H1 is
the 3-dimensional face. These directional derivatives are continuous in the configuration, so Theta0 is C^1 in
(w1, w2, w3). The Gram map is a submersion at independent triples, so Theta0 is C^1 in (u,v,w), and
F'(0) = <n,w2> dTheta0/du.

To compute the integral over the face, write x = w1 + p + t e, where p lies in P = E ∩ w1^perp (a 2-plane) and e
is orthogonal to E. The face becomes the region Omega = {|p| < 1, <p, nu2> > c2, <p, nu3> > c3} in P, with weight
2 sqrt(1 - |p|^2). Here nu_j is the unit vector along the P-component of w_j, c2 = sqrt((1-u)/(1+u)),
c3 = sqrt((1-v)/(1+v)), and <nu2, nu3> = gamma = (w - uv)/sqrt((1-u^2)(1-v^2)). The function
Psi(r) = -(2/3)(1 - r^2)^{3/2} is C^1 on the closed unit disc, zero on the circle, and satisfies
grad Psi(|p|) = 2p sqrt(1 - |p|^2), so the divergence theorem gives

  int_Omega p 2 sqrt(1-|p|^2) dp = sum_j nu_j (2/3) int_{chord_j} (1 - |p|^2)^{3/2} ds,

where chord_j is the part of the line <p,nu_j> = c_j that bounds Omega. Moreover, n is orthogonal to nu3, and
<n, nu2> = <n,w2>/sqrt(1-u^2), because w2 = u w1 + sqrt(1-u^2) nu2.

Hence dTheta0/du = (2/3)(1-u^2)^{-1/2} int_{chord_2} (1 - |p|^2)^{3/2} ds. The integrand is >= 0, which gives
monotonicity.

Parametrise chord_2 by arclength t from its foot point, so 1 - |p|^2 = T^2 - t^2 with T^2 = 2u/(1+u). Constraint 3
cuts the chord at t >= t3 = (c3 - c2 gamma)/sqrt(1 - gamma^2). The two identities
c3 - c2 gamma = (1+u-v-w)/((1+u) sqrt(1-v^2)) and 1 - gamma^2 = det G/((1-u^2)(1-v^2)) give t3 in closed form:
t3 = (1+u-v-w) sqrt((1-u)/(1+u))/sqrt(det G), and t3 >= 0 on [0, 1/2]^3. Then
int_{min(t3,T)}^T (T^2 - t^2)^{3/2} dt = T^4 Q(phi), with cos phi = min(t3/T, 1), and
1 - t3^2/T^2 = [2u det G - (1+u-v-w)^2 (1-u)]/(2u det G) = (1+u) q/(2u det G), by the polynomial identity
2u det G - (1+u-v-w)^2 (1-u) = (1+u) q (checked with sympy: expand(difference) = 0).

Finally (2/3)(1-u^2)^{-1/2} T^4 = (8/3) u^2 (1+u)^{-2} (1-u^2)^{-1/2}.

Checks:
- The formula agrees with central differences of the independent exact evaluator t3exact.py
  (divergence theorem in E) to about 1e-12 at random points.
- At (1/2,1/2,1/2) it gives 0.0510221751.

## Lemma 2 (one-dimensional formula)

For (u,v,w) in piece II with v, w < 1/2, let u0 and u0p be (sqrt((1-v)(1-w)) ∓ sqrt(vw))^2. Then
q = (u - u0)(u0p - u), u0 <= u <= u0p, and

  Theta0(u,v,w) = int_{u0}^{u} dTheta0/du(s, v, w) ds.

*Proof.* The factorisation of q is a direct expansion, and q >= 0 on piece II gives u0 <= u <= u0p. By Lemma 0 (iv)
the only points of piece II with a zero entry are the permutations of (1/2, 1/2, 0), so v, w < 1/2 gives v, w > 0.
Also u0 > 0, since (1-v)(1-w) - vw = 1 - v - w > 0. As u <= 1/2, the segment (s, v, w), s in [u0, u], lies in
(0, 1/2]^3. Its endpoint (u0, v, w) is in A (2uvw >= 0 and u^2 + v^2 + w^2 <= 3/4 give det G >= 1/4, so G is
positive definite) and has q = 0, so Theta0(u0, v, w) = 0 by Lemma 0 (iv). Lemma 1 and the fundamental theorem
of calculus give the formula.

*Evaluation.* Substitute s = u0 + D tau^2 with D = u - u0. Along the segment,
z(s) = tau^2 K with K = D (u0p - s)(1+s)/(2 s det G(s)), and K > 0 when D > 0 (u0p > 1/2 >= s). Hence
sin phi = tau sqrt(K), and the integrand 2 D tau (8/3) s^2 (1+s)^{-2} (1-s^2)^{-1/2} Q(asin(tau sqrt K)) is
analytic on a neighbourhood of tau in [0, 1]. The substitution removes the square-root branch point at s = u0.

The integral is enclosed with Arb's acb.integral (acb_calc_integrate, Petras' algorithm; Johansson,
"Numerical integration in arbitrary-precision ball arithmetic", 2018). The error bound is rigorous provided the
integrand returns a non-finite ball whenever holomorphy on the input ball is not certain. Our integrand meets this
condition:
- the two square roots use sqrt(analytic=True);
- asin is evaluated only on balls with |y| < 1 (it is holomorphic on the unit disc), and otherwise the integrand
  returns NaN;
- poles of the divisions yield non-finite balls automatically.

The constants u0, u0p, D are Arb balls; ball arithmetic is inclusion-monotone, so the result contains the
integral at the true constants.

Check: agreement with t3exact.py to 2e-17 at 40 random points of piece II.

## Verification of items 3 and 5

**Item 3** (rig/verify_p2.py). Subdivide [0, 1/2] into intervals I = [c - r, c + r] (dyadic). Let t_k be the
exact Taylor coefficients of p2+ at c (exact rational shift). By the mean value theorem for Pi0,

  Pi0(c+h) - p2+(c+h) >= [Pi0(c) - t_0] - r max_{y in Pi0'(I)} |y - t_1| - sum_{k>=2} |t_k| r^k.

Pi0(c) uses the Lemma P closed form and Pi0'(I) its derivative formula, both in Arb. eps2 = max(0, -min_I LB).

**Item 5** (rig/verify_p3.py). Symmetry reduces the check to the sorted part u >= v >= w. p3+ was checked to be
exactly S3-symmetric by composing with transpositions. Take dyadic cubes B (centre c, half-side r) of an adaptive
octree of [0, 1/2]^3.

A cube is discarded only in two cases, both exact tests:
- it misses {u >= v >= w};
- q < 0 on all of B, i.e. the exact Taylor shift satisfies q(c) + sum_{a != 0} |q_a| r^|a| < 0.

Otherwise, let s_a be the exact Taylor coefficients of p3+ at c, from fmpq_mpoly composition. Let g_i(B) be
enclosures of dTheta0/dx_i over B: dTheta0/da = C(a) Qz(z) with C(a) = (8/3)a^2(1+a)^-2(1-a^2)^-1/2 and
Qz(z) = Q(asin sqrt z). Both factors are >= 0 and increasing, and z is clamped to [0,1] (z <= 0 exactly where
q <= 0, where the derivative is 0, and z <= 1 always), so the range is [C(a_lo) Qz(z_lo), C(a_hi) Qz(z_hi)] for
any enclosure [z_lo, z_hi] of z over B. The enclosure of z used is the intersection of the natural interval
extension of z and the centred (mean-value) form of z.

By the mean value theorem for Theta0 (C^1, Lemma 1):

  p3+(c+h) - Theta0(c+h) >= s_0 - Theta0(c)^up - sum_i r max_{y in g_i(B)} |s_i - y| - sum_{|a|>=2} |s_a| r^|a| =: LB(B).

Here Theta0(c)^up is the upper end of the Lemma 2 enclosure, or 0 if q(c) <= 0 (Lemma 0). A cube is certified
if LB(B) >= -EPS; otherwise it is split into 8. The proved eps3 is max(0, -min LB) over all certified cubes,
which cover the sorted piece II; every cube is logged.

## Results

| item | result | how it was checked | log |
|---|---|---|---|
| 1 | S0r - S0 = 2.70e-15 > 0 | Arb, S0 = pi^2/2 - 4pi/3 | verify_p2_level18.log |
| 2 | Pi0 = 0 on [-1, 0] | Lemma P(a) | — |
| 3 | **eps2 = 2.8111e-12** (proved value 2.8110732894564e-12, rounded up) | 2^18 intervals, 7 s | verify_p2_level18.log |
| 4 | Theta0 = 0 on A \ piece II (degenerate triples included) | Lemma 0 (iii), (iv); Lemma P(a) | — |
| 5 | **eps3 = 1.0e-6** (every certified cube satisfies LB >= -1e-6 in Arb; min LB = -9.999965e-7) | see below | p3run_eps1e-6.log, p3run_eps1e-6_summary.json, p3run_eps1e-6_ok.txt.gz |

Item 5 in detail:
- 1,762,248 certified cubes from octree levels 6-9. There were no failures and the cover is complete; 27,136
  cubes lie outside q >= 0 and 298,885 outside the sorted region.
- The run took 518 s on 40 cores. Each cube's line in the log is "nu nv nw level LB": centre
  (2n+1)/2^(level+2), half-side 1/2^(level+2).
- As a sanity check, 1,500 random rational points of the sorted piece II give 8.8e-11 <= p3+ - Theta0 <= 8.1e-9.
  So p3+ >= Theta0 probably holds exactly; the proof only claims -1e-6.

**Rigorous bound:** with the certificate value V(23) = 2 pi^2 - KFIX = 8.0387480021787, eps2 = 2.8111e-12 and eps3 = 1.0e-6:
8.0387480021787 - 253 x 2.8111e-12 - 1771 x 1.0e-6 = 8.0387480021787 - 7.112083e-10 - 0.001771
= **8.0369770014674917** (exact decimal arithmetic). V(23) itself is checked by the certificate checker
(certificate/), not here.

Cost of a smaller eps3: each extra octree level divides the worst bound by about 4 and multiplies the cube count by
about 8. eps3 = 2.5e-7 would need about 13M more cubes.
