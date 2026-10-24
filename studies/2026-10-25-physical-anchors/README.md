# Physical anchors for the DICTONIC loops (2026-10-25)

This study extends the web-of-bonds study (`../2026-10-25-web-of-bonds/`). The names of the loops, solids and stops are the ones used in papers #48 and #51, in the app and in web of bonds. This study gives **physics anchors for the geometry**. It is not new physics. All the crystal chemistry used here is standard.

## Question

The web-of-bonds study proved that both DICTONIC loops are power diagrams of fixed sites:
- **golden:** w_big − w_small = (φ²/4)(x − 1)/(x + 1) on the bcc sites φZ³ and φZ³ + (φ/2)(1,1,1);
- **Delian:** w_tet − w_oct = (3/8)(2t − 1) on (Z + ½)³/√2 and the odd integer points /√2.

This study asks five questions:
1. Is the weight the squared sphere radius of a radical (Laguerre) tessellation of spheres? What radius ratio ρ belongs to each x and each t? Which ρ are physically possible, and where do the stops fall?
2. Are the golden sites the CsCl (B2) structure, and are the Delian sites the fluorite (C1) structure? Which site is which ion, and how does the lattice constant map to app units?
3. Where do real compounds sit on the loops, using Shannon (1976) radii? For each one: ρ, x or t, the bonds and the bond areas.
4. How does this compare with known crystal chemistry (Pauling's radius-ratio rule, neighbour shells)?
5. What is the prior art: binary colloidal crystals, and radical tessellation in crystal chemistry?

## Method

- **Part A, `scripts/symbolic.py` (sympy, exact, whole parameter ranges).**
  - A1: weight equals radius².
  - A2: golden map.
  - A3: non-overlap feasibility for any radii, not only touching ones.
  - A4: Delian map.
  - A5: stops.
  - A6: structure identification (exact coset comparison with B2 Wyckoff 1a/1b and fluorite 4a/8c).
  - A7: area identity.
- **Part B, `scripts/compounds.py` (exact over Q, cells built from scratch).** This part uses the web of bonds `lib.py` and `samples.py`, imported and not copied. The radical tessellation is built with weight = r² itself, not only the weight difference.
  - B0 known cases: equal spheres on bcc give the Kelvin truncated octahedron; equal spheres on fcc give the rhombic dodecahedron.
  - B1: rational loop stops as touching packings.
  - B2: every compound, with Shannon radii converted to Fractions. The checks are that the cell equals the app's piece, the bond counts, and the bond areas against the web of bonds closed forms.
  - B3: the contact window equals Pauling's 8-coordination limit, for every compound.
- **Radii.** `scripts/parse_shannon.py` reads the saved pages in `data/raw/shannon-db/` into `data/raw/shannon.json`. The pages were fetched on 2026-10-25 from the Imperial College *Database of Ionic Radii*, http://abulafia.mt.ic.ac.uk/shannon/, which states that all of its data are taken from Shannon, Acta Cryst. A32 (1976) 751–767. The printed table could not be downloaded (IUCr and Wiley returned 403), so **the values are Shannon's as transcribed by that database and have not been checked against the printed page.** The main values use the effective ionic radii (IR). The crystal radii (CR) are kept as a sensitivity check.
- **References.** `scripts/crossref_check.py` looks up every cited DOI on api.crossref.org and writes `data/raw/crossref.json`. `data/raw/ask-library.txt` holds the four `ask-library` queries. INDEX.html, README.md and READING-LIST.md were also searched by keyword.
- **Runs.** All runs were on dicto-big-brother with `nice -n 10`, at load < 0.1. A took 2.4 s and B took 45 s.

## Results

### Q1. Weight = radius², and the maps ρ(x), ρ(t)

**Theorem (standard; A1).**
- The radical plane of two spheres (c_i, r_i) and (c_j, r_j) is the set where |p − c_i|² − r_i² = |p − c_j|² − r_j².
- This is exactly the power-diagram bisector with w = r² + C, for any common constant C (A1a).
- The bisector is the plane 2p·(c_j − c_i) = |c_j|² − |c_i|² + w_i − w_j. It depends on the weights only through w_i − w_j (A1b).
- On a connected adjacency graph, the faces therefore fix every weight up to one common C. The exception is the Delian ends t = 0 and t = 1, where the vanishing kind's cell is a point and its weight is only bounded.
- So the radical tessellation of a sphere packing is the power diagram with **w = r² (+ C)**, and a power diagram fixes the radii only up to r_i² → r_i² + C.
- Two further facts:
  - For touching spheres, the radical plane passes through the contact point (A1c).
  - For non-overlapping spheres, each sphere lies in its own cell. Proof: if q is on sphere i, then |q − c_j| ≥ r_i + r_j − r_i = r_j, so pow_j(q) ≥ 0 ≥ pow_i(q).

**Consequence.** A loop parameter fixes only r_big² − r_small² (or r_tet² − r_oct²). Fixing ρ needs one more physical condition. The natural one is the radius-ratio picture: **unlike neighbours touch**, so r_1 + r_2 equals the unlike nearest distance d. Then r_1 − r_2 = Δ/d, and:

| loop | contact map (one line) | inverse | d (app units) |
|---|---|---|---|
| golden | **ρ = r_small/r_big = (x + 2)/(2x + 1) = (2 − s)/(1 + s)** | x = (2 − ρ)/(2ρ − 1) | (√3/2)φ, with cube edge a = φ |
| Delian | **ρ = r_tet-site/r_oct-site = t/(1 − t)** | t = ρ/(1 + ρ) = r_tet/d | √6/4, with octet edge 1 |

Some exact consequences:
- r_big/d = (1 + s)/3 and r_small/d = (2 − s)/3 (A2d).
- In the Delian loop, **t is the fraction of the unlike bond taken by the tet-site sphere**.
- x ↔ 1/x sends ρ ↔ 1/ρ (A2c).
- dρ/dx = −3/(2x + 1)² (A2g).

**What is physically possible (A2, A3, A4).** Here "possible" means that the spheres do not overlap. The like neighbours are at a = φ (golden), at 1 (Delian oct–oct) and at 1/√2 (Delian tet–tet).

| | golden | Delian |
|---|---|---|
| touching window (unlike in contact, like not overlapping) | x ∈ [(√3 − 1)/2, √3 + 1] ≈ [0.366, 2.732], ρ ∈ [√3 − 1, (√3 + 1)/2] ≈ [0.732, 1.366] | t ∈ [1 − √(2/3), 1/√3] ≈ [0.1835, 0.5774], ρ ∈ [√(3/2) − 1, (√3 + 1)/2] ≈ [0.2247, 1.366] |
| window ends | the like spheres touch. **ρ = √3 − 1 is Pauling's 0.732 limit for 8-coordination** | at t = 1 − √(2/3) the oct spheres touch (**√(3/2) − 1 = Pauling's 0.225 limit for 4-coordination**); at t = 1/√3 the tet spheres touch (1/ρ = √3 − 1, the 0.732 limit again) |
| any non-overlapping packing (not necessarily touching) | **every x ∈ [0, ∞]**, because \|Δ\| ≤ (a/2)² always (A3g) | **only t ∈ [1/6, 2/3]** (A4f) |
| packings outside the window (largest ρ) | x ≥ √3 + 1: ρ ≤ √(2/(x + 1)) (big spheres touch, small ones rattle); x ≤ (√3 − 1)/2: by the swap | t ∈ [1/6, 1 − √(2/3)]: ρ ≤ √((6t − 1)/2); t ∈ [1/√3, 2/3]: ρ ≥ 1/√(4 − 6t) |

