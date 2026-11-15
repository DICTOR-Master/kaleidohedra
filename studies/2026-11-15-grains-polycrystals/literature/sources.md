# GRAINS: sources checked (15 Nov 2026; free sources only)

Marks: FT = full text read · AB = abstract or landing page only · 2nd = known from another paper · memory = recalled, not checked.
Read by two literature passes on 15 Nov 2026 (grain-growth events; ice and rocks). Numbers are quoted from the source.

## A. Grain growth: topology and events (theory and simulation)
- Mason, Lazar, MacPherson, Srolovitz, Phys. Rev. E 92 (2015) 063308, arXiv:1507.03379 (FT). 2D steady state: "6.000 ± 0.001 edges
  per face in 2D, with a standard deviation 1.273 ± 0.001" (so mu2 = 1.620). 3D: <F> = 13.766 ± 0.009, edges per face 5.1283 ± 0.0006;
  faces with 4/5/6 edges 26.2/36.4/22.0 %. Statistics from 269,555 grains in 25 runs of 100,000; steady state at just over 10 %
  remaining (3D), about 4 % (2D, 10^7 start). Topology is changed "by removing an edge or a grain, or by flipping an edge".
  **No event counts are reported.**
- Lazar, MacPherson, Srolovitz, "A more accurate two-dimensional grain growth algorithm", Acta Mater. 58 (2010) 364; author PDF
  u.math.biu.ac.il/~lazarem/paper2D.pdf (FT). No T1/T2 counts, no p(n) table (figure only).
- Lazar, Mason, MacPherson, Srolovitz, Acta Mater. 59 (2011) 6837, doi:10.1016/j.actamat.2011.07.052; author PDF paper3D.pdf (FT)
  (+ 2014 correction on Fig. 15). <F> = 13.769 ± 0.016. Events implemented: disappearance of edges, triangular faces, two-sided faces,
  tetrahedral grains, three-faced grains; "The two most frequent changes ... are the disappearance and creation of edges and
  triangular faces." **No counts or rates.**
- Lazar, Han, MacPherson, Srolovitz et al., Phys. Rev. E 88 (2013) 063309, arXiv:1401.1736 (FT): Poisson-Voronoi <F> = 15.535
  (= 48 pi^2/35 + 2), SD 3.335.
- MacPherson & Srolovitz, Nature 446 (2007) 1053: dV/dt = -2 pi M gamma (L - M/6) (2nd, as restated by Mason 2015 eq. 2).
- von Neumann 1952 (discussion in Metal Interfaces, ASM) and Mullins, J. Appl. Phys. 27 (1956) 900: dA/dt = (pi/3) M gamma (n - 6)
  (memory; textbook law).
- Wakai, Enomoto, Ogawa, Acta Mater. 48 (2000) 1297 and Wakai, Shinoda, Ishihara, Dominguez-Rodriguez, J. Mater. Res. 16 (2001)
  2136, doi:10.1557/JMR.2001.0291 (AB, verbatim): 3D Surface Evolver: "For the disappearance of one grain, face-creation switching
  occurred 3.7 times and face-elimination switching occurred 13.2 times on the average." (The 2000 paper: memory.)
- Sprague, Patterson, Grandhi, Metall. Mater. Trans. A (2009/10), doi:10.1007/s11661-009-0139-0 (AB, **unverified**: wording seen only
  as a search-engine paraphrase): 2D vertex model, "constant ratio of 1.34 boundary-switching events per grain disappearance".
- Fradkov, Udler, Kris 1988 (2nd via Henseler, Herrmann, Niethammer, Velazquez, arXiv:0807.3529, FT): flux weight 0.8 < beta < 1.5
  (a model parameter, not a T1/T2 count).
- Rutenberg & McCurdy 2006 and Herdtle & Aref 1992 (as quoted in studies/2026-11-15-tissue-null-models): 2D froth T1 per T2 = 0.53
  macroscopic, 3/2 with side-shedding; vanishing cells 9/84/7 % 3/4/5-sided. 2D froth and 2D grain growth obey the same von Neumann law.
