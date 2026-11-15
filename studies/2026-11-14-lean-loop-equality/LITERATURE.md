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

---

# Literature search for the second entry: the Loop Equality (#102, Theorem 1) (2026-11-15)

**Question.** Has anyone already stated that every site of every close-packed stacking has the same number of closed non-backtracking walks of each length?

**Conclusion.** We found no such statement. The nearest results are each one step short of it:
- the equality for **all closed walks** in periodic polytypes (Thorpe 1972; Nagle 1966 for ice);
- the equality of **band structures** of all close-packed stackings through a layer gauge (He–Wilson–Ganesh 2024), and of their nearest-neighbour **transport** (Wilson–Ganesh–Samokhin 2026);
- for periodic stackings, the **site-averaged** loop counts, which follow from Thorpe together with the Bass formula for periodic graphs (Guido–Isola–Lapidus 2008), as #102 already says.

New in #102 are the statement at every single site (walk-regular, not vertex-transitive), aperiodic stackings, and the corollaries. The formal proof makes the dependence explicit: the loops through a bond are fixed by the walk counts on that bond's four end pairs (#102, Lemma 3), and those counts do not depend on the stacking.

**Honest notability estimate: 3 out of 5, 3.5 at best.** That is still below Palomar's floor of 4, though better than #43 Theorem 4 (2 out of 5).
- For: the research audience is clear (polytypes, spin ice and ice entropy, Ihara zeta functions of periodic and aperiodic graphs). The statement is exact, for all lengths, and covers aperiodic stackings, which the periodic-graph zeta literature does not reach. The ice-polytype entropy question is active (Chen–Ran 2026; Xu–Lin–Zhang 2025).
- Against: an editor may read it as a corollary. Thorpe's closed-walk equality plus the standard Hashimoto/Ihara reduction gives it once one also checks the bond walk counts (#102, Lemma 2 (b)), which is a short Fourier computation.

## Queries and sources (15 November 2026)

**Web searches**, with the query strings used:
1. `non-backtracking walks closed same count hexagonal cubic polytypes diamond lonsdaleite every site`: only structural papers on lonsdaleite and diamond.
2. `Ihara zeta function close-packed stacking fcc hcp polytype equal non-backtracking cycles`: only stacking-statistics papers (arXiv 1706.07852, 1708.01460, cond-mat/9810287) and arXiv 2602.18574.
3. `"walk-regular" infinite graph not vertex-transitive stacking polytype closed walks equal Thorpe`: arXiv 1211.5689 (walk-regular graphs and hitting times), 0806.2074 (periodic graphs), 2401.06022 (walk-regular planar graphs). None treats stackings.
4. `Thorpe "Random walks in polytype structures" 1972 citing non-backtracking` (extended search): Thorpe's abstract (ResearchGate listing) and one citing book chapter (*Energy Bands*, Springer). No non-backtracking follow-up.
5. `Wilson Ganesh Samokhin 2602.18574 close-packed gauge symmetry hopping`: arXiv 2602.18574 (abstract read: nearest-neighbour conductance is insensitive to stacking disorder; the first difference comes from next-nearest-neighbour hopping) and arXiv 2405.15865 (He–Wilson–Ganesh, abstract read).
6. `"non-backtracking" OR "Hashimoto" "stacking" lattice cubic hexagonal ice loops same number Bethe lattice Pauling`: arXiv 2608.07613 (Chen–Ran, *Hexagonal stacking maximizes proton configurational entropy among ice-I polytypes*). Abstract read: entropy bounds and an inequality method on even-length words; it says the equality of the cubic and hexagonal constants is open, and states no loop equality. Also arXiv cond-mat/0208303 and 1308.1014 (spin ice background).
7. `cospectral vertices local spectrum infinite graphs layered gauge equivalent periodic aperiodic stacking walk counts`: arXiv 2308.04339 (de la Harpe, cospectral infinite graphs), 2205.12819 (local spectral measures; all vertices are dominant in walk-regular graphs), 2007.07609, 2111.01265. None treats stackings.
8. `"non-backtracking" closed walks "close-packed" OR "polytypes" equal every vertex aperiodic stacking theorem` (extended search): Kempton arXiv 1610.04672 (closed non-backtracking walks on ℤ²), 1209.3996, 1507.03411, 2406.05759. None treats stackings.

**Already searched for #102 itself** (7 November 2026; listed in #102 Section 5): DICTO's reference library (259 items, catalogue and full text); OEIS A002895, A293237; Thorpe 1972 and Betteridge 1981 (Crossref abstracts); He–Wilson–Ganesh; Isaev–McKay–Zhang §8.2; Bercu–Montégut; the OpenAlex list of the 17 works citing Thorpe 1972.

