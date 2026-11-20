# Packet screen (21 Nov 2026): which helpers carry a cancelling packet for each centre pyramid?

**DICTO's question:** "can any central pyramid have a complementary stand-in to help it fill space?"
**DICTO's idea (the packet):** each solid carries its Dehn invariant as a packet. If pieces fill space together in fixed
proportions, their packets must cancel in those proportions: n·D(P) + m·D(H) (+ …) = 0. This is necessary, not sufficient.
The octet is the model: 2·D(tetrahedron) + D(octahedron) = 0.

**Conclusion.** Of the 47 centre pyramids of the Platonic, Archimedean and Catalan solids, 3 have zero packets (cube, rhombic
dodecahedron, rhombic triacontahedron). 10 have a single helper in the library whose packet cancels theirs. 17 more need two
helpers. For the other 17 the library has nothing (this "none" result rests on a numerical independence check). All 97
cancellations found are exact: 26 with one helper and 71 two-helper sets. The cubic-family cancellations all run through one angle, arccos(1/3), and most of them are
known honeycombs cut into centre pyramids. The new leads are icosahedral:
the dodecahedron's pentagon pyramid with the truncated icosahedron (12:1, equal edges), and the icosahedron's triangle
pyramid with the truncated dodecahedron (20:1, equal edges). There is also one cross-symmetry pair: the tetrakis
hexahedron's triangle pyramid with the truncated icosahedron (9:1).

## Status box
- Study note, not published. Run on the compute host (~/venvs/indep/bin/python: sympy 1.14, mpmath; nothing installed).
  Every step was run in the foreground for at most 275 s. No background jobs.
- Exact: every piece, every edge length, every dihedral cosine, every angle relation (50 of 50 proved) and every cancellation
  listed (26 one-helper and 71 two-helper sets, all proved by exact identities).
- Numerical only: whether the 32 basis angles are independent over Q mod π. PSLQ at 300 digits found no further relation
  with coefficients ≤ 10⁴. Every "none in the library" verdict depends on this. Cancellations do not depend on it.
- The Vacuus pieces were not added. The Vacuus of #87 is the complex of fins O–A–B. Its cells are exactly the centre pyramids,
  which are already in the library. Sources checked: studies/2026-11-02-dicto-vacuus (README, data/vacuus-census.json,
  data/classical), the concordance entries for #87, #105 and #111 (papers/dicto-concordance/concordance.json), and
  studies/2026-11-21-gap-study. None of them gives a solid gap piece with exact coordinates other than the centre pyramids.
  #105 is 4D slices; #111 is fair dice.

## Library (80 pieces, data/pieces.json)
- **Solids (33).** 5 Platonic (D·I·C·T·O). 13 Archimedean, including both snubs, built exactly: the snub cube in Q(t), with
  t the tribonacci constant; the snub dodecahedron in Q(ξ), with ξ³ − 2ξ = φ. 13 Catalan, built as exact polar
  reciprocals in the midsphere. Square and pentagonal antiprisms.
- **Centre pyramids (47).** Apex at the solid's centre, base one face. Faces are grouped by exact edge data, which gives one
  type per face size; even the snub triangles in two symmetry orbits give the same pyramid.
- **Scale.** Platonic, Archimedean and antiprisms have edge 1. Each Catalan is the dual of the edge-1 Archimedean (canonical
  form). Each pyramid inherits its solid's scale.
- **Regular prisms.** Every dihedral is π/2 or (n−2)π/n, so the packet is zero by inspection. Prisms are neutral: they can
  join any mixture without changing the balance. They are listed here and not screened. The other zero-packet pieces in the
  library are the cube, rhombic dodecahedron, rhombic triacontahedron, truncated octahedron, truncated cuboctahedron and
  truncated icosidodecahedron. The last of these is exact here: its three dihedral angles sum to 5π/2.
- **Coordinates.** Platonic and 11 Archimedean: the exact textbook coordinates of studies/2026-11-02-dicto-vacuus
  (data/inputs). Snubs and antiprisms: built in scripts/solids.py. Every face is checked exactly for planarity and convexity.

## Method
1. **scripts/nf.py.** Exact arithmetic in K = Q[x]/(m) for four fields: Q(√2,√5), Q(2^¼), Q(t) and Q(ξ). It provides
   exact minimal polynomials (characteristic polynomial, then factor), exact square roots in K, and a formal radical ring
   K[y₁…y_k]/(y_i² − a_i). An identity that holds in the formal ring holds for every choice of the roots, so it is a sound
   proof.
2. **scripts/solids.py.** For every piece and every edge: the squared length, and cos² of the dihedral with its sign, all
   exact in K.
