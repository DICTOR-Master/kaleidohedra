**Verdict: feasible, and the statement fits the published definitions with no change (pilot compiles). The proof is MEDIUM to LARGE work: smaller than Theorem 14's Lean proof, because every verified tool exists, but not a re-run of scripts. Three parts are new: √5 in the coefficients, a box that is unbounded in u, and a fresh analysis of the box's degenerate corners. The "traditional form" counts (43 triangles, 24 sandhis) should stay outside Lean. Put Theorem 15 on Palomar only as Version 2 of the existing entry, never as a separate entry, and run one blind pre-score of the Version 2 Challenge before building.**

# Theorem 15 of #103 in Lean: scope (study 2026-11-20)

DICTO, 20 Nov 2026: make the DICTO Yantra's result more visible. The plan: Theorem 15 in Lean as Version 2 of the Yantra Palomar entry (PALOMAR-2026-11-17-000006; one resubmission that also carries his ORCID), then #103 v6 leading with it. This study is a feasibility check only. Nothing was built beyond a statement pilot. The entry repository and the paper were not touched.

Read: #103 v5 (paper.html, Theorems 14 and 15, their certificates, §10); studies 2026-11-15-yantra-uniqueness, 2026-11-15-dicto-yantra-uniqueness, 2026-11-15-yantra-box-certificate (the Lean route), 2026-11-16-palomar-yantra, 2026-11-15-open-problems-to-close (blind score Y3); the entry repository (GitHub, head 6bf9e04, ORCID commit); the Lean workspaces on the compute host; palomar-kit CHECKLIST.md and prescore/policy (CONTRIBUTING §1 and §7, prompt 04, rubric); the public record of PALOMAR-2026-11-17-000006 v1.

## 1. How Theorem 14's Lean proof works

The Lean proof does **not** follow the paper's proof of Theorem 14. The paper eliminates (resultant E of degree 1744, then certified roots of f348 and f396). That identity is too large for a kernel (a 40 × 40 Sylvester matrix with entries of hundreds of digits). The Lean proof uses a branch-and-bound box certificate instead (study 2026-11-15-yantra-box-certificate):

1. **Derivation from the geometry.** Huet + Kulaichev + admissibility force 26 named quantities, one meeting point at a time (`Geom`, `GeomSteps`; `linear_combination` certificates found by Singular). A verified sparse-polynomial normaliser (`ZPoly`, `ZPolySound`, `Frac`) checks every identity from the figure to the stored polynomials G~, H~, D~ (13, 522 and 359 terms) and to the 36 admissibility tests. The divisor lemma becomes mechanical (`step_inv`).
2. **Box bounds.** Every admissible yantra lies in 0 < u < 1, 0 < τ < 1, 0 < ρ ≤ 6 (`BoxBounds`), with t = uτ and S = R + ρ(1 − u)(1 − R).
3. **Charts.** F~ = 0 meets the box's boundary at exactly two points, (0, 0, 1) and (1, 1, 2), where every equation and test vanishes. They are resolved by 9 blow-up charts (A, B; C1, C2; and a weighted tower W, Wt±, Wr±), read off Newton polygons. The coverings are hand-written case splits (`Charts`, `Unique3`).
4. **The certificate.** 64,613 rational boxes in 10 charts, 68,041 polynomial evaluations, 18.4 million term evaluations. Each box is closed by one sign test (an equation nonzero, or a test N·D < 0), checked by `decide +kernel` through a checker proved sound (`Check`, `Sound`, `Cover`). Generated as 1,216 modules; 6,387 s of module time.
5. **Krawczyk box.** The one box left (half-width 2⁻²²) holds exactly one zero (`krawczyk_unique`, contraction); existence on a box of half-width 2⁻¹⁰⁰ by Banach's theorem (`krawczyk_exists`). The slope theorem gives that zero's u to width 2⁻²¹.
6. **Existence.** The figure rebuilt at that zero meets every condition (`Exist`, `ExistFinal`).

