# Changeover evidence in real crystals (2026-10-25)

This study follows the Relay Census (`../2026-10-25-relay-census/`), Physical Anchors (`../2026-10-25-physical-anchors/`) and Scale Anomalies (`../2026-10-25-scale-anomalies/`) studies. "Flip", "hinge", "soft/hard relay" and "relay census" are the working names from those studies; DICTO decides the names. **This is a test of geometry against known crystal chemistry. It is not new physics or chemistry.** Exact geometry is exact (sympy); every physical number is cited, and the way each source was read is recorded.

## Question

The census walks give, for each crystal network, exact weights λ = w_A − w_B where the radical (power) faces change: flips, hinges and named stops. With weight = r² + C (Physical Anchors), a weight is a statement about sphere sizes. **Do real compounds change structure (or bond type) where these stops say, once the stops are turned into radius ratios?**

1. Contact map ρ(λ) for each census network; every flip, hinge and named stop as a radius ratio.
2. Known changeovers and their published size boundaries (Pauling 0.225 / 0.414 / 0.732; B1 ↔ B2 in alkali halides with transition pressures; zinc blende / wurtzite ↔ rock salt; Laves √(3/2) and observed range; A15; Goldschmidt t).
3. Real compounds placed; do known changeovers coincide with stops, sit near them, or not? Gaps against the ±0.14 Å radius-convention shift.
4. Verdict per network.

## Method

- **`scripts/geometry.py`** (sympy, exact). Imports the census site sets (`../2026-10-25-relay-census/scripts/networks.py`) and reads its `relay-summary.json` and `perovskite.json`.
  - G1 contact map. With unlike neighbours touching, r_A + r_B = d (d = unlike nearest distance from the site sets) and r_A² − r_B² = λ, so **ρ = r_A/r_B = (d² + λ)/(d² − λ)** and r_A − r_B = λ/d. Regressions: the golden map (x + 2)/(2x + 1) and the Delian map t/(1 − t) of Physical Anchors.
  - G2 like-contact (touching) window: λ ∈ [(d − ℓ_B)d, (ℓ_A − d)d], ℓ = like nearest distances. Checked against Pauling's limits.
  - G3 a general fact, checked per network: when two like spheres touch in a non-overlapping packing, the contact point has power 0 for both and positive power for every other sphere, so their radical face exists (with an open neighbourhood). **So a Pauling contact limit always lies strictly inside the life of the like bond; no flip can coincide with a contact limit of the same network.**
  - "Max-packing" map: the lattice fixed, radii in ratio ρ scaled up to the first contact of any kind. It reduces to the contact map inside the window and to like-contact outside; each stop is solved exactly on every branch.
  - C15 and A15 like-contact models; hcp-hole site identification (exact coset/neighbour checks); perovskite walls in Goldschmidt coordinates (t, μ_oct = r_B/r_X).
- **`scripts/compounds.py`**: real compounds with Shannon radii (IR and CR) from the Imperial College transcription (`data/raw/shannon-db/`, 29 element pages fetched 2026-10-25; the 19 pages from Physical Anchors were copied, 10 new). **Same caveat as Physical Anchors: values as transcribed, not checked against the printed table.** Halide and S/Se/Te anion radii exist only for CN VI and are used as proxies for other CN.
- **`scripts/crossref_check.py`**: every DOI looked up on api.crossref.org (16/16 match title, journal, volume, year).
- **Runs.** dicto-big-brother, `nice -n 10`, load 0.00–0.01, one job at a time: geometry 4.9 s, compounds < 1 s. Crossref on the Pi.

## Results

### Q1. Stops as radius ratios (contact map; exact)

ρ = r_A/r_B with the census's own A, B. "Window" = unlike contact with like spheres not overlapping (Pauling's geometry).

