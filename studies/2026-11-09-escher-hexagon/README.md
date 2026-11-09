# Escher stepped hexagon (9 Nov 2026)

**Conclusion:** the Escher stepped hexagon does not force an aperiodic stacking. In a layered tiling, the surface between two layers is a single-valued height function, so a full turn cannot rise. Every climb of the six plates is paid back by risers, which gives Escher's staircase with its impossible step made real. Whenever a staircase layer can carry a staircase layer of translates, the continuation is a screw of finite order (turns are multiples of 60°), and the stack repeats after at most 6 layers. Across the 6 named designs and 580 370 scanned pieces (a three-fold family and a helical-ramp family, each with every matching bottom), every piece either fails to fill a small patch or tiles periodically. The ramp pieces that tile are forced into h (hcp) at every interface, with three turns of the piece repeating in the plane.

**Status:** CLOSED for the aim in this form: the plate model on the RD/TRD carrier, with keys on the top and bottom only. All scripts end FINAL ok. Not committed, not published.

Credit: DICTO proposed an Escher stepped hexagon of tilting plates: the hexagon top (and the matching bottom) is cut into six tilted plates that climb round the vertical axis like Escher's endless staircase, so that one full turn rises by one seat level and a piece fits the one below only by continuing the staircase. The plate model, the consistency analysis, the families and the tests are Claude's (session 9 Nov 2026).

## 1. Construction (exact, integer heights)

**Carrier.** The carrier is close-packed layers along [111], ball spacing 1, layer spacing √(2/3). Heights are integers in units of 1/12 of a layer, so the layer spacing is 12.
- The seat points A ∪ B ∪ C form the fine triangular lattice, and every fine triangle has one corner of each letter.
- A layer-k cell sits on a seat of its layer's letter at height 12k. Its footprint is the hexagon of the 6 fine triangles round it, with vertical side walls, exactly as for the RD and TRD (hat-sectors study).
- Over each of its 6 sectors the cell is a prism between a planar bottom plate and a planar top plate. Each plate is given by integer values at its 3 corners.
- Neighbouring plates need not agree along their shared radial edge. A jump there is a vertical step (a riser) of the piece.
- The piece is the union of the 6 prisms. It is a polyhedron, not necessarily convex. `valid()` checks two things: positive thickness at all 18 sector corners, and that neighbouring prisms share a wall of positive area.

**Tiling rule (exact).** A layered tiling exists exactly when, on every fine triangle, the top plate of the lower cell equals the bottom plate of the upper cell plus 12. Each triangle column is then a stack of prisms with coinciding planes, so space is filled exactly once.
- An upper cell touches its 3 lower cells, each on 2 fine triangles.
- Neighbours in the same layer meet only on vertical walls, which carry no condition.
- So every constraint runs between layers.

**Checks (`01_controls.py`):**
- The RD relief (centre 9, corners 3 and 6) equals the exact hat-sectors relief (√3/2, 1/√3, 1/(2√3)), verified with sympy.
- The RD and TRD volumes come out exactly 1/√2.
- A space-filler must have mean thickness one layer (thickness sum 216). Every tested piece meets this.

**The stepped hexagon.** Plate s spans the rim corners D_s → D_{s+1}, going counterclockwise. It "climbs" when its value at the leading corner is higher than at the trailing corner. Named tops (`02_named.py`):

| Name | Top | Rise per turn | Risers |
|---|---|---|---|
| **E1** | helical ramp: six plates climbing 2 each, plate centres at the mean of their rim ends | 12 = one layer per turn | one riser of 12 |
| E3 / E3p | three flights (three-fold) | 12 | three risers of 4 |
| E6 | six risers (six-fold) | 12 | six risers of 2 |
| RDE / RDE2 | RD cap with its descending plates turned to climb | 18 | three risers of 6 |

E1 is figure 1, `figures/escher-hexagon-piece.png`.

**Matching bottoms (free parameter: how the next piece continues the staircase):**
- (a) Reassembly from the tops of the 3 lower cells, each upright and turned by k·60°, with the lower lean either way:
  - uniform: all 3 lower cells turned alike;
  - mixed: the 3 lower cells turned differently, so the climb is shared across neighbours.
- (b) The top turned end over end by a C2 about a horizontal axis. A helicoid is its own image under this turn, so the piece stays chiral.

