# Local gpt-oss-120b read of the paper under review

**Referee Report – “The Rule of Halves: the Holes of Every Close‑Packed Stacking”**  

Below I list the points that, in my view, a careful referee would raise before recommending publication.  The comments are grouped as requested:

---

### 1.  Mathematical claims that appear wrong or insufficiently proved  

| # | Claim (quoted) | Issue / Why the proof is not complete |
|---|----------------|---------------------------------------|
| 1 | *“The pieces of the holes of gap k depend only on the layers k‑2,…,k+3.”* (Step 1) | The argument rests on three ingredients: (i) an exhaustive computer check of 176 “windows”, (ii) a hand‑derived distance bound, and (iii) a convexity argument.  The distance bound uses the inequality “\((|q‑p|^{2}+w_{p}-w_{q})/(2|q-p|) \ge ((2.5d)^{2}-11/24)/(5d)\)”.  No justification is given that the constant 2.5 d is the *smallest* possible separation for any hole three gaps away; a more careful geometric analysis (or a reference) is needed.  Moreover, the convexity argument (“squared distance along a straight path is convex in λ”) is stated without proof; convexity of a quadratic function of λ is trivial, but the dependence of the *corner* on λ is only asserted to be affine (Lemma 1).  A rigorous statement that the corner stays inside the ball of radius √½ for the whole stretch would require an explicit bound on the affine coefficients.  As written the proof leaves a gap. |
| 2 | *“Lemma 1. … the corner is … affine in λ.”* | The proof says the three defining planes have normals independent of λ and right‑hand sides affine in λ, then concludes the corner is a fixed matrix times an affine function of λ.  This is true only if the three planes remain linearly independent for the whole stretch; the lemma does not address the possibility that two planes become parallel (a “stop”).  A stop is later handled separately, but Lemma 1 should explicitly state the condition “as long as the three planes remain distinct”. |
| 3 | *“The volume of an octahedral piece is the mean of the volumes of its cubic and hexagonal parents (or equal to the parent’s, when both layers have the same type).”* (Corollary (ii)) | The argument given is: each pure octahedral piece has a centre of symmetry, so its two halves have equal volume; the mixed piece is “half of one parent and half of the other”.  This reasoning shows the *top* half has the same volume as the *bottom* half of the same pure piece, but it does **not** prove that the *mixed* piece’s total volume equals the arithmetic mean of the two pure volumes for *all* λ.  The mixed piece’s shape changes with λ, and the claim that the top half’s volume equals the top‑half volume of the cubic parent while the bottom half equals that of the hexagonal parent needs a precise statement (e.g. “the top half of the mixed piece coincides with the top half of the cubic piece for the same λ”).  The current proof only sketches the idea and does not verify that the two halves together indeed sum to the mean. |
| 4 | *“There are finitely many pieces in all close‑packed stackings together: 21 combinatorial kinds.”* | The enumeration of 21 kinds is based on the 16 “windows” and the stretches inside each window.  However, the paper does not explain why the list of windows is exhaustive for *all* infinite stackings (including aperiodic ones).  The statement “six layers decide” is used, but the proof that any stacking can be locally embedded in a periodic stacking containing the same six layers is only sketched.  A rigorous argument (or a citation to a known result on the locality of power diagrams for periodic point sets) is required. |
| 5 | *“The rule was not found in the sources checked; its classical counterpart … is the reason the h/c notation … exists.”* | The claim of novelty is strong, but the literature search described is informal (“eight queries”, “five web searches”, “local model”).  It is possible that similar statements appear in the extensive literature on Voronoi cells of FCC/HCP mixtures (e.g. in works on “polytypic Voronoi cells” or “layer‑dependent Voronoi decompositions”).  A more systematic review (including older crystallography monographs, the Hales decomposition‑star literature, and recent computational geometry papers) is needed before asserting originality. |

---

### 2.  Claims of novelty that may be too strong  

| # | Claim (quoted) | Why it may be overstated |
|---|----------------|--------------------------|
| 1 | *“The rule of halves … was not found in the sources checked.”* | The search description is vague; many crystallography texts discuss “layer‑dependent Voronoi cells” and the “h/c notation” without using the term “rule of halves”.  The author should either provide a more exhaustive bibliography or phrase the claim more modestly (e.g. “to the best of our knowledge …”). |
| 2 | *“Our theorem is the counterpart for the holes, along the whole walk.”* | The “whole walk” (λ varying from –11/24 to 3/8) is a specific one‑parameter family of weighted power diagrams.  Similar families have been studied in the context of “Laguerre tessellations of close‑packed sphere packings” (see e.g. An, Wang et al., 2005).  The author should acknowledge that related families have been examined, even if the exact statement of the rule is new. |
| 3 | *“The pieces of the holes of mixed stackings … are finite catalogue.”* | Finite‑type classifications of Voronoi cells for periodic packings are known (e.g. in the work of Delone & Dolbilin, 1991).  The claim should be qualified (“for the specific weight walk considered here”). |

---

### 3.  Unclear explanations that a reader would stumble on  