**Not searched:** MathOverflow (not reachable from here), and the full texts of the 17 works citing Thorpe (only their titles were read).

**Palomar database:** the one indexed entry (read 15 November for #43) is unrelated.

## Fidelity of the Lean statement

`DictoLoopEquality.loop_equality` states exactly the counting claim of Theorem 1: for every stacking (periodic or not), every site and every length m, the number of closed non-backtracking loops equals the number at diamond's site. It needs no extra hypothesis; for m = 1, 2 both sides are 0. The explicit series and values (Ihara–Bass, Domb numbers) are **not** part of the formal statement. `nbLoops_finite` makes sure `ncard` is a true count.

---

# The strengthened entry: explicit count and the Fibonacci corollary (2026-11-15, later)

**Question.** Does the explicit count (`loop_count_eq`, `W_closed`) together with the aperiodic Fibonacci corollary lift the Loop Equality entry to Palomar's notability floor of 4?

**Conclusion. Honest estimate: 3.5 out of 5, not reliably 4.** The strengthening makes the entry more complete and easier to judge, but it does not change what an editor will see as the new mathematics.
- **For.** The formal statement now carries the number itself: every site of every stacking has exactly `loopCount m` loops, with all fifteen of #102's values (m = 6..34) proved, and the closed walks given in closed form (#102 Proposition; the chain form of the Domb numbers). The local loop formula (`Graph.sum_F_eq`) is a general fact about walk-regular graphs with q + 1 neighbours everywhere. In that setting the loops at a single vertex follow from the closed walks alone; for finite graphs this is usually seen only through the Ihara–Bass trace formula. The Fibonacci corollary shows, in the same formal development, that the theorem covers a genuinely aperiodic network, which the periodic-graph zeta literature (Clair–Mokhtari-Sharghi 2001; Guido–Isola–Lapidus 2008) does not reach.
- **Against.** The closed-walk values for diamond are classical: Domb numbers (Domb 1960; OEIS A002895). So is the reduction of non-backtracking loops to walks (Ihara 1966; Hashimoto 1989; Bass 1992). The explicit count adds a computation, not a new idea. The aperiodicity of the Fibonacci word is classical (Morse–Hedlund 1940; Lothaire 2002, Ch. 2), and the Fibonacci corollary is an instance of the main theorem. The identity with #102's Ihara–Bass series and with Domb's closed form is checked only for small m and n. An editor could still read the whole entry as "Thorpe 1972 plus the standard Ihara–Bass reduction".
- **What could reach 4.** Proving the Ihara–Bass series for all m. Better still, adding a second, independent result of the same series that is clearly new. Neither is done here.

**Credits at the point of use (Lean doc strings and the outline, Section 7).** Ihara 1966, Hashimoto 1989, Bass 1992 (the recursion and the series); Domb 1960 and OEIS A002895 (Domb numbers); Peter Bala's OEIS comment (chain form); Nagle 1966, Thorpe 1972 (closed walks); Morse–Hedlund 1940 and Lothaire 2002 (Sturmian words, aperiodicity, cut-and-project form); Jagodzinski (the c/h layer rule).

**Extra searches (15 November 2026, web):**
1. `Fibonacci stacking close-packed polytype aperiodic random walks spectrum`: stacking-disorder and diffraction papers (Varn–Canright–Crutchfield, arXiv cond-mat/0302585 and cond-mat/0203290), Fibonacci-chain hyperuniformity (arXiv 2405.03752), polytype band gaps (arXiv 2306.17756). None treats walk or loop counts on a Fibonacci-stacked network.
2. `Ihara zeta function aperiodic graph Fibonacci non-backtracking walks quasiperiodic`: periodic-graph zeta functions (arXiv math/0605753, math/0608229, 2102.09486, 1910.12782), non-backtracking walk matrices (arXiv 1706.00851). Nothing on aperiodic or Fibonacci graphs.

**Novelty text for the Fibonacci part:** the Fibonacci stacking itself and its aperiodicity are not claimed as new. The new content is the loop statement on it, which is an instance of #102 Theorem 1.

**Fidelity notes.**
1. `fibonacci` is defined for all k ∈ ℤ by the cut-and-project form of the Sturmian word, the natural two-sided extension. DICTO's study and #102's checks use the one-sided substitution word (c ↦ ch, h ↦ c, from c). The two are proved equal at positions 0..99 (`isH_eq_word`); equality at every position is the classical Sturmian characterisation and is not formalised.
2. The steps follow Jagodzinski's rule exactly as in `letters_from_ch` of #102's checks: σ0 = A, σ1 = B, and the step reverses at h layers (`fibonacci_layer_type`).
3. Aperiodicity is proved both for the type word (`isH_not_periodic`) and for the stacking itself (`fibonacci_not_periodic`, every nonzero shift).