| network (A, B; d²) | touching window in ρ | stop (λ) | ρ at the stop (exact) | inside window? |
|---|---|---|---|---|
| CsCl (big, small; 3) | [√3 − 1, (√3 + 1)/2] = [0.732, 1.366] | flips −1, +1 | **1/2, 2** | no — reached only by rattling packings (max-packing map has no positive solution) |
| | | named 0 (Kelvin), ±(2√2 − 1) (uniform truncated cubic) | 1; 3√2 − 4 = 0.243, 2 + 3√2/2 = 4.12 | only ρ = 1 |
| NaCl (Na, Cl; 1) | [√2 − 1, √2 + 1] = [0.414, 2.414] | **hinge 0** | **1** | yes |
| | | named ±(4 − 2√3) (all edges equal) | (4√3 − 3)/13 = 0.302; 1 + 4√3/3 = 3.31 | no |
| zinc blende (Zn, S; 3) | [√(3/2) − 1, 2 + √6] = [0.225, 4.449] | flips −1, +1 | **1/2, 2** | yes |
| fluorite / Delian (tet, oct; 3/8) | [√(3/2) − 1, (√3 + 1)/2] | **hinge −1/8 (octet)** | **1/2** | yes |
| | | named √6/10 − 21/40, 7/8 − √2/2 | (√6 − 1)/10 = 0.145; (1 + 3√2)/2 = 2.62 | no |
| hcp holes (tet, oct; 3/8) | **the single point λ = −1/8, ρ = 1/2** (both like pairs touch there) | flip −1/8 (gyrated octet) | 1/2 | yes (it *is* the window) |
| | | flip 5/24 | 7/2 | no |
| | | lower end −11/24 | — (|λ| > d²: no contact radii) | no |
| A15 (Si = B-site, Cr = A-site; 5/4) | [√5 − 1, (3 + √15)/2] = [1.236, 3.44] | flips 1/4, 3/4 | **3/2, 4** | 3/2 yes; 4 no |
| C15 (Mg, Cu; 11) | **empty**: √11 > √3 + √2, unlike spheres cannot touch without like overlap | flips −5, 7, 9 | 3/8, 9/2, 10 (formal) | — |

Exact consequences:
- The Pauling limits come out as window ends in every ionic network (G2 PASS): 0.732 (CsCl), 0.414 (NaCl), 0.225 (zinc blende, fluorite).
- **No flip or hinge equals a Pauling limit** (G3, strict). The flips sit at ρ = 1/2, 1, 2 (CsCl, zinc blende, fluorite, NaCl, hcp), not at 0.225/0.414/0.732.
- CsCl and zinc blende have the same d² = 3 and the same flips, hence the same flip ratios 1/2 and 2. The fluorite hinge and the gyrated-octet flip are also at ρ = 1/2.
- hcp holes: the touching window collapses to the gyrated octet itself (oct–oct along c and tet–tet across the shared face touch at the same λ = −1/8).
- **C15 (Laves):** in ideal Laves the unlike pair does *not* touch; the right model is like contact. With both like pairs touching, r_Mg/r_Cu = √(3/2) and λ = 1. Under max packing (Cu–Cu contact for ratio ≤ √(3/2), Mg–Mg above) λ stays in (−2, 3) for **every** ratio, so the flips −5, 7, 9 are unreachable.
- **A15:** with Cr chains and Cr–Si both touching, r_Si/r_Cr = √5 − 1 ≈ 1.236 and λ = (5 − 2√5)/4. The flip 1/4 (Si–Si faces born) is at r_Si/r_Cr = √2 (chain contact) or 3/2 (unlike contact); the flip 3/4 at 2 or 4.
- **hcp holes, which real structures?** (G7, exact) The census "oct" sites are the octahedral holes of an ideal hcp (6 atoms at distance² 1/2) and the "tet" sites its tetrahedral holes (4 atoms at 3/8). The hcp atoms themselves are the missing third kind. NiAs puts cations on all the oct sites (anions on the hcp atoms, tet sites empty); wurtzite puts cations on one tet site of each face-sharing pair (anions on the hcp atoms, oct sites empty). The oct set is simple hexagonal (nearest distance² 2/3 along c), not hcp, so the network is not a hexagonal fluorite either. **No real two-kind structure with exactly these two site sets was found; the census oct–tet contact is hole-to-hole, not cation–anion.**
- **Perovskite walls in Goldschmidt coordinates** (radii relative to r_X; lattice fixed by B–X contact for t ≤ 1, A–X for t ≥ 1):
  - λ = 0 (A–A faces born) ⇔ **r_A = r_X** ⇔ **t = √2/(1 + μ_oct)** (scale-free);
  - λ + 2μ = 0 (A–B faces born) ⇔ r_A² + 2r_B² = 3r_X² ⇔ t = (1 + √(3 − 2μ_oct²))/(√2(1 + μ_oct)) (scale-free);
  - λ + μ = 1 (X–X faces die): t = (1 + √(3 + 2μ_oct))/(√2(1 + μ_oct)) with B–X contact, (2 + √(6 − 2μ_oct²))/(√2(1 + μ_oct)) with A–X contact.
  - The ideal all-touching perovskite (μ_oct = √2 − 1, t = 1) lies on the A–A wall. For μ_oct in [0.35, 0.65] the A–B and X–X walls lie at t > 1 (1.27 and 2.13 at μ_oct = 0.45), outside the perovskite range t ≤ 1. The A–B wall reaches t ≈ 1.01 only at μ_oct = 0.70.

