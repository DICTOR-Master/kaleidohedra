# Hat sectors on RD/TRD layers (desk study, 9 Nov 2026)

**Conclusion:** the hat route does not serve the aim. A hat-shaped piece made of RD sectors needs its own mirror image (turning it over covers only half of the orientations the hat tiling uses). With mirror images allowed it tiles only c-layers, so it forces the periodic fcc stacking, with aperiodic layers that are independent of each other (weakly aperiodic). A TRD-sector piece cannot even tile a 19-hexagon patch of one layer.

**Status:** CLOSED for the aim (exact geometry + SAT certificates, all scripts FINAL ok). Not committed, not published.

Credit: DICTO proposed the aim (one RD/TRD cross piece forced into an aperiodic stacking; Narcissus). The hat route tested here is Claude's proposal (session 8/9 Nov 2026). DICTO replied "good call".

Files: `scripts/hatgrid.py` (exact kite grid + hat), `01_sectors_exact.py` (sympy, exact), `02_orientation_sat.py` (SAT, pysat Cadical), `03_piece_orientations.py` (all 4^8 sector patterns), `04_figure.py`; logs in `data/`; figure `figures/hat-piece-rd.png`. Everything ran on compute-host (`python3`), each in under 5 minutes.

## Task 1: exact geometry (01_sectors_exact.py, 17 PASS)

RD with corners (±1,0,0) and (±½,±½,±½) (volume 2), stacking axis [111] vertical. Heights are in Q(√3).

- **Mid-section:** this part of the claim holds, and it is stronger than stated. For both RD and TRD, the 6 faces whose normals are perpendicular to [111] are **vertical**. The cell's projection along [111] is the same regular hexagon (circumradius √6/3, apothem √2/2) as its mid-section. Each cell is therefore a hexagonal prism with a slanted top and bottom. The cells of one layer project onto the hexagonal tiling, and the 6 kite sectors of a cell (cut by vertical half-planes from the axis to the edge midpoints) are **prisms over the kites, with vertical walls**. Their top and bottom surfaces are linear on the two triangles of each kite, with a crease only along centre–tip.
- **Relief** (heights, bottom to top): at the centre C, [−√3/2, √3/2]; at every edge midpoint M, [−√3/4, √3/4] (the same for RD and TRD). Only the kite tips V differ:
  - RD: the tips alternate between [−1/(2√3), 1/√3] and [−1/√3, 1/(2√3)].
  - TRD: the tips alternate between fat [−1/√3, 1/√3] and thin [−1/(2√3), 1/(2√3)].
- **RD sectors:** this part of the claim is confirmed. The 6 sectors are congruent, each has 1/6 of the volume, and alternate ones are each other turned upside down (by S6, and also by a proper half-turn C2, because each sector has its own vertical mirror).
- **TRD sectors:** this part of the claim is **corrected**. The horizontal mirror maps each sector to itself, not to its neighbour. The TRD has two non-congruent sector kinds, with volumes 13/36 and 11/36 (13/72 and 11/72 of the cell).
- **Does the hat piece tile the layer, and does the turned-over copy fit?** Any 2D hat tiling cuts the corrugated layer exactly into 8-sector pieces. Those pieces are one 3D piece only if every hat lies in orientations that the layer's motions reach (03, exhaustive over all 4^8 sector patterns and all 4 layer contexts):
  - **RD piece in a c-layer, proper motions only:** it reaches {turns by 0/120/240°, reflections in the centre–midpoint lines}. Turning it over does give the reflected hat, but only in 3 of its 6 orientations. The unreflected hat turned by 60/180/300° can only be reached as the 3D mirror image (S6).
  - **TRD piece in an h-layer:** it reaches {0/120/240°, reflections in the centre–vertex lines}, with or without mirrors (the piece is its own mirror image in h = 0).
  - **RD piece with mirrors allowed:** it reaches all 12 orientations, in c-layers only.
  - **No sector pattern** fits both a c-layer and an h-layer.
- **SAT** (02), on discs of the kite grid where every kite is covered exactly once and pieces may stick out into a 3-hexagon margin:
  - Controls: all 12 orientations give SAT at R = 0…6; rotations only give UNSAT from R = 2.
  - The RD proper set {r0 r2 r4 s1 s3 s5} is **UNSAT already at R = 1** (7 hexagons).
  - The TRD set {r0 r2 r4 s0 s2 s4} is **UNSAT from R = 2** (19 hexagons).
  - The two twin cosets give the same results.
  - So no hat patch even of radius 2 stays inside half of the orientations. This matches SMKG §2: "unreflected tiles come in six orientations".

## Task 2: which stackings, what is forced

- The RD hat piece (mirror images allowed) tiles each c-layer as a hat tiling and fits nowhere in an h-layer, so **every layer is c: the stacking is forced to ABCABC (or its twin), which is periodic.**
- The TRD hat piece tiles no layer. No mixed piece of this kind works in both c and h.
- The interfaces between layers are the RD's own upper and lower faces, whatever the kite grouping, so the layers' hat tilings are **fully independent**. Copying one layer's tiling up the fcc vector gives a 3D period.
- Assuming the piece only tiles in layers (not proved here), the result is weakly aperiodic: no rank-3 period lattice exists (that would leave a period inside a hat layer), but a 1D period does. This is the Socolar–Taylor 3D / hat-prism situation.
- There is no coupling between the hat hierarchy and c/h. The 1D obstruction is not even reached, because the c/h choice itself is fixed.

## Task 3: prior art (sources checked)

