DICTO · dictospheres.com

> **Note (2026-10-15, after step 30):** where this review says "equal-cost fork" or "tie", read: minimal removal departs from the canonical window at |h| = 12.81. Step 30 showed it is not a tie (keeping the core copy is cheaper by one ring). The prior-art verdicts are unaffected.

# Prior-art review: the OCD five-fold chorus and the Ogdoecontahedron

Fable review for DICTO, 2026-10-15. Scope: steps 21–29 of `README.md` and `FABLE-REPORT.md`, plus the Ogdoecontahedron (OCD) itself as a polyhedron. Nothing committed or published.

Labels used throughout:
- **verified**: I read the source (abstract, record or text) or checked it by computation, and the DOI resolves on Crossref (`api.crossref.org`, 2026-10-15).
- **record only**: the DOI and bibliographic record are verified on Crossref, but I did not read the paper; the content statement is standard knowledge or comes from a secondary source.
- **not checked**: named here as a lead, not read or not reachable.

About 30 web lookups plus Crossref checks were used. This is a careful search, but not a full specialist review.

## Short verdict

- The chorus belongs to a known family: irrational interfaces between periodic crystals are quasiperiodic (Sutton; Gratias–Thalal; Rivier–Lawrence), and the five-fold icosahedral irrational twin is known (Ranganathan, Srivastava & Lord).
- The idea that hard-core exclusion shapes a cut-and-project window is also known in general (Katz & Gratias 1993; the 1D lattice-gas literature).
- What I did not find: an exact Fibonacci chain **along a five-fold junction line** between periodic domains; a window **selected by a ring of copies clashing with itself**, with an exact critical distance that is close to, but not equal to, the canonical window; and the **equal-cost fork** at height 12.81.
- The OCD (20 regular hexagons + 60 kites) was not found under any name. Its combinatorial type can be reached with extended Conway-type operators, so only the metric solid, with its regular hexagons, is a candidate for being new.

## Q1. Quasiperiodic order along a five-fold junction line

**Question.** Has anyone shown a Fibonacci or cut-and-project arrangement *along* a five-fold twin junction or disclination line, rather than across a planar interface?

**Closest prior work.**
- **Irrational planar interfaces are 1D (or 2D) quasicrystals.** Sutton 1988, 1989, 1992; Gratias & Thalal 1988; Rivier & Lawrence 1988 (all in the library). They cover the **seams** (our wedge boundaries). They are about planes, not about the line where five planes meet. *Record only.*
- **Five-fold twinned (decahedral) particles and nanowires.** The five-fold axis is a partial wedge disclination with a 7.35° gap, closed by strain, dislocations or lost domains (de Wit 1972; Ino 1969; Marks 1984; Hofmeister 1998 review; Sun et al. 2025; Fasce et al. 2026, arXiv:2603.28399). The axis is one atomic column, or a relaxed core. None of the abstracts I read mentions quasiperiodic, Fibonacci or vacancy order along the axis. *Verified for Fasce et al. (abstract); record only for Hofmeister.*
- **Disclination-line models of icosahedral order.** Kléman & Sadoc 1979 and Kléman 1989 describe amorphous and Frank–Kasper structures as curved-space crystals with disclination lines. Mosseri & Sadoc 2014 describe a dodecagonal quasiperiodic Frank–Kasper phase with a *network* of disclination lines. There the quasiperiodicity is in how the lines are arranged across the plane, not along one line. *Record only (abstracts not read in full).*
- **Icosahedral twins in real alloys.** Regions about 1 µm across are twin-related through a common five-fold axis (Singh & Ranganathan 1995; Srivastava & Ranganathan 1997; in the library). No statement about order along the axis was seen. *Record only.*
- **Prodan et al. 2017.** Cyclic twinning of golden rhombohedra is equivalent to an icosahedral tiling, with Fibonacci periodicities. The twins intergrow without obvious twin boundaries, so there is no junction line to study. *Verified (search summary of the open-access paper).*