3. **scripts/angles.py.** There are 91 distinct dihedral angles. Each has an exact minimal polynomial of its cosine. Whether
   θ/π is rational is decided exactly by the Chebyshev test, reused from studies/2026-11-21-gap-study/scripts/pyramid_dehn.py:
   cos(2πk/n) has degree φ(n)/2, and minpoly | T_n − 1. Result: 9 rational, 82 irrational.
4. **scripts/relations.py.** Finds the Q-linear relations among the 82 irrational angles and π.
   - The angles are grouped by the square class of c²(1−c²). For an angle θ, e^{2iθ} lies in K(√−c²(1−c²)).
   - Kummer lemma, used only to order the search: if an angle's class lies outside the span of the other classes in a
     relation, apply the automorphism that flips that root. It sends e^{2iθ} to its inverse and fixes the rest, so
     e^{4kiθ} = 1 and θ would be rational. So no relation contains such an angle.
   - The basis is built greedily with PSLQ (mpmath, 300 digits, coefficients ≤ 10⁴). Each angle is tested first against its
     own class and then against the whole basis.
   - Every relation Σ k_j θ_j = pπ is proved exactly as the identity Π(cos θ_j + i sin θ_j)^{k_j} = (−1)^p in the formal
     radical ring. Result: basis of 32 angles; 50 relations, all proved (data/relations.json).
5. **scripts/screen.py.** The packet of a piece is D = Σ_b c_b ⊗ β_b. Each c_b is a sum of rational multiples of edge
   lengths, kept exactly in the radical ring.
   - Cancellation with free scales: n·P + Σ m_i·(λ_i H_i) = 0 holds if and only if c(P) = −Σ a_i c(H_i) with a_i > 0.
   - A single helper is proved exactly by c_b(P)·c_{b₀}(H) − c_{b₀}(P)·c_b(H) = 0 for every b. A pair of helpers is proved
     by 3×3 minors.
   - **Proportions.** We give the integer proportion pyramid:helper when the helper is scaled so that one of its edges equals
     one of the pyramid's edges. Each one is proved exactly. For two helpers, the proportion is given at the canonical
     scales.
   - Two-helper sets are searched only when no single helper exists. All pairs from the 80-piece library are tried.
6. **scripts/report.py.** Writes data/table.md and data/leads.json.

## Controls (logs/screen.log; all pass)
- Cube, rhombic dodecahedron and rhombic triacontahedron pyramids: packet exactly zero.
- Dodecahedron pyramid: packet nonzero.
- Tetrahedron + octahedron cancel, 2:1 at equal edges (the octet).
- Cuboctahedron triangle + square pyramids cancel 1:1 (the octet again, as in the 21 Nov gap study).
- Icosidodecahedron triangle + pentagon pyramids do NOT cancel (the gap study theorem).
- Tetrahedron + cube do NOT cancel.
- Additivity, for all 31 solids: the face-weighted sum of a solid's centre pyramids equals the solid's packet. This is exact,
  and it checks every relation used.

## Table: centre pyramid → zero packet / cancelling helpers / none
"Free scale" means each helper may be scaled. The proportion is pyramid:helper with one edge of the helper made equal to one
edge of the pyramid (unit edges unless noted in data/leads.json). "Scale-dependent" means no such matched-edge proportion
exists with denominators ≤ 48. A sibling pyramid (same solid) or the pyramid's own solid is a trivial helper.

