# A402191 and the Vacuus of the permutohedron, every dimension (24 Nov 2026)

DICTO · study for row V of the V SF A project. A402191 (approved, OEIS) counts the hyperplanes through the centre of the (n−1)-dimensional permutohedron spanned by its ridges. This is DICTO's Vacuus (#110, edge-plate definition: one plane through the centre O and each edge, equal planes merged; in dimension d the edges become the ridges, the faces of dimension d − 2, as in #105). So A402191(n) is the number of Vacuus plates of the permutohedron, in every dimension.

**Conclusion.** Proved in every dimension: each Vacuus plate of the permutohedron has the explicit equation of Theorem A, and the plates number A402191(n). The plates in centred coordinates are of two kinds: those with two values, which are hyperplanes of the resonance (all-subset) arrangement (all of them for n odd, the even–even half for n even), and those with three values, which lie in no named arrangement we found. No plate is a mirror x_i = x_j of the type-A arrangement (n ≥ 3). For the type-B permutohedron with any values the same method gives a closed count (Theorem B). For the uniform one (truncated cuboctahedron in 3D) the count is (5^n − 2·3^n + 1)/2, and every plate carries exactly one ridge and its opposite. In 3D the B count is 36 and the H count is 90 (exact). The Vacuus is not a simplicial arrangement (A, n = 4: 176 regions, 624 wall incidences instead of 3·176; n = 5 and uniform B3 likewise). The construction itself (the hyperplanes through the origin spanned by the codimension-2 faces) was studied by Cellini and Marietti (2014) for root polytopes, not for permutohedra (see Sources).

## 1. Setting

Π_n = conv{permutations of (1, …, n)} lies in the hyperplane Σx = n(n+1)/2 and has dimension n − 1. Centre O = ((n+1)/2, …). Write y = x − O, so y lies in V₀ = {Σy = 0}. A linear form w·y on V₀ is unchanged when a multiple of (1, …, 1) is added to w. So a hyperplane of V₀ through O is a vector w taken up to scale and up to adding multiples of 1.

Faces (classical; Ziegler, Lectures on Polytopes, Example 0.10): facets F_S ↔ proper nonempty S ⊂ [n], F_S = Π_n ∩ {Σ_S y = −|S|(n−|S|)/2} (the positions S hold the |S| smallest values; Rado 1952 for the inequalities). Ridges ↔ ordered partitions (B₁, B₂, B₃) of [n] into three nonempty blocks, of sizes (a, b, c). The ridge is F_{B₁} ∩ F_{B₁∪B₂}.

## 2. The pencil lemma (any polytope)

**Lemma P.** Let Q be a polytope with O in its interior, and let R = F₁ ∩ F₂ be a ridge, F_i ⊂ {u_i·y = h_i} (h_i ≠ 0 because O is interior). Then the Vacuus plate of R is {(h₂u₁ − h₁u₂)·y = 0}.

*Proof.* The form vanishes at O and, on R, equals h₂h₁ − h₁h₂ = 0. It is not zero, because u₁ and u₂ are independent (two different facets). R has dimension d − 2 and O is not in aff R (O is interior), so R and O span exactly one hyperplane, and it is this zero set. ∎

So the plate of a ridge is the member of the pencil of its two facet hyperplanes that passes through O. Lemma P gives the normal at once from the facet data, in any dimension and for any polytope.

## 3. Theorem A (type A, every n ≥ 3)

**Theorem A.** (i) The Vacuus plate of the ridge (B₁, B₂, B₃) of Π_n is

  P(B₁, B₂, B₃) = { y ∈ V₀ : c(a+b)·Σ_{i∈B₁} y_i + a(b+c)·Σ_{i∈B₃} y_i = 0 }.

(ii) Two ridges have the same plate exactly when they are equal or reverses (B₃, B₂, B₁) of each other, or when both have equal outer sizes (a = c) and the same pair {B₁ ∪ B₃, B₂} up to order. (iii) The number of plates is A402191(n):

  a(n) = Σ_{a<c, a+b+c=n, a,b,c ≥ 1} n!/(a! b! c!) + T(n),  T(n) = 2^{n−1} − 1 (n odd), 2^{n−2} − 1 (n even),

