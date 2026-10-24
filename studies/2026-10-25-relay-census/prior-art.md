# Prior-art search: relay census (2026-10-25)

Study read: `README.md`, `data/raw/tables.md`, `data/raw/a15.json` (A15 volumes). Companion search
`../../papers/2026-10-25-web-of-bonds/prior-art.md` already covers power diagrams in general
(Aurenhammer), GKZ / Alexeev §5.12 / L-types, Pauling's limits, radical tessellations of CsCl and
fluorite, Wang et al. 2018 and Koch 1973 as the nearest analogue. Those are not repeated here except
where a census claim needs them.

Verdicts: **(a)** known, cited; **(b)** known in a more general form that implies it; **(c)** not
found in the sources searched. "Not found" is limited to the sources listed at the end. Nothing here
is called new.

Every DOI below was checked on api.crossref.org on 2026-10-25 (title, venue, volume, pages, year).
"Not read" means only the abstract or a citing source was seen.

## Most important finds

1. **The A15 walk below the first flip is in Weaire & Phelan 1994 and Kashyap & Neuhoff 2001.**
   Sloane & Vaishampayan 2002 (arXiv:math/0207146, read in full) say that Weaire and Phelan use a
   weighted Voronoi decomposition of A15: like-type walls on bisectors, even–odd walls on the plane
   (X − E)·(D − E) = μ|D − E|², and "for 0 < µ < 3/5 there are two types of Voronoi cells: 12-sided
   ... at the even points and 14-sided ... at the odd points". That plane is a power bisector. In the
   census units (cell edge 2) it is **λ = (5/4)(2μ − 1)**: μ = 0 ↔ λ = −5/4 (the census's lower end),
   μ = 1/2 ↔ λ = 0 (Weaire–Phelan cells), **μ = 3/5 ↔ λ = 1/4 (the census's first flip)**. Kashyap
   & Neuhoff (quoted there) give V₁ = 4α³ with μ = 2α/5, i.e. α = λ + 5/4. Rescaled to cell edge 2
   this is (λ + 5/4)³/2 = (4λ + 5)³/128, **exactly the census's Si-cell volume on (−5/4, 1/4)**
   (checked against `a15.json`). So the A15 interval (−5/4, 1/4), its end flip and its volume are
   **(a)**. The census's further intervals (1/4, 3/4), (3/4, 5/4) and the stops there were not found.
2. **Every named uniform tiling at a stop follows from one classical rule.** If a face-to-face tiling
   has cells that are all inscribed (circumcircle/circumsphere), then adjacent cells' circles meet in
   the shared edge/face, so the shared edge lies on their radical axis/plane, and the tiling is the
   power diagram of its circumspheres (the same argument as "a Delaunay tessellation is the power
   diagram of its circumspheres"; general criteria in Aurenhammer 1987 and Ash & Bolker 1985/1986).
   All uniform tilings and honeycombs have inscribed cells, so each is a power diagram with
   λ = R²(A-cell) − R²(B-cell). Checked numerically here (float, 15 digits) against the census:
   4.8.8 → 2√2 − 2; 3.12.12 → 1 − √3; trihexagonal → −1/2; truncated cubic honeycomb → 2√2 − 1;
   octet / gyrated octet → −1/8 (companion search). All match. So the **values** are **(b)**; their
   place inside a full walk is the census's.
3. **Hinges = non-simplicial dual cells = walls of the secondary fan.** At every hinge the dual
   weighted-Delaunay cell is non-simplicial (square, rhombus, cube, RD), so the hinge is a wall
   point and the two sides are the two regular refinements of that cell, which differ by flips
   (GKZ 1994; De Loera, Rambau & Santos 2010; for lattices, Voronoi's L-type theory — at equal
   weights NaCl and square + centres are the lattices Z³ and Z², whose Delone cells are cubes and
   squares). The diagonal swap in a quadrilateral is the elementary 2D flip; the two splittings of
   the cube that use only one tetrahedron-set of face diagonals are the two "corner-cut" (5-tetrahedra)
   triangulations. Mechanism **(b)**; the classification of these networks into hard/soft **(c)**.
4. **Rock salt at radius ratio √2 − 1 is in Wang et al. 2018.** Their fcc + octahedral-pore crystal
   has large-sphere radical polyhedra with 6 quadrangles + 12 hexagons and small-sphere cubes
   (fetched page, table read): a single point of the census's NaCl interval (0, 1). The full NaCl
   walk, its closed forms and the all-edges-equal point λ = 4 − 2√3 were not found.
5. **One wording issue in the census README** (zinc blende note): "the second kind sits at the deep
   hole of the first kind's lattice, at squared distance 3" is true for CsCl (body centre = deep hole
   of the simple cubic lattice) but **not for zinc blende**: S sits at a tetrahedral hole of fcc,
   which is the *shallow* hole; the deep hole of fcc is the octahedral hole (squared distance 4 in
   those units) (Conway & Sloane, ch. 2/4). Suggest "at a hole of the first kind's lattice (the deep
   hole for CsCl, a shallow tetrahedral hole for zinc blende)".

## Verdict table

| # | Claim | Verdict | Sources (verified DOIs) | Note |
|---|---|---|---|---|
| 1 | Equal-weight and end cells are the classical Voronoi cells (sc cubes, fcc RD, bcc truncated octahedra, diamond triakis truncated tetrahedra, hcp-oct-holes hexagonal prisms, square/hexagon/triangle/rhombille in 2D) | **(a)** | Conway & Sloane, SPLAG 10.1007/978-1-4757-6568-7; Grünbaum & Shephard, *Tilings and Patterns* (1987, no DOI); Conway, Burgiel & Goodman-Strauss 2008 (in library); Blatov 2004 10.1080/08893110412331323170 | Sanity checks only. |
| 2 | Weight walk, CsCl (bcc two-kind): range (−3, 3), flips ±1, soft relay | **(b)** for the framework and the special members; **(c)** for the walk | Companion search (Alexeev 2002 10.2307/3062130; Wang et al. 2018 10.1063/1.5052478) | Already in paper #52. |
| 3 | Weight walk, fluorite: range (−3/8, 3/8), one flip at −1/8 (octet), hard relay | **(b)** for the octet as power diagram; **(c)** for the walk | Companion search | Already in paper #52. |
| 4 | Square + centres: range (−2, 2), hinge at 0, 4.8.8 on each side | **(b)** | Aurenhammer 1987 10.1007/BF02187870; Ash & Bolker 1986 10.1007/BF00164401; Kennedy 2006 10.1007/s00454-005-1172-4 (binary disc packing at ratio √2 − 1, context only) | Equal weights = the lattice (rotated Z²) whose Delone cells are squares, so a wall is forced there; each side is one diagonal triangulation. Whole walk is elementary; no paper giving it was found. |
| 5 | Honeycomb + centres: hinge at −1/2 = trihexagonal 3.6.3.6; 3.12.12 side | **(b)** for the tilings and their weights; **(c)** for the walk | as #4; Grünbaum & Shephard | 3.6.3.6 has inscribed faces, so it is the power diagram of its circumcircles: λ = R²_tri − R²_hex = −2a²/3 = −1/2 at a² = 3/4 (checked). |
| 6 | Kagome + centres: no flip in the whole range | **(c)** | — | Equal-weight cells (rhombille = kagome Voronoi) are classical. |
| 7 | NaCl: range (−1, 1), hinge at 0 (cubes), 6-square + 12-hexagon Na cells | **(a)** at one point; **(b)** for the hinge; **(c)** for the walk, closed forms and λ = 4 − 2√3 | Wang et al. 2018 10.1063/1.5052478 (one point: ratio √2 − 1); Dutour Sikirić, Schürmann & Vallentin 2008 10.1215/00127094-2008-003 (L-types; via companion) | λ = 4 − 2√3 "all edges equal" is not a uniform polyhedron (chamfered-cube face vector), so rule 2 above does not cover it. |
| 8 | Zinc blende / diamond: range (−3, 3), flips ±1, soft relay | **(c)** | Equal-weight cell (a): Conway & Sloane | — |
| 9 | CsCl ≡ zinc blende: identical λ-polynomials up to constants | **(c)** | Context: Conway & Sloane (bcc = Z³ ∪ (Z³ + deep hole); diamond = D₃⁺ = D₃ ∪ (D₃ + [½³]) in their notation) | No explanation found. See find 5: the "deep hole" wording is wrong for zinc blende, so the README's proposed common reason does not hold as written. |
| 10 | hcp holes: range (−11/24, 3/8); flips −1/8 and 5/24; no hinge (gyrated octet keeps cross-layer like bonds) | **(b)** at −1/8; **(c)** for the walk, the 5/24 flip and the "switch splits" reading | Gyrated tetrahedral–octahedral honeycomb = Delaunay of hcp, dual trapezo-rhombic dodecahedra: Conway, Burgiel & Goodman-Strauss 2008 (in library); Wikipedia PDF in library | Same circumsphere rule as the octet (both circumradii are those of the regular octahedron/tetrahedron), so λ = −1/8 again. |
| 11 | A15: range (−5/4, 5/4), flips 1/4 and 3/4, overlap (1/4, 3/4) | **(a)** for (−5/4, 1/4], the flip at 1/4 and the Si volume there; **(c)** beyond 1/4 | Weaire & Phelan 1994 10.1080/09500839408241577 (not read; content via the next); Sloane & Vaishampayan 2002 10.1109/TIT.2002.805086, arXiv:math/0207146 (read); Kashyap & Neuhoff 2001 10.1109/18.945264 (not read; formula quoted by Sloane–Vaishampayan) | See find 1. The 3/4 stop (Si combinatorially icosahedral, Cr tetrahedra) and 5/4 end not found. |
| 12 | A15 equal weights = Weaire–Phelan cells | **(a)** | Weaire & Phelan 1994; Frank & Kasper 1958 10.1107/S0365110X58000487 and 1959 10.1107/S0365110X59001499; Reddy et al. 2018 PNAS 10.1073/pnas.1809655115 (A15 as 2 Z12 + 6 Z14 Voronoi cells; weighted partitions after Kusner & Sullivan) | — |
| 13 | C15: range (−11, 11), flips −5, 7, 9; equal-weight cells 12- and 16-faced | **(a)** for the equal-weight cells; **(c)** for the walk | Frank & Kasper 1958/1959; Reddy et al. 2018 (Laves Voronoi volume asymmetry) | Weighted ("Kusner–Sullivan") partitions of FK phases are used in the soft-matter literature; no C15 weight walk found. |
| 14 | Perovskite: rectangle −2 ≤ λ ≤ 2, −1 ≤ μ ≤ 1; three straight walls, 5 chambers; B–B never | **(b)** for "chambers bounded by walls" (secondary fan); **(c)** for this chamber map | GKZ 1994 10.1007/978-0-8176-4771-1; Alexeev 2002 | — |
| 15 | Hard vs soft relay classification across networks | **(c)** | — | Not found as a notion. |
| 16 | Flip locations as exact rationals | **(b)** in principle (walls of a secondary fan are rational hyperplanes for rational data); **(c)** for the values except A15 at 1/4 (a) and the octet −1/8 (b) | GKZ; De Loera, Rambau & Santos 2010 10.1007/978-3-642-12971-1 | — |
| 17 | Hinges: square tiling, 3.6.3.6, cubes (NaCl), octet (fluorite) | **(b)** | as #4, #5, #7, companion | Each is a power diagram whose dual has non-simplicial cells (wall points). |
| 18 | Named stops 4.8.8 at ±(2√2 − 2), 3.12.12 at 1 − √3, uniform truncated cubic honeycomb at ±(2√2 − 1) | **(b)** | Aurenhammer 1987 10.1007/BF02187870; Ash & Bolker 1985 10.1007/BF00181470, 1986 10.1007/BF00164401; tilings: Grünbaum & Shephard 1987; Andreini 1905 (no DOI) | Values = differences of circumradii², checked here (find 2). |
| 19 | Diagonal-swap pattern at every hinge | **(b)** | GKZ 1994; De Loera, Rambau & Santos 2010 (flips on circuits; cube triangulations) | The four cases are instances of a flip at a wall; that the swapped pair is always a like/like diagonal pair of one dual quadrilateral **(c)**. Census itself says "not proved in general". |
| 20 | The unlike bond never breaks while both kinds have cells (two-kind networks) | **(c)** | — | No general statement found; the census has it for 10 networks only, and it fails for perovskite. Not claimable as a theorem without proof. |
| 21 | Golden loop = exactly the soft chamber [−1, 1] of CsCl | **(c)** | — | Follows from #2 and paper #52's weights. |

## What a census paper could honestly claim

- **Method.** An exact (rational-arithmetic) walk of power diagrams of fixed two-kind and three-kind
  crystal site sets along the weight difference, with every stop exact and every interval checked
  (volumes, faces, Euler, completeness). Software that computes radical tessellations numerically
  exists (Voro++, ToposPro, Zeo++/CAVD); an exact walk with certified intervals was not found.
- **Data.** The full sequence of face lattices, bond lives and flips for square + centres, honeycomb
  + centres, kagome + centres, NaCl, zinc blende, hcp holes, A15 (beyond λ = 1/4), C15 and
  perovskite, with closed-form areas and volumes — not found in the sources searched, with the
  explicit exceptions: A15 up to its first flip (Weaire & Phelan 1994; Kashyap & Neuhoff 2001),
  single points (Wang et al. 2018), and all classical equal-weight cells.
- **Explained as instances of known theory, and should be presented that way:** the named uniform
  tilings at stops and their weights (circumsphere rule), the hinges as walls of the secondary fan
  with non-simplicial dual cells, the diagonal swap as the elementary flip, the octet/gyrated-octet
  stops.
- **Observations, labelled as observations (not theorems):** the hard/soft split; the unlike bond
  surviving the whole range in every two-kind case computed; the CsCl ≡ zinc blende polynomial
  coincidence (unexplained; fix the "deep hole" wording); the hcp split at −1/8 and 5/24.
- **Should not be claimed:** that power diagrams, radical tessellations, Weaire–Phelan as A15
  Voronoi, A15 weighted cells on (−5/4, 1/4], or any of the named tilings are discovered here;
  any priority on "flips at walls".
- **Credit line suggestion:** the A15 paragraph should open with "Weaire and Phelan already used this
  family for 0 < μ < 3/5 (our λ < 1/4); Kashyap and Neuhoff gave its cell volumes".

## Legally free copies for the library (not added)

| Source | Free copy |
|---|---|
| Sloane & Vaishampayan 2002 | arXiv:math/0207146 (read here) |
| Reddy et al. 2018 PNAS | arXiv:1806.01726 |
| Wang et al. 2018 | AIP Advances, open access CC BY (doi link) |
| Kashyap & Neuhoff 2001 | no free copy found (IEEE); an ISIT 2001 abstract exists, 10.1109/ISIT.2001.936047 (not verified by direct DOI lookup) |
| Weaire & Phelan 1994 | no free copy found (Taylor & Francis) |
| Frank & Kasper 1958/1959 | IUCr journals; older Acta Cryst. articles are often free to read at journals.iucr.org (check rights) |
| Koch 1973, Koch & Fischer 1978 | De Gruyter; no free copy found |
| Alexeev 2002, Dutour Sikirić et al. 2008 | arXiv:math/9905103, arXiv:math/0601084 (from companion) |

## Sources searched (2026-10-25)

- DICTO's library: `~/bin/ask-library`, 3 queries (Voronoi cells of lattice complexes Koch/Fischer;
  Laguerre/radical tessellation of NaCl/zinc blende; weighted Voronoi of Archimedean tilings): no
  relevant hits (nearest: Garber 2019, Erdahl 1999, Gabbrielli–Jiao–Torquato 2012). INDEX.html
  searched for Koch, Fischer, Sloane, O'Keeffe, Hyde, Blatov, Dolbilin, Engel, Dirichlet, Kasper,
  Weaire, Laves, lattice complex, Archimedean, Grünbaum, Shephard: Koch 1973, Blatov 2004, O'Keeffe
  1979 and Frank & Kasper 1958 are listed link-only; no Weaire, Laves, Fischer, Hyde, Dolbilin.
