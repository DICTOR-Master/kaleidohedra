# Prior-art search: paper #52 draft, "The Web of Bonds" (2026-10-25)

Draft read: `~/Documents/papers-to-read/web-of-bonds-52-draft.pdf` (source `paper.src.html`).
Verdicts: **(a)** known, cited; **(b)** known in a more general form that implies it; **(c)** not found
in the sources searched. "Not found" is limited to the sources listed at the end. Nothing here is
called new.

Every DOI below was checked on api.crossref.org on 2026-10-25 (title, venue, volume, pages, year).
arXiv identifiers checked on export.arxiv.org.

## Verdict table

| # | Claim (as in the draft) | Verdict | Sources (verified DOIs) | Note |
|---|---|---|---|---|
| 1a | Golden loop at its special points: x = 1 is the Voronoi diagram of bcc (Kelvin cells); x = 0, ∞ is the octahedron + cuboctahedron (rectified cubic) honeycomb as a power diagram with w_B − w_S = −φ²/4 | **(b)** | Aurenhammer 1987 SIAM J. Comput. 10.1137/0216006; Aurenhammer 1991 ACM Comput. Surv. 23, 345–405, 10.1145/116873.116880; Thomson 1887 10.1080/14786448708628135 | Any Delaunay tessellation is the power diagram of its own circumspheres (paraboloid lifting; two-line proof). Octahedron circumradius² φ²/4, cuboctahedron φ²/2: difference −φ²/4, the draft's value at x = 0, checked by hand. Kelvin = plain Voronoi of bcc. |
| 1b | The whole family T(x), T(1/x) on B2 sites is a power diagram with w_B − w_S = (φ²/4)(x−1)/(x+1); constant face lattice on 0 < x < ∞ | **(b)** for "is a power diagram", **(c)** for the explicit weight formula along the whole family | Aurenhammer 1987 DCG 2, 49–64, 10.1007/BF02187870 (criterion: cell complexes are power diagrams iff they lift; Aurenhammer 1991, in the passage on reciprocal figures, says "several well-known types of cell complexes are power diagrams"); Rybnikov 1999 DCG 21, 481–517, 10.1007/PL00009434 (liftings of cell complexes); Koca et al. arXiv:1506.04600 / 10.24200/squjs.vol21iss2pp139-149 (the T(x) orbit itself) | One instance is in the materials literature: Wang, An, Gou, Zhao, Wang, Huang 2018, AIP Advances 8, 105203, 10.1063/1.5052478, build CsCl-type binary hard-sphere crystals at size ratio √3 − 1 and find both radical polyhedra are 14-faced (6 squares + 8 hexagons). That is exactly the draft's window end x = √3 + 1. No continuous sweep there. Aurenhammer 1987 DCG not read in full; the precise "simple complex ⇒ power diagram" statement should be quoted only after reading. |
| 2a | Delian loop at its special points: t = 0 rhombic dodecahedra = Voronoi of fcc; t = 1 cubes = Voronoi of the tet sites; t = 1/3 octet = power diagram of fluorite sites with w_Q − w_O = −1/8 | **(b)** | Aurenhammer 1987/1991 as above; Knoll & Morgan 2003 (Bridges, no DOI) | The octet is the Delaunay tessellation of fcc, so it is the power diagram of its circumspheres, which sit on the oct holes (r² = 1/2) and tet holes (r² = 3/8): difference −1/8, which is the draft's (3/8)(2t − 1) at t = 1/3. Checked by hand. |
| 2b | The interpolating Delian family is a power diagram for every t, with w_Q − w_O = (3/8)(2t − 1) | **(c)** | — | Weights at samples already in paper #51 (as the draft says). |
| 2c | Octet is the unique single-bond-type member; dual flips once at t = 1/3; rhombus long diagonal → short diagonal | **(b)** for the two dissections; **(c)** for the flip along this family | Alexeev 2002 (below) for the flip framework; the two dissections of the rhombic dodecahedron (octahedron + 8 tetrahedra on its 4-valent/3-valent corners; cube + 6 square pyramids) are classical | The rhombic dodecahedron with both dissections is textbook geometry; that the power-diagram family passes from one to the other exactly at the octet was not found. |
| 3 | Closed-form bond (face) areas along both families; coordination numbers along the families; "radical polyhedra" of ions in CsCl/fluorite vs radius ratio | **(c)** for closed forms and counts along the families; **(a)** for radical-polyhedron face counts at single fixed ratios | Wang et al. 2018 10.1063/1.5052478 (fixed ratios: SC/CsCl-type at √3 − 1, 14 + 14 faces; fcc with small spheres in oct holes etc.); Richard, Oger, Troadec, Gervois 1998 Physica A 259, 205–221, 10.1016/S0378-4371(98)00323-9 (radical tessellation of binary *random* assemblies vs size ratio); Gellatly & Finney 1982 10.1016/0022-3093(82)90093-X; O'Keeffe 1979 10.1107/S0567739479001765; Blatov 2004 10.1080/08893110412331323170 | Software (Voro++, ToposPro) computes such faces numerically; no closed-form family found. Blatov 2004 not read in full: whether it discusses radical (weighted) partitions of B2/C1 could not be confirmed. |
| 4 | Touching windows end exactly at Pauling's limits √3 − 1 (CN 8) and √(3/2) − 1 (CN 4) | **(a)** | Pauling 1929 10.1021/ja01379a006; Murray & Sanders 1980 Phil. Mag. A 42, 721–740, 10.1080/01418618008239380 (packing densities of binary sphere arrangements vs radius ratio); Wang et al. 2018 (CsCl type built at √3 − 1) | The window ends are the same anion–anion contact condition from which Pauling derived the limits; the radical-tessellation reading adds no new contact geometry. The upper ends (√3 + 1)/2 are the reciprocal of the 0.732 limit (8-coordination with the roles of the sites exchanged). |
| 4' | Theorem 2(a): radical tessellation = power diagram with w = r² + C | **(a)** | Gellatly & Finney 1982; Imai, Iri, Murota 1985 10.1137/0214006; Aurenhammer 1987 | Classical. |
| 4'' | Theorem 2(c) contact maps ρ = (x + 2)/(2x + 1), ρ = t/(1 − t); 2(e) packing range 1/6 ≤ t ≤ 2/3; Cor. 6, 7 | **(c)** | — | Elementary once the weights are known. |
| 5 | Secondary fan / chambers of weights for periodic point sets; golden segment in one chamber, Delian segment crosses one wall | **(b)** | Gelfand, Kapranov, Zelevinsky 1994 10.1007/978-0-8176-4771-1; De Loera, Rambau, Santos 2010 10.1007/978-3-642-12971-1; **Alexeev 2002, Ann. Math. 155, 611–708, 10.2307/3062130, arXiv:math/9905103, §5.12** "Generalized secondary polytopes for periodic decompositions": decompositions of X_R/Y, Y ⊂ X of finite index, faces of the secondary polytope ↔ regular subdivisions; Erdahl 1999 10.1006/eujc.1999.0294 and Erdahl & Rybnikov arXiv:math/0112097 (L-types = secondary cones of lattice Delaunay subdivisions) | Alexeev's setting covers the golden case directly (X = the bcc lattice, Y = φℤ³, heights |p|² − w by coset) and the Delian case with Q ∪ O as a pointed subset of a finer lattice. So "chambers of the secondary fan" for these weights is an instance of known theory. The Delaunay subdivision of the bcc lattice into tetragonal disphenoids (the golden dual at x = 1) is classical. The specific chambers and walls for these two segments: **(c)**. |
| 6 | "Relay": bond types born/dying along a one-parameter weight family in a binary crystal | **(c)** for weight families on fixed sites; nearest analogues listed | Koch 1973, Z. Kristallogr. 138, 196–215, 10.1524/zkri.1973.138.1-4.196 (Dirichlet-domain types of cubic lattice complexes as *positional* parameters vary; topology changes at critical values; unweighted; not read); Richard et al. 1998 (neighbour statistics vs size ratio, random packings); Schürmann 2010 Adv. Math. 225, 2546–2564, 10.1016/j.aim.2010.05.002, arXiv:0808.2013 (parameter space of periodic sets, Delone subdivision changes) | The colloid/nanoparticle literature already cited ([12–17]) and Hopkins, Stillinger, Torquato 2012 PRE 85, 021130, 10.1103/PhysRevE.85.021130 (arXiv:1111.4917) vary size ratio and track phases, not radical faces. |

