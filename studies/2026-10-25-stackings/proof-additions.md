# Additions after the local 120b referee read (2026-10-25 23:20; report in referee-120b.md; my judgement below)
Accepted (write-up gaps, no error found):
1. Hand bound, arithmetic: for t = |q − p| ≥ 2.5d (d² = 2/3) and w_p − w_q ≥ −11/24 (weights in {0, λ}, λ ∈ [−11/24, 3/8]),
   distance of the radical plane = (t² + w_p − w_q)/(2t) ≥ (t² − 11/24)/(2t), increasing in t; at t = 2.5d: (25/6 − 11/24)/(5d) = (89/24)/(5d);
   squared: (7921/576)/(25·2/3) = 23763/28800 > 1/2. Holds for every λ in the range.
2. LEMMA (corners are affine in λ on a stretch): a corner is the common point of three radical planes 2(q_i − p)·x = |q_i|² − |p|² − w_{q_i} + w_p;
   the normals do not depend on λ and the right-hand sides are affine in λ; on a stretch the same three planes (linearly independent normals)
   define the corner, so the corner = M⁻¹·(affine in λ) is affine in λ.
3. STOPS: λ where the combinatorial type of some cell changes (a face appears/vanishes); finitely many per window because the type is
   constant on each open stretch and the engine finds each stretch's ends exactly (finite site list). Continuity: each cell is the
   solution set of finitely many inequalities whose offsets vary continuously, so cells vary continuously (Hausdorff) where non-empty;
   the census checks that the stretch limit equals the cell computed at the stop.
4. Convexity step explicit: by 1, every far radical plane misses the closed ball of radius √(1/2) about p for every λ; by (i) C_W lies in it.
5. The 24 maps are rigid motions used to exhibit congruence; they need not be symmetries of the weighted configuration.
6. Prior work to cite and distinguish (CHECK before citing): Conway & Sloane (Sphere Packings, Lattices and Groups) and Voronoi cells of
   sphere packings — cells of the BALLS, not of the holes; Cadotte et al. 2016 (c-OT2/h-OT2).
7. Paper apparatus: definitions of piece / upper and lower half, figure of one gap (X, Y, Z and the three sites), figure of halves, code links.
Rejected: "Fang and Chucky undefined" (defined with figures in the paper). Recommendation "major revision" = for the write-up; no
mathematical flaw identified.
