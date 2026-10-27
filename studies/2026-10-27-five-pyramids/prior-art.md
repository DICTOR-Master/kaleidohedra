# Prior art: five pyramids, shared networks and new deltahedra (2026-10-27)

Every source actually checked, the query that found it, and what it says.

## Private reference library (`~/bin/ask-library`, run from the Pi, top 6 each)

| Query | Items returned and checked | What they say for this study |
|---|---|---|
| "non-convex deltahedra enumeration" | Richter-Gebert 2026, "An almost trivial observation about the icosahedron"; Johnson 1966, "Convex polyhedra with regular faces"; Wikipedia "Rhombic dodecahedron"; Devadoss–Harvey–Richter 2026, "Unfolding overlaps of the exceptional regular polytopes"; Magazinov 2015 (Delaunay faces of parallelohedra); Messer 1995 (stellations of the RT); pages: Grünbaum 2010 Bilinski dodecahedron pp. 4, 19, 25; Kepler 1619 p. 271; arXiv 1206.3716 (dense packings) p. 21; Al-Siyabi–Koca–Koca 2020 p. 6 | No deltahedron enumeration in the library. Johnson 1966 covers the convex regular-faced solids (the 8 convex deltahedra among them as Platonic solids and J12, J13, J17, J51, J84). |
| "deltahedron equilateral triangle faces polyhedra list" | Wikipedia "Rhombic dodecahedron"; Richter-Gebert 2026; Wikipedia "Goldberg polyhedron"; Hynd 2023 (Reuleaux polyhedra); Sommerville 1922, "Space-filling tetrahedra in Euclidean space"; Johnson 1966; pages: Kepler 1619 pp. 89, 271; Pacioli 1509 pp. 32, 111; Bianchi–Doná–Speziale 2011 p. 6 | Nothing on non-convex deltahedra. |
| "face-to-face gluing of regular tetrahedra octahedra icosahedra polyhedra" | Richter-Gebert 2026; Kabai 2010 (30 cubes on an RT); Montejano et al. 2019 (Reuleaux graphs); Wikipedia "Goldberg polyhedron"; Johnson 1966; O'Rourke 2010; pages: Akpanya–Goertzen–Niemeyer 2024, "Topologically interlocking blocks inside the tetroctahedrille" pp. 1, 4; Bianchi et al. 2011 p. 6; Al-Siyabi et al. 2020 p. 6 | Akpanya et al. use face-glued tetrahedra and octahedra inside the octet (tetroctahedrille) as building blocks; they do not list deltahedra. |
| "central pyramids of Platonic solids space filling" | Torquato–Jiao 2009 (two items, dense packings of Platonic and Archimedean solids); Sommerville 1922; Kramer 1982, "Non-periodic central space filling with icosahedral symmetry using copies of seven elementary cells"; Kubala 2019; Datta–Maity 2018; pages: Lagarias–Zong 2012 p. 1; Koskinen 2011 p. 2; Gabbrielli–Jiao–Torquato 2012 p. 1; Wikipedia "Tetrahedral-octahedral honeycomb" p. 1 | Lagarias–Zong: Aristotle's claim and the history (already used in #44). The octet honeycomb is classical. Nothing beyond #44 on face pyramids sharing tilings. |
| "Mosseri Sadoc golden tetrahedra tiles" | Koca–Koc–Koca–Al-Siyabi 2020, "Dodecahedral structures with Mosseri-Sadoc tiles"; Al Raisi–Koca–Koca–Koc 2026, "Modified Mosseri-Sadoc tiles from D6"; Papadopolos–Ogievetsky 1999 (inflation rules; Dehn invariants, two copies); Chentouf–Sun 2023, "Tetrahedra tiling problem"; Winkler 2021; Goodman-Strauss 2026 | The six golden tetrahedra (edges 1 and τ) and their tilings; the edge tables used here for AXE (t6), CLEO (t4), Tricap (t3), Hound Tooth (t2) come from Koca et al. 2020, Table 1 (library file shapes/mosseri-sadoc-tiles.json). Nothing on deltahedra built from them. |

## Web

- Query "non-convex deltahedra enumeration Cundy Trigg Freudenthal van der Waerden" (web search). Results checked:
  - https://en.wikipedia.org/wiki/Deltahedron (fetched): only 8 convex deltahedra (Freudenthal and van der Waerden 1947);
    infinitely many non-convex ones (Trigg 1978; Eppstein 2021); Cundy 1952 listed 17 with two vertex types, Olshevsky
    added 11; the stella octangula, the excavated dodecahedron and the Boerdijk–Coxeter helix are examples. Joining two
    deltahedra face to face gives another, which is why the class is infinite.
  - https://www.cgg.cs.tsukuba.ac.jp/projects/2014/deltahedral_graph/ICGG2014-tsuruta.pdf (fetched, pp. 1–4 read):
    Tsuruta, Mitani, Kanamori, Fukui, "Enumeration of deltahedral graphs with up to 10 vertices" (ICGG 2014). They
    realize every polyhedral triangulation with at most 10 vertices that can be a deltahedron (no self-intersection, no
    180° dihedral), and show that one graph can have a convex and several non-convex forms (their graph 9_50, Figure 3):
    the idea of class (b) "variants" in this study has this prior art. All solids of class (c) found here with at most 10
    corners (one with 6, three with 7 corners) are in the range of their enumeration.
  - Also listed by the search, not opened: mathworld.wolfram.com/Deltahedron.html, georgehart.com/virtual-polyhedra/ex-cd2.html,
    archive.lib.msu.edu/crcmath (CRC entry "Deltahedron").

## DICTO's own papers (cited, for question 1)

- #44 Aristotle's Pyramid (DICTO DOI 10.5281/zenodo.23529497): of the five face pyramids only {C}, {T, O}, {C, T, O} fill
  space (any positions, not necessarily face to face); Cleo-Icos + Antonius fill space two to one (#20).
- #47 Every Mix of the Platonic Solids Fills Space (DICTO DOI 10.5281/zenodo.23551326): all five Platonic solids fill
  space together with connectors (P, Q, Q′, Admiral Caps, Dogstar, X/Y); icosahedron + 6 Admiral Caps = octahedron.
- #20 (DICTO DOI 10.5281/zenodo.23357896): Cleo-Icos and Antonius from the golden rhombohedron; Penta-cleo.
- #19 (DICTO DOI 10.5281/zenodo.23351291): AXE = M-S t6, CLEO = M-S t4 (scaled by 1/τ).
- F21 (study 2026-10-10-icosa-networks-3): the icosahedral octet; Weirdstone (corner cap) and Tadpole (edge cap).
- #48 / #54 (Icosaxes papers): Tricap = dodecahedron corner = M-S t3; Lotus Jewel Axes = Icosaxes − 8 Tricaps.

## Status of the results

The face-to-face statements of question 1 extend #44 (which allowed any contact); they are proved here from the exact
face shapes. The deltahedra found are all face-gluings of regular tetrahedra, octahedra and icosahedra (a classical
construction, see above) or re-cut regular solids; none uses DICTO's pieces in a new way, so nothing is claimed new.
