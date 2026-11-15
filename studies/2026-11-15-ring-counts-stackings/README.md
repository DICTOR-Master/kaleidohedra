# Where ring counts first differ between stackings (15 November 2026)

**Verdict.**
- **All four standard ring statistics are blind to stacking.** King's rings, Guttman's rings, shortest-path (primitive) rings and strong rings give the same answer at every site of every stacking: 12 six-rings and nothing else. This is already published for ice Ih and Ic (Herrero–Ramírez 2013). For every stacking it is new in the sources we checked (LITERATURE.md). The strong-ring case is a short proof. The other three are exact computation: SP rings to length 24 on 11 polytypes, and to length 20 on every local c/h pattern.
- **The counts that do differ are the self-avoiding polygons** (all simple cycles through a site). They agree for every stacking up to length 16. **They first differ at m\* = 18:** diamond (3C) has 349236 eighteen-cycles through each site, and lonsdaleite (2H) has 349128.
- **The count at a site is an exact linear function of the c/h letters of four nearby bilayers** (Theorem 1). Averaged over a period, it is linear in the fraction of h layers up to length 22. At length 24 it also needs the fraction of c/h boundaries (Theorem 2).
- **Ice:** in Nagle's form of the ice-rule count, the bond-graded series of ln Z per site first differs between stackings at **16 bonds**, two orders before the polygons do. The difference is +64·3⁻¹⁵ per unit h-fraction, in favour of h (Theorem 3).
- None of these thresholds, values or formulas was found in the sources checked. OEIS has polygon counts for diamond only.

**Status:** all runs done, FINAL ok. 5058 exact checks, 0 failed (`data/CHECKS.txt`). Not yet in a paper. Lean has not been started (§6).

## 1. Network and definitions

- **The network** is the tetrahedral network of a stacking, built the same way as in #102.
  - Bilayer k has a lower and an upper atom at the in-plane position of its letter s[k] ∈ {A, B, C}, joined by a vertical bond.
  - The upper atom of bilayer k bonds to the three lower atoms of bilayer k+1 that sit at in-plane distance a/√3.
  - Bilayer k is **h** if s[k−1] = s[k+1], and **c** otherwise (Jagodzinski).
- **Sheets.** The slanted bonds between bilayers k−1 and k form a puckered honeycomb, which we call sheet k. The vertical bonds of bilayer k join sheet k to sheet k+1.
  - At an h bilayer the two sheets are eclipsed: their hexagons lie exactly above one another and form hexagonal prisms.
  - At a c bilayer they are staggered.
- **Coordinates** are exact integers (in-plane, in thirds of the lattice basis). All counts are exact integers; series coefficients are exact fractions.

The ring definitions, as in the ISAACS manual (LITERATURE.md §2):
- **(a) SP rings (primitive rings).** A cycle C is an SP ring if d_G(a, b) = d_C(a, b) for every two vertices a, b of C. That is, C has no shortcut: no path in the network is shorter than the shorter arc of C between two of its vertices. This is Franzblau's shortest-path criterion (1991) and the computational test for primitive rings of Yuan–Cormack (2002). A cycle with a shortcut is the sum of two strictly shorter cycles, so it is not primitive in the Goetzke–Klein sense either.
- **(b) King's rings (1967).** For each pair of neighbours of a site: the shortest paths between them that avoid the site.
- **(c) Guttman's rings (1990).** For each bond at a site: the shortest cycles through that bond.
- **(d) Strong rings** (Goetzke–Klein 1991). A cycle that is not a sum, in the cycle space over GF(2), of any number of strictly shorter cycles.
- **(e) Polygons.** Every simple cycle through the site, each counted once.

Counts are given per site, for the lower and the upper atom separately, and per bond: the vertical bond V and the three slanted bonds S.

## 2. Results

### 2.1 Ring statistics (a)–(d): the same for every stacking

