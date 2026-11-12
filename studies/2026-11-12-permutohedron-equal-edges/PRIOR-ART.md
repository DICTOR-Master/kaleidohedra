# Prior-art check: DICTO 13-Corner Octet Atom and the 369 new atoms (13 Nov 2026)

Literature only. No computation was run for this check. Matches are made against the study's own tables
(`data/raw/solids-*.csv`), the corners in `figures/a3-16.json`, and the published lists named below.

## Conclusions

**1. DICTO 13-Corner Octet Atom (DICTO 13-COA, A3-16 = B3-36): (a) known.** The solid is the
**augmented cuboctahedron**: a cuboctahedron with a square pyramid (J1) on one square face. The four pyramid triangles
lie in the planes of the four neighbouring cuboctahedron triangles, so each pair merges into a 60°/120° rhombus.
- Tupelo-Schneck's table of the convex regular-faced polyhedra with conditional edges lists it as **P3,35** (Timofeenko's
  numbering) = **S20** (Gurin–Zalgaller's numbering), "augmented cuboctahedron", composition M2 + M4 + M4′
  (square pyramid + two triangular cupolas), with V 13, E 24, F 13, F3 = 4, F4 = 5, F3+3 = 4.
- Kaufman's page "Convex Diamond-Regular Polyhedra" (Doskey, Kaufman and Waterman list, 2006) lists it as
  (B4)+Y4[TT], C4v, 4 diamonds, 4 triangles, 5 squares, F 13, E 24, V 13. It credits the solid to B. M. S.
  (Bonnie M. Stewart, *Adventures Among the Toroids*, 1970; 2nd ed. 1980).
- Wikipedia, "Diminished rhombic dodecahedron": "the same topological polyhedron with different proportions can be
  constructed as an augmented cuboctahedron… merging of neighboring coparallel triangular faces into new 60° rhombic
  faces. It retains 5 square faces, and 4 equilateral triangle faces of the cuboctahedron." C4v.
- Timofeenko proved the list of 78 complete (Gurin–Zalgaller 2008; Timofeenko 2009, 2010, corrections 2011). Our solid is
  convex, every corner is a real corner, and every face is regular or a 3+3 rhombus, so it must be on that list.
  P3,35 is the only entry with these counts.

*Match checked against the corners* (`figures/a3-16.json`, edge 1, read by hand). Corners 0–3 (x = 0.816), 4, 5, 6, 8
(x = 0.109) and 7, 9, 11, 12 (x = −0.598) form a cuboctahedron seen along a four-fold axis: a unit square, a square of side √2,
and a unit square aligned with the first. The two unit squares are √2 apart, and every square-to-middle distance is 1. Corner 10
lies 1/√2 below the centre of the square 7, 9, 11, 12, so it is a square-pyramid apex. Each rhombus, e.g. [10, 7, 5, 11], is
the cuboctahedron triangle (5, 7, 11) together with the pyramid triangle (10, 7, 11). The four triangles and five squares that remain
are the cuboctahedron's. The study's description, "a square cupola (J4) with four 60° rhombi", describes the same solid.
It is not a Johnson solid only because the merged triangles are coplanar.

**What may still be called new, as far as the sources checked show:** that this solid is an *indecomposable (atom)
equal-edged member of the A3 permutohedron deformation cone*. No source checked discusses it as a Minkowski summand. The
shape itself must not be printed as new. DICTO's name **DICTO 13-Corner Octet Atom** stays as DICTO's name for its role as
the A3 atom. Text should say it "is the augmented cuboctahedron (Stewart 1970; P3,35 / S20)". The companion
atom A3-10 = B3-19 is the **augmented octahedron**, P3,33 = S15 ("trirhomb", Gurin–Zalgaller), as the README already says.
Subbotin (2026) treats P3,33 and the biaugmented cuboctahedron P4,13 as RR-polyhedra with conditional edges.

**2. The 369 new atoms (2 in A3/B3, 367 in H3): (c) partly known.**

| group (faces) | atoms | where known | status |
|---|---|---|---|
| A3/B3: A3-10, A3-16 | 2 | P3,33, P3,35 (complete list of 78) | **known** |
| H3, regular faces + 60/120 rhombi only | 13 | complete list of 78 (Timofeenko), so membership is certain; see table A | **known**; 6 fixed by counts, 7 tied between 2–3 entries |
| H3, regular faces + 72/108 rhombi only | 14 | Kaufman, "Convex 108 Degree Rhombi Regular Polyhedra" (86 solids, not claimed complete); see table B | **matched by face counts**; 6 unique, 8 tied; corners not compared |
| H3-16 (5 triangles, 5 rhombi 36/144, 1 pentagon) | 1 | Subbotin 2022: the 5-rhombic pyramid (building block of the composite RR-polyhedra) | **known** (angle checked exactly, below) |
| all other H3 atoms (mixed rhombus angles, 72/144, 108/144 hexagons, 108/144 octagons) | **339** | none | **(b) not found in the sources checked** |

So the "new atoms" count to print is **339 (H3 only)**, new "as far as the sources checked show". A3 and B3 have no new
atom. The 30 others are known solids that are *also* atoms of these cones, and that role is still new.

Sums of atoms (not asked, noted for the same tables): H3-4267 = P2,48 gyrate augmented truncated dodecahedron (list of 78,
unique). H3-3791, H3-3793 match Kaufman's 108 J76/J78/J79 by counts; H3-4051 matches 108 U27/J73/J74/J75 by counts.
The other 50 sums were not found.

H3-16 angle: Subbotin 2022 eq. (3) gives the acute rhombus angle of an n-rhombic pyramid with triangles in the free angles (β = 60°)
as sin(α/2) = sin(β/2) / (2 sin(π(n−2)/2n)). For n = 5: sin(α/2) = 1/(4 cos 36°) = (√5 − 1)/4 = sin 18°, so α = 36°
exactly. That matches H3-16's 36/144 rhombi, its 11 corners (apex, 5 rhombus tips, 5 base) and its faces. Other n give
41.4° (4), 33.6° (6), 31.4° (8), 30.5° (10), so they lie outside these cones. n = 3 gives 60°, the augmented octahedron (A3-10).

H3-81 = Kaufman's "108 Sheered Icosahedron" (C3v; 10 triangles, 3 rhombi; F 13, E 21, V 10). It is also Subbotin's
13-faced RR-polyhedron (Chebyshevskii Sb. 22:4, 2021, Thm 1, part 2): remove 10 faces of the icosahedron, then close the boundary
with a 3-star of rhombi. The boundary angles of the remaining 10-face icosahedron patch are 108° (two unit edges to
non-adjacent corners of a vertex pentagon), so the rhombi are 72/108, as in H3-81. The paper prints the obtuse angle as 2π/3.
That disagrees with the icosahedral geometry, and we did not settle it. A corner comparison is a lead.

### Table A: H3 atoms with regular faces + 60/120 rhombi vs the list of 78 (counts V, E, F, F3, F4, F5, F6, F10, F3+3)
| atom | faces | entry |
|---|---|---|
| H3-374 | 7 tri, 3 sq, 3 pent, 1 hex, 3 rh | Q6 Pryakhin solid (unique) |
| H3-400 | 7 tri, 5 pent, 1 dec, 4 rh | P2,30 meta-augmented pentagonal rotunda (unique) |
| H3-401 | 5 tri, 5 pent, 1 dec, 5 rh | P2,31 para-augmented pentagonal rotunda (unique) |
| H3-605 | 12 tri, 3 sq, 2 pent, 1 hex, 3 rh | P2,33 augmented triangular hebesphenorotunda (unique) |
| H3-652 | 4 tri, 4 pent, 1 dec, 8 rh | P3,37 metabiaugmented pentagonal cupola [sic on the page] (unique) |
| H3-1044 | 5 tri, 9 pent, 15 rh | P5,4 triaugmented icosidodecahedron (unique) |
| H3-197 | 9 tri, 2 sq, 3 pent, 2 rh | Q3 Ivanov solid or P2,29 augmented bilunabirotunda |
| H3-404 | 15 tri, 11 pent, 5 rh | P3,40 augmented icosidodecahedron or P3,44 para-augmented pentagonal orthobirotunda |
| H3-653 | 12 tri, 5 sq, 6 pent, 4 rh | P3,38 or P3,39 meta-augmented pentagonal gyro-/orthocupolarotunda |
| H3-654 | 10 tri, 5 sq, 6 pent, 5 rh | P3,42 or P3,43 para-augmented pentagonal gyro-/orthocupolarotunda |
| H3-656, H3-657 | 10 tri, 10 pent, 10 rh | two of P4,16, P4,18, P4,22 (bi-augmented icosidodecahedra / orthobirotunda) |
| H3-1042 | 9 tri, 5 sq, 5 pent, 8 rh | P4,14 or P4,15 metabiaugmented pentagonal gyro-/orthocupolarotunda |

### Table B: H3 atoms with regular faces + 72/108 rhombi vs Kaufman's 108° list (counts R, F3–F10, F, E, V)
| atom | entry |
|---|---|
| H3-48 | 108 Sheered Pentagonal Anti-Prism (Cs) (unique) |
| H3-81 | 108 Sheered Icosahedron (C3v) (unique); = Subbotin 2021 13-faced RR-polyhedron |
| H3-114 | 108 Misc1 (Cs) (unique) |
| H3-171 | 108 J92b (Cs) (unique) |
| H3-187 | 108 Dodecahedron Half (C5v) (unique) |
| H3-375 | 108 J6 (Cs) (unique) |
| H3-107 | 108 Dodecahedron Full, 108 J30 or 108 J31 |
| H3-376 | 108 U24 1 or 108 J34 1 |
| H3-544, 545, 546 | three of 108 U24 2,1–2,3 / 108 J34 2,1–2,3 |
| H3-617 | 108 J32 or 108 J33 |
| H3-638, 639 | 108 U24 3,1 / 3,2 |

LEADS: (1) compare corners for the tied rows of Tables A and B, and for H3-81 against Subbotin's 13-faced solid (settles the
2π/3 misprint question). (2) Read Subbotin's figure lists for the 54 composite and the non-composite second-type RR-polyhedra (figures only,
no tables) to confirm that none of the 339 is RR. By definition it cannot be: their rhombi are not all equal, or they have non-regular, non-rhombus faces.

