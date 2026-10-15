# The OCD five-fold chorus: what is known, and what to test next

Fable report for DICTO, 2026-10-16. Scope: literature check plus one light computation. Nothing committed or published.

Every statement is tagged:
**(a)** checked fact from our data or from the computation in this report;
**(b)** established result from a cited source;
**(c)** my hypothesis or suggestion.

## 1. Findings

### 1.1 The closest known idea: "irrational twins" of cubic crystals with an icosahedral motif

- **(a)** Two neighbouring voices (two cubes inscribed in the dodecahedron of hexagon directions) share exactly 2 directions, one body diagonal, which is a three-fold axis. The rotation about that shared axis taking one cube to the other is **44.4775°** (`scripts/chorus_min_silence.py`). The same pair of cubes is also related by 72° about a five-fold axis (step 17).
- **(b)** This exact pair of descriptions is known in materials science as the **icosahedral "irrational twin"**: five cubic variants related by 72° about an irrational axis, or equivalently by 44.48° about [111]. The variants share **no coincidence-site lattice (CSL)**. Ranganathan, Srivastava and Lord (2006) show this twin is the limit of a sequence of rational CSL twins about [111], Σ = 3, 7, 19, 49, 129, 337, ... [R1, R2].
- **(b)** Pauling (1985) proposed that icosahedral quasicrystal diffraction comes from a cubic crystal of icosahedral clusters, multiply twinned in such orientations [P1]. That was rejected as an explanation of quasicrystals, but the geometry is the nearest historical match to the chorus: an icosahedral building block, cubic lattices, five-fold related twin orientations.
- **(b)** Twinning about a five-fold axis is observed in real icosahedral-phase grains (Al-Mn-Fe, Singh and Ranganathan 1995) [R3].
- **(c)** So the chorus is, in crystallographic language, a **five-fold irrational twin (a "fiveling") of a bcc packing of icosahedral bodies**, in which the twin operation is a symmetry of the body itself. That last point is what makes it exact: since the OCD is icosahedral, a 72° turn about a five-fold axis maps every copy to itself, so only the lattices rotate and all copies share one orientation.

### 1.2 The bcc OCD packing is the 1/1 approximant cluster network

- **(b)** In α-AlMnSi and the Bergman phase, icosahedral clusters sit on a bcc lattice. This is the cubic 1/1 rational approximant of the icosahedral quasicrystal (Elser and Henley 1985; Cooper and Robinson 1966; Bergman, Waugh and Pauling 1957, already in our library) [Q1, Q2].
- **(b)** Henley's canonical cell geometry links cluster centres along two-fold axes ("b-linkages") and three-fold axes ("c-linkages") with c = (√3/2) b [Q3]. Fujita et al. (2013), in our library, use the same cells [Q4].
- **(a)/(b)** In the OCD bcc packing, the 8 contacts run along three-fold axes (hexagon normals), and the 6 next neighbours run along the cube axes, which are two-fold axes of the OCD. The bcc ratio of second to first neighbour distance is 2/√3, the same as b/c. So the OCD bcc packing has **the same linkage graph as the 1/1 approximant**: c-links are the hexagon joints, b-links are the non-touching neighbours across the square faces of the Voronoi cell (the "X holes" of step 15).
- **(c)** The five voices are the five ways an icosahedral body can sit in a cubic 1/1 setting (the five conjugate pyritohedral subgroups T_h of I_h, one per inscribed cube). That is standard group theory, but I did not find it written in this "chorus" form.

### 1.3 Contrast with fcc decahedra, Frank–Kasper lines and disclinations

