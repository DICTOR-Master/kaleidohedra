# Leaning-sided Escher hexagon (9 Nov 2026)

**Conclusion:** the leaning sides do not force an aperiodic stacking, alone or combined with the ABC waveform. Leaning sides do open the in-plane channel (neighbours must match leans on shared sides), but a rigidity theorem closes it again. In every layer the leans are the gradient of one function on the cells, and that function can only be (i) one shear for the whole layer, which locks every cell of the layer, and every layer across a non-flat interface, into a single lean orientation; or (ii) a pattern with upright and turned-over copies in exactly equal numbers (stripes, or a few 2×2 patterns). (i) turns the 12 lean states per site into one per layer, so Theorem B and the 1D obstruction apply again. (ii) stacks only on flat interfaces, and only in h. Across 55 104 leaning pieces and 13 700 leaning-plus-wave combinations there are 0 candidates; every tiling piece has a periodic tiling. The one new effect is a weak one: the six-riser staircase E6 with all six sides leaning one way tiles only fcc (c), plus at most one paired stacking fault "hh".

**Status:** CLOSED for the aim in this form: planar leaning side plates on the RD/TRD carrier, plates on the 6 sectors, ≤ 12 placements (24 with mirror copies), with or without crest planes. All scripts end FINAL ok. Not committed, not published.

Credit: the leaning-sided Escher hexagon is DICTO's idea (9 Nov 2026). DICTO proposed the Escher stepped hexagon with all six sides leaning too, each side a tilted plate, so that the whole piece is a twisted, leaning hexagonal block whose neighbours in a layer rest on each other's leaning sides like plates in a rack. He also proposed turning the piece so that it leans in different directions (12 lean states), and combining the leaning sides with his ABC waveform. The closure analysis, rigidity theorem, model, scans and checks are Claude's (session 9 Nov 2026).

## 1. Construction (exact)

**Model (`scripts/leanplates.py`).** The model extends the plate model of the escher-hexagon study (`plates.py`, copied unchanged). All work is in fine-lattice coordinates, an affine image of space, so planarity, incidence, volume ratios and winding numbers are exact integer computations. Heights are in twelfths of a layer.

**The leaning cell.** At its waist (seat height) a cell is the regular hexagon round its seat. Its six vertical edges become lines:
- corner s: X + D_s + κ(z − 12k) w_s
- centre: X + κ(z − 12k) w_c

Here the leans w are integer vectors and κ is a free small scale. Side s is the strip between corner lines s and s+1. It is a plane (a tilted plate) exactly when w_{s+1} − w_s ∥ D_{s+2}. So a leaning hexagon is w_0 plus six numbers λ_s, with two closure equations. The top and bottom are the plate model's six sector plates, with their vertices on these lines.

**Contacts.**
- *In a layer:* two cells share a side plate iff they carry the same lines at both shared corners (corner leans equal). This is the new in-plane channel.
- *Between layers:* on every shared fine triangle the plate vertices coincide, both in height (as before) and in position: h·w_low − (h − 12)·w_up = Δ, with one drift Δ per interface.
- *Consequence:* leaning keeps every vertical-model condition and adds new ones. So a leaning piece tiles only if its plates tile with vertical sides, and its c/h words are a subset of the vertical words.

**Placements.** The 6 turns and the 6 turned-over placements (12; 24 with mirror copies) are distinct lean states. A turn turns every lean. Turning over maps w ↦ −f(w), so an outward lean becomes an inward one.

## 2. What leaning sides can do in one layer (`01_closure.py`; proofs + exact checks)

**Lemma L1 (closure: plates in a rack must close up).** Three tilted plates round a corner meet in one line iff their tilts sum to zero. The sympy determinant is (√3/2)·z·(t1 + t2 + t3).

**Theorem L2 (potential; Laguerre form).**
- The tilts of a layer are the differences ψ(Y) − ψ(X) of one function on the cells.
- Each corner line leans along the gradient of ψ on the three cells round it.
- Every horizontal cross-section is the power (Laguerre) diagram of the seats with weights −2zψ.