and in closed form a(n) = (3^n − 3·2^n + 3 − A_n)/2 + T(n), A_n = c_n − 1 − [n even]·C(n, n/2), with c_n the central trinomial coefficient (A002426). (iv) The plates with a = c are exactly the resonance hyperplanes Σ_{i∈S} y_i = 0, i.e. Σ_{i∈S} x_i = |S|·(n+1)/2, for those splits {S, [n]∖S} with a part of even size. For n odd that is every resonance hyperplane of V₀ (2^{n−1} − 1 of them). For n even it is the 2^{n−2} − 1 with both parts even. The plates with a ≠ c have a normal with three distinct values and are not resonance hyperplanes. (v) For n ≥ 3 no plate is a mirror x_i = x_j of the type-A (braid) arrangement.

*Proof.* (i) Apply Lemma P with u₁ = 1_{B₁}, h₁ = −a(b+c)/2, u₂ = 1_{B₁∪B₂}, h₂ = −(a+b)c/2. Up to the factor −2 the normal is (a+b)c·1_{B₁} − a(b+c)·1_{B₁∪B₂}. Adding a(b+c)·1 gives w = c(a+b)·1_{B₁} + a(b+c)·1_{B₃}.

(ii) The normal w is 0 on B₂, c(a+b) > 0 on B₁ and a(b+c) > 0 on B₃. The two positive values are equal exactly when a = c. Scaling and adding a constant (w ↦ λw + μ1) keeps the number of distinct values, and keeps which level is the middle one. If a ≠ c, the three level sets are therefore read off the plate: B₂ is the middle level, and {B₁, B₃} are the outer two. Exchanging B₁ and B₃ gives the same w: the formula is symmetric under (a, B₁) ↔ (c, B₃). This is the reversed ridge, the image of R under y ↦ −y, as Π_n is centrally symmetric. So a ≠ c plates ↔ ridges up to reversal, and no a ≠ c plate equals an a = c plate. If a = c, w = a(a+b)·1_S with S = B₁ ∪ B₃. Modulo 1 and scale this is the class of 1_S ≡ −1_{[n]∖S}, which determines exactly the unordered pair {S, B₂}.

(iii) The first sum counts the ridges with a < c (one of each reverse pair). The a = c plates are indexed by unordered pairs {S, T}, S ⊔ T = [n], both nonempty, with a part of even size (≥ 2, automatically): when n is odd exactly one part of each pair is even, giving 2^{n−1} − 1; when n is even both parts have the same parity, so we need even–even, giving (2^{n−1} − 2)/2 = 2^{n−2} − 1. The closed form: ridges = 3^n − 3·2^n + 3 (A001117), and the a = c ridges are the central trinomial sum c_n minus its terms with a = 0 or b = 0.

(iv) As in (ii): the a = c plates are 1_S, and the conditions are those of (iii). A three-valued class has no representative with only the values 0, 1.

(v) The class of e_i − e_j: λ(e_i − e_j) + μ1 must equal some w, which is ≥ 0, takes the value 0 on B₂ ≠ ∅, and is positive elsewhere. μ = 0 gives mixed signs. μ = λ > 0 gives the values 2λ on {i}, 0 on {j} and λ on the other n − 2 positions. So B₂ = {j}, and (B₁, B₃) = ({i}, rest) or (rest, {i}). Then w is 2(n−2) on B₁ and n−1 on B₃ (or n−1 on the rest and 2(n−2) on {i}), and the ratio 2 : 1 would need 2(n−2) = 2(n−1). That is impossible (for n = 3 the a = c case needs 2λ = λ, also impossible). μ = −λ is the same with signs reversed. ∎

**On the mirrors of the full symmetry.** −σ (σ ∈ S_n) is a reflection of V₀ only when σ is an involution with k transpositions and f fixed points with k + f = 2, i.e. n = 3 (σ a transposition) or n = 4 (σ = (12)(34)). Its mirror is a resonance hyperplane. So the plates lying on mirrors of S_n × {±1} are: n = 3, all 3 (the hexagon's long diagonals); n = 4, the 3 two-valued plates (#105's 3 octagon slices, the coordinate mirrors of the truncated octahedron); n ≥ 5, none.