| centre pyramid | faces | packet | cancelling helpers (free scale), best edge-matched proportion pyramid:helper |
|---|---|---|---|
| dodecahedron pentagon pyramid | 12 | nonzero, 1 basis angle(s) | 1: truncated icosahedron 12:1 |
| icosahedron triangle pyramid | 20 | nonzero, 1 basis angle(s) | 1: truncated dodecahedron 20:1 |
| cube square pyramid | 6 | **zero** (fills alone as far as Dehn can tell) | not needed |
| tetrahedron triangle pyramid | 4 | nonzero, 1 basis angle(s) | 5: octahedron triangle pyramid 1:1; truncated tetrahedron 4:1; cuboctahedron square pyramid 4:1; octahedron 8:1; rhombicuboctahedron 8:1 |
| octahedron triangle pyramid | 8 | nonzero, 1 basis angle(s) | 5: tetrahedron triangle pyramid 1:1; tetrahedron 4:1; cuboctahedron triangle pyramid 4:1; cuboctahedron 8:1; truncated cube 8:1 |
| truncated tetrahedron triangle pyramid | 4 | nonzero, 2 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrahedron triangle pyramid + truncated tetrahedron hexagon pyramid 1:1:1; truncated tetrahedron hexagon pyramid + cuboctahedron triangle pyramid 4:4:1; tetrahedron + truncated tetrahedron hexagon pyramid 4:1:4; truncated tetrahedron hexagon pyramid + cuboctahedron 8:8:1 |
| truncated tetrahedron hexagon pyramid | 4 | nonzero, 2 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrahedron triangle pyramid + truncated tetrahedron triangle pyramid 1:1:1; truncated tetrahedron triangle pyramid + cuboctahedron triangle pyramid 4:4:1; tetrahedron + truncated tetrahedron triangle pyramid 4:1:4; truncated tetrahedron triangle pyramid + cuboctahedron 8:8:1 |
| triakis tetrahedron triangle pyramid | 12 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| cuboctahedron triangle pyramid | 8 | nonzero, 1 basis angle(s) | 5: truncated tetrahedron 1:1; cuboctahedron square pyramid 1:1 (sibling pyramid (same solid)); octahedron 2:1; rhombicuboctahedron 2:1; octahedron triangle pyramid 1:4 |
| cuboctahedron square pyramid | 6 | nonzero, 1 basis angle(s) | 5: tetrahedron 1:1; cuboctahedron triangle pyramid 1:1 (sibling pyramid (same solid)); cuboctahedron 2:1 (its own solid); truncated cube 2:1; tetrahedron triangle pyramid 1:4 |
| rhombic dodecahedron rhombus pyramid | 12 | **zero** (fills alone as far as Dehn can tell) | not needed |
| truncated cube triangle pyramid | 8 | nonzero, 2 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. octahedron triangle pyramid + truncated cube octagon pyramid 4:4:3; cuboctahedron square pyramid + truncated cube octagon pyramid 4:1:3; octahedron + truncated cube octagon pyramid 8:1:6; truncated tetrahedron + truncated cube octagon pyramid 4:1:3 |
| truncated cube octagon pyramid | 6 | nonzero, 1 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. octahedron triangle pyramid + truncated cube triangle pyramid 3:4:4; cuboctahedron square pyramid + truncated cube triangle pyramid 3:1:4; octahedron + truncated cube triangle pyramid 6:1:8; truncated tetrahedron + truncated cube triangle pyramid 3:1:4 |
| triakis octahedron triangle pyramid | 24 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| truncated octahedron square pyramid | 6 | nonzero, 2 basis angle(s) | 1: truncated octahedron hexagon pyramid 3:4 (sibling pyramid (same solid)) |
| truncated octahedron hexagon pyramid | 8 | nonzero, 2 basis angle(s) | 1: truncated octahedron square pyramid 4:3 (sibling pyramid (same solid)) |
| tetrakis hexahedron triangle pyramid | 24 | nonzero, 1 basis angle(s) | 1: truncated icosahedron 9:1 |
| rhombicuboctahedron triangle pyramid | 8 | nonzero, 2 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrahedron triangle pyramid + rhombicuboctahedron square pyramid 4:4:9; cuboctahedron triangle pyramid + rhombicuboctahedron square pyramid 4:1:9; tetrahedron + rhombicuboctahedron square pyramid 4:1:9; cuboctahedron + rhombicuboctahedron square pyramid 8:1:18 |
| rhombicuboctahedron square pyramid | 18 | nonzero, 1 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrahedron triangle pyramid + rhombicuboctahedron triangle pyramid 9:4:4; cuboctahedron triangle pyramid + rhombicuboctahedron triangle pyramid 9:1:4; tetrahedron + rhombicuboctahedron triangle pyramid 9:1:4; cuboctahedron + rhombicuboctahedron triangle pyramid 18:1:8 |
| deltoidal icositetrahedron kite pyramid | 24 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| truncated cuboctahedron square pyramid | 12 | nonzero, 2 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated cuboctahedron hexagon pyramid + truncated cuboctahedron octagon pyramid 6:4:3 |
| truncated cuboctahedron hexagon pyramid | 8 | nonzero, 1 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated cuboctahedron square pyramid + truncated cuboctahedron octagon pyramid 4:6:3 |
| truncated cuboctahedron octagon pyramid | 6 | nonzero, 3 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated cuboctahedron square pyramid + truncated cuboctahedron hexagon pyramid 3:6:4 |
| disdyakis dodecahedron triangle pyramid | 48 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| snub cube triangle pyramid | 32 | nonzero, 2 basis angle(s) | none in the library (needs basis independence: numerical) |
| snub cube square pyramid | 6 | nonzero, 2 basis angle(s) | none in the library (needs basis independence: numerical) |
| pentagonal icositetrahedron pentagon pyramid | 24 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| icosidodecahedron triangle pyramid | 20 | nonzero, 2 basis angle(s) | no single helper; 21 two-helper sets (21 exact), e.g. icosahedron triangle pyramid + tetrakis hexahedron triangle pyramid (scale-dependent: a = 1, 0.6325); dodecahedron pentagon pyramid + icosahedron triangle pyramid (scale-dependent: a = 1.342, 1); icosahedron triangle pyramid + icosidodecahedron pentagon pyramid (scale-dependent: a = 1, 1.085); dodecahedron + icosahedron triangle pyramid (scale-dependent: a = 0.1118, 1) |
| icosidodecahedron pentagon pyramid | 12 | nonzero, 1 basis angle(s) | 1: truncated icosahedron scale-dependent (mu = 0.103006) |
| rhombic triacontahedron rhombus pyramid | 30 | **zero** (fills alone as far as Dehn can tell) | not needed |
| truncated dodecahedron triangle pyramid | 20 | nonzero, 3 basis angle(s) | no single helper; 2 two-helper sets (2 exact), e.g. icosahedron triangle pyramid + truncated dodecahedron decagon pyramid 5:5:3; icosahedron + truncated dodecahedron decagon pyramid 20:1:12 |
| truncated dodecahedron decagon pyramid | 12 | nonzero, 2 basis angle(s) | no single helper; 2 two-helper sets (2 exact), e.g. icosahedron triangle pyramid + truncated dodecahedron triangle pyramid 3:5:5; icosahedron + truncated dodecahedron triangle pyramid 12:1:20 |
| triakis icosahedron triangle pyramid | 60 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| truncated icosahedron pentagon pyramid | 12 | nonzero, 3 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrakis hexahedron triangle pyramid + truncated icosahedron hexagon pyramid (scale-dependent: a = 0.4714, 1.667); dodecahedron pentagon pyramid + truncated icosahedron hexagon pyramid 3:3:5; icosidodecahedron pentagon pyramid + truncated icosahedron hexagon pyramid (scale-dependent: a = 0.809, 1.667); dodecahedron + truncated icosahedron hexagon pyramid 12:1:20 |
| truncated icosahedron hexagon pyramid | 20 | nonzero, 2 basis angle(s) | no single helper; 5 two-helper sets (5 exact), e.g. tetrakis hexahedron triangle pyramid + truncated icosahedron pentagon pyramid (scale-dependent: a = 0.2828, 0.6); dodecahedron pentagon pyramid + truncated icosahedron pentagon pyramid 5:3:3; icosidodecahedron pentagon pyramid + truncated icosahedron pentagon pyramid (scale-dependent: a = 0.4854, 0.6); dodecahedron + truncated icosahedron pentagon pyramid 20:1:12 |
| pentakis dodecahedron triangle pyramid | 60 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| rhombicosidodecahedron triangle pyramid | 20 | nonzero, 3 basis angle(s) | none in the library (needs basis independence: numerical) |
| rhombicosidodecahedron square pyramid | 30 | nonzero, 2 basis angle(s) | none in the library (needs basis independence: numerical) |
| rhombicosidodecahedron pentagon pyramid | 12 | nonzero, 3 basis angle(s) | none in the library (needs basis independence: numerical) |
| deltoidal hexecontahedron kite pyramid | 60 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| truncated icosidodecahedron square pyramid | 30 | nonzero, 3 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated icosidodecahedron hexagon pyramid + truncated icosidodecahedron decagon pyramid 15:10:6 |
| truncated icosidodecahedron hexagon pyramid | 20 | nonzero, 2 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated icosidodecahedron square pyramid + truncated icosidodecahedron decagon pyramid 10:15:6 |
| truncated icosidodecahedron decagon pyramid | 12 | nonzero, 3 basis angle(s) | no single helper; 1 two-helper sets (1 exact), e.g. truncated icosidodecahedron square pyramid + truncated icosidodecahedron hexagon pyramid 6:15:10 |
| disdyakis triacontahedron triangle pyramid | 120 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |
| snub dodecahedron triangle pyramid | 80 | nonzero, 2 basis angle(s) | none in the library (needs basis independence: numerical) |
| snub dodecahedron pentagon pyramid | 12 | nonzero, 2 basis angle(s) | none in the library (needs basis independence: numerical) |
| pentagonal hexecontahedron pentagon pyramid | 60 | nonzero, 1 basis angle(s) | none in the library (needs basis independence: numerical) |