- **(b)** In fcc five-fold twinned particles, five tetrahedral domains are bounded by coherent {111} twin mirrors at 70.53°, leaving a 7.35° gap. It is closed by elastic strain or a partial wedge disclination (Ino 1969; Marks 1984; Howie and Marks 1984; de Wit 1972) [T1-T4]. Real particles also relieve misfit by dislocations along the five-fold axis and by sacrificing domains (Sun et al. 2025) [T5]. Colloidal polyhedra also form fivelings, with the same lattice-forced angular gap (Lee and Glotzer 2022) [T6].
- **(b)** In Frank–Kasper phases and in Nelson's picture of icosahedral order, five-fold bonds are disclination-free lines; ±72° disclination lines carry the frustration [F1, F2].
- **(a)** In the chorus each wedge is exactly 72°, by construction, and the building block has one orientation everywhere. **(c)** So there is **no rotational defect at all**: no angular gap, no wedge disclination, no strain. The cost of the five-fold symmetry is purely translational, and it is paid by vacancies (silenced copies) rather than by strain. Put simply: the decahedron trades a 7.35° gap for elastic strain; the chorus trades it for incoherent boundaries plus vacancies. I found no source describing this trade for a polyhedral packing.
- **(b)** Wedge boundaries between two cubic lattices related by an irrational rotation are **irrational (non-CSL) interfaces**. Gratias and Thalal (1988) and Sutton (1989, 1992) show that such interfaces are quasiperiodic: the relative registry of the two lattices along the boundary is a projection of a higher-dimensional lattice [G1-G3].
- **(c)** This predicts that the chorus boundary vacancies are not random and not periodic: their positions along each boundary should form a quasiperiodic pattern whose spacings lie in ℚ(√5), and the vacancy density per unit boundary area should settle to a constant. This is the best-supported theoretical expectation for the "vacancies at every radius" observation.

### 1.4 Decagonal approximants

- **(a)/(c)** The five-fold axis is an irrational direction of every voice lattice, so the chorus has **no periodicity along the axis**. Decagonal phases and their approximants are periodic along the ten-fold axis, so the chorus is not a decagonal approximant. The resemblance is only in the 72° twinning. Decagonal phases can twin by 72° with coherent boundaries (Al-Cu-Cr) for a different reason: their structure is a packing of decagonal columns.

### 1.5 Is the exact construction known?

- I searched the web (materials science, quasicrystals, polyhedron packing, colloids) and our library for "an icosahedral body packed in five rotated cubic lattices around a five-fold axis, one orientation for all copies, hollow core and boundary vacancies". **I found nothing that matches the whole construction.**
- The nearest pieces are: the irrational icosahedral twin [R1, R2], Pauling's twinned cubic model [P1], the 1/1 approximant cluster network [Q1-Q3], and quasiperiodic irrational boundaries [G1-G3].
- **(c)** The parts that look new are: (i) a **hard-body packing** (not atoms) in which the irrational twin is exact and verified in ℚ(√5); (ii) the vacancy accounting (an empty core plus boundary vacancies); (iii) the "voices" reading of the five T_h settings. Absence in my search is not proof of novelty. A specialist search of the Ranganathan/Lord and Gratias groups' later papers is still worth doing before any public claim.

### 1.6 Library note

- **(a)** **Ino 1969 and Marks 1984 were not in the reference library**, although step 17 of the README cites them as if they were. I added them, plus 14 other references from this report, as **link-only** entries to `~/Documents/kaleidohedra-references/papers/MANIFEST.json` (accessed 2026-10-16; not committed). Marks 1984 has a free author copy at Northwestern (URL in the entry). Lee and Glotzer 2022 and Sun et al. 2025 are open access and could be downloaded later.

## 2. The one computation: is the greedy silencing minimal?

`scripts/chorus_min_silence.py` → `data/chorus-min-silence.txt` (8 s on the Pi; float clash graph on the same 336 sites as step 22; exact integer linear programming).