**What is not covered.** I found no paper with a 1D model set lying *along* a five-fold junction. The chorus also differs from every fiveling above. Its wedges are exactly 72° and the body has one orientation everywhere, so the axis is **not** a disclination. It is a line of irrational direction shared by five lattices. That is why a textbook strip projection (a rank-2 lattice cut along an irrational line) appears there.

**Verdict.** Not found. Present it as a new exact *instance* of the irrational-interface family, at a junction line rather than a plane. Note that "lattice points near an irrational line form a model set" is textbook (Baake & Grimm 2013). The new part is that the silencing puts exactly those points in.

## Q2. A cut-and-project window derived from hard-core exclusion

**Question.** Has anyone derived a cut-and-project window from overlap or packing constraints?

**Closest prior work.**
- **Katz & Gratias 1993.** They shaped the atomic surfaces (windows) of an icosahedral model with **closeness and hard-core conditions**, to maximise density while staying bounded by 2-fold planes. *Verified* through the Widom & Mihalkovič review (2023, Isr. J. Chem.), which I read on arXiv: "Katz and Gratias used theoretical arguments (closeness and hard core conditions) to create atomic surfaces that maximize the density". This is the nearest general principle: **a minimum-distance rule bounds the window.**
- **Sphere packings on quasilattices.** Henley 1986 studies sphere packings and local environments in Penrose tilings. *Record only.*
- **1D lattice gases.** With convex repulsion, ground states at irrational density are the "most homogeneous" (generalised Wigner) configurations (Hubbard 1978; Bak & Bruinsma 1982). These are Sturmian words, so they are cut-and-project chains. van Enter, Koivusalo & Miękisz 2019 build lattice-gas models whose ground states are Sturmian (Fibonacci as the example), using energies on forbidden patterns. Miękisz 1997 gives stable quasicrystalline ground states. *Abstract seen (through search results) for van Enter et al. and for the Jędrzejewski–Miękisz review of the Hubbard line; record only for Hubbard, Bak & Bruinsma and Miękisz 1997.*
- **Overlap and covering rules that force quasiperiodicity.** Gummelt 1996 (overlapping decagons cover a Penrose tiling); Steinhardt & Jeong 1996 and Jeong & Steinhardt 1997 (maximising cluster density forces it). These derive quasiperiodicity from overlap rules, but on clusters that are *allowed* to overlap. They do not derive a window from hard bodies that must not overlap. *Record only.*
- **Foundations.** de Bruijn 1981; Levine & Steinhardt 1986; Socolar & Steinhardt 1986. *Record only.*

**What is not covered.** In all of these, the window is a design input (Katz–Gratias), or the exclusion is an energy or tiling rule. None of them has a window that falls out of **one hard polyhedron clashing with its own five-fold images**, with one exact critical distance t_c² = 8/9 + 8√5/45. None has a hard-core window that sits *slightly inside* the canonical window (t_c < L), so that the two agree only up to a height (|h| < 12.81).

**Verdict.** The general principle is known and must be cited (Katz & Gratias first; the lattice-gas line as the 1D analogue). The specific mechanism and the exact t_c ≠ L result were not found.

## Q3. Packings of one hard polyhedron in five-fold twinned periodic domains

**Closest prior work.**
- **Lee & Glotzer 2022.** Hard truncated tetrahedra form five-fold and icosahedral twinned clusters in Monte Carlo. The twins come from cubic/hexagonal diamond stacking, with the usual angular gap. Overlap is tested move by move in floating point. There is no exact junction analysis. *Verified (abstract and PMC record).*
- **Conway & Torquato 2006.** Five regular tetrahedra around an edge leave a gap, and 20 around a point leave gaps (the hard-polyhedron version of the fiveling gap). *Record only.*
- **Dense packings and self-assembly of polyhedra.** Torquato & Jiao 2009 (densest packings of Platonic and Archimedean solids); Haji-Akbari et al. 2009 (a dodecagonal quasicrystal of hard tetrahedra); Damasceno, Engel & Glotzer 2012 (145 polyhedra self-assembled). None studies five twinned periodic domains of one body. *Record only.*

