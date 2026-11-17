# The Integer Queens: the 600-cell deconstruction for E7 and E8 (18 Nov 2026)

DICTO · dictospheres.com

**DICTO's approval (18 Nov 2026):** "start the E7 E8 integer queens". Paper #110 *Walls of Silence* takes the 600-cell apart into five orbits of S5 in sum-zero R⁵. The construction works because W(A4) ⊂ W(H4). The heptagonal-queen study proved that W(A6) lies in no larger reflection group, and its LEADS named the next cases, A7 ⊂ E7 and A8 ⊂ E8. Here we run the deconstruction for those two. Every coordinate is rational, with no φ. Computation was done with Claude (Anthropic). This study serves aim 2 (geometry gives laws).

Labels: **exact** means integer or rational arithmetic, or a proof. **Certified** means found in floating point and then confirmed exactly. No label is upgraded.

## Answer

1. **Orbit splits** (exact). The S9 split of the E8 roots (Gosset's 4_21) is **240 = 72 + 84 + 84**:
   - 72 = the A8 roots;
   - 84 + 84 = ±Δ(9,3), centred.

   The S9 split of the 2160 corners of 2_41 is **2160 = 756 + 630 + 630 + 72 + 72**:
   - 756 = the norm-4 vectors of A8;
   - ± a stericated 8-simplex (630 each);
   - ± a truncated 8-simplex (72 each).

   For E7 under S8:
   - the roots (2_31) split as **126 = 56 + 70**: the A7 roots and Δ(8,4), centred;
   - the corners of 3_21 split as **56 = 28 + 28**: ±Δ(8,2), centred.

   All three expected starting points hold. Every orbit is a uniform polytope.
2. **Hidden symmetry** (exact; theorem plus a full reflection search). The only finite reflection groups of rank n ≥ 5 that contain W(A_n) are W(A_n) itself, plus W(E7) for n = 7 and W(E8) for n = 8. B_n, C_n and D_n never contain it, and neither does E6 for n = 6.
   - Each E_n containing the A_n is unique.
   - An S_{n+1}-invariant set either gains all of W(E_n) or keeps exactly S_{n+1} or S_{n+1} × {±1}. It gains W(E_n) exactly when it is a union of whole W(E_n)-orbits.
   - Within the four shells, of the 7 + 31 + 3 + 3 unions of S-orbits, **only the four whole shells gain**:
     - 4_21 and 2_41 have order 696729600;
     - 2_31 and 3_21 have order 2903040.
   - Every other union keeps exactly the 36 (or 28) reflections of S9 (or S8).
3. **Walls and Vacuus** (#110 §2; exact facets, certified plate normals).
   - **4_21 has 9840 walls**: 120 mirrors and 9720 cross walls. **2_31 has 379**: 63 mirrors and 316 cross walls.
   - The orbits from the root shells are all **hidden**:
     - the A8 roots and the A7 roots (heart; 9 and 8 plates, all cross walls), the analogue of C3;
     - ±Δ(9,3) (inherited heart; 36 S9 mirrors and 72 cross walls);
     - Δ(8,4) (heart; 28 S8 mirrors and 28 cross walls).
   - The orbits of 2_41 and 3_21 are only **partly hidden**.
   - **No orbit has a plate on one of the hidden E mirrors** (the 84 mirrors of E8 outside S9, the 35 of E7 outside S8). This differs from the 600-cell, where A's plates fill the hidden H4 mirrors. Here the larger symmetry reaches the orbits only through cross walls.
4. **Heptagon link** (exact). Under S7 (on the first seven coordinates), the E7 roots split as **126 = 42 + 7 + 7 + 35 + 35**. This is the 7-fold symmetry that E7 hides, one dimension above the heptagonal setting.

## Construction (scripts/s1_orbits.py, data/s1_orbits.log, FINAL ok, 25 checks)

The lattices are built by gluing, following Conway and Sloane (SPLAG, ch. 4; cited, not opened). The glue vectors [i] are those of A_n*:
- E8 = A8 ∪ (A8 + [3]) ∪ (A8 + [6]). Scaled by 3, this is the set of integer vectors in R⁹ with sum 0 and all coordinates congruent mod 3.
- E7 = A7 ∪ (A7 + [4]). Scaled by 4, all coordinates are ≡ 0 mod 4, or all are ≡ 2 mod 4.
- E7* = A7 + {[0], [2], [4], [6]}. Scaled by 4, all coordinates are congruent mod 4.

Each shell was enumerated as sorted tuples, and each sorted tuple is one S-orbit. Checks:
- the shell counts 240, 2160, 126 and 56 (theta series);
- S + the reflection s_r in one glue root generates W(E) (sympy Schreier–Sims), checked by stabiliser × orbit;
- each shell is one W(E)-orbit.

Gaps are listed with the Dynkin rings (Coxeter's t-notation, nodes 0 to n−1).

| shell | corners | S-orbit: seed (sorted) | corners | polytope |
|---|---|---|---|---|
| 4_21 (E8 roots) | 240 | (1, 0⁷, −1) | 72 | expanded 8-simplex t₀,₇ (A8 root polytope) |
| | | (2/3³, −1/3⁶) | 84 | Δ(9,3) centred = birectified 8-simplex t₂ |
| | | (1/3⁶, −2/3³) | 84 | its negative, Δ(9,6) (t₅) |
| 2_41 | 2160 | (1, 1, 0⁵, −1, −1) | 756 | t₁,₆{3⁷}, uniform (the norm-4 vectors of A8) |
| | | (4/3, 1/3⁴, −2/3⁴) | 630 | stericated 8-simplex t₀,₄ |
| | | (2/3⁴, −1/3⁴, −4/3) | 630 | its negative (t₃,₇) |
| | | (5/3, 2/3, −1/3⁷) | 72 | truncated 8-simplex t₀,₁ |
| | | (1/3⁷, −2/3, −5/3) | 72 | its negative (t₆,₇) |
| 2_31 (E7 roots) | 126 | (1, 0⁶, −1) | 56 | expanded 7-simplex t₀,₆ (A7 root polytope) |
| | | (1/2⁴, −1/2⁴) | 70 | Δ(8,4) centred = trirectified 7-simplex t₃ |
| 3_21 | 56 | (3/4², −1/4⁶) | 28 | Δ(8,2) centred = rectified 7-simplex t₁ |
| | | (1/4⁶, −3/4²) | 28 | its negative, Δ(8,6) |

As with the 600-cell, a host splits into an A_n root orbit and other orbits on the same sphere. Here the other orbits are the "wedge" orbits ∧³ and ∧⁶ of A8, and ∧⁴ of A7. In the 600-cell, A and B are non-uniform (golden). Here every orbit is uniform.

## Hidden symmetry (exact)

**Theorem.** Let X be a finite set in sum-zero R^{n+1}, n ≥ 5, that S_{n+1} maps to itself, and let G be its symmetry group.
1. The reflections in G generate a normal subgroup R ⊇ W(A_n). It is irreducible, since A_n acts irreducibly.
2. All A_n reflections are conjugate in R, so the A_n roots lie in one root length of R. In B_n and C_n that length is D_n, or A1ⁿ, which is impossible since A_n is connected. In F4 it is D4.
3. Normalise the roots to norm 2. The A_n root lattice then has full rank in the root lattice of R, so det(A_n)/det(R) = (n+1)/det(R) must be the square of an integer (the index).
   - Exact Cartan determinants: A_n gives n+1, D_n gives 4, E6, E7 and E8 give 3, 2 and 1.
   - The ratio is a square only for R = A_n, E7 (8/2 = 2²) and E8 (9/1 = 3²). D7 gives 2, D8 gives 9/4, E6 gives 7/3.
   - Non-crystallographic groups exist only up to rank 4.
4. **Uniqueness.** The lattice of R sits between A_n and A_n*, and A_n*/A_n is cyclic of order n+1. It therefore has exactly one subgroup of index 2 (for n = 7) or 3 (for n = 8). The roots of E_n are the norm-2 vectors of that lattice.
5. G normalises R, so G ⊆ Aut(Φ_R). This is W(A_n) × {±1} if R = A_n, and W(E_n) if R = E_n (which contains −1).

**Corollary.** X gains E_n symmetry exactly when s_r(X) = X for one glue root r. This holds exactly when X is a union of W(E_n)-orbits. Otherwise |G| = (n+1)! or 2(n+1)!, according to whether X = −X.

**Check without the theorem.** Every reflection of X maps some x to some y ≠ x, so its root is parallel to x − y. For every union, every difference line was tested exactly, one per S-class. This finds the complete set of reflections of X.

| shell | unions of S-orbits | gain W(E) | reflections in every other union |
|---|---|---|---|
| 4_21 (72, 84, 84) | 7 | only all three (120 reflections) | 36 |
| 2_41 (756, 630, 630, 72, 72) | 31 | only all five | 36 |
| 2_31 (56, 70) | 3 | only both (63) | 28 |
| 3_21 (28, 28) | 3 | only both | 28 |

The orders of the single orbits are:
- A8 roots, ±Δ(9,3) together, the 756 orbit, A7 roots and Δ(8,4): S × {±1} (725760 for S9, 80640 for S8);
- Δ(9,3), the 630, 72 and 28 orbits: S alone.

Further checks:
- 4_21 ∪ 2_41 (2400 points) gains W(E8).
- **Must fail, and did:**
  - 4_21 ∪ one S9-orbit of 2_41;
  - the A8 roots ∪ 2·(±Δ(9,3)), the same orbits at the wrong radius, which keep only 36 reflections.

**Controls** (scripts/s0_controls.py, data/s0_controls.log, FINAL ok, 11 checks):
- The 600-cell is the closure of A = perms(φ², φ², φ², φ, 0) under reflection in its own members, exact in Q(φ). It has 120 corners, which split under S5 as 20 + 20 + 20 + 30 + 30 = A, −A, C3, B, −B. S5 and one reflection generate order 14400.
- An ordinary orbit is not closed (must fail).
- The same index test reproduces the heptagonal result: for n = 4, 5, 6 only A_n itself (plus H4 for n = 4).
- **Note:** the order-divisibility test of the heptagonal study does not decide n = 7. B7, C7 and D7 pass it; the index test excludes them. For n = 6 both tests agree.

## Walls and Vacuus (scripts/s2_walls.py, data/s2_walls_E7.log FINAL ok 17 checks, data/s2_walls_E8.log FINAL ok 21 checks)

We use the definitions of #110 §2.
- A ridge's plate is its span through the centre.
- A plate is a full sheet, a shared sheet or a single fin.
- An orbit hull is of the heart kind if every plate is a full sheet, of the non-heart kind if every plate is a single fin, and of the inherited heart kind otherwise.
- The host's walls are its mirrors plus its cross walls (central hyperplanes parallel to a pair of opposite facets, not already mirrors).

Methods:
- **Host facets** (exact). Each host is one W(E)-orbit, so its normal fan coarsens the Coxeter fan, and every facet normal is a W-image of a fundamental weight. Each weight was tested exactly, and its W-orbit was generated exactly.
  - Result: 4_21 has 17280 7-simplices and 2160 7-orthoplexes; 2_41 has 17280 simplices and 240 copies of 2_31.
  - 2_31 has 576 6-simplices and 56 copies of 2_21; 3_21 has 576 simplices and 126 6-orthoplexes.
  - The ridge counts 207360, 144960, 4788 and 6048 match Wikipedia's pages on 4_21, 2_41, 2_31 and 3_21 (read 18 Nov 2026).
  - In the first run the expected value for 2_41 was entered as 7-orthoplexes. The check failed, and it was corrected to 2_31, by Coxeter's 2_k1 rule and the 2_41 page.
- **Orbit hulls** (exact). By the rearrangement inequality (Hardy, Littlewood and Pólya), the face of perms(a) that maximises c is fixed by the ordered level sets of c. Facets and ridges were therefore enumerated as all ordered partitions into 2 or 3 blocks.
  - Ranks are exact.
  - Every ridge lies in exactly 2 facets.
- **Plate normals** (certified). Each was found by SVD, recovered as an integer vector, and checked exactly: zero integer dot product with every ridge corner.
- **Controls:**
  - #110's Figure 1: the tetrahedron is non-heart with 6 plates; the octahedron is heart with 3 plates; the cuboctahedron is heart with 4.
  - Ordinary orbits must fall mostly on no wall. They did: E8 (7, 2, 0⁵, −4, −5)/3 has 4500 of 4509 plates on no wall, and E7 (5, 2, 0⁴, −3, −4)/4 has 1960 of 1968.
  - A rescaled hypersimplex must repeat its hidden verdict, and it did.

**Walls.**
- W(4_21) = 120 mirrors (36 from S9 + 84 hidden) + 9720 cross walls (8640 simplex pairs + 1080 orthoplex pairs) = **9840**.
- W(2_31) = 63 mirrors (28 + 35) + 316 cross walls (288 + 28) = **379**.
- Every facet line of 2_41 lies in W(4_21), and every facet line of 3_21 in W(2_31). So the smaller wall systems sit inside the larger ones:
  - W(2_41) = 120 + 8640;
  - W(3_21) = 63 + 288.

| solid | corners | ridges | plates (ridges per plate) | kind | S mirrors | hidden E mirrors | cross walls | no wall | verdict (host walls) |
|---|---|---|---|---|---|---|---|---|---|
| **E8, host 4_21** | | | | | | | | | |
| 4_21 itself | 240 | 207360 | 8760 (120 × 576, 8640 × 16) | heart | 36 | 84 | 8640 | 0 | hidden |
| A8 roots | 72 | 2286 | 9 (× 254) | heart | 0 | 0 | 9 | 0 | **hidden** |
| Δ(9,3) (and its negative) | 84 | 144 | 108 (36 × 2, 72 × 1) | inherited heart | 36 | 0 | 72 | 0 | **hidden** |
| 2_41 itself | 2160 | 144960 | 69240 (120 × 56, 69120 × 2) | heart | 36 | 84 | 0 | 69120 | partly |
| t₁,₆ (756) | 756 | 5562 | 1971 (9 × 182, 1962 × 2) | heart | 36 | 0 | 639 | 1296 | partly |
| stericated (630, each sign) | 630 | 2322 | 2322 (× 1) | non-heart | 36 | 0 | 576 | 1710 | partly |
| truncated (72, each sign) | 72 | 108 | 108 (× 1) | non-heart | 36 | 0 | 0 | 72 | partly |
| **E7, host 2_31** | | | | | | | | | |
| 2_31 itself | 126 | 4788 | 351 (63 × 12, 288 × 14) | heart | 28 | 35 | 288 | 0 | hidden |
| A7 roots | 56 | 1008 | 8 (× 126) | heart | 0 | 0 | 8 | 0 | **hidden** |
| Δ(8,4) | 70 | 112 | 56 (× 2) | heart | 28 | 0 | 28 | 0 | **hidden** |
| 3_21 itself | 56 | 6048 | 2079 (63 × 32, 2016 × 2) | heart | 28 | 35 | 0 | 2016 | partly |
| Δ(8,2) (each sign) | 28 | 84 | 84 (× 1) | non-heart | 28 | 0 | 0 | 56 | partly |

Readings:
- The root-orbit plates (9 and 8) are the hyperplanes "coordinate k equals the mean". These are the same kind of plate as C3's five in #110 Table 1. They are cross walls of the host, as C3's are.
- Δ(9,3)'s 72 single plates have normals in the S9-class (5, 2, −1⁷). These are the orthoplex-pair cross walls of 4_21: their normals point at corners of 2_41.
- Measured against their own shell's walls instead, the 2_41 orbits keep fewer:
  - the 630 orbits keep 36 + 504;
  - the 756 orbit keeps 36 + 9;
  - the 72 orbits keep 36.
- Measured against 3_21's walls, Δ(8,2) keeps 28.
- The orbits of 2_41 and 3_21 do not lie on their host's corners, so "partly hidden" reports wall coincidence only.

## Heptagon link (s1, exact)

The heptagonal group S7 = W(A6) sits inside W(A7) ⊂ W(E7), acting on the first seven of eight coordinates. The E7 roots split into five S7-orbits:

| count | seed (first seven \| last) |
|---|---|
| 42 | (1, 0⁵, −1 \| 0): the A6 roots |
| 7 | (1, 0⁶ \| −1) |
| 7 | (0⁶, −1 \| 1) |
| 35 | (1/2³, −1/2⁴ \| 1/2) |
| 35 | (1/2⁴, −1/2³ \| −1/2) |

In sum-zero R⁷ the heptagonal theorem holds: no hidden symmetry. One dimension up, S7 is no longer irreducible (6 + 1), and E7 contains it.

## Prior art and sources checked (18 Nov 2026)

- **Classical facts, credited:**
  - Gosset (1900) and Coxeter, *Regular Polytopes* (1948), for 4_21, 2_41, 2_31 and 3_21 (not opened; counts checked on Wikipedia);
  - Conway and Sloane, SPLAG, for E8 = A8 + glue [3], [6] and E7 = A7 + [4] (not opened);
  - Borel and de Siebenthal (1949), for subsystems of maximal rank; our index test is a short special case;
  - Humphreys, *Reflection Groups and Coxeter Groups*, for normal fans and stabilisers of fundamental weights (not opened);
  - Hardy, Littlewood and Pólya, for the rearrangement inequality.
- **Wikipedia, read 18 Nov 2026:**
  - "4_21 polytope" gives the 9-dimensional decomposition 72 + 84 + 84 ("similarly to the relation of the A8 lattice and E8 lattice"), with 207360 6-faces in its table. Its text says 259200, so the page is inconsistent; our exact count is 207360.
  - "3_21 polytope" gives the 56 corners as ±perms(−3, −3, 1⁶), which is ±Δ(8,2).
  - "2_41 polytope" gives the facets 240 2_31 + 17280 simplices and f₆ = 144960. Its coordinates are 16 + 1120 + 1024, not an A8 split.
  - "2_31 polytope": 4788 5-faces, 576 + 56 facets.
  - "E8 (mathematics)": E8 contains A8 (72 roots).

  So the splits 240 = 72 + 84 + 84 and 56 = 28 + 28 are known. 126 = 56 + 70 is the standard A7 glue.
- **Library** (reference library MANIFESTs, search terms E8/E7/Gosset/4_21/hypersimplex/Koca/Coxeter/root system/Wythoff). Hits, titles and abstracts only:
  - Koca, Al-Ajmi, Koca 2009, snub 24-cell from the E8 roots (arXiv:0906.2109);
  - Dechant 2017, "From the icosahedron to E8" (arXiv:1712.06436);
  - "The isomorphism of H4 and E8" (arXiv:2311.01486);
  - Deza and Shtogrin, Wythoffians (math/0407527);
  - Ozdes Koca et al. on A_n lattices (arXiv:1811.12176, 2604.10574).

  None splits 2_41 under S9, and none treats walls or Vacuus.
- The 2_41 split 2160 = 756 + 630 + 630 + 72 + 72, the classification of the hidden-symmetric unions, and all wall and Vacuus results are **not found in the sources checked**. We do not claim them as new. The theorem is a standard consequence of the classification. What is ours is its use as a hidden-symmetry test, and the fact that no orbit uses a hidden E mirror.

## Files

- `scripts/qlib.py`: exact helpers (shell enumeration, orbits, exact rank and null vectors, Weyl orbits).
- `scripts/s0_controls.py`: 600-cell control in Q(φ); containment theorem table.
- `scripts/s1_orbits.py`: shells, S-orbit splits, group orders, all unions, the S7 split.
- `scripts/s2_walls.py`: host facets and walls; orbit-hull Vacuus. Run as `s2_walls.py out.json 7` or `8`.
- `data/*.log` (each ends FINAL ok) and `data/*.json` (results, including plate classes by normal type).
- `data/concordance-patch.json`: proposed ledger entry.
- Runs on a compute host: s0 1 s, s1 21 s, s2 1 s (E7) and 61 s (E8).

## LEADS

1. **Cross walls only.** Find out why no S-orbit uses a hidden E mirror, and whether this holds for every S-orbit of every W(E)-orbit, for example the S9-orbits of 1_42 (17280 corners) and the S8-orbits of 1_32 (576 corners).
2. **Polars.** Following #110 §6, compute the duals of the 4_21 orbits (72, 84, 84). Test whether their intersection is the polar of 4_21 and whether their plates lie on its mirrors.
3. **Chambers.** Count the chambers cut by W(2_31) (379 walls), as #110 Theorem C did for the 360 walls of the 600-cell.
4. **Heptagonal picture.** Project the E7 S7-split (42 + 7 + 7 + 35 + 35) on the A6 Coxeter plane.
5. **E6 ⊃ A5 × A2.** E6 has no full-rank A6, but it is the next case of a hidden symmetry with a reducible S-action.
