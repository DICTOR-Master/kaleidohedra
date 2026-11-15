# Companions for the Loop Equality entry (2026-11-15)

**Conclusion.** On 15 November DICTO asked that the companion be "very close or related", and then chose the **aperiodic Fibonacci stacking**. It is now **fully proved in Lean** (`lean/LoopEquality/Fibonacci.lean`):
- it is a close-packed stacking;
- its hexagonal layers are exactly the h letters;
- it is not periodic;
- at every site its loop count equals diamond's, which is the explicit `loopCount m`.

The best further companion on the same subject is **#102 Corollary 3**, the sphere packings (fcc, hcp, …). Its statement compiles (`lean/SphereLoops.lean`, proof `sorry`), but it is not proved.

**Status:**
- Fibonacci: proved, in the clean build of 15 Nov (FINAL ok, only the three allowed axioms).
- Two more candidates were already proved as by-products of the main proof: the closed-walk equality and the bond walk counts.
- Corollary 3: statement typechecks.
- Corollary 2 and the #74 ring count: assessed only.
- Nothing is submitted, and no repository has been created.

The far candidates first proposed (#108 Theorem 3, the rosette balance law, Theorem N) were dropped on DICTO's instruction. They are not on the subject of the Loop Equality.

## 1. The Fibonacci stacking (chosen by DICTO; proved)

**Definition.** It is the one used in DICTO's study `2026-10-28-fibonacci-stackings` and in #102's checks (`loop_checks.py`).
- The layer types follow the Fibonacci word (c ↦ ch, h ↦ c, starting from c).
- The steps follow Jagodzinski's rule: the step keeps its direction at a c layer and reverses at an h layer, with σ0 = A and σ1 = B.

In Lean the word is given by its cut-and-project (Sturmian) form: the letter at position k is h exactly when ⌊(k+2)α⌋ ≠ ⌊(k+1)α⌋, with α = 1/φ² = (3 − √5)/2 (Morse–Hedlund 1940; Lothaire 2002, Ch. 2). It is defined for every k ∈ ℤ, so the one-sided word of DICTO's study gets its natural two-sided extension.

| Lean | Statement |
|---|---|
| `fibonacci_isStacking` | `IsStacking fibonacci` |
| `fibonacci_zero`, `fibonacci_one` | σ0 = A, σ1 = B |
| `fibonacci_layer_type` | `fibonacci (k-1) = fibonacci (k+1) ↔ IsH k` (Jagodzinski: layer k is hexagonal exactly at the h letters) |
| `isH_eq_word` | for k < 100, `IsH k` agrees with the substitution word `fibWord 10` (kernel computation through an integer form of ⌊nα⌋, `floor_eq_flipZ`, which uses Nat.sqrt and the irrationality of √5) |
| `isH_not_periodic`, `fibonacci_not_periodic` | for every p ≠ 0, neither the type word nor the stacking has period p |
| `fibonacci_loop_equality` | at every site and for every m ≥ 1: loops = diamond's loops, and = `loopCount m` |

**Aperiodicity proof.** This is the standard frequency argument for Sturmian words of irrational slope (Morse–Hedlund 1940; Lothaire 2002), done directly.
1. If the letters had period p, then ⌊(k+p+2)α⌋ − ⌊(k+2)α⌋ would be a constant c. Hence ⌊(np+2)α⌋ = nc for every n.
2. So |n(pα − c)| ≤ 2 for every n, which forces pα = c.
3. Then √5 = 3 − 2c/p would be rational, a contradiction.

**Size:** 303 lines. **Notability:** as a stand-alone entry, low (2 out of 5): it is an instance of the main theorem, and Sturmian aperiodicity is classical. As a second configuration beside the main entry, it makes the aperiodic claim concrete and checkable. **Novelty:** the stacking and its aperiodicity are not new. Only the loop statement on it is, as an instance of #102 Theorem 1.

## 2. The closed-walk equality with backtracking (already proved)

- **Lean:** `W_closed (σ) (x) (i) : Graph.W (nbr σ) i x x = closedWalks i`, for every atom of every stacking (`ClosedWalks.lean`); also `W_site` (`Counts.lean`).
- **In #102:** stated as its own sentence after Theorem 1 ("The same holds for all closed walks"), as Lemma 2 (a), and as the Proposition (the chain form).
- **Known:** Thorpe 1972 for periodic polytypes (Nagle 1966 for ice). New are only aperiodic stackings and the formal proof.
- **Mathlib:** nothing beyond what is used. **Size:** done (`ClosedWalks.lean`, 269 lines, including the closed form).
- **Notability:** 2 out of 5 as a stand-alone entry, because the periodic case is Thorpe's.

## 3. Walk counts along each bond type (already proved)

- **Lean:** `W_vert`, `W_cross`, `W_nbr` (`Counts.lean`): along a vertical bond the count is `Vv i`, along a slanted bond `Cv i`, for every stacking.
- **In #102:** Lemma 2 (b). Lemma 2 (c), for paths of two bonds, is not formalised.
- **Novelty:** we found nothing earlier (LITERATURE.md, second part).
- **Gap:** the formal proof does not show `Vv = Cv`. #102 gets this equality from diamond's symmetry; formalising it would need diamond's 24 symmetries, or the J-integral identity of fact (ii).
- **Notability:** 2 out of 5 alone, because it is a lemma.

## 4. #102 Corollary 3: sphere packings (best further companion; statement only)

- **Statement:** `lean/SphereLoops.lean`, typechecked on 15 Nov, proof `sorry`. At every sphere of the packing of every close-packed stacking (fcc, hcp, dhcp, …), the closed non-backtracking loops of every length equal fcc's.
- **Mathlib needed:** nothing new. It reuses `Levels.lean`, with lazy level paths (one level per layer, in-layer steps weighted by c = gḡ − 3), the group ring of `Counts.lean`, and `Graph.lean` with q = 11.
- **Gaps:**
  - a new neighbour list with 12 contacts;
  - the gauge lemma for lazy paths (the in-layer factor is a function of N, so `E` still depends only on N);
  - two kinds of touching pairs.
- **Size:** about 900–1,300 lines; 1–2 weeks.
- **Notability:** 3 out of 5, by the same reading as the main theorem. The audience is wider (sphere packings, fcc/hcp: Ishioka–Koiwa 1978 for return probabilities).
- **Novelty:** the closed-walk part is Thorpe's (1972) for periodic stackings. The loop part is new in #102.

## 5. #102 Corollary 2: pyrochlore network, spin ice (assessed only)

- **Statement:** like Corollary 3, on the line graph of the tetrahedral network (q = 5). It needs walks between bond ends and over paths of two bonds, which means Lemma 2 (c), not yet formalised.
- **Size:** about 1,000–1,500 lines.
- **Notability:** 3 out of 5. The audience is spin ice (#60, #74).
- **Novelty:** new in #102 (LITERATURE.md).

## 6. HexOct / #84 Window Law, Rule of Halves, #74 ring counts (assessed only)

- These are statements about pieces and holes of the packing (Rule of Halves, #57; Window Law, #84). Only the #74 count of boat-shaped six-rings (3h/2 per atom) is about the contact network itself.
- **Lean for the ring count:** it needs the shape of a six-ring (chair or boat) as a definition, which is a new and fidelity-sensitive notion.
- **Size:** about 500–800 lines.
- **Notability:** 2 out of 5: a linear count in the share of h layers.
- **Not recommended** beside the Loop Equality: it is about shapes, not loop counts. #102 Section 4 (1) notes that the loop counts agree even though the shapes differ.

## Recommendation

A series of two configurations in one repository, if DICTO later decides to submit:
1. the Loop Equality with the explicit count;
2. the Fibonacci corollary.

Corollary 3 would be the third. The honest notability estimate for the series stays at 3.5 out of 5 (LITERATURE.md, last part).
