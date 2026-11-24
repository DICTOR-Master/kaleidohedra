# Tacitus: harmonic silence of face directions (25 November 2026)

DICTO · dictospheres.com · study 2026-11-25-tacitus · with Claude (Anthropic).

DICTO names a fourth quality, alongside Vacuus, Resonus and Aequus: **Tacitus** (Latin: silent), harmonic silence. This study fixes
the definition, runs one census over 163 polyhedra, 15 126 Aequi and the six regular 4D polytopes (degrees k ≤ 20), and asks
which silences go **beyond symmetry**. Checks: tacitus.py FINAL ok (logs/poly.log, 4d.log, aequi-0/1/2.log); post.py FINAL ok;
exact_check.py FINAL ok (logs/exact.log); summarize.py FINAL ok (logs/summary.md, the full tables).

## Definition

Let P be a polyhedron with outward unit face normals n_f and weights w_f > 0. Two variants:
(i) w_f = 1, each face once; (ii) w_f = Ω_f, the solid angle of face f seen from the centre (corner centroid).
For an Aequus every Ω_f = 4π/N, so (i) = (ii).

**P is Tacitus in degree k** when Σ_f w_f h(n_f) = 0 for every harmonic polynomial h of degree k. Equivalently
Σ_f w_f P_k(n_f·x) = 0 for all x, or e_k = (Σw)⁻² Σ_{f,g} w_f w_g P_k(n_f·n_g) = 0 (P_k Legendre; e_k ≥ 0 because the zonal kernel is
positive definite: the zonal test of Delsarte, Goethals and Seidel [1], used in #109 *Silent Running*). Silent in all k = 1..t is a
spherical t-design. On S³ (4D) P_k is replaced by the Gegenbauer polynomial C_k^(1) = U_k, as in #109.

**Forced silence** (Sobolev [3]; Goethals and Seidel [2]): if G is the symmetry group of the weighted set and G has no invariant
harmonic of degree k, the set is silent in k. Here G is the group of the weighted **direction set**, which can be larger than the
polyhedron's own group (the truncated tetrahedron's 8 unweighted normals are the cube's diagonals: Oh, not Td).
**Silence beyond symmetry** = silent in k although G has an invariant harmonic of degree k. That is the Tacitus content.

Which degrees are informative: a centrally symmetric set (−I in G) is silent in every odd k, so only even k carry information;
a set without central symmetry has informative odd degrees as well. Even-degree silence depends only on the multiset of face
**axes** (P_k is even), so for even k a direction and its opposite count alike. Baseline for Ih: silent in 1–5, 7, 8, 9, 11, 13,
14, 15, 17, 19 (k ≤ 20); invariant harmonics in 6, 10, 12, 16, 18, 20; the even degrees Ih forces are exactly 2, 4, 8, 14
(even invariant degrees are 6a + 10b; every even number ≥ 16 is one).

## Method

- scripts/extract_polyhedra.py: the 163 polyhedra of study 2026-11-24-vacuus-resonus-catalogue (5 Platonic, 13 Archimedean,
  13 Catalan, 40 prisms, antiprisms and their duals for n = 3..12, 92 Johnson), built with that study's exact builders unchanged;
  normals and corners written in floating point.
- scripts/tacitus.py: one generic census. e_k for k ≤ 20; G found as all orthogonal maps permuting the weighted set; dim H_k^G
  by the character average (rotation by θ: χ_k = 1 + 2Σcos mθ; improper g: (−1)^k χ_k(−g)). 4D: Coxeter degrees and Molien.
  Silent: e_k < 1e-11; nonzero: e_k > 1e-8; in between ("grey") goes to the exact check. Aequi: the 4 553 of study 2026-11-19,
  the 1 083 of study 2026-11-20 (two placements; with 149 of the 4 553 these are the catalogued 1 232) and the 9 490 of
  catalogue-2 (Nos. 1236–10725); the 4 404 of study 2026-11-24-aequi-certify-4404 are a subset of the 4 553 (tagged).
  Face directions are the exact frame directions of those studies.
- scripts/post.py: for each Aequus silence beyond symmetry, an **exact cover** test: can the face set (odd k), or its multiset of
  axes (even k), be split into whole orbits of subgroups H of the frame groups (Ih in either icosahedron placement, Oh; 374
  subgroups) with H forcing degree k? If so the silence is **composite**: a sum of forced silences of the pieces (exact: index sets
  and group theory). Otherwise **accidental**.
- scripts/exact_check.py: exact arithmetic in Q(√5) with the radicals √2, √3, √(φ+2) kept apart (they are linearly independent
  over Q(√5): Q(√2, √3, √5) is multiquadratic and cannot contain the cyclic quartic Q(√(φ+2))). Every accidental silence is proved
  exactly zero; every near miss (1e-11 < e_k < 1e-5) is proved exactly nonzero; the one grey case is settled.
- Rigour of "not silent" for the 163 polyhedra: e_k > 1e-8 in double precision (smallest 1.48e-8, J85 variant ii) against an
  a-priori rounding bound below 1e-12 (N² terms, stable three-term recurrence on |t| ≤ 1). The solid angles of (ii) are
  computed in floating point (they are transcendental in general).

## Results

**Platonic, Archimedean, Catalan, prisms, antiprisms and their duals, the three permutahedra: no silence beyond symmetry,
in either variant, for k ≤ 20.** Each is silent in exactly its forced degrees: Ih family 1–5, 7–9, 11, 13–15, 17, 19; I (snubs
of the dodecahedron and its dual) the same without 15; Oh family odd degrees and 2; O (snub cube and dual) 1, 2, 3, 5, 7, 11;
Td (tetrahedron, triakis tetrahedron) 1, 2, 5. The three permutahedra are the truncated octahedron (Oh), truncated cuboctahedron
(Oh) and truncated icosidodecahedron, the hub (Ih): nothing beyond symmetry. Weighting by solid angle (ii) changes no silent set
except where it lowers the symmetry (truncated tetrahedron: Oh → Td) or breaks a balance (J7).

**Near miss.** The triakis tetrahedron in degree 17: e₁₇ = 9.2 × 10⁻⁹, exactly nonzero (its normals are (3, 1, 1) with an even
number of minus signs; rational arithmetic). It is the closest any of the 163 comes to an unforced silence.

**Johnson polyhedra: 9 of 92 are silent beyond symmetry**, all explained by Theorem 2:

| polyhedron | faces | \|G\| | silent (i) | beyond (i) | beyond (ii) | reason |
|---|---|---|---|---|---|---|
| J7 elongated triangular pyramid | 7 | 6 | 1 | 1 | – | 2(c) |
| J12 triangular bipyramid | 6 | 12 | 1, 5 | 5 | 5 | 2(c) |
| J27 triangular orthobicupola | 14 | 12 | 1, 2 | 2 | 2 | 2(a), cuboctahedron, n = 3 |
| J34 pentagonal orthobirotunda | 32 | 20 | 1, 2, 3, 4, 8, 14 | 2, 4, 8, 14 | 2, 4, 8, 14 | 2(b), icosidodecahedron |
| J37 elongated square gyrobicupola | 26 | 16 | 1, 2, 3 | 2 | 2 | 2(a), rhombicuboctahedron, n = 4 |
| J72 gyrate rhombicosidodecahedron | 62 | 10 | 1–4 | 1–4 | 1–4 | 2(a), n = 5 |
| J73 parabigyrate rhombicosidodecahedron | 62 | 20 | 1–5, odd | 2, 4 | 2, 4 | 2(a), n = 5 |
| J74 metabigyrate rhombicosidodecahedron | 62 | 4 | 1–4 | 1–4 | 1–4 | 2(a), n = 5 |
| J75 trigyrate rhombicosidodecahedron | 62 | 6 | 1–4 | 1–4 | 1–4 | 2(a), n = 5 |

**Regular 4D polytopes (facet normals on S³): nothing beyond symmetry.**

| polytope | normals | silent k ≤ 20 |
|---|---|---|
| 5-cell | 5 | 1, 2 |
| tesseract | 8 | odd, 2 |
| 16-cell | 16 | odd, 2 |
| 24-cell | 24 | 1–5, 7, 9, 10, 11, odd |
| 120-cell | 120 | 1–11, 13–19 |
| 600-cell | 600 | 1–11, 13–19 |

(The 120-cell's normals are the 600-cell's corners, an 11-design; classical, [1, 2].)

**The stellation cycle.** The Kepler–Poinsot stars have the 12 face planes of the dodecahedron (small stellated, great, great
stellated dodecahedron) or the 20 of the icosahedron (great icosahedron), one face per plane, so their face directions with
multiplicity are the Platonic sets: silent exactly in the Ih degrees. The Dogstar's 12 face planes are one orbit of its group Th,
so they carry equal multiplicity and again form the dodecahedron's direction set (Ih). Measured against the Dogstar's **own** group
Th, it is therefore silent beyond symmetry in **4, 8 and 14** (Th forces only 2 and the odd degrees). This is the same mechanism as
the Th and T Aequi below.

**Aequi: 813 of 15 126 dice (987 die-degree pairs) are silent beyond symmetry.**

| set | dice | beyond symmetry |
|---|---|---|
| 2026-11-19 (4 553) | 4 553 | 314 |
| 2026-11-20 two placements | 1 083 | 75 |
| catalogue-2 (Nos. 1236–10725) | 9 490 | 424 |
| of which the catalogued 1 232 | 1 232 | 79 |
| of which the 4 404 | 4 404 | 310 |
| stellation-cycle coincidence dice (the 42 entries of that study's data/aequi.json; its README counts 39) | 42 | 4 (all composite, k = 5) |

- **701 pairs are composite** (Theorem 3): for example every T, Th, Td and O die silent in 4, 8, 14 is a union of whole Ih-orbits
  taken from the two icosahedron placements (silent in all Ih degrees each, while the common group is only Th or T); the D2 and
  D2d dice silent in 5 are unions of regular tetrahedra (Td forces 5) and similar pieces.
- **286 pairs are accidental**, all proved exactly zero: degree 2 (90 pairs: S6 41, D2d 14, D4h 13, C4h 9, D2h 5, D3d 4, D3 4),
  degree 3 (111: D2 71, D3 32, D2d 8), degree 4 (13: T 12, S6 1), degree 5 (72: D3 65, D2d 7). Examples: D4h: C6/4 + RD12/8 (k = 2);
  T: C6 + RD12 + RT24/12 (k = 4); D3: O8+I12/6 + D12/6 (1) (k = 5); D2: RT24/4a + RT24/4b (1) (k = 3). 152 are in catalogue-2, 126 in
  the 4 553 (122 of them in the 4 404), 8 in the two-placement set.
- **No accidental silence above degree 5**, and no die is silent beyond symmetry above degree 14.
- **Near misses:** 125 die-degree pairs have 1e-11 < e_k < 1e-5; all are exactly nonzero. Closest: D5d: C6+RT24/10a + C6+RT24/10b +
  O8+I12/10 + D12/2 (4), k = 4, e = 4.9e-8.
- The hub (the H3 permutahedron) has no Aequus counterpart with extra silence; the stellation-cycle dice do not stand out (4 of 42,
  all composite, against 813 of 15 126 overall).

## Theorems and observations

**Theorem 1 (forced silence; classical).** A set whose symmetry group G has no invariant harmonic of degree k is silent in k.
*Proof.* Σ_f h(n_f) = Σ_f (Πh)(n_f), Π the averaging over G, and Πh = 0. (Sobolev [3]; Goethals and Seidel [2].)

**Theorem 2 (moving a piece).** Let X = A ⊎ B be silent in degree k and g an isometry with g·M_k(A) = M_k(A), where M_k(A) is the
degree-k harmonic moment of A. Then gA ⊎ B is silent in k. This holds in particular when
(a) A is invariant under the n-fold rotation about an axis u, g is any rotation about u, and k < n (M_k(A) then has only the
    zonal component m = 0, which every rotation about u fixes);
(b) X = T ⊎ (−T) and k is even (then M_k(T) = ½M_k(X) = 0, so T ⊎ g(−T) is silent for every isometry g);
(c) X = A ⊎ {a}, a on the axis u: M_k(A) = −M_k({a}) is zonal about u, so for odd k the reflection σ in the plane at right angles to
    u gives M_k(A ⊎ σA) = 0.
*Proof.* M_k is additive over multisets and equivariant: M_k(gA) = g·M_k(A). In (a) the moment of a C_n-invariant set has only
components m ≡ 0 mod n, and |m| ≤ k < n leaves m = 0. In (c) a zonal harmonic of odd degree changes sign under σ. ∎
*Corollaries:* J27, J37, J72–J75 (gyrated caps, (a)); J34 = icosidodecahedron with one rotunda turned, silent in exactly the even
Ih-forced degrees 2, 4, 8, 14 in every degree (by (b) these hold; every even degree ≥ 16 and 6, 10, 12 carry an Ih invariant, so
(b) gives no more); J12 = two tetrahedra less their shared faces ((c), k = 5); J7: Σ n_f = 0 directly (tetrahedron sides + base,
prism sides cancel), which fails with solid-angle weights.

**Theorem 3 (composite silence; checked here).** If the face set (odd k) or the face-axis multiset (even k) splits into whole orbits
of groups H_j each forcing degree k, it is silent in k. 701 of the 987 Aequi pairs have such a split inside the frame groups
(post.py, exact covers recorded in data/post.json).

**Observation 4 (accidental silence).** 286 Aequi die-degree pairs are silent with no such split: exactly zero in Q(√5), all in
degrees 2–5, for the groups S6, D2, D2d, D2h, D3, D3d, D4h, C4h and T. Degree 2 means the face directions have
isotropic second moment (Σ n_f n_fᵀ = (N/3)I) without a symmetry reason. Whether some signed decomposition explains the
degree-3, 4 and 5 cases is open.

**Observation 5.** In the 163 polyhedra and the six regular 4D polytopes every silence beyond symmetry comes from Theorem 2
(cut-and-turn operations on a symmetric parent). No polyhedron of the catalogue is accidentally silent.

## Prior art and credit

Classical and credited: spherical designs and the zonal (Gegenbauer) test, Delsarte, Goethals and Seidel [1]; designs from orbits
of finite groups and the invariant-harmonic criterion, Goethals and Seidel [2] after Sobolev [3]; the 11-design of the 600-cell
corners, [1, 2]; silent degrees and twisted silence in the 600-cell, DICTO's #109 *Silent Running* (definitions reused here);
harmonic index designs, Bannai, Okuda and Tagami (cited in #109). The Aequi frame directions, groups and the frame-group code are
from studies 2026-11-19-aequi-complete and 2026-11-24-aequi-certify-extend (groups.py, reused unchanged).
New here (to our knowledge): the Tacitus census of face directions (both weightings) over the catalogue and the Aequi; Theorem 2
as applied to the Johnson polyhedra (the moving-a-piece principle itself is elementary); the composite/accidental split and the
286 exact accidental Aequi silences; the triakis tetrahedron near miss. Sources checked (free routes): Goethals–Seidel record at
research.tue.nl; Nozaki and Sawa, "Note on cubature formulae and designs obtained from group orbits", Canad. J. Math. (2012,
arXiv 1102.4891), which cites [2, Thm 3.12]; Bannai's survey of spherical designs (math.unipd.it lecture PDF, title page only); a
web search for spherical designs from Johnson or Archimedean face normals (nothing found). [1]–[3] are cited, not opened.

[1] P. Delsarte, J. M. Goethals, J. J. Seidel, Spherical codes and designs, Geom. Dedicata 6 (1977) 363–388.
[2] J. M. Goethals, J. J. Seidel, Cubature formulae, polytopes, and spherical designs, in: The Geometric Vein, Springer (1981) 203–218.
[3] S. L. Sobolev, Cubature formulas on the sphere invariant under finite groups of rotations, Soviet Math. Dokl. 3 (1962) 1307–1310.

## Files

scripts/ (extract_polyhedra.py, tacitus.py, post.py, exact_check.py, summarize.py); data/polyhedra.json (corners, faces, normals),
data/poly.jsonl, data/4d.jsonl, data/aequi-0/1/2.jsonl (per set: N, |G|, silent, forced, beyond, explanation class),
data/post.json (beyond and near-miss dice with exact covers), data/exact.json; logs/ (summary.md = full tables).

## LEADS

1. Explain the 286 accidental Aequi silences: allow signed splits (Theorem 2(c) style) and blocks leaving the frame; see whether
   the degree-3 D2 and degree-5 D3 cases follow from one identity.
2. Degree-2 accidental silence = isotropic face directions: characterise it as one equation on the orbit sizes and directions;
   it is a candidate rule for "Tacitus Aequi".
3. Apply Theorem 2 to the Aequi: turning a C_n-symmetric cap of a die keeps degrees < n silent; when does it keep the die fair?
4. The triakis tetrahedron near miss (k = 17, e = 9.2e-9): is there a nearby Td set, varying the pyramid height, that is exactly
   silent in 17? A one-parameter family through it would give a Td 17-silent set.
5. Odd degrees for J34: Theorem 2(b) is silent on them; the census finds none beyond D5h up to 20; prove for all k.