The rings were computed at every site of every bilayer of 11 polytypes: 3C, 2H, 4H, 6H, 8H, 9R, 10H, 15R, 12R, 21R, and 10H\* = (hhchc). They were also computed at both sites for all 2048 c/h words on the 11 bilayers around the site, and at 8 sites of the Fibonacci stacking. In every case:
- **SP rings:** 12 six-rings, and none of length 8 to 24 (named polytypes) or 8 to 20 (all local words, Fibonacci). Each bond lies on 6 of them.
- **King's rings:** 12. Each of the six angles at a site lies on exactly two six-rings, and these are the shortest paths.
- **Guttman's rings:** 24 bond–ring incidences, which is the same 12 six-rings.
- **Strong rings:** only the 12 six-rings.
  - *Proof:* every stacking is tiled by cages bounded by hexagons: the adamantane cage (4 chairs) and the hexagonal-prism cage (2 chairs and 3 boats). The 2-skeleton of a cell decomposition of ℝ³ is simply connected, so the hexagons span the cycle space. Every longer cycle is therefore a sum of six-rings.
  - *Check:* all 1392 cycles of lengths 8–12 through each tested site lie in the GF(2) span of nearby six-rings (`strong-ring check` lines).
- **Why it is always 12:** combinatorially, each site has 6 six-rings through its vertical bond, 3 in its own sheet and 3 through the vertical bonds of its sheet neighbours. This holds for c and h alike, so the six-ring structure at a site never depends on the stacking.

**Control:** this reproduces Herrero–Ramírez 2013 (Table II: 12 six-membered rings at every site of Ih and Ic, and no others).

### 2.2 Polygons: the first difference is at length 18

Cycles through a site:

| length | 6 | 8 | 10 | 12 | 14 | 16 | **18** | 20 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|
| 3C (diamond) | 12 | 24 | 240 | 1128 | 8148 | 50016 | **349236** | 2362200 | 16716612 | 118335744 |
| 2H (lonsdaleite) | 12 | 24 | 240 | 1128 | 8148 | 50016 | **349128** | 2361840 | 16712916 | 118322280 |

