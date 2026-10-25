# Local gpt-oss-120b read of the paper under review

**Referee Report – points to be addressed**

Below I list the items that, in my view, require clarification, additional justification, or correction before the manuscript can be accepted.  I quote the relevant sentences verbatim and then explain the problem.

---

### (1) Mathematical claims that appear unproved or questionable  

1. **Locality claim (Step 1).**  
   > “*Claim: the cells of the sites of gap k are determined by the six layers k−2,…,k+3.*”  

   The argument consists of three sub‑steps (i)–(iii).  Sub‑step (i) is a *computer check* on the 16 possible type‑patterns; sub‑step (ii) gives a hand‑derived distance bound; sub‑step (iii) uses a convexity argument that the “far constraints miss the closed ball of radius √½ about p”.  None of these pieces constitute a rigorous, *mathematical* proof that the six‑layer neighbourhood is sufficient for *all* possible (aperiodic) stackings.  In particular:

   * The bound in (ii) uses the inequality  
     \[
     \frac{(|q-p|^{2}+w_{p}-w_{q})}{2|q-p|}\ge\frac{(2.5d)^{2}-11/24}{2\cdot2.5d},
     \]  
     but the derivation of the numerical value \(23763/28800>1/2\) is omitted, and it is not shown that this lower bound is *sharp* for every admissible λ.  A short calculation should be inserted, or a reference to a lemma that guarantees the bound for the whole λ‑interval.

   * The convexity argument in (iii) assumes that “all far constraints miss the closed ball of radius √½ about p”.  This is asserted without proof; one needs to show that for any site q outside the six‑layer window the corresponding radical plane lies entirely outside that ball for *every* λ in the prescribed interval.  The statement “C_W lies in that ball (i)” is also not justified: why does the cell computed from the periodic test stacking automatically stay inside the ball?

2. **Affineness of corner functions (Step 2).**  
   > “*Equality of affine corner functions gives equality of the cells (convex hulls) for every λ in the stretch;*”  

   It is claimed that each corner of a cell moves affinely with λ.  No argument is given why the intersection of two radical planes (each defined by a linear expression in λ) yields an affine dependence; the possibility of a *piecewise* linear behaviour at the endpoints of a stretch is not excluded.  A short lemma (e.g. “the intersection of two families of planes whose coefficients are affine in λ is itself affine as long as the planes remain non‑parallel”) should be added, together with a justification that the non‑parallel condition holds throughout each stretch.

3. **“Stops” and continuity (Step 3).**  
   > “*At the finitely many stop values the cells are the limits of the cells on the adjacent stretches (checked: the limit equals the cell computed directly at the stop), so the congruences persist.*”  

   The term “stop values” is never defined earlier.  Moreover, the statement that “the limit equals the cell computed directly at the stop” is again a *computer verification* claim without any description of how the limit was taken or how the direct computation was performed.  A rigorous argument (or at least a precise definition of a stop value and a proof that the power diagram varies continuously in λ) is needed.

4. **Corollary about finiteness of pieces.**  
   > “*The catalogue of all pieces of all close‑packed stackings is finite (21 combinatorial types).*”  

   The proof of finiteness relies entirely on the exhaustive computer check of the 16 windows and the claim that each window yields a unique combinatorial type.  However, the manuscript does not explain why *no* new combinatorial type can arise from longer-range interactions (e.g. from a pattern that repeats only after more than six layers).  The locality claim of Step 1 is supposed to guarantee this, but as noted above the locality proof is incomplete.  Consequently the finiteness statement is not fully justified.

---

### (2) Claims of novelty that may be overstated  

1. **“The catalogue of all pieces … is finite (21 combinatorial types).”**  
   The authors present this as a new classification result.  To the best of my knowledge, similar finiteness statements have appeared in the literature on Voronoi (or Dirichlet) cells of close‑packed sphere packings (e.g. in works by Conway & Sloane, and by Torquato & Stillinger).  The manuscript does not cite any of these prior results, nor does it explain how the present 21 types differ from previously known classifications.  Without a clear comparison, the claim of novelty is too strong.

2. **“Fang and Chucky (new pieces of the double‑hexagonal stacking ABAC) are each a cubic half glued to a hexagonal half; the tetrahedral piece TT is the cubic piece.”**  
   The names “Fang” and “Chucky” are introduced without any reference or definition.  If these are new objects, the authors should provide a precise description (or a figure) and a citation to a pre‑print or to a forthcoming work.  Otherwise the statement reads as an unsubstantiated claim of discovery.

---

### (3) Unclear explanations that would hinder a reader  