| μ_oct | t on A–A wall | t on A–B wall | t on X–X wall |
|---|---|---|---|
| 0.40 | 1.010 | 1.332 | 2.214 |
| √2 − 1 | **1.000** | 1.315 | 2.189 |
| 0.45 | 0.975 | 1.273 | 2.129 |
| 0.50 | 0.943 | 1.217 | 2.048 |
| 0.60 | 0.884 | 1.109 | 1.899 |
| 0.70 | 0.832 | 1.007 | 1.764 |

(The X–X column is the A–X-contact form; exact values in `data/raw/geometry.json`.)

- **Convention invariance (G9, exact).** The IR → CR shift (cation +0.14 Å, anion −0.14 Å; confirmed on 7 ions, C0) leaves d = r₊ + r₋ and Goldschmidt t unchanged, but moves λ by 2δd and changes every ratio ρ and μ_oct.

### Q2. Known changeovers and size boundaries (cited)

| changeover | published boundary / data | source (how read) |
|---|---|---|
| Pauling radius-ratio rule | 0.225 / 0.414 / 0.732 (derived exactly here as window ends) | Pauling 1929 (not re-read); George et al. 2020 (full text): **rule 1 agrees with only 66 % of ~5000 oxide environments** |
| B1 ↔ B2 alkali halides, ambient | all alkali halides NaCl type except CsCl, CsBr, CsI | Weir & Piermarini 1964 (full text) |
| B1 → B2 under pressure | KI 1.785, KBr 1.805, KCl 1.968, RbI 0.397, RbBr 0.451, RbCl 0.490 GPa (Bridgman's measurements); KF ≈ 2.0, RbF ≈ 1.18, CsF ≈ 2.0 GPa (their estimates) | Weir & Piermarini 1964, Table 2 (read from the page image; 10⁹ dyn/cm² = 0.1 GPa; data from Bridgman 1945) |
| | NaCl about 30 GPa | Xu et al. 2024 (full text, arXiv version), citing Bassett et al. 1968 |
| wurtzite → rock salt | CdSe ≈ 2.5, CdS ≈ 2.5–3.2, ZnS ≈ 12 GPa (experimental values quoted) | Grünwald, Geissler & Rabani 2012 (full text, secondary for the experiments) |
| tetrahedral vs rock salt, ambient | ZB: Be/Zn/Cd chalcogenides, Cu halides; wurtzite: ZnO, CdS, CdSe, AgI; RS: Mg/Ca/Sr/Ba chalcogenides, CdO | Wikipedia "Cubic crystal system", "Wurtzite crystal structure" (fetched 2026-10-25; **secondary, general knowledge**) |
| Laves AB₂ | ideal r_A/r_B = 1.225; observed **1.05–1.68** | Costa, de Almeida & Paixão, Portgal. Phys. 21 (1992) 31 (full text; no DOI) |
| | hard-sphere Laves for diameter ratio 1.19–1.35 | Lindquist, Jadrich & Truskett 2018 (full text), citing Hynninen et al. 2007 |
| A15 | **no published radius-ratio stability range found**; Stewart 2015 (full text) gives none; Geller 1956 CN-12 radii not available | — |
| perovskite | 0.8 ≤ t ≤ 1: perovskites form, tilts in the lower part; t > 1 A too large; μ_oct > 0.41 | Travis et al. 2016 (full text); Li, Soh & Wu 2004 via Travis (163/192 ABO₃ classified) |
| | SrTiO₃ cubic at room T (t ≈ 1.00); BaTiO₃ t ≈ 1.06, cubic → tetragonal at ≈ 393 K; CaTiO₃ orthorhombic Pnma (tilts) | Pai et al. 2018, Amoroso, Cano & Ghosez 2018 (full texts, arXiv versions) |

### Q3. Real compounds against the stops

**Alkali halides (20; IR, cation and anion CN VI; CR as check).** ρ = small/large.

| | ρ (IR) | ρ (CR) | ambient | P(B1→B2), GPa |
|---|---|---|---|---|
| LiF, LiCl, LiBr, LiI | 0.571, 0.420, 0.388, 0.346 | 0.756, 0.539, 0.495, 0.437 | B1 | — |
| NaF, NaCl, NaBr, NaI | 0.767, 0.564, 0.520, 0.464 | 0.975, 0.695, 0.637, 0.563 | B1 | NaCl ≈ 30 |
| KF, KCl, KBr, KI | 0.964, 0.762, 0.704, 0.627 | 0.783, 0.910, 0.835, 0.738 | B1 | ≈2 (est.), 1.968, 1.805, 1.785 |
| RbF, RbCl, RbBr, RbI | 0.875, 0.840, 0.776, 0.691 | 0.717, 0.994, 0.912, 0.806 | B1 | ≈1.18 (est.), 0.490, 0.451, 0.397 |
| CsF, CsCl, CsBr, CsI | 0.796, 0.923, 0.852, 0.759 (Cs VIII: 0.764, 0.961, 0.888, 0.791) | 0.658, 0.923, 0.995, 0.879 | B1, **B2, B2, B2** | CsF ≈ 2 (est.) |

- Pauling's 0.732 (= the CsCl window edge) classifies **13/20 (IR) and 11/20 (CR)**; misfits (IR): NaF, KF, KCl, RbF, RbCl, RbBr, CsF. This is the known failure of the radius-ratio rule for alkali halides.
- The census CsCl flip at ρ = 1/2 is not a B1/B2 separator at all (7/20 IR, 5/20 CR if used as one). Every B2 compound sits in the soft chamber (1/2, 1], but so do 13 of the 17 B1 compounds.
- NaCl hinge at ρ = 1: KF, RbF, CsF have the cation larger (Na–Na-type faces), all the others the anion larger. All are B1: **no structural change at the hinge.**
- Transition pressure against ρ (6 measured K and Rb halides): Spearman −0.03, i.e. no rank relation. Within each family the pressure *rises* with ρ (KI < KBr < KCl; RbI < RbBr < RbCl), the opposite of "closer to 0.732, easier B2". The pressures group by cation (Rb ≈ 0.4–0.5, K ≈ 1.8–2.0, Na ≈ 30 GPa), not by any census ratio.

**AB tetrahedral (ZB/W, 14) vs rock salt (10).** ρ = r₊/r₋; four radius conventions. Count of compounds classified correctly (RS if ρ ≥ threshold):

| radii | Pauling 0.414 | census zinc-blende flip **1/2** | best single threshold |
|---|---|---|---|
| IR, actual CN (IV tetrahedral, VI rock salt) | 19/24 (wrong: ZnO, CdS, AgI, MgS, MgSe) | **22/24** (wrong: MgS, MgSe) | 22/24, any threshold in (0.455, 0.514] |
| IR, all cations CN VI | 16/24 | 19/24 | 21/24 at 0.543 |
| CR, actual CN | 17/24 | 19/24 | 22/24 at 0.671 |
| CR, all CN VI | 13/24 | 15/24 | 21/24 at 0.671 |

- With IR and actual CN, the empirical boundary between the last tetrahedral compound (AgI 0.455) and the first rock-salt oxide (MgO 0.514) brackets **1/2**, not 0.414. Gap of the flip to Pauling's 0.414: 0.086 in ρ.
- But the IR → CR shift moves these ratios by 0.08–0.22, i.e. more than that gap, and under CR the best boundary moves to ≈ 0.67. The "actual CN" rows also use the known structure to pick the radius. **So the coincidence holds in one convention only.**

**Titanate perovskites (A XII, Ti⁴⁺ VI, O²⁻ VI).**

| | t (IR = CR) | μ_oct IR / CR | r_A/r_X IR / CR | side of the A–A wall (λ = 0) IR / CR | room-T structure |
|---|---|---|---|---|---|
| CaTiO₃ | 0.966 | 0.432 / 0.591 | 0.957 / 1.175 | **no A–A faces** / A–A faces | orthorhombic, tilted |
| SrTiO₃ | 1.002 | 0.432 / 0.591 | 1.029 / 1.254 | A–A faces / A–A faces | cubic |
| BaTiO₃ | 1.062 | 0.432 / 0.591 | 1.150 / 1.389 | A–A faces / A–A faces | tetragonal (cubic above ≈ 393 K) |

- With IR the A–A wall (t = 0.988 at μ_oct = 0.432) falls between tilted CaTiO₃ (t = 0.966) and cubic SrTiO₃ (t = 1.002): a gap of 0.014 in t to SrTiO₃. With CR it moves to t = 0.889 and all three are on the same side. t itself is convention-free; the wall is not.
- All three lie on the "no A–B faces" side (λ + 2μ < 0) in both conventions, and far from the X–X wall.

**Laves (C15).** No per-compound metallic radii were verified, so no compound is placed. The published ranges map, under max packing, to λ ∈ [0.205, 1.937] (observed 1.05–1.68) and [0.832, 1.354] (hard-sphere 1.19–1.35): all inside the census chamber (−5, 7), and the flips are unreachable at any ratio.

**A15.** Not placed: no verified radii and no published ratio range.

### Q4. Verdict per network

| network | census stops as ρ | nearest known boundary | gap | verdict |
|---|---|---|---|---|
| CsCl (B2) | flips 1/2, 2 | B1/B2 at Pauling 0.732 (window edge) | 0.23 in ρ | **unrelated**. The flips are reachable only by rattling packings. The B1/B2 boundary is Pauling's contact limit (known geometry) and fails for 7/20 halides anyway. P(B1→B2) shows no relation to ρ |
| NaCl (B1) | hinge 1 | Pauling 0.414; B1/B2 0.732 | 0.59; 0.27 | **unrelated**. Compounds on both sides of ρ = 1 are all B1 |
| zinc blende | flips 1/2, 2 | tetrahedral ↔ rock salt; Pauling 0.414 | 0.086 to Pauling; 1/2 is *inside* the empirical gap (0.455, 0.514] with IR | **near, convention-dependent**: coincides with IR (22/24 vs 19/24 for 0.414) but not with CR (best ≈ 0.67); the gap is smaller than the convention shift (0.08–0.22) |
| fluorite (Delian) | hinge 1/2 | no structural changeover found at ρ_anion/cation or ρ_cation/anion = 1/2; Li₂O straddles it (Physical Anchors) | — | **undecidable from data** |
| hcp holes | flip 1/2 (= the whole touching window), 5/24 → 7/2 | none (hole sites, not ions) | — | **undecidable / not applicable** |
| A15 | flips 3/2 or √2 (1/4), 4 or 2 (3/4) | none published found | — | **undecidable from data** |
| C15 Laves | flips unreachable | observed 1.05–1.68, ideal √(3/2) | stops never reached | **unrelated**: the whole physical range is one chamber |
| perovskite | A–A wall t = √2/(1 + μ_oct) | cubic vs tilted near t ≈ 1 | 0.014 in t (IR); wall moves to 0.889 under CR | **near, (b) known, convention-dependent**: r_A = r_X is the close-packed AX₃ condition, and the ideal t = 1 lies on the wall. A–B and X–X walls (t ≥ 1.1 for μ_oct ≤ 0.6) unrelated |
| 2D square / honeycomb / kagome | — | — | — | skipped: no real two-kind 2D family on these exact sites with unlike contact was found |

**What known rules explain (verdict (b)).**
- Every Pauling limit is a census window end, i.e. a contact condition, and by G3 never a flip.
- The perovskite A–A wall at r_A = r_X is the classical close-packed AX₃ picture (Travis et al.: "a cubic close packed AX3 array"), and the ideal t = 1 lies on it.

**Coincidence not explained by the known rules found here.**
- The zinc-blende flip ρ = 1/2 separates tetrahedral from rock-salt AB compounds with Shannon IR (22/24) better than Pauling's 0.414 (19/24).
- At this flip the cation's radical cell stops being its bare coordination tetrahedron (cation–cation faces appear).
- Pauling's geometry does not give 1/2, and no source read here states a 1/2 boundary. The known explanation of the 0.414 misfits is covalency (ionicity scales), not a size ratio. Phillips's ionicity was not read here.
- **This is weak evidence:** the structure labels are secondary, the IR/CR shift is larger than the gap, and the best threshold moves to 0.67 with CR radii.

## PASS / FAIL

| part | PASS | FAIL |
|---|---|---|
| G geometry (contact maps, windows, G3 theorem per network, stops, C15/A15 models, hcp identification, perovskite walls, convention invariance) | 49 | 0 |
| C compounds (convention shift on 7 ions, regressions, placements, monotonic-pressure finding, perovskite sides) | 15 | 0 |
| Crossref (16 DOIs: title, journal, volume, year) | 16 | 0 |
| **total** | **80** | **0** |

Check lists: `data/checks/geometry-checks.txt`, `compounds-checks.txt`, `crossref-checks.txt`.

## Sources

DICTO's library first: 5 `ask-library` queries and a keyword search of INDEX.html / README.md / READING-LIST.md (`data/raw/ask-library.txt`). Only George et al. 2020 (and the Pauling and Shannon entries) were relevant; nothing on B1/B2, Laves, A15 or perovskite. Then web search.

| reference | DOI (Crossref-checked) | read |
|---|---|---|
| R. D. Shannon, Acta Cryst. A32 (1976) 751 | 10.1107/S0567739476001551 | via the Imperial College transcription |
| L. Pauling, JACS 51 (1929) 1010 | 10.1021/ja01379a006 | not re-read |
| C. E. Weir, G. J. Piermarini, J. Res. NBS 68A (1964) 105 | 10.6028/jres.068A.009 | full text |
| W. A. Bassett et al., J. Appl. Phys. 39 (1968) 319 | 10.1063/1.1655752 | not read (cited by Xu et al.) |
| F. Xu et al., Appl. Phys. Lett. 125 (2024) | 10.1063/5.0231544 | full text, arXiv:2209.10899 |
| J. George et al., Angew. Chem. Int. Ed. 59 (2020) 7569 | 10.1002/anie.202000829 | full text (library) |
| W. Travis et al., Chem. Sci. 7 (2016) 4548 | 10.1039/C5SC04845A | full text |
| C. Li, K. C. K. Soh, P. Wu, J. Alloys Compd. 372 (2004) 40 | 10.1016/j.jallcom.2003.10.017 | secondary (via Travis) |
| V. M. Goldschmidt, Naturwiss. 14 (1926) 477 | 10.1007/BF01507527 | not read |
| Y.-Y. Pai et al., Rep. Prog. Phys. 81 (2018) 036503 | 10.1088/1361-6633/aa892d | full text, arXiv:1702.07690 |
| D. Amoroso, A. Cano, Ph. Ghosez, PRB 97 (2018) 174108 | 10.1103/PhysRevB.97.174108 | full text, arXiv:1801.08886 |
| M. Grünwald, P. L. Geissler, E. Rabani, J. Chem. Phys. 136 (2012) | 10.1063/1.4729468 | full text, arXiv:1201.2992 |
| B. A. Lindquist, R. B. Jadrich, T. M. Truskett, J. Chem. Phys. 148 (2018) | 10.1063/1.5028279 | full text, arXiv:1803.03327 |
| A.-P. Hynninen et al., Nat. Mater. 6 (2007) 202 | 10.1038/nmat1841 | not read |
| S. Geller, Acta Cryst. 9 (1956) 885 | 10.1107/S0365110X56002515 | not read |
| G. R. Stewart, Physica C 514 (2015) 28 | 10.1016/j.physc.2015.02.013 | full text, arXiv:1505.06393 |
| M. M. R. Costa, M. J. M. de Almeida, J. A. Paixão, Portgal. Phys. 21 (1992) 31 | none | full text (spf.pt PDF) |
| Wikipedia, "Cubic crystal system", "Wurtzite crystal structure" | — | fetched 2026-10-25; secondary |
| Imperial College *Database of Ionic Radii*, abulafia.mt.ic.ac.uk/shannon | — | pages saved in `data/raw/shannon-db/` |

**Left out (unverified):**
- metallic radii for Laves and A15 compounds;
- transition pressures for Li and Na halides other than NaCl, and for ZnO;
- the "cubic perovskite for 0.9 < t < 1" bands (not found in a source read);
- MgTe (its ambient structure is not settled in the sources read).

## Limits

- Hard spheres, contact model: as in Physical Anchors, a power diagram fixes only r_A² − r_B², and the ratio needs a contact assumption.
- Radii are CN-VI proxies for the halides and chalcogenides.
- A threshold fitted on 24 compounds with secondary labels is not evidence of a rule.

## Files

- `scripts/geometry.py`: part G. Writes `data/raw/geometry.json` and `data/checks/geometry-checks.txt`.
- `scripts/compounds.py`: part C. Writes `data/raw/compounds.json` and `data/checks/compounds-checks.txt`. Literature values are inline, each with its source.
- `scripts/parse_shannon.py`: turns `data/raw/shannon-db/*.html` into `data/raw/shannon.json`.
- `scripts/crossref_check.py`: writes `data/raw/crossref.json` and `data/checks/crossref-checks.txt`. `scripts/crossref_find.py`: the DOI lookup helper.
- `data/raw/ask-library.txt`: the library queries.
- `scripts/run.sh`: reruns G and C on dicto-big-brother.