| # | Passage (quoted) | Problem |
|---|-------------------|---------|
| 1 | *“The walk is λ sliding over –11/24 ≤ λ ≤ 3/8, the range in which, in at least one of the two pure stackings, both kinds of piece are present …”* | The definition of the “walk” is never made precise: what does “sliding λ” mean for the power diagram?  How does λ affect the weights of the tetrahedral sites (λ) and octahedral sites (0)?  A short formal definition (e.g. “for each λ we set w_{tet}=λ and w_{oct}=0”) would help. |
| 2 | *“Step 1: six layers decide. … (i) Exact computation. … (ii) By hand. … (iii) Convexity.”* | The three sub‑steps are described in a very terse style.  The reader is left wondering: what exactly is being computed in (i)?  What is the “census engine of #53”?  How does (iii) follow from (i) and (ii)?  A more explicit roadmap would make the argument easier to follow. |
| 3 | *“The same three planes, with independent normals, define the corner, so the corner is a fixed matrix times an affine function of λ, hence affine in λ.”* | The phrase “with independent normals” is contradictory: normals of three planes are *linearly independent* (i.e. not parallel), not “independent”.  Moreover, the “fixed matrix” is not defined.  This sentence obscures rather than clarifies Lemma 1. |
| 4 | *“The windows are finitely many and so are their stretches.”* | The term “window” is introduced only in Step 1, but never formally defined (is it a pattern of six layers? a set of admissible (k‑1,…,k+2) types?).  Likewise “stretch” is used without a precise definition (open interval of λ between two “stops”). |
| 5 | *“Stops”* | The notion of a “stop” (where a piece changes its faces) appears only in the proof of the theorem, but the paper never defines it earlier, nor explains how many stops exist or how they are identified. |
| 6 | *Figures* | The manuscript refers to several figures (Fig. 1, Fig. 2, Fig. 3) that are not included in the PDF.  Since the visualisation of the pieces is central to the claim, the figures must be present. |
| 7 | *Appendix table* | The table in the Appendix uses a compact notation (e.g. “tetrahedral (-11/24, -3/8) … 4 4 triangles … √2·(24·λ + 11)³/6144”).  It is not explained what the first two numbers in parentheses mean (presumably the λ‑interval), nor how to interpret “4 4 triangles”.  A legend is needed. |
| 8 | *“The proof was read by an independent local model acting as referee; it found no mathematical error and asked for the additions now in this section.”* | This statement is unusual for a research article and raises questions about the peer‑review process.  It would be better to acknowledge the assistance of a colleague or a formal verification tool, rather than a “local model”. |

---

### 4.  Missing elements that a referee would normally request  

| # | Missing item | Suggested addition |
|---|--------------|--------------------|
| 1 | **Precise definitions** of “piece”, “hole”, “weight walk”, “stop”, “window”, “stretch”. | Include a short formal subsection (e.g. 2.1) with notation and definitions before the theorem. |
| 2 | **Proof of Lemma 1** with a clear statement of the condition “as long as the three planes remain distinct”. | Provide a short algebraic derivation (solve the linear system) and discuss what happens at a stop. |
| 3 | **Justification of the distance bound** in Step 1(ii). | Either give a geometric lemma (with a diagram) showing that any hole three gaps away is at least 2.5 d away, or cite a known result. |
| 4 | **Explanation of the computational verification**: what software, how rational arithmetic is ensured, how periodic boundary conditions are handled, and how the 176 cases are generated. | A brief “Computational methods” paragraph, plus a reference to the repository with a checksum of the data. |
| 5 | **Discussion of degenerate λ‑values** (the endpoints –11/24, –3/8, 3/8).  At these values some tetrahedral pieces shrink to points; the paper should explain how the theorem is interpreted there (limits, continuity). | Add a remark after the theorem stating the behaviour at the endpoints. |
| 6 | **Comparison with existing literature** on Voronoi (Laguerre) cells of FCC/HCP mixtures. | Cite at least one additional source (e.g. Delone & Dolbilin, “Geometry of Positive Quadratic Forms”, 1991; or recent computational geometry papers on polytypic Voronoi diagrams). |
| 7 | **Figures** showing the three new pieces (Chucky, Fang, Triskelion Tetrahedron) and a schematic of the weight walk. | Insert the missing figures or provide high‑resolution PDFs as supplementary material. |
| 8 | **Explicit statement of the corollary** that the number of combinatorial types is 21, together with a short proof (e.g. count of windows × stretches). | A paragraph summarising the counting argument. |
| 9 | **Clarification of the notation in the Appendix table** (what each column means, units, and how the volume formulas were derived). | Add a caption or a legend. |
|10| **Ethical statement** regarding the use of AI tools (Claude, gpt‑oss‑120b). | Many journals now require a brief statement of the role of AI in writing. |

---

### Summary  

The paper presents an interesting observation about weighted power diagrams of close‑packed stackings and supplies a large amount of computational data.  However, the current manuscript leaves several mathematical gaps (especially the locality argument and the volume‑mean claim), uses informal language for key concepts, and makes strong novelty statements without a sufficiently thorough literature review.  Moreover, essential definitions and figures are missing, and the computational verification is not described in enough detail for reproducibility.

**Recommendation:** *Major revision.*  The authors should address the points above—particularly the rigorous justification of Step 1, a precise definition of all terminology, a more modest claim of originality, and the inclusion of the missing figures and a clearer Appendix—before the paper can be considered for publication.


_usage: {'completion_tokens': 3520, 'prompt_tokens': 6184, 'total_tokens': 9704, 'prompt_tokens_details': {'cached_tokens': 0}}_
DONE
