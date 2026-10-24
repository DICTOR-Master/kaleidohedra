# Scale anomalies of the physical anchors (2026-10-25)

This study follows up the Physical Anchors study (`../2026-10-25-physical-anchors/`), which built on Bond Relay (`../2026-10-25-bond-relay/`). It **tests the model's inputs**: the radii and the conditions they hold for. It is not new physics. Exact geometry stays exact (sympy). Every physical number is an **estimate**, and is labelled as one.

## Question

The DICTONIC loops are exact power diagrams of the CsCl (golden) and fluorite (Delian) structures. Under the contact model:
- golden: ρ = (x + 2)/(2x + 1);
- Delian: ρ = t/(1 − t).

The touching windows end exactly at Pauling's limits. Three compounds fall outside, using Shannon's effective ionic radii (IR):

| compound | ρ | window edge | gap in ρ |
|---|---|---|---|
| UO₂ | 1.3800 | (√3 + 1)/2 ≈ 1.3660 | 1.02 % |
| CeO₂ | 1.4227 | (√3 + 1)/2 | 4.15 % |
| cubic ZrO₂ | 1.6429 | (√3 + 1)/2 | 20.27 % |

The gap is measured as (ρ − edge)/edge. Measured as a fraction of ρ instead, the gaps are 1.01 %, 3.98 % and 16.9 %. The brief quoted 1.1 %, 4.0 % and 20.5 %, which are close to these but not identical.

Li₂O lies on one side of the octet stop (t = 1/3, ρ = 1/2) or the other, depending on the radius convention.

DICTO asked what could explain these misfits: gravity, pressure, temperature, slow cooling, or less accurate reference data. The study asks seven questions:
1. Error bars.
2. Pressure.
3. Temperature.
4. Slow cooling, metastability and nonstoichiometry.
5. Gravity.
6. Covalency.
7. A verdict for each misfit.

## Method

**`scripts/anomalies.py`** (sympy + floats). It runs on dicto-big-brother with `nice -n 10`, at load 0.8, in 1.6 s. It reads the anchors study's `shannon.json` and `compounds.json`. It recomputes every ρ and asserts that each one equals the anchors value.
- **E: exact.** Window edges and the octet stop as surds.
- **Q1: required radius changes (exact).** For every compound, the exact radius each ion would need to put it on the nearest window edge, and (Delian) on the octet stop. Each ion is moved alone, and also both ions together by equal relative amounts. These are compared with:
  - IR vs crystal radii (CR);
  - the other coordination-number (CN) entries;
  - the 0.005 Å rounding of the tabulated values;
  - the CN VI stand-in for halides;
  - the additivity residual r⁺ + r⁻ − d against measured lattice constants.
  - A second placement is also computed from the measured lattice: t = ½ + (8/3)(r_tet² − r_oct²)/a². This uses the power-diagram weight alone, with no contact assumption.
- **Q2: pressure (estimate).** Third-order Birch–Murnaghan with the published K₀, and K₀′ = 4 assumed. The bond shortening is split between the ions in three ways:
  - H, homothetic: ρ does not change;
  - A, anion takes all of it (the bound most favourable to entering the window);
  - C, cation takes all of it.
- **Q3: temperature (estimate).** UO₂ expansion from the IAEA table, and the superionic temperatures.
- **Q4: radius averaging (Vegard-type estimate).** Mixed-valence and doped compositions.
- **Q5: gravity (estimate).** Built from exact-defined constants.
- **`scripts/crossref_check.py`**: checks every DOI on api.crossref.org. It also finds DOIs by title, and a match is accepted only if the title agrees (`data/raw/crossref.json`).
- **`data/raw/values.json`**: every external number, with its source and how it was read:
  - *text*: read in a saved full text or table;
  - *abstract*: read in the publisher's abstract;
  - *secondary*: from a search summary only, so not used in the conclusions;
  - *unverified*: not used.

**Library first.** `ask-library` was run with 4 queries: Shannon accuracy, fluorite under pressure, superionic fluorites, and Pauling's rules. INDEX.html was searched by keyword. The library has only *link-only* catalogue entries for Shannon 1976 and Pauling 1929, added by the anchors study. It has no PDFs and nothing on pressure, temperature or superionics.

## Results

