# Shape kernel, stage 1 proper: one kernel of exact numbers for every copy (18 Nov 2026)

Plan: `papers/plan-shape-language.md`, stage 1 ("Kernel of exact numbers"). Follows the pilot
(`studies/2026-11-18-shape-kernel-pilot`, unchanged); its kernel, tests and replay method are reused and extended here.

**Question.** Can one kernel replace every exact-number copy in the studies, including the fields the pilot left out
(Q(√2, √5), the golden basis a + bφ, Z[φ], the cubic fields and Q(t) of exactlib.py), with exact signs that never rest on
a float, and give the same results as the copies and as the stored study outputs?

**Answer.** Yes for every copy found. 84 copies in 8 groups (and one vectorised copy kept apart by design) agree with the
kernel on every operation they provide. In 17 comparisons two copies give a wrong sign; there the kernel agrees with a
120-digit check. 61 study runs replayed with the kernel in place of their number code give byte-identical output to the
original runs (times masked). 3 further runs could not be counted because their inputs are not in the study. No group
failed to reproduce.

## 1. Inventory (scripts/inventory.py, data/inventory.json, data/inventory.log)

The scan reads all 2515 study scripts with the AST; no study code runs. G1–G3 use the pilot's rules unchanged.

| Group | What | Copies | Studies | Distinct sources | Kernel type |
|---|---|---|---|---|---|
| G1 | Q(√5) as a class `Q5` / `Q` | 32 | 27 | 30 | `Quad` (pilot) |
| G2 | Q(√d) as a class `QF` | 14 | 14 | 9 | `Quad` (pilot) |
| G3 | Q(√5) as Fraction pairs (`qa`, `qm`, `sgn` …) | 10 | 8 | 7 | `pairs` (pilot) |
| G4 | the pilot's "four-term field" list, class `K` | 6 | 6 | 4 | `MQ`, `NF`, `Quad` |
| G5 | golden basis a + bφ as a class | 4 | 4 | 3 | `NF` over `GOLDEN` |
| G6 | Z[φ] as integer pairs (`zadd`, `zmul`, `zsign` …) | 4 | 4 | 3 | `zphi` |
| G7 | cubic and general fields (`KC`, `AlgField`, `RF`; a general `Field`/`E`) | 7 | 3 | 4 | `NF`, `NumberField` |
| G8 | other Q(√d) classes, found by the wider scan | 7 | 7 | 6 | `Quad` |

**G4 is not one field.** Read by its product, the pilot's list of six `K` classes holds four different things:

- cubes_lib.py ×3 (identical): the four-term field Q(√2, √5).
- octet_special_exact.py: the radical field Q(k^(1/n)), with n and k set per run (√2, √6, 2^(1/3)).
- pds_line.py: plain Q(√5) under the name K.
- law-giving census exact.py: Q(√D) on python-flint rationals.

**G5–G7, new copies found.**

- G5: echo_lib.py and qlib.py carry a golden-basis `Q5`; residents.py has a class `E` that is a + bφ or a + b√2, chosen per element.
- G6: get-palomar getgeom.py has its own Z[φ] functions. independent-checks 110-exact common.py also has them (see below).
- G7: web-of-bonds lib.py has a general field element `E` over a monic minimal polynomial, with its sign read from an
  80-digit evaluation.

**Wider scan (W).** Each item gets a verdict:

- **Real copies, added as G8:** sweeplib `F`, R5 ×3 (on gmpy2 rationals), amp_dist `QD`, middles `QS`, tw_binary `F`.
- **Kept apart by design:** two Z[φ] copies written from scratch for independent checks: 110-chambers zphi.py (numpy,
  vectorised) and 110-exact common.py. Both are compared below, but an independent check must not share the kernel.
- **Number-field operations, not whole copies:**
  - `conj2`, `conj5`: inside cubes_lib.
  - `sqrtQ` ×3: a square root in Q(√5), found by a float search over small denominators.
  - `qsqrt` ×4: a square root by sympy. The kernel now has an exact `Quad.sqrt`.
- **Not copies:**
  - `exact_volume` ×5 and `faces_exact` ×3: geometry computed with a number class.
  - 6 other classes with a product: an interval wrapper, a divisor logger, interval values with derivatives, expression
    trees, the law-giving polynomial classes `E` and `KP`.
  - 199 scripts that use sympy: library use.
