# Switch theorem for the web of bonds (2026-11-08)

**Conclusion.** Every flip of a two-kind weight walk sits at the one root λ* = S₀/S_A of an affine lifted determinant (Theorem A), and at a switch point each dual cell is cut by the hull of its A sites on one side and of its B sites on the other (Theorem B). This proves #53 Observation 1 for the four networks of #53 and gives its general form. The quadrilateral wording of Observation 1's open problem is **false** in general: the h-BN honeycomb and Si/Al sodalite are counterexamples. Theorem C proves Observation 4.

**Status: PROVED** (Theorems A, B, C, each with an exact computer check on all ten networks of #53 and two control networks). **DISPROVED**: the quadrilateral version of #53 Observation 1's open problem. **PARTIAL**: Observation 3 (a criterion is given, but no rule that reads the type off the sites). **OPEN**: Observation 2.

DICTO proposed the two DICTONIC loops, the web of bonds and the question of whether the switch points share a common reason (#53 §6, Concordance gap "a common reason for the switch points"). The lifted-determinant reading follows Edelsbrunner and Shah [ES]. Computation, proofs and drafting were done with Claude (Anthropic).

## Set-up (as in #52 and #53)

The sites p_i are periodic, of two kinds A and B, with weights w_A = λ and w_B = 0. The power cell of p_i is {x : |x − p_i|² − w_i ≤ |x − p_j|² − w_j for all j}. Two sites are **bonded** when their cells share a facet. The bonds are the edges of the dual regular (weighted Delaunay) subdivision S(λ): lift each p_i to (p_i, |p_i|² − w_i) and take the lower hull [Au87, #53 §2]. This is #53's own model, so the brief's hypothesis that "bonds = edges of the regular subdivision" holds by definition. One correction: S(λ) is in general **not a triangulation**. Non-simplicial cells, such as the octahedra and cubes of fluorite, persist on whole intervals. So the right setting is regular *subdivisions* and the walls of the secondary fan [GKZ, DRS]. Edelsbrunner–Shah's general-position triangulations are not the right setting.

A **flip** is an interior λ at which S(λ) changes (#53 Main theorem (ii)). A **switch point** is a λ in the range at which every bond is unlike (#53 §2).

## Theorem A (the flip formula)

Let Z = {p_0, …, p_{d+1}} be d+2 sites with d+1 of them affinely independent, and let α be their affine dependence (Σα_i p_i = 0, Σα_i = 0, unique up to scale). Put

  S₀ = Σ α_i |p_i|²,  S_A = Σ_{p_i ∈ A} α_i.

Then the lifted orientation determinant is det[p_i, |p_i|² − w_i, 1] = c·(S₀ − λ S_A) with c ≠ 0. So Z is co-power-spherical at λ = S₀/S_A only (if S_A ≠ 0), never (if S_A = 0 ≠ S₀), or always (if S_A = S₀ = 0).

**The flips are exactly** the values λ* = S₀/S_A, inside the open range, of the sets Z with S_A ≠ 0 whose power sphere at λ* is empty (no site has smaller power at its centre). In particular every flip is rational for rational sites in a rational metric.

*Proof.* Expand the determinant along the lift column. The cofactors are ±(d+1)-point determinants, proportional to α_i (Cramer). Since w_i = λ·[p_i ∈ A], the result is affine in λ. This is the lifted test of [ES]. Linearity in the weight is also used for kinetic flip times in [MS].

(⇒) At a flip λ*, some cell C of S(λ*) does not survive to nearby λ. If the lifted heights of C's sites stayed affine for all λ, C would remain a lower face as long as no other site reached its sphere. A site that reaches the sphere at λ* is already in C. So the heights are affine at λ* only. Then some d+1 independent sites of C and one further site of C form a Z with D ≢ 0 and D(λ*) = 0, and its sphere at λ* is C's sphere, which is empty.

(⇐) If such a Z exists, conv Z lies in a cell of S(λ*). For λ ≠ λ* nearby, the points of Z are not co-power-spherical, so that cell is split. Both sides refine S(λ*) by the opposite height functions ±χ_A (Theorem B, step 1), and a nontrivial subdivision differs from its opposite: if ψ and −ψ were both convex, ψ would be affine. So the two sides differ. ∎

## Theorem B (inside a cell at a flip; the switch theorem)

Let λ* be a flip and C a cell of S(λ*) whose sites are its vertices. Write A_C and B_C for its sites of each kind.

1. For all small ε > 0, S(λ*+ε) restricted to C is the regular subdivision of C with heights 0 on A_C and 1 on B_C, and S(λ*−ε) restricted to C uses heights 1 on A_C and 0 on B_C.
2. If every edge of C is unlike (C is bipartite), then above λ* the cell C is cut into conv(A_C) and the pyramids conv(b ∪ F), for b ∈ B_C and F a facet of conv(A_C). Below λ*, swap A and B. The only new bonds in C are therefore the edges of conv(A_C) above (all A–A) and the edges of conv(B_C) below (all B–B). The unlike bonds are the edges of C on both sides.
3. **Switch theorem.** At a switch point λ*, every cell of S(λ*) is bipartite and none is a simplex (#53 Corollary 2). So just above λ* the like bonds are exactly ⋃_C edges(conv A_C), all A–A, with no B–B bond. Just below λ* they are exactly ⋃_C edges(conv B_C), with no A–A bond. Each bipartite cell has at least d sites of each kind, so both sets are nonempty. Hence **a switch point is always a single switch**: one like bond is born exactly where the other dies. Conversely, a λ* where one like-bond life ends and the other begins, with neither alive at λ*, is a switch point by definition.

*Proof.*

Step 1: on C the lift |p|² − w(λ*) is affine. For λ = λ*+ε the lift adds −εχ_A = εχ_B − ε. Up to an affine function this is ε·χ_B. For ε below the smallest positive gap among the finitely many cell configurations mod translation, S(λ*+ε) refines S(λ*) by these heights cell by cell. This is the standard refinement lemma for regular subdivisions [DRS §2.3; GKZ ch. 7].

Step 2: let Q be a cell above λ* with affine lower function ℓ (ℓ ≤ h on all sites, with equality on Q's sites). Suppose b ∈ B_C is a site of Q, and y is another site of Q adjacent to b in Q. Since y ∈ C and the cone of C at b is spanned by C's edges at b, which all end at sites a ∈ A_C, we can write y = b + Σ μ_a (a − b) with μ ≥ 0. Then ℓ(y) = 1 + Σ μ_a (ℓ(a) − 1) ≤ 1 − Σ μ_a, because ℓ(a) ≤ h(a) = 0.
- If y ∈ B, then h(y) = 1 forces Σμ = 0, so y = b, a contradiction. So no cell holds two B sites.
- If y ∈ A, then 0 = ℓ(y) forces Σμ ≤ 1. Then y is a convex combination of b and C's vertices, and y is itself a vertex of C. So Σμ = 1 and y is one of the a: [b, y] is an edge of C.

Every lifted A site is at height 0, so conv(A_C) is a lower face. Each remaining cell has exactly one B site b, and its A sites lie on {ℓ = 0}, a facet F of conv(A_C). So the cell is conv(b ∪ F). Below λ* the same argument holds with A and B swapped.

Step 3: at a switch point every edge is unlike. A simplex with three or more vertices of two kinds always has a like edge, so no cell is a simplex. Apply step 2 to every cell. ∎

The structure in step 2 is the classical *pushing* of vertices [DRS §4.3; LW]. Pushing a vertex b replaces C by conv(C ∖ b) and the cones from b over the faces it sees. Because B_C is an independent set in C's graph, pushing all of B_C at once gives conv(A_C) plus the pyramids. We found no statement of the bipartite case, or of its consequence for the like bonds, in the sources listed below.

### What it says about #53 Observation 1

At the four switch points of #53 the dual cells are squares, rhombi, cubes and rhombic dodecahedra. Every edge of conv(A_C) or conv(B_C) is a diagonal of a quadrilateral face:
- square + centres: the segment of the two like corners;
- honeycomb + centres: the same, in each rhombus;
- rock salt: the tetrahedron of 4 Na or 4 Cl in each cube, whose edges are the cube's face diagonals;
- fluorite: the octahedron of 6 oct sites, whose 12 edges are the long diagonals of the 12 rhombi, and the cube of 8 tet sites, whose 12 edges are the short diagonals.

So Observation 1 is a corollary of Theorem B for these four networks.

**The open problem's quadrilateral version is false.**
- **h-BN** (the honeycomb with its two sublattices as the kinds). λ* = 0 is a switch point. The dual cells are hexagons B N B N B N, and the like bonds born there are the triangles of alternate vertices, whose edges are the short diagonals of the hexagons (squared length 3, 6 per site). There are no quadrilaterals.
- **Sodalite** (the vertices of the bitruncated cubic honeycomb, with the Si/Al order that obeys Loewenstein's rule). λ* = 0 is a switch point, and the dual cells are truncated octahedra. Per site, the like bonds are 2 square diagonals (squared length 4) and 8 hexagon short diagonals (squared length 6).

The correct general statement is Theorem B(3): **the switch trades, in every dual cell, the edges of the hull of one kind for the edges of the hull of the other.**

## Theorem C (the ends of the range; #53 Observation 4)

For an A site a, let V(a) be its Voronoi cell among the A sites, and let f_a(x) = max over B sites b of (|x − a|² − |x − b|²), a convex piecewise-affine function.
1. The A cell of a is nonempty exactly for λ ≥ m_a = min over V(a) of f_a, and it has positive volume exactly for λ > m_a.
2. f_a(a) = −d_a², with d_a the nearest unlike distance. So m_a ≤ −d_a², with equality **iff a lies in the convex hull of its nearest unlike neighbours**. At λ = m_a the cell is the set of minimisers.
3. The range is (max_a m_a, −max_b m_b), where m_b is defined in the same way for B with the kinds exchanged.

*Proof.* x is in the cell of a iff x ∈ V(a) and |x − a|² − λ ≤ |x − b|² for every b, that is, iff f_a(x) ≤ λ. a is interior to V(a), and ∂f_a(a) = conv{2(b − a) : b nearest}, so a is a minimiser iff 0 ∈ ∂f_a(a). ∎

For the hcp holes, each tet site has only 3 nearest oct sites. Its hull is a triangle that misses the site, so m = −11/24 < −3/8. The minimiser is the midpoint of the two face-sharing tet sites, as #53 found.

## Checks (all exact; floats only choose candidates)

| Script | What | Result |
|---|---|---|
| `scripts/circuits.py` | Theorem A by brute force. All (d+2)-sets with pairwise squared distance ≤ (2ρ)², where ρ is the largest corner-to-site distance from #53's data. Every dual cell lies inside this bound, and only sets whose lexicographically smallest site is in the motif are enumerated. Exact roots S₀/S_A in the open range, with an exact empty-sphere test, compared with the flips of the exact walk | **12/12 PASS**: the set of roots equals the flip list in every network, with nothing missed and nothing extra |
| `scripts/switchlocal.py` | Theorem B at the six switch points. Each switch point gets 5 checks: (1) every dual cell's sites are vertices of it; (2) no dual cell is a simplex; (3) every cell is bipartite; (4) the cells, one per translation class, fill the lattice cell exactly; (5) the predicted like bonds (hull edges) and unlike bonds (cell edges), by site and squared length, equal the exact walk on both neighbouring intervals | **30/30 PASS** |
| `scripts/rangeends.py` | Theorem C. Exact hull test and exact LP certificate (primal vertex plus non-negative dual multipliers), with the same optimum from a site list twice as large, for every motif site of all 12 networks; the range compared with the walk | **103/103 PASS** |
| `scripts/walks.py` | Exact walks of the two controls with #53's engine and checks | hbn 13/13, sodalite 54/54 PASS |

In all: **212 PASS, 0 FAIL.** Every script ends with a conditional FINAL line, and all are `FINAL ok`. Run on dicto-big-brother (`~/geom/bin/python`), one job at a time, about 40 s in all. #53's engine and site lists are imported from `../2026-10-25-relay-census/scripts`.

**Known-case sanity (reproduces #53).** For the fluorite octet, take the circuit oct (1,0,0), tet (3/2,−3/2,−1/2), (3/2,−1/2,−1/2), (3/2,−3/2,1/2), oct (2,−1,0) in the metric G = I/2, with α = (−1/2, −1/2, 1, 1/2, −1/2). Then S₀ = −1/8 and S_A = 1, so **λ* = −1/8**, #53's octet switch. Its empty power sphere carries 14 sites (6 oct + 8 tet): the rhombic dodecahedron.

All flips as S₀/S_A (one witnessing circuit each; `data/circuits-stdout.txt`):

| Network | Flip = S₀/S_A | Dual cell at the flip |
|---|---|---|
| square + centres | 0/−4 = 0 | square (2 + 2) |
| honeycomb + centres | −1/2 | rhombus (2 + 2) |
| CsCl | −8/8 = −1, −8/−8 = 1 | octahedra (2 big + 4 small; 4 + 2) |
| fluorite | −1/8 | RD (8 tet + 6 oct) |
| rock salt | 0/−2 = 0 | cube (4 + 4) |
| zinc blende | −16/16 = −1, 16/16 = 1 | 10 sites (6 S + 4 Zn; 4 + 6) |
| hcp holes | (1/16)/(−1/2) = −1/8, (−5/48)/(−1/2) = 5/24 | 14 sites (TRD); 8 sites |
| A15 | (9/16)/(9/4) = 1/4, (3/2)/2 = 3/4 | 5 sites; 8 sites (4 + 4) |
| C15 | 240/−48 = −5, 224/32 = 7, 288/32 = 9 | 8; 5; 8 sites |
| kagome + centres | none | — |
| h-BN (control) | 0/−3 = 0 | hexagon (3 + 3) |
| sodalite (control) | 0/2 = 0 | truncated octahedron (12 + 12) |

For the two controls the "flips of the exact walk" in `circuits.py` come from our own walks (`data/*-walk.json`), not from #53.

## Findings on #53

- No numerical inconsistency. All ten flip sets, all ten ranges and the like bonds on both sides of the four switch points are reproduced exactly by independent methods.
- **Observation 1 wording.** "Trades one set of diagonals for the other in a single flip" holds in the plane. In space, at fluorite, neither side is a triangulation: the cell becomes octahedron + 8 tetrahedra below and cube + 6 pyramids above. The switch is a wall of the secondary fan, not one bistellar (2-3) flip. #53 Corollary 2 already says "flip in that sense". The Concordance gap text "flips of regular triangulations (Edelsbrunner–Shah)" should read "walls between regular subdivisions; located by Edelsbrunner–Shah's lifted determinant".
- **Observation 3.** Theorem B(3) gives the criterion: a network has a single switch iff some λ* = S₀/S_A in its range makes every dual cell bipartite. This is finitely checkable by Theorem A. "Gradual" and "switch" are exclusive. The equal-weight cases (square, rock salt) are those where the Delaunay graph of the union lattice is already bipartite. A rule that predicts the type from the site set alone is still open.
- **Observation 4** is now Theorem C, with the exact criterion "a site lies in the hull of its nearest unlike neighbours" and the LP value otherwise.

## Prior art (sources checked)

- **Read, abstract or bibliographic page.** [ES] H. Edelsbrunner, N. R. Shah, "Incremental topological flipping works for regular triangulations", *Algorithmica* 15 (1996) 223–241, doi:10.1007/BF01975867 (Springer page; ISTA record). This is the lifted test and flips of regular triangulations in general position. Not in DICTO's library (Concordance: "to read").
- **Search snippets only.** [MS] G. L. Miller, D. R. Sheehy, "A new approach to output-sensitive Voronoi diagrams and Delaunay triangulations", arXiv:1212.5098 (abstract page): flip times are linear when weights change linearly. J. R. Shewchuk, flip-based constrained Delaunay notes (Shewchuk03-cdtflip, WIAS course copy): regular triangulations with heights changing linearly in time. [LW] C. W. Lee, W. Weber, "Recovering lexicographic triangulations", arXiv:1711.06699 (abstract page): pushing and pulling.
- **Cited from #53, not re-read.** [GKZ] Gelfand–Kapranov–Zelevinsky 1994, doi:10.1007/978-0-8176-4771-1. [DRS] De Loera–Rambau–Santos 2010, doi:10.1007/978-3-642-12971-1 (§2.3 refinement, §4.3 placing/pushing; link only). [Au87] Aurenhammer, *SIAM J. Comput.* 16 (1987) 78, doi:10.1137/0216006, and *DCG* 2 (1987) 49. Alexeev 2002 §5.12.
- **DICTO's reference library** (dicto-big-brother `~/kaleidohedra-references`; `cited/`, `papers/`, `expansion/` manifests and INDEX.html), searched for: Edelsbrunner, regular triangulation, weighted Delaunay, secondary, flip, Laguerre, power diagram, Aurenhammer, De Loera, Gelfand, Lawson, Alexeev, bipartite, Cayley trick, regular subdivision, Okabe. Hits: Edelsbrunner–Nikitenko arXiv:1705.08735 (weighted Poisson–Delaunay, not relevant); Garanzha–Kudryavtseva–Kamenski arXiv:2201.05135 (non-simplicial Delaunay meshing via radical partitions, title and abstract only); GKZ, DRS, Aurenhammer 1987, Ash–Bolker 1985 and Alexeev 2002 (as in #53).
- **Web queries (3):** the ES title; "kinetic regular triangulation weights vary linearly flip time affine power diagram"; "regular subdivision lowering a subset of vertices convex hull of subset pyramids pushing independent set".
- **Verdicts.** Theorem A: classical in substance (ES, MS, GKZ); the closed form λ* = S₀/S_A for a two-kind weight line was not found as stated. Theorem B(1): classical (DRS). B(2): a case of pushing (DRS, LW). B(3), the switch theorem for the bonds, and the two counterexamples were not found. Theorem C: elementary; not found as stated. "Not found" is limited to these sources.

## LEADS

1. **Observation 2 (CsCl ↔ zinc blende).** Both walks have flips ±1 from circuits with S₀ = ±8 and ±16 and S_A = ±8 and ±16, the same ratio. Diamond is half of bcc (2D₃ ⊂ 2ℤ³). Test whether the zinc blende circuits are the CsCl circuits scaled by 2 and whether that forces the same polynomials up to a constant.
2. **The DICTONIC network.** Apply Theorem B(3) to DICTO's own HexOct, TRD and RD-cross networks: a switch requires a bipartite weighted Delaunay subdivision. This is a quick screen for "one piece, any stacking" candidates whose bonds hand over at one weight.
3. **Three kinds (perovskite).** Theorem A extends to an affine function in (λ, μ), whose zero lines are #53's three walls. Check that the walls λ = 0, λ + 2μ = 0 and λ + μ = 1 are S₀ − λS_A − μS_B = 0 for explicit circuits.
4. **Sodalite and h-BN as real materials.** Loewenstein-ordered aluminosilicates and the B/N honeycomb. The switch at equal weights is where the Si/Al (or B/N) power diagram has only Si–O–Al-type contacts. The radical-tessellation literature on zeolites was not searched.
5. **A paper home** (route via the Concordance destinations; DICTO decides): Theorems A–C close #53 Observations 1 and 4. They fit a "Version 2 adds …" of #53 or a short note. Ask DICTO which.

## Ledger line (for the Concordance; not entered by this study)

`{"question": "#53 Obs 1/4: general switch theorem via lifted determinant", "method": "circuits.py brute force (S0/SA, exact empty sphere) + switchlocal.py exact hulls + rangeends.py exact LP", "status": "SETTLED", "result": "flips = empty-sphere roots S0/SA (12/12 nets); switch ⇒ hull(A)/hull(B) swap per bipartite cell, single switch; quadrilateral version false (h-BN, sodalite); range ends = LP, −d² iff site in hull of nearest unlike", "retry": "never", "study": "2026-11-08-switch-theorem", "date": "2026-11-08"}`

## Files

`scripts/`: circuits.py, switchlocal.py, rangeends.py, walks.py, extra_nets.py (the h-BN and sodalite nets).
`data/`: circuits-all.json and checks, circuits-stdout.txt; switchlocal.json and checks; rangeends.json and checks; hbn-walk.json, sodalite-walk.json and checks.