### Q1. Error bars: how far each radius must move

Each "needed" shift moves one ion alone onto the nearest edge. All radii are Shannon IR in Å.

**Misfits and Li₂O:**

| compound | edge | cation alone | anion alone | both (equal %) | IR→CR ρ | other CN choices | ±0.005 Å rounding band |
|---|---|---|---|---|---|---|---|
| UO₂ | tet–tet contact | **+0.0102 Å (+1.02 %)**: U⁴⁺ ≥ 1.38(√3 − 1) = 1.0102 | **−0.0140 Å (−1.01 %)**: O²⁻ ≤ (√3 + 1)/2 = 1.3660 | 0.51 % each | 1.088 (in) | O CN VI 1.400, CN VIII 1.420 (further out) | 1.368–1.392 (still out) |
| CeO₂ | tet–tet contact | +0.0402 Å (+4.15 %) | −0.0550 Å (−3.98 %) | 2.0 % each | 1.117 (in) | 1.443 / 1.464 (further out) | 1.410–1.435 (out) |
| ZrO₂ (cubic) | tet–tet contact | +0.170 Å (+20.3 %) | −0.233 Å (−16.9 %) | 9.2 % each | 1.265 (in) | 1.667 / 1.690 (out) | 1.627–1.659 (out) |
| Li₂O | octet ρ = ½ | Li⁺ +0.120 Å (+20.3 %) | O²⁻ −0.240 Å (−16.9 %) | 9.2 % each | **0.570 (past the octet)** | Li CN VI: **0.535 (past)**; O CN IV/VI 0.428/0.421 (not past) | 0.411–0.421 (not past) |

**All other compounds.** The table gives each compound's margin to its nearest edge.

| compound | nearest edge | margin | cheapest single-ion move |
|---|---|---|---|
| CsCl | like contact √3 − 1 | 31 % | Cs⁺ −0.42 Å |
| CsBr | like contact √3 − 1 | 21 % | Cs⁺ −0.31 Å |
| TlCl | like contact √3 − 1 | 20 % | Tl⁺ −0.27 Å |
| TlBr | like contact √3 − 1 | 11 % | Tl⁺ −0.16 Å |
| CsI | like contact √3 − 1 | 8.0 % | Cs⁺ −0.13 Å |
| CaF₂ | tet–tet contact | 14 % | — |
| SrF₂ | tet–tet contact | 24 % | — |
| BaF₂ | tet–tet contact | 32 % | — |
| CdF₂ | tet–tet contact | 13 % | Cd²⁺ −0.14 Å |
| β-PbF₂ | tet–tet contact | 26 % | — |
| ThO₂ | tet–tet contact | **3.8 %** | Th⁴⁺ −0.040 Å, or O²⁻ +0.054 Å |
| Na₂O | — | in window | — |
| K₂O | — | in window | — |

Two further notes on the other compounds:
- **Octet side.** Every Delian compound except Li₂O is at least 39 % from the octet (Na₂O 39 %; the others 84 % or more).
- **Halide CN VI stand-in.** A labelled estimate scales the anion radius by O²⁻'s own CN VI→VIII ratio (1.42/1.40). This moves every halide about 1.4 % towards the edge, and all of them stay inside.

**What the data can support:**
- **Shannon's own stated accuracy: not verified.** The full text of Shannon 1976 could not be read. IUCr/Wiley returned 403 before, and today the WIPP copy refused the connection. No number for it is used here.
  - Usable instead: the tabulation step of 0.01 Å, giving a ±0.005 Å half-unit.
  - Also usable: Shannon's reliability keys (R, C, E, ?, *, …), from the database footnote. For the misfits: U⁴⁺ VIII is "R*" and Ce⁴⁺ VIII is "R" (from r³-vs-V plots). Zr⁴⁺ VIII and Li⁺ IV are "*" (most reliable). O²⁻ has no key.
- **Additivity residual against measured lattices.** This is an empirical error bar.
  - UO₂, a = 5.47127 Å (Leinders 2015): r⁺ + r⁻ − d = **+0.011 Å**.
  - CeO₂, a = 5.411102 Å (NIST SRM 674a): **+0.007 Å**.
  - In both, Shannon's sum is slightly too long. The O–O overlap 2r(O²⁻) − a/2 is 0.024 Å (0.89 %) for UO₂ and 0.054 Å (2.0 %) for CeO₂.
