# Twisted silence across groups and dimensions (15 Nov 2026)

Aim 2 (geometry gives laws). Follows the golden A4 mechanism study of the same day (Fable, `studies/2026-11-15-fable-golden-a4`), which proved the twisted-class silence theorem and applied it to 2I in the 600-cell. That study is credited for the theorem and for the quaternion form of the outer automorphism σ of 2I. This study runs the general search across groups and dimensions. The orbit map inside the 600-cell, 120-cell, 24-cell, snub and E8 belongs to the parallel study `2026-11-15-hidden-zeros-h4` and is not repeated here.

## Verdict

1. **General theorem.** The theorem holds for any compact group H, any finite subgroup G, any automorphism σ of G and any irreducible representation Π of H (§1). The proof is the same as Fable's. Sets on spheres arise in three ways:
   - the circle S¹ = SO(2) inside O(2);
   - S³ = SU(2);
   - the matrix spheres S^{n²−1}, which contain O(n).
2. **Where a genuine twist exists (classification, §2).** A twist gives something new only when ρ∘σ is not ρ times a 1-dimensional character. Among the finite irreducible reflection groups and their binary covers this happens only for the non-crystallographic ones, through Galois conjugation: I2(n) (n = 5 or n ≥ 7), H3 and H4. Weyl groups and 2T, 2O give only rotated ordinary classes or latitude slices. This was checked by computation for 2T and 2O: their twist groups are reducible on R⁴, and every class lies in one hyperplane or two parallel ones. The step "automorphisms of Weyl groups do not move the reflection character" is quoted from Bannai 1969 and Franzsen 2001 and was not re-read today.
3. **Only one genuinely new family on a sphere that is itself the group: 2I on S³.** Its twist group is the only irreducible one among all (G, σ) on S¹ and S³ (Σχ²/|G| = 1; all others give 2). The table of twisted classes (20, 20, 20, 30, 30) reproduces Fable's exactly:
   - full symmetry group of order 120;
   - X kills {1,2,5,7} and F kills {1,2,3,6}, unforced.

   The other cases add nothing new:
   - **Dihedral family:** reduces to an elementary cosine rule.
   - **H3:** reduces to 2I.
   - **W(H4) in S¹⁵:** gives new degree-3 silences (twisted-silent by the theorem), but whether a larger symmetry forces them is not yet tested.
4. **Criterion equals direct sums everywhere tested.** Every class gives the same answer both ways:
   - D_n: 12 values of n, every twist, modes ≤ 2n, closed-form criterion.
   - 2T, 2O, 2I: degrees ≤ 30, numerical block test against exact sums.

   Controls:
   - Ordinary classes show only the latitude/cosine zeros.
   - Wrong twists fail the automorphism test and the intertwining test.
   - In the dihedral family wrong twists give 552 criterion mismatches.