Counts: zero packet 3 · one helper 10 · two helpers only 17 · none in the library 17. The 17 "none" pyramids are 10 Catalan
pyramids (all except the rhombic dodecahedron, the rhombic triacontahedron and the tetrakis hexahedron), the 4 snub
pyramids and the 3 rhombicosidodecahedron pyramids. Each of the 10 Catalan pyramids carries a packet on an angle that only
its own solid has. The solid's packet is F times the pyramid's, in the same direction, so it cannot help.

Trivial or already realised (Dehn agrees with a known tiling):
- tetrahedron pyramid + octahedron pyramid 1:1 (the octet with each solid cut into its centre pyramids);
- cuboctahedron triangle pyramid (a regular tetrahedron) + truncated tetrahedron 1:1 (quarter cubic honeycomb);
- cuboctahedron square pyramid (a half octahedron) + truncated cube 2:1 (truncated cubic honeycomb, octahedra halved);
- octahedron pyramid + cuboctahedron 8:1 (rectified cubic honeycomb, octahedra cut into 8 pyramids);
- every set made of sibling pyramids of a zero-packet solid: truncated octahedron 6:8, truncated cuboctahedron 12:8:6,
  truncated icosidodecahedron 30:20:12;
- every set that completes the pyramid's own solid (for example truncated tetrahedron triangle + hexagon pyramids
  + tetrahedra).