- **Measured-lattice placement.** This uses no contact assumption, and it also leaves both outside: t = 0.5806 (UO₂) and 0.5878 (CeO₂), against 1/√3 = 0.5774. So **the misfit is a property of the radii, not of the contact model.**
- **Convention spread.** IR→CR moves every cation by +0.14 Å and every anion by −0.14 Å. This shifts ρ by 21–23 % in the dioxides and by 37 % in Li₂O, which dwarfs every other effect here. It puts all three misfits inside, and it moves Li₂O past the octet.

### Q2. Pressure (estimates; K₀′ = 4 assumed)

- **Exact point.** In CsCl and fluorite every atom sits on a special position, so compression is homothetic: all lengths scale by the same factor. With equal radius scaling (model H), **ρ does not depend on pressure at all**. Pressure can move ρ only if the anion and the cation compress by different relative amounts. No per-ion compressibility was verified, so only bounds are given.

| compound | K₀ (source) | dρ/dP, anion-only (A) | dρ/dP, cation-only (C) | P to reach the edge, model A | known transition (source) |
|---|---|---|---|---|---|
| UO₂ | 207 GPa (Idiri 2004) | −0.0038 /GPa (−0.28 %/GPa) | +0.0053 /GPa (moves out) | **3.8 GPa** (V/V₀ = 0.982) | cotunnite type, sluggish; still cubic at 69 GPa in that run (Idiri 2004) |
| CeO₂ | 230 GPa (Duclos 1988) | −0.0035 /GPa (−0.25 %/GPa) | +0.0050 /GPa (moves out) | **18.9 GPa** (V/V₀ = 0.931) | → α-PbCl₂-like Pnam at 31.5 ± 1.0 GPa (Duclos 1988) |
| ThO₂ (control, inside) | 198 GPa (Idiri 2004) | moves further in | +0.0051 /GPa | under C, it *leaves* the window at 10.9 GPa | cotunnite type (Idiri 2004) |
| Li₂O | 90 ± 1 GPa (Lazicki 2006) | +0.0022 /GPa (+0.52 %/GPa) | moves away | **73.9 GPa > 50 GPa** transition | → anticotunnite at 50 ± 5 GPa (Lazicki 2006) |

- **EoS check.** BM3 with K₀ = 230 GPa gives V/V₀ = 0.896 for CeO₂ at 31.5 GPa. Duclos 1988 gives about 0.89 as the transition volume of these dioxides. The two agree to within 0.01.
- **Direction.** Pressure can bring UO₂ and CeO₂ inside only if the O²⁻ ion takes most of the compression. Even under that most favourable bound, the needed pressures are 3.8 and 18.9 GPa. The observed fluorite → cotunnite transitions go to a higher cation coordination. That fits a rising r⁺/r⁻ under pressure, but this is an interpretation and was not checked against a source.
- **Li₂O cannot be pushed across the octet by pressure**, because it changes structure first.
- **Pressure cannot explain an ambient misfit.** Shannon's radii are fitted to ambient (≈ 1 atm) structures, so ambient conditions are already built into them.

### Q3. Temperature (estimates)

- **UO₂ expansion.** The linear expansion from 293 K is **3.39 % at the superionic λ transition (2670 K)** and **4.67 % at melting (3120 K)**. The uncertainty is 7 % of ΔL/L above 1400 K. Source: IAEA-TECDOC-1496 Table 1, recommending Martin 1988.
- **Homothetic expansion (H)** leaves ρ unchanged, as with pressure.
- **Rigid ions** (ambient radii kept, measured lattice expanding): heating UO₂ to about **1170 K** would remove its 0.89 % O–O overlap. This is a bound only, because real radii also change with temperature.
  - One XAS study reports that the local U–O distance *shrinks* with temperature (P. M. Martin et al., an HZDR record). No journal DOI was found on Crossref, so it is unverified and not used.
