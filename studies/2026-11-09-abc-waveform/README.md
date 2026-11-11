# ABC waveform on Narcissus (9 Nov 2026)

**Conclusion:** DICTO's ABC wave does not force an aperiodic stacking on one Narcissus. We tested 1944 crest designs under two matching rules, with and without mirror copies (7774 runs). Each run either fails to fill a patch or fills it periodically. The fillings that survive allow every stacking word, or only SSSS (h), or only TTTT. No design excludes both constant words. Three short proofs explain why: (1) a golden wave cannot be carried by one piece; (2) a wave on the top and underside alone couples nothing; (3) the "lean back" rule with mirror copies always allows the h-stacking.

**Status:** CLOSED for the aim in this form (Narcissus carrier, crest planes from the close-packed families, face matching). All scripts end FINAL ok. Not committed, not published.

Credit: DICTO proposed an ABC waveform on the surfaces, a golden mix of waves: crests at the three seat positions A, B, C on top, the reciprocal wave underneath, and the wave decides whether the next layer keeps leaning (c) or leans back (h). He also agreed to the Ammann-bar adaptation, in which different orientations of the one piece show different wave phases. The formalisation, the design menu and the tests are Claude's (session 9 Nov 2026).

## 1. Formalisation

**Carrier.** The carrier is the Narcissus slab stacking of #97 (`scripts/n_slabs.py`, copied from `studies/2026-11-05-one-piece-any-stacking`).
- Slab k holds down-N on the X sites (hexagon on top) and up-N on the Y sites (hexagon below).
- Each interface is S (straight: the next slab is the mirror in the interface plane) or T (turned: mirror, then a 60° turn). SSS… is the hcp h-tiling and TTT… is the Covenant pairs. S is "lean back" and T is "keep leaning".
- Every face of N touches exactly one neighbour, whole face to whole face:
  - the hexagon touches the hexagon across the interface;
  - the 3 quads touch opposite-pointing N in the same slab (honeycomb);
  - the 6 vertical triangles touch same-pointing N (triangular lattice).

**Wave = crest planes.** A design is a finite set of coloured planes fixed in the reference piece P0. Each piece in a tiling carries these planes moved by its own placement: 3 turns, plus 3 mirror placements if mirror copies are allowed. So the same piece shows different crest directions and phases in different orientations, as Ammann bars do on Penrose tiles.

**Menu of crest planes (67 planes that cut the piece):**
- 6 tilted close-packed families: "lean B-ward" b1, b2, b3, spanned by a row direction and the A→B stacking vector; "lean C-ward" c1, c2, c3, the same with the A→C vector.
- The horizontal family z.
- Offsets H·j/6, which put crests through the seat rows A, B, C and the rows between them.
- Golden phases H(j + 1/φ) and H(j + 1/φ²).

**Designs (1944 up to the symmetry of N and colour swap):**
- the empty control;
- every single plane;
- every pair, either as one wave (one colour) or as DICTO's two-wave golden mix (two colours);
- the 3-fold closure of every plane and the 6-fold (C3v) closure of every plane.

