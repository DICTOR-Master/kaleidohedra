# Literature: ring statistics of close-packed tetrahedral stackings (15 November 2026)

Free sources only. Everything listed was opened unless marked "abstract only" or "via citations".

## Findings that bear on the question

**1. Ring statistics of ice Ih and ice Ic are already known to be identical.**
C. P. Herrero and R. Ramírez, *Topological characterization of crystalline ice structures from coordination sequences*, Phys. Chem. Chem. Phys. 15, 16676 (2013); arXiv:1307.4611 (read in full via ar5iv).
- They use "fundamental rings": rings "that cannot be divided into two smaller ones". They credit this definition to Marians and Hobbs (1990).
- Table II: every site of Ih (both sites) and of Ic has 12 six-membered rings and no other rings.
- They write: "A distinct property of ices Ih and Ic is that all rings in their crystal structures have the same size (six-membered rings, L = 6)."
- Their coordination sequences first differ at the third shell (Ih 25, Ic 24).

So for the two end members, equality of primitive-ring statistics is **published**. Our computation reproduces it (control), and extends it to every stacking. Strong rings are covered by a proof, and SP rings, King rings and Guttman rings are covered by computation.

**2. Definitions of ring statistics.** The ISAACS manual, https://isaacs.sourceforge.io/phys/rings.html, read in full, gives these definitions with references:
- King's rings: S. V. King, Nature 213, 1112 (1967).
- Guttman's rings: L. Guttman, J. Non-Cryst. Solids 116, 145 (1990).
- Primitive (irreducible) rings: "cannot be decomposed into two smaller rings". K. Goetzke and H. J. Klein, J. Non-Cryst. Solids 127, 215 (1991); X. Yuan and A. N. Cormack, Comput. Mater. Sci. 24, 343 (2002). The term "irreducible" also appears in F. Wooten, Acta Cryst. A 58, 346 (2002).
- Strong rings: "cannot be decomposed into a sum of smaller rings whatever this sum is". Goetzke–Klein; Yuan–Cormack.
- D. S. Franzblau, *Computation of ring statistics for network models of solids*, Phys. Rev. B 44, 4925 (1991). Abstract only, via scilit: it introduces the shortest-path (SP) criterion within a hierarchy of criteria for irreducible rings. **The full text was not read**, because it is paywalled.
- The RINGS code (Le Roux and Jund) project page, https://sourceforge.net/projects/rings-code/, gives no definitions. Its documentation site redirects to that page. The code's paper was not read.

**3. Polygon (self-avoiding polygon) counts.**
- OEIS A038515 (closed 2n-step self-avoiding walks on the diamond net: 6, 12, 120, 564, 4074, 25008, 174618, 1181100, …), citing A. J. Guttmann and I. Jensen, *Polygons, Polyominoes and Polycubes*, LNP 775 (2009), Table 16.12. Opened: the entry and its b-file. With our normalisation, cycles through a site = 2·a(n). This is our positive control for diamond.
- OEIS searches for "lonsdaleite", "wurtzite", "tridymite" and "hexagonal diamond" returned only coordination sequences (A008264, A008524–A008526) and a theta series (A217511). **No polygon or ring series was found for lonsdaleite or for any other polytype.**
- G. R. Grimmett, *On counting polygons in a crystal*, arXiv:2601.01128 (2026), abstract only. It concerns growth rates in quasi-transitive graphs. Diamond, lonsdaleite and stackings are not mentioned.

**4. Ice Ic versus Ih, residual entropy (the physics side).**
- J. F. Nagle, *Lattice statistics of hydrogen bonded crystals. I. The residual entropy of ice*, J. Math. Phys. 7, 1484 (1966). Known via citations only (paywalled). His series gives 1.50685(15) for both Ih and Ic.
- Z. Chen and S. Ran, *Hexagonal stacking maximizes proton configurational entropy among ice-I polytypes*, arXiv:2608.07613 (Aug 2026). Read via the HTML page. They write Nagle's identity as Z(G) = (3/2)^N Σ_F 3^(−n₂(F)), the sum running over even subgraphs F. They prove that the hexagonal stacking maximises the ice-rule count among periodic polytypes, and they give the two coordination sequences. They give no loop-by-loop comparison.
- X.-Z. Xu, T.-Y. Lin and G.-M. Zhang, *Equivalence of residual entropy of hexagonal and cubic ices from tensor network methods*, arXiv:2511.22477; Phys. Rev. B 113, 214416 (2026). Abstract and HTML read. They argue numerically for S_h = S_c and quote Nagle's entry as identical for both.
- D.-Z. Li, Y.-J. Cen, X. Wang and X.-B. Yang, *Residual entropy of ice: a study based on transfer matrices*, arXiv:2404.13897; Phys. Rev. B 110, 195414 (2024). Abstract only. They show S_h ≥ S_c and attribute the argument to Onsager.
- J. Tindall, G. M. Sommers and H. Kappen, *Contracting tensor networks with generalized belief propagation*, arXiv:2604.24760 (Apr 2026). The PDF text was read.
  - Table II: Nagle's loop series truncated at n = 6 gives 1.504115 for both Ic and Ih. At n = 14 it gives 1.506362 for Ic and 1.506375 for Ih.
  - Footnote [52]: order n counts Eulerian subgraphs with up to n vertices of degree 2 and any number of degree-4 vertices.
  - So the two stackings' series **are known to differ somewhere between n = 6 and n = 14 in Nagle's grading**. The exact first order and the configurations responsible are not stated.
