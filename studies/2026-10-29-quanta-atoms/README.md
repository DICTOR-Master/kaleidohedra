# All the atoms (Quanta of Space chapter)

DICTO 2026-10-29: Quanta of Space is the overview book, with "all the atoms" as a chapter.

**Conclusion:** stage 1 done: the catalogue chapter "All the atoms" (Chapter 1, after the single-solid entries): 101 new shapes D1–D101 and 54 known/rediscovered ones from DICTO Solids v5 index.csv; 62 drawn from exact geometry (render_atoms.py, one pose, gold new / silver known), the rest in a table. Status: in the Quanta draft (DRAFT-quanta.pdf, 156 pp); stages 2–4 (Stacking chapter, manifesto, front/back matter) to come.

- scripts/render_atoms.py (dicto-big-brother): icons from solids/*.json (polygon faces, Newell normals).
- scripts/atoms.py: index.csv → papers/book-quanta-of-space/atoms-catalogue.html, inserted between <!--ATOMS START--> and <!--ATOMS END--> in paper.html.
- Quanta v1.5 draft (2026-11-03): index.csv brought to DICTO Solids v7 (Kagemusha, D106–D109) plus the 16 golden cut solids of #88 and #89 (14 new ones with D— until DICTO confirms the numbers; the two Golden Cut Icosidodecahedra rediscovered, Zefiro 2011). scripts/new_atoms.py (dicto-big-brother, with gcb.py and data/s2b-rhombic.json of studies/2026-11-03-golden-cuts-beyond-plato) writes their models, drawn by render_atoms.py as icons/piece-*.png; atoms.py lists D— rows with the atoms.
- Split (2026-11-03, DICTO: "yes split it with that title"): the catalogue is now Volume II, Quanta of Space II: The DICTOnary of Atoms (papers/book-quanta-dictonary; icons moved to its figures/atoms). atoms.py takes Volume I's paper.html as 4th argument and names under each entry the chapter of Volume I that tells it; picture borrowing stays off (BORROW=1 to turn it on). The 14 golden cut solids are D110–D123 (DICTO 11-03): #88's eight in D·I·C·T·O order, then #89's rhombic dodecahedra, rhombic triacontahedra and snub dodecahedra. Run through papers/book-quanta-dictonary/split_volumes.py.