**Local rule, checked on every face contact:**
- **STRICT** (Ammann): the set of crest planes that cut the shared face is the same on both sides. Crests run straight through the piece boundary.
- **BEND** (DICTO's lean back): only the crest *lines* on the shared face must agree. A crest may change direction at a face, for example reflect at an S interface.
- Colours must agree in both rules.

**Tests** (`scripts/scan.py`, SAT with CaDiCaL, one variable per piece and placement; `scripts/wave_lib.py`):
- (a) **PATCH**: a decorated filling exists for some S/T word of 5 slabs on the n = 3 patch. That is 490 pieces, of which 200 are interior with all 10 contacts.
- (b) **PERIODIC**: a decorated filling exists on a torus. The tori cover the words S, T⁶ and (ST)⁶, every in-plane sublattice of index ≤ 3 (Hermite forms) and every skew representative. These are the skewed tori of the 6 Nov review, 57 tori in all.
- (c) **WORDS**: the set of S/T words of length 4 admitted on the patch.
- A **CANDIDATE** passes (a) and fails (b). Each candidate was followed up with:
  - a patch of n = 5 (1210 pieces) and tori of index ≤ 9 (1326 tori), `scripts/followup.py`;
  - then a patch of n = 7 (2250 pieces).

## 2. Three facts that bound the idea (proofs short, all checked against the data)

**Lemma 1 (a golden wave needs infinitely many phases).** Take a relief w(x) = cos 2π(k·x) + cos 2π(φk·x).
- Every Narcissus position lies in one fixed lattice Λ (the close-packed positions with heights in H·Z).
- k·x is unbounded on the positions a tiling uses. So the pair (k·x, φk·x) mod 1 takes infinitely many values: if k·Λ ⊂ sZ, then φsm mod 1 repeats only if φs is rational, and then s itself is irrational.
- One rigid piece shows at most 6 profiles.
- So the golden mix must be discretised in the Ammann way: finitely many crest positions per placement. Any golden order would then have to come from *which* placements sit where. That is the symbolic question the scan tests.

**Lemma 2 (a wave on the top and underside alone couples nothing).** Suppose the wave is a relief on the hexagon only (the top of a down-N, the underside of an up-N).
- Each hexagon contact joins one down-N of slab k to one up-N of slab k+1, and neither piece has a second hexagon.
- So the admitted words are exactly all words over the set of single bits that some pair accepts. This always includes a constant word, so the stacking can always be periodic. This is the 1D obstruction with zero layers coupled.
- Checked exhaustively (`scripts/hexrelief.py`) on all 165 reliefs (levels 0/1/2 at the 6 hexagon corners, which are the B and C seats; crest into trough). The product law holds for every relief:

  | Admitted bits (mirror copies no / yes) | Reliefs |
  |---|---|
  | none (no filling) | 144 / 144 |
  | T only | 16 / 16 |
  | S only | 3 / 2 |
  | S and T, every word | 2 / 3 |

**Lemma 3 (lean back with mirror copies always allows h).** Use the BEND rule with mirror copies allowed.
- Take any valid decorated slab X. Stack X, σX, X + 2H, … where σ is the mirror in the interface plane. This is the all-S word.
- σ preserves every in-slab contact and maps crest lines on the hexagon to themselves, so every contact still matches.
- So if the design fills anything, it fills the h-stacking SSSS…, with vertical period 2 slabs.
- Data: all 105 BEND runs with mirror copies that fill a patch admit SSSS.
- With STRICT the mirror breaks any crest plane that crosses the hexagon (it is reflected, not continued). That is why straight tilted crests force T instead (below).

## 3. Results (numbers)

Full scan, 3 shards on compute-host, 609 + 572 + 534 s, `data/scan-full-shard*.log`; merged by `scripts/merge.py` into `data/merge.log`.

**Control (empty decoration):** PATCH with all 16 words and PERIODIC at index 1, under both placement rules. The test catches it, as it must.

**7774 runs:**

| Verdict | Runs |
|---|---|
| NO PATCH at n = 3 | 7549 |
| PERIODIC (torus found) | 213 |
| CANDIDATE | 12 |

**The 225 runs that fill the n = 3 patch, by admitted word set:**

| Word set | Runs | What it means |
|---|---|---|
| all 16 words | 67 | the wave does not read the stacking: horizontal crests, controls, some BEND pairs |
| SSSS only | 133 | the wave forces h, periodic |
| TTTT only | 23 | forces "keep leaning": STRICT tilted c-lean crests, e.g. C3:c1 at H/3 (figure 2) |
| 11 words | 2 | C3:b1 at the golden phase H(1/φ − 1), BEND; excludes STTS, STTT, TTSS, TTST, TTTS but keeps SSSS and TTTT |

**No run that fills a patch excludes both SSSS and TTTT.** At no size did any design show a Fibonacci-like word set (one with neither SS nor TT runs). STRICT tilers number 16 with mirror copies and 15 without: horizontal crests give all words, tilted crests give TTTT only.

**The 12 candidates all use a golden-phase b-lean crest:**
- At n = 5, six die (NO PATCH).
- The other six shrink to the 4 words TS·· and no torus of index ≤ 9 holds them (`data/followup-K5-n5-I9.log`).
- At n = 7, all six die (`data/followup-K5-n7-patch.log`).
- So the candidates were finite-patch artefacts. A golden crest phase on one piece can almost never be continued by a neighbour, because the neighbour's crest offsets differ by lattice amounts. This is Lemma 1 seen from the other side.

**Forced words (`scripts/forced.py`, K = 5, n = 3):**
- C3:c1 at H/3 STRICT → TTTT only.
- C3:b1 golden BEND → the 11 words above, which die at n = 7.

**Figures:**
- `figures/abc-wave-piece.png`: Narcissus with DICTO's golden-phase lean crests (C3:b1, BEND) and the hexagon top view with the seats A, B, C.
- `figures/abc-wave-straight-stack.png`: the TTTT-forcing design. Straight lean crests run through the hexagon centre A, and a decorated TTTT stack from the SAT model is shown.
- No aperiodic forced stack exists to draw.

## 4. Verdict against the aim

The literal idea (top relief + reciprocal underneath) fails by Lemma 2. Its 3D form (crests through the body, BEND = lean back) fails by Lemma 3 when mirror copies are allowed, and in the scan without them. The golden mix fails by Lemma 1: it can only enter as finitely many Ammann phases, and these give no new constraint.

Across the menu, a crest decoration on one Narcissus acts as a **filter on single interface bits**: it allows S, T or both, never a correlation between interfaces. The 1D obstruction then applies directly.

The underlying wall is the per-site capacity: one piece has at most 6 placements per site.
- The Kari-type counts of 6 Nov need 8 or more states per site.
- Edge keys (64 967 designs, 6 Nov) all repeat.
- Face crests (this study, 1944 designs) all repeat or die.

## LEADS

1. **Lemma 3 as a design rule (remark-sized, any destination DICTO picks):** any "lean back" rule must not be reflection-symmetric across the hexagon, or mirror copies hand back the h-stacking for free. Future one-piece keys should be chiral in that sense, or should forbid mirror copies.
2. **Where the wave idea can still live (best open adaptation):** the vertical plane of route 4. A vertical plane along a row of pieces is a triangular lattice whose rows are the layers. The tilted lean planes cut it in the other two line directions, which zig-zag at h. Two Ammann-like crest families crossing in that plane with Fibonacci spacing would be a genuine 2D Ammann system whose row-spacing word is the stacking word. This needs several piece types (the #97 count). With one piece it would need a capacity of at least 8 per site.
3. **Golden geometry instead of golden decoration (outside the plan):** Ammann's golden spacings come from tile lengths in the golden ratio. Here all positions sit on one lattice. If S-slabs and T-slabs had different thicknesses in the ratio φ, the crest heights themselves would carry the Fibonacci signal. That needs two slab types, so two pieces, or a piece that fills a slab in two thicknesses (none known).
4. **Carrier check not done:** the RD/TRD half-cell as carrier (top = 3 rhombi seating on 3 balls, closer to DICTO's seat picture). Lemmas 1–3 transfer verbatim: one hexagon equator per half-cell, and the mirror across the equator. Expect the same verdict. Retry only with a chiral key.

## Prior art (sources checked)

- **Ammann bars / Fibonacci:** B. Grünbaum, G. C. Shephard, *Tilings and Patterns* (Freeman 1987), ch. 10. In DICTO's library only as a citation (`papers`/`cited` MANIFEST), not read. Its Ammann-bar/Fibonacci content was taken from secondary sources: Bielefeld Tilings Encyclopedia, "Ammann Bars" glossary (tilings.math.uni-bielefeld.de/glossary/ammann-bars/); arXiv 2205.13973 "Ammann Bars for Octagonal Tilings", which states that G–S detail Ammann bars for Penrose tilings and their relation to the Fibonacci word, and that this inspired Stehling's 3D analogue.
- **3D Ammann planes:**
  - J. E. S. Socolar, P. J. Steinhardt, "Quasicrystals. II. Unit-cell configurations", Phys. Rev. B 34 (1986) 617: library entry (link only, not read); abstract via search.
  - C. Hann, J. E. S. Socolar, P. J. Steinhardt, "Local growth of icosahedral quasicrystalline tilings" (2016), library pdf, read §II: Ammann rhombohedra with chiral matching decorations, both enantiomorphs needed, "at least weak matching rules"; perfect matching rules not proved.
  - Web: arXiv 2603.13553 (matching rules as cocycle conditions; Ammann icosahedral tiling).
- **Socolar–Taylor:** digest of arXiv 1003.4279 and 1009.1419 from 5 Nov (compute-host `study-runs/2026-11-05-one-piece/digest.md`). Their 3D tile stacks corrugated slabs *periodically*, which is the same lesson as here. Also in the library: Resnikoff 2015 (arXiv 1504.06823), not re-read.
- **3D monotiles:** I. Tsiokos, arXiv 2609.19214 (Chair44) and F. Flicker, arXiv 2609.23783 (cited from the 8 Nov record, not re-read today). Both use cubic chair carriers, not close-packed stacking. Also in the library: D. Kamenetsky, arXiv 2610.00916, title only.
- **Close-packed stacking:**
  - Web query "matching rules force aperiodic stacking sequence close-packed layers Fibonacci polytype fcc hcp tiling" found background only: arXiv 1706.07852 (finite-range layer interactions); arXiv 0707.4263 (hybrid close packings); arXiv 2102.08418 (Markov stacking disorder); F. Gähler lecture notes (PIMS) on perfect matching rules and non-local decorations.
  - No source forces a Fibonacci c/h polytype by a single decorated tile.
- **Other web queries:**
  - "Ammann planes three dimensions Fibonacci spacing matching rules Socolar Steinhardt 1986 icosahedral"
  - "Grünbaum Shephard Tilings and Patterns section 10.6 Ammann bars Penrose musical sequence long short Fibonacci" (section number not confirmed)
- **Library grep** (compute-host `~/kaleidohedra-references`, all MANIFEST.json, for Ammann/Socolar/Steinhardt/Grünbaum/Tsiokos/Flicker): the items named above, plus Jagannathan–Duneau 2023 (Ammann–Beenker approximants, not relevant), Levine–Steinhardt 1986, Fu–Steinhardt et al. 2015 (sphere packings in cylinders, not relevant).

## Files

- **Scripts:**
  - `scripts/wave_lib.py`: geometry, signatures, SAT, tori
  - `scripts/scan.py`: design menu and scan
  - `scripts/merge.py`
  - `scripts/followup.py`
  - `scripts/hexrelief.py`: Lemma 2
  - `scripts/forced.py`
  - `scripts/fig_piece.py`
  - `scripts/n_slabs.py`: copy
- **Logs and data:** `data/*.log`, `data/*.json`. Pilot runs: `data/scan-K4-*-pilot.json`. The structure caches (`*.pkl`) stay on compute-host only.

## Ledger line (ready for concordance.json ledger.entries)

```json
{"question": "DICTO 9 Nov: ABC waveform on the surfaces (crests at seats A,B,C, reciprocal underneath, golden mix of waves; Ammann-style phases per orientation) to force aperiodic c/h stacking with ONE Narcissus", "method": "crest planes in Narcissus (6 tilted close-packed families + horizontal, offsets H/6 steps + golden phases; 1944 designs up to symmetry: singles, one- and two-colour pairs, C3/C3v closures); rules STRICT (planes continue) and BEND (crest lines match, lean back); mirror copies yes/no; SAT patch K=5 n=3 + skewed tori index<=3, candidates to n=5/index<=9 and n=7; hexagon-only reliefs exhaustive (165); three lemmas", "status": "SETTLED (closed for the aim in this form)", "result": "7774 runs: 7549 no patch, 213 periodic, 12 candidates all die by n=7 (golden-phase crests: finite-patch artefacts); every filling run admits SSSS or TTTT (none excludes both); word sets only all/SSSS/TTTT (+1 transient). Lemma 1: a golden two-wave relief needs infinitely many phases, one piece shows <=6. Lemma 2: hexagon-only relief couples one pair per interface, words = all words over admitted bits (checked on 165 reliefs). Lemma 3: BEND + mirror copies always admits all-S (h) by mirroring a slab (all 105 such runs confirm). Straight tilted crests (STRICT) force TTTT (keep leaning), periodic", "retry": "never as face/crest decorations of one Narcissus; only a chiral, non-reflection-symmetric key, the vertical-plane (route 4) Ammann system with several pieces, or two slab thicknesses in golden ratio", "study": "2026-11-09-abc-waveform", "date": "2026-11-09"}
```