**Check (exact, independent of the proof).** `scripts/a_vacuus.py` builds Π_n from its vertices, finds facets and ridges by exact rank (not from the ordered-partition description), and solves for each plate by exact elimination. For n = 3, …, 8 every ridge's plate equals the formula (i), and the counts equal both the OEIS formula and the closed form: 3, 15, 65, 225, 770, 2443. In the same runs every two-valued plate is a resonance hyperplane, no three-valued plate is one, and no plate is a type-A mirror. The two-valued plates number 3, 3, 15, 15, 63, 63 out of 3, 7, 15, 31, 63, 127 resonance hyperplanes. Plates carry 2, 6, 20 ridges (n = 7) or 2, 12, 22 (n = 8). `data/a_vacuus.json`. (#105 Theorem 3 already counted n = 3, …, 9; the recount is the control.)

## 4. Theorem B (type B, any values)

Let λ₁ > λ₂ > … > λ_n > 0 and P(λ) = conv{signed permutations of λ} (the B_n permutohedron; uniform omnitruncated n-cube when λ_k = 1 + (n−k)√2). Write Λ(s) = λ₁ + … + λ_s and N(s, d) = λ_{s+1} + … + λ_{s+d}. Facets ↔ nonempty signed subsets (S, ε): Σ_S ε_i x_i ≤ Λ(|S|). Ridges ↔ signed chains S₁ ⊊ S₂ (signs ε on S₂), |S₁| = s ≥ 1, D = S₂ ∖ S₁, |D| = d ≥ 1: 5^n − 2·3^n + 1 ridges. This is the face structure of the orbit polytope of a generic point of a reflection group (faces ↔ cosets of standard parabolic subgroups; Björner–Brenti, Combinatorics of Coxeter Groups), checked by brute force for n = 3, 4.

**Theorem B.** (i) The plate of the ridge (S₁ ⊂ S₂, ε) has normal N(s,d)·ε·1_{S₁} − Λ(s)·ε·1_D (zero off S₂). (ii) The number of plates is

  Σ_{s,d ≥ 1, s+d ≤ n, Λ(s) ≠ N(s,d)} n!/(s! d! (n−s−d)!)·2^{s+d−1}  +  Σ_{t ∈ E} C(n, t)·2^{t−1},

where E is the set of t for which some s < t has Λ(s) = N(s, t−s). (iii) If no such equality holds (generic values; in particular the uniform polytope for every n), the count is (5^n − 2·3^n + 1)/2, and every plate carries exactly one ridge and its opposite. (iv) No plate is a mirror (x_i = 0, x_i = ±x_j) of B_n.

*Proof.* (i) Lemma P with h₁ = Λ(s), h₂ = Λ(s+d), u₁ = ε1_{S₁}, u₂ = ε1_{S₂}: the normal is Λ(s+d)ε1_{S₁} − Λ(s)ε1_{S₂}, as stated. (ii) The normal has support S₂, magnitude p = N(s,d) on S₁ and q = Λ(s) on D, both > 0, and an arbitrary sign pattern (given by ε). Suppose p ≠ q. The two magnitude levels are then read off the plate, and so is the sign pattern up to a global sign. Only one assignment of the levels can fit: exchanging the roles of S₁ and D would need N(s,d)·N(d,s) = Λ(s)·Λ(d). With Λ(s) + N(s,d) = Λ(d) + N(d,s) = Λ(s+d), this forces N(s,d) = Λ(d), which is impossible, since λ_{s+i} < λ_i. So the plate determines the ridge up to the global sign, which is the opposite ridge. If p = q, the normal is a signed 0/±1 vector on S₂, and all ridges with the same support, the same signs up to a global sign, and a size s satisfying the equality share it. (iii) is (ii) with E empty. For λ_k = 1 + (n−k)√2, the equality Λ(s) = N(s,d) forces s = d (rational parts) and then fails (the top s values exceed the next s). (iv) A mirror normal has support of size 1, or of size 2 with equal magnitudes. Plate supports have size s + d ≥ 2, and size 2 means s = d = 1 with magnitudes λ₂ ≠ λ₁. ∎

