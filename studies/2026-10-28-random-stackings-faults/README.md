# Random stackings and stacking faults under the Hexagonality Law (DICTO 10-28)
Status 10-28: results 1-3 done; Laves foot-atom test on 7- and 8-layer stackings running (dicto-big-brother).

## 1. Random stackings (corollary of #66, wherever its hypothesis holds)
For ANY stacking, repeating, faulted or random, each kind of piece averages exactly
   V(cc) + h (V(hh) - V(cc)) per layer, h = the fraction of hexagonal layers (the hexagonality),
independent of the order and of every correlation between layers (proof: #66, T = n_c V(cc) + n_h V(hh), applied to any long
stretch; the ends contribute at most two layers). So one measured number, h, fixes the exact hole volumes of a random stacking.
Physical cases where h is measured: hard-sphere colloids in random hexagonal close packing (stacking probability alpha, alpha = 1/2
completely random, so h = 1/2; Pusey et al. 1989; Kegel and Dhont 2000; Martelozzo et al. 2002); stacking-disordered ice I_sd
(cubicity = 1 - h, e.g. 73.3% cubic, Malkin et al. 2015; 78%, Amaya et al. 2017; Malkin et al. PNAS 2012). The ice framework is the
diamond/lonsdaleite stacking = our pyrochlore run (#60; zinc blende with mu = 0), where the law holds 96/96.
The SPLIT among the four kinds of piece (cc, ch, hc, hh) needs the pair statistics, not only h (Markov stacking models:
Hart, Hansen and Kuhs 2021; Ganesh and Nasr 2023); the TOTAL does not.

## 2. Stacking faults (scripts/faults.py, faults.json)
Change in hexagonal layers, Jagodzinski's rule, classical letter sequences:
  fcc twin +1, fcc intrinsic +2, fcc extrinsic +2  (1 : 2 : 2);  hcp I1 -1, hcp I2 -2, hcp E -3  (1 : 2 : 3).
By the law each fault changes the total of every kind of piece by exactly (change) x (V(hh) - V(cc)).
Rock salt / NiAs at lambda = 1/3 (fault_volumes_rocksalt.json), per hexagonal layer: ball +71/3456, octahedral hole -215/10368,
each tetrahedral hole +1/10368; the changes add to 0 (space is conserved: the balls gain exactly what the holes lose).
Physics: fault ENERGIES in the ANNNI picture are combinations of the polytype energies (e.g. E_ESF = 4(E_dhcp - E_fcc)/A; second
order E_ISF = (E_hcp + 2E_dhcp - 3E_fcc)/A); for hcp faults "to zeroth order the ordering of the energies can be understood in terms
of the number of fcc-like planes" (Mg study, search summary). Our ratios are the exact geometric counterpart, for volumes.

## 3. Ice / diamond
covered by #60's pyrochlore run (mu = 0 is "the pyrochlore / diamond run" in zincblende_mix.py).

## Sources checked (28 October 2026)
ask-library: "randomly stacked close packed colloidal crystals hexagonality stacking probability" (Ganesh-Nasr 2023; Hart-Hansen-
Kuhs 2021, catalogue abstracts); "stacking fault energy intrinsic extrinsic twin ratio fcc hcp ANNNI" (Howie-Marks 1984, Marks 1984,
Hofmeister 1998: twinned particles, not relevant); "hydrogen interstitial octahedral tetrahedral sites fcc hcp" (nothing relevant).
Web search summaries (not full texts): Martelozzo et al. 2002 (era.ed.ac.uk); Kegel-Dhont 2000 (dspace.library.uu.nl); arXiv
1406.7697; Malkin et al. 2012 PNAS and later cubicities (arXiv 1812.04333; J. Appl. Cryst. 2018 summary; RSC PCCP 2015 c4cp02893g);
ANNNI fault energies: arXiv 1704.00313, 2111.03591, 2405.04876, 1505.00431, PRB 56 10844, Leoben DFT Cu Ag Au.
