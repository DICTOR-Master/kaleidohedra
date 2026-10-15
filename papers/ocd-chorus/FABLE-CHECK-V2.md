DICTO · dictospheres.com

# Fable check, Version 2 additions (overstatement only)

Scope: the four new pieces of paper.html (abstract sentence, §1 "A bridge…", §9 "Why it is a structural bridge", new reference). Evidence: study README steps 22–30, data/chorus-modelset.txt, chorus-canonical.txt, chorus-window-why.txt, chorus-rules.txt, chorus-fork-min.txt; bridge study (master, commit 3fd407f). One web lookup (arXiv 2603.21158).

The results themselves are stated correctly elsewhere in the paper. The problems are all in the framing, which is stronger than the data and the earlier sections support.

## Piece (1): abstract

**P1. "The result is a structural bridge between periodic and aperiodic order: the lattice and the window of the chain are both physical, a plane of the packing and the distance from the axis."**
- "Structural bridge" is not defined anywhere, and it reads as a new kind of result. The established version of the phenomenon is aperiodic order appearing where periodic crystals meet at an irrational orientation (Sutton; Ranganathan et al.; Xiong et al.). The abstract cites that work in the very next sentence.
- The sentence also mixes up two things. "The distance from the axis" is the internal *coordinate*. The *window* is an interval of that coordinate, and its physical value is t_c, not W (chorus-window-why.txt).
- **Replace with:** "Thus aperiodic order appears where periodic packings meet: the lattice of the chain is a plane section of one packing, its internal coordinate is the distance from the axis, and its window is fixed by the ring clash at t<sub>c</sub>."

## Piece (2): §1 paragraph

**P2. "How periodic and aperiodic order can be joined is the question that runs through DICTO's work."**
- This is author biography used as motivation. It is not a scientific reason to read the paper.
- **Replace with:** "How periodic and aperiodic order can coexist in one structure is the question behind the twinning and interface work cited above; it also motivates this series of studies."

**P3. "An earlier check (DICTO's bridge study, 2026) found that the Ogdoecontahedron on its own is not a cluster of the standard icosahedral quasicrystal: as a single solid it carries the two kinds of order only side by side (regular hexagons, icosahedral symmetry)."**
- The summary is mostly accurate, but it drops two things.
  - **Scope.** The study tested only the canonical primitive 6D tiling and three standard cluster shells. It says explicitly that F/I lattices, other windows and decorated tilings were not tested.
  - **The one tie it found.** The Ogdoecontahedron's 30 two-fold corners are exactly the corners of the icosidodecahedron, the classical 30-atom shell of quasicrystal clusters.
- "Carries … order" is also loose. A single solid has features *associated with* each kind of order; it does not carry the order itself.
- **Replace with:** "An earlier check (DICTO's bridge study, 2026) found that the Ogdoecontahedron alone is neither a patch nor a cluster of the canonical icosahedral quasicrystal (canonical primitive tiling and three standard cluster shells tested; its one tie is the classical icosidodecahedral shell formed by its two-fold corners). In a single solid, its regular hexagons and its icosahedral symmetry sit side by side without a structural link."

**P4. "The chorus joins them structurally. Nothing aperiodic is put in: there are five periodic packings of one solid and one rule, that hard copies may not overlap."**
- The aperiodicity comes from an input, not from the rule. The five 72° wedges round a five-fold axis, a non-crystallographic arrangement, are the icosahedral irrational twin. In each voice's plane lattice, the axis has the irrational slope −φ (chorus-modelset.txt).
- The study itself calls this "the standard cut-and-project mechanism" (README step 24). Any lattice cut along an irrational line gives an aperiodic set; hardness only picks the window.
- "One rule" also leaves out three choices:
  - the wedge start angle (59°, "a choice", §2), which was not varied;
  - removal of whole five-fold rings;
  - the removal rule (greedy rule A as built; the minimum is not unique, §4). Steps 29–30 show that the choice of rule decides the spine beyond |h| = 12.81: rule D gives Fibonacci, rules A, B and C give the thinned chain (chorus-rules.txt).
- **Replace with:** "The chorus joins them structurally. No aperiodic structure is put in, only five periodic packings of one solid meeting round an irrational (five-fold) axis, removal in whole five-fold rings, and the rule that hard copies may not overlap."

**P5. "Where the packings meet, that rule alone produces an aperiodic, exactly Fibonacci chain."**
- "Rule alone" is wrong, for the reason in P4: the irrational axis supplies the aperiodicity.
- "Exactly Fibonacci" needs two qualifiers:
  - It holds only for |h| < 12.81. Beyond that, minimal removal gives a thinned chain (chorus-fork-min.txt).
  - The chain is the removed copies *plus the kept central copy*. The removed copies alone have a T = L + S gap (chorus-canonical.txt (a), (c)).
- **Replace with:** "Along the axis the rule forces out every copy of the core plane nearer than t<sub>c</sub>; together with the central copy, these are exactly the Fibonacci chain for |h| &lt; 12.81, and beyond that, at the points checked, a thinned chain of the same cut-and-project kind."