- Web (about 12 standard/extended queries): radical/Laguerre tessellation with NaCl, zinc blende,
  perovskite, binary hard-sphere crystals; Archimedean tilings as power diagrams; Koch 1973; Fischer,
  Koch & Hellner; Frank–Kasper/Laves Voronoi; Weaire–Phelan weighted Voronoi; Kusner–Sullivan;
  O'Keeffe & Hyde; weighted Delaunay flips in crystals; trihexagonal tiling as power diagram.
- Read in full: Sloane & Vaishampayan 2002 (arXiv). Read in part: Wang et al. 2018 (publisher page).
- Crossref: all DOIs in the table.
- **Not reached / not read:** the full texts of Koch 1973, Koch & Fischer 1978, Weaire & Phelan 1994,
  Kashyap & Neuhoff 2001, Ash & Bolker, Blatov 2004, Engel 1986 (*Geometric Crystallography*,
  10.1007/978-94-009-4760-3), O'Keeffe & Hyde (*Crystal Structures I*, MSA 1996 / Dover 2020, no
  DOI), Delone/Dolbilin; Google Scholar; Fischer, Koch & Hellner 1971 ("Wirkungsbereiche in
  Strukturen anorganischer Verbindungen", cited from memory, not found online, not verified). Koch's
  later papers on cubic point configurations (Z. Kristallogr. 1984) were not resolved to a DOI.