## Most important finds

1. **Endpoints and midpoints are classical.** Every Delaunay tessellation is the power diagram of its
   circumspheres. So the octet (t = 1/3) and the octahedron + cuboctahedron honeycomb (x = 0, ∞) are
   power diagrams with exactly the draft's weights, and x = 1, t = 0, t = 1 are plain Voronoi diagrams.
   What remains of the Main theorem (i) is the interpolation between these known points. The paper
   should say so.
2. **Alexeev 2002, §5.12** is the published GKZ framework for periodic point sets (Y-periodic
   decompositions of a lattice X, with periodic secondary polytopes). Corollary 4 is an instance of it.
   Cite it next to [5, 6] and Erdahl [22].
3. **Wang et al. 2018 (AIP Advances, open access)** already found the window-end CsCl-type member
   (size ratio √3 − 1, two 14-faced radical polyhedra). It is a published point on the golden loop.
4. **Pauling's limits come from the same contact geometry.** "Derived here, not quoted" overstates it:
   the window ends are Pauling's anion–anion contact condition, rederived.
5. **George et al. 2020** (Angew. Chem. Int. Ed. 59, 7569–7575, 10.1002/anie.202000829, CC BY):
   in ~5000 oxides only 13 % satisfy Pauling's rules 2–5 together. This is a good citation for §6:
   it shows how weak the rules are as predictors.

## Suggested wording changes (not applied: paper.src.html untouched)