- **Inline norm or sign tests (a² against d·b²):** 40 files without their own number class (48 formulas). These use a
  copy's numbers or plain Fractions. They belong to stage 2, where the geometry moves to the kernel.

## 2. Design (kernel/)

- `exact.py` (pilot) gains the following:
  - `qsign(a, b, d)`, the one quadratic sign rule. `Quad.sign` and `zphi.zsign` both use it.
  - `Quad.sqrt()`, an exact square root, or None if the number is not a square in its field.
  - `float_hp`, now correctly rounded.
  - Three printed styles for the G8 copies.
- `field.py` (new):
  - `NumberField(p, lo, hi, name)`: Q(t), where t is the only root of p in a rational isolating interval.
    - It has the same constructor and methods as exactlib's `AlgField`.
    - A Sturm count checks that the interval holds exactly one root.
    - `pure_field(k, n)` gives Q(k^(1/n)). `GOLDEN` is φ² = φ + 1.
  - `NF(c, F)`: an element of F.
    - `+ − × ÷` (the inverse by the extended Euclidean algorithm), integer powers and the norm. `conj` in degree 2.
    - Exact `sign`, `== < <= > >=`, `abs`.
    - `float`, `dec`, `mp` and `digits`.
  - `MQ(a, b, c, d)`: a + b√p + c√q + d√(pq), with (p, q) = (2, 5) by default.
- `zphi.py` (new): the Z[φ] pair functions. Ints in, ints out, as zsurf.py uses them in its hot loops.

**Built on established libraries (credited).**

- **python-flint** (FLINT and Arb; W. Hart, F. Johansson et al.):
  - Irreducibility of every defining polynomial comes from FLINT's `fmpz_poly.factor`.
  - `arb_sign_nf` and `arb_sign_mq` give a second, certified sign with Arb ball arithmetic. The tests require it to agree
    with the kernel's sign on every element.
- **sympy** (`minimal_polynomial`): confirms the minimal polynomials of the bronze and heptagonal numbers.
- **mpmath**: the 120–150-digit reference values.
- **Sturm's theorem and interval bisection** are the textbook methods. The bisection itself is exactlib's `AlgField`, kept
  step for step, because the copies' printed decimals depend on its order.

The kernel is therefore a thin compatibility layer: styles, hashes and the copies' API, over exact arithmetic that the
libraries certify.

**Exact sign, never a float.**

- `NF`:
  - Interval Horner evaluation on the rational interval of t, bisected until 0 is excluded. The bisection is exactlib's,
    step for step, so a shared field refines in the same order and printed decimals stay the same.
  - Every 64 steps an exact zero test runs: the gcd of the element's polynomial with p, then a Sturm count on the
    interval. So a reducible p cannot loop forever.
  - Degree-2 fields that the kernel makes itself (GOLDEN, pure √k) use the quadratic rule instead and leave the interval
    untouched.
- `MQ`: rational enclosures of √p, √q, √pq from integer square roots at 32, 64, 128 … bits, until the interval of the
  value excludes 0.

