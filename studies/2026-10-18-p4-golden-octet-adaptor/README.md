# Project 4 — Golden octet adaptor (DICTO 2026-10-18)

DICTO · dictospheres.com

**DICTO 10-18:** "wondering about fusing all as one piece, and as adaptor to any golden envelope solid — golden octet"; "and two shape set as solid too"; "as well as any golden envelope adaptor".
Source: studies/2026-10-18-p3-golden-envelope-octet (golden envelopes in the octet, exact 10/φ⁶).

## Step 1 — exact (`scripts/p4_adaptor.py` → `data/p4-adaptor.json`)
- Give every point to its nearest envelope centre: the fcc Voronoi cell, the **rhombic dodecahedron** |x|+|y|, |y|+|z|, |z|+|x| ≤ R (R = 2φ/3), volume = the cell (32 + 16√5)/27.
- **The golden envelope lies inside its rhombic dodecahedron (exact) and touches each of its 12 faces at one corner** — the 12 golden-section corners on the octahedron edges ((2/3, (√5 − 1)/3, 0) and its turns).
- **Adaptor = rhombic dodecahedron − envelope: 352/27 − 16√5/3 = 1.111341** (44.27% of space).
## Step 2 — the adaptor as a piece (`scripts/p4_mesh.py` on dicto-node → `data/p4-mesh.json`)
- One solid, centrosymmetric (no left/right), but a **closed shell (cavity)**: the envelope is sealed inside. To assemble, it **opens in two identical halves along z = 0** (each 0.555671, one solid, sphericity 0.37; the half-turn about the x axis maps one onto the other). (Each half has the same volume as a grown core piece of set 3.)
- Sets: **one-piece golden octet** = rhombic dodecahedron with the envelope fused: one shape, fills space alone (fcc). **Two-shape golden octet** = solid envelope + adaptor half (×2): 2 shapes, no mirror images. **Adaptor for any golden-envelope solid**: the cavity takes any solid whose golden envelope it is (the OCD, the envelope itself, …).
## Step 3 — 3D page (`scripts/p4_page.py` → `renders/p4-golden-octet-adaptor.html`, claude.ai/artifact/3Qw1XztMnTGiUuN1ntq1L9)
- Views: two shapes (envelope + two halves), adaptor round any golden-envelope solid (OCD shown), one piece network, see-through network, and set 3's two-shape set with a solid envelope (DICTO: "two shape set as solid too").
## Notes
- The rhombic dodecahedron is the classical fcc space-filler; the new content is the exact golden envelope inside it touching all 12 faces at golden-section points, and the adaptor shell. Prior-art check: as in the envelope-network note.
- Next: Fable check; STL (halves at 60 mm octahedron edge); names.