- **Superionic (Bredig/Faraday) transition.** The temperatures below are reference values quoted in Fossati, Chartier & Boulle 2021, Table 3.
  - Values: CaF₂ 1430 K, SrF₂ 1370–1400 K, BaF₂ 1275–1300 K, β-PbF₂ 711 K, Li₂O 1350 K, UO₂ 2670 K.
  - Above these temperatures, "the X sublattice is expected to be highly disordered", Frenkel pairs form, and the lattice parameter rises anomalously.
  - The anion (tet-site) hard sphere then has no fixed site. So **the model does not apply above T_S at all**: there is no ρ to shift.
- **Temperature also cannot explain an ambient misfit**, for the same reason as pressure.

### Q4. Slow cooling, metastability and nonstoichiometry (radius averages are Vegard-type estimates)

- **β-PbF₂ (in window, 26 % margin).**
  - The fluorite form made by heating α-PbF₂ does not revert on cooling. It is metastable at ambient, and milling returns it to α. Source: Dénès & Madamba 1997, read from a search summary only (secondary).
  - So the β placement describes a kinetically trapped form. The radii are the same in both forms, so ρ itself does not change. What changes is which structure is actually present.
- **Cubic ZrO₂.**
  - Pure monoclinic ZrO₂ has Zr seven-coordinated. Source: McCullough & Trueblood 1959, DOI verified, abstract read only via a secondary summary.
  - In Y-doped cubic zirconia, the charge-compensating O vacancies sit preferentially next to Zr, and Y keeps 8-fold coordination (Li, Chen & Penner-Hahn 1993, abstract).
  - Radius averaging alone would need a **Ca²⁺ cation fraction of 0.61** (Ca²⁺ VIII = 1.12 Å) to reach the window. That is not a dilute dopant.
  - So the model's 8:4 input (Zr in CN VIII, O in CN IV) does not describe the stabilised material: **the real Zr environment is under-coordinated.**
- **CeO₂₋ₓ.**
  - Ce³⁺ VIII = 1.143 Å, compared with Ce⁴⁺ VIII = 0.97 Å. Reaching the window by the mean cation radius needs x ≈ **0.116** (CeO₁.₈₈). This ignores the vacancies.
  - The measured CeO₂ standard (NIST 674a) is the stoichiometric oxide, so reduction does not explain its ambient misfit.
- **UO₂₊ₓ.**
  - Oxidation makes the cation smaller: U⁵⁺ VII = 0.84 Å (CN VII used as a stand-in), and U⁶⁺ VIII = 0.86 Å. The mean cation at x = 0.13 is 0.958–0.982 Å, so ρ moves **further out**.
  - The excess O sits as interstitials displaced from the empty octahedral 4b sites (Wang, Ewing & Becker 2014). The model has no site for these.
  - Leinders 2015 attributes its higher, stoichiometric lattice constant mainly to avoiding hyperstoichiometry. So older a-values for "UO₂" may be biased low.

### Q5. Gravity (estimates, exact constants)

| quantity | value |
|---|---|
| UO₂ density from a and formula mass (4 formula units per cell) | 10.95 g/cm³ |
| pressure at the base of a 1 cm / 1 m / 1 km column of UO₂ | 1.07 kPa / 107 kPa / 107 MPa |
| elastic strain P/(3K₀), the same three heights | 1.7 × 10⁻⁹ / **1.7 × 10⁻⁷** / 1.7 × 10⁻⁴ |
| gravitational / Coulomb force between U⁴⁺ and O²⁻ (independent of distance) | **3.8 × 10⁻³⁴** |
| UO₂ column whose own weight gives the 3.8 GPa of Q2 (model A) | 35 km |
| the same, as a depth in rock of assumed density 3300 kg/m³ (estimate) | ≈ 117 km |

- **Gravity in a crystal on a table:** a 1 m crystal is strained by its own weight about 10⁻⁷. That is about 10⁻⁵ of the 1 % that UO₂ needs. **Gravity is negligible**, except as the source of geological pressure at depths of order 100 km. Q2 already covers that, and there the bound is the most favourable one.

### Q6. Covalency and polarizability: where hard-sphere radius ratios fail

- **George et al. 2020** (Angew. Chem. Int. Ed. 59, 7569; DOI Crossref-verified; full text read):
  - Over about 5000 oxides, only **66 %** of the tested local environments agreed with Pauling's first rule (using Pauling's univalent radii).
  - They link the failure to the assumption that a cation has only one environment.
  - They note that Shannon radii depend on the environment, "and cannot be used for local-environment prediction".
  - Only 13 % of the oxides satisfy rules 2–5 together.
