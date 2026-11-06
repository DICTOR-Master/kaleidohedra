# C + T + O with no connector (#47 open question 1), 6 Nov 2026
DICTO: "go ahead with #47" (after "what gaps in concordance might new tools help with").

**Conclusion:** YES. Cubes, tetrahedra and octahedra of edge 1 fill space together with no connector: the octet cut along its
close-packed planes is a stack of flat slabs (each octahedron and tetrahedron spans one plane gap), cube layers are flat slabs, and tiles
need not meet face to face. NEVER face to face (only the cube has square faces, so a cube's face-neighbours are cubes). The slab stack is
not periodic in three directions (square vs triangular periods share no second vector); whether any C + T + O tiling is 3-periodic stays open.
Status: written into #47 as version 3 (draft DRAFT-47-v3-Platonic-Mixes.pdf, for DICTO's read).

- scripts/cto_stack.py: three octet layers between cube slabs; 864 T, 409 O, 576 C, every edge measured; 200 000 random points each in
  exactly one tile. FINAL OK (46 s, Pi).
- Prior art: Gabbrielli, Jiao, Torquato 2012 (library copy, read again): pairs only; cubes with T and O not treated. Not found within the
  sources checked; a short consequence of the classical octet layering.