## Sources checked (13 Nov 2026)
Subbotin's RR-polyhedra (full texts read):
- V. I. Subbotin, "On the completeness of the list of convex RR-polyhedra", Chebyshevskii Sb. 21:1 (2020) 297–309, doi 10.22405/2226-8383-2020-21-1-297-309.
- V. I. Subbotin, "On the existence of RR-polyhedra associated with the icosahedron", Chebyshevskii Sb. 22:4 (2021) 253–264, doi 10.22405/2226-8383-2021-22-4-253-264.
- V. I. Subbotin, "On composite RR-polyhedra of the second type", Vladikavkaz Math. J. 24:1 (2022) 100–108, doi 10.46698/w8842-6654-4046-v.
- V. I. Subbotin, "On the enumeration of convex RR-polyhedra", Chebyshevskii Sb. 24:5 (2023) 194–207, doi 10.22405/2226-8383-2023-24-5-194-207.
- V. I. Subbotin, "On free angles of RR-polyhedra", Chebyshevskii Sb. 27:1 (2026) 97–110, doi 10.22405/2226-8383-2026-27-1-97-110.
- V. I. Subbotin, "On non-composite RR-polyhedra with conditional edges", DGMF 57(1) (2026) 81–92, doi 10.5922/0321-4796-2026-57-1-7.
- Abstract only: Subbotin, Itogi Nauki i Tekhniki 181 (2020) (mathnet into663); Subbotin, Siberian Math. J. 64:2 (2023) 500–506, doi 10.1134/S0037446623020209 (cited in the 2026 paper, not read).