- **(a)** The 336 sites form 1 axis site (the centre) and 67 five-fold orbits. 25 pairs of orbits clash, and 6 orbits clash with their own rotated images, so those 6 must be silenced.
- **(a)** The minimum number of orbits to silence for a five-fold symmetric, clash-free result is **16 orbits (80 copies)**. **The greedy choice is minimal.** It is **not unique**: at least one other 16-orbit choice exists.
- **(a)** Without imposing five-fold symmetry, the minimum is **72 copies** (165 clashing copy pairs). Symmetry costs 8 extra silences at radius 5.
- **(a)** All silenced copies lie within 0.61 of a wedge-boundary half-plane or the axis. The median for all sites is 0.77, so silences hug the boundaries. 30 of the 80 (6 orbits, within 1.05 of the axis) form the core.
- **(c)** The 6 self-clashing orbits and the 6 core orbits are probably the same set, which would make the empty core forced by symmetry rather than chosen. Not checked.
- Caveats: this is the minimum for this one finite ball (radius 5) at this one start angle (59°). Sites near the ball's surface have fewer neighbours. The clash graph is float (tolerance 1e-9); the step 22 exact check confirms the greedy set, but the alternative optimum has not been checked exactly.

## 3. Recommended next tests, ranked by value

1. **Boundary vacancy pattern and density (highest value).** Grow to radius 8–10 on dicto-node. For one boundary, record each silenced copy's coordinates in the boundary half-plane (distance from the axis, height along it). Test: (i) does the vacancy count per unit boundary area converge; (ii) do the spacings take only a few values in ℚ(√5) with ratios of τ, as Gratias–Thalal predicts for an irrational interface? A clean yes turns "vacancies at every radius" into a theorem-like statement: a quasiperiodic boundary with a computable density. A cheap exact handle: reduce each boundary site of voice k modulo voice k+1's lattice. Clash or no clash is then a window condition on a torus, which is cut-and-project language.
2. **Make the core and the boundaries canonical.** Repeat the minimum-silence integer program at radius 6–8 with symmetry imposed. Report which orbits are in every optimum (forced) and which are optional (choice). If the core orbits are exactly the self-clashing ones, the core shape is forced. Then name it: the convex hull of the forced-empty region around the axis, compared with a pentagonal prism or antiprism.
3. **Wedge start angle, judged by vacancy density, not first-shell clashes.** The 59° choice came from a float scan of collisions within radius 2. Re-score a coarse set of angles (say 10) by minimum silences per volume at radius 5. Also test the symmetric angles where a boundary half-plane contains a mirror of the OCD; those may give mirror-related boundaries and fewer vacancies.
4. **The Σ-sequence as rational approximants (outside the plan, low cost to think about).** Ranganathan et al. approximate the 44.48° twin by CSL twins Σ7, 19, 49, ... about [111]. A "rational chorus" would rotate the lattices by a nearby CSL angle. The OCD copies would then no longer map to themselves, so copies would need small turns, which breaks DICTO's no-rotation rule. Mention only, to keep the periodic/aperiodic bridge in view.
5. **Mixed silencing.** Since the non-symmetric minimum (72) is below the symmetric one (80), check whether any defect-free five-fold arrangement exists by letting a few boundary sites take a copy of the neighbouring voice instead of being silenced. This is a different construction, so do it only if 1–3 look regular.

## 4. Citations