**What is not covered.** I found no study of five periodic packings of one hard, icosahedral body joined at a five-fold axis, with **exact** overlap checks at the junction (the chorus: 0 overlaps to radius 10, in ℚ(√5)). The no-gap, no-strain, vacancy-paid construction remains unreported in what I searched.

**Verdict.** Not found. Cite Lee & Glotzer and Conway & Torquato as the nearest hard-shape work.

## Q4. Equal-cost "forks" in minimal silencing

**Closest prior work.**
- **Singular model sets.** When lattice points fall exactly on the window edge, there is more than one valid choice, and each gives an element of the same hull (for the Fibonacci chain, the two words that differ by swapping "ab" and "ba" at one place). This is standard (Baake & Grimm 2013, Vol. 1). Step 27's "singular member" sits here. *Record only.*
- **Phason freedom at irrational interfaces.** For an irrational interface, a relative translation of the two crystals acts as a phason shift, so many registries are locally equivalent (Gratias & Thalal 1988; Sutton 1992). *Record only; I did not read these papers.*
- **Random tilings and phason flips.** Equal-energy rearrangements that differ by phason flips are the basis of random-tiling models (Henley; Elser). *Not checked in detail.*

**What is not covered.** The step 29 fork is not a window-edge ambiguity. It is a tie between two *different windows*: the canonical one [0, L) and the narrower ring-clash one, which differ by whether a whole five-fold ring is silenced. I found no report of such a tie in a minimum-vacancy problem at a twin junction.

**Verdict.** Related ideas (singular choice, phason degeneracy) are known and should be named as context. The specific fork was not found. Describe it as a degeneracy of the minimal silencing, and do not call it a new phenomenon.

## Q5. The Ogdoecontahedron as a polyhedron

### Exact data (from `polar-dharma/data/hstar-render.json`, recomputed 2026-10-15, float)

- **Counts:** 102 vertices, 180 edges, 80 faces (20 hexagons + 60 kites). Euler holds. *Verified.*
- **Vertex degrees:** 12 of degree 5, 30 of degree 4, 60 of degree 3. *Verified.*
- **Faces:** every hexagon is regular (all angles 120°), and its corners alternate degree 3 and degree 4. Every kite has angles 117.845°, 68.619°, 117.845°, 55.691°, with corners of degree 3, 5, 3, 4 in that order. *Verified.*
- **Radii:** 90 vertices lie on one sphere (radius 1), and 12 lie at 1.042799. The faces lie at two distances: 0.934172 and 0.979432. *Verified.*
- **Not canonical.** Edge lines lie at two distances from the centre, 0.983956 and 1.0, so no midsphere touches every edge. The OCD is not the canonical form of its combinatorial type. *Verified (float).*
- **Origin:** it is the polar dual of the Hecatodihedron. Geometrically, it is the pentakis dodecahedron with its 20 six-fold corners cut flat, so deep that the two cuts on each dodecahedron edge meet at its midpoint. Each triangle then becomes a kite (apex, cut point, edge midpoint, cut point). The degree pattern above confirms this. *Verified from the data.*

### Combinatorial matches (same faces and arrangement)

