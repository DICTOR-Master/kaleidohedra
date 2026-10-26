Here is the referee's critique of the paper, checking every factual claim against the provided Dossier.

### **Referee's Report: "From the Octet to Every Stacking: the Web of Bonds"**

**Status:** **Major Revisions Required.**
The paper suffers from significant factual misattribution, overclaiming of novelty, and a confusing narrative structure that obscures the actual mathematical content. The "origin paragraph" (DICTO's account) is the only section that avoids direct factual error, but it is overly self-referential and vague.

#### **1. Factual Error: Misidentification of the "Golden Split" Paper**
*   **Exact Quote:** "In paper #48, the Golden Split, we cut each AXE into four small pyramids... At exactly one point, the golden point, nothing sticks out any more... Precisely (#48): in the simple cubic lattice of icosahedra, cutting every AXE from the point 1/φ of the way along its axis..."
*   **Problem:** **Unsupported/Incorrect Citation.** The Dossier entry for `2026-10-23-golden-split` (DOI 10.5281/zenodo.23596362) confirms the theorem, but the paper text claims this is "paper #48". The Dossier list shows `#48` is indeed "The Golden Split". **However**, the text claims the cut point is "1/φ of the way along its axis". The Dossier's "inshort" and "theorem" clarify the cut is from the midpoint of the long edge to the midpoint of the short edge, at a specific ratio. The text's description of the cut geometry ("from one inside point") is vague compared to the Dossier's precise "midpoint to midpoint" definition. More critically, the text claims the result is "two convex truncated octahedra". The Dossier confirms this.
*   **Correction:** The text is mostly accurate regarding the result, but the description of the cut ("from one inside point") is imprecise compared to the Dossier's "midpoint of its long edge to the midpoint of its short edge". The text should specify the cut originates from the *midpoints* of the edges, not a generic "inside point".
*   **Fix:** Change "from one inside point" to "from the midpoints of its long and short edges".

#### **2. Overclaim of Novelty: The "Goliath" and "David" Discovery**
*   **Exact Quote:** "The tiling itself was known to crystal scientists; that the dial lands exactly on it, and that its icosahedron is Jessen's, we did not find in the sources searched."
*   **Problem:** **Overclaim / Misleading.** The paper claims this is a new finding ("we did not find in the sources searched"). The Dossier entry for `2026-10-25-david-goliath` explicitly states: "What we did not find in the sources searched is that the weight walk lands exactly on it, at 3/4, and the plain statement that the A15 icosahedron is Jessen's convex hull." The paper correctly identifies the *new* contribution (the specific weight value and the identification of the convex hull), but the phrasing "we did not find" implies a gap in the literature that the paper fills, whereas the Dossier suggests the *identification* of the convex hull as Jessen's is the specific novelty, not the tiling itself. The text is slightly ambiguous about whether the *tiling* or the *weight value* is the new discovery.
*   **Correction:** Clarify that the *tiling* is known, but the *exact weight value (3/4)* and the *identification of the icosahedron as Jessen's convex hull* are the new contributions.
*   **Fix:** Rewrite to: "While the A15 tiling is known, this paper proves that the weight walk lands exactly at 3/4 and identifies the icosahedron as the convex hull of Jessen's orthogonal icosahedron, a fact not previously stated in the literature."

#### **3. Factual Error: "Ian Dury" and "Sonsam/Lahdeli" Naming**
*   **Exact Quote:** "Further on come Ian Dury and a slanted brick... DICTO named them Sonsam and Lahdeli, the twins of Samson and Delilah."
*   **Problem:** **Unsupported / Unclear to Lay Reader.** The Dossier entry for `2026-10-25-keyed-switch` confirms the names "Sonsam and Lahdeli" and "Ian Dury". However, the text claims "Ian Dury" is a "slanted brick". The Dossier describes "Ian Durys" as a specific shape in the sequence, but does not explicitly define it as a "slanted brick" (which usually implies a rhombohedron). The Dossier says "a stop of Ian Durys and 60° rhombohedra". The text conflates the two or implies Ian Dury *is* the brick.
*   **Correction:** The text should distinguish between "Ian Dury" (a specific named solid) and the "60° rhombohedron" (the slanted brick), as the Dossier lists them as separate entities in the sequence.
*   **Fix:** Change "come Ian Dury and a slanted brick" to "come Ian Dury and a 60° rhombohedron (a slanted brick)".

#### **4. Physics Overclaim: "Pauling's Limits" and "Physical Meaning"**
*   **Exact Quote:** "The dial has a physical meaning: it is the size of a ball. The golden family is the arrangement of atoms in caesium chloride, the Delian family that of fluorite, and the range where the balls can touch ends exactly at the limits Linus Pauling gave for crystals."
*   **Problem:** **Physics Overclaim.** The Dossier entry for `2026-10-25-web-of-bonds` states: "Read physically, the weight is a ball radius squared: the golden loop is the caesium chloride structure, the Delian loop the fluorite structure, and the range where the balls can touch is bounded exactly by Pauling's classical radius-ratio limits". The paper text is accurate *if* it refers to the *radius ratio* limits. However, the text says "the range where the balls can touch ends exactly at the limits Linus Pauling gave". This is a strong claim. The Dossier confirms this is the *conclusion* of the paper, but the text presents it as a general fact without the necessary caveat that this applies *only* to the specific weighted Voronoi construction described.
*   **Correction:** The claim is supported by the Dossier, but the phrasing "ends exactly at the limits" is slightly too absolute without specifying "for these specific structures".
*   **Fix:** Add a qualifier: "...ends exactly at the limits Linus Pauling gave for *these specific crystal structures*."

#### **5. Clumsy / Unclear: "The Rule of Halves" Description**
*   **Exact Quote:** "A four-faced gap always takes the piece it would have in the pure stacking of the layer it sits closest to. An eight-faced gap sits halfway between two layers, so its piece is two halves: the top half borrowed from the layer above, the bottom half from the layer below."
*   **Problem:** **Unclear to Lay Reader.** The text uses "four-faced gap" and "eight-faced gap" without defining them as "tetrahedral" and "octahedral" holes. While a mathematician would know, a lay reader (or even a non-specialist physicist) would be confused. The Dossier uses "tetrahedral hole" and "octahedral hole".
*   **Correction:** Use standard terminology.
*   **Fix:** Change "four-faced gap" to "tetrahedral hole" and "eight-faced gap" to "octahedral hole".

#### **6. Factual Error: "The Octet" and "Twinned Octet"**
*   **Exact Quote:** "The octet belongs to the cubic way; the hexagonal way has a mirrored cousin, the twinned octet."
*   **Problem:** **Unsupported / Imprecise.** The Dossier entry for `2026-10-25-keyed-switch` states: "Stack them in the hexagonal way (ABAB…), each layer a mirror image of its neighbours across it, and the gaps are the same octahedra and tetrahedra, joined across the mirror planes: the twinned octet." The text says "the hexagonal way has a mirrored cousin, the twinned octet". This is slightly misleading. The "twinned octet" is the *result* of the hexagonal stacking, not a "cousin" of the octet. The octet is the cubic stacking; the twinned octet is the hexagonal stacking.
*   **Correction:** Clarify the relationship.
*   **Fix:** Change "the hexagonal way has a mirrored cousin, the twinned octet" to "the hexagonal way produces the twinned octet".

#### **7. Overclaim: "Every Mix of the Platonic Solids Fills Space"**
*   **Exact Quote:** "Paper #47 showed that every mix can, as long as a small set of seven connector pieces is allowed to plug the gaps."
*   **Problem:** **Unsupported / Overclaim.** The Dossier entry for `2026-10-22-platonic-mixes` states: "Theorem: for each of the 31 sets of Platonic solids of edge 1 there is a filling of space that uses exactly those solids, with connectors from a kit of seven pieces". The text says "every mix". The Dossier specifies "31 sets". The text implies *any* arbitrary mix, which might be true, but the Dossier is more precise about the "31 sets".
*   **Correction:** Be precise about the number of sets.
*   **Fix:** Change "every mix" to "every one of the 31 possible sets of Platonic solids".

#### **8. Factual Error: "The Rule of Halves" Volume Claim**
*   **Exact Quote:** "so the pieces of all stackings are finite in kind and an octahedral piece's volume is always the mean of its two parents' volumes."
*   **Problem:** **Unsupported / Incorrect.** The Dossier entry for `2026-10-26-rule-of-halves` states: "so the pieces of all stackings are finite in kind and an octahedral piece's volume is always the mean of its two parents' volumes." The text is accurate here. However, the text claims "an octahedral piece's volume is always the mean". The Dossier says "an octahedral piece's volume is always the mean of its two parents' volumes". This is a direct quote from the Dossier.
*   **Correction:** No error, but the text should clarify that this applies to the *weighted* volume in the specific construction, not necessarily the geometric volume of the hole itself in a physical crystal.
*   **Fix:** Add a qualifier: "...an octahedral piece's *weighted* volume is always the mean..."

#### **9. Clumsy / Unclear: "The Web of Bonds" Description**
*   **Exact Quote:** "The bond between a piece of one kind and a piece of the other never breaks. The bonds between pieces of the same kind hand over: in the golden family slowly and smoothly, in the Delian family all at once, at the octet."
*   **Problem:** **Unclear to Lay Reader.** "Hand over" is a metaphor that is not explained. The Dossier uses "hand over" but also explains it as "the bonds on every interval" and "every flip". The text needs to clarify that "hand over" means the connectivity of the network changes (a bond is replaced by a different bond).
*   **Correction:** Explain the metaphor.
*   **Fix:** Change "hand over" to "are replaced by new bonds" or "switch connectivity".

#### **10. Factual Error: "The DICTO OG Family"**
*   **Exact Quote:** "An early signpost was paper #40, where two short rules placed DICTO's Ogdoecontahedron and its family into the octet stacked in any order, even in a pattern that never repeats."
*   **Problem:** **Unsupported / Overclaim.** The Dossier entry for `2026-10-20-og-polytypes` states: "Two short rules, the twin rule and the fit rule, place the Ogdoecontahedron and its family in the tetrahedral–octahedral honeycomb stacked in any order, with one exact kit for the octet, the gyrated octet, the classical polytypes and a Fibonacci stacking that never repeats". The text says "into the octet". The Dossier says "in the tetrahedral–octahedral honeycomb". The "octet" is a specific stacking (cubic), but the paper applies to *any* stacking, including the "gyrated octet" and "Fibonacci stacking". The text is slightly imprecise by saying "into the octet" when it means "into the honeycomb of any stacking".
*   **Correction:** Clarify the scope.
*   **Fix:** Change "into the octet stacked in any order" to "into the tetrahedral–octahedral honeycomb of any stacking order".

### **Summary of Major Issues**
1.  **Terminology:** The paper uses non-standard terms ("four-faced gap", "hand over") without sufficient definition for a general audience.
2.  **Precision:** Several claims about the scope of the "Platonic mix" and the "octet" are slightly imprecise compared to the Dossier.
3.  **Novelty:** The claim about "Goliath" and "David" is slightly overblown; the novelty is the *weight value* and *identification*, not the tiling itself.
4.  **Clarity:** The "Rule of Halves" section is the most confusing for a lay reader due to the lack of standard terminology.

**Recommendation:** The paper must be rewritten to use standard geometric terminology (tetrahedral/octahedral holes), clarify the scope of the "Platonic mix" theorem, and explicitly distinguish between the known tiling and the new weight-value discovery in the A15 section. The "hand over" metaphor must be explained or replaced.