- **§8 "Known"**, add after "regular subdivisions change only at the walls of the secondary fan [5, 6]":
  "including for periodic decompositions (Alexeev [new], §5.12)". Add: "every Delaunay tessellation is
  the power diagram of its circumspheres [3, Aurenhammer 1991], so the octet at t = 1/3 and the
  octahedron–cuboctahedron honeycomb at x = 0, ∞ are power diagrams with the weights of the Main
  theorem; x = 1, t = 0 and t = 1 are ordinary Voronoi diagrams". Add: "a CsCl-type binary crystal at
  size ratio √3 − 1 with two 14-faced radical polyhedra (Wang et al. 2018)". Add: "radius-ratio-
  dependent packings of two sphere sizes (Murray and Sanders 1980)".
- **§8 "Not found"**: remove "the touching windows bounded exactly by Pauling's limits". Replace it with
  a statement under "Known": "the window ends are Pauling's contact limits [9]". Narrow "the sequence of
  dual cells along each loop" to "the sequence of dual cells between the classical end and middle
  members".
- **§5 "Agreements"**: "The touching windows are Pauling's limits, derived here, not quoted" →
  "The touching windows end at Pauling's limits; this is Pauling's own contact condition, rederived
  in the language of radical tessellations."
- **Abstract / In short**: after "bounded exactly by Pauling's classical radius-ratio limits" add
  "(the same contact condition as Pauling's)". Optionally add to the Main theorem paragraph: "At the
  ends and at Kelvin's cell and the octet these are classical Voronoi or Delaunay tessellations;
  the theorem gives the whole family between them."
- **Proof of the Main theorem, (i)**: add a one-line remark: "At t = 1/3 and x = 0, ∞ the identity also
  follows from the circumsphere description of a Delaunay tessellation." This gives an independent
  check.
- **Corollary 4**: "form the chambers of the secondary fan [5, 6]" → "[5, 6]; for periodic sets see
  Alexeev [new, §5.12]".
- **§5 zirconia sentence**: "which fits the general knowledge that cubic zirconia is not stable at room
  temperature unless doped": add a citation or soften it to "consistent with cubic ZrO₂ needing
  dopants to be stable at room temperature".
- **§6**: cite George et al. 2020 where Pauling's rule misses UO₂/CeO₂/Na₂O/K₂O.
- **§7 "Open: … a web search before any claim of novelty"**: replace with a reference to this search
  (Appendix A updated).
- **Appendix A**: list the sources below. Note that Aurenhammer 1987 DCG, Blatov 2004 and Koch 1973 were
  identified but not read in full.
- **[6] and [20]** now have verified DOIs: De Loera et al. 10.1007/978-3-642-12971-1; Thomson 1887
  10.1080/14786448708628135.

## Legally free copies for the library (not downloaded into the library)

| Source | Free copy |
|---|---|
| Alexeev 2002 | arXiv:math/9905103 (v4) |
| Koca et al. 2015 | arXiv:1506.04600 |
| Erdahl & Rybnikov, Voronoi–Dickson hypothesis | arXiv:math/0112097 |
| Dutour Sikirić, Schürmann, Vallentin 2008 (Duke 142, 127–164, 10.1215/00127094-2008-003) | arXiv:math/0601084 |
| Schürmann 2010 | arXiv:0808.2013 |
| Hopkins, Stillinger, Torquato 2012 | arXiv:1111.4917 |
| Wang et al. 2018 | AIP Advances, open access CC BY (doi link) |
| George et al. 2020 | Angewandte open access CC BY; ChemRxiv 10.26434/chemrxiv.9255446 |
| Aurenhammer 1991 survey | a course-hosted copy exists at cs.jhu.edu (rights unclear); prefer the ACM DL |

## Sources searched (2026-10-25)

- DICTO's library: `~/bin/ask-library`, four queries (power diagram/Laguerre and radius ratio; radical
  Voronoi binary packing CsCl; lattice Delaunay subdivisions/L-types/secondary fan; Laguerre weight
  flips). There are still no power-diagram, radical-tessellation or ionic-radius papers in the library.
  Erdahl 1999, Garber 2019 and Gabbrielli–Jiao–Torquato 2012 (fcc retessellations; checked, no power
  diagrams) are the nearest. INDEX.html was grepped for Laguerre/radical/power diagram: no hits.
- Web (standard and extended search, about 15 queries): radical/power/Laguerre with CsCl, fluorite,
  ionic radii, radius ratio, binary hard-sphere crystals, bidisperse foams, Fischer–Koch, Blatov/ToposPro,
  periodic secondary fan/Delone subdivisions, Delaunay as power diagram.
- arXiv (Alexeev full text searched for the periodic sections), Crossref (all DOIs), and the AIP
  Advances page of Wang et al. 2018.
- Not reached: Google Scholar itself; the full texts of Blatov 2004, Koch 1973, Aurenhammer 1987 DCG,
  Richard et al. 1998 (publisher 403); and any closed-form face-area tables in crystal-chemistry
  handbooks.