The proof for the general packings (A3) uses u = r_1 + r_2. Then r_{1,2} = (u ± Δ/u)/2. Both radii increase with u, and ρ moves monotonically towards 1. So the feasible u form an interval, and the interval is nonempty exactly when the larger radius √|Δ| (with the other radius 0) fits.

**Stops (A5).**

| stop | ρ (contact map) | in touching window? | any packing? |
|---|---|---|---|
| golden x = 0 | 2 | no | yes, only one: small spheres touching on a simple cubic lattice, big sites points |
| golden x = 1 (Kelvin) | 1, which is forced (Δ = 0: equal spheres) | yes | yes |
| golden x = τ (= φ, as in the code) | √5/φ² = (3√5 − 5)/2 ≈ 0.8541 | yes | yes |
| golden x = ∞ | 1/2 (map) | no | yes, only one: big spheres touching on a simple cubic lattice, small sites points (ρ = 0) |
| Delian t = 0 | 0 | no | **no** |
| Delian t = 1/6 | — | no | yes, the end case: touching fcc spheres, tet sites points |
| Delian octet t = 1/3 | **1/2** | yes | yes |
| Delian bond t = 1 − (2/3)·2^(−1/3) ≈ 0.4709 | **(3/2)·2^(1/3) − 1 ≈ 0.8899** | yes | yes |
| Delian t = 1/2 (unweighted Voronoi) | 1 | yes | yes |
| Delian t = 2/3 | — | no | yes, the end case: touching simple-cubic spheres on the tet sites, oct sites points |
| Delian t = 1 | ∞ | no | **no** |