Five-fold twins and disclinations
- [T1] S. Ino (1969). Stability of multiply-twinned particles. J. Phys. Soc. Jpn. 27, 941–953. doi:10.1143/JPSJ.27.941
- [T2] L. D. Marks (1984). Surface structure and energetics of multiply twinned particles. Phil. Mag. A 49, 81–93. doi:10.1080/01418618408233431 (author copy: https://www.numis.northwestern.edu/Research/Articles/1984/Phil_Mag_MTP_1.pdf)
- [T3] A. Howie, L. D. Marks (1984). Elastic strains and the energy balance for multiply twinned particles. Phil. Mag. A 49, 95–109. doi:10.1080/01418618408233432
- [T4] R. de Wit (1972). Partial disclinations. J. Phys. C 5, 529–534. doi:10.1088/0022-3719/5/5/004
- [T5] Z. Sun, Y. Zhang, Z. Li, Z. Xie, Y. Dai, X. Du, C. Ophus, J. Zhou (2025). Strain release by 3D atomic misfit in fivefold twinned icosahedral nanoparticles with amorphization and dislocations. Nat. Commun. 16. doi:10.1038/s41467-025-56842-6
- [T6] S. Lee, S. C. Glotzer (2022). Entropically engineered formation of fivefold and icosahedral twinned clusters of colloidal shapes. Nat. Commun. 13. doi:10.1038/s41467-022-34891-5

Irrational twins and Pauling's model
- [R1] S. Ranganathan, A. K. Srivastava, E. A. Lord (2006). Coincidence-site lattices as rational approximants to irrational twins. J. Mater. Sci. 41, 7696–7703. doi:10.1007/s10853-006-0966-y
- [R2] A. K. Srivastava, S. Ranganathan (1997). Twinning of quasicrystals and related crystals. Prog. Cryst. Growth Charact. Mater. 34, 251–262. doi:10.1016/S0960-8974(97)00017-X
- [R3] A. Singh, S. Ranganathan (1995). A transmission electron microscopic study of icosahedral twins. 1: Rapidly solidified Al-Mn-Fe alloys. Acta Metall. Mater. 43(9). doi:10.1016/0956-7151(95)00024-P
- [P1] L. Pauling (1985). Apparent icosahedral symmetry is due to directed multiple twinning of cubic crystals. Nature 317, 512–514. doi:10.1038/317512a0

Approximants and cluster cells
- [Q1] V. Elser, C. L. Henley (1985). Crystal and quasicrystal structures in Al-Mn-Si alloys. Phys. Rev. Lett. 55, 2883. doi:10.1103/PhysRevLett.55.2883
- [Q2] M. Cooper, K. Robinson (1966). The crystal structure of the ternary alloy α(AlMnSi). Acta Cryst. 20, 614. doi:10.1107/S0365110X6600149X
- [Q3] C. L. Henley (1991). Cell geometry for cluster-based quasicrystal models. Phys. Rev. B 43, 993. doi:10.1103/PhysRevB.43.993
- [Q4] N. Fujita, H. Takano, A. Yamamoto, A.-P. Tsai (2013). Cluster packing geometry for Al-based F-type icosahedral alloys. Acta Cryst. A 69, 322. arXiv:1301.6823 (in library, bridges/)
- G. Bergman, J. L. T. Waugh, L. Pauling (1957). The crystal structure of the metallic phase Mg32(Al,Zn)49. Acta Cryst. 10, 254. doi:10.1107/S0365110X57000808 (in library)

Frank–Kasper and frustration
- [F1] F. C. Frank, J. S. Kasper (1958). Complex alloy structures regarded as sphere packings. I. Acta Cryst. 11, 184–190. doi:10.1107/S0365110X58000487
- [F2] D. R. Nelson (1983). Order, frustration, and defects in liquids and glasses. Phys. Rev. B 28, 5515–5535. doi:10.1103/PhysRevB.28.5515

Irrational grain boundaries
- [G1] D. Gratias, A. Thalal (1988). Hidden symmetries in general grain boundaries. Phil. Mag. Lett. 57, 63–68. doi:10.1080/09500838808229611
- [G2] A. P. Sutton (1989). Quasiperiodicity in irrational interfaces. Phase Transitions (volume not checked). doi:10.1080/01411598908245732
- [G3] A. P. Sutton (1992). Irrational interfaces. Prog. Mater. Sci. 36, 167–202. doi:10.1016/0079-6425(92)90008-U

Not found: any five-fold twinned **bcc** analogue of the fcc decahedron in metals (a 2020 study notes that twinning in bcc Fe/W nanoparticles is poorly documented: Nanoscale 2020, https://pubs.rsc.org/en/content/articlelanding/2020/nr/d0nr06957d, not read in full), and any packing paper with the full chorus construction.

All DOIs were looked up on Crossref on 2026-10-16. The full texts of R1, R2, R3, G1 and G3 were not read; only abstracts and bibliographic records.