- **"Rectify the six-fold corners of the pentakis dodecahedron."** Shallower cuts give t6kD (20 hexagons + 60 pentagons). The OCD is the limit where each pentagon closes to a kite. *Verified by reasoning and the degree data.*
- **Dual of the "joined-lace" dodecahedron (L0D).** Antiprism's `conway` program defines lace (each face augmented by an antiprism) and joined-lace L0 (the new quads not split). L0D gives 12 pentagons, 30 quads and 60 triangles, with 80 vertices: 20 of degree 6 and 60 of degree 4. Those are exactly the Hecatodihedron's counts, so the OCD is combinatorially dL0D. Equivalently, the Hecatodihedron is j6tI (kis on the truncated icosahedron's hexagons, with the hexagon–hexagon edges dissolved). *Reasoned from the operator definition and counts; not run in Antiprism.*
- **Conclusion:** the combinatorial type is reachable with extended Conway operators, so it should **not** be claimed as a new type. I found no page that names or pictures this type.
- **Not matches (checked):** deltoidal hexecontahedron (60 kites, 62 vertices); rectified truncated icosahedron (20 hexagons + 12 pentagons + 60 triangles); truncated pentakis dodecahedron (12 + 80 faces, GV(3,0)); chamfered dodecahedron (80 vertices, 42 faces); Hart's propello-icosahedron (60 kites + 20 triangles, 72 vertices); small icosacronic hexecontahedron (60 kites, non-convex; its dual has 20 hexagons but is a star polyhedron). The standard edge-factor-6 operators (meta, bevel, quinto, join-lace) applied to I or D were compared by counts. Only dL0D matches both counts and face types (quinto qI has the same counts but has triangles and pentagons). *Verified by counts.*

### Metric matches (regular hexagons with these kite angles)

None found.
- **Not a zonohedron:** kites are not centrally symmetric. *Verified by definition.*
- **Not a Johnson solid or near-miss:** the kites are far from regular polygons. *Verified.*
- **Not a Catalan or Archimedean solid:** it is neither face- nor vertex-transitive. *Verified.*
- **Canonical form:** the canonical form of dL0D would have a midsphere. The OCD does not, so even a canonical-polyhedron catalogue would show a different shape. *Verified (float).*

### Sources searched

| Source | Result | Status |
|---|---|---|
| Wikipedia (icosahedral solids, Conway notation, near-miss, Catalan and Goldberg pages) | no 80-face hexagon+kite solid | verified (the "Solids with icosahedral symmetry" page timed out, so not read) |
| Hart, Virtual Polyhedra index and Conway-notation page | no hexagon+kite solid; sections cover uniform, Johnson, zonohedra, stellations | verified (index) |
| Antiprism `conway` docs | operators t_r, k_r, L0 exist; ambo has no degree-restricted form | verified |
| Polytope Wiki (Klitzing, Bowers lists) | nothing matched in searches | search only, lists not browsed |
| MathWorld / PolyhedronData | nothing matched in searches | not checked directly (needs Mathematica) |
| Wenninger *Dual Models*, Holden, Pugh, Inchbald | books, not opened | not checked |
| Counts 102/180/80 and 80/180/102 | no hit | verified search |

**Verdict.** The combinatorial type is reachable by known operators (dL0D, or a6 of the pentakis dodecahedron) but I found it unnamed. The metric solid, with 20 regular hexagons, kites of 117.85°/68.62°/55.69°, and 90 of its 102 vertices on one sphere, was not found. Claim it modestly: "a named metric realisation, not a new combinatorial type".

## Overall novelty statement

The five-fold chorus is a new, exact instance of known ideas, not a new phenomenon. Irrational interfaces are quasiperiodic (Sutton, Gratias–Thalal). The five cubic voices form the icosahedral irrational twin (Ranganathan, Srivastava & Lord). Exclusion can shape a window (Katz & Gratias). What we did not find in the literature:
1. the exact Fibonacci chain **along** the junction axis of five periodic hard-body packings;
2. its selection by a five-fold ring's **self-clash**, with t_c² = 8/9 + 8√5/45, and the result that this window is slightly narrower than the canonical one, so the two agree only for |height| < 12.81;
3. the **equal-cost fork** beyond that height.

All three are exact in ℚ(√5) within the build. The OCD is unnamed in the sources checked, but its combinatorial type follows from standard operators.

## Must-cite list (DOIs verified on Crossref, 2026-10-15)

Interfaces and twins (already in the library):
1. A. P. Sutton (1988). Irrational tilt grain boundaries as one-dimensional quasicrystals. *Acta Metall.* 36, 1291. doi:10.1016/0001-6160(88)90281-7
2. A. P. Sutton (1992). Irrational interfaces. *Prog. Mater. Sci.* 36, 167–202. doi:10.1016/0079-6425(92)90008-U
3. D. Gratias, A. Thalal (1988). Hidden symmetries in general grain boundaries. *Phil. Mag. Lett.* 57, 63–68. doi:10.1080/09500838808229611
4. S. Ranganathan, A. K. Srivastava, E. A. Lord (2006). Coincidence-site lattices as rational approximants to irrational twins. *J. Mater. Sci.* 41, 7696–7703. doi:10.1007/s10853-006-0966-y
5. L. Pauling (1985). *Nature* 317, 512–514. doi:10.1038/317512a0
6. A. Prodan et al. (2017). *Sci. Rep.* 7, 12474. doi:10.1038/s41598-017-12669-w

Window from exclusion (new):
7. A. Katz, D. Gratias (1993). A geometric approach to chemical ordering in icosahedral structures. *J. Non-Cryst. Solids* 153–154, 187–195. doi:10.1016/0022-3093(93)90340-4
8. J. Hubbard (1978). Generalized Wigner lattices in one dimension and some applications to TCNQ salts. *Phys. Rev. B* 17, 494–505. doi:10.1103/PhysRevB.17.494
9. A. C. D. van Enter, H. Koivusalo, J. Miękisz (2019). Sturmian ground states in classical lattice-gas models. *J. Stat. Phys.* 178, 832–844. doi:10.1007/s10955-019-02464-4
10. M. Baake, U. Grimm (2013). *Aperiodic Order, Vol. 1*. Cambridge UP. doi:10.1017/CBO9781139025256

Five-fold junctions and hard shapes:
11. S. Lee, S. C. Glotzer (2022). *Nat. Commun.* 13. doi:10.1038/s41467-022-34891-5
12. J. H. Conway, S. Torquato (2006). Packing, tiling, and covering with tetrahedra. *PNAS* 103, 10612–10617. doi:10.1073/pnas.0601389103
13. H. Hofmeister (1998). Forty years study of fivefold twinned structures in small particles and thin films. *Cryst. Res. Technol.* 33, 3–25. doi:10.1002/(SICI)1521-4079(1998)33:1<3::AID-CRAT3>3.0.CO;2-3
14. M. Kléman (1989). Curved crystals, defects and disorder. *Adv. Phys.* 38, 605–667. doi:10.1080/00018738900101152

Useful context (optional): Rivier & Lawrence 1988 (doi:10.1016/0378-4363(88)90122-2); Sutton 1989 (doi:10.1080/01411598908245732); Xiong, Zou, Zhang & Jiang, arXiv:2603.21158; Gummelt 1996 (doi:10.1007/BF00239998); Jeong & Steinhardt 1997 (doi:10.1103/PhysRevB.55.3520); Henley 1986 (doi:10.1103/PhysRevB.34.797); Mosseri & Sadoc 2014 (doi:10.1016/j.crhy.2013.09.006).

## Open doubts

- **Katz & Gratias.** I know their hard-core argument only from the Widom–Mihalkovič review. Read the 1993 paper before writing "known in general". It may come closer to our mechanism than the review suggests.
- **Gratias–Thalal and Sutton** may already discuss junctions of several irrational boundaries. Their full texts were not read.
- **Russian and French schools** (Kléman, Sadoc, Mosseri, Rivier; Kalugin; the Gratias group's later work on twins in i-phases) were reached only through abstracts. A specialist could know a junction-line result.
- **Hard-particle literature** is large. Ordering in confined cylinders and on five-fold twinned seeds of hard polyhedra (Glotzer and Damasceno group work after 2022) was not searched exhaustively.
- **The OCD book sources** (Wenninger *Dual Models*, Holden, Pugh, Inchbald), Bowers' and Klitzing's full lists, and MathWorld's PolyhedronData were not opened.
- **dL0D identification** is reasoned from counts and the Antiprism definition, not computed. One run of Antiprism (`conway dL_0D`), or a graph-isomorphism check, would settle it.
- **Library hygiene:** Sutton 1992 "Irrational interfaces" appears twice in `MANIFEST.json` (a pre-existing duplicate). I left it as it was.