### Q2. Structures: confirmed exactly (A6)

**Golden = CsCl (B2, Pm-3m).**
- φZ³ is Wyckoff position 1a and φZ³ + (φ/2)(1,1,1) is position 1b, with **a = φ in app units**.
- The unlike nearest distance is (√3/2)a and the like nearest distance is a.
- The two sites are equivalent, so either ion can sit on "big". This study puts the larger ion on big, so ρ ≤ 1 and x ≥ 1. The x ↔ 1/x swap exchanges the two.
- A real crystal of lattice constant a_real maps to app units by lengths × φ/a_real.

**Delian = fluorite (C1, Fm-3m).** Shift the sites by (1,0,0)/√2.
- The oct sites become fcc 4a and the tet sites become 8c (¼,¼,¼): all the tetrahedral holes. The lattice constant is **a = √2 in app units**.
- The octet edge 1 is the cation–cation distance a/√2. The cation–anion distance is (√3/4)a = √6/4, and the anion–anion distance is a/2 = 1/√2.
- **Fluorite (CaF₂):** the cation is on the oct sites (8-coordinated by anions) and the anion is on the tet sites (4-coordinated).
- **Antifluorite (Li₂O):** the two are swapped: the anion is on the oct sites and the cation on the tet sites.
- Real lengths map to app units by × √2/a_real.

Caution on names: in the app, the "oct" pieces sit on the 8-coordinated fcc sites, and the "tet" pieces sit on the 4-coordinated tetrahedral holes.

### Q3. Compounds placed (contact model; Shannon 1976 effective ionic radii)

How to read the tables:
- All radii are in Å, from Shannon (1976) via the Imperial College transcription, for the CN shown. The key is Shannon's reliability flag.
- **CsCl-type halides: Shannon gives Cl⁻, Br⁻ and I⁻ only for CN VI**, so the CN VI value is used as a proxy for the true CN VIII. This is flagged in every row.
- The areas are the web of bonds closed forms, in app units (golden L = φ; Delian octet edge 1). They were verified in B2 from cells built with w = r².
- Every B2 row also passed this check: the radical cell is exactly the app's piece at that x or t.

**CsCl type (golden)**: in every row the larger ion (anion) is on the big site, and the bonds are 8 big–small + 6 big–big per big piece and 8 big–small + 6 small–small per small piece.

| compound | r(cation) CN | r(anion) CN | ρ | x (exact) | big–small | big–big | small–small | window |
|---|---|---|---|---|---|---|---|---|
| CsCl | Cs⁺ 1.74 VIII | Cl⁻ 1.81 VI (proxy; key P) | 0.9613 | 188/167 ≈ 1.126 | 0.8492 | 0.3671 | 0.2897 | in |
| CsBr | Cs⁺ 1.74 VIII | Br⁻ 1.96 VI (proxy; key P) | 0.8878 | 109/76 ≈ 1.434 | 0.8412 | 0.4544 | 0.2209 | in |
| CsI | Cs⁺ 1.74 VIII | I⁻ 2.20 VI (proxy; key A) | 0.7909 | 133/64 ≈ 2.078 | 0.8155 | 0.5966 | 0.1382 | in |
| TlCl | Tl⁺ 1.59 VIII (key R) | Cl⁻ 1.81 VI (proxy) | 0.8785 | 203/137 ≈ 1.482 | 0.8396 | 0.4666 | 0.2125 | in |
| TlBr | Tl⁺ 1.59 VIII (key R) | Br⁻ 1.96 VI (proxy) | 0.8112 | 233/122 ≈ 1.910 | 0.8225 | 0.5639 | 0.1546 | in |