- Weygand, Brechet, Lepinoux, Phil. Mag. B 78 (1998) 329 (AB record only): vertex model with virtual vertices (credited for our scheme).
- Lepinoux, Weygand, Verdier, C. R. Physique 11 (2010) (FT): T1/T2 diagrams, no rates.
- Fan & Chen, Acta Mater. 45 (1997) 611 (FT): 2D phase field, qualitative topology only.
- Esedoglu & Otto, Comm. Pure Appl. Math. 68 (2015) 808; Merriman, Bence, Osher, J. Comput. Phys. 112 (1994) 334; Elsey, Esedoglu,
  Smereka, J. Comput. Phys. 228 (2009) 8015 (memory; credited for the 3D method).
- Not obtained (paywalled or blocked; no purchase): DeHoff & Patterson, Acta Mater. 201 (2020) 403 (3D Monte Carlo event rates by face
  class; numbers not seen); Zollner & Rios, Acta Mater. 2017 "Topological changes in coarsening networks"; Rios & Glicksman 3D theory
  (abstract only, no numbers); Kawasaki vertex-model counts; Anderson, Srolovitz, Grest, Sahni 1984 p(n); Fradkov & Udler 1994 review.
  Free routes if needed: NDL copy or library visit.

## B. Experiments: 2D films and 3D X-ray time series
- Fradkov, Glicksman, Palmer, Nordberg, Rajan, Physica D 66 (1993) 50 (AB): small 4- and 5-sided grains in succinonitrile films
  "usually shrink almost to the vanishing limit, without losing sides through the expected topological cascade of neighbor switchings".
- Fradkov, Glicksman, Palmer, Rajan, Acta Metall. Mater. 42 (1994) 2719 (AB): "The mean topological class of vanishing two-dimensional
  (2-D) grains was found experimentally to be about 4.5."
- Zhang, Zhang, Ludwig, Rowenhorst, Voorhees, Poulsen, Acta Mater. 156 (2018), doi:10.1016/j.actamat.2018.06.021 (FT, accepted
  manuscript at DTU Orbit): pure Fe, synchrotron DCT, 1327 -> 776 grains in 15 steps (interior 387 -> 189); <F> = 13.77 ± 0.13;
  "disappearing face number ... F0 = 3.33 ± 0.10". No event counts.
- Shahani, Walter, Zhang, Ludwig, Juul Jensen, Zhang, Acta Mater. 274 (2024) 119987 (FT, CC-BY): same Fe data; grain disappearance,
  face creation and face loss counted per grain per step, **figure only (Fig. 6a)**; "The total number of events per grain does not
  reach an asymptote, but decreases almost monotonically with time." **Data not public** (no data statement found).
- Shen, Maddali, Menasche, Bhattacharya, Rohrer, Suter, Phys. Rev. Materials 3 (2019) 063611 (FT accepted): alpha-Fe HEDM, 885 grains
  (17.8 %) disappeared in one anneal; <F> about 12.0 (resolution). No switching counts.
- Bhattacharya et al., Science 374 (2021) 189 (FT, OSTI accepted manuscript): Ni HEDM, six states, about 2500 grains. Peng et al.,
  Phys. Rev. Materials 6 (2022) 033402 (FT): about 10 % of grains vanish per interval. **Data public** (below).
- McKenna, Poulsen, Lauridsen, Ludwig, Voorhees, Acta Mater. 78 (2014) 125 (AB): beta-Ti, phase field reproduces "the sequence of
  topological transitions"; no counts seen; no data found.
- Xu et al., Acta Mater. 264 (2024) 119541, arXiv:2311.11219: alpha-Fe, two states, public (below).
- Sun et al. (Armco Fe LabDCT, 3 states), Mosayebi/Phillion Mendeley 10.17632/5vg72jgbcs.2 (single state; snippet only): not used.

## C. Polar ice
- EPICA Dome C grain radius vs depth (Durand & Weiss), PANGAEA doi:10.1594/PANGAEA.198745, NOAA mirror edc_grainradius.txt (12 KB):
  means only.
