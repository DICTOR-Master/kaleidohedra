# Gap batch B (2026-11-21): #53 Observation 3, #54 open points, #111 fields of the radii

**Conclusion.** All three items are closed by exact checks. (1) The type of hand-over (#53 Observation 3) cannot be read off site symmetry alone: CsCl and rock salt have the same site groups and opposite types. A symmetry rule does hold for the networks with a kind swap: there the type is read off the Voronoi cells at equal weights. (2) #54: using the cycle's own solids at other scales gives classical gnomons shorter than a turn, down to one step. Capped cubes with heights adding to 1 never fill space together, at any sizes, with or without the Tricaps. (3) #111: (R/r)² has degree 16 (T ∩ D), 24 (42 faces) and 20 (50 faces), each with non-real conjugates, so none of the three lies in the field of a regular polygon.

**Status: CLOSED** (items 1, 2a, 2b, 3). Gap study rows: R11 / L19 (Observation 3 part), L20, L43 (the fields part).

The questions and the stations, pieces and dice are DICTO's (#53, #54, #111). Computation, proofs and drafting were done with Claude (Anthropic).

Run on the compute host (`~/venvs/sym`, sympy 1.14, mpmath). Every script ends with a conditional FINAL line, and every log ends with `FINAL ok`. Inputs reused (not changed): the relay-census nets and engine, the switch-theorem nets, `2026-11-09-cscl-zincblende/data/likebirth.json` (τ values), `2026-10-25-gnomon-shapes/stations-exact.json`, and `2026-11-18-fair-32-die/data/verts-*.json` (140-digit μ_f).

---

## Item 1. #53 Observation 3: τ_A + τ_B against site symmetry (`scripts/obs3_symmetry.py`, 77/77 PASS)

**Question.** Observation 3 left open "a rule that reads the type off the symmetry or the hole type alone". Here τ_A + τ_B (Proposition D, study 2026-11-09) is tabulated against the exact symmetry of the twelve networks.

**Method.** For each two-kind site set we enumerate exactly every lattice isometry x ↦ Rx + t (mod T) that keeps the kinds ("sym") or exchanges them ("swap"). From these we get the site groups (named from their element types, with any unknown signature counted as a FAIL), centrosymmetry, and the Voronoi cells of the union at λ = 0 (exact corners, relay-census engine). We also compute the distance value μ_K = min over like pairs of (ℓ²/4 − δ²), where ℓ is the like distance and δ the distance from the pair's midpoint to the nearest unlike site.

| network | site group A | site group B | swap | centro | τ_A + τ_B | type | like faces at λ = 0 (A; B) | μ = τ? |
|---|---|---|---|---|---|---|---|---|
| square + centres | 4mm | 4mm | yes | yes | 0 | switch | 0; 0 | yes |
| honeycomb + centres | 3m | 6mm | no | yes | 0 | switch | 3; 0 | yes |
| kagome + centres | mm2 | 6mm | no | yes | 0 | one like bond | 4; 0 | no (kagome) |
| CsCl | m-3m | m-3m | yes | yes | −2 | gradual | 6; 6 | yes |
| fluorite | -43m (tet) | m-3m (oct) | no | yes | 0 | switch | 6; 0 | yes |
| rock salt | m-3m | m-3m | yes | yes | 0 | switch | 0; 0 | yes |
| zinc blende | -43m | -43m | yes | no | −2 | gradual | 12; 12 | no |
| hcp holes | 3m (tet) | -3m (oct) | no | yes | −2/3 | gradual | 10; 2 | yes |
| A15 | m-3 (Si) | -42m (Cr) | no | yes | −1/2 | gradual | 0; 10 | yes |
| C15 | -43m (Mg) | -3m (Cu) | no | yes | −14 | gradual | 4; 6 | Mg yes, Cu no |
| h-BN (control) | 3m | 3m | yes | no | 0 | switch | 0; 0 | no |
| sodalite (control) | -42m | -42m | yes | yes | 0 | switch | 0; 0 | yes |

These are the groups of the site sets alone. For example, sodalite's T sites without the oxygens have -42m, not the -4 of the full mineral.

**Results.**
1. **Site symmetry alone does not decide (exact counterexample).** In CsCl and rock salt both kinds have site group m-3m. Both are centrosymmetric and both have a kind swap. CsCl is gradual (τ_A + τ_B = −2) and rock salt is a single switch (0).
2. **The hole type alone does not decide across dimensions.** Take the d-dimensional CsCl family: (2ℤ)^d plus the centres of its cubes, so each kind fills every cube hole of the other. The midpoint of a like pair is an inversion centre, so τ = ℓ²/4 − δ² = 1 − (d − 1) = 2 − d. The hand-over is a switch for d = 2 (square + centres) and gradual for d = 3 (CsCl). This was checked for d = 1 to 4. Among the twelve 3D networks, no two share a hole type and differ in type, so no counterexample inside 3D was found.
3. **Swap Corollary (proved here).** Suppose an isometry of the site set exchanges the two kinds. Then τ_A = τ_B ≤ 0, and the hand-over is a single switch, at λ = 0, if and only if no Voronoi cell of the union at equal weights has a like neighbour. Equivalently, the kinds properly 2-colour the Delaunay graph of the union. Otherwise it is gradual on (τ, −τ).
   *Proof.* The swap carries the diagram at λ to the diagram at −λ with the kinds exchanged; adding −λ to every weight does not change a power diagram. So A–A bonds at λ correspond to B–B bonds at −λ, and τ_A = τ_B. Proposition D gives τ_A + τ_B ≤ 0. A switch means τ_A = −τ_B, so τ = 0, which holds iff no like bond exists at λ = 0. ∎
   Checked on all six swap networks: square, CsCl, rock salt, zinc blende, h-BN and sodalite (6/6). CsCl (bcc union, 6 like faces) and zinc blende (diamond union, 12 like faces) are gradual; the other four are switches.
   Control that fails as it should: honeycomb + centres has no swap and has 3 like faces at λ = 0, yet it switches (at −1/2). So the corollary needs its hypothesis. Fluorite has no swap and τ_tet ≠ τ_oct.
4. **Distance rule.** μ_K ≥ τ_K always, because the midpoint is feasible. Equality holds whenever a minimising pair has an inversion centre at its midpoint. Equality holds for both kinds on 8 of the 12 networks, and then the type is read off distances alone. The exceptions are kagome (degenerate: the one like bond sits at the range end), zinc blende, h-BN and the Cu of C15, where the LP of Proposition D is needed.

**Verdict: CLOSED.** The answer to "a rule from the symmetry or the hole type alone" is no. Site symmetry fails inside 3D (CsCl / rock salt) and hole type fails across dimensions (τ = 2 − d). In its place:
- the Swap Corollary, an exact symmetry rule for the swap class;
- the distance rule, which covers 8 of the 12 networks;
- Proposition D, which covers the rest.

Together the Swap Corollary and the distance rule decide 10 of the 12 without an LP. The two left are kagome (the degenerate case) and C15.

**Proposed home.** #53, next version: Observation 3 becomes "closed". Add the table, the Swap Corollary and the CsCl/rock-salt counterexample beside Proposition D.

---

## Item 2. #54 open points (`scripts/gnomon_open.py`, 16/16 PASS)

### 2a. "Whether another choice of stations makes a shorter run of steps a classical gnomon"

**Question as made precise.** If stations may be chosen freely, the answer is trivially yes (X and 1.01·X are nested). So we ask it for the cycle's own solids: can one station X, scaled by s with 1 < s < φ³, be inserted into the chain S_j ⊂ sX ⊂ S_{j+1}? If it can, then the run X → … → sX is shorter than a turn and is a classical gnomon of X (#54 Theorem A: a run is a gnomon exactly when its end is similar to its start).

**Method (exact, ℚ(√5)).** All twelve stations are rebuilt from `stations-exact.json`. Facets are proposed by a float hull and then proved exactly. The window for each station and gap is max_f h_{S_j}(u_f)/c_f ≤ s ≤ min_g c_g/h_X(u_g).

The Cleo star is not convex. It is star-shaped, and inside the cone over each face F of I it is exactly the bipyramid conv(0, F, tip_F). So its window is computed exactly in one face cone, after checking that every station is invariant under the 120 symmetries of I.

Controls:
- I·φ³ = φ³·I;
- all 11 nestings hold;
- RT ⊄ TI (fails, as it should);
- s·I ⊂ Cleo star exactly for s ≤ 1;
- the Cleo star's hull D′ fits in it only for s ≤ 9/4 − (3/4)√5 < 1.

**Results.** There are 23 proper windows.
- **One-step gnomons** come from thin homothetic shells:
  - D′ ⊂ s·D′ ⊂ ID for 1 < s ≤ (3 + √5)/4 = φ²/2;
  - OG ⊂ s·OG ⊂ rTI for 1 < s ≤ 13/3 − (22/15)√5 ≈ 1.0538.
- **Golden scales that touch both neighbours exactly:**
  - φ·ID sits exactly between M and I·φ³;
  - (φ³/3)·rTI and (φ³/3)·TI sit exactly between M and I·φ³;
  - (φ³/3)·RT sits exactly between I·φ³ and the Cleo star·φ³ (exact star test);
  - (3/2 − √5/6)·jtI sits exactly between RT and M;
  - (11/18 + 5√5/18)·H, ·jtI and ·RT sit exactly between M and I·φ³.
- **Wider windows:**
  - 2·M up to φ²·M fits between D′·φ³ and ID·φ³ (s ∈ [2, φ²]);
  - ID·s fits there for s ∈ [1 + √5, φ³).
- The Dharma dodecahedron D = (3/2)·D′ is not in D′'s only window, since 3/2 > φ²/2.

**Verdict: CLOSED.** With the twelve stations as they are, Theorem A stands: only the whole turn is a gnomon. If the cycle's own solids may be used at other scales, shorter runs are classical gnomons, down to a single step. The exact windows are in `data/gnomon_open.json`.

The golden cases (φ·ID, φ³/3·RT and others, each touching both neighbours) are the ones worth a sentence in the paper. The thin-shell ones are trivial.

### 2b. "Whether pyramid-capped cubes with heights adding to 1 can fill space together at other sizes or with the Tricaps as separate pieces"

**Method.** We use the dihedral-angle obstruction. It holds for any sizes and for tilings that are not face-to-face. At a generic point of an edge, the dihedral angles of the tiles that meet there, plus π for each tile that has the point inside a face, sum to 2π.

Let P(h) be the cube of half edge 1 with a pyramid of height h on each face (0 < h < 1). It has two edge angles, both in (π/2, π):
- the cube-edge angle A(h) = π/2 + 2·atan h;
- the apex-edge angle B(h) = π − arccos(1/(1 + h²)).

So every closing combination is exactly three angles. For each of the 20 triples from {A(h), B(h), A(1−h), B(1−h)}, we take sin(sum) = 0, which is equivalent to sum = 2π on the possible range. The square roots are eliminated by resultants, the real roots in (0, 1) are isolated exactly, and each root is tested at 60 digits.

Controls:
- A(1) = π and B(1) = 2π/3 (the rhombic dodecahedron);
- A(1/2) = B(1/2) = arccos(−4/5) (tetrakis hexahedron);
- the #54 golden angles 153.43°, 136.35°, 131.81° and 150.77° are reproduced;
- pass control: h = 2 − √3 (3·A = 2π) is found by the elimination.

**Results.**
- Six candidate heights: h = 2 − √3, √3 − 1, 0.16015…, 0.22734…, 0.77266…, 0.83985… At each of them, at least one edge type of P(h) or P(1−h) has no closing triple; the four edge types never all close at once. So **no pair P(h), P(1 − h), 0 < h < 1, fills space together, at any sizes and in any proportion**. No single P(h) fills space either.
- **With the Tricaps (golden pair).** The Tricap's dihedral angles are exact:
  - arccos(−1/√5) = 116.565° at its three apex edges;
  - atan(2/φ²) = 37.377° at its three base edges, with cos² = 1/3 + (2/15)√5 = φ⁴/(φ⁴ + 4).
- The only closing combination is A(1/φ) + A(1/φ²) + 2·atan(2/φ²) = 2π. It is exact: A(1/φ) + A(1/φ²) = π + 2·atan(φ²/2), because 1/φ + 1/φ² = 1.
- The apex edges of both polars (136.35° and 150.77°) have no closing combination at all; the nearest miss is 0.51°. So **the golden polars with the Tricaps as separate pieces cannot fill space, at any sizes**.

**Verdict: CLOSED (no).** This makes the float edge count of #54's Remark exact and extends it to every h, every size and the Tricaps.

**Proposed home.** #54, next version: a "Version N adds …" line, with 2a as a Remark after Theorem A and 2b replacing the float Remark in §6.

---

## Item 3. #111: the fields of the radii of T ∩ D and of the 42- and 50-face dice (`scripts/radii_fields.py`, `scripts/radii_fields2.py`)

**Method.** First, `radii_fields.py` finds every corner at 80 digits from the planes of each die, with μ_f taken from Corollary 7. That closed form agrees with the earlier 140-digit μ_f to 10⁻¹⁰⁰ on all three dice, and r/R agrees with Table 1.

On all three dice the farthest corners lie on three B planes only. So R² = κ·μ_f², where κ is the squared distance of that corner of the B solid at face distance 1, and κ is exact in ℚ(√5):
- T ∩ D: κ = 15 − 6√5;
- D ∩ RT: κ = (9 − 3√5)/2;
- I ∩ RT: κ = (5 − √5)/2.

The coefficients b·a², b·u², (b·a)(b·u) and tan²(π/m) all lie in ℚ(√5), each verified exactly. Write t² = tan²(π/m)·(1 − c)/(1 + c) − 1 with c = cos 2θ. Then R² is a root of (Y − P)² − Q²t² over ℚ(√5, c).

`radii_fields2.py` eliminates c and √5 by resultants and takes the one irreducible factor that vanishes at R²; the gap to the other factors is ≥ 0.67. It counts the real roots exactly (Sturm).

Controls: O ∩ D gives Y² − 218Y + 361, that is (R/r)² = 109 − 48√5 (Theorem 4A), and its Galois group is found abelian exactly. C ∩ O gives Y³ − 21Y² + 35Y − 7, the heptagon field of Theorem 2.

| die | line | θ | (R/r)² | minimal polynomial degree | real roots | field |
|---|---|---|---|---|---|---|
| 16 | T ∩ D | 5π/24 | 1.78057876749… | 16 | 12 of 16 | not Galois: in no field of a regular polygon |
| 42 | D ∩ RT | 13π/42 | 1.16261608243… | 24 | 16 of 24 | not Galois: in no field of a regular polygon |
| 50 | I ∩ RT | 9π/50 | 1.42537560591… | 20 | 14 of 20 | not Galois: in no field of a regular polygon |

The polynomials are in `logs/field-*.log` and `data/field-*.json`. The earlier search (degree ≤ 24, coefficients < 10⁹) missed them because their coefficients are up to about 10²⁰. These minimal polynomials are exact by elimination, not identified by PSLQ.

**Verdict: CLOSED.** The fields of the radii of T ∩ D, D ∩ RT and I ∩ RT have degrees 16, 24 and 20. None is Galois over ℚ, so by Kronecker–Weber none lies in a cyclotomic field or in the field of a regular polygon.

With Proposition 5 this answers #111's first open question for all twelve lines: the polygon is in the lengths on exactly C ∩ O, O ∩ RD, O ∩ D and D ∩ I. The other eight lines do not put it there: T ∩ C, T ∩ RD, C ∩ RD, T ∩ D, D ∩ RT and I ∩ RT have no polygon field, and C ∩ D and RD ∩ D have no regular faces.

**Proposed home.** #111, next version: extend Proposition 5 to the 16-face (T ∩ D), 42- and 50-face dice, and mark open question 2 (and 1, for the twelve lines) answered.

---

## LEADS
1. #53: is there a hole-type rule inside 3D? Among the twelve, no two networks share a hole type and differ in type. A screen of more 3D two-kind structures (perovskite B/X, fluorite variants) would test it.
2. #53: the Swap Corollary turns "switch" into a Delaunay 2-colouring test. This is a fast screen for DICTO's own HexOct / TRD / RD-cross networks (the switch-theorem lead 2).
3. #54: the golden touching insertions (φ·ID between M and I·φ³; φ³/3·RT just outside I·φ³) suggest a second, finer chain. Check whether the pieces they cut are any of the Julias.
4. #111: Theorems 3, 4 and 4A rest on PSLQ for minimality. `radii_fields2.py` gives their minimal polynomials by exact elimination in the same way (O ∩ D done here), so all of them can be made exact.

## Ledger lines (for the Concordance; not entered by this study)
- `{"question": "#53 Obs 3: type from symmetry/hole type", "method": "obs3_symmetry.py exact space groups, site groups, Voronoi at lam=0, tau from likebirth.json", "status": "SETTLED", "result": "no rule from site symmetry alone (CsCl vs NaCl, both m-3m/m-3m); hole type fails across d (tau = 2 - d); Swap Corollary: with a kind swap, switch iff equal-weight Voronoi has no like face (6/6); distance rule mu = tau on 8/12", "retry": "never", "study": "2026-11-21-gaps-batch-b", "date": "2026-11-21"}`
- `{"question": "#54 shorter gnomon run; capped cubes tiling", "method": "gnomon_open.py exact Q(sqrt5) windows + star test; dihedral elimination by resultants", "status": "SETTLED", "result": "rescaled stations give gnomons down to one step (D' to phi^2/2 D'); no P(h)+P(1-h) tiling at any size; golden polars + Tricaps cannot tile (apex edges never close)", "retry": "never", "study": "2026-11-21-gaps-batch-b", "date": "2026-11-21"}`
- `{"question": "#111 fields of radii T∩D, 42, 50", "method": "radii_fields2.py exact elimination R^2 = kappa mu^2, Sturm count", "status": "SETTLED", "result": "degrees 16, 24, 20; mixed signature; not Galois; no polygon field", "retry": "never", "study": "2026-11-21-gaps-batch-b", "date": "2026-11-21"}`

## Files
- `scripts/`: obs3_symmetry.py, gnomon_open.py, radii_fields.py (corners, controls co/od), radii_fields2.py (exact fields).
- `data/`: obs3_symmetry.json and checks; gnomon_open.json and checks; radii-co/od and field-td/dt/it/od, each .json with its checks.
- `logs/`: one log per run, each ending `FINAL ok`. The first radii_fields.py run on T ∩ D (sympy minimal_polynomial on the full radical expression) hit the time limit and was replaced by radii_fields2.py; its partial log was deleted.