**Fluorite and antifluorite (Delian).** For t > 1/3, oct piece = 8 oct–tet, and tet piece = 4 oct–tet + 6 tet–tet. For t < 1/3, oct piece = 12 oct–oct + 8 oct–tet, and tet piece = 4 oct–tet.

| compound | oct site (CN 8) | tet site (CN 4) | ρ = r_tet/r_oct | t | side of octet | oct–tet | like bond | window |
|---|---|---|---|---|---|---|---|---|
| CaF₂ | Ca²⁺ 1.12 (key *) | F⁻ 1.31 | 1.1696 | 0.5391 | > 1/3 | 0.2070 | tet–tet 0.2610 | in |
| SrF₂ | Sr²⁺ 1.26 | F⁻ 1.31 | 1.0397 | 0.5097 | > 1/3 | 0.2342 | tet–tet 0.2296 | in |
| BaF₂ | Ba²⁺ 1.42 | F⁻ 1.31 | 0.9225 | 0.4799 | > 1/3 | 0.2636 | tet–tet 0.1956 | in |
| CdF₂ | Cd²⁺ 1.10 (key C) | F⁻ 1.31 | 1.1909 | 0.5436 | > 1/3 | 0.2030 | tet–tet 0.2656 | in |
| PbF₂ (β) | Pb²⁺ 1.29 (key C) | F⁻ 1.31 | 1.0155 | 0.5038 | > 1/3 | 0.2398 | tet–tet 0.2231 | in |
| UO₂ | U⁴⁺ 1.00 (key R*) | O²⁻ 1.38 | 1.3800 | 0.5798 | > 1/3 | 0.1720 | tet–tet 0.3014 | **out** (tet–tet overlap) |
| ThO₂ | Th⁴⁺ 1.05 (key RC) | O²⁻ 1.38 | 1.3143 | 0.5679 | > 1/3 | 0.1819 | tet–tet 0.2900 | in |
| CeO₂ | Ce⁴⁺ 0.97 (key R) | O²⁻ 1.38 | 1.4227 | 0.5872 | > 1/3 | 0.1660 | tet–tet 0.3083 | **out** |
| ZrO₂ (cubic) | Zr⁴⁺ 0.84 (key *) | O²⁻ 1.38 | 1.6429 | 0.6216 | > 1/3 | 0.1395 | tet–tet 0.3389 | **out** (packing still exists: t < 2/3) |
| Li₂O (anti) | O²⁻ 1.42 | Li⁺ 0.59 (key *) | 0.4155 | 0.2935 | **< 1/3** | 0.3358 | **oct–oct 0.0794** | in |
| Na₂O (anti) | O²⁻ 1.42 | Na⁺ 0.99 | 0.6972 | 0.4108 | > 1/3 | 0.3382 | tet–tet 0.1094 | in |
| K₂O (anti) | O²⁻ 1.42 | K⁺ 1.37 | 0.9648 | 0.4910 | > 1/3 | 0.2524 | tet–tet 0.2086 | in |

Areas in Å² under the contact model (lattice set so that r_1 + r_2 = d) are in `data/raw/compounds.json`. One exact identity (A7): for t ≥ 1/3 the Delian oct–tet face has area (3√3/2)·r_oct², and for t ≤ 1/3 it has area 6√3·r_tet². This is why BaF₂, Na₂O and K₂O, which all have r_oct = 1.42 Å, share the same oct–tet area of 5.239 Å².

**Sensitivity to the radius convention (crystal radii, CR = IR ± 0.14).**
- CsCl moves from x = 1.126 to 1.432. The other halides move towards x = 1.
- UO₂, CeO₂ and ZrO₂ move *into* the window (t = 0.521, 0.528 and 0.559).
- **Li₂O moves to t = 0.363, past the octet.** So Li₂O's side of the octet stop depends on the radius convention, and it is not a conclusion of this study.
- For all the other compounds, the side of the octet is the same under both conventions.

**Left out (radius unverified or not tabulated):**
- NH₄Cl: there is no NH₄⁺ entry in the by-element Shannon transcription.
- CuZn (β-brass), NiAl, FeAl, CoAl: metallic radii unverified. Teatum, Gschneidner and Waber (1968) was found on Crossref (doi:10.2172/4789465), but its tables could not be read from here.
- Rb₂O: there is no Rb⁺ CN IV entry.