- Durand et al., J. Geophys. Res. 111 (2006) F01015, doi:10.1029/2005JF000320 (AB): mean-size model (normal growth, rotation
  recrystallisation, dust pinning). Faria, Weikusat, Azuma, J. Struct. Geol. 61 (2014) 21 (AB): the "three-stage" paradigm is flawed.
- Gay & Weiss, J. Glaciol. 45 (1999) 547 (FT): sides per grain are "easily obtained", none reported. Binder et al., EGU 2011 (FT):
  neighbour numbers shown "only occasionally". Roessiger et al., J. Glaciol. 2011 (AB, ELLE). Llorens et al. 2016 (AB).
- Data with grain outlines: NEEM structural parameters PANGAEA.919775 (CC-BY, 15,499 points); NEEM raw scans PANGAEA.743296 (login,
  no licence); EGRIP maps with SVG outlines PANGAEA.933045 (CC-BY, 11 samples); EGRIP sizes .933049, .957032; EDML/EGRIP .924849;
  GRIP Eemian crystal size .859170.
- Time-lapse ice: Hidas et al., EGU 2017 (AB; anneal steps with EBSD, recovery, no growth counts); Shimada et al. 2015 (AB). No 3D
  diffraction time series of ice found.
- Searched, nothing found: NGRIP, Vostok, Dome Fuji crystal-size data (single searches; a gap, not proof of absence).

## D. Metamorphic rocks and analogues
- Octachloropropane movies (Means; Albany): www.atmos.albany.edu/geology/webpages/wdm/wdmoviep.html; 13.mov "Grain growth at zero strain
  rate" (629 KB); 15 movies, about 13 MB; no licence stated.
- Journal of the Virtual Explorer Vol. 2 (Means volume, 2000), mirror tectonique.net/MeansCD (FT contents): Urai & Humphreys time-lapse
  collection (camphor, OCP, bischofite, carnallite); Ree (OCP): "neighbor switching can be achieved by grain boundary migration only
  (Means and Ree, 1990; Bons and Urai, 1992)" (single events described, none counted).
- Bons & Urai, J. Struct. Geol. 14 (1992) 1101 (2nd only).
- ELLE (Jessell, Bons, Evans, Barr, Stuwe, Comput. Geosci. 27 (2001) 17 (memory for the citation); GPL-2, sourceforge.net/projects/elle,
  elle-2.7.1, 17.9 MB; www.ub.edu/elle): front tracking with double and triple nodes; neighbour switch when triple nodes come closer
  than 'switchdistance'. Piazolo et al., J. Struct. Geol. 125 (2019) 111, doi:10.1016/j.jsg.2018.05.025 (FT): no counts.
- Kellermann Slotemaker & de Bresser, Tectonophysics 427 (2006) 73, doi:10.1016/j.tecto.2006.05.017 (FT): ELLE static growth
  non-hexagonal fraction 0.67-0.72 (0.54 in long runs), growth exponent 2.3 ± 0.3; calcite mylonites 0.74-0.93; they track the
  fraction, not events.
- Pankhurst et al., Mineral. Mag. 83 (2019) 705 (AB): olivine LabDCT, no public grain maps found.

## Public data used or usable
| data | states | size | used here |
|---|---|---|---|
| Ni HEDM, Bhattacharya 2021 (mimp.materials.cmu.edu/~gr20/Grain_Boundary_Data_Archive/Ni_velocity/) | 6 | 0.37 GB voxel maps; 4.4 GB meshed; 0.9 GB face tables | yes: voxel maps (pilot, Section 3) |
| alpha-Fe, Xu 2024 (same archive, alpha_Fe_3D_2_times) | 2 | 0.17 GB / 1.3 GB | no |
| OCP grain-growth movie 13.mov | about 100 s of film | 0.6 MB | no (low resolution) |
| EGRIP grain outlines PANGAEA.933045 | 11 depths (one section each) | small | no |
