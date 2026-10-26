# Stage 0: is the #57 piece census more than the h/c statistics? (DICTO 10-26)

Question (from DICTO's paper57-analysis-and-development.md): could the Rule of Halves give crystallography a new structural descriptor?

Answer, exact (census_check.py on #57's appendix.json, ALL PASS, 28 checks, sympy on dicto-big-brother):

1. **Census = pair statistics.** By #57, each layer owns two tetrahedral pieces of its own type (c or h), and each gap owns one octahedral piece fixed by the (below, above) types. So the full piece census of any stacking, at any weight, is fixed by the numbers of c and h layers and of neighbouring pairs cc, ch, hc, hh: the first- and second-order statistics of the Jagodzinski h/c sequence, which crystallography already records. As a *descriptor* the census adds no information.
2. **Mean rule checked on every interval** of the weight walk: O(c over h) = O(h over c) = (O(cc) + O(hh))/2.
3. **Corollary (new, exact): the split of space between tetrahedral and octahedral pieces depends only on the hexagonality**, the fraction of h layers, at every weight; not on the order of the layers. Proof: each layer is "below" once and "above" once, so by the mean rule the sum of octahedral volumes equals the sum of the pure ones layer by layer. Checked on hhcc/hchc, hhhccc/hchchc, hhccc/hchcc.
4. Each layer takes the same total space in c and h (2 tets + one octahedral share), as it must.

**What is new is geometric, not informational:** the exact shapes and volumes, the halves, and corollary 3. Public text must not claim #57 gives crystallography new information about a stacking. Real polytypes (SiC, ZnS) also put atoms in half the tetrahedral holes, so the equal-ball model does not map onto them directly.