**Proper motions.** A full cell with a hexagonal footprint has 12 proper placements per site: 6 turns and 6 turned-over placements. With mirror copies it has 24.

## 2. What the screw consistency forces (proofs)

**Lemma A (no net rise; this is Escher's impossibility).** In a layered tiling, the region below interface k is the union of layers ≤ k, so the interface is the graph of a function.
- Round any vertical line, the climbs of the plates plus the jumps (risers and wall steps) add up to 0.
- So "one full turn rises one seat level" can only be realised as climbs paid back by risers of the same total.
- Checked for every named top: rim climb + risers = 0 (E1: climb 12, riser −12).
- A true rise per turn would be a screw dislocation of the layer stack. Its Burgers vector would have to be a lattice vector, and rigid congruent cells do not fill a dislocation core.
- This is the reason Escher's 1960 lithograph and the Penroses' 1958 stairs need an impossible picture.

**Lemma A′ (corners).** Round a vertical edge where three cells of a layer meet, each cell's riser is answered by a wall step between neighbouring cells.
- In a layer of translates, the interface round every corner is a zig-zag (E1 corner values 9, 9, 1, 13, 5, 5; E3 1, 5, 1, 5, 1, 5), never a staircase.
- A staircase shared round a corner by 3 differently turned cells: 0 of 216 turn patterns, for every named top (`02_named.py`).

**Theorem B (a continued staircase is a finite screw).** Suppose a layer of translates in placement g carries a layer of translates in placement g′. Let τ be the motion that takes the lower layer onto the upper one: a turn by a multiple of 60° about a seat, then a shift to the next seat and up one layer.
- τ preserves every contact, so τ, τ², … stack the layers into a tiling.
- The turn has order m ≤ 6, so τ^m is a translation: the tiling is periodic with vertical period m ≤ 6 layers.
- So "a piece fits the one below only by continuing the staircase" always yields a periodic stack.
- The Schmitt–Conway–Danzer biprism escapes this only because its layer turn is an irrational angle. A hexagonal footprint allows only multiples of 60°.
- Every uniform-bottom piece in 02 is caught this way (verdict PERIODIC-1). Its stacking is all c or all h, or every word for the six-fold E6.

**Lemma C (Narcissus carrier, by argument; no new computation).** Put the staircase on the hexagon of Narcissus. The hexagon contact is then coaxial, which is exactly DICTO's picture. But it is a hexagon-only contact between one down-N and one up-N, so Lemma 2 of the ABC-waveform study applies unchanged: the admitted words are all words over the admitted bits, so the stacking can always be periodic.

A turned-over helicoid is the same screw, so it does mate with itself, but that does not change the product law. This is why this study uses the full RD/TRD cell, which carries two staircases (top and bottom) and couples consecutive interfaces.

## 3. Results (numbers)

**Controls (01).** All three behave as they must:

| Pieces | Admitted c/h words | Periodic tiling | Exact contacts checked |
|---|---|---|---|
| RD | only ccc | found | 276 |
| TRD | only hhh | found | 288 |
| RD + TRD | all 8 words | found | 252 |

Contacts were checked column by column, independently of the SAT model.

**Named designs (02; 6 tops, every bottom, proper motions and with mirror copies).** Each run ends in one of three verdicts:
- uniform bottoms: PERIODIC-1;
- mixed bottoms: NO PATCH (4 layers, radius 2) or PERIODIC-3 with only hhhh;
- C2-turned bottoms: NO PATCH. For E1 all six are valid solids (minimum thickness 2–12) but fill nothing.

No candidates.

**Scan (03, every piece with a non-uniform bottom; periodic test = finite layer graph for every in-plane period lattice of index ≤ 3, any vertical period, any skew):**

| Family | Tops | Pieces | NO PATCH | PERIODIC-3 | CANDIDATE |
|---|---|---|---|---|---|
| C3 (every plate climbs 1–4, centres 0–12, heights 0–13) | 51 376 | 575 049 | 541 296 reassembled + 33 753 C2 | 0 | 0 |
| C1 helical ramp (rim climbs 1–3, rise per turn 6/12/18, centre offset −2…4) | 1 001 | 5 321 | 3 775 reassembled + 201 C2 | 1 345 (hhhh only, also with mirror copies) | 0 |

**Follow-up (04).**
- 62 sampled periodic ramp pieces on 6-layer patches of radius 3 admit only hhhh, with or without mirror copies.
- The E1 piece with the forced-h bottom admits only hhhhh on 7-layer patches. Its only periodic lattice up to index 4 is the √3×√3 sublattice (HNF (3,1,1)), where the three turns of the piece cycle.
- The explicit stack (leans 2,1,2,1; 147 cells) passes 600 exact column contacts with 0 mismatches. This is figure 2, `figures/escher-forced-stack.png`.

**Against the three proofs of the ABC-waveform study:**
1. **Golden phases:** not relevant here. The steps are heights on one lattice, so there is no irrational phase.
2. **Hexagon-only contacts:** escaped in form. The full cell couples its bottom and top interfaces, with 3 contacts of 2 plates each. In practice, though, the word sets seen are only all-c, all-h or every word: still a filter on single letters, never a correlation. The structural reason: in this model, cells of one layer never constrain each other (their walls are vertical and free), so in-plane information has no channel except through the layers above and below.
3. **Mirror copies give all-S:** escaped. The pieces are chiral, and the C2-turned and ramp pieces behave the same with and without mirror copies. But the 1D obstruction returns through Theorem B.

**Capacity.** The full chiral cell has 12 proper placements per site, against ≤ 6 for Narcissus. This passes the ≥ 8 count of the 6 Nov Kari analysis on paper. The staircase pieces never use it: three-fold tops collapse to 4 distinct placements, and the ramp pieces settle into a cycle of 3.

## 4. Verdict against the aim

The staircase is chiral and reaches between two interfaces, so it meets both requirements the earlier proofs set. It still cannot force aperiodicity:
- Lemma A turns DICTO's endless climb into climbs plus risers.
- Theorem B turns "fits only by continuing the staircase" into a screw of order ≤ 6, which is periodic.
- Every staircase piece that does not continue uniformly either fails to fill a patch or settles into the √3×√3 three-turn pattern with forced h.

The c/h choice is again only filtered (all c, all h, or free), never correlated.

## LEADS

1. **Theorem B as a design rule (remark-sized, destination DICTO's choice):** a one-piece key must make every two consecutive uniform layers impossible, or a finite screw period follows. So any forcing piece must force non-uniform layers, which means in-plane structure.
2. **The free channel:** the vertical walls between cells of one layer carry no condition in the plate model. A key on the six vertical faces, together with plate steps, is the only way left for in-plane information. This is route 4 (vertical-plane hierarchy) on the full chiral cell, now with 12 placements per site instead of 6.
3. **Forced-h ramp (small result):** the E1 ramp with a mixed reassembled bottom is a chiral RD/TRD-type piece that tiles only the hcp stacking, in a three-turn √3×√3 pattern. It is a chiral analogue of the TRD. Prior art and the identity of the piece are not yet checked.
4. **Retry only with:** wall keys plus plates (lead 2), or turns that are not multiples of 60° (impossible on a hexagonal footprint, so this needs a different carrier).

## Prior art (sources checked)

- **Escher, Ascending and Descending** (lithograph, March 1960), and **L. S. Penrose and R. Penrose**, "Impossible objects: a special type of visual illusion", Br. J. Psychol. 49 (1958) 31–33, doi:10.1111/j.2044-8295.1958.tb00634.x. Read via Wikipedia "Impossible object" and "Penrose stairs" (search snippets), which also give the 1956–1959 drafting dates and record that Escher received the article. Lemma A is the geometric form of why the staircase is impossible.
- **Schmitt–Conway–Danzer biprism.** The layers turn by θ, and with θ/π irrational there is no translation; some tilings keep a screw symmetry, so the tile is weakly aperiodic, and mirror copies allow periodic tilings.
  - Sources: MathWorld "Schmitt-Conway Biprism"; Socolar–Taylor arXiv:1009.1419 (intro); Baake–Frettlöh, "SCD patterns have singular diffraction", math-ph/0411052 (title and abstract via search).
  - In DICTO's library (title only, not re-read): L. Danzer, "Three-dimensional analogs of the planar Penrose tilings and quasicrystals" (1989).
  - Also cited by Tsiokos arXiv:2609.19214 §1, read 8 Nov.
  - Theorem B is the close-packed counterpart: there, only finite turns are possible.
- **Helical stacking of space-fillers:**
  - M. Ebert, E. Akleman, V. Krishnamurthy, R. Kulagin, Y. Estrin, "VoroNoodles: Topological Interlocking with Helical Layered 2-Honeycombs", Adv. Eng. Mater. 2023, doi:10.1002/adem.202300831. Read the first page: tiles stacked along helical paths, periodic, for interlocking, not for aperiodicity.
  - C. H. Séquin, Bridges 2008 "3D tiles" (search snippet: 2D tiles assembled layer by layer by a helical screw motion, M. Goerner's cog-wheel tiles).
  - Neither forces a stacking.
- **Web queries:**
  - "Schmitt Conway Danzer biprism screw aperiodic prototile irrational rotation layers"
  - "Penrose stairs 1958 Impossible objects …"
  - "helicoidal space-filling polyhedron screw tile stacking tiling three dimensions" (also returned Wikipedia "Space-filling polyhedron" and the SCD wiki pages)
- **Library grep** (dicto-big-brother `~/kaleidohedra-references`, all MANIFEST.json, for danzer, schmitt, escher, penrose stair, helicoid, screw): Danzer 1989 (above), Penrose-tiling titles ("Algebraic theory of Penrose's non-periodic tilings of the plane" I/II, "Constructing Penrose-like tilings from a single prototile …", "Penrose tilings as coverings of congruent decagons"), and "Helical microtubules of graphitic carbon" (not relevant). Nothing on helicoidal or stepped space-fillers.
- Not found: any stepped-helicoid piece on close-packed (RD/TRD) cells, or any stacking forced by one.
- **Also cited for the aim:** Tsiokos arXiv:2609.19214 (Chair44) and Flicker arXiv:2609.23783 (cited from the 8 Nov record, not re-read today).

## Files

- **Scripts (`scripts/`):**
  - `plates.py`: model, placements, compatibility, patches, layer-graph periodic test
  - `escher.py`: tops, bottoms, test battery
  - `01_controls.py`
  - `02_named.py`
  - `03_scan.py`: families C3 and C1
  - `04_followup.py`
  - `05_figure.py`
- **Data (`data/`):** `*.log` and `*.json`; pilots `03_pilot.log`, `*_pilot.json`.
- **Figures (`figures/`):** `escher-hexagon-piece.png` and `escher-forced-stack.png` (DICTO mark on both).
- Everything ran on dicto-big-brother (`~/geom/bin/python`; the longest run, the C3 scan, took 817 s on 22 workers).

## Ledger line (ready for concordance.json ledger.entries)

```json
{"question": "DICTO 9 Nov: Escher stepped hexagon - top/bottom hexagon cut into six tilted plates climbing round the axis (endless staircase), one turn = one seat level, piece fits only by continuing the staircase; chiral + two-layer, screw on close packing", "method": "exact integer plate model on RD/TRD carrier (prisms over the 6 fine triangles, plates per sector, risers = vertical steps; tiling <=> top plate = bottom plate + H on every fine triangle); controls RD/TRD/RD+TRD; 6 named tops x every matching bottom (reassembled from 3 lower cells uniform/mixed, C2-turned); scans C3 (51376 tops, 575049 pieces) and C1 helical ramp (1001 tops, 5321 pieces); SAT patches + finite layer graph for every in-plane period lattice index <= 3 (<= 4 follow-up), proper motions and mirror copies", "status": "SETTLED (closed for the aim in this form)", "result": "Lemma A: interfaces are graphs, so net rise per turn = 0; the climb is paid back by risers (Escher/Penrose impossibility); round 3-cell edges risers are answered by wall steps (zig-zag; shared staircase 0/216 patterns). Theorem B: a uniform layer carrying a uniform layer gives a screw of order <= 6 -> periodic, period <= 6 layers (SCD escapes only by irrational turns). Scans: 0 candidates; every piece NO PATCH or periodic; ramp pieces that tile are forced hhhh with sqrt3 x sqrt3 three-turn pattern (1345; E1 stack checked exactly, 600 contacts). Escapes proofs 2 and 3 in form, not in effect; capacity 12 per site unused", "retry": "never as top/bottom plates alone; only with keys on the vertical walls (in-layer channel, route 4 on the full chiral cell, 12 placements per site) or a carrier allowing non-60-degree turns", "study": "2026-11-09-escher-hexagon", "date": "2026-11-09"}
```