Cited:
- D. Smith, J. S. Myers, C. S. Kaplan, C. Goodman-Strauss, "An aperiodic monotile", arXiv:2303.10798 (Combinatorial Theory 2024).
- Same authors, "A chiral aperiodic monotile" (spectre), arXiv:2305.17743.
- I. Tsiokos, "A Strongly Aperiodic Monotile in Three Dimensions", arXiv:2609.19214 (Chair44; §1 history of the SCD biprism and the Socolar–Taylor 3D slabs; §10 Q8 asks for the mechanism "on other lattices").
- F. Flicker, "Matching Rules for a Three-Dimensional Strongly Aperiodic Monotile", arXiv:2609.23783 (cited from the 11-08 record, not re-read today).

Checked:
- **DICTO's library** (compute-host `~/kaleidohedra-references`, MANIFEST grep for monotile/einstein/spectre/hat/Socolar/Danzer/aperiodic):
  - SMKG 2023 pdf (full text grep: 3D mentioned only as "a three-dimensional shape" enforcing matching rules, plus the SCD tile; "unreflected tiles come in six orientations" §2; tiles aligned to the [3.4.6.4] Laves grid §3).
  - Baake–Grimm 2012; Baake–Damanik–Grimm 2015; Al-Siyabi–Koca–Koca 2020.
  - expansion/MANIFEST arXiv query "aperiodic monotile OR einstein tile": hat metasurface paper; Ising model on the Smith hat; Schirmann–Franca–Flicker–Grushin (dropped file); translational-tiling undecidability papers.
  - None of them treats a 3D hat on RD/close-packed layers.
- **Web queries:**
  - "hat monotile extruded prism three dimensions weakly aperiodic"
  - "hat aperiodic monotile rhombic dodecahedron OR close-packed layer stacking"
  - "aperiodic monotile 3D polykite hat 3D tile layers arXiv 2024 2025"
  - "spectre OR hat monotile prism space-filling 3D aperiodic layer einstein three-dimensional generalization"
- **Pages:**
  - arXiv 2609.19214 (full text)
  - aperiodical.com comments on "Now that's what I call an aperiodic monotile!": Jens, 11 Jul 2023, a hat-like tile "that seems to tile 3D space aperiodically", unverified, no paper; B. Klaassen, 11–12 Sep 2023, on SCD's screw symmetry
  - Wikipedia "Socolar–Taylor tile" (3D version weakly aperiodic, periodic stacking)
  - J. Smith, "Turtles, Hats and Spectres: Aperiodic structures on a Rhombic tiling", arXiv:2403.01911 (snippet)
  - divisbyzero.com 3D-printable monotiles (thin extrusions; snippet only)
  - MyMiniFactory hat print
  - lifeboat.com repost on Tsiokos
- **Not found:** any hat built from RD/TRD sectors, or any hat forcing a close-packed stacking. Extruded hat prisms (hat × interval) are folklore: weakly aperiodic, with mirror images.

## Task 4: figure

`figures/hat-piece-rd.png` has three panels:
- top view of the hat over the hexagon/kite grid (gold = tip high on top, blue = tip deep below);
- the RD hat piece in 3D;
- the same piece turned over.

DICTO mark included.

## LEADS

1. **Remark-sized result:** the RD hat piece with mirrors is a 3D tile whose layers are forced aperiodic while the stacking is forced *periodic* (fcc), the opposite of the aim. Destination: DICTO's choice (a remark in a later Narcissus/aim paper?). Still open: proving that the piece only tiles in layers.
2. **General criterion found here:** a piece made of close-packed cell sectors over a 2D tile works with proper motions only if the 2D tile's tilings use only 120° turns plus one mirror family (p31m/p3m1 orientations). The hat fails at radius 1–2. The spectre should fail too (its tilings need 30° turns; expected, not checked). Is there a 2D aperiodic monotile with only 3-fold orientations? None known to us.
3. **Only place the in-plane pattern can see c/h:** pieces straddling the flat slab between two atomic mid-planes (upper half-cells of layer k + lower half-cells of layer k+1, the half-cell framing of the 4 Nov ledger entry). Even there, the 1D obstruction needs a hierarchy in a vertical plane (route 3, 11-05).
4. **Tsiokos Q8 ("other lattices"):** features on an RD (fcc) carrier could force a strongly aperiodic lattice substitution, but on a fixed fcc carrier, so again not the c/h stacking aim.
5. **Best next step for the aim:** return to route 3 (hierarchy in a vertical plane, rows = layers, c/h = level parity) on the Narcissus carrier. The hat route is closed.

## Ledger line (ready for concordance.json ledger.entries)

```json
{"question": "Claude 8/9 Nov (DICTO: 'good call'): hat monotile as in-plane engine; hat-shaped piece of 8 RD/TRD kite sectors, mirror hat by turning over, one piece", "method": "exact sympy relief of RD/TRD about [111] (01_sectors_exact.py, 17 PASS); all 4^8 sector patterns x 4 layer contexts (03); SAT exact cover of kite-grid discs per orientation set (02, pysat Cadical)", "status": "SETTLED (closed for the aim)", "result": "RD/TRD equatorial faces vertical: sectors are kite prisms with slanted top/bottom; RD 6 sectors congruent (1/6 each); TRD 2 kinds 13/36, 11/36 (claim 'related by horizontal mirror' wrong). Turning over reaches only {0,120,240 deg + centre-midpoint mirrors}; hat needs more: UNSAT at disc R=1 (RD set) and R=2 (TRD set), controls ok. With mirrors allowed the RD piece tiles c-layers only -> forces periodic fcc stacking, layers independent (weakly aperiodic); TRD piece tiles no layer; no piece fits both c and h", "retry": "never as layer pieces; only straddling pieces (half-cells of two layers) or a 3-fold-only 2D aperiodic monotile would reopen it", "study": "2026-11-09-hat-sectors", "date": "2026-11-09"}
```
