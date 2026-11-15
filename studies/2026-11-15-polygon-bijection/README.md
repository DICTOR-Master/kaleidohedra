# A local proof of the polygon laws of #102 v5 (15 November 2026)

**Verdict.**
- **Proved (all lengths):** at every site of every stacking, the polygons that cross each bilayer's vertical bonds at most twice are equally many in every stacking, length by length and crossing profile by crossing profile. The proof is a bijection: cut the polygon at the two vertical bonds of a bilayer and turn the far part a half-turn about the midpoint of the two bonds (Theorem A). It also covers every polygon whose crossing points at a bilayer, with their far-side pairing, have a half-turn or a mirror symmetry of the right kind.
- **Proved (all lengths): an exact formula for what is left.** Flipping one bilayer's c/h letter changes the count by Δ = −½ Σ A_root · A_far (Theorem B). Each A measures how one half of the network (one side of that bilayer) fails to be symmetric under the half-turn. It needs only pairs of arcs that **meet**, so it is a finite, local table. Two-crossing terms are zero (that is Theorem A again). Six-crossing terms vanish at l ≤ 20 by a short hand argument.
- **Proved with a small finite computation (l = 18, 20): Theorem 5 of #102 v5.** The four-crossing tables reproduce every coefficient: 12, 30, 42, 24 at l = 18 and 30, 114, 204, 12 at l = 20. They give 0 at every l ≤ 16, 0 for flips outside bilayers −2…1, and the same values for all 512 patterns of the neighbouring letters, at l = 18 and at l = 20. So the law is linear, with no products, for a structural reason. The l = 18 table is small: 1038 arcs, 7713 meeting pairs.
- **Why 18:** half-structure asymmetry first appears with 6 bonds. All 12 asymmetric six-bond shapes carry their asymmetry on the same pairing on both sides, and two equal pairings cannot close into one polygon. So the first nonzero product needs 6 + 8 bonds plus 4 crossing bonds: 18.
- **Checked exhaustively on finite windows:** the surgery is a bijection in every run (3C and 2H at every flip, both atoms, to l = 20; every c/h word of 7 bilayers to l = 16; of 5 bilayers to l = 18). Three wrong twists fail in every run, as they must.
- **Still open:** the absolute constant (diamond's 349236, 2362200) is the Guttmann–Jensen count. A local argument gives only the differences between stackings. The laws at l = 22 and 24 are now proved the same way (§8).

**Status:** all runs done; 2208 surgery runs, 0 failures; every table check passes (`data/CHECKS.txt`). Job polybij printed FINAL FAIL only because its count found 25 ok files for 24 parts: the output of the second job had landed in the same folder. All 24 parts are ok, and the count is fixed. Job polyhalves20 ended FINAL ok. Not yet in a paper. Lean has not been started. The plan and its size are in §7.

## 1. Setting

Network, stackings and letters as in #102 and study 2026-11-15-ring-counts-stackings.
- Bilayer k has a lower atom L_k and an upper atom U_k at every point of the lattice T_{s[k]}, with s[k] ∈ {A, B, C}. The three lattices are the cosets of one triangular lattice T.
- The vertical bond L_k–U_k joins them. U_k bonds to the three nearest L_{k+1}.
- Bilayer k is h if s[k−1] = s[k+1].

**Cut.** The vertical bonds of bilayer k are the only bonds between two halves:
- the **lower half** H⁻_k (L_k and everything below);
- the **upper half** H⁺_k (U_k and everything above).

A polygon crosses the cut an even number n of times. Call its crossing points P ⊂ T_{s[k]}. For a polygon through a site v, the **root half** is the half that contains v and the **far half** is the other.

**Plane symmetries.**
- Γ⁺ is the group of plane isometries that map each of T_A, T_B, T_C to itself (translations by T, 120° turns about lattice points, and the three mirrors through lattice points along the long diagonals).
- For a letter a, Tog_a is the set of isometries that map T_a to itself and exchange the other two lattices. It contains the half-turn about any point of ½T_a, and mirrors along the nearest-neighbour directions.
- Every half is Γ⁺-invariant, since it is a stack of translates of T.

**Lemma 1 (one flip = one twist).** Let g ∈ Tog_{s[k]}. Replacing the far half by its image under g gives the network of the stacking whose letter at bilayer k is flipped (c ↔ h). Every other letter is unchanged, and the root half and the site v stay where they are.

*Proof.* The letters on the far side become σ(s[j]), where σ exchanges the two letters other than s[k], while s[k] stays fixed. Bilayer k compares s[k−1] with s[k+1], and exactly one of the two has been changed by σ. Both differ from s[k], so the equality flips. Every other bilayer compares two letters on the same side, and σ preserves equality. ∎

**Lemma 2 (two points).** For p ≠ q in T_a, the half-turn about (p+q)/2 lies in Tog_a and exchanges p and q.

*Proof.* A point reflection maps the lattice coset T_a + (1,1)/3 to T_a − (1,1)/3, which is the third coset. ∎

## 2. Theorem A: the half-turn surgery

Let C be a polygon through v. At bilayer k it has crossing points P, root-side arcs, and far-side arcs pairing P by a matching M. Call C **symmetric at k** if some involution g ∈ Tog_{s[k]} has g(P) = P and g(M) = M. Such a g fixes the centroid of P, so it is the half-turn about the centroid or one of the toggle mirrors through it. Fix that order and take the first such g.

**Surgery.** Φ_k(C) has these edges:
- the root-side edges of C;
- the g-images of the far-side edges;
- the n vertical bonds at P. These are unchanged, since g(P) = P.

**Theorem A.** Φ_k is a bijection from the polygons through v that are symmetric at k in G_s onto those in G_{s'}, where s' has bilayer k flipped (Lemma 1). It preserves:
- the length;
- the site v;
- the crossing number at every bilayer;
- the crossing points and both pairings at k.

*Proof.*
1. The image edges lie in G_{s'}: the root half is unchanged, and g maps the far half of G_s onto the far half of G_{s'}.
2. Every atom has degree 2.
3. The far arcs are moved onto arcs that pair g(M) = M. The root arcs keep their pairing. The union of the two pairings is therefore the same single cycle on P as before, so the image is one polygon.
4. The image is simple, because the two halves share no atom.
5. Lengths and v are kept, since the root half is fixed.
6. Crossing numbers are kept at every bilayer, since g is horizontal and keeps each atom in its bilayer.
7. Φ_k(C) has the same (P, M), so the same g is chosen again. g is an involution, so applying the same rule in G_{s'} gives back C.
8. A polygon with n = 0 lies in the root half and is fixed. ∎

**Corollary A1 (all lengths).** Every polygon with n = 2 at k is symmetric, by Lemma 2. Fix a site and a crossing profile in which every bilayer is crossed at most twice. The number of polygons of length l with that profile is the same in every stacking.

*Proof.* Change the letters one at a time. A polygon of length l meets only bilayers within l/4 + 1 of v (Lemma 4 of #102), so only finitely many flips matter. ∎

This answers question 1 at full strength (all lengths). The same bijection also covers four-crossing polygons whose crossing points form a parallelogram (the half-turn keeps every pairing), and those with a toggle-mirror symmetry that keeps M.

The twist is the infinite-graph analogue of a Whitney twist across a 2-separation. Whitney's 2-isomorphism theorem (1933) says such twists preserve cycles. Here the cut is a whole layer of bonds, and the twist works polygon by polygon whenever only two bonds of the layer are used.

## 3. Theorem B: an exact local formula for the rest

For a crossing set S taken up to translation, and a matching M of S:
- f(S, M, F) is the number of far-side linkages (vertex-disjoint arcs in the far half pairing S by M, F bonds in total);
- w(S, M, R) is the number of root-side linkages, each weighted by the number of its atoms of the root's type (same bilayer and same lower/upper position as v).

**Product structure.** A polygon is a root linkage plus a far linkage, with pairings M ≠ M' whose union is one cycle on S. Every such pair forms a polygon, because the halves are disjoint. Summing over the translates of S (the root half is T-invariant) gives

    p_l(v) = Σ_{n, S, M, M'} w(S, M, R) · f(S, M', F),   with R + F + n = l.

This was checked on 19,314 polygons: the product structure holds for every key (`linkages.py`).

**Theorem B.** Let G' be G with bilayer k flipped, and let g be any element of Tog_{s[k]}. Then

    p_l(v; G') − p_l(v; G) = −½ Σ_{n, S, M, M'} A_w(S, M, R) · A_f(S, M', F),

where A_f(S, M, F) = f(S, M, F) − f(gS, gM, F), and A_w is defined the same way with w.

*Proof.*
1. By Lemma 1, f in G' equals f(gS, gM') computed in G. Since f is Γ⁺-invariant and Tog = gΓ⁺, the choice of g does not matter.
2. So Δ = Σ w(S)(f(gS) − f(S)) = −Σ w A_f.
3. Write w = ½(w(S) + w(gS)) + ½ A_w. The symmetric part pairs with the antisymmetric A_f to give zero under S ↦ gS. That leaves −½ Σ A_w A_f. ∎

**Locality.** For n = 4, f = (all pairs of arcs) − bad, where "bad" counts the pairs of arcs that share an atom.
- The number of all pairs is a product of single-arc counts. Each single-arc count is Tog-invariant by Lemma 2, applied to the half-turn about the midpoint of the arc's ends.
- So A_f(S) = bad(gS) − bad(S), and A_w is the same with weights.
- Only pairs of arcs that meet enter, so the table is finite.
- A 2-point S has A = 0, which is Theorem A in counting form.

**Six crossings at l ≤ 20 (by hand).**
- n = 6 needs R, F ≥ 6. At l = 18 that forces three arcs of length 2 on each side. At l = 20 it forces one side with exactly 6 bonds.
- A 2-bond arc between neighbouring points p, q of T_{s[k]} is unique: it runs through the centre of the triangle on pq whose letter is the first sheet's letter. Two disjoint pairs never use the same centre, since a centre touches only one triangle.
- So with three 2-bond arcs, f = [all three pairs are neighbours]. The weights are constant: 6 boundary atoms and 3 middle atoms. Both are Tog-invariant, so A = 0 on any side with 6 bonds.
- Hence every six-crossing term is zero at l = 18, 20. n ≥ 8 needs at least 24 bonds.

**The finite tables (`halves.py`).** All arcs from a boundary atom with at most F_max − 2 bonds, all meeting pairs, then A for each half.

| | arcs | meeting pairs | configurations | A ≠ 0 (far type) | first F with A ≠ 0 |
|---|---|---|---|---|---|
| l ≤ 18 (F_max 10) | 1038 | 7713 | 1917 | 840 | 6 |
| l ≤ 20 (F_max 12) | 6756 | 74493 | 6591 | 3318 | 6 |

**Result.** For the lower atom of bilayer 0 and flips at kf = −2, −1, 0, 1:

| | kf = −2 | −1 | 0 | 1 |
|---|---|---|---|---|
| Δ at l = 18 | −12 | −30 | −42 | −24 |
| Δ at l = 20 | −30 | −114 | −204 | −12 |

- For all l ≤ 16, Δ = 0.
- The same values hold on four bases (3C, 2H, (ch)*, (hhcc)*). They also hold, at l = 18 and at l = 20, for all 512 patterns of the six letters around each flip, kf = −4…3, with 0 outside −2…1 (`data/pilot/halves18-all.txt`, `data/full/halves20-all.txt`). The tables reach at most three levels into each half, so this covers every stacking.
- **Negative control:** with a class-preserving mirror in place of the toggle (WRONG=1), every A is 0 and all four checks fail.

**Why the first difference is at 18 (`probe16.py`).**
- Asymmetry first appears with 6 bonds, as a 2-bond arc plus a 4-bond arc, in 12 shapes (three points in a row plus one neighbour).
- In each shape, the far A (±1) and the weighted root A (∓5) sit on the **same** single pairing. Theorem B needs M ≠ M', so the 6 + 6 term (l = 16) is 0.
- The first nonzero products are 6 + 8 and 8 + 6, with 4 crossing bonds: l = 18.

**Corollary (Theorem 5 of #102 v5, proved up to the diamond constant).**
- (a) For l ≤ 16, p_l is the same at corresponding sites of all stackings.
- (b) p_18 and p_20 differ from diamond's values by exactly the stated linear forms.

Proof: telescope over flips. Each flip changes the count by its tabulated Δ, which does not depend on the other letters. The constants 349236 and 2362200 are diamond's numbers (2·A038515, Guttmann–Jensen 2009). They are not proved here.

## 4. Controls

**Positive:**
- 3C totals equal 2·A038515 (12, …, 2362200) in every run.
- The surgery's images are valid, distinct, and equal to the symmetric set of G' in every run.
- Δ by direct enumeration (rigid G' − rigid G) equals Σ r·(f′ − f) from the linkages: −42 at flip 0, l = 18.
- The half tables reproduce Theorem 5.

**Negative:**
- Three wrong twists break in every run: the half-turn about one crossing point instead of the midpoint, no twist, and a 60° turn about a crossing point.
- The class-preserving mirror in Theorem B gives 0 instead of the coefficients.

## 5. Literature (free sources; see LITERATURE.md for the list)

No source found treats polygons, or any cycle count, on lonsdaleite or other polytypes by a surgery argument. The nearest are:
- Whitney's twist (cycle-preserving flips at 2-separations);
- Benito et al. 2023, who find SAW counts on hcp versus fcc (close-packed spheres) differing beyond some length, by enumeration;
- Herrero–Ramírez 2013 (ring statistics of Ih and Ic).

## 6. Runs and files

Runs went through the job gate on the compute hosts:
- pilot (named l = 16, 33 s; dumps; l = 18 local formula);
- polybij: 24 parts (bij named 18/20, all words, negatives, halves 18 and halves 20 on 4 bases);
- polyhalves20: halves 20 on all 512 patterns.

Files:
- `scripts/bij.c`: polygon enumeration, crossing data, the symmetry test, the surgery (and three wrong twists), checks of the image set, rigid counts, dumps.
- `scripts/bij.py`: the driver (modes named, words, negative, dump).
- `scripts/halves.py`: the half-structure tables and Theorem B (modes: bases, `all`, WRONG=1).
- `scripts/linkages.py`: product structure and Δ = Σ r(f′ − f) from dumps.
- `scripts/probe16.py`: the l = 16 cancellation.
- `scripts/rigid_shapes.py`, `scripts/testB.py`: diagnostics. testB shows that a root-side twist fixing the site never applies.
- `scripts/run_bij.sh`: the job script.
- `scripts/fig102v6.py`: Figure 4 of #102 v6 (the twist on one 10-polygon); it first re-checks Theorem A on all 150 two-crossing 10-polygons at the site (output `data/fig102v6.txt`, FINAL ok).
- `data/pilot/`, `data/full/`: raw outputs, each ending ALLCHECKS ok or FAIL.
- `logs/`: the job logs.

## 7. Lean plan (not started)

**Statements.** These reuse the #102 Challenge definitions (stacking, network, polygon through a site).
- (A) Corollary A1 for all lengths.
- (B) The difference form of Theorem 5: p_l(v; σ) − p_l(v'; 3C) = 0 for l ≤ 16, and the stated linear forms for l = 18, 20.

The absolute numbers need diamond's counts. Those are out of kernel reach (50016 to 2362200 polygons), so they enter as a stated hypothesis or as a citation.

**Proof parts and estimated size:**

| part | content | estimate |
|---|---|---|
| 1 | Plane lattice, Γ⁺, Tog, Lemma 1 (flip = twist of the far half), Lemma 2 | 400–700 lines |
| 2 | Cut lemma (vertical bonds are the only links), arcs, crossing sets, Theorem A with the involution argument | 1,000–1,800 lines |
| 3 | Product structure p = Σ w·f, the symmetrisation of Theorem B, locality f = all − bad with single arcs Tog-invariant (finite sums over a bounded window: locality as Lemma 4 of #102) | 1,200–2,000 lines |
| 4 | Six-crossing vanishing by hand; reach lemma (arcs of at most 8 or 10 bonds stay within 2 or 3 levels, so at most 64 letter patterns per half) | 300–500 lines |
| 5 | Finite tables by `decide` | see below |

**Part 5 at l = 18.**
- Each table is 1038 arcs and 7713 meeting pairs over atoms with small integer coordinates. At most 2 × 64 normalised tables are needed (fewer after the toggle identity A_{gH} = −A_H), with a sum over about 1900 configurations.
- This is at the edge of kernel `decide` but plausible if done as a verified enumerator by structural recursion, with the tables passed as certificates and checked rather than searched.
- If `decide` stalls, the fallback is to split by pattern (64 independent lemmas).

**Part 5 at l = 20.** About 10× the arcs and pairs (6756 and 74493). This is probably beyond the kernel without `native_decide`. Formalise l = 18 and state l = 20 as checked.

**Total:** about 3,000–5,000 lines on top of #102 for (A) plus the l = 18 part of (B).

CONCLUSION:
- Polygons crossing each bilayer at most twice are stacking-blind at every length: proved by the half-turn surgery (Theorem A).
- Every stacking difference is −½ Σ A_root A_far over local, asymmetric linkages (Theorem B). With 4-crossing tables of about 8000 meeting pairs this proves Theorem 5's linear laws at l = 18, 20, and equality for l ≤ 16, up to diamond's constants.
- STATUS: proved, plus finite tables computed for every letter pattern at l = 18 and 20; not yet in #102.

LEADS:
1. Write Theorem A and Theorem B into #102 v5 §5, replacing "why 18 is open" (DICTO to decide the placement).
2. The l = 22, 24 local laws via Theorem B: tables with F_max 14–16, plus the six-crossing terms through inclusion–exclusion. The 108 b pair term at l = 24 should appear as a product of two flips' asymmetries.
3. Lean: part 1 + 2 (Theorem A) first. It has no tables and is a clean standalone result.
4. The same surgery for close-packed spheres (fcc versus hcp, Benito et al. 2023), and for the ice series of study 2026-11-15-ring-counts-stackings, which uses even subgraphs with the same cut.

## 8. Lengths 22 and 24 (15 November 2026, second run)

**Verdict.**
- **Proved, up to diamond's constants (finite tables + Theorems A, B):** for the lower atom of bilayer 0,

      p22 = 16716612 − 96·h[−3] − 390·h[−2] − 1029·h[−1] − 1437·h[0] − 552·h[1] − 192·h[2]
      p24 = 118335744 − 732·h[−3] − 507·h[−2] − 4299·h[−1] − 7200·h[0] + 618·h[1] − 1128·h[2]
                      − 54·h[−2]h[−1] − 72·h[−1]h[0] − 90·h[0]h[1]

  For the upper atom, reflect the indices (j → −j), as at 18 and 20.
- **p22 is linear; p24 has exactly three products, all of neighbouring bilayers.** No other product, and no bilayer outside −3…2, occurs.
- **Checked against direct enumeration, exactly:** all 512 c/h words on bilayers −4…4, both atoms, l = 18…24 (1024 runs, new), and all 80 sites of the 11 named polytypes (ring-counts study). Every number matches.
- **Theorem 2 of the ring-counts study follows:** averaged over a period, p22 = 16716612 − 3696 f and p24 = 118335744 − 13248 f − 216 ⟨hh⟩, where ⟨hh⟩ is the frequency of two neighbouring h bilayers. Since b = 2(f − ⟨hh⟩), this is 118335744 − 13464 f + 108 b. So both period laws are now proved (up to the diamond constants), not only checked.
- **What the b term is, locally:** a pair of neighbouring h bilayers costs 216 polygons of length 24 more than the two h bilayers cost separately (54 + 72 + 90, by the pair's place relative to the site). It comes from four-crossing polygons with 14 bonds on one side of the flipped bilayer and 6 on the other. The asymmetry of a 14-bond half linkage depends on whether the bilayer next to the cut is h; it never depends on the bilayer after that, and no half linkage of 12 bonds or fewer depends on either. A c/h boundary is where the pair term is missing, hence the +108 per boundary.
- **Six crossings now count:** they add +24 (h[−1]) and +42 (h[0]) at l = 22, and −24, +186, +318, −48 (h[−2] … h[1]) at l = 24, all linear. Without them the law fails (negative control). Eight crossings give 0.
- **Negative controls fail as required:** the tables built with a class-preserving mirror in place of the half-turn (WRONG=1), and the law with the six-crossing terms left out, each disagree with the direct counts.

**Status:** all jobs FINAL ok (one first run failed a check that was too strict and was rerun; §8.5). Not in #102 (DICTO's read of v6 is pending). Lean not started.

### 8.1 Four crossings (`halves24.py`)

- The same Theorem B sum as §3, to F = 14 bonds per side. The code was written again. Each meeting pair of arcs is counted through its 8 ordered representations and the total divided by 8, with no dedup set. To F = 12 it gives exactly the tables of `halves.py` for all 8 letter patterns, unweighted and with 6 root weights (`check12.txt`).
- **Sizes at F = 14:** 45834 arcs from a boundary atom, 18477 configurations (S, M, F) per letter pattern, about 10400 with A ≠ 0.
- **No side with A ≠ 0 has fewer than 6 bonds** (read off the tables). So at l ≤ 24 both sides have 6 to 14 bonds, and an arc has at most 12.
- **Reach lemma.** An arc of at most 12 bonds goes down to the near atom N_3 at most: 5 bonds down and 5 up. The far atom F_3 would need its vertical bond twice. So a table depends on the letters c[0..3] of its half only, which the code asserts. It follows that Δ_kf depends only on h[kf−2], h[kf−1], h[kf+1], h[kf+2]. It is computed for all 512 patterns of kf ± 1, 2, 3 at flips kf = −4…3, and the letters at kf ± 3 indeed never matter.
- **Results, all other letters c (four-crossing part of Δ_kf):**

| kf | −3 | −2 | −1 | 0 | 1 | 2 |
|---|---|---|---|---|---|---|
| l = 22 | −96 | −390 | −1053 | −1479 | −552 | −192 |
| l = 24 | −732 | −483 | −4485 | −7518 | +666 | −1128 |

  Flips −4 and 3 give 0. At l = 18 and 20 every pattern reproduces Theorem 5 again.

### 8.2 Six and eight crossings (`six.py`)

- An n-crossing polygon is a cyclic chain of n/2 disjoint root arcs and n/2 disjoint far arcs. `six.py` counts these chains exactly in G (bilayer kf c) and in G′ (kf h). Each shape is weighted by its atoms of the root's type and divided by n, its number of representations. This is the product structure p = Σ w·f evaluated directly. No symmetrisation is used, so it needs no extra lemma.
- **Positive control:** the absolute numbers of polygons that cross bilayer 0 (or −1) exactly six times are 180 and 3198 (90 and 1722) at l = 18, 20, in 3C and in 2H. They equal the crossing profiles of the direct enumeration (ring-counts study, `diag.txt`).
- **Lemma 7, extended (by hand, confirmed on every line):**
  - a side with exactly 6 bonds (three 2-bond arcs) has no asymmetry, so at l = 22 only the split (8, 8) can contribute, and at l = 24 only (8, 10) and (10, 8);
  - eight crossings at l = 24 need four 2-bond arcs on each side, which have no asymmetry by the same argument, so their term is 0;
  - ten crossings need at least 30 bonds.
- **Arcs of at most 8 bonds see c[0..2] only** (asserted), so the six-crossing term depends only on h[kf ± 1]. It turns out not to depend on them:

| kf | −3 | −2 | −1 | 0 | 1 | 2 |
|---|---|---|---|---|---|---|
| l = 22 | 0 | 0 | +24 | +42 | 0 | 0 |
| l = 24 | 0 | −24 | +186 | +318 | −48 | 0 |

### 8.3 The laws (`law.py`)

- Δ_kf = (four-crossing part) + (six-crossing part) + (eight-crossing part) exactly at l ≤ 24. The two-crossing part is 0 by Theorem A.
- p(word) is built by telescoping from 3C for all 4096 words on bilayers −6…5, once flipping the letters in increasing order and once in decreasing order. The two agree on every word, which checks that the tables are consistent.
- Möbius inversion gives the multilinear laws above. The window edges −6 and 5 never occur.
- **Proof of the laws (up to the constants).** Telescope over flips: each flip changes p_l by its tabulated Δ, which depends only on the listed neighbour letters. The constants 16716612 and 118335744 are diamond's values (2·A038515, Guttmann–Jensen 2009); they are not proved here.

### 8.4 The product terms (`pairterm.py`)

- Δ at l = 24, split by (R, F) = (root bonds, far bonds). Switching one neighbour letter changes only the split (14, 6) when the neighbour is on the root side, or (6, 14) when it is on the far side, and only for the neighbour next to the flipped bilayer:
  - h[−1] changes Δ_−2 by −54 and h[−2] changes Δ_−1 by −54;
  - h[0] changes Δ_−1 by −72 and h[−1] changes Δ_0 by −72;
  - h[1] changes Δ_0 by −90 and h[0] changes Δ_1 by −90.
- The two directions agree, as they must for a product term.
- **Half tables:** switching the half's first bilayer c → h changes its asymmetry first (and only) at F = 14, both unweighted and weighted. Switching its second bilayer changes nothing up to F = 14.

### 8.5 Runs and files

- Jobs (job gate, pilots ≤ 5 min first):
  - polylaw24-tables: four-crossing tables + check12 + WRONG=1 control;
  - polylaw24-six-dbb (flips 0, 1, 2), polylaw24-six (flips −3, −2, −1, second host), polylaw24-sixneg;
  - polypair24;
  - polylocal24-dbb (chunks 0–27), polylocal24-dbb2 (chunks 28–31, moved from the overloaded second host);
  - polylawfinal (law + two negative controls).
- polylaw24-six ended FINAL FAIL: its check that the root half is the same in G and G′ compared letters exactly. For kf < 0 the letter construction runs upward, so G′'s root half comes out with its letters exchanged by the toggle, which is a global isometry. The check now compares up to the toggle. Its DELTA values were kept in `data/law24/node-firstrun/`, and the rerun (polylaw24-sixneg) gave the same values with ALLCHECKS ok.
- Files:
  - `scripts/halves24.py`, `six.py`, `law.py`, `pairterm.py`, `run_law24.sh`, `run_local24.sh` (direct enumeration with the unchanged `rings.py` of the ring-counts study), `run_lawfinal.sh`;
  - `data/law24/`: `halves24*.txt`, `tables24.txt.gz` (all four-crossing tables to F = 14), `check12.txt`, `six24-*.txt`, `local24-*.txt`, `pairterm24.txt`, `law*.txt`.

CONCLUSION (§8):
- p22 and p24 are proved local laws, up to diamond's constants. p22 is linear in h[−3..2]; p24 adds three neighbour products −54, −72, −90.
- The period laws 16716612 − 3696 f and 118335744 − 13464 f + 108 b follow. The b term is the neighbour-pair interaction, carried by four-crossing polygons with a 14-bond half linkage that reaches across the next bilayer.
- STATUS: proved and exactly checked (1024 local runs, 80 named sites); not in #102.

LEADS (§8):
1. l = 26: tables to F = 16, six-crossing splits up to (10, 10); products of bilayers two apart may first appear there.
2. A hand proof that half asymmetry ignores the second bilayer up to F = 14. It would shorten the Lean part 5 tables.
3. Placement in #102 after DICTO's read of v6 (DICTO decides).