- **Shannon 1976 abstract** (as reproduced in the search results):
  - Radius additivity is affected by polyhedral distortion, partial occupancy, covalence and metallic character.
  - Covalence shortens bonds, with smaller effects for Zn²⁺, Cd²⁺, In³⁺, Pb²⁺ and Tl⁺.
- **For this study:** the UO₂ and CeO₂ misfits (1–4 %) are far smaller than the scatter George et al. report for the rule itself. They are also smaller than the IR/CR convention shift.

### Q7. Verdict per misfit

| compound | needed shift | compared with | verdict |
|---|---|---|---|
| **UO₂** (out by 1.0 %) | +0.010 Å on U⁴⁺, or −0.014 Å on O²⁻ | additivity residual +0.011 Å (Leinders lattice); 2× the rounding half-unit; CR puts it inside | **Within data error.** The radii cannot place it on either side of the edge at the 0.01 Å level. No physical effect is needed. |
| **CeO₂** (out by 4.2 %) | +0.040 Å on Ce⁴⁺, or −0.055 Å on O²⁻ | about 6× the additivity residual (0.007 Å) and 8× the rounding; the measured-lattice placement keeps it out; CR puts it inside; pressure would need ≥ 18.9 GPa even in the most favourable bound | **Not within IR numerical error. Explained only by the radius convention** (IR vs CR) and by the known limits of hard-sphere ratios (Q6). No named physical effect (P, T, g, stoichiometry) explains it at ambient. **Unexplained by physics; an input-convention effect.** |
| **cubic ZrO₂** (out by 20 %) | +0.170 Å on Zr⁴⁺ | not stable undoped; dopant O vacancies sit next to Zr, so Zr is not 8-coordinated (Li 1993); radius averaging would need 61 % Ca | **Explained by a named effect: defect chemistry.** The model's 8:4 input does not describe the real material. |
| **Li₂O** (octet side) | +0.12 Å on Li⁺, or −0.24 Å on O²⁻ | IR→CR (±0.14 Å) and Li CN VI both cross the octet; pressure cannot (73.9 GPa needed, above the 50 GPa transition) | **Within the convention spread: undecidable from the radii.** Not a physical anomaly. |

**Biggest effect found.** The radius convention (IR vs CR, ±0.14 Å per ion) shifts ρ by 21–37 %. That is larger than every physical effect. Among the physical effects, the largest is defect chemistry in stabilised zirconia. Pressure gives at most about 0.3 %/GPa, and only in the bound most favourable to entering the window. Gravity gives at most about 10⁻⁷ for a 1 m crystal.

## PASS / FAIL

`data/checks/anomalies-checks.txt`

| part | checks | PASS | FAIL |
|---|---|---|---|
| E exact edges | octet ↔ ρ = ½; (√3 + 1)/2 = 1/(√3 − 1); the golden lower edge equals the inverted Delian upper edge | 3 | 0 |
| Q1 error bars | misfit set; the exact UO₂ condition; CR puts all three inside; Li₂O straddles; measured-lattice placement also out; additivity residual < 0.02 Å | 8 | 0 |
| Q2 pressure | homothetic → no change; bound below the transitions; cation-only moves out; Li₂O needs more than its transition pressure; EoS sanity against Duclos | 5 | 0 |
| Q3 temperature | expansion to T_S from the IAEA table; rigid-ion window temperature | 2 | 0 |
| Q4 metastability | CeO₂₋ₓ x ≈ 0.12; UO₂₊ₓ moves out; Ca fraction > 0.5 | 3 | 0 |
| Q5 gravity | density sanity; own-weight strain < 10⁻⁶; F_g/F_C < 10⁻³⁰ | 3 | 0 |
| **total** | | **24** | **0** |

## Sources

Every DOI below was checked on api.crossref.org: the title, journal, year, volume and pages match (`data/raw/crossref.json`). How each one was read is recorded in `data/raw/values.json`.