- C. P. Herrero and R. Ramírez, arXiv:1406.5929 (2014). Snippet only: w_h = 1.50786(12), w_c = 1.50778(11).
- J. Kolafa, J. Chem. Phys. 140, 204507 (2014). Via citations only.

**5. SiC polytypes and zeolite polytypes.**
- A search for ring or topology statistics of SiC polytypes (3C, 2H, 4H, 6H) found only crystallography: the Wikipedia page "Polymorphs of silicon carbide" and the TU Wien thesis node on SiC crystallography.
- For zeolites, the IZA *Database of Disordered Zeolite Structures* (FAU/EMT family, https://europe.iza-structure.org/IZA-SC/DO_structures/DO_family.php?ID=3) lists the same ring sizes (12, 6, 4) for the cubic (FAU) and hexagonal (EMT) end members. It gives sizes, not counts per site by length.
- No paper comparing ring counts across polytypes by length was found.

## Queries run (web search, 15 Nov 2026)
1. `ring statistics ice Ih ice Ic hexagonal cubic difference number of rings diamond lonsdaleite`
2. `Nagle residual entropy ice Ic Ih series loop expansion differ order polygons`
3. `self-avoiding polygons diamond lattice wurtzite lattice count differ polytypes`
4. `Chen Ran 2026 residual entropy hexagonal cubic ice arXiv loop`
5. `primitive rings diamond lattice lonsdaleite ring statistics King criterion Franzblau "lonsdaleite" rings per atom`
6. `Franzblau 1991 "Computation of ring statistics for network models of solids" primitive rings definition`
7. `Nagle 1966 ice series expansion "cubic ice" "hexagonal ice" identical terms first difference twelve loops figure eight` (extended search)
8. `SiC polytypes 3C 4H 6H 2H ring statistics topology "rings" stacking self-avoiding loops difference graph theory`
9. `Nagle "residual entropy of ice" series coefficients Ih Ic "agree" terms through order hexagonal cubic difference arises`
10. `"self-avoiding" polygons OR walks "hexagonal diamond" OR lonsdaleite OR "wurtzite lattice" enumeration series connective constant`
11. `zeolite intergrowth polytypes FAU EMT ring statistics identical topology stacking faults "ring" counts`
12. OEIS JSON search: `diamond lattice polygons`, `self-avoiding polygons diamond`, `polygons diamond lattice self-avoiding`, `2,3,24`, `diamond self-avoiding walks`, `lonsdaleite`, `wurtzite`, `tridymite`, `hexagonal diamond`.

The RCSR entry for lon (rcsr.anu.edu.au/nets/lon) could not be reached (connection refused). DICTO's library was not searched for this study.

## Verdict on priority
- **Known:** ring statistics (fundamental or primitive rings) are identical for Ih and Ic: 12 six-rings per site and nothing else (Herrero–Ramírez 2013). The Ih and Ic residual-entropy series in Nagle's grading are known to differ by order 14 (Tindall–Sommers–Kappen 2026, Table II). S_h ≥ S_c is known (Onsager; Li et al. 2024; Chen–Ran 2026).
- **Not found in the sources checked:**
  - the statement for every stacking (all four standard ring criteria blind to stacking);
  - the first polygon length at which any two stackings differ (l = 18) and its exact local formula;
  - polygon counts for lonsdaleite or any polytype other than diamond;
  - the first bond order at which the ice polymer series of two stackings differ (16), with its exact coefficients and local formula.