**Values.** Uniform: 4, 36, 232, 1320, 7084, … (n = 2, 3, 4, 5, 6; not in the OEIS, searched 24 Nov). The count depends on the values, not only on the combinatorial type. Signed permutations of (3, 2, 1) give 28 plates, because λ₁ = λ₂ + λ₃ merges the 24 ridges with (s, d) = (1, 2) onto the 4 planes ±x ± y ± z = 0, 6 ridges each. Values (4, 3, 2, 1) give 232 (no equality).

**Check.** `scripts/b_vacuus.py` (exact in Q and Q(√2), brute force from vertices): uniform B3 36 plates (2 edges each, none on a mirror), (3,2,1) 28, (7,3,1) 36, uniform B4 232, (4,3,2,1) 232, all equal to the formula. The ridge counts are 72 and 464. These agree with the vacuus-enumeration study (B3 36, B4 232).

**H3 (3D).** The truncated icosidodecahedron has 90 plates (60 cutting 12-gons, 30 cutting 20-gons), each carrying exactly one edge and its opposite (180/2), and none on a mirror. This comes from the exact computation in Q(√5) of the 2026-11-24-vacuus-enumeration study (`vacuus_exact.py`), not recomputed here. Its 4D analogue is H4, 8520 (same study, 4D section). Uniform proof for H: open (LEAD 2).

## 5. The Vacuus as an arrangement (question (c))

`scripts/arr.py`: intersection lattice, characteristic polynomial, regions (Zaslavsky: r = Σ|μ|) and the simplicial test. Summed over chambers, the number of walls is 2·Σ_H r(A^H). This equals rank·r exactly when every chamber is a simplicial cone.

| arrangement | planes | flats by rank | χ(t) | regions | walls (sum) | rank·r | simplicial |
|---|---|---|---|---|---|---|---|
| A Vacuus, n = 4 (truncated octahedron) | 15 | 1, 15, 69, 1 | t³ − 15t² + 87t − 73 | 176 | 624 | 528 | no |
| A Vacuus, n = 5 (4D permutohedron) | 65 | 1, 65, 1615, 11575, 1 | t⁴ − 65t³ + 1810t² − 22060t + 20314 | 44250 | 230120 | 177000 | no |
| uniform B3 Vacuus (truncated cuboctahedron) | 36 | 1, 36, 537, 1 | t³ − 36t² + 579t − 544 | 1160 | 4464 | 3480 | no |

In every case χ(1) = 0, and in rank 3 V − E + F = 2 on the sphere is satisfied (138 − 312 + 176 = 2 for A).

In 3D coordinates (truncated octahedron = permutations of (0, ±1, ±2)) the A, n = 4 Vacuus is the 3 coordinate planes plus the 12 planes ±2x ± 2y ± z = 0 and their coordinate permutations (normal (2,2,1) = edge direction × vertex). It is not simplicial, so it is not in Grünbaum's catalogue of simplicial arrangements. It is not a reflection arrangement (it contains no x_i = x_j, and its 12 three-valued planes are not mirrors). Its 3 two-valued planes are the only resonance planes in it. No named arrangement with exactly these planes was found (Sources).

## 6. Sources checked

