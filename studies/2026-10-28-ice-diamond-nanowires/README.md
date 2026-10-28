# Ice, diamond and nanowires: the Hexagonality Law on tetrahedral networks (DICTO 10-28) — Real Materials V, last of the materials line
All three are close-packed layers of tetrahedral units: ice Ih/Ic (O on lonsdaleite/diamond net), diamond/lonsdaleite (C),
III-V nanowires zinc blende/wurtzite (GaAs, InP). Stacking-disordered ice and diamond are measured by "cubicity" = 1 - h.
Plan: 1. exact counts on any stacking (eclipsed bonds, boat rings, 3rd-neighbour distances) from coordinates;
2. data: polytype energies/volumes/gaps (Panse, Kriegner, Bechstedt 2011 GaAs/InP...; carbon polytypes; ice Isd);
3. prior art: Jagodzinski h; Choyke/Bechstedt gap vs hexagonality in SiC; Cheng-Heine-Needs ANNNI; Malkin/Kuhs ice Isd.

## Progress 10-28: 1. Exact counts (tetra_counts.py, .out) — DONE
Tetrahedral network on any stacking (3C, 2H, 4H, 6H, 9R, 15R): per atom 2 bonds; eclipsed bonds h/2; eclipsed third-neighbour pairs
3h/2 (at 5/3 bond length; staggered ones at 1.915 and 2.517; 2.333 appears only with h > 0). Exact on all six.

## Progress 10-28: 2. III-V nanowire polytypes, bands (iii_v_bands.py, .out) — DONE
Belabbes, Panse, Furthmueller, Bechstedt, arXiv 1206.2209 (PRB 86, 075208 (2012)), Table II: 6 compounds x 3C/6H/4H/2H.
Deviation from the 3C->2H law line at 6H and 4H, as % of the full change: conduction-band offset 4% (mean), crystal-field
splitting 7%, valence offset 10%, direct gap ~11% (GaP excluded: 3C indirect). Best: dEc and Delta_cf.
PRIOR ART: Belabbes et al. themselves plot against "hexagonality h" (their Fig. 2, c/a) and call trends monotonic; Bechstedt's
group (Panse et al. PRB 84, 075217 (2011)) did energies per pair vs h. New here: the straight-line test with numbers.
Energies per pair (Panse 2011) not open; Dacal & Cantarero InP (PMC5036193) has no polytype energy table. Still to get: energies.

## Progress 10-28: 3. Diamond and group IV (group_iv.py, .out) — DONE
Keller et al. arXiv 2302.10822 Table I (Si, Ge energies, volumes) + Table II; Ziembicki et al. arXiv 2404.05718 Table III (ANNNI C,Si,Ge,Sn,SiC).
Distance from the law (|J2|+|J3|)/J1: Sn 0.02, Ge 0.08, diamond C 0.15 (like cobalt/iron), Si 0.32, SiC 1.03.
Energies: Ge 4H/6H within 6% of the change of the law line; Si 21-24% below. Volumes: changes only 0.1-0.2% and not law-shaped.
Reading: SiC, the most polytypic material known, is the one furthest from the law; Sn and Ge, nearly on it, show few polytypes.
Next: ice (Tonauer et al. 2023 Ic->Ih -37.7 J/mol, PMC10240532; Malkin et al. 2012/2015 Isd cubicity); counts: eclipsed H-bonds h/2.

## Progress 10-28: 4. Ice — DONE (data + prediction)
Tonauer, Yamashita, del Rosso, Celli, Loerting, J. Phys. Chem. Lett. 14, 5055 (2023) (loerting.at PDF, read): pure cubic ice Ic -> Ih
dH = -37.7 +- 2.3 J/mol (9 runs), T 226 K; dG(c->h) = -16.5 J/mol cited; literature Isd -> Ih values scatter <-10 to -160 J/mol,
partly from differing cubicity, partly calorimetry artefacts; "ice Isd with significant hexagonal stacking faults will inevitably
show a less negative dH" and smaller vapour-pressure excess (their words, qualitative).
Law (J2 = J3 = 0) makes it quantitative: dH(Isd -> Ih) = -37.7 x cubicity J/mol; vapour-pressure excess of Isd over Ih
= cubicity x that of Ic (ln p ratio = cubicity x 16.5/RT ~ 0.9% at 226 K for Ic). Testable PREDICTION, not tested (no paired
cubicity+enthalpy data found). Exact count: eclipsed hydrogen bonds per molecule = h/2 (= (1 - cubicity)/2), tetra_counts.py.
Sources checked: Tonauer et al. 2023 (read); Malkin et al. PNAS 2012 and PCCP 2015 (search summaries); arXiv 2607.03465 (summary:
nucleus cubicity ~0.35 rising to ~0.62); Hondoh 2015 (summary: 13-50 J/mol by preparation).
CONCLUSION (study): tetrahedral networks obey the exact counts (eclipsed bonds h/2); III-V nanowire band offsets and crystal-field
splitting lie on the law line within 4-7%; energies rank the elements by distance from the law (Sn 0.02 < Ge 0.08 < C 0.15 < Si 0.32
< SiC 1.03), and the most polytypic, SiC, is furthest; ice gives a clean prediction for clouds. Ready for Real Materials V (#73).
