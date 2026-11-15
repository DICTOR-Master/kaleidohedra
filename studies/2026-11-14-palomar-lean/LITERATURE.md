# Literature search for the Palomar entry: #43 Theorem 4, the octahedral constant 3 (2026-11-15)

**Conclusion.** The covering lemma is **known**: it says that the orbit space S²/O has diameter arccos(1/√3), and that value is in print (Greenwald 2000; Dunbar–Greenwald–McGowan–Searle 2009, Table 2), together with the icosahedral value that Theorem 2 uses. We did not find the containment S ⊂ 3·P(S) for the foot-point hull stated anywhere. But it follows from the known diameter in two elementary steps (#43 Theorem 1 and the orbit hull), and sharpness is a one-line check on the cube. An editor will likely read the entry as a neat corollary of a known orbit-space computation, not as a research result. **Honest notability estimate: 2 out of 5, 3 at best.** That is below Palomar's floor of 4.

**Status:** search done (web, arXiv, the Palomar database and DICTO's reference library). MathOverflow could not be reached, and the indexes of Grünbaum and Schneider were not read, because no legal copy was at hand. Nothing has been submitted.

## 1. Statements checked (from #43 v3 and `lean/OctahedralNesting.lean`)

- **Covering lemma (O).** For all unit vectors u and w, some rotation g of the octahedral group O (24 rotations) has ⟨gu, w⟩ ≥ 1/√3.
- **Theorem 4.** A convex polytope S = {x : ⟨nᵢ, x⟩ ≤ hᵢ} with octahedral rotational symmetry about O satisfies S ⊂ 3·P(S), where P(S) = conv{hᵢnᵢ} is the hull of the foot points (Smarandache's face pedal polyhedron).
- **Sharpness.** For the cube no c < 3 works.
- **Theorem 2.** With icosahedral rotational symmetry, S ⊂ (15 − 6√5)·P(S), sharp (icosahedron, dodecahedron). Its covering lemma uses c = √((5 + 2√5)/15).
- **Related.** Corollary 7: 3 for T_h and 9 for T and T_d. Theorem 1: S ⊂ (R/r)²·P(S) for every polytope with O inside.

## 2. Queries and sources

**Web and arXiv searches (15 November 2026), with the query strings used:**
1. `Fazekas Levenshtein covering radius spherical designs upper bound 1995`
2. `convex body octahedral symmetry circumradius inradius ratio sqrt 3 rotation group`
3. `"covering radius" orbit finite rotation group sphere octahedral icosahedral worst orbit`
4. `diameter of 2-sphere quotient S^2/G orbifold finite group octahedral icosahedral diameter`
5. `Dunbar Greenwald McGowan Searle "Diameters of 3-sphere quotients" Differential Geometry and its Applications`
6. `convex polytope contained in dilate of convex hull of feet of perpendiculars to facets pedal polytope containment constant`
7. `site:mathoverflow.net convex hull of tangency points facets symmetric polytope dilate contains` (returned no MathOverflow pages)
8. `convex body "enough symmetries" John ellipsoid ball circumradius inradius ratio n irreducible symmetry group`
9. `inradius of orbit polytope finite reflection group minimum over orbits "orbit polytope" inradius circumradius`
10. `Smarandache "pedal polyhedron" foot points face planes antipedal polyhedron`
11. `arXiv convex body invariant under finite rotation group sharp bound circumradius over inradius tetrahedral 3 octahedral sqrt3 icosahedral` (extended search)

**Read in full or in the relevant part:**
- W. D. Dunbar, S. J. Greenwald, J. McGowan, C. Searle, *Diameters of 3-sphere quotients*, arXiv:math/0702680 (2007); Differential Geom. Appl. 27(2) (2009) 307–319 (journal details from a citing reference, not the publisher's page). Read: Lemma 3.2, its proof, Table 2 and the references.
- arXiv:2007.05599, P. Boyvalenkov, M. Stoyanova, *Linear programming bounds for covering radius of spherical designs* (abstract page). It cites Fazekas–Levenshtein for covering-radius bounds of τ-designs, but the abstract does not state the formula.

**Seen at abstract or snippet level only:**
- G. Fazekas, V. I. Levenshtein, *On upper bounds for code distance and covering radius of designs in polynomial metric spaces*, J. Combin. Theory Ser. A 70 (1995): the MaRDI catalogue entry only.
- Boyvalenkov–Dragnev–Hardin–Saff–Stoyanova, arXiv:1906.03062 (also in the library).
- arXiv:1903.12619, *A diameter gap for quotients of the unit sphere*.
- arXiv:2608.01156, which treats the least covering radius of finite orthogonal orbits.
- A. Barvinok, G. Blekherman, *Convex geometry of orbits*, arXiv:math/0312268: for a G-invariant body, the John and Löwner ellipsoids are balls when G is rich enough.
- R. Holmes, T.-Y. Tam, distance to the convex hull of an orbit, J. Austral. Math. Soc. (1999).
- arXiv:2110.09322 (orbit polytopes).
- arXiv:1003.2153 (Smarandache's face pedal polyhedron, posed as an open problem).
- arXiv:2108.08293 and arXiv:1008.0110 (pedal and antipedal polygons).
- arXiv:2509.05028 and arXiv:2402.06629 (inequalities between radii in 3D, with no symmetry group).
- Sloane's tables of spherical coverings (Hardin–Sloane–Smith), via cohn.mit.edu/sloane. These give the best coverings by N points, not the worst orbit of a group, so they do not bear on the lemma.

**MathOverflow:** the site could not be fetched from here, and the `site:` search returned no MathOverflow pages. **MathOverflow was therefore not searched.**

**Books:**
- Grünbaum, *Convex Polytopes*: link-only in DICTO's library, with no legal copy, so the index was **not read**.
- Schneider, *Convex Bodies: The Brunn–Minkowski Theory*: not in the library and no legal copy, so the index was **not read**.
- Conway–Sloane, *SPLAG*: link-only, not read.

**Palomar.** Repositories read:
- `henriqueheine/PalomarDatabase` @ 23da4f1: `index.json` and the one entry, PALOMAR-2026-07-29-000001 v1/v2 (K. Morrison, "Uniform-constant Erdős unit-distance conjecture is false", MSC 52C10)
- `PalomarRegistry/PalomarReviewer` @ ba9b26c: the file list; the editorial prompts are not published there
- the organisation's repository list

The database holds no similar entry, and its only accepted entry sets a high bar.

**DICTO's reference library.** Six MANIFEST.json files (papers, bridges, history, expansion, gaps, cited) were searched for: Schneider, Grünbaum, convex body or polytope, covering, spherical design, Delsarte, Levenshtein, John ellipsoid, Banach, Macbeath, pedal, orbit polytope, Sloane, Hardin, inradius, circumradius, cubature, Seidel. Relevant hits:
- Grünbaum 1967 (link-only)
- Castellano–Manack 2013 and Hsu et al. 2021 (pedal polygons; planar only)
- Ferrarello–Mammana–Pennisi (pedal polygons; link-only)
- Boyvalenkov et al. 2019 (Levenshtein framework)
- Conway–Sloane (link-only)

None states the containment or the orbit covering. The full-text search of 77 library sources made for #43 v1 (21 October 2026) also found nothing.

**Macbeath:** searched within the library only; no hit bears on foot-point hulls. Macbeath regions concern floating bodies and are not related.

## 3. Verdicts

**Covering lemma (O): KNOWN.** The lemma says exactly that diam(S²/O) ≤ arccos(1/√3), where the orbit-space distance is d([u], [w]) = min_g d(gu, w).
- Dunbar–Greenwald–McGowan–Searle (2009), Table 2 "Subgroups of O(3) and Corresponding Diameters", lists S²/O (432) with diameter arccos(1/√3). The same table gives T: arccos(1/3), T_d: arccos(1/3), T_h: arccos(1/√3), O_h: arccos(1/√3), I and I_h: arccos(tan(3π/10)/√3).
- They credit S. Greenwald, *Diameters of spherical Alexandrov spaces and curvature one orbifolds*, Indiana Univ. Math. J. 49(4) (2000) 1449–1479 (and the 1998 PhD thesis), and J. McGowan, Compositio Math. 87 (1993) 79–98.
- A second route, known in substance: O's orbits are spherical 3-designs (Goethals–Seidel 1981, already cited in #43), and linear-programming covering-radius bounds for designs go back to Fazekas–Levenshtein 1995. We believe their τ = 3 bound in ℝ³ is 1/√3, which is the #43 cubic argument, but we have **not verified** the formula from the paper itself.

**Icosahedral covering lemma: KNOWN.** The same Table 2 gives diam(S²/I) = arccos(tan(3π/10)/√3). Since tan(54°)/√3 ≈ 0.79465 = √((5 + 2√5)/15), this is #43's c.

**Containment constant 3 (Theorem 4): NOT FOUND in the sources checked as a statement about foot-point hulls; KNOWN IN SUBSTANCE.** The translation needs two short steps:
1. A G-invariant S contains the hull of the orbit of a farthest corner. So r(S) ≥ R(S)·cos(diam(S²/G)).
2. #43 Theorem 1 gives S ⊂ (R/r)²·P(S). We did not find Theorem 1 in the literature, but its proof is a few lines.

So the constant is sec²(diam(S²/G)). This gives:
- 3 for O, O_h and T_h
- 9 for T and T_d (Corollary 7)
- 3·tan²(π/5) = 15 − 6√5 for I and I_h (Theorem 2)

For the centrally symmetric groups (O_h, T_h, I_h), John's theorem with an irreducible symmetry group already gives R/r ≤ √3, and so the constant 3, though not 15 − 6√5 for I_h. For the chiral group O the John bound is only R/r ≤ 3, giving 9, so the orbit-space diameter is needed.

**Sharpness: KNOWN IN SUBSTANCE (elementary).** For the cube, R/r = √3 and P(S) is the octahedron conv{±eᵢ}. The corner (1, 1, 1) lies in c·P(S) only if c ≥ 3. This is a check, not a result.

**Icosahedral constant 15 − 6√5: NOT FOUND as a containment statement; KNOWN IN SUBSTANCE.** It is sec² of the known diameter of S²/I, by the same two steps. The closed form 15 − 6√5 = 3·tan²(π/5) may be worth one line in the paper.

**Polar side (Lemma 3, polar(P(S)) = T(polar S)):** not found. It is elementary, and #43 already says so.

## 4. Notability, as an editor would see it

What is true and checkable:
- The statement is clean and sharp.
- The idea of comparing a polytope with the hull of its foot points is DICTO's.
- The constants for all three polyhedral groups come out in one formula.

What an editor will weigh:
- The deep step, the covering radius of the worst orbit, is a recorded computation in the orbifold-diameter literature.
- The rest is an elementary inequality.
- The audience is narrow: discrete geometry with a recreational flavour.
- Palomar's bar is that the result "plausibly warrants a research paper or a serious research note". A Lean proof of a corollary of a known 2000/2009 table is unlikely to meet it.

**Estimate: notability 2 out of 5, 3 at best, so likely rejected on notability.**

This also bears on the plan in README §3. #102, the Loop Equality, has a stronger claim to notability and should be weighed as the first entry instead. If #43 is still submitted, the informal account must cite Greenwald and Dunbar et al. for the covering lemma, so that the entry is not read as repackaged work.

## 5. Proposed `formalization.yaml` novelty text

```yaml
novelty: >
  The covering lemma formalised here (every orbit of the octahedral rotation
  group on the unit sphere comes within arccos(1/sqrt 3) of every direction)
  is equivalent to the known diameter of the orbit space S^2/O, recorded by
  S. Greenwald (Indiana Univ. Math. J. 49 (2000) 1449-1479) and in Table 2 of
  Dunbar, Greenwald, McGowan and Searle (Differential Geom. Appl. 27 (2009)
  307-319). The containment S ⊆ 3·P(S) of an octahedrally symmetric polytope
  in three times the hull of its facet foot points, with sharpness for the
  cube, is stated in DICTO, "Kyushindo Cores" (Zenodo, 2026, Theorem 4). In a
  literature search (web and arXiv queries, the Palomar database, and the
  author's reference library; listed in LITERATURE.md) we did not find this
  containment stated elsewhere, but it follows from the known orbit-space
  diameter by an elementary argument, and we make no stronger novelty claim.
  To our knowledge this is the first Lean formalisation of either statement.
```

The last sentence must be checked against Mathlib and Reservoir before use. If it cannot be checked, drop it.
