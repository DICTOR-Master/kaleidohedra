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

## Step 2 — the slab face tiled, and two layers side-on (`step2_slab_face.py` → `data/step2-slab.json`; `draw_step2.py` → `renders/step2-slab.html`) — picture first, for DICTO
- Exact: the face edges lie along two five-fold axes, length 3φ·e (e = λ/φ rhombohedron edge, 0.09978), and 3φ = 3 + 3/φ.
- One natural tiling: each edge cut into three e then three e/φ → **9 golden rhombi e×e, 9 golden rhombi e/φ×e/φ, 18 golden parallelograms e×e/φ** (36 tiles; area checked exactly). Pushed along a third five-fold axis they become rhombohedra and golden bricks (parallelepipeds with edges e, e/φ along five-fold axes).
- Exact: **four third-edge choices give a layer exactly half the slab** (0.052460): two of length e (on the e×e tiles: λ/φ rhombohedra), two of length e/φ (on the e×e tiles: bricks e, e, e/φ; on the e/φ tiles: λ/φ² rhombohedra).
- Exact: within each length the two choices have opposite sideways shifts, so **two layers leaning opposite ways end exactly on the neighbour's face** (closing pairs: axes 4/5 with length e, axes 1/3 with length e/φ).
- Spill: each layer is an oblique prism; at mid-height the stack sticks out past the slab's side by the shift (**0.0849 for length e, 0.0324 for length e/φ**) into the wedge, leaving an equal hollow on the opposite side. Smaller spill with the e/φ choice.
- Page: claude.ai/artifact/61qCpWTyzEuR9YfvfDgep1. Open: do neighbouring spills and hollows meet up with the wedges?

## Step 3 — envelope keys and the five-fold corners (`step3_keys_and_fivefold.py` → `data/step3-keys.json`, exact)
- DICTO 10-18: "go on with step 3, cant see the minimal solution without penrose".
- **Keys:** each envelope (RT, volume (−320 + 160√5)/27) overlaps its 8 first neighbours in a convex 8-cornered piece (a golden rhombohedron) of volume (−704 + 320√5)/729; no point lies in three envelopes. Rule: an OCD keeps the overlaps towards the 4 first neighbours of tetrahedral class + and gives away the other 4 — consistent (each overlap claimed exactly once). **Keyed envelope = RT − 4 overlaps = (−5824 + 3040√5)/729 = 1.335592**, one per cell; the keyed envelopes fill **839/8 − 93√5/2 = 89.784%** of space without overlap.
- **So G′ = 93√5/2 − 831/8 = 10.216% of space exactly** (the earlier grid estimate 10.34% was float).
- **Five-fold corners:** all 12 five-fold corners of each envelope are free (in G′, not buried in a neighbour). Each faces the antiparallel five-fold corner of a **third neighbour** (12 of them, squared distance 64/27 + 64√5/81): gap 0.6231 (squared (88/27 − 104√5/81)), 0.4122 along the axis, 0.4673 sideways — further apart than in the octet (0.363). These are the places for Penrose links in the bcc packing.

## Step 4 — the facing envelope stars, Penrose check (`step4_rt_stars.py` → `data/step4-stars.json`; `draw_step4.py` → `renders/step4-stars.html`, claude.ai/artifact/NDp4CAELa7btS3kLTH5LvT)
- Down the five-fold axis: star = 5 golden rhombi of the RT round a five-fold corner (spoke radius 0.4332, tip radius 0.7010).
- Exact: the facing corner's sideways offset runs **along one of corner 1's spokes** (opposite a tip); its length is **exactly 2/3 of the tip radius** (= 2φ/3 × the spoke).
- Exact search: the offset is **not** a φ-scaled spoke/tip vector, singly or in pairs (powers φ^−4…φ^4) → **no thick Penrose rhombus joins the corners directly**, unlike the octet. The 2/3 (the lattice's thirds) breaks it. The gap is also longer (0.6231 vs 0.363).
- Reading for DICTO: in the bcc packing a Penrose link would have to be a longer bridge through G′, or come from a different site (e.g. the OCD's own five-fold corners, or Penrose pieces between envelope stars and slab covers).