Checked exactly on a random 6×6 torus:
- 0 mismatches in corner lines or side planarity;
- total cross-section area equals the torus area identically in z;
- 36 of 36 corners are the power vertex;
- the closure system has rank 71 on 108 tilts, so the solution dimension is 37 = (#cells − 1) + 2 (potential plus two global shears).

**Theorem L3 (rigidity).** Let a = (a0, a1, a2) be the coefficients of 2·area(z) = a0 + a1·z + a2·z². Turning over flips the sign of a1. The total area of a layer is constant, and a bounded harmonic gradient is constant (discrete Liouville). Hence:

| Case | Lean | What the layer can be |
|---|---|---|
| P1 | λ = 0 (pure shear) | every cell of the layer has the same corner lines |
| P2 | λ ≠ 0, a1 = 0 | no layer |
| P3 | a2 ≠ 0 | no layer |
| P4 | a1 ≠ 0, a2 = 0 | upright and turned-over copies, exactly half each |

Consequences:
- **P1:** of the 12 lean states, only the placements that keep the lean can share a layer: 1 lean state per layer.
- **P4:** an outward-leaning (flaring) copy must rest on inward-leaning (tapering) turned-over copies. These are DICTO's plates in a rack.

**Census (every prediction holds).**

| Box | Classes (up to the 24 motions) | P1 shear | P3 | P4 that fill a layer | P4 that do not |
|---|---|---|---|---|---|
| w0 ∈ {−1,0,1}², λ ∈ {−1,0,1}⁶; tori of index ≤ 12 | 57 | 3 | 48, none fill | 6, all stripe type | none |
| w0 ∈ {−2..2}², λ ∈ {−2..2}⁶; tori of index ≤ 9 | 933 | 6 | 844, none fill | 34 | 49 |

- Of the 34 fillers in the larger box, 30 are stripes. In a stripe, two opposite sides stay vertical and four lean, giving rows of upright and turned-over wedges.
- The other 4 are 2D patterns, filling only tori of index 4 (2×2).
- No class fills an open patch of radius 4 without also filling a torus.

**Lean states, from DICTO's question "can it be revolved to lean in different directions" (`03` part D).**

| Lean type | Lean states per site | Most different lean states one layer can hold |
|---|---|---|
| Shear | 6 or 12 (24 with mirror copies) | 1 |
| Stripe | 6 to 24 | 2 or 4 |
| 2D pattern | 12 or 24 | 4 |

So the turned placements are real, distinct lean states, and each one does constrain its neighbours. The rigidity theorem is why most of them can never sit together in one layer.

## 3. Stacking (`02_stack.py`, `03_followup.py`)

**Controls.** All must come out as in the vertical model, and they do:

| Piece | Admitted c/h words | Periodic tiling caught |
|---|---|---|
| RD | ccc | yes |
| TRD | hhh | yes |
| RD + TRD | all 8 words | yes |
| sheared RD, (1,0) and (2,1) | ccc | yes |

**Lemma S (exact).**
- Two consecutive layers with different shears meet only where the interface is flat. Among sheared pieces: 1 152 such contacts, all flat, 0 not flat.
- Subset property: 0 violations.
- So on creased plates a shear is global: the stack is a sheared vertical tiling that uses only the placements fixing the lean. Part (A) confirms this exactly: the leaning words equal the union, over orientation classes, of the restricted vertical words (5 and 8 layers, proper and with mirror copies).

**Scan.**
- *Reliefs:* all 32 that tile with vertical sides: FLAT, RD, TRD, E1h (the forced-h ramp) and every uniform-bottom version of E1, E3, E3p, E6, RDE, RDE2.
- *Lean menus:* first run 307 leans, 19 648 batteries; second run, every layer-filling class of the larger box, 861 leans × 32 reliefs × 2, 55 104 batteries.
- *Battery:* SAT patches of 5 layers and radius 2 with in-layer contacts and drift, for every lean word; then the finite layer graph for every in-plane lattice of index ≤ 3, any vertical period, any skew.

Results of the second run:

| Lean type | Batteries | Outcome |
|---|---|---|
| Vertical sides | 64 | the escher-hexagon results; E1h with mirror copies is periodic on (3,1,1), hhhh (`03` C) |
| Shear | 637 | 503 NO PATCH; the rest PERIODIC-1 with words all c, all h, all, or the fault set |
| Stripe | 48 000 | 47 984 NO PATCH; 16 tile, all FLAT, all only hhh, PERIODIC-2 (rows) |
| 2D pattern | 6 400 | all NO PATCH |
| All | 55 104 | 0 CANDIDATE |

**The one correlation: the fault set.** E6u0 (six risers of 2) with all six sides leaning one way, shear (1,0), centre leaning the same way:
- Its patch words are ccc, cch, chh, hcc and hhc. The h letters come in pairs (8-layer patches: interior h-runs only of length 2).
- In the layer graph (every lattice of index ≤ 3, proper and with mirror copies), every cycle is an all-c loop. The 6 steps that change the lean (12 with mirror copies) join the 12 (24) one-cell components one way, and the longest chain of such steps is 1 (`scc_probe.py`).
- So the piece tiles fcc (c), with at most one paired stacking fault "hh" (a stacking fault of the fcc stack) in each stack whose layers have one of these periods.
- With vertical sides the same E6 admits every word. The lean does all of this by locking the orientation.
- It forces c, the periodic stacking, so it is the opposite of the aim. Recorded as a small result.

**Exact filling, independent of the contact tables (`03` B).** Explicit periodic tilings were built as closed polyhedral surfaces in integer coordinates at two lean scales, κ = 1/120 and 1/30:
- every wall and riser is planar;
- every cell volume is 36 (hexagon 3 × layer 12);
- the winding number of random points (exact ray casting) is exactly 1.

| Tiling | Cells | Random points | Winding numbers |
|---|---|---|---|
| RD with six sides leaning | 183 | 250 + 150 | all 1 |
| FLAT stripe (rows of wedges, hh) | 305 | 250 + 150 | all 1 |
| E6u0 with six sides leaning | 183 | 250 + 150 | all 1 |

## 4. Theorem B and the three earlier proofs

**Theorem B.**
- *Shear:* consecutive identical layers still occur in every shear tiling (all are PERIODIC-1), so Theorem B applies.
- *Stripe, FLAT:* every layer is forced non-uniform. In the 6 pieces of `03` D, every layer step changes the lean pattern, which meets Theorem B's escape condition in its narrow form. But layer k+2 is a translate of layer k, so the general form applies: any layer L with a motion τ such that τ(L) fits on L gives a periodic stack. Here it is period 2: hh.
- *Count:* in the layer graphs of all 153 tiling leaning pieces there are 2 416 steps with the same lean orientations above and below, and 1 080 with different ones.

**Lemma A.** It survives in its topological form. With overhangs the interface is no longer a graph, but it is still an embedded plane, so a closed loop on it cannot rise.

**The three earlier proofs:**
1. Golden phases: not relevant here.
2. Hexagon-only contacts: escaped in form, since the sides now carry conditions. Theorem L3 then collapses the in-plane lean information to one shear per layer, or one stripe direction and phase. That is a finite layer alphabet, and on it the stacking rules are a 1D shift of finite type, which always has periodic points.
3. Mirror copies: the results are the same with and without them.

## 5. Combination with the ABC waveform (`04_combined.py`; DICTO: "maybe combination can provide the extra impetus")

**Setup.**
- *Crest planes:* the abc-waveform menu adapted to the plate carrier. Tilted close-packed crests contain a row direction AC[t] and the seat step up one layer (D_u, 12), lean B-ward or C-ward, at offsets through the plate vertices; horizontal crests are added. That gives 37 planes per carrier.
- *Designs:* every single plane, every pair as one wave or as a two-colour mix, plus the empty design: 1 370 designs.
- *Rules:* STRICT and BEND (`wave_lib.py`), matched on the plates. The leans are matched on the sides.
- *Carriers:* RD, E6u0 and FLAT with six sides leaning; FLAT stripe; FLAT stripe2 (the always-changing one). Proper motions only, ≤ 12 placements.

**Results (13 700 batteries).**
- Controls: every empty design tiles periodically, exactly as in 02.
- 1 447 designs tile; 0 are CANDIDATE.
- 120 designs need non-uniform layers (the index-1 lattice is dead), but all are periodic on index 2.
- Every word set seen is all c, all h, every word, or the fault set. No new correlation appears.
- The combination adds rules on both channels but does not escape Theorem B.

## LEADS

1. **Rigidity theorem as a remark** (Theorem L2/L3: leaning layers are Laguerre diagrams, with rigidity by discrete Liouville). It is clean, short and new as stated here. Destination is DICTO's choice: the any-stacking paper or a small note.
2. **The fault-forcing piece.** E6u0 with all six sides leaning tiles only fcc with at most one paired fault "hh". It is a chiral, orientation-locked analogue of the RD. Prior art for "a monotile with bounded stacking faults" has not been checked.
3. **What is left for the aim.** In-plane information must be infinite-state per layer. Leaning sides cannot supply it (L3), and neither can locking orientation. A remaining route is the hierarchy of route 4 (vertical-plane hierarchy, Kari-type key), which needs non-uniform, non-repeating layers, as in the 6 Nov Kari analysis.
4. **Retry only with:** curved or bent (two-plate) sides, which escape L1 since the potential is then not linear in z; or a carrier other than the hexagonal footprint.

## Prior art (sources checked)

- **Topological interlocking** (Dyskin, Estrin, Kanel-Belov, Pasternak, 2001–2003). Platonic solids form interlocking assemblies; osteomorphic blocks have non-planar contacts.
  - Read via search snippets and abstracts: Cambridge MRS proceedings "Topological interlocking in design of structures and materials"; Bar-Ilan record "The principle of topological interlocking in extraterrestrial construction" (Acta Astronautica 2005); UWA "Toughening by fragmentation - how topology helps"; HEP "Mortarless structures based on topological interlocking"; arXiv 2312.01958 (arrangement strategies); arXiv 2405.01944 (Akpanya, interlocking blocks in the tetroctahedrille).
  - These are slabs of leaning or tilted blocks held by their neighbours, as in DICTO's rack. They are periodic, and are designed for mechanics, not for forcing a stacking.
- **VoroNoodles** (Ebert, Akleman, Krishnamurthy, Kulagin, Estrin, Adv. Eng. Mater. 2023, doi:10.1002/adem.202300831). Read in the escher-hexagon study, not re-read: helical layered space-fillers, periodic.
- **Laguerre/power diagrams and congruent cells.** Query "space-filling polyhedra tilted faces Laguerre power diagram layered tiling congruent cells": Wikipedia "Space-filling polyhedron" and "Plesiohedron" pages (Voronoi cells of symmetric Delone sets are congruent); Gabbrielli et al., Phys. Rev. E 86, 041141 (2012), tetrahedra–octahedra families; "Soft cells and the geometry of seashells" (arXiv 2402.04190). None treats leaning layered cells or the rigidity of L3.
- **Schmitt–Conway–Danzer biprism and Socolar–Taylor** (arXiv 1009.1419): cited from the escher-hexagon record, not re-read. SCD escapes Theorem B only by an irrational turn. Socolar–Taylor needs non-adjacent matching, which the closure lemma cannot provide.
- **Also cited for the aim:** Tsiokos arXiv:2609.19214 (Chair44) and Flicker arXiv:2609.23783, cited from the 8 Nov record, not re-read.
- **Not found:** any leaning-sided piece on close-packed (RD/TRD) cells, or the Laguerre rigidity statement in this form.

## Files

- **Scripts (`scripts/`):**
  - `plates.py`, `escher.py`: copied from the escher-hexagon study
  - `leanplates.py`: model, contacts, SAT, layer graph
  - `pieces.py`: reliefs and lean menus
  - `01_closure.py`: run as is, and with `box2`
  - `02_stack.py`: run as is, with `box2`, and with `pilot`
  - `03_followup.py`
  - `scc_probe.py`
  - `04_combined.py`: run as is and with `pilot`
  - `05_figure.py`
- **Data (`data/`):** `*.log` and `*.json`.
- **Figures (`figures/`), both with the DICTO mark:**
  - `leaning-hexagon-piece.png`: the E6 staircase with six sides leaning, from above and below, and the stripe pair (upright and turned over);
  - `leaning-hexagon-cluster.png`: a layer of seven with copies above, and the stripe rows over two layers.
- Everything ran on dicto-big-brother (`~/geom/bin/python`, 22 workers). The longest run, 04, took 220 s.
- The figures use matplotlib's depth sorting, which is imperfect at a few overlaps; the geometry itself is checked in 03 (B).

## Ledger line (ready for concordance.json ledger.entries)

```json
{"question": "DICTO 9 Nov: leaning-sided Escher hexagon - all six sides tilted plates (plates in a rack), piece revolved to lean in different directions (12 lean states), alone and combined with the ABC waveform crest planes", "method": "exact integer leaning-plate model on the RD/TRD carrier (corner lines X+D_s+kappa z w_s, planar sides w_{s+1}-w_s || D_{s+2}; in-layer contact = equal corner lines, interlayer = plate vertices coincide in height and position with one drift per interface); closure + rigidity checked on tori (sympy, SAT; 57 + 933 lean classes); scans 19648 + 55104 leaning pieces (32 reliefs that tile vertically x every layer-filling lean x centre leans x mirrors), SAT patches 5 layers + layer graph index <= 3; combination 13700 (5 carriers x 1370 crest designs x STRICT/BEND); exact filling by integer winding numbers + volumes", "status": "SETTLED (closed for the aim in this form)", "result": "L1: three tilted plates meet in a line iff tilts sum 0; L2: tilts = differences of a potential psi on cells, cross-sections = Laguerre diagrams with weights -2 z psi; L3 rigidity (area + discrete Liouville): one shear per layer (orientation lock, 1 lean state per layer out of 6-12) or upright/turned 50:50 patterns (stripes, four 2x2 patterns); Lemma S: different shears meet only on flat interfaces. Stacking: 0 candidates; shear pieces = vertical model restricted to the lean's stabiliser; stripes stack only on FLAT, only hh (period 2, layers alternate but Theorem B general form); combination with ABC waves: 1447 tile, 0 candidates, 120 need non-uniform layers but are periodic-2. Small result: E6u0 with six sides leaning tiles only fcc with at most one paired fault hh", "retry": "never with planar leaning sides on the hexagonal footprint (L3 makes the lean channel finite-state per layer); only with bent/curved sides (escape L1), infinite-state in-plane keys (route 4 hierarchy), or another carrier", "study": "2026-11-09-leaning-hexagon", "date": "2026-11-09"}
```