1. **Definition of “piece”, “cubic half”, “hexagonal half”.**  
   The terms appear in the theorem and corollary but are never formally defined.  A reader cannot tell whether a “cubic half” refers to the upper (or lower) half of an octahedral cell in a cubic stacking, or to some other geometric object.

2. **Notation for layers and positions.**  
   The manuscript uses “positions A, B, C” and later “position X, Y, Z” without a clear diagram.  While the text says “the octahedral hole over the third position Z”, it is not obvious which of the three possible positions is “the third”.  A small schematic of a single gap with the three possible layer positions and the three interstitial sites would eliminate this ambiguity.

3. **Weight assignment and λ‑range.**  
   The choice “w_oct = 0, w_tet = λ” and the admissible interval “−11/24 ≤ λ ≤ 3/8” are justified only by the parenthetical “outside this range one kind of cell is empty”.  No proof or reference is given for why exactly these bounds are the maximal interval for non‑empty cells.  A short argument (or a citation) would make the statement transparent.

4. **“Symmetry g of the layer lattice about the site’s vertical axis (the 12 plane symmetries of the triangular lattice, with or without the reflection z↦−z: 24 maps)”.**  
   It is unclear whether the reflection in z is actually a symmetry of the *weighted* configuration (since the weights differ for tetrahedral and octahedral sites).  The reader is left to guess why the full 24‑element group can be applied to the corner functions.

5. **“The program verifies on each stretch that its finite site list suffices and that cell volumes add up to the lattice cell.”**  
   No description of the program (language, libraries, verification methodology) is provided, nor is the output (e.g. a table of stretches) shown.  Without this, the claim that the program “verifies” the statement is not reproducible.

---

### (4) Missing material that a referee would normally request  

1. **Explicit description of the computational verification.**  
   * Provide the source code (or a repository link) and a description of the algorithm used to compute the power diagram exactly (e.g. rational arithmetic with exact arithmetic libraries).  
   * Include a table listing the 16 type‑patterns, the λ‑intervals (stretches) where the combinatorial structure changes, and the corresponding numbers of cells/corners.  

2. **Proof that the λ‑interval is optimal.**  
   * Show (or cite) that for λ < −11/24 a tetrahedral cell disappears, and for λ > 3/8 an octahedral cell disappears.  This can be done by a simple distance comparison, but it should be presented.

3. **Figures.**  
   * At least two figures: (i) a schematic of a single gap showing the three layer positions (A, B, C) and the three interstitial sites (octahedral and the two tetrahedral holes); (ii) an illustration of a “cubic half” and a “hexagonal half” of an octahedral cell, to make the statement of the theorem concrete.

4. **References to prior work.**  
   * Cite earlier studies on Voronoi/Dirichlet cells in close‑packed sphere packings (e.g. Conway & Sloane, *Sphere Packings, Lattices and Groups*; Torquato & Stillinger, “New conjectural lower bounds on the maximal density of sphere packings”).  
   * If the “catalogue of 21 types” is new, explain how it refines or extends these earlier classifications.

5. **Definition of “stop values”.**  
   * Give a precise definition (e.g. λ at which two corner functions become equal, causing a combinatorial change) and explain why there are only finitely many such values.

6. **Discussion of the implications.**  
   * The theorem is presented without any context: why is the “rule of halves” interesting?  How does it relate to physical properties of close‑packed structures (e.g. stability, defect formation)?  A short discussion would help readers understand the significance.

7. **Notation consistency.**  
   * In the statement of the theorem the phrase “the cell of a tetrahedral site is congruent to the cell of a tetrahedral site of the pure stacking of the type (c or h) of the layer nearest to the site” is cumbersome.  It would be clearer to introduce a notation such as \(C^{\mathrm{tet}}_{k+3/4}\) and \(C^{\mathrm{tet}}_{\mathrm{pure}}(h)\) etc., and then write the congruence succinctly.

---

### Summary  

The manuscript contains an intriguing observation about the geometry of weighted power diagrams in close‑packed stackings, but the current proof relies heavily on undocumented computer checks and on a locality argument that is not fully justified.  Moreover, several key definitions are missing, the novelty claims are not contextualised, and the exposition would benefit from figures and a more detailed description of the computational methodology.

I recommend **major revision**: the authors should (i) supply a rigorous, self‑contained proof of the six‑layer locality, (ii) provide the code and a reproducible data set for the exhaustive verification, (iii) clarify all terminology and include illustrative figures, and (iv) situate the result within the existing literature and temper the novelty statements accordingly.  Once these issues are addressed, the paper may be suitable for publication.


_usage: {'completion_tokens': 2837, 'prompt_tokens': 1554, 'total_tokens': 4391, 'prompt_tokens_details': {'cached_tokens': 0}}_
DONE