**Printed forms, floats and hashes** follow each copy through named styles (`NF_STYLES`, `NF_FLOATS`, `MQ_STYLES`, plus
the pilot's `STYLES`). Each study's shim names its style in one line (replay/shims/).

**Floats** are refused in arithmetic. As a coefficient, a float is taken only when it is a small dyadic rational
(denominator ≤ 2^16, such as 1.0 or 0.5). 0.1 raises TypeError. The copies took every float at its binary value. One
replayed study builds `K(abs(float(c)))` from such small values (§5).

## 3. Tests (all run on a compute machine; logs in data/)

**Pilot kernel tests, unchanged: `tests/test_kernel.py`. 37 checks, FINAL ok.**

**Field tests: `tests/test_fields.py`. 42 checks, 0 failed, FINAL ok** (run with python-flint 0.9.0 and sympy 1.14.0).

- **A. Ported checks:**
  - cubes_lib: √2² = 2, √5² = 5, √10² = 10, φ² = φ + 1; conj2 and conj5 are automorphisms; the kstr form.
  - exactlib KC: r³ = 2; the norm formula; sign = sign of the norm (on 600 elements); the KC printed form.
  - The #56 field: its polynomial, its key and the 30-digit decimal of t stored in dicto-lahdeli.json, reproduced.
  - octet: (2 − √2)² = 6 − 4√2.
  - mixlib: the norm a² + ab − b².
  - zsurf: the six AX6 axes, |e|² = φ + 2 and e·f = ±φ; zconj is an automorphism.
- **B. Field and order axioms** on random triples in 10 fields: Q(√2, √5), Q(√13), Q(cos 2π/7), Q(2^(1/3)),
  Q(3^(1/3)), Q(6^(1/3)), Q(2^(1/4)), the #56 field Q(t), the golden basis, and Q(√6) in the power basis. 250–1000 triples each.
- **C. Exact sign against 150-digit mpmath:**
  - Q(√2, √5): 529 near-zero elements (products and differences of the units (√2 − 1)^i and φ^−j, Lucas/Fibonacci and
    Pell units) and 333 random ones.
  - The NF fields: 680 near-zero elements (powers and differences of the units β, ρ, 1 + 2^(1/3) + 4^(1/3),
    4 + 3·3^(1/3) + 2·9^(1/3), 5 + 2√6, 1 + 2^(1/4), φ) and 900 random ones.
  - The smallest |x| is 1.4·10⁻⁴³. 0 mismatches.
  - For comparison, float64 gets the sign wrong on 165 of the 529 near-zero elements of Q(√2, √5).
- **H. The bronze and heptagonal scales** (added at DICTO's request, 18 Nov):
  - Bronze: β = (3 + √13)/2 with β² = 3β + 1. Sign, product and inverse agree with `Quad` in Q(√13) on 1116 elements,
    β^−k included.
  - Heptagonal field, ρ = 2cos(π/7), σ = ρ² − 1:
    - ρ³ − ρ² − 2ρ + 1 = 0 and ρσ = ρ + σ.
    - c = cos 2π/7 = (ρ² − 2)/2 satisfies 8c³ + 4c² − 4c − 1 = 0.
    - T = 9 − 4c − 16c² satisfies x³ − 9x² − x + 1 = 0 exactly and equals tan(π/14)·tan(2π/7) to 140 digits.
    - 34 elements built from ρ, σ, c, T and the units ρ, σ: every sign and all 1156 comparisons agree with 150-digit values.
- **L. Libraries:**
  - The kernel sign equals the certified Arb ball sign (python-flint) on all 2476 elements of C1 and H4.
  - FLINT's factorisation finds every test field irreducible and (x² − 2)(x − 3) reducible.
  - sympy's `minimal_polynomial` gives x³ − 9x² − x + 1 for tan(π/14)tan(2π/7), x² − 3x − 1 for (3 + √13)/2, and
    x³ − x² − 2x + 1 for 2cos(π/7).
- **D. Cross-checks:**
  - MQ's interval sign equals the tower rule computed with `Quad` (862 elements).
  - NF over GOLDEN equals `Quad` (716 elements).
  - zphi equals NF over GOLDEN, and ints stay ints (669 pairs).
  - NF over x² − 2 equals `Quad(a, b, 2)` (1000 elements).
  - `Quad.sqrt` (2000 elements).
- **E. Guards:** mixed fields, floats, division by zero, the reducible (x² − 2)(x − 3), an interval with two roots,
  non-square radicands.
- **Not found:** a unit of the #56 field with coefficients ≤ 40 in Z[24t]. Its near-zero elements come from rational
  approximations of t instead (LEAD 3).

**Differential test: `tests/test_differential.py` + `tests/diff_fields.py`. FINAL ok** (data/differential.json).

- **How it works:**
  - Every copy is lifted from its study file with the AST; no study code runs.
  - Each operation is compared with the kernel's counterpart, which is the replay shim wherever one exists: + − × ÷,
    inv, conj, norm, sign, comparisons, abs, pow, iszero, float, dec, mp, hash and the printed form. For AlgField this
    includes `interval_value` and the bisection state after every call.
  - The elements are random (small and 9-digit) plus near-zero units of each field.
  - Where a copy and the kernel give a different sign, an independent 120-digit mpmath value decides which is right.

| Group | Copies | Comparisons | Result |
|---|---|---|---|
| G1 | 32 | 152 440 | all agree |
| G2 | 14 | 333 177 | all agree |
| G3 | 10 | 37 080 | all agree |
| G4 | 6 | 37 421 | all agree; octet K wrong on 10 signs (kernel = 120 digits) |
| G5 | 4 | 17 654 | all agree |
| G6 | 4 | 8 196 | all agree |
| G7 | 7 | 26 785 | all agree; web-of-bonds E wrong on 7 signs (kernel = 120 digits) |
| G8 | 7 | 29 832 | all agree |
| W (numpy Z[φ]) | 1 | 717 | agrees |

**Where copies refuse or are wrong:**

- octet_special_exact.py `K` reads its sign from a float, guarded by |f| > 10⁻⁹.
  - On near-zero units of Q(√6) with coefficients near 10⁹, the float error (about 10⁻⁷) exceeds the guard, and the
    copy returns a wrong sign 10 times. It refused 56 more by its guard.
  - It refuses 1/0 with StopIteration, and so does exactlib's RF.
- web-of-bonds `E` evaluates at 80 digits. On units of large height it returned 7 wrong signs and refused 1.
- In the replayed runs below, the numbers are small, and the kernel and the copies give the same output.

**Mutants.** One planted wrong copy per group (G1, G2, G4, G5, G6, G7, G8; 7 in all) is flagged on the planted operation.
A planted wrong sign is caught as "copy wrong at 120 digits".

## 4. Replays (replay/: cases.py, setup.py, swap.py, replay.py, shims/; data/replay.log, data/replay.json, data/replay/)

**Method.**

- Each case runs twice on the same machine. The trees:
  - **orig/**: the case's studies copied unchanged; other studies linked read-only.
  - **kern/**: the same, except the number code. `swap.py` replaces only the named top-level definitions with a few-line
    shim. data/replay-swaps.json lists every replaced line range.
- Study files themselves are not edited.
- **Compared:**
  - stdout, kern with orig and with the stored log;
  - every file the run writes, kern with orig and with the stored file.
- **Masked:** only elapsed times and the tree's own path.
- **Counted:** a case counts when the original finishes within 280 s with exit 0.
- The trees are rebuilt by setup.py and are not kept in the repository.

| Studies (group) | Cases | kern = orig | stdout kern = stored log |
|---|---|---|---|
| the pilot's 3 studies, re-run on this kernel (G1–G3) | 4 | 4 | 4 |
| shadow-forms octet_special_exact (G4, Q(k^(1/n))) | 1 | 1 | 1 |
| pds-hopscotch-line pds_line --pilot (G4, Q(√5)) | 1 | 1 | no* |
| golden-cuts-beyond-plato s9 A–E, s10, s11 (G4, Q(√2, √5)) | 7 | 7 | (JSON only) |
| 6d-golden-cubes s1–s4, dual-pairs-dimensions s1–s8 (G4) | 19 | 19 | (JSON only) |
| get-mixing: pilot_lib, layers, 3 patches, 2 free patches, decorated, decorated-sft (G5 + G6) | 9 | 9 | 7 of 9* |
| grunbaum-k10: vclass3, search6-pilot, cover6, cover-gnomon, verify, gnomon-sources (G6) | 6 | 6 | 6 |
| get-palomar gen_data (G6, getgeom + the k10 zsurf) | 1 | 1 | (JSON + Lean data) |
| atoms-missing-2: 8 builds incl. build_keyed in Q(t) (G7 + exactlib QF) | 8 | 8 | 8 |
| atoms-missing: hexoct, octet, mine xy/towers/polar (G7 + QF) | 5 | 5 | 4 of 5* |
| **all** | **61** | **61** | |

\* **Where the stored output differs, the original run differs the same way.** The kernel is not the cause:

- pds-line-pilot.log was written by an earlier version of the script.
- In the free-patch logs, a dict prints its keys in another order. This is hash-order in the stored run.
- build_octet.log came from a different part list.

**Files.**

- All 223 written files are identical between kern and orig.
- 166 are also identical to the stored files. For the other 57, the original run's file differs from the stored file in
  the same way. The stored files were
  edited after the runs (D-number notes in the model JSON, labels and a later MAXLEN in dual-pairs JSON, and the fans-law
  JSON whitespace noted by the pilot).

**Not counted** (3): atoms-missing build_dharma, build_early and build_mine shield. They read `ref/*.json` dataset files
that are not in the study, so the original fails here too.

**Not replayed:**

- **Over 5 minutes:** pds_line full (469 s); grunbaum-k10 tile4/tile12, gnomon and search6; get-mixing corona_enum (20 workers).
- **Arguments not recorded:** get-mixing neighbours (max solutions); atoms-missing turn.py, build_tq (needs state files).
- **Law-giving census:** its K holds python-flint `fmpq` numbers, which its polynomial class E and arb balls read directly
  (`.a.p`, `fmpq_poly([k.a])`). A Fraction kernel cannot stand in without editing those lines. Its arithmetic and signs are
  covered by the differential test.
- **G8 copies and the golden Q5 of echo_lib/qlib:** covered by the differential test only. They have no shim yet.

## 5. What stage 2 needs

- **Switch the studies:**
  - A module copy (cubes_lib.py, exactlib.py, zsurf.py, mixlib.py, q5.py, qf.py) switches with its shim, as replayed here.
  - Inline classes (octet K, pds_line K, the G1/G8 classes) need an edit at the class.
  - Finished studies stay unchanged and are covered by the differential test and the replays.
- **Write G8 and golden-Q5 shims** (styles and hashes are already in the kernel), and replay their studies.
- **Polytope tools and the inline norm tests (40 files):** these are geometry on top of the numbers. They are stage 2
  ("shapes as exact objects").
- **The law-giving census:** a kernel element whose rationals can be python-flint `fmpq`, or an edit of its E class.

## 6. Risks

- **Byte-identical output depends on matching each copy's printed form, float formula and hash.**
  - The kernel carries 30 quadratic styles, 5 NF styles, 5 NF float formulas and 2 MQ styles for this.
  - Example: residents.py rounds φ before multiplying; mixlib multiplies first. The last bit differs.
- **Floats:**
  - The rule above accepts small dyadic floats. One replayed study (s10_honeycomb_cubes) needed it: it failed under the
    first, stricter rule.
  - A study that builds a number from a float such as 0.1 now stops with TypeError, where the copy used the binary value.
- **Interval state:**
  - Kernel and copy fields that are driven by the same calls refine identically (checked).
  - The kernel's own fast quadratic path is never used for a field a study builds as AlgField.
- **Coverage:** the replays cover module copies and three inline classes. The other inline copies rest on the differential
  test alone.
- **Environment:** gmpy2 is absent on the compute machine. The R5 copies were lifted with Fraction for `mpq`, which is the
  same rational arithmetic, but they were not run on gmpy2 itself.

## 7. LEADS

1. Two copies give wrong signs that their guards miss:
   - octet_special_exact.py `K`: a float guard of 10⁻⁹.
   - web-of-bonds lib.py `E`: 80 digits.
   Both happen on near-zero elements with large coefficients. Check whether any stored result of those studies came near
   these bounds; the replay of octet-special-exact agrees exactly.
2. 110-exact common.py `zsign` decides by float when |a + bφ| ≥ 0.01. For coefficients near its 2^50 limit, the float
   error (about 0.1) exceeds that. No wrong sign was found in 100 large near-zero tests, but the bound is not proved.
   It is an independent check: fix it there, not by the kernel.
3. A unit of the #56 field (1536t³ + 5184t² − 3384t + 11) was not found with coefficients ≤ 40. A class-group/unit
   computation (e.g. PARI bnfinit) would give a stronger near-zero test set for that field.
4. sqrtQ ×3 search for square roots over small denominators by float. `Quad.sqrt` is exact and always finds the root when
   one exists. Where a copy returns None, a root may still exist.
5. The law-giving census: a kernel element over python-flint rationals would bring its 3 E-based scripts in.

Every test and run script (inventory, test_kernel, test_fields, test_differential, setup, replay) ends with a FINAL ok / FINAL FAIL line that depends on its checks; swap.py, cases.py and diff_fields.py are helpers. The replay trees and the studies source copy live only on the compute machine. Nothing outside this folder was changed.