### Q4. Against crystal chemistry

**Agreements.**
- The model's sites are exactly B2 and C1 (A6).
- The touching window *is* Pauling's radius-ratio limits. They come out of the loops exactly: √3 − 1 ≈ 0.732 for 8-coordination, and √(3/2) − 1 ≈ 0.225 for 4-coordination. Pauling's first rule is from J. Am. Chem. Soc. 51 (1929) 1010; the numbers are derived here, not quoted. B3: for every CsCl-type and fluorite compound, "in window" equals "r⁺/r⁻ ≥ 0.732".
- All five CsCl-type halides sit inside the window, at x ≈ 1.1–2.1. That is the big-ion-heavy side of Kelvin, between x = 1 and the like-contact limit √3 + 1. The golden stop x = τ ≈ 1.618 lies among them (between CsBr/TlCl and TlBr/CsI).
- Each golden piece has 14 radical faces (8 unlike + 6 like). These match the two bcc neighbour shells: 8 at (√3/2)a and 6 at a.
- Cubic ZrO₂ is far outside the window (r⁺/r⁻ = 0.61). This fits the general crystal-chemistry knowledge (not re-read for this study) that cubic zirconia is not stable at room temperature unless it is doped: pure ZrO₂ is monoclinic with Zr in 7-coordination.

**Disagreements and limits.**
- UO₂ (r⁺/r⁻ = 0.725) and CeO₂ (0.703) are stable fluorites, yet they fall outside the touching window with effective ionic radii. Both the hard-sphere contact model and Pauling's rule miss here. With crystal radii both fall inside. So the verdict depends on the radius convention.
- BaF₂ has r⁺/r⁻ = 1.08 > 1, and Pauling's rule would prefer a higher coordination. The hard-sphere model has no objection, because it tests only overlap.
- Na₂O (0.697) and K₂O (0.965) are far above the 0.414 upper limit for 4-coordination. Pauling's rule would predict a higher coordination for Na and K, yet both are antifluorites. The model allows them (they are in the window): it has no upper "rattling" limit of this kind.
- The radical faces are not the same as the distance shells. In fluorite with t > 1/3 (all the fluorides and oxides listed), the cation has 12 cation neighbours at a/√2 but **no** cation–cation face. Its cell has only the 8 cation–anion triangles, and the anions' cubes separate the cations.
- PbF₂: the fluorite (β) form is not the ambient form. Ambient PbF₂ is orthorhombic α, of cotunnite type (general knowledge, not re-read). The placement is for β-PbF₂.
- Limits of the model:
  - Real ions are not hard spheres.
  - A power diagram fixes only r₁² − r₂² (Q1). The radius ratio needs the contact assumption.
  - The real lattice constant is set by the crystal, not by r₁ + r₂. A placement from the measured lattice constant (Δ = (r₁² − r₂²)·(app/real)²) would differ from the contact placement, and was not done because no lattice constants were verified here.
  - The halide radii are CN VI proxies.
  - The radii come from a transcription of Shannon's table, not from the printed table.

### Q5. Prior art

**DICTO's reference library.** Four `ask-library` queries were run (`data/raw/ask-library.txt`), and INDEX.html, README.md and READING-LIST.md were searched by keyword ("Shannon", "radical tess", "Laguerre", "Gellatly", "Blatov", "colloid", "radius ratio", "ionic radi", "CsCl", "fluorite", "power diagram"). **Nothing was found** on CsCl-type colloidal crystals, radical/Laguerre tessellation, ionic radii or radius-ratio rules. The nearest entry is Cadotte, Dshemuchadse, Damasceno, Newman & Glotzer (2016), *Self-assembly of a space-tessellating structure in the binary system of hard tetrahedra and octahedra*, Soft Matter 12, 7073. That paper is about binary hard polyhedra, not spheres.

**Web.** One web search for radical tessellation in ionic crystals found no paper linking power diagrams with ionic radii, CsCl or fluorite. The candidates below were found from general knowledge plus Crossref queries. **Every DOI was checked on api.crossref.org (title, journal, year, volume and pages match), but none of these papers was read for this study.**