## Step 4 — hollow spherical chamber (outside the plan; DICTO 10-18: "1, hollow chamber also half RD networks open with golden envelope exposed on outside") (`scripts/p4_chamber.py` → `data/p4-chamber.json`)
- Cells of the golden octet with centres between radius 2.4 and 5.4 (octahedron "radius" R = 2φ/3 = 1.0787 as unit frame): 230 cells.
- Inside the wall: 68 full rhombic dodecahedra (envelope fused). **Outermost layer (162 cells with a neighbour beyond the outer radius): golden envelope + only the inward adaptor half**, so the envelopes are exposed on the outside. The adaptor halves split on a mirror plane (x = 0, y = 0 or z = 0); each outer cell uses the plane facing most outward (the three are turns of one another under the envelope frame's symmetry, so it is still one half-shape).
- 3D page (same link): "Chamber" and "Chamber, cut open". Geometry only — nothing structural is claimed.
- DICTO 10-18: "make the inner surface half-open too". Inner-surface cells (a neighbour inside the inner radius) now carry the envelope + only the OUTWARD adaptor half, so envelopes line the hollow centre too. Same chamber (radii 2.4–5.4): 162 outer cells, 60 inner-surface cells, 8 full rhombic dodecahedra between, 0 cells that are both (if a wall were one cell thick, those cells would be bare envelopes).

## The general idea (DICTO 10-18): a "half-RD network" of any golden-adaptable solid
- DICTO: "this could be a half RD pyrochlore network of any golden adaptable solid … I meant figuratively, with RD equivalent". Recorded as the general system: **RD-equivalent cells (golden envelope + adaptor), each cell full or half-open (adaptor half kept on one side), arranged in any network on the fcc lattice; any solid whose golden envelope this is can sit in each socket.** The chamber (step 4) is one instance.
- Two RD-equivalents are now known: the **envelope-centred** rhombic dodecahedron (adaptor shell round one envelope, opens in two halves; this project) and Fable's **vertex-centred** rhombic dodecahedron minus its 6 envelope bites (W, one solid glue piece, achiral; octet fable-review-2).

## Step 5 — envelope + W in 3D (`scripts/p4_W.py` on dicto-node → `data/p4-W.json`)
- W = rhombic dodecahedron round the octet vertex (0, 0, R) minus the envelopes biting into it: volume 1.111341 (= the exact (352 − 144√5)/27), one solid, sphericity 0.574 (Fable's numbers confirmed).
- 3D page (same link): "Envelope + W" (one envelope with the 6 W at its octahedron corners), "the set", and "network" (envelopes on the octahedron sites, W on the octet vertices).

## Step 6 — W with exact OCD imprints (DICTO 10-18: "like this last Fable W particularly, and face could be exact imprint of OCD?!"; `scripts/p4_W_ocd.py` on dicto-node → `data/p4-W-ocd.json`)
- **W_OCD = rhombic dodecahedron round each octet vertex minus the 6 OCDs biting into it** (OCD-shaped sockets instead of envelope-shaped).
- Space filling by construction: the vertex rhombic dodecahedra tile space (fcc), so every point outside the OCDs lies in exactly one W_OCD; **kit OCD + W_OCD fills space exactly**.
- Exact volume = cell − OCD = **(2824 − 328√5)/1539 = 1.358395**; one solid (genus 0); **centrosymmetric — no mirror pair**; **sphericity 0.648** (chunkier than the envelope W, 0.574); the OCD stays whole (0.979).
- **So: OCD + W_OCD — two shapes, no mirror images, both chunky; the 6 sockets of each W are exact OCD imprints.** (Fable check to do.)
- 3D page (same link): "OCD + W with OCD imprints", "the set", "network".

## Step 7 — W centred on the Penrose star (DICTO 10-18: "could the imprint be centred on the Penrose star also?!"; `scripts/p4_W_star.py` on dicto-node → `data/p4-W-star.json`)
- Sites: the midpoints m of the octahedron edges, where two OCDs' five-fold stars face each other and the thick Penrose rhombus joins them ((R/2)(a,b,c), exactly two of a,b,c odd; 6 per cell).
- **Their Voronoi cell is an octahedron with corners at the two OCD centres, the two edge ends and the two tetrahedron centres** (e.g. 0, (0,R,R), (0,R,0), (0,0,R), (±R/2, R/2, R/2)), volume = the octet tetrahedron's (16 + 8√5)/81 = cell/6.
- **Star-centred W = that octahedron minus its 2 OCDs** (imprints at two opposite corners): (cell − OCD)/6 = (1412 − 164√5)/4617 = **0.226399**; one solid (genus 0); centrosymmetric about m (no mirror pair); **sphericity 0.690** (the chunkiest glue so far); holds 97.7% of the middle piece between the facing stars (so nearly all the Penrose link region).
- **Kit OCD + star-centred W: two shapes, no mirror images, fills space exactly** (Voronoi cells of the edge midpoints tile space; the OCDs lie inside their union). 12 W round each OCD, 6 per cell.
- 3D page (same link): "OCD + W centred on the Penrose star" and "the set".

## Step 8 — keyed Penrose pattern, one piece type (DICTO 10-18: "could the outer part include a keyed Penrose pattern also?" → "as many as possible" → "while maintaining singularity as the piece adaptor")
- Exact pairing check (`scripts/p4_key_pairing.py` → `data/p4-key-pairing.json`): the star-centred W's 8 triangular faces (corners: an OCD centre, an edge end, a tetrahedron centre) pair with neighbouring W's faces under the structure's symmetries; **no face pairs with itself and the pairing graph is bipartite: faces {0,1,6,7} = bumps, {2,3,4,5} = dents** — so raised keys on 4 faces and the same keys sunk on the other 4 lock every pair, **with all W still one identical piece**.
- 2D drawing (`scripts/p4_key_drawing.py` → `data/p4-penrose-keys.json`, `renders/p4-penrose-keys.html`, claude.ai/artifact/…): the face with the OCD imprint cut away leaves a free disc of radius 0.1508; a Penrose sun (5 thick rhombi) + ring of 5 thin rhombi fits with rhombus edge 0.0548 (≈ 2.2 mm at a 60 mm octahedron edge — small; a bigger print or one larger key may suit stone).
- Still to draw (DICTO: "as many as possible"): the central Penrose prism as a key piece through W; a Penrose pattern on a chamber's exposed outer skin.
- **Step 8 set aside (DICTO: "not what I meant at all").** DICTO's meaning (10-18): "star centred W the set — the single piece meeting with itself around OCD locking together with keyed Penrose pattern"; "they all have to show because they are all keying joints, I don't need the star on the edges just a lobe or two, same scale as star though"; "the pattern seems continuous across the whole piece".

## Step 9 — picture first: lobed Penrose seams round one OCD (`scripts/p4_lobed_map.py` → `data/p4-lobed-map.json`, `renders/p4-lobed-map.html`)
- Exact fact used: every W–W joint next to the OCD passes through the OCD centre and the 12 edge midpoints are equidistant, so round the OCD the 12 star-centred W split directions like the spherical rhombic dodecahedron of the directions (0, ±1, ±1): **12 four-sided regions, one star each**; joints meet 4 at a time (6 places) or 3 at a time (8).
- Proposal drawn: every one of the 24 seams carries **two lobes, one each way** (thick Penrose rhombi, edge 0.2166 = the facing-star link rhombus, ≈ 8.5 mm at a 60 mm octahedron edge); each W gives as many lobes as it takes, so all W stay one piece; in 3D each lobe would run through the joint from the OCD outwards. Waiting for DICTO's read.

## Fable review 3 (654943a, `fable-review-3/REPORT.md`)
- **Both kits PROVED EXACTLY**: OCD + W_OCD and OCD + W_star (4 000 000 points each, 0/0).
- W_OCD: bites = OCD/6 each; 407 exact convex cells, one component; symmetry exactly m3̄ (achiral); 132 faces (120 imprints = one whole OCD surface); sharpest edge 86.9°, no knife edges; neighbouring sockets 0.1898 apart; 60 mm print: 73.5 mm across, smallest features 7.5 mm.
- W_star: octahedral cell confirmed; bites OCD/12; symmetry exactly 2/m; 32 faces; sharpest edge 75.4°; **the central and both flanking Penrose cores lie wholly inside one W_star (exact)**; it is a lens 60 × 42 mm with a **7.5 mm waist** at the centre (fixed by the OCD surfaces) — fine for print, the weak spot in stone.
- Wording: "centrosymmetric" → m3̄ / 2/m. Untested option: tetrahedron-site glue (cube − 4 OCDs, chiral pair). Open for DICTO: one big adaptor vs six links; 7.5 mm waist OK?
