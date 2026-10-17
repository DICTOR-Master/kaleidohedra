# A golden kit for the OCD bcc packing — DICTO 2026-10-18

DICTO · dictospheres.com

**Ask (DICTO, 10-18):** "Does any of this help point us to a realisable golden solution" → plan agreed "yes, start after Fable's verdict" (Fable proved the OCD octet kits exact, ba28bd0).
Plan (Claude): OCDs joined hexagon to hexagon on the bcc lattice, each in its golden envelope (RT). Fill the golden gap G′ (space minus the RTs) in this order: (1) cover the slabs between second neighbours with golden layers; (2) give each envelope overlap to one side as a key (the octet's key trick); (3) Penrose cores at facing five-fold corners; (4) only then a puzzler with the RX sizes on the wedges. Known limit: G′ cannot be tiled face to face by golden rhombohedra alone, so other golden pieces (envelope corners, Penrose prisms, golden bricks) are allowed.
Every step saved here. Exact arithmetic `scripts/q5.py`, `scripts/exactpoly.py` (from the OCD octet study).

## Step 1 — the frame and the slabs, exact (`step1_frame_and_slab.py` → `data/step1-frame.json`)
- Neighbours: 8 first (hexagon joints), 6 second (slabs), 12 third (squared distances 8/9 + 8√5/27, 32/27 + 32√5/81, 64/27 + 64√5/81).
- **The slab is a right prism:** the neighbour's facing RT face is directly opposite (no sideways offset), gap 0.104919 (exact (32/9 − 128√5/81)/|n|).
- **RT face edge = 3φ × the λ/φ rhombohedron edge** (and 3φ² × the λ/φ² edge) exactly. So one layer cannot be rhombohedra of one size: the face edge 3φe = 3e + 3e/φ needs mixed lengths, i.e. golden parallelepipeds (bricks with edges e and e/φ along five-fold axes) as well as rhombohedra.
- And since rhombohedra are oblique, a layer stacked in a right prism must spill past the prism's sides into the wedges.