5. **Turning the dial (§5).** For the golden twist (A5 acting on R⁴ = the A4 picture), as the base point moves:
   - **Exact on both 1-dimensional strata, to degree 30.** The only points silent in two or more unforced degrees are the twisted classes X, −X, F, −F and antipodal points, where the odd degrees are forced. Every other special point on these circles is silent in exactly one degree.
   - **Faces (2-dimensional) and the interior (3-dimensional), degrees ≤ 12.** The located multi-silent points are isolated and Krawczyk-certified. All of them have exactly their defining silences and no extra ones. The search located 259 roots: 55 certified isolated points (47 distinct orbits), 105 on lower strata (edges and lines, treated exactly in 5.1), 97 on the antipodal circle (5.3) and 2 spurious (rejected by the direct sums). Classification log: `data/dial_check.log`.
   - **Law-giving coincidences** (more silences than the stratum's dimension allows) occur only at the twisted classes and on the antipodal circle (a,b,0,−b,−a), where −1 lies in the orbit.
6. **Inverse question (§6).**
   - On the circle the answer is closed-form.
   - For the golden twist, pattern {1,2,5,7} is realised by X and −X only (exact on the edges, numerical elsewhere). Pattern {1,2,3,6} is realised only by F and −F.
   - Two-degree patterns {1,2,a,b}, with a, b in 3..11, occur at isolated certified 60-point orbits. Some pairs are found only at X and F: (5,7) and (3,6).
7. **Prior art (§7).** The algebraic core is published: twisted class functions are spanned by twisted characters (Fel'shtyn–Troitsky 2017; classical for finite groups). The 20+20+20+30+30 split of the 600-cell under S5 is in Koca et al. 2011. Neither the silence theorem for harmonic sums nor its application to designs was found. The closest design paper is Hirao–Nozaki–Tasaka 2025, which covers whole groups 2T, 2O, 2I only.

## 1. The theorem in general form

**Setting.**
- H is a compact group, G ⊂ H a finite subgroup and σ an automorphism of G.
- The twisted class of x₀ is O = {a x₀ σ(a)⁻¹ : a ∈ G}. It is an orbit of the subgroup {(a, σa)} of H × H acting by x ↦ a x b⁻¹, so it is invariant under these isometries of H.
- For an irreducible unitary representation Π of H, the set O *kills* Π when Σ_{x∈O} Π(x) = 0, that is, when every matrix coefficient of Π sums to zero over O.

**Theorem (twisted silence; Fable's proof, H general).** Let x₀ ∈ G. Then O kills Π if and only if χ̃_π(x₀) = tr(π(x₀) J_π⁻¹) = 0 for every σ-stable irreducible constituent π of Π|_G. Here J_π intertwines π∘σ with π. Constituents that are not σ-stable never contribute. A union of twisted classes O₁, …, O_m kills Π if and only if Σ_i |O_i| χ̃_π(O_i) = 0 for every σ-stable π.

**Proof.** S = Σ_a Π(a)Π(x₀)Π(σa)⁻¹ preserves every G-isotypic block, because all three factors do (σ(a) ∈ G). On a block of type π it intertwines π∘σ with π. Schur's lemma then gives zero unless π is σ-stable, and c·J_π if it is. The trace against J_π⁻¹ gives c = |G| χ̃_π(x₀)/dim π. ∎

**Base point off the group (x₀ ∉ G).** The same sum is the projection of Π(x₀) onto the twisted intertwiners. O kills Π if and only if every twisted-invariant matrix coefficient of Π vanishes at x₀. On spheres this is Sobolev's / Goethals–Seidel's criterion: an orbit kills degree k if and only if every invariant harmonic of degree k vanishes at the base point. The extended twisted character x ↦ tr(Π(x) J⁻¹) is such an invariant harmonic. So the theorem at x₀ ∈ G says exactly when the group points lie on the zero sets of these invariants.

**On spheres.**
- **S¹:** H = O(2), with Π running over the 2-dimensional irreducibles ρ_k. Matrix coefficients on the rotation circle and on the reflection circle are the Fourier modes k.
- **S³:** H = SU(2) and Π = V_k = Sym^k C², so harmonic degree k corresponds to V_k (Peter–Weyl).
- **Matrix spheres S^{n²−1} ⊃ O(n)** (Frobenius norm): a degree-k harmonic restricted to O(n) lies in the span of matrix coefficients of the O(n)-irreducibles of polynomial degree ≤ k with the same parity. The theorem governs each of these. A set killing all of them kills degree k, but the converse is not automatic. Here signatures are therefore computed directly (§3.3).

The algebraic core is Fel'shtyn–Troitsky's Lemma 5.1 (2017): twisted class functions are spanned by the twisted characters Tr(S ρ(g)). Our step is the restriction of an H-representation to G, combined with that lemma. It is credited at that point.

## 2. Where a twist can give something new (classification)

Let ρ be the defining representation of G ⊂ O(n). The twist group acts on End(V) by ρ ⊗ (ρ∘σ)*.

- **(a) ρ∘σ ≅ ρ.** Then σ is conjugation by an element n of the normaliser, and a x₀ σ(a)⁻¹ = (a (x₀n) a⁻¹) n⁻¹. The twisted class is an ordinary conjugation orbit (in G⟨n⟩), moved by an isometry. This covers Weyl groups with their diagram automorphisms and 2T with its outer automorphism; 2T is computed.
- **(b) ρ∘σ ≅ ρ ⊗ λ, with λ a 1-dimensional character ≠ 1.** Then ρ ⊗ (ρσ)* contains λ̄, the identity direction is an eigenline, and every class lies in the two hyperplanes tr(X) = ±c: a latitude pair. This covers 2O (here Galois √2 ↦ −√2 *is* a ↦ ε(a)a), central twists w ↦ w·z^{ℓ(w)} of Weyl groups with −1, and W(E7) w ↦ det(w)w. The silences are classical latitude zeros. Computed for 2O: the 8-point classes kill 2, unforced by their full symmetry (order 48), and lie at w = ±1/2, where the latitude factor of degree 2 vanishes.
- **(c) ρ∘σ ≇ ρ ⊗ λ for every λ.** Then χ∘σ ≠ λχ. For a reflection group whose automorphisms send reflections to reflections, ρ∘σ is again a reflection representation. It is therefore a Galois conjugate ρ^γ (the reflection representations of a finite Coxeter group are the Galois conjugates of the geometric one), so the character field must be larger than Q.
  - Weyl groups have rational characters. Their automorphisms are inner × graph × central (Bannai 1969; Franzsen 2001; quoted from memory), so they fall under (a) or (b).
  - What remains: **I2(n) (n = 5, n ≥ 7), H3, H4**, through Galois conjugation of Q(cos 2π/n) or Q(√5).
  - For the binary covers in SU(2):
    - 2D_n: case (c), but ρ₁ ⊗ ρ_m = ρ_{1+m} ⊕ ρ_{1−m} is reducible, so classes lie on great circles. Reduction to S¹ was checked for every class, n ≤ 30.
    - 2I: case (c) with ρ ⊗ ρσ irreducible (Σχ²/|G| = 1, checked exactly). This is the only case where the twisted action on the group sphere is irreducible.
    - 2T, 2O: cases (a) and (b) (Σχ²/|G| = 2).

**Proved here:** (a), (b), the reduction for 2D_n, and the irreducibility counts.

**Quoted:**
- the Bannai/Franzsen description of Aut(W);
- the fact that reflection representations are Galois conjugates of the geometric one.

Both should be read in the source before publication.

## 3. Computations (all exact unless marked)

Scripts are in `scripts/` and logs in `data/`. Every job printed CHECK lines and ended with a conditional FINAL ok.

**3.1 Dihedral D_n on S¹.** `tw_dihedral.py` (pure Python, integer cyclotomic arithmetic). Log `data/tw_dihedral.log`: 1498 CHECK OK, 0 FAIL.
- Coverage: n = 5, 7, 8, 9, 10, 12, 15, 16, 18, 20, 24, 30; every twist σ_m (m a unit, up to ±); every twisted class.
- Result: the closed-form criterion equals the direct sums for every mode up to 2n (the period is n).
- Formula: the twisted class of r^t is {r^{±t + dj}} with d = gcd(n, m−1). Its mode k vanishes unless (n/d) | k and cos(2πkt/n) ≠ 0.
- Binary dihedral 2D_n on S³ (same n): every class lies on one great circle, and S³ degree k is killed exactly when the circle modes k, k−2, … vanish (all classes checked).
- Wrong twist r ↦ r^m with gcd(m, n) > 1: not bijective, 552 criterion mismatches.

**3.2 Binary polyhedral groups on S³.** `tw_binary.py`. Log `data/tw_binary.log`: 68 CHECK OK, 0 FAIL.
- **Exact direct sums** to degree 40.
- **Numerical criterion** to degree 30:
  - isotypic blocks come from a Hermitian central element, and the same label is matched at every k;
  - σ-stability comes from the twisted central element;
  - block zero tolerance is 1e-7.
- **Theorem content tested on every class:**
  - (i) unstable blocks are zero;
  - (ii) the block status depends on (π, class), never on k;
  - (iii) the prediction equals the direct sums.

  It passed for all 38 classes of 2T, 2O, 2I under σ = id and σ outer.
- **Forced degrees:** exact, (1/|G|)Σ U_k(Re a) U_k(Re σa).
- **Full symmetry of each 4-dimensional set:** Gram backtracking, with forcing by it from characters (numerical, rounded to integers).

**3.3 Matrix spheres.** `tw_matrix.py`. Log `data/tw_matrix.log`: 0 FAIL.
- **Sets covered:** W(H3) in S⁸; the rotation group W⁺(H4) = (2I×2I)/±1 and W(H4) in S¹⁵. Elements are pairs of 2I indices with a conjugation flag.
- **Exact quantities:**
  - traces tr(x↦axb) = 4 Re a Re b and tr(x↦a x̄ b) = −2⟨a,b⟩;
  - Gegenbauer sums with λ = 7/2 and λ = 7;
  - forced degrees from the power sums tr(g^m) tr(σ(g)^{−m}) and Newton's identities.
- **Twists:** id; Galois on both factors; for W⁺(H4) also Galois on the left factor only. The left-only twist is an automorphism of W⁺(H4) but not of W(H4); the control confirms it is rejected there.

**3.4 Dial.**
- `dial_a5.py` covers the golden twist (§5).
- `ord_dial.py` is the ordinary control (§5.4).

## 4. Signature table (the "sonar" signatures; degrees ≤ 30)

The forced degrees are those with no invariant harmonic for the twist group. "Unforced" means killed although forced by nothing.

| family | set (size) | silence signature, k ≤ 30 | forced | unforced | status |
|---|---|---|---|---|---|
| 2I, σ outer (S³) | X, −X: perms (φ²,φ²,φ²,φ,0) (20) | 1, 2, 5, 7 | 1, 2 | **5, 7** | twisted-silent; full symmetry 120 |
| 2I, σ outer | F, −F: perms (φ²,φ²,1,1,0) (30) | 1, 2, 3, 6 | 1, 2 | **3, 6** | twisted-silent; full symmetry 120 |
| 2I, σ outer | R: A4 roots (20, antipodal) | 1, 2, all odd | 1, 2 | odd | forced by −1 (full symmetry 240) |
| 2I, σ = id | 12-classes (cos φ/2) | 4 | none | 4 | latitude zero |
| 2I, σ = id | 20-classes (cos ±1/2) | 2, 5 | none | 2, 5 | latitude zero |
| 2I, σ = id | 30-class (equator) | all odd | none | odd | antipodal slice |
| 2O, σ outer (= Galois √2) | 8-point classes (w = ±1/2) | 1, 2 | 1 | 2 | latitude pair; full symmetry 48 |
| 2O, σ outer | 12, 6, 2-point classes | 1 and all odd | 1 | odd | antipodal |
| 2T, σ outer | 6-point classes | 3 | none | 3 | one hyperplane (octahedron slice) |
| D16, σ₇ | rectangle at ±22.5°, ±157.5° (4) | 1,3,4,5,7,9,11,12,13,15,…,28,29 | k ≢ 0 mod 2 | 4, 12, 20, 28 | cosine rule, cos 4α = 0 |
| D24, σ₇ | ±15° + 120°j (6) | 1,2,4,5,6,7,8,10,11,13,14,16,17,18,19,20,22,23,25,26,28,29,30 | k ≢ 0 mod 3 | 6, 18, 30 | cosine rule |
| D24, σ₁₁ | rectangle at ±15°, ±165° (4) | 1,3,5,6,7,9,…,17,18,19,…,29,30 | odd | 6, 18, 30 | cosine rule |
| W(H3), σ Galois (S⁸) | classes of size 10, 20, 30 | 1 | 1 | none | nothing new (reduces to 2I) |
| W⁺(H4), σ Galois both (S¹⁵) | 600 ×4, 900 ×2 | 1, 2, 3 | 1, 2 | **3** | candidate; full symmetry not tested |
| W⁺(H4), σ Galois both | 200, 400 ×2, 600 ×2 | 1, 2, 3, all odd | 1, 2 | 3, odd | odd part antipodal |
| W⁺(H4), σ Galois both | 400 ×2 | 1, 2 | 1, 2 | none | |
| W(H4), σ Galois (S¹⁵) | 1200 ×2, 900 ×2 | 1, 2, 3 | 1, 2 | **3** | candidate |
| W(H4), σ Galois | 200, 800, 1200, 1800 | 1, 2, 3, all odd | 1, 2 | 3, odd | odd part antipodal |
| W(H4), σ Galois | 60 ×2, 400 ×2, 1200 ×2, 1440 ×2 | 1, 2 | 1, 2 | none | |
| W⁺(H4), Galois left only | 30 ×2, 360 ×4 | 1, 3 | 1 | 3 | candidate |
| W⁺(H4), Galois left only | 600 ×2 | 1, 2, 3 | 1 | 2, 3 | candidate |
| W⁺(H4), Galois left only | 400 ×2 | 1, 2 | 1 | 2 | candidate |

The full per-class lists are in the logs, on the lines starting `SIG`. Ordinary classes of the dihedral groups (two points ±α) show the same cosine-rule zeros: 2-point pairs at α with cos kα = 0.

## 5. Turning the dial (golden twist; ordinary control)

Model: A5 acting on R⁴ = {x ∈ R⁵ : Σx = 0} by even permutations. This is the twisted action of 2I; the dimension counts below match the harmonic Molien series (1+t¹⁰)/((1−t³)(1−t⁴)(1−t⁵)) exactly. The invariant harmonics h_k come exactly from the centred power sums and the Vandermonde: dimension 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 2, 3 for k = 1…12. The silence locus L_k is the common zero set of the h_k:
- a surface for k = 3…7 (one equation);
- a curve for k = 8, 9, 11;
- points for k = 10, 12.

The orbit-type strata (stabiliser in A5) are:
- the 60-point generic stratum (3-dimensional);
- the faces x_i = x_j (2-dimensional);
- the C3 circle (a,a,a,b,c), which contains X;
- the C2 circle (a,a,b,b,c), which contains F;
- the lines of the 5- and 10-point orbits.

A point is *law-giving* when it carries more independent silences than its stratum's dimension. On a circle that means two or more unforced silences.

**5.1 Edges, exact to degree 30.** F_k restricted to each circle is a polynomial over Q. A gcd-free basis of all F_k with k ≤ 30, with real roots counted by Sturm sequences, gives every special point and its exact signature.

| circle | special points (minimal polynomial degree, real roots) | signature ≤ 30 |
|---|---|---|
| C3 (a,a,a,b,c) | s² − 3s + 1 (2): **X, −X** | 1, 2, **5, 7** |
| | s = 0: A4 root (antipodal) | 1, 2, all odd |
| | degree 4 (2 real) | 1, 2, 4 |
| | degree 6 (2 real) | 1, 2, 6 |
| | degree 4 (4 real) | 1, 2, 7 |
| C2 (a,a,b,b,c) | s² − 5 (2): **F, −F** | 1, 2, **3, 6** |
| | s = ∞: (1,1,−1,−1,0) (antipodal) | 1, 2, all odd |
| | degree 4 (2 real) | 1, 2, 4 |
| | degree 4 (2 real) | 1, 2, 6 |
| | degree 6 (2 real) | 1, 2, 7 |

On both circles, degrees 3 and 5 and every degree ≥ 8 are silent only at the twisted classes and the antipodal points. Elsewhere each degree from 4 to 7 (and 3 on C2, only at F) is silent at isolated irrational points, one degree at a time. Turning the dial along an edge, silences switch on singly. The double silences appear exactly at the 600-cell points.

Figure: `figs/dial_edges.png`.

**5.2 Faces and interior, degrees ≤ 12.** Every square system (as many equations as the stratum's dimension) built from the h_k was solved by batched Newton from 300 starts. Each root was certified by a Krawczyk test in exact rational interval arithmetic: a unique zero in a box of radius 10⁻⁸. The signatures for k ≤ 12 were then certified, with nonzero meaning that some h_k interval excludes 0. Extra zeros up to degree 30 were checked numerically.

Result:
- **259 located roots.** They are:
  - 55 Krawczyk-certified;
  - 99 on the edge circles or the 5- and 10-point lines, plus 6 converging there within 5·10⁻³ (all treated exactly in 5.1);
  - 97 on the antipodal circle (5.3);
  - 2 false Newton convergences, rejected by the direct sums.
- **The certified generic orbits carry exactly their defining silences, never an extra one** (k ≤ 12 certified, k ≤ 30 numerical).
  - On the faces: single silences of degree 8, 9, 10, 11 (dimension-2 equations); pairs (3,4), (4,5), (4,6)×2, (4,7), (5,6)×3, (6,7)×3.
  - In the interior: pairs (4,9), (4,11), (5,8), (5,9), (5,11), (6,8), (6,9)×2, (6,11), (7,8)×3, (7,9)×2, and degree 10 alone.
  - No generic interior point killed three of the degrees 3…7 together. Those triples were found only on the antipodal circle.
  - The pairs (3,5), (3,6), (3,7) and (5,7) were found only at lower-strata points: X, F and the roots.
- **Not exhaustive.** Newton search cannot prove that no other root exists. Proving that would need elimination (lead 4).

Figures: `figs/dial_face_loci.png` (L3…L7 on a face) and `figs/dial_chamber_points.png`.

**5.3 The antipodal circle.** The points (a, b, 0, −b, −a) satisfy −x = (15)(24)·x, with (15)(24) ∈ A5. Their orbits are therefore antipodal and kill every odd degree, which is forced by −1. On this circle, extra even silences sit at certified isolated points (degree 4 at (0.6661, 0.2374), degree 6 at (0.6015, 0.3717)). Newton systems built from odd degrees are singular there, which is why those located roots are not certified; they are explained, not new.

**5.4 Ordinary control.** `ord_dial.py` (numerical; control: the 12-class at w = φ/2 kills exactly degree 4; FINAL ok). Ordinary classes of 2I are latitude slices x = (w, √(1−w²) n), and the dial is w ∈ [−1, 1] for six axes n (vertex, face, edge and three random), k ≤ 20.

Ordinary classes are *not* silent only at isolated points:
- **w = ±1/2:** degrees 2 and 5 together, for every axis n, generic ones included. This is a whole 2-dimensional family of 60-point orbits. The reason is the latitude: the icosahedral orbit of n kills the spherical parts l = 1…5, so only the l = 0 factor is left, and that factor vanishes for k = 2 and k = 5 at w = 1/2.
- **w = 0:** all odd degrees on the three axes (antipodal equator); 1 to 13 on generic n.
- **Elsewhere:** 8 single-silent latitudes per axis.

So the ordinary dial gives multi-silence only in families, forced by the latitude structure. The twisted dial gives it only at isolated, overdetermined points: the 600-cell classes. That is the contrast DICTO asked to see.

**5.5 Other dial settings.** Each setting of the dial is a different (group, twist):
- 2T and 2O outer twists: latitude families; every silence is the latitude factor U-type zero.
- Dihedral σ_m: the cosine rule, with one 1-parameter family per twist; silences are isolated in α and appear in arithmetic progressions.
- W⁺(H4) with three twists (id, Galois both, Galois left): signatures in §4. The silences change from all-odd (antipodal) to {1,2,3} as the twist turns.

## 6. Inverse question: which sets have a prescribed silence pattern

- **Circle (any dihedral orbit {±α + 2πj/N}).** The pattern is {k : N ∤ k} ∪ {k = cN : cos(cNα) = 0}. A prescribed extra silence at k = cN therefore fixes α ∈ {(2l+1)π/(2cN)}. Every such α kills the whole progression c(2j+1)N and nothing else. A pattern with extra silences that are not one odd progression is impossible on the circle.
- **Golden twist, S³:**
  - {1,2,5,7}: exactly X and −X on the C3 circle (exact). In the faces and interior, no generic point has (5,7) without lying on the circle (numerical, 300 starts).
  - {1,2,3,6}: F and −F (exact on the C2 circle; the face search finds only F).
  - {1,2,a,b} for (a,b) ∈ {(3,4), (4,5), (4,6), (4,7), (5,6), (6,7)}: isolated 60-point orbits on the faces.
  - {1,2,a,b} for (a,b) ∈ {(4,9), (4,11), (5,8), (5,9), (5,11), (6,8), (6,9), (6,11), (7,8), (7,9)}: isolated 60-point orbits in the interior.
  - {1,2,10}: three certified interior orbits.

  The list is from the certified run (`data/dial_a5.log`, TABLE certified …). Every multi-silent orbit off the 600-cell classes has exactly the two (or, for degrees 8–11, one) defining silences.
- **Inside the 600-cell:** see the parallel hidden-zeros study.

## 7. Prior art (free sources only; full list of what was checked)

Opened and read in part:
- **Fel'shtyn & Troitsky,** arXiv 1704.09013 (2017), Theorem 4.3 and Lemma 5.1. The number of twisted classes equals the number of σ-fixed irreducibles, and the twisted characters span the twisted class functions. This is the algebraic core of §1, credited there.
- **de la Harpe & Pache,** "Cubature formulas, geometrical designs, reproducing kernels, and Markov operators", arXiv math/0502312 (2005). Covers classical orbit designs (every H4 orbit is an 11-design; Salihov's 19-design); nothing twisted.
- **Hirao, Nozaki & Tasaka,** "Spherical designs for finite quaternionic unit groups …", arXiv 2507.01358 (2025). Gives the harmonic strength of the whole groups 2T, 2O, 2I and their cosets only: no subgroup orbits, no twisted classes, no Galois.
- **Mohammadpour & Waldron,** arXiv 2308.02499 (complex designs from orbits, harmonic Molien series): nothing twisted.
- **Ehler et al.,** "Hybrid spherical designs", arXiv 2502.07720: orbits at roots of invariants (the Goethals–Seidel mechanism); nothing twisted.
- **Koca, Ozdes Koca & Al-Ajmi,** arXiv 1106.2957 (2011): the 600-cell splits under W(A4) into 20+20+20+30+30. This is prior art for the decomposition, not for the silence.
- **Wikipedia** "Kepler–Poinsot polyhedron" and "Grand antiprism": no Galois or design content.

Seen as abstract, title or citation only:
- Fel'shtyn–Troitsky arXiv 1204.3175, 0909.1710, math/0606179, math/0606764, math/0606161, 2210.00591; arXiv 2603.01679 (bi-twisted classes).
- Lemaire, arXiv 1007.3576 (twisted characters).
- Shintani descent / norm map: arXiv 1205.6448, 0810.0787, math/0502180; Shelstad, Pacific J. Math. 110 (1984) (swap automorphism of G×G).
- Soto-Andrade & Yáñez, arXiv 1303.4800.
- Goethals & Seidel 1981 (paid; known through citations).
- Bannai, J. Math. Soc. Japan 36 (1984) (free on Project Euclid; to read).
- Sobolev's theorem through arXiv 1204.1779 and 1102.4891.
- Hardin & Sloane, arXiv math/0207211, and Sloane's design tables (title).
- Bannai–Okuda–Tagami, arXiv 1308.5101, 1507.05373, EJC v24i2p14 (designs of harmonic index t).
- arXiv 1912.07151, 2508.12580, 2609.25032, 2405.19353, 0712.1939, 1506.08414: nothing relevant.
- Monson 2024 (preprints.org 202408.0116; title).
- "From Pentagons to Pentagrams" (blog, Galois conjugation of Kepler–Poinsot solids).
- Conway & Smith, *On Quaternions and Octonions*: not accessible; the ±[I×Ī] notation was not confirmed.

Searches with no hits:
- "twisted conjugacy class" spherical design (only the algebraic-group sense of "spherical");
- spherical design "Galois conjugate" icosahedral orbit;
- 600-cell A5 20/30-point orbits design;
- orbit design higher strength than group (MathOverflow);
- twisted diagonal subgroup SU(2)×SU(2) design.

Quoted from memory, not re-read today:
- Bannai 1969 and Franzsen 2001 (automorphisms of Coxeter groups);
- the Galois-conjugate description of reflection representations.

**What is known:**
- twisted characters and twisted classes as algebra;
- orbit designs and the invariant-zero mechanism;
- the 600-cell's S5 decomposition.

**Not found:**
- the silence theorem for harmonic (matrix-coefficient) sums over twisted classes;
- its use to explain unforced design zeros;
- the signatures {1,2,5,7} and {1,2,3,6};
- the classification in §2.

## Leads

1. **W(H4) degree-3 silences in S¹⁵.**
   - Compute the full symmetry groups of the 600- to 1200-point classes.
   - Find which O(4)-irreducible carries the invariant cubic.
   - Test whether the twisted character explains the zero.
2. **Read the sources quoted in §2** (Bannai 1969 or Franzsen 2001; the Galois description of reflection representations) and write the classification as a proposition.
3. **Turn the dial for W⁺(H4) in S¹⁵** (base point in O(4) off the group) to see whether the degree-3 silences form families.
4. **Extend the face and interior search** past degree 12, or certify the absence of generic (5,7) and (3,6) points by elimination (resultants) rather than by Newton starts.

## Files

- `scripts/tw_dihedral.py`, `tw_binary.py`, `tw_matrix.py`, `dial_a5.py`, `ord_dial.py`
- `data/*.log`, `data/dial_a5_edges.json`, `data/dial_a5_points.json`
- `figs/dial_edges.png`, `figs/dial_face_loci.png`, `figs/dial_chamber_points.png`