Regular faces with composite (parquet) faces:
- R. R. Tupelo-Schneck, "Convex regular-faced polyhedra with conditional edges", tupelo-schneck.org/polyhedra (table of 78), and its background page (references).
- A. V. Timofeenko, "Convex polyhedra with parquet faces", Doklady Math. 80:2 (2009) 720–723, doi 10.1134/S1064562409050238; "Junction of noncomposite polygons", St. Petersburg Math. J. 21:3 (2010) 483–512, doi 10.1090/S1061-0022-10-01105-2; corrections, St. Petersburg Math. J. 23:4 (2012) 779–780; "About convex polyhedrons with equiangular and parquet faces", Chebyshevskii Sb. 12:2 (2011) (abstract). Cited through Tupelo-Schneck; not read in full.
- A. M. Gurin, V. A. Zalgaller, "On the history of the study of convex polyhedra with regular faces and faces composed of regular ones", Proc. St. Petersburg Math. Soc. XIV, AMS Transl. (2) 228 (2009) 169–229 (via Tupelo-Schneck; not read in full).
- B. A. Ivanov, Ukr. Geom. Sb. 10 (1971); Yu. A. Pryakhin, Ukr. Geom. Sb. 14 (1973) and J. Math. Sci. 10 (1978) 486–487 (via Tupelo-Schneck).
- R. Kaufman (with A. Doskey, S. Waterman), "Convex Diamond-Regular Polyhedra" (interocitors.com/polyhedra/120s, 71 solids, 2006) and "Convex 108 Degree Rhombi Regular Polyhedra" (interocitors.com/polyhedra/108s, 86 solids, 2006–2024).
- B. M. Stewart, *Adventures Among the Toroids* (1970; 2nd ed. 1980): credited by Kaufman for A3-16; copy listed in DICTO's library, page not checked.

