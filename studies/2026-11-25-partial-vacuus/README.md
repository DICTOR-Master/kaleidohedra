# Partial Vacuus: a Vacuus that stops short of the centre (25 November 2026)

DICTO · study, V SF A project. The idea is **DICTO's** (25 Nov): "the excavated dodecahedron is kind of a vacuus"; "it reminded me of
my B1NR build as depth doesn't go all the way to center"; "it may be just a practical solid as a true vacuus or resonus barely exists";
"it's a chain stage 3" (his Lotus seed and Dodecahedral Chain, stage 3 = the excavated dodecahedron, Polyhedraverse TRANS_LOTUS_3).

> **Status box.** Study note, not published. Part 1 exact (sympy over Q(√5), faces found numerically, every wall checked).
> Part 2 (thickness rule for real builds) and the Archimedean/Catalan extension still to run.

**Definition.** A partial Vacuus of a solid P: every face dug in as a pyramid pit with its apex on the face's axis at a fraction s of the
face's distance from the centre (s = 0: the Vacuus pyramids meet at the centre; s = 1: the solid). A depth is **special** when every wall
of every pit lies in a face plane of one other solid Q (then the pits end exactly on Q, the core).

## Part 1 (scripts/special_depths.py, logs/special_depths.log, FINAL ok)
Among the five Platonic solids (P and Q both Platonic, same centre) there are exactly two special depths:

| P | pits end on Q | apex at s = | solid |
|---|---|---|---|
| dodecahedron | icosahedron | 5 − 2√5 ≈ 0.528 | the excavated dodecahedron (DICTO's Lotus seed / Dodecahedral Chain, stage 3); all 60 faces equilateral, each pit half a J13 |
| icosahedron | dodecahedron | 3√5 − 6 ≈ 0.708 | the great dodecahedron (Kepler–Poinsot), read as an icosahedron with its 20 faces dug in as triangular pits |

Rejected (only some walls on Q): cube pits at s = 1/φ on icosahedron planes; dodecahedron pits on tetrahedron and octahedron planes.
The tetrahedron, octahedron and cube have no special depth within the Platonic solids.


## Part 1b: all Platonic, Archimedean and Catalan solids (scripts/special_depths_all.py, special_check.py; data-special-*.json; FINAL ok)
Every solid put in a common frame (three perpendicular half-turn axes on x, y, z), the other solid tried in all 24 frame orientations
(both icosahedron placements, both tetrahedron placements). A depth is kept once per solid (pits ending on the icosidodecahedron's
triangles are the icosahedron's planes again). For every depth below the pits were checked to be interior-disjoint (the excavated
body is a solid). Control: both depths of part 1 found again.

| P (pits on its faces) | apex at s = | walls lie on the faces of (scaled) | closed form |
|---|---|---|---|
| tetrahedron | 0.5147186 | triakis octahedron | 9 − 6√2 |
| octahedron | 0.6000000 | triakis tetrahedron | 3/5 |
| octahedron | 0.3167184 | disdyakis triacontahedron | 3 − 6√5/5 |
| octahedron | 0.4810724 | deltoidal hexecontahedron | (12 − 3√5)/11 |
| dodecahedron | 0.2992542 | triakis icosahedron | (10 − 3√5)/11 |
| dodecahedron | 0.5278641 | icosahedron | 5 − 2√5 (the excavated dodecahedron, DICTO's chain stage 3) |
| dodecahedron | 0.7453560 | deltoidal hexecontahedron | √5/3 |
| icosahedron | 0.4014916 | pentakis dodecahedron | (6√5 − 9)/11 |
| icosahedron | 0.7082039 | dodecahedron | 3√5 − 6 (the great dodecahedron) |
| icosahedron | 0.8977626 | deltoidal hexecontahedron | (30 − 9√5)/11 |
| rhombic triacontahedron | 0.7639320 | **a smaller rhombic triacontahedron** (scale 1/φ) | 3 − √5 |
| triakis icosahedron | 0.9159606 | deltoidal hexecontahedron | (42 − 11√5)/19 |

No Archimedean solid and no other Catalan solid has a special depth against these solids. The rhombic triacontahedron is the one
solid whose pits end on a smaller copy of itself (scale 1/φ, pits reaching 3 − √5 of the way in): a self-similar partial Vacuus.
All twelve depths are roots of quadratics over Q (scripts/exact_forms.py + sympy factor; data-exact-forms.json; logs/exact_forms*.log): each depth refined over every wall at double precision, its integer polynomial found, factored, and the factor with the matching root kept. A symbolic proof from exact coordinates (as part 1) remains LEAD 4.


**Permutahedra and associahedra (DICTO 26 Nov: "any permutahedra or associahedra etc").** The three permutahedra (truncated
octahedron A3, truncated cuboctahedron B3, truncated icosidodecahedron H3) and their duals (tetrakis hexahedron, disdyakis
dodecahedron, disdyakis triacontahedron) are in the run above: none has a special depth of its own; the disdyakis triacontahedron is
the core for the octahedron's pits at s ≈ 0.3167. The twelve associahedra of study 2026-11-24-permutahedron-leads (A3, B3, H3, every
Coxeter element computed there), in their permutahedra's Coxeter frames (checked: three half-turn axes on x, y, z, as the common frame),
tried as pitted solid and as core against all 31 solids and each other (scripts/special_depths_all.py with ASSOC=1,
logs/special_assoc.log): **no special depth**. Their low symmetry (order 2) leaves nothing to carry every wall onto one solid's faces.

4. (LEAD) Exact derivation of every depth in part 1b, as part 1 did for the Platonic pairs.
5. (LEAD) Which of these excavated solids are classical stellations (as the excavated dodecahedron and the great dodecahedron are).

## Next
1. DONE (part 1b above).
2. Thickness rule: plates of thickness t, the smallest open core per solid (DICTO: a true Vacuus barely exists; every build is partial).
3. DICTO's B1NR cube as a measured example (core size from his build, when he gives it).

## Prior art (DICTO 26 Nov: "prior art"; sources checked 26 Nov 2026)
- The **excavated dodecahedron**: Wenninger, *Polyhedron Models* (1971), model 28, "third stellation of icosahedron" (the Ef1g1
  stellation in Coxeter, Du Val, Flather and Petrie, *The Fifty-Nine Icosahedra*, 1938). Who first called it "excavated" was not found.
  Sources: Wikipedia "Excavated dodecahedron" and "List of Wenninger polyhedron models" (checked); the books themselves not opened.
- The **great dodecahedron**: Poinsot (1809); Kepler–Poinsot polyhedron (Wikipedia, checked).
- **Excavating any solid by face pyramids of a chosen height** is a standard operation (augment faces with pyramids of negative height)
  in Robert Webb's *Stella4D*; Robert Austin's blog (robertlovespi.net, tags "excavation"/"excavated") shows excavated tetrahedra,
  octahedra, snub cubes and truncated icosahedra made with it, and notes that taller pits on the octahedron meet at the centre.
  Polytope Wiki has "excavated truncated rhombicuboctahedron". Checked: search pages only, posts not each opened.
- Not found anywhere: the family read **from the Vacuus outward** (the centre built out into a scaled dual core), the special sizes
  as the points where every pit wall lies on a face of a core solid, and the census over all Platonic/Archimedean/Catalan pairs
  (12 depths, including the rhombic triacontahedron on a 1/φ copy of itself). Those are DICTO's reading and this study's results.
- **As a key** (DICTO 26 Nov: "its a kind of key" — a pit takes a spike of the same height, lock and key; given to steer the prior-art
  search): the nearest prior art is **topological interlocking** (Dyskin, Estrin et al., 2001: term coined; Platonic solids and the
  concavo-convex "osteomorphic" blocks interlock), Belov-Kanel et al., arXiv:0812.5089 (interlocking of convex polyhedra), and
  Akpanya, arXiv:2405.01944 (interlocking blocks built from tetrahedra and octahedra in the tetroctahedrille). Abeille's flat vault
  (1699) is the classical ancestor. None found uses face pyramids (pits and matching spikes) as the key on a space-filling piece.
  Checked: search pages and abstracts only.

## Part 3: building out the core of any Vacuus, and solidity (scripts/build_out_general.py; data-build-out-*.json; FINAL ok)
Core = the solid's polar dual scaled by lam (corners lam n_f/d_f on the face axes); t = lam / min d_f² from 0 (Vacuus) to 1 (solid).
Solidity: the thinnest material wedge between two pits along an edge. Yardstick (DICTO: "just the classics for models"): the
excavated dodecahedron, 41.81° (the great dodecahedron: 63.43°).
- Platonic + cuboctahedron (control: both classics found again): cuboctahedron no special size; as solid as the classics from
  t ≈ 0.64 (tetrahedron 0.64, cube 0.56, octahedron 0.54, dodecahedron 0.54, icosahedron 0.58; grid step 0.02).
- McCooey's 162 self-duals (dbb job build-out-mccooey, 0 errors): **no special size** in any; pits disjoint at every size tested in
  all 162; **32 of 162** reach the classics' solidity (median from t ≈ 0.78), the other 130 never do (their thinnest wedge stays
  below 41.8° at every core size).