- A402191 entry (fetched 24 Nov) and its home paper #105 (DICTO 1:2 Truncated Octahedron: The 4D Vacuus of the Permutohedron, Theorem 3, with its proof via the normal formula and its resonance remark).
- Ziegler, Lectures on Polytopes, Example 0.10 (faces of Π_n as ordered partitions); Rado 1952 (facet inequalities); Björner–Brenti (faces of Coxeter permutohedra as parabolic cosets).
- Resonance / all-subset arrangement: Kamiya, Takemura and Terao, Ranking patterns of unfolding models of codimension one, Adv. Appl. Math. 47 (2011) 379–400 (the all-subset arrangement); Billera, Tatch Moore, Dufort Moraites, Wang and Williams, Maximal unbalanced families, arXiv:1209.2309; Kühne, Combinatorica 43 (2023). These are the same citations as #105, not reopened today.
- **Cellini and Marietti, Root polytopes and abelian ideals, J. Algebraic Combin. 39 (2014) 607–645, arXiv:1207.3429, Section 3** (opened and read 24 Nov). It defines H_Φ := {Span F : F a face of codimension 2} for the root polytope P_Φ: the same construction as the Vacuus in every dimension, for root polytopes. They show that for A_n and C_n each facet cone is a single region, and that H_Φ is the W-orbit of ω₁^⊥. This is prior art for the construction (all dimensions), not for the permutohedron or for A402191. For A₃ it agrees with the Vacuus of the cuboctahedron (4 hexagon plates = the orbit of ω₁^⊥, i.e. y_i = 0).
- Web: "hyperplanes through center of permutohedron containing codimension two faces" (hits: Cellini–Marietti; Early, permutohedral plates, arXiv:1712.08520; covering the permutohedron by affine hyperplanes, arXiv:2305.06202, a different question). OEIS: 4,36,232,1320,7084; 8,72,464,2640,14168; 15,87,73; 1,36,579,544: no results.
- Grünbaum's catalogue of simplicial arrangements: not needed once non-simpliciality was shown.

## 7. Suggested OEIS facts (facts only; DICTO writes any text)

For A402191, facts that could support a comment (each proved above):
1. Ridge (B₁,B₂,B₃) with block sizes (a,b,c) spans the hyperplane c(a+b)·Σ_{B₁} x_i + a(b+c)·Σ_{B₃} x_i = (c(a+b)·a + a(b+c)·c)·(n+1)/2. In centred coordinates y = x − (n+1)/2 this is c(a+b)Σ_{B₁}y + a(b+c)Σ_{B₃}y = 0.
2. The T(n) two-valued hyperplanes are Σ_{i∈S} x_i = |S|(n+1)/2. For odd n these are all 2^{n−1} − 1 hyperplanes of the resonance (all-subset) arrangement restricted to the permutohedron's hyperplane; for even n, those with |S| and n − |S| even. A002426 (central trinomial) already appears in %Y.
3. For n ≥ 3 none of the hyperplanes is x_i = x_j.
4. a(n) is also the number of hyperplanes through the centre in the pencils of pairs of adjacent facets (Lemma P).
5. Possible link: Cellini–Marietti 2014 study the same construction (span of codimension-2 faces) for root polytopes (they do not treat the permutohedron).
6. Possible new sequence (needs DICTO's decision, rule 14 queue): the type-B analogue (5^n − 2·3^n + 1)/2 = 4, 36, 232, 1320, 7084, 36876, 188752 (n ≥ 2), uniform B_n permutohedron. Not in the OEIS. Its home paper would need this result first (rule 13).

Model entries (to look at before wording): A402191 itself; A001117 (ridges); A002426.

## 8. LEADS

1. The characteristic polynomial of the A Vacuus for all n (computed for n = 4, 5 only).
2. A uniform proof for H3/H4 (and all Coxeter permutohedra). Lemma P reduces it to whether h₂u₁ − h₁u₂ are pairwise non-parallel over the rank-2 parabolic cosets. Type A is the only one of A, B, H where generic counting fails (the a = c merges).
3. Regions of the three-valued part (A402191 minus T(n) planes) and its intersection with the resonance arrangement; compare with Cellini–Marietti's facet-cone result (here the facet cones are not single regions: the 26 facet cones of the truncated cuboctahedron versus 1160 regions).
4. The type-A count for other values (generalized permutohedra conv S_n·λ): Lemma P gives the normal directly. The merges a = c are special to arithmetic values.

## Files

`scripts/exact.py` (Q, Q(√2) exact linear algebra), `scripts/a_vacuus.py`, `scripts/b_vacuus.py`, `scripts/arr.py`; `data/a_vacuus.json`, `data/b_vacuus.json`, `data/arrangement.json`, `data/run.log`.