- The 3C row equals 2·A038515 at every length (Guttmann–Jensen's diamond data). This is our positive control.
- Up to length 16, every site of every stacking gives the 3C value. **m\* = 18.**
- Per bond in 2H at length 18: the vertical bond lies on 174522 eighteen-cycles and each slanted bond on 174578. In 3C every bond lies on 174618.

### 2.3 Theorem 1 (local formula, l = 18 and 20)

Take the **lower atom of bilayer 0**, and let h[j] = 1 if bilayer j is h and 0 if it is c. The number of cycles of length l through it is:

    p18 = 349236 − 12·h[−2] − 30·h[−1] − 42·h[0] − 24·h[1]
    p20 = 2362200 − 30·h[−2] − 114·h[−1] − 204·h[0] − 12·h[1]

- For the **upper atom**, reflect the bilayer indices (j → −j). For example, p18 = 349236 − 24·h[−1] − 42·h[0] − 30·h[1] − 12·h[2].
- For l ≤ 16, p_l is a constant: 12, 24, 240, 1128, 8148, 50016.
- **How this was established:**
  - All 2¹¹ c/h words on bilayers −5…5 were computed at both atoms. The unique multilinear polynomial in the h[j] was found by Möbius inversion.
  - Only the four listed bilayers occur, all with linear terms only, so products such as h[0]h[1] have coefficient 0.
  - Every 8th word was recomputed with random letters outside the window and a larger in-plane window. Nothing changed.
- **Fibonacci stacking:** the 8 tested sites (positions up to 2584) agree with the formula, and with the network windows of two sizes.
- **Per site the count is not stacking-free:** at a c site with h neighbours it already drops, for example 349182 at Fibonacci position 233.

### 2.4 Theorem 2 (period averages)

Over one period of any periodic stacking, let f be the fraction of h bilayers and b the fraction of bilayers whose letter differs from the next one (c/h boundaries). Then the average number of cycles through a site is:

    l ≤ 16:  the 3C value
    l = 18:  349236 − 108 f
    l = 20:  2362200 − 360 f
    l = 22:  16716612 − 3696 f
    l = 24:  118335744 − 13464 f + 108 b

- **Proof for l = 18, 20:** this follows from Theorem 1, since each bilayer is h for a fraction f of the sites. The coefficients sum to 108 and 360.
- **Check:** the formulas hold exactly for all 11 polytypes. At length 24 the linear law fails; for example 4H is 108 above it. The deviation is exactly 108 b in all 11 polytypes.
- **Scope:** the l = 22 and l = 24 lines are checked identities on 11 polytypes. Their local formulas were not computed, because the word window stopped at l = 20.

### 2.5 The local configuration that makes the difference (diagnostic, l ≤ 20)

`diag.py` classifies each cycle by how often it crosses the vertical bonds of each bilayer. The crossing number is always even, because those bonds are the only links between two neighbouring sheets.
- **Cycles that cross every bilayer at most twice are equinumerous** in 3C and 2H at every length up to 20.
- **The whole difference comes from cycles that cross one bilayer four times.**
  - At the site's own bilayer, two-sheet cycles of length 18 crossing it four times number 11814 in c and 11880 in h (+66). One bilayer down: 7518 and 7560 (+42).
  - The cycles that cross one bilayer four times and a neighbouring bilayer twice are fewer in h. In total: −108.
- **Reading:** an h bilayer makes the two sheets eclipsed, so their hexagons line up into prisms. This creates more short ways to weave back and forth across one bilayer and fewer ways to continue into the next sheet.
- Why the first such length is exactly 18 is not explained by this diagnostic. It is LEAD 1.

### 2.6 Theorem 3 (ice: Nagle's series, graded by bonds)

**The series.**
- The ice-rule count satisfies Z = (3/2)^N Σ_F 3^(−n₂(F)), over all even subgraphs F, where n₂ is the number of vertices of degree 2 (Nagle 1966; written so in Chen–Ran 2026). Mark each bond of F with y.
- Then ln Z/N = ln(3/2) + Σ_k a_k y^k. The a_k come from the cluster (Mayer) expansion over connected even subgraphs ("polymers"). Two polymers are compatible if they are vertex-disjoint. We computed this exactly to k = 18 at every site of the 11 polytypes.

**Result.**
- a_6 … a_14 are the same for every stacking: 2/729, 1/2187, 8/19683, 55/177147, 290/1594323.
- **a_16 = (4037 + 128 f)/(2·3¹⁵)** and **a_18 = (123404 − 2016 f)/3¹⁹**, exactly, on all 11 polytypes.
- So the series first differs at 16 bonds, by +64·3⁻¹⁵·f, with h higher.
  - It comes mainly from connected 16-bond even subgraphs made of two rings that meet at exactly two vertices (two degree-4 vertices). There are 7 per site in 2H and 4 in 3C, each with weight 3⁻¹².
  - Figure-eights (450 per site in 2H, 456 in 3C, weight 3⁻¹⁴) and overlapping pairs pull back slightly.
  - Total: (189 + 3)·3⁻¹⁶ = 64·3⁻¹⁵.
- **Control:** summed over all sites, the cluster expansion equals brute-force ln Σ_F over the whole cycle space on 4 finite pieces of the networks (cycle-space dimensions 20, 20, 21, 23). Every coefficient to y¹⁸ matches.

**What this says about physics, and what it does not.**
- The sign at the first differing order agrees with the known inequality S_h ≥ S_c (Onsager; Li et al. 2024; Chen–Ran 2026).
- It is consistent with Tindall–Sommers–Kappen 2026, whose Nagle-graded series (degree-2 vertices) is equal for Ic and Ih at order 6 and differs at order 14.
- The order-18 term has the opposite sign. **We claim nothing about the full sum**, and nothing about whether S_h = S_c.

## 3. Controls (all passed; `data/CHECKS.txt`)

**Positive controls:**
- NB loops at every tested site equal #102's values (24, 48, 480, 3432, 25704, 194256, 1509072, 11820000 for m = 6…20) for all stackings. This is Loop Equality, re-checked.
- Diamond cycles = 2·A038515 to l = 24.
- Coordination sequences: 3C gives 1, 4, 12, 24, 42, 64, 92, … and 2H gives A008264 (1, 4, 12, 25, 44, 67, 96, …).
- 12 six-rings at Ih and Ic sites (Herrero–Ramírez).
- No odd cycles.
- Letters outside the window and the window size do not matter.
- Fibonacci results do not depend on the window.
- Cluster expansion = brute force (4 pieces).
- The analysis confirms that the window-edge bilayers ±5 are never needed.

**Negative controls:**
- A deliberately wrong expectation (12-cycles of diamond = 1129) is rejected, while its true twin (1128) is accepted.
- A network with one bond moved breaks Loop Equality at the site.

## 4. Files

- **`scripts/rings_core.c`**: exact enumeration of cycles through a site, with the SP test and per-bond tallies. It exits if the network window is too small.
- **`scripts/rings.py`**: network, stackings, NB loops, King/Guttman rings, the strong-ring span check, the ice cluster expansion, and the modes `named`, `local`, `fib`, `icecontrol`, `negative`, `analyze`.
- **`scripts/diag.py`**: crossing profiles of the cycles.
- **`scripts/pilot.sh`, `scripts/run_full.sh`**: the job scripts.
- **`data/full/`**: the raw outputs.
  - `named-*.txt`: every site of every bilayer of 11 polytypes. Cycles and SP rings to 24, per bond, King/Guttman, strong check, ice series, cluster counts.
  - `local-*.txt`: 2048 words × 2 sites, to l = 20.
  - `analyze.txt`: the formulas.
  - `fib.txt`, `icecontrol.txt`, `negative.txt`, `diag.txt`.
- **`data/pilot/`**: the pilot outputs.
- **`logs/`**: the job logs. They end in FINAL ok: ringstack-pilot, ringstack, ringdiag.
- **`LITERATURE.md`**: every source and query checked.

Runs (on the compute hosts, through the job gate):
- ringstack-pilot: 0.5 min.
- ringstack: 26 parts in parallel, about 35 min, 27/27 ALLCHECKS ok.
- ringdiag: about 30 min.

## 5. Credit

- The network, the stackings and Loop Equality are from DICTO's #74 and #102.
- Ring definitions: King 1967, Guttman 1990, Franzblau 1991, Goetzke–Klein 1991, Yuan–Cormack 2002.
- Ih/Ic ring statistics: Herrero–Ramírez 2013.
- Diamond polygon data: Guttmann–Jensen 2009 (OEIS A038515).
- Ice series form: Nagle 1966, as written by Chen–Ran 2026.
- Computations: Claude, for DICTO.

## 6. Lean feasibility (not started)

**The statement is small.** It reuses the #102 Challenge definitions (stacking word, network, `Bond`) and adds the number of simple cycles of length l through a site, as `SimpleGraph.Walk.IsCycle` up to rotation and reversal, or as a `Finset` of vertex lists. About 60–120 Challenge lines.

Possible theorems:
- (A) For every stacking, every site, and l ≤ 16: p_l is the 3C value.
- (B) p18 at a site = 349236 − 12h[−2] − 30h[−1] − 42h[0] − 24h[1] (Theorem 1). Its corollary m\* = 18 needs only 3C ≠ 2H.

**The proof by the route used here is large and probably out of reach without `native_decide`.**
- Locality: a cycle of length l stays within l/4 + 1 bilayers and within a bounded in-plane disc. This is about 300–600 lines, in the style of #102's window lemmas.
- After locality, the theorem is a finite check: 2⁴ local patterns for (B), but each needs about 349,000 cycles enumerated in a graph of about 1500 vertices. The kernel's `decide` cannot do that, and Palomar bans `native_decide`. A verified enumeration by reflection in the kernel would be a research project in itself.
- (A) alone faces the same problem (50,016 cycles per site).
- **A feasible route needs a structural proof first.** One candidate: a bijection between the cycles of c and h that cross every bilayer at most twice (the diagnostic says these are equinumerous to l = 20), plus an explicit count of the four-crossing cycles. If such a bijection exists, the Lean proof might be about 2,000–4,000 lines on top of #102.

**The strong-ring blindness** (every stacking's cycle space is spanned by its six-rings) has a short statement. Its proof needs a cell-complex or cage argument that Mathlib does not have for graphs. That is large, and its notability is low on its own.

**Recommendation:** Theorems 1–3 are a natural paper section ("where Loop Equality stops"), and the answer to the reviewer's question. For Palomar, first look for the bijective explanation of §2.5; without it the formal proof is not practical.

CONCLUSION:
- Ring statistics are stacking-blind (known for Ih/Ic; all stackings here).
- Polygons first differ at length 18, with the exact local law p18 = 349236 − 12h[−2] − 30h[−1] − 42h[0] − 24h[1].
- Ice series first differ at 16 bonds, +64·3⁻¹⁵ f.
- STATUS: computed and checked; not yet written into #102 or a new paper.

LEADS:
1. A bijective proof of the equality of cycles that cross every bilayer at most twice. It would explain m\* and make Lean feasible.
2. The local formula at l = 22, 24 (W = 6 word run). Find the pair term behind 108 b.
3. Local per-site ice coefficients (they need a site convention) and the order-20 term.
4. Ask DICTO where this goes: #102 v-next as "where the equality stops", or a separate note. Where to place it is DICTO's choice.