## LEADS for an actual tiling search, ranked
1. **Dodecahedron pentagon pyramid + truncated icosahedron, 12:1, equal edges (exact).** D(P) = 5 ⊗ β₁ and
   D(TI) = −60 ⊗ β₁, where β₁ = arctan φ (58.28°). Twelve pyramids balance one truncated icosahedron. That is the same
   balance as dodecahedron : truncated icosahedron = 1:1, but the pyramids can be placed one by one, which the
   dodecahedron cannot. No icosahedral tiling is known, so this is open.
2. **Icosahedron triangle pyramid + truncated dodecahedron, 20:1, equal edges (exact).** D(P) = −3 ⊗ β₇₆ and
   D(TD) = 60 ⊗ β₇₆, where cos β₇₆ = 1/√6 (65.91°). This is the same structure as lead 1, from the dual side.
3. **Tetrakis hexahedron triangle pyramid + truncated icosahedron, 9:1 (exact).** The pyramid's edge 9√2/8 is matched to
   the truncated icosahedron's edge 1. With its long base edge 3√2/2 matched instead, the proportion is 12:1. This pair crosses
   symmetry families: the tetrakis hexahedron's dihedral arccos(−4/5) equals 4β₁ − π/2 (a proved relation), so a cubic
   Catalan pyramid shares the dodecahedron's packet line. The same line holds the icosidodecahedron pentagon pyramid, but
   its helper (the truncated icosahedron) cancels it only at an irrational scale (μ = 0.10301). That one is weaker.
4. **Tetrahedron + rhombicuboctahedron, 2:1 at equal edges** (as the cuboctahedron triangle pyramid + rhombicuboctahedron
   2:1, or the tetrahedron pyramid + rhombicuboctahedron 8:1). This is in the cubic family; cubes, which are neutral,
   may be added freely. It has not yet been checked against the uniform and non-uniform honeycomb lists. Do that before any
   search.
5. **Icosidodecahedron triangle pyramid.** It has no single helper, but 17 exact two-helper sets. The simplest use
   equal-edge pieces: icosahedron triangle pyramid + tetrakis hexahedron triangle pyramid (a = 1 and 0.63246), and
   dodecahedron pentagon pyramid + icosahedron triangle pyramid (a = 1.3416 and 1). Every one of them needs an irrational
   ratio at the canonical scales (numerical recognition, denominators ≤ 48), so this lead is weak.

Not promising in this library: the snubs, the rhombicosidodecahedron and 10 Catalan pyramids (packets on angles no other
piece has; numerical independence). The truncated-solid pyramids (truncated tetrahedron, truncated cube,
rhombicuboctahedron, truncated dodecahedron, truncated icosahedron) cancel only with a sibling pyramid present, which in
effect rebuilds the solid.

## Files
- scripts/: nf.py, solids.py, angles.py, relations.py, screen.py, report.py (run in that order).
- data/pieces.json: exact edge data. data/angles.json: 91 angles with minimal polynomials and the rationality test.
  data/relations.json: 32 basis angles, 50 relations, each with proved_exact = true. data/packets.json: exact and
  numerical packets, and the screen. data/leads.json, data/table.md. data/inputs: exact coordinates copied from
  2026-11-02-dicto-vacuus.
- logs/: solids, angles, relations (three parts), screen, report. Each ends with FINAL ok.