| reference | DOI (Crossref-checked) | relevance |
|---|---|---|
| R. D. Shannon, Acta Cryst. A32 (1976) 751–767 | 10.1107/S0567739476001551 | the radii |
| L. Pauling, J. Am. Chem. Soc. 51 (1929) 1010–1026 | 10.1021/ja01379a006 | the radius-ratio rule |
| B. J. Gellatly, J. L. Finney, J. Non-Cryst. Solids 50 (1982) 313–329, *the radical alternative to the Voronoi polyhedron* | 10.1016/0022-3093(82)90093-X | radical tessellation of spheres of two or more sizes |
| H. Imai, M. Iri, K. Murota, SIAM J. Comput. 14 (1985) 93–105, *Voronoi diagram in the Laguerre geometry* | 10.1137/0214006 | Laguerre diagrams of circles and spheres |
| F. Aurenhammer, SIAM J. Comput. 16 (1987) 78–96, *Power diagrams* | 10.1137/0216006 | power diagram ↔ regular triangulation |
| V. A. Blatov, Crystallogr. Rev. 10 (2004) 249–318, *Voronoi–Dirichlet polyhedra in crystal chemistry* | 10.1080/08893110412331323170 | Voronoi–Dirichlet polyhedra and coordination in crystals |
| M. O'Keeffe, Acta Cryst. A35 (1979) 772–775, *a proposed rigorous definition of coordination number* | 10.1107/S0567739479001765 | coordination from Voronoi faces |
| F. M. Richards, J. Mol. Biol. 82 (1974) 1–14 | 10.1016/0022-2836(74)90570-1 | radius-weighted cell volumes (proteins) |
| M. E. Leunissen et al., Nature 437 (2005) 235–240, *ionic colloidal crystals of oppositely charged particles* | 10.1038/nature03946 | CsCl-type colloidal crystals |
| A.-P. Hynninen et al., Phys. Rev. Lett. 96 (2006) 018303 | 10.1103/PhysRevLett.96.018303 | CsCl / CuAu phases of oppositely charged colloids |
| E. V. Shevchenko et al., Nature 439 (2006) 55–59, *binary nanoparticle superlattices* | 10.1038/nature04414 | size-ratio-controlled binary superlattices |
| D. Nykypanchuk et al., Nature 451 (2008) 549–552 | 10.1038/nature06560 | DNA-guided bcc/CsCl nanoparticle crystals |
| S. Y. Park et al., Nature 451 (2008) 553–556 | 10.1038/nature06508 | DNA-programmable nanoparticle crystals |
| R. J. Macfarlane et al., Science 334 (2011) 204–208, *nanoparticle superlattice engineering with DNA* | 10.1126/science.1210493 | phase choice (including CsCl type) set by the particle size ratio |
| A. E. Teatum, K. A. Gschneidner, J. T. Waber, LA-4003 (1968), OSTI | 10.2172/4789465 | metallic radii (would be needed for CuZn, NiAl, …) |

None of this is claimed as new. The following were **not found in DICTO's library, and not found in one web search**:
- the one-line contact maps ρ = (x + 2)/(2x + 1) and ρ = t/(1 − t);
- the fact that each loop's touching window is bounded exactly by Pauling's limits;
- the packing range t ∈ [1/6, 2/3] of the Delian loop.

These are elementary consequences of standard theory, and they are very likely known in some form.

## PASS / FAIL

| part | checks | PASS | FAIL |
|---|---|---|---|
| A symbolic (A1–A7) | weight = r², maps, windows, feasibility, stops, B2/C1, area identity | 32 | 0 |
| B exact cells (B0–B3) | Kelvin and RD sanity, 9 loop stops, 17 compounds, Pauling = window | 29 | 0 |
| **total** | | **61** | **0** |

## Files

- `scripts/symbolic.py`: part A. Writes `data/raw/symbolic.json` and `data/checks/symbolic-checks.txt`.
- `scripts/compounds.py`: part B. Writes `data/raw/compounds.json` (per compound: radii IR/CR, keys, ρ, x or t, counts, areas in app units and Å², CR sensitivity) and `data/checks/compounds-checks.txt`.
- `scripts/parse_shannon.py`: turns `data/raw/shannon-db/*.html` into `data/raw/shannon.json`.
- `scripts/crossref_check.py`: writes `data/raw/crossref.json`.
- `data/raw/ask-library.txt`: the library queries.
- `scripts/run.sh`: reruns everything.