Library: 28 hand-written or generated top-level files (7,370 lines) plus 1,369 generated data and derivation files; entry build 10,305 jobs, 26 min on 4 CPUs, peak 8.2 GB after the memory fixes; comparator export 379 MB (26,164 declarations).

**General (reusable for any polynomial system on a box):** `Check`, `Sound` (monotone split and slope form), `Cover` (`checkTree_sound`), `Krawczyk` (any finite dimension), `ZPoly`/`ZPoly2`/`ZPolySound`, `Frac`/`Frac2`, `GlueLemmas`, `Pull`; the generators c1, c2, c5–c15; the build-order and memory tooling; the Palomar kit.

**Specific to Kulaichev's conditions:** the stored polynomials and tests; `GeomSteps` (it uses u = v); `BoxBounds` (u < 1 comes from b3 < b7 when u = v); the 9 charts and their coverings; `Unique1`–`Unique4`; `KBoxData`, `KBox`; `Exist`, `ExistFinal`; the Challenge's `Kulaichev` definition.

## 2. Theorem 15's certificate, and how it differs

From #103 v5 §10.2 and study 2026-11-15-dicto-yantra-uniqueness:

- **The extra equation.** v = c/u with c = 2√5 − 4 = 2/φ³. All work is exact over ℚ(√5). The system after substitution: G 6 terms, H1 106, D 132, with coefficients a + b√5 (Kulaichev's over ℚ: 10, 312, 252). H1 has u-degree 15 (Kulaichev 21).
- **Elimination.** R1 = u¹⁰·A, A of degree (20, 20) in (u, t); R2 = u⁸·B, B of degree (28, 20). E = Res_t(A, B) has degree 560 = u⁴⁰⁰ · g80 · g80′ over ℚ(√5). Norms: f160 (Theorem 9) and h160. The second census (values at 869 integers, exact interpolation) gives E2 of degree 460 = u³⁸⁰ · g80, norm f160 only.
- **Roots.** f160 has 30 positive roots, h160 29 (Cauchy bounds 2¹⁸⁰ and 2¹⁸²). 177 branches (u, t); 165 rejected by B, 8 by H1 or D; **4 true solutions**, each in a Krawczyk box of radius 10⁻³⁰⁰.
- **The four solutions.** u = 0.57120 (passes Theorem 1's admissibility, but b5 > 1/2: the centre is an excentre, so (d) fails); u = 0.67176 and u = 0.88628 (not admissible); **u = 0.67931858870677… (the DICTO Yantra)**. Kulaichev's equations had 2 real solutions in range; here there are 4.
- **u is unbounded.** b3 < b7 only says uv < 1, which always holds. The census covers every u > 0, so the box of §1 (0 < u < 1) does not apply.
- **The traditional-form counts** (43 triangles, 18 marmas, 24 sandhis) are certified separately, outside Theorems 14/15's pipeline: #103 Proposition 11, script `certified_counts.py` (audit study 2026-11-09). It builds the planar arrangement of 27 sides in 560-digit interval arithmetic (vertices, edges, faces by rotation system, containment depths), deciding each near-zero concurrency exactly in Singular. The 18 marmas are already in the Lean statement as Huet's concurrencies. The 43 triangles and 24 sandhis are not, and Theorem 14's Lean entry likewise does not formalise its 45 regions or 28 sandhis.

## 3. What carries over unchanged, and what is new

**Unchanged:** the definitions `Yantra`, `Huet`, `OnCircle`, `InDisc`, `Admissible`, and Kulaichev's (b), (c), (d) word for word (pilot, §4); the soundness proofs (`Sound`, `Cover`, `Krawczyk`, `ZPolySound`, `Frac`); the tree checker; the module, build-order and memory tooling; the comparator, negative controls, fit check and preflight scripts.

**New:**
1. **√5 in the checked polynomials.** The checker and the normaliser work with integers in three variables. Two routes: (a) monotone split with interval coefficients, a⁺ + b⁺·[s_lo, s_hi], sound because every coordinate is ≥ 0: a small change to `Check` and `Sound`; or (b) √5 as a fourth variable on a thin box, which means generalising `ZPoly`, `Check` and `Cover` from three variables. The derivation identities can be checked over ℤ[u, v, t, S] with v free before v = c/u is applied (the paper's divisor lemma is already done that way), which needs a 4-variable `ZPoly` or reduction modulo s² − 5. Route (a) for the certificate, plus a 4-variable normaliser for the derivation, is the likely choice.
2. **An unbounded box.** u ∈ (0, ∞). The natural split: u ≤ 1 in u, and u ≥ 1 in v = c/u ≤ c < 1. New box bounds (the τ bound becomes t < v; the ρ bound must be re-derived from b9 < 1 and w9 ≤ 1/2) and their Lean proofs.
3. **A new boundary and corner analysis.** This is the main risk. For Kulaichev it needed 9 charts and a weighted tower of 7 at the collapse corner (0, 0, 1), found by hand from Newton polygons, with hand-written covering proofs. The DICTO system has two degenerate ends (u → 0 and v → 0), and nothing yet says how many charts they need.
4. **A new certificate.** Generation, exact recheck and independent Arb recheck (token-free compute). Size: of the same order as Kulaichev's, tens of thousands of boxes or a few times more. The polynomials are shorter, but the domain is two halves and the system has 4 real solutions in range instead of 2, so more boxes are needed near each.
5. **Regenerated proof layers.** `GeomSteps` (u, v free), `Unique1`–`Unique4`, `KBoxData`/`KBox` at the DICTO root, `Exist`/`ExistFinal` with √5. The generators exist; their inputs change.
6. **The excentre solution (u = 0.57120)** is an exact zero of G, H1, D inside the box, so its neighbourhood is closed only by the test b5 < 1/2, which the Lean (d) already contains. It needs no new idea, but it makes the boxes near it small.

## 4. Pilot (compute host, foreground, each call under 5 s)

- **The existing library compiles.** `lake build YantraCert Solution` in the workspace of the published entry: "Build completed successfully (10305 jobs)", 3.8 s (already built, so a replay).
- **Theorem 15 is expressible with the existing definitions.** `pilot/DictoYantraStatement.lean` imports `YantraCert.Main` and adds two definitions only:
  - `Yantra.KulaichevBCD`: (b), (c), (d) copied from `Yantra.Kulaichev`;
  - `Yantra.CleoAntonius`: (w7/b7)·(w3/(1 − b3)) = 2√5 − 4.
  - `kulaichev_eq_a_and_bcd : y.Kulaichev ↔ ((a) ∧ y.KulaichevBCD)` closes by `Iff.rfl`, so the reuse is exact.
  - `two_div_phi_cube : 2/φ³ = 2√5 − 4` is proved.
  - `dicto_unique : ∃! y : Yantra, y.Huet ∧ y.KulaichevBCD ∧ y.CleoAntonius ∧ y.Admissible` and `dicto_slope` (w7/b7 in [3059377869223857, 3059380016707505]/2⁵², width 2⁻²¹, around 0.6793185887…) compile with `sorry`, which is allowed in this pilot only.
  - Result: no errors, two `sorry` warnings, 3.4 s, peak 6.7 GB (the Mathlib import). Log: `pilot/pilot-log.txt`.
- **Challenge size.** The two definitions and two theorems add about 40 lines to the published Challenge (133 lines, 8,215 bytes in the public record): about 175 lines, inside the preferred 300 lines and 32 KiB.

## 5. Effort, risks and the Palomar route

**Effort: medium to large.** It is medium if the new box's degenerate ends resolve with a few charts. It is large if they need a tower like Kulaichev's (0, 0, 1) corner. One cheap first step decides which: the face analysis of the new box (the equivalent of scripts/explore x4–x6), with no Lean. Adding the traditional-form counts to the Lean statement would be a separate **large** project (planar arrangements, faces and a definition of "region" and "sandhi" that the reviewer must audit). Keep them out of Lean: the counts stay certified by #103 Proposition 11, and the abstract says plainly that they are not formalised.

**Risks:**
- **Corner charts (main risk).** Unknown number, hand-written coverings (§3.3).
- **Certificate size.** Of the order of Kulaichev's or a few times more. Kernel time is not the limit (Kulaichev: 6,387 s of module time; modules cut at 1.9 GB each).
- **Build memory against Palomar's runners.** Version 1 was cut from over 16 GB to 8.2 GB by chaining heavy modules. The new derivation modules with √5 can be larger and must be measured the same way (`measure_lean_mem.sh`). Palomar ran the Dehn entry on 16 CPUs / 32 GB; the workflow's standard runner is 4 CPUs / 16 GB.
- **Comparator.** The export will roughly double (Version 1: 379 MB). con-ron at Palomar's 2 workers and 1800 s budget may run out of capacity. Palomar then records "declined" with a warning, not a rejection (checklist §D). The public record of Version 1 lists NanoDa beside Lean's kernel.
- **Challenge limit.** No risk: about 175 lines.
- **Review risk (the real one).** CONTRIBUTING §1 excludes "theories whose definitions have been designed merely to manufacture the advertised conclusions". The earlier blind replay scored the DICTO Yantra (Y3) at notability 2: the golden condition "reads as chosen to get the count; no source asks for it" (study 2026-11-15-open-problems-to-close). Version 2 is reviewed as a whole, so a finding against the Cleo-Antonius definition would attach to the whole entry.

**Version 2, not a separate entry.**
- **A separate entry would fail.** CONTRIBUTING §7: "A notability score below 4 is a fundamental editorial failure and leads to `rejected`." Theorem 15 alone has a blind 2 or 3.
- **Version 2 keeps the anchor.** Kulaichev's question (posed in print 1984; called open by Chiodo 2021) carries Version 1's 4. Theorem 15 enters as its companion: the same conditions with the fourth replaced, and the only figure is then the traditional one. That is the contrast #103 already draws (Theorem 14: unique but not traditional; Theorem 15: unique and traditional).
- **One configuration.** CONTRIBUTING §7: "One Palomar submission records one Comparator configuration." Version 2 lists all four theorems in one `comparator.json`.
- **One resubmission.** Checklist §C: the ORCID added later "means a resubmission". Checklist §E: "Avoid resubmissions" (Version 1 cost about 3.5 h of verification). The ORCID commit (6bf9e04) is already on GitHub. Carrying it and Theorem 15 in one Version 2 is one resubmission, not two.
- **The rule that cuts against it.** Checklist §A: "A wider scope that does not raise notability stays in the paper" (Dehn D2, Grünbaum G2), and "Blind pre-score before building". By that rule Theorem 15 would stay in #103. DICTO's aim here is visibility, not a higher score, so the rule does not forbid Version 2. It does require the blind pre-score first, with the Version 2 Challenge quoted in full. Build only if both scorers keep 4 and report no "manufactured definition" finding.
- **The source rule** (checklist §B) holds as it is. The entry is already source-based, with #103 `formalizes`. Version 2 cites #103 v5 (released, DOI 10.5281/zenodo.24379694), where Theorem 15 is first stated.
- **Background.** DICTO decided on 17 Nov that the entry stays unchanged (consolidation ledger, #103 headline point). His word of 20 Nov supersedes that for this plan.

**Order of work proposed:** (1) the blind pre-score of the Version 2 Challenge (pilot statement plus the published one); (2) the face analysis of the new box; (3) then the build, as in §3.

## Files

- `pilot/DictoYantraStatement.lean`: the pilot statement (two `sorry`, pilot only).
- `pilot/pilot-log.txt`: the two compile runs, with times and peaks.

FINAL ok