## Piece (3): §9 paragraph

**P6. "In the usual cut-and-project construction the lattice lives in a space of higher dimension and the window in an abstract internal space. Here both are physical."**
- The first sentence is fair for the general formalism (Baake & Grimm) and for 6D icosahedral quasicrystals.
- The contrast is not novel, though. The paper's own cited literature on irrational interfaces is physical in the same sense:
  - Sutton builds the interface quasicrystal from the real lattice of a real bicrystal, with the perpendicular coordinate in real space.
  - The interface framework of arXiv 2603.21158 ("proximal coincidence point set") is also built on the two real crystal lattices.
  - Any 2D crystal cut by an irrational line (the textbook Z² Fibonacci picture read as a crystal) is the same.
- As written, the passage implies this case is unusual.
- **Replace with:** "In the general cut-and-project construction the lattice lives in a space of higher dimension and the window in an abstract internal space. Here, as for irrational interfaces between real crystals (Sutton 1988; Xiong et al. 2026), both are physical."
- **Precision point.** The "plane through the axis" belongs to one voice only on one side. The opposite half-plane lies in another wedge, and the window [0, W) uses one sign of the transverse coordinate. "In one half-plane bounded by the axis" would be exact. Check before changing.

**P7. "The window, the one free choice of the construction, is not chosen either: the copies inside it are forced out by a five-fold ring of copies clashing with itself (§6)."**
- The window is not the only free choice. The lattice and the slope are choices too; here they come from the solid and from the axis, which was chosen.
- "The window" is ambiguous. The ring clash fixes [0, t_c), not the canonical window [0, W): t_c ≠ W (chorus-window-why.txt). The two select the same points only for |h| &lt; 12.81.
- **Replace with:** "The window is not chosen either: hardness fixes it at t<sub>c</sub>, the distance below which a five-fold ring of copies clashes with itself (§6). For |h| &lt; 12.81 it selects the same lattice points as the canonical window W."

**P8. "Periodic order on either side of the junction and aperiodic order along it come from one solid and one rule."**
- There are five wedges, so "either side" does not fit.
- The wedges are not purely periodic either. Removals also fall along the seams at every radius, in a pattern that is strongly ordered but not proven quasiperiodic (steps 22, 23, 26).
- "One rule" has the same problem as P4.
- **Replace with:** "Periodic order inside each of the five wedges and aperiodic order along the axis come from one solid, its five periodic packings and the no-overlap rule (the seams between the wedges also carry ordered removals, §8)."
- Adjust the section reference to wherever the seams are discussed.

**P9. "Beyond |h| = 12.81 the same rule, with minimal removal, gives a thinned chain, so the bridge still holds there, but its window is the narrower ring-clash window rather than the canonical one (§7)."**
- This is checked only at the first four departure points, on finite patches of about 1130–1155 sites, with an integer program and a float clash test (exact only at 12.81).
- That the thinned spine follows [0, t_c) at every height is "not proved" (README step 30, Limits).
- The built chorus used greedy rule A, not minimal removal. The two agree at these four points.
- **Replace with:** "Beyond |h| = 12.81, at the four departure points checked (finite patches, float clash test), minimal removal keeps the core copy, so the spine there is consistent with the cut-and-project chain of the narrower window [0, t<sub>c</sub>): a thinned three-gap chain, still aperiodic, but not the Fibonacci chain (§7)."

## Piece (4): reference

**P10. "DICTO, Is the Ogdoecontahedron a bridge? Study, 16 October 2026: https://github.com/…/tree/master/studies/2026-10-16-ogdoecontahedron-bridge"**
- **Date.** The study was committed 2026-10-15 (3fd407f). A 16 October date on a reference in a paper dated 15 October looks wrong. The "10-16" is only the folder label.
- **Title.** The README's actual title is "Is the DICTO Ogdoecontahedron a real periodic ↔ aperiodic bridge?".
- **Link.** A `tree/master` link can change after the DOI freezes the paper; a commit permalink is safer.
- **Replace with:** "DICTO, Is the DICTO Ogdoecontahedron a real periodic–aperiodic bridge? Study, 15 October 2026: https://github.com/DICTOR-Master/kaleidohedra/tree/3fd407f/studies/2026-10-16-ogdoecontahedron-bridge"
- Check that the in-text "(DICTO's bridge study, 2026)" matches.

## Also consider

The subtitle line (line 12) says V2 "adds the periodic–aperiodic bridge". After the fixes above, "adds a discussion of the chain as a link between periodic and aperiodic order" would be more modest.

## Verdict

**Ready as Version 2 after these fixes.** No result is wrong. The overstatements are all framing: "nothing aperiodic / rule alone" (P4, P5), the window conflation (P1, P7), the beyond-12.81 extrapolation (P9) and the implied novelty of a "physical" cut-and-project (P6). Each is fixed by the replacement sentence given.

Lookup: arXiv 2603.21158, "Framework for Quasiperiodic Interfaces: Proximal Coincidence Point Set and Computation" (https://arxiv.org/pdf/2603.21158). The search did not confirm its author list; check it before citing as Xiong et al.
