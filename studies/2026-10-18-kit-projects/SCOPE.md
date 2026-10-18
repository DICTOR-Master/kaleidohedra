# Space-filling kit projects without the OCD — scope (DICTO 2026-10-18)

DICTO · dictospheres.com

**DICTO 10-18:** "I would like to scope building all of these kits minus the OCD, fused where appropriate, as separate space-filling projects" + "minimal parts sets".
Source: studies/2026-10-18-ocd-octet (steps 1–27, Fable review ba28bd0), envelope-network prior-art note. All three share the octet frame: octahedra |x|+|y|+|z| ≤ R, R = 2φ/3, on the fcc lattice, and regular tetrahedra T± (left/right where marked).

## Project 1 — Golden-key octet (from the keyed kit, step 5)
- Fuse: OCD + its 6 caps = the octahedron. **Minimal set: keyed octahedron (octahedron + 8 golden-envelope corner keys, exact (−32/9 + 64√5/27) = 1.744754) + dented tetrahedron, left and right (64/27 − 8√5/9 = 0.382754).** 2 shapes (+ mirror).
- Status: tiling PROVED EXACTLY by Fable (the fusion does not change it). Keys' base corners at the golden-section points of the octahedron edges.
## Project 2 — Penrose-core octet (from the keyless kit, steps 18–20)
- Fuse: OCD + its notched caps = the octahedron minus its 12 middle-piece notches. **Minimal set: notched octahedron + middle piece M₀ ((310 + 26√5)/4617) + notched tetrahedron L/R (0.265776).** 3 shapes (+ mirror). Penrose option: M₀ split into central core + flanking cores (L/R) + rest → 6 shapes (+ mirrors).
- Status: keyless kit tiling PROVED by Fable (sampled + exact construction); M₀ is defined from the OCD's five-fold stars (the OCD shapes the pieces even when it is fused away).
## Project 3 — Golden envelope octet (steps 21–27)
- No fusion needed beyond a solid envelope (the OCD is a passenger inside). **Minimal set: golden envelope (rhombic triacontahedron) + grown core piece L/R (0.555671).** 2 shapes (+ mirror). Larger sets: envelope kit (envelope, outer corner, dented tetrahedron L/R: 3) and refined kit (envelope, φ⁻² vertex cuboctahedron, wedge, cut-down tetrahedron L/R: 4).
- Status: exact construction; Fable review running (fable-review-2). Prior art: none found (Lalvani's RT packing differs).

## Per project (proposed deliverables)
1. Own study folder; Fable exact check of the minimal set; 2. 3D page; 3. printable STL per piece with the DICTO mark (scale to agree); 4. piece names in DICTO's scheme "DICTO <utility> set n (source)" — proposed, DICTO approves; 5. prior-art note; later: app world, paper/Zenodo.
## Outside the plan (noted only)
- bcc golden kit (golden gap unsolved), OCD-specific Penrose stars as their own art network.

## Decisions (DICTO 10-18)
- Go ahead with projects 1, 2, 3. Project 2: **whole middle piece** (minimal, 3 shapes). First step for each: **Fable exact check + 3D page**; STL and names after. Print size: **octahedron edge 60 mm**.
- DICTO: "does this include sets with cuboctahedron, and new dodecahedral shape derived kit?" → added as variants of project 3:
  - **3b Cuboctahedron set** (refined envelope kit, step 24/25): golden envelope + φ⁻² vertex cuboctahedron + wedge + cut-down tetrahedron L/R (4 shapes).
  - **3c Cuboctahedron + dodecahedron set** (new): as 3b, with each cut-down tetrahedron split into the central 12-pentagon dodecahedron (step 26) + the shell round it (L/R). To compute: is the shell one piece? exact faces of the dodecahedron.
  - 3 (two-shape set) is itself the dodecahedron grown to fill its cube (step 27).

## Outside the plan (DICTO 10-18): spherical containment chambers
- DICTO: "they would all work well in construction of spherical containment chambers". Idea noted: shells of lattice cells within a radius band (hollow chamber), or nested shells of different sets; adaptor halves let envelopes be left out to open/line the inner surface. Geometry only — nothing structural is claimed. Waiting for DICTO's choice (hollow chamber / nested shells / other) before a first picture.

## Status at a glance (10-18, end of day)
| Project | Minimal set | Exact | Fable | 3D page |
|---|---|---|---|---|
| 1 Golden-key octet (`2026-10-18-p1-golden-key-octet`) | keyed octahedron + dented tetrahedron L/R (2) | yes | keyed kit proved (ba28bd0) | BMcKgGY7iAYGZsWbQMWpE9 |
| 2 Penrose-core octet (`2026-10-18-p2-penrose-core-octet`) | notched octahedron + middle piece + notched tetrahedron L/R (3) | yes | keyless kit proved (ba28bd0) | BAQrqDmtUuuNUeXe4aexg4 |
| 3 Golden envelope octet (`2026-10-18-p3-golden-envelope-octet`) | envelope + grown piece L/R (2); 3b/3c need rework (wedges unbuildable) | yes | two-shape kit proved (8af2336); tetartoid exact | FBjG7XTk3xFykgUCfyGQXS |
| 4 Golden octet adaptor (`2026-10-18-p4-golden-octet-adaptor`) | envelope + adaptor half ×2 (2); one-piece RD; **envelope + W (Fable, 2, achiral)** | yes | W proved (8af2336) | 3Qw1XztMnTGiUuN1ntq1L9 |
- Ideas recorded: spherical chamber (half-open inside and outside), the general "half-RD network" of any golden-adaptable solid.
- Open for DICTO: grown piece (mirror pair, ψ 0.60) vs W (single, ψ 0.57); hidden flat cuts and 0.083 ridges OK?; STL (60 mm octahedron edge) and names next.

## Queue (DICTO 10-18, "save all points to research and queueing") — paused until Fable's keyed-W answer
1. **Keyed star-centred W (running, Fable):** the OCD imprint's rhombus pattern continued across the flat faces as a self-keying raised/sunk relief; one identical piece; 3D model + checks (brief in the SendMessage of 10-18; my failed attempt `p4_keyed_W.py` — raised tiles detached).
2. **Tiling the adaptor piece** (DICTO: "could these pieces be made by tiling, if so all our questions would be answered"; "we have potentially one adapter piece now to build from tiles"): which tile set builds the piece exactly. Facts: the envelope = 20 golden rhombohedra; the OCD's kites are not golden/Penrose angles; G′ is not face-to-face tileable by golden rhombohedra alone. Proposed order: envelope W first (golden sockets, best chance), then DICTO's keyed W (golden tiles + kite tiles for the imprint). Me stepwise, Fable only for the final check.
3. **Other networks for the casing** (DICTO: "are there other possible configurations which could orient it on icosahedral, tetrahedral or other networks?"):
   - **Diamond (tetrahedral):** OCDs joined on one tetrahedral set of 4 joint hexagons (the bump/dent split); casing = the diamond-network cell. Next after Fable (cleanest).
   - **Icosahedral cluster:** OCD + 12 on its five-fold axes, stars facing head-on (the exact OCD Stella seed pattern); several casing types because the OCD is only pyritohedral. Second.
   - Simple cubic (six two-fold joints), bcc (done: golden gap open), quasicrystal (golden envelopes in a 3D Penrose-type tiling; the full bridge; hardest).
4. Token thrift (DICTO): Fable only for proofs/hard builds; restate + yes before building; pages updated only when asked; short replies; background jobs, no polling.
5. **bcc casing (DICTO 10-18: "does any of our research bring us closer to solving the BCC gap?"):** the octet's casing trick carries over — each OCD's bcc cell (truncated octahedron) minus the OCD = one identical casing piece per OCD that fills the bcc gap exactly (thin shell, 8 openings at the joint hexagons; one-piece check to do); W-style variants (vertex/edge-centred) also exist in bcc. It fills the gap but not with golden pieces — the golden fill becomes the tiling question (item 2). Related exact results: G′ = 93√5/2 − 831/8, slabs closed by two rhombohedron layers, consistent keys, no Penrose link in bcc; Lin & Corbett 2006 precedent (rhombohedra between bcc triacontahedral clusters).

## Keyed W — Fable built it (978b0b0, `2026-10-18-p4-golden-octet-adaptor/fable-review-4/`, page claude.ai/artifact/9WH92CtD2ZLovmrqjY369u)
- One OCD star kite per flat face (4 raised, 4 sunk) at exact star scale, continuing a pierced star-edge row; one solid, every W identical, OCD + keyed W fills space (6 M points 0/0); the 12 W round an OCD cannot slide out in any direction; 60 mm: kite 9.4/7.8 mm edges, relief 2 mm, sharpest edge 75°. Only one kite per face fits at star scale.
- **DICTO 10-18 follow-up:** "I meant the keys to provide a continuous decorative pattern as well as key" → chose **option 2: star-scale kites running ACROSS the seams** (each kite split between neighbouring W, raised/sunk halves keying), pattern continuous over the whole assembly, all W identical, **"at a similar pattern depth to OCD"**. Open: depth = the OCD's facet fold (~1.1 mm at 60 mm) or the star's height (~5 mm)? Then Fable build or a 2D seam drawing first.
