# Physical corollaries of the web of bonds (2026-10-25)

This study follows the web-of-bonds study (`../2026-10-25-web-of-bonds/`, paper #52), the physical-anchors study (`../2026-10-25-physical-anchors/`), the scale-anomalies study (`../2026-10-25-scale-anomalies/`), the changeover-evidence study and the relay census. The names of the loops, pieces and stops are the ones used there. **It tests the geometry against measured physics. It is not new physics.** Exact geometry stays exact; every physical number comes from a cited source, with the way it was read recorded in `data/raw/values.json`. Numbers that could not be verified are left out.

## Question

The web of bonds gives the exact area of every shared face ("bond") of the two DICTONIC loops, and the physical-anchors study places real CsCl-type compounds on the golden loop and fluorite-type compounds on the Delian loop (contact model, Shannon radii). **Do any measured physical properties of real crystals depend on these bond-face sizes, so that the bond areas could be tested against data?** Five candidate links were tested:

1. solid-angle / face-weighted coordination numbers (O'Keeffe 1979; Hoppe's ECoN; Blatov's Voronoi–Dirichlet polyhedra);
2. ionic transport in fluorites (superionic transition temperature T_S, anion diffusion activation energy) against the tet–tet face that the anion hop crosses;
3. bond valence (Brown) against contact-face area;
4. elastic anisotropy and the Cauchy relation in CsCl-type crystals against the golden-loop position;
5. contact-face areas in colloids and granular binary sphere packings.

## Method

- **Part G, `scripts/geom.py` (exact cells; solid angles at 40 digits).** Every cell is built from scratch over Q with the web-of-bonds `lib.py` (`power_cell`, `cell_faces`), at rational parameters: golden s = k/40 (k = 0…40, s = x/(1 + x)), Delian t = k/60 (k = 1…59), and the 17 placed compounds under both radius conventions (effective ionic radii IR and crystal radii CR, the anchors study's Shannon values, parameters recomputed exactly and checked against the anchors study). Every face area² is checked exactly against the web-of-bonds closed forms. Solid angles are transcendental: they are evaluated with mpmath at 40 digits from the exact corners (Van Oosterom–Strackee triangle formula), and the faces of every cell must add up to 4π (to 10⁻³⁰). The site is always inside its own cell: each site has a cubic point group that fixes only the site, so the centroid of the (invariant, convex) cell is the site.
  - **O'Keeffe coordination number** N = Σ Ω_i / Ω_max (each face weighted by its solid angle relative to the largest). The original paper could not be read (IUCr pages return 403). This formula was adopted because it reproduces both published values quoted for O'Keeffe's definition: bcc **10.16** (computed 10.16061) and diamond **4.54** (computed 4.53812). These two published values were seen only in a search-engine summary of an IUCr Acta Cryst. B 2019 paper, so they are a sanity check, not evidence.
  - G5 asks which cell contains the midpoint of the ⟨100⟩ anion hop in fluorite (between two neighbouring tet sites), exactly, by minimal power.
- **Part P, `scripts/links.py` (floats).** Spearman rank correlations with **exact permutation p-values** (all n! orderings). Where a measured quantity is a range (two references disagree), every endpoint combination is tried and the range of ρ_S is reported, with the p-value of the most extreme choice.
- **References.** `scripts/crossref_check.py` checks every DOI on api.crossref.org (title, journal, year, volume, pages; `data/raw/crossref.json`). DICTO's library first: five `ask-library` queries (`data/raw/ask-library.txt`) plus keyword search of INDEX.html / README.md / READING-LIST.md for O'Keeffe, coordination number, solid angle, superionic, fluorite, bond valence, Cauchy, elastic constant, Richard, Finney, force chain, ionic conduct. **Nothing relevant was found in the library** (the only hit is the earlier bond-web note on Richards' 1974 method B). Web searches and Crossref queries were then used.
- **Runs.** Part G on dicto-big-brother, `nice -n 10`, load 2.7 at start, 154.9 s. (A duplicate run was started by mistake and stopped before it wrote anything; its output was not used.) Part P and the Crossref check on the Pi, under 2 s.

## Results

### Geometry (part G): solid-angle coordination along the loops

O'Keeffe N per piece (exact cells; values to 4 decimals):

| golden s (x) | N big | N small | big: share of solid angle in big–big faces |
|---|---|---|---|
| 0 (x = 0) | 8 | 9.2444 | 0 |
| 1/4 (1/3) | 8.4915 | 13.8571 | 0.058 |
| 1/2 (Kelvin) | **10.1606** | **10.1606** | 0.213 |
| 3/5 (3/2) | 11.3070 | 9.3197 | 0.292 |
| 3/4 (3) | 13.8571 | 8.4915 | 0.423 |
| 1 (∞) | 9.2444 | 8 | 0.649 |

- N_big(s) = N_small(1 − s) at every sample (the x ↔ 1/x swap).
- N is **not monotone**: it reaches the maximum possible value **14** where a square and a hexagon subtend the same solid angle (then all 14 faces subtend 4π/14 = 2π/7). Float bisection: s* = 0.7565821359, **x* = 3.1081619210** (big piece; the small piece at 1/x*). x* is not one of the named stops, and all five CsCl-type halides lie below it (x = 1.13–2.08 with IR).

| Delian t | N oct | N tet | tet: share of solid angle in tet–tet faces |
|---|---|---|---|
| 1/12 | 12.6765 | 4 | 0 |
| 1/6 | 15.7306 | 4 | 0 |
| 1/4 | 14.2320 | 4 | 0 |
| 1/3 (octet) | **8** | **4** | 0 |
| 2/5 | 8 | 5.0950 | 0.215 |
| 1/2 (unweighted Voronoi) | 8 | 8 | 0.500 |
| 11/20 | 8 | 9.6999 | 0.619 |
| 3/5 | 8 | 8.3456 | 0.719 |
| 2/3 | 8 | 7.2770 | 0.825 |
| 5/6 | 8 | 6.1991 | 0.968 |

At t = 1/3 the O'Keeffe numbers are exactly the chemical coordination numbers 8 and 4 (G2b). For t > 1/3 the oct (cation in fluorite) piece keeps N = 8; the tet piece (anion) gains 6 tet–tet faces and its N rises above the chemical 4.

**Placed compounds** (O'Keeffe N of the two pieces; IR / CR):

| compound | x or t (IR / CR) | N anion | N cation |
|---|---|---|---|
| CsCl | x 1.126 / 0.699 | 10.464 / 9.402 | 9.884 / 11.160 |
| CsBr | x 1.434 / 0.907 | 11.166 / 9.931 | 9.398 / 10.408 |
| CsI | x 2.078 / 1.318 | 12.433 / 10.908 | 8.847 / 9.556 |
| TlCl | x 1.482 / 0.899 | 11.268 / 9.912 | 9.341 / 10.431 |
| TlBr | x 1.910 / 1.165 | 12.126 / 10.556 | 8.954 / 9.809 |
| CaF₂ | t 0.539 / 0.481 | 9.858 / 7.295 | 8 / 8 |
| SrF₂ | t 0.510 / 0.455 | 8.411 / 6.447 | 8 / 8 |
| BaF₂ | t 0.480 / 0.429 | 7.238 / 5.731 | 8 / 8 |
| CdF₂ | t 0.544 / 0.486 | 9.929 / 7.439 | 8 / 8 |
| β-PbF₂ | t 0.504 / 0.450 | 8.159 / 6.295 | 8 / 8 |
| UO₂ | t 0.580 / 0.521 | 8.815 / 8.928 | 8 / 8 |
| ThO₂ | t 0.568 / 0.510 | 9.138 / 8.436 | 8 / 8 |
| CeO₂ | t 0.587 / 0.528 | 8.632 / 9.255 | 8 / 8 |
| ZrO₂ (cubic) | t 0.622 / 0.559 | 7.930 / 9.418 | 8 / 8 |
| Li₂O (anti) | t 0.294 / 0.363 | O: 10.259 / 8 | Li: 4 / 4.434 |
| Na₂O (anti) | t 0.411 / 0.469 | O: 8 / 8 | Na: 5.321 / 6.868 |
| K₂O (anti) | t 0.491 / 0.541 | O: 8 / 8 | K: 7.647 / 9.976 |

(For the antifluorites the anion is on the oct site and the cation on the tet site; the columns give O and the alkali.) The radius convention moves N by up to 2.6 (CaF₂ anion 9.858 → 7.295).

**G5, the anion hop.** For every t > 1/3 the midpoint of the ⟨100⟩ hop between neighbouring tet sites lies on their shared tet–tet face and in no other cell: **the straight vacancy hop crosses exactly the tet–tet bond face**. For t < 1/3 (no tet–tet face) the midpoint lies in two oct cells only, so the straight path leaves the tet cells. Li₂O sits there with IR (t = 0.294) but past the octet with CR (t = 0.363), as found before.

### Link 1. Solid-angle / face-weighted coordination numbers

- Computed exactly along both loops and for all 17 compounds (tables above). Sanity: the formula reproduces the quoted O'Keeffe values for bcc (10.16) and diamond (4.54).
- **The published descriptors cannot test the loop position.** O'Keeffe's N and Blatov's Voronoi–Dirichlet polyhedra use the *unweighted* Voronoi cell of the measured structure. CsCl (B2) and fluorite (C1) have no free atomic coordinates: the measured structure fixes only the lattice constant, which only scales the cells. So the Voronoi cell is the loop piece at equal weights, **s = 1/2 (x = 1, Kelvin) and t = 1/2**, for *every* compound: N = 10.1606 for both ions of every CsCl-type crystal, and N = 8 for both sites of every fluorite (L1b, G4). Hoppe's ECoN is computed from distances, which in these structures also scale with a alone, so it too is the same for every compound of a type (Hoppe 1979 was not read; this follows from the structures alone). The weighted (radical) values in the tables depend on the radii put in, so comparing them with data would be circular.
- No published radical-tessellation coordination numbers for real CsCl-type or fluorite compounds were found.
- **Verdict: undecidable.** No measured, compound-dependent number exists to compare with. The geometry agrees with the two published sanity values.

### Link 2. Ionic transport in fluorites

Data: Fossati, Chartier & Boulle 2021, Table 3 (reference T_S and T_m) and Table 5 (experimental anion diffusion activation energies, normal phase), read in the full text by web fetch. The table layout was garbled in extraction, so row/reference pairing was rebuilt from printed reference numbers (flagged). Values marked DFT were excluded. In every compound the mobile ion sits on the tet (8c) site (F⁻, O²⁻, and Li⁺ in antifluorite Li₂O).

| compound | t (IR) | tet–tet face (app units, IR) | T_S (K) | T_S/T_m | E_a normal phase (eV) |
|---|---|---|---|---|---|
| CaF₂ | 0.539 | 0.2610 | 1430 | 0.843–0.876 | 1.92–3.34 |
| SrF₂ | 0.510 | 0.2296 | 1370–1400 | 0.785–0.813 | 1.81 |
| BaF₂ | 0.480 | 0.1956 | 1275–1300 | 0.783–0.836 | 1.6–2.52 |
| β-PbF₂ | 0.504 | 0.2231 | 711 | 0.630 | 1.04 |
| UO₂ | 0.580 | 0.3014 | 2670 | 0.854 | 2.46–2.57 |
| Li₂O | 0.294 | **none** (t < 1/3) | 1350 | 0.793 | 1.6–2.52 |

Rank correlations, tet–tet area against each measured quantity (exact permutation p of the most extreme choice within the measured ranges):

| sample | vs T_S/T_m | vs E_a (normal) | vs T_S |
|---|---|---|---|
| n = 5 (fluorides + UO₂), IR | ρ_S +0.60 … +0.90, p = 0.083 | 0.00 … +0.90, p = 0.083 | +0.90, p = 0.083 |
| n = 6 (+ Li₂O), IR | +0.49 … +0.77, p = 0.10 | −0.41 … +0.81, p = 0.072 | +0.77, p = 0.10 |
| CR | identical ranks, identical results | | |

- **Equivalence (L2a):** on t ∈ (1/3, 1) the tet–tet area rises strictly with t and the oct–tet area falls strictly. So every rank test with a bond area **is** a rank test with t, that is, with the radius ratio ρ = t/(1 − t). The bond areas add no information beyond the radius ratio here.
- **Direction:** a larger window should make the hop easier (lower E_a, lower T_S/T_m). The data go the other way, or are flat. None of the correlations reaches p < 0.05; at n = 5 the smallest possible two-sided p is 2/120 ≈ 0.017, and the observed best is 0.083. The positive trend rests on β-PbF₂ (smallest homologous T_S; Pb²⁺ is a lone-pair, highly polarisable cation, a property the hard-sphere geometry does not contain) and on UO₂ (charge 4+/2−; energies scale with charge, not with the dimensionless face).
- Li₂O has no tet–tet face under IR yet is a superionic conductor (T_S = 1350 K): if the face were the necessary "window", this would be a counterexample. Under CR it has a tiny one (0.044). Its placement is convention-dependent (scale-anomalies study), so it decides nothing.
- **Verdict: no supported link** (small samples, n = 5–6; not significant; the sign is opposite to the window picture; the test reduces to the radius ratio). The geometric statement G5 (the hop crosses the tet–tet face exactly when t > 1/3) holds, but it is geometry, not a data test.

### Link 3. Bond valence against contact-face area

- In CsCl and fluorite every cation–anion bond of an ion is symmetry-equivalent, so Brown's valence-sum rule fixes the bond valence exactly: s = V/N = 1/8 (Cs–X, Tl–X), 1/4 (M²⁺–F, and A⁺–O in A₂O), 1/2 (M⁴⁺–O). This is the same at every loop position: the model has nothing to correlate with the loop parameter within a structure type.
- Like-ion contacts carry valence 0 in the bond-valence model, but they take a large share of the cell surface:

| type | anion like-face share of its cell surface (IR) |
|---|---|
| CsCl-type halides (big–big) | 0.245 (CsCl) … 0.354 (CsI) |
| fluorites (tet–tet), excl. ZrO₂ | 0.527 (BaF₂) … 0.736 (CeO₂); ZrO₂ 0.785 |

In every placed fluorite **more than half of the anion's radical-cell surface faces other anions** (L3a), so "bond valence ∝ face area" is contradicted for like contacts.
- Unlike faces in the fluorites (contact-model areas in Å²) against valence: ρ_S = −0.87 (n = 9, valence takes only two values: 1/4 fluorides, 1/2 dioxides). The higher-valence bonds have the *smaller* faces, because the 4+ cations are smaller; the bond-valence model already explains this through bond length (shorter, stronger bonds). The face area adds nothing.
- A published correlation of Voronoi face solid angle with internuclear distance exists (Ge–C contacts, a Russ. J. Phys. Chem. A 2023 paper, seen only in a search summary; not used). No published correlation of radical face area with bond valence was found.
- **Verdict: no link** (valences symmetry-fixed; like faces large with zero valence).

### Link 4. Elastic anisotropy and the Cauchy relation (CsCl type)

Verified elastic constants exist here for only two of the five halides: Vallin, Beckman & Salama 1964 (abstract), at 4.2 K, in 10¹⁰ N/m².

| | x (IR / CR) | c₁₁ | c₁₂ | c₄₄ | c₁₂ − c₄₄ | c₁₂/c₄₄ | Zener A = 2c₄₄/(c₁₁ − c₁₂) |
|---|---|---|---|---|---|---|---|
| CsBr | 1.434 / 0.907 | 3.437 | 1.035 | 0.999 | +0.036 | 1.036 | 0.832 |
| CsI | 2.078 / 1.318 | 2.737 | 0.793 | 0.825 | −0.032 | 0.961 | 0.849 |

- Both are within 4 % of the Cauchy relation. The Cauchy discrepancy changes sign between them, but two points cannot carry a correlation.
- CsCl (Slagle & McKinstry 1967: the abstract has no numbers), TlCl (Kodama, Saito & Minomura 1972: page 403, no abstract) and TlBr (Solid State Commun. 1967: no abstract) could not be read; their values are left out.
- **Verdict: undecidable** (n = 2).

### Link 5. Colloid and granular evidence

- Richard, Oger, Troadec & Gervois 1998 (Physica A 259, 205): radical tessellation of *random* binary sphere assemblies (packing fractions up to about 0.60; topological and metric deviations from a random froth). Read only as the abstract in a search summary of its IDEAS/RePEc page. It concerns disordered packings, not CsCl/fluorite lattices, and no face-area-versus-contact-force data were found.
- Gellatly & Finney 1982: the radical tessellation of multi-size sphere models (metadata only; used as prior art for the construction).
- Leunissen et al. 2005 (CsCl-type ionic colloidal crystals): metadata only; no published radical-face areas or contact statistics were found.
- One Crossref query and one web search found no paper relating radical face areas to force chains or contact statistics in an ordered binary crystal.
- **Verdict: undecidable** (data missing).

### Summary

| link | verdict | numbers |
|---|---|---|
| 1. O'Keeffe / ECoN / VDP coordination | **undecidable**: published values are structure constants (Voronoi = equal weights: x = 1, t = 1/2) for every compound | sanity PASS: bcc 10.16, diamond 4.54 reproduced; weighted N tabulated exactly |
| 2. fluorite transport (T_S, E_a) vs tet–tet face | **no supported link** | ρ_S +0.49 … +0.90, p ≥ 0.072, n = 5–6; sign opposite to the window picture; equivalent to radius ratio |
| 3. bond valence vs face area | **no link** | valences fixed by symmetry; anion like faces 25–35 % (CsCl type) and 53–78 % (fluorites) of the surface with valence 0 |
| 4. elastic / Cauchy (CsCl type) | **undecidable** | only CsBr, CsI verified (n = 2) |
| 5. colloids / granular | **undecidable** | no ordered-crystal face-area or contact data found |

**Strongest supported link: none.** The nearest is a geometric fact, not a correlation with data: in fluorite the straight anion vacancy hop crosses exactly the tet–tet bond face whenever t > 1/3 (G5), so the tet–tet face is the right geometric "window". But the measured transport data (n = 5–6) do not follow its size. The reason underlying all five links is the same: CsCl and fluorite have no free structural parameter, so every measured structural descriptor is the same for all compounds of a type, and every bond area along a loop is a monotone function of the one radius ratio that was put in.

## PASS / FAIL

| part | checks | PASS | FAIL |
|---|---|---|---|
| G geometry (`data/checks/geom-checks.txt`): published bcc/diamond values, 82 golden + 118 Delian + 68 compound cells exact (areas = closed forms, 4π, site list), swap, octet, equal-weight points, hop | 10 | 10 | 0 |
| P links (`data/checks/links-checks.txt`): equal-solid-angle point, Voronoi constants, area monotonicity, test bookkeeping, like-face shares, elastic sample size | 7 | 7 | 0 |
| **total** | | **17** | **0** |

The cell-level checks inside G cover 268 cells (each must pass every exact test for its line to PASS).

## Sources

All DOIs were checked on api.crossref.org (title, journal, year, volume, pages; `data/raw/crossref.json`).

| reference | DOI | used for | read as |
|---|---|---|---|
| M. O'Keeffe, Acta Cryst. A35 (1979) 772–775, *A proposed rigorous definition of coordination number* | 10.1107/S0567739479001765 | link 1 definition | not read (IUCr 403); formula fixed by reproducing the quoted 10.16 / 4.54 |
| IUCr Acta Cryst. B 2019 paper (journals.iucr.org/b/issues/2019/01/00/lo5042) | — | the quoted O'Keeffe values bcc 10.16, diamond 4.54 | search summary only (secondary; sanity check only) |
| R. Hoppe, Z. Kristallogr. 150 (1979) 23–52, ECoN and MEFIR | 10.1524/zkri.1979.150.1-4.23 | link 1 | metadata only |
| V. A. Blatov, Crystallogr. Rev. 10 (2004) 249–318, Voronoi–Dirichlet polyhedra | 10.1080/08893110412331323170 | link 1 | metadata only |
| P. C. M. Fossati, A. Chartier, A. Boulle, Front. Chem. 9 (2021) 723507 | 10.3389/fchem.2021.723507 | link 2: T_S, T_m (Table 3), E_a (Table 5), H_f (Table 4, context) | full text (web fetch; table pairing rebuilt, flagged) |
| I. D. Brown, D. Altermatt, Acta Cryst. B41 (1985) 244–247 | 10.1107/S0108768185002063 | link 3 (bond-valence model) | metadata only; only the valence-sum rule is used |
| I. D. Brown, Chem. Rev. 109 (2009) 6858–6919 | 10.1021/cr900053k | link 3 | metadata only |
| J. Vallin, O. Beckman, K. Salama, J. Appl. Phys. 35 (1964) 1222–1223 | 10.1063/1.1713597 | link 4: CsBr, CsI c_ij at 4.2 K | abstract (Crossref) |
| W. C. Slagle, H. A. McKinstry, J. Appl. Phys. 38 (1967) 451–458 | 10.1063/1.1709358 | link 4 (CsCl) | abstract; no numbers in it |
| Kodama, Saito, Minomura, J. Phys. Soc. Jpn. 33 (1972) 1361–1371 (TlCl) | 10.1143/JPSJ.33.1361 | link 4 | metadata only (403) |
| Solid State Commun. 5 (1967), TlBr elastic constants | 10.1016/0038-1098(67)90019-1 | link 4 | metadata only |
| P. Richard, L. Oger, J.-P. Troadec, A. Gervois, Physica A 259 (1998) 205–221 | 10.1016/S0378-4371(98)00323-9 | link 5 | abstract via search summary (IDEAS/RePEc) |
| B. J. Gellatly, J. L. Finney, J. Non-Cryst. Solids 50 (1982) 313–329 | 10.1016/0022-3093(82)90093-X | link 5, construction | metadata only |
| M. E. Leunissen et al., Nature 437 (2005) 235–240 | 10.1038/nature03946 | link 5 | metadata only |
| R. D. Shannon, Acta Cryst. A32 (1976) 751–767 | 10.1107/S0567739476001551 | radii (via the anchors study) | transcription (as in the anchors study) |

**Left out (could not be verified):** the elastic constants of CsCl, TlCl and TlBr; isolated vacancy-migration enthalpies (only total diffusion activation energies were read); any published radical-tessellation coordination number of a real compound; any contact-force statistics of ordered binary colloidal crystals; the T_S of ThO₂ and CeO₂ (not in Fossati et al.).

## Files

- `scripts/geom.py`: part G; writes `data/raw/geom.json` and `data/checks/geom-checks.txt`.
- `scripts/links.py`: part P; writes `data/raw/links.json` and `data/checks/links-checks.txt`.
- `scripts/crossref_check.py`: writes `data/raw/crossref.json`.
- `scripts/run.sh`: reruns everything.
- `data/raw/values.json`: every external number, its source and reading level.
- `data/raw/ask-library.txt`: the five library queries.