| reference | DOI | used for | read as |
|---|---|---|---|
| R. D. Shannon, Acta Cryst. A32 (1976) 751–767 | 10.1107/S0567739476001551 | the radii (via the Imperial College transcription) and the reliability keys | transcription and abstract; **stated accuracy not verified** |
| L. Pauling, JACS 51 (1929) 1010–1026 | 10.1021/ja01379a006 | the radius-ratio rule | (anchors study) |
| J. George et al., Angew. Chem. Int. Ed. 59 (2020) 7569–7575 | 10.1002/anie.202000829 | the 66 % / 13 % figures; why rule 1 fails | full text (PMC7217010) |
| G. Leinders et al., J. Nucl. Mater. 459 (2015) 135–142 | 10.1016/j.jnucmat.2015.01.029 | UO₂ a = 547.127 ± 0.008 pm | abstract |
| NIST SRM 674a certificate (1989), Table 3 | — | CeO₂ a = 5.411102 Å (information value) | text |
| M. Idiri et al., PRB 70 (2004) 014113 | 10.1103/PhysRevB.70.014113 | K₀ of UO₂ (207 GPa) and ThO₂ (198 GPa); transitions | abstract |
| S. J. Duclos et al., PRB 38 (1988) 7755–7758 | 10.1103/PhysRevB.38.7755 | CeO₂ K₀ = 230 GPa; 31.5 GPa transition; V/V₀ ≈ 0.89 | abstract |
| A. Lazicki et al., PRB 73 (2006) 184120 | 10.1103/PhysRevB.73.184120 | Li₂O K₀ = 90 GPa; 50 GPa transition | abstract |
| IAEA-TECDOC-1496 (2006) | — | UO₂ ΔL/L table; λ transition at 2670 K; melting at 3120 K | text (excerpt saved) |
| D. G. Martin, J. Nucl. Mater. 152 (1988) 94–101 | 10.1016/0022-3115(88)90315-7 | the source of the IAEA recommendation | not read directly |
| M. T. Hutchings, J. Chem. Soc. Faraday Trans. 2, 83 (1987) 1083 | 10.1039/F29878301083 | neutron confirmation of the 2670 K transition (as cited by IAEA) | not read directly |
| P. C. M. Fossati, A. Chartier, A. Boulle, Front. Chem. 9 (2021) 723507 | 10.3389/fchem.2021.723507 | T_S and T_m; anion disorder above T_S | full text (web fetch) |
| J. Wang, R. C. Ewing, U. Becker, Sci. Rep. 4 (2014) 4216 | 10.1038/srep04216 | interstitial O near the octahedral 4b sites in UO₂₊ₓ | full text (PMC3958918) |
| P. Li, I-W. Chen, J. E. Penner-Hahn, PRB 48 (1993) 10074–10081 | 10.1103/PhysRevB.48.10074 | O vacancies next to Zr in YSZ | abstract |
| J. D. McCullough, K. N. Trueblood, Acta Cryst. 12 (1959) 507–511 | 10.1107/S0365110X59001530 | monoclinic ZrO₂ with CN 7 (context only) | secondary summary |
| G. Dénès, M. C. Madamba, MRS Proc. 481 (1997) 673 | 10.1557/PROC-481-673 | β-PbF₂ metastable at ambient (context only) | secondary summary |

**Left out (could not be verified):**
- Shannon's own stated numerical accuracy.
- The CaF₂ transition at 9.5 GPa (Gerward 1992; Dorfman 2010): secondary only, and no Crossref match was found for Dorfman.
- The CaF₂ and CeO₂ thermal-expansion coefficients.
- The "negative local thermal expansion" of UO₂ (no DOI).
- Li₂O and ThO₂ lattice constants. The additivity check was done only for UO₂ and CeO₂.

## Files

- `scripts/anomalies.py`: everything above. Writes `data/raw/anomalies.json` and `data/checks/anomalies-checks.txt`.
- `scripts/crossref_check.py`: writes `data/raw/crossref.json`.
- `scripts/run.sh`: reruns everything (Crossref on the Pi, the analysis on dicto-big-brother).
- `data/raw/values.json`: every external number, with its source and how it was read.
- `data/raw/sources/`: `george2020-pmc.txt` and `wang2014-pmc.txt` (full texts from PMC), `iaea-tecdoc-1496-excerpt.txt` (UO₂ expansion and the λ transition), `nist-srm-674a-table3.txt` (the CeO₂ lattice parameter).