Johnson solids, near misses, catalogues:
- N. W. Johnson, "Convex polyhedra with regular faces", Canad. J. Math. 18 (1966) 169–200; V. A. Zalgaller, *Convex Polyhedra with Regular Faces* (1969) (both in DICTO's library; used through the lists above).
- Wikipedia: "Diminished rhombic dodecahedron" (augmented cuboctahedron section), "Near-miss Johnson solid"; Polytope Wiki "Near-miss Johnson solid" (search result).
- MathWorld "Johnson Solid" (nothing on coplanar or rhombic faces); OEIS search "permutohedron equilateral" (no results).
- G. W. Hart, Virtual Polyhedra and zonohedrification pages (equilateral zonohedra: "any zonohedron can be made equilateral"); D. McCooey, Visual Polyhedra (no rhombus/regular list found by search).
- Steven Dutch's polyhedron enumeration pages; Tom Ruen's polytile polyhedra page (bendwavy.org/polytile/polyhedra returned 404; a search snippet says there has been no serious attempt to enumerate convex equilateral polytile polyhedra).

Zonohedra:
- B. Grünbaum, "The Bilinski dodecahedron, and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra" (2010; library copy), with Fedorov's four monohedral zonohedra; E. S. Fedorov 1885, ch. 13 (library); H. S. M. Coxeter, "The classification of zonohedra by means of projective diagrams" (1962; citation only). Wikipedia "Zonohedron". None concerns non-zonohedral atoms. The 675 zonohedra of H3 were not in question.

Generalized permutohedra and deformation cones (no equal-edge classification found):
- A. Postnikov, arXiv math/0507163; Ardila–Castillo–Eur–Postnikov, arXiv 1904.11029; Castillo–Liu, arXiv 1710.01899;
  Padrol–Poullot, arXiv 2512.05307 (edge-length deformation cone); Poullot, arXiv 2404.02669 (graphical zonotopes);
  arXiv 1804.05460 (kinematic space); FPSAC 2025 abstract 155; Poullot, "Deformed permutahedra: a visit" (slides).
- Web searches: "generalized permutohedra equal edge lengths equilateral deformation cone"; "unit-edge / equilateral convex polyhedra
  enumeration icosahedral rhombi pentagons triangles"; "Grünbaum equilateral zonohedra"; "cuboctahedron augmented square pyramid
  coplanar faces rhombi 13 vertices"; "Subbotin RR-polyhedra"; "Timofeenko parquet faces"; "McCooey near-miss Johnson rhombi";
  a Russian query on RR-polyhedra and the icosahedron. Earlier (12 Nov) searches are listed in the README.

DICTO's private reference library: manifests `papers`, `cited`, `bridges`, `history`, `expansion`, `gaps` searched for Subbotin,
Timofeenko, Pryakhin, Zalgaller, Johnson, cupola, augment, rhomb, equilateral, equal edge, permutohedron, Postnikov, Castillo,
McCooey, Hart, regular-faced, near-miss, zonohedra, Coxeter. Relevant holdings: Zalgaller 1969, Stewart 1980, Johnson,
Baumann's near misses, Wikipedia "Near-miss Johnson solid", orchidpalms.com "Convex Polyhedra containing Golden Rhombi", Hart's
Virtual Polyhedra, McCooey's Visual Polyhedra, Makai 2019 (approximately equal edges), Göring–Winter 2020 (edge-transitive).
No Subbotin, Timofeenko, Postnikov or Castillo–Liu copies. The six earlier ask-library queries are in `data/raw/ask-library.txt`.
