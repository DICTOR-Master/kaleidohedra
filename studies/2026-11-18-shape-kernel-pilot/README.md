# Shape kernel, stage 1 pilot: one kernel of exact numbers (18 Nov 2026)

Plan: `papers/plan-shape-language.md`, stage 1 ("Kernel of exact numbers"), pilot on the three most-copied modules.

**Question.** Can the exact-number code that the studies copy from one to another be replaced by one module that gives
the same results, checked against every copy and against stored study outputs?

**Answer.** Yes, for the three most-copied groups: 56 copies in 48 studies agree with the kernel on every operation they
provide, and three study runs (4 scripts) give byte-identical output with the kernel in place of their number module.

## 1. Inventory (scripts/inventory.py, data/inventory.json, data/inventory.log)

The Concordance code map (`papers/dicto-concordance/code_map.py`) records a copy as a function name defined in 3 or more
studies. It does not group whole classes, so `inventory.py` scans all 2515 study scripts with the AST and groups the
number classes and pair functions directly. Number-class names such as `add`, `sign` and `inv` in the code map
(20, 17 and 17 scripts) mostly point to these same copies.

| Group | What | Copies | Studies | Distinct sources | Identical sets |
|---|---|---|---|---|---|
| G1 | Q(√5) as a class `Q5` / `Q` (a + b√5, Fractions) | 32 | 27 | 30 | q5.py ×3 (turn-theorem, regular-stars-census, icosahedral-line) |
| G2 | Q(√d) as a class `QF` (d = 2, 3, 5, 6) | 14 | 14 | 9 | qf.py ×3 (dicto-vacuus, vacuus-origami, platonic-fans-law); qf.py ×3 (splash2-approximants, ab-turn, icosahedra-fill); exactlib.py ×2 |
| G3 | Q(√5) as Fraction pairs (`q, qa, qs, qm, qn, qr, qinv, qd, qf, sgn, qsgn, cmp, qsum, qstr, qs_`) | 10 | 8 | 7 | q5.py ×4 (bcc-golden-kit, ocd-octet, p4-golden-octet-adaptor, harmonic-gaps) |

The code map also finds two related groups that the pilot does not cover: `K` = Q(√2, √5) and similar four-term fields
(6 copies, 3 of them the identical cubes_lib.py), and a + b·φ in the golden basis (mixlib.py, 1 copy). Other related
code: zsurf.py's Z[φ] (2 copies) and the cubic-field classes in exactlib.py (2 copies).

**How the copies differ.** The arithmetic and the sign rule are the same in all 56 (checked, §3). They differ in:

- **Methods provided.** Every copy has `+` and `*`. `sign` appears in 19 of the G1 copies, `<` in 9, `floor` only in
  G2, and `__pow__`, `__abs__`, `norm` and `conj` (also called `gal` or `sig`) in a few.
- **Printed form.** There are 26 different `repr`/`str` texts, e.g. `(1/2 + 3/2*sqrt5)`, `(1/2+3/2r5)`,
  `(1/2) + (3/2)√5` and `1/2 − 3/2√5` (with a Unicode minus).
- **Hash.** Most copies use `hash((a, b))`. yarr.py and yantra_regions45.py use `hash(a)` for rationals, which matches
  `==` with plain integers.
- **Field handling.** Some copies use a class-level `QF.D` that `field()` sets per run. Others store `d` in each element
  and refuse mixed fields. sri-yantra makes one subclass per field, and `D` can be a Fraction there.
- **Float.** All copies use the double-precision sum except yantra_regions45.py, which uses mpmath at 60 digits.
- **Equality.** Four copies have no `__eq__`, so `==` compares object identity: dial_a5.py, polar_hafner_exact.py,
  gbpc_periodic_count.py and sri-yantra quadfield.py. See LEADS.
- **Name clash.** `qstr` means a √5 text in two copies and an `a|b (float)` text in three fable-review scripts.

## 2. Design (kernel/)

- `kernel/exact.py`: one element type, `Quad(a, b, d)` = a + b√d.
  - a and b are Fractions; d is any positive rational that is not a square (Q, Q(√2), Q(√3), Q(√5), Q(√6) and more).
    A square d is reduced to a rational.
  - Rationals combine with every field. Two different irrational fields raise `ValueError`.
  - Exact sign by the rule every copy uses (same signs win; otherwise compare a² with d·b²). Exact `== < <= > >=`,
    `floor`/`ceil`, `norm`, `conj` (aliases `gal`, `sig`), `inv`, integer powers (including negative ones) and `abs`.
  - Conversions: `float` (the copies' double-precision sum, so printed floats stay the same); `float_hp` (from at least
    20 exact digits, no cancellation, matching the mpmath copy); `digits(n)` (exact decimal string); `dec` (as in
    exactlib); `sympy()`.
  - `parse` reads pair text, the parsable form and to_str forms; anything else goes to `parse_sympy`.
  - `cos2_exact`, `rational_pi` and `rational_pi_float` come from the qf.py copies.
  - Floats are refused in arithmetic and comparison (`TypeError`). Copies silently turned a float into its exact binary
    Fraction. This is the one deliberate change.
  - Class settings, so a study can keep its own output: `D` (default field), `HASH_PAIR` (copy hash) and `STYLE` (one of
    26 named printed forms in `STYLES`, covering every copy's form). Results keep the more derived class, so a study's
    subclass keeps its printed form.
- `kernel/pairs.py`: the G3 function names on plain Fraction tuples, computed by `Quad`. `qstr` (√5 text) and
  `qstr_float` (the fable form) resolve the name clash.
- `kernel/vec.py`: exact vector helpers. The container follows the input (tuple or list) unless `out=` is given, so
  q5.py (tuples) and qf.py (lists) are both reproduced.

A study switches by replacing its number class with a few-line subclass that names its style, hash and field (see
`replay/shims/`).

## 3. Tests and results (all ran on a compute machine; logs in data/)

**Kernel tests: `tests/test_kernel.py`. 37 checks, 0 failed, FINAL ok** (data/test_kernel.log).

- Checks ported from the copies' asserts:
  - φ² = φ + 1 and 1/φ = φ − 1.
  - The icosahedral frame: 12 five-fold and 20 three-fold axes, each three-fold axis nearest to exactly 3 corners at
    φ² (the q5.py assert, done exactly here instead of in floats).
  - The icosidodecahedron's 30 corners at |v|² = φ².
  - Mixed fields refused; a square field parameter is rational.
  - The cos 2πk/n table, and `rational_pi` on the apex angles in the Vacuus census log.
  - Pair round trips and parse round trips.
- Field and order axioms on 3000 random triples over d = 2, 3, 5, 6: associativity, commutativity, distributivity,
  identities, inverses, conjugation as an automorphism, multiplicative norm and sign, trichotomy, order compatible with
  + and with positive ×, transitivity, powers, floor/ceil, hash consistent with ==, parsable round trip, abs.
- Sign against high-precision decimals. 3000 random elements with 12-digit parts, plus 454 near-zero units
  (L_n − F_n√5 and Pell units in √2, √3 and √6), all with magnitudes below 10²⁹ so that 60 digits decide.
  - The exact sign equals the sign at 60 digits (Python decimal) and at 80 digits (mpmath) on all of them.
  - For comparison, float64 gets the sign wrong on 250 of the 454 near-zero units.
  - `digits(50)` agrees with the 60-digit value to 10⁻⁴⁹.

**Differential test: `tests/test_differential.py`. FINAL ok** (data/differential.log, data/differential.json).

- How it works:
  - Each of the 56 copies is lifted from its study file with the AST. Only imports, function and class definitions,
    and simple constants are run; no study code runs.
  - Every operation the copy has is compared with the kernel's on 300+ elements per field, including Lucas/Fibonacci
    near-zeros: + − × ÷, neg, inv, conj, norm, pow, abs, sign, == and the four comparisons, floor, float, dec, the
    zero test and hash.
  - Each copy's repr/str is matched to a kernel style.
- Result: all 32 G1, 14 G2 and 10 G3 copies agree on every operation they provide (several thousand comparisons per
  copy). Every copy's printed form is reproduced by one named style.
- Harness self-test: two planted wrong copies (sign comparing |a| with |b|; product with √5 fixed in a √d class) are
  flagged, on `sign` and on `*`.

**Replay: `replay/setup.sh` + `replay/replay.py`. FINAL ok** (data/replay.log, data/replay.json, data/replay-*.log).

- Method:
  - Each script runs twice on the same machine: as stored in its study (`orig/`), and with only its number module
    replaced by a kernel shim (`kern/`). The scripts themselves are unchanged.
  - Both outputs are compared with each other and with the outputs stored in the study.
  - Only elapsed-time fields (`<n> s`) are masked.

| Case (group) | Script | Output | kern = orig | kern = stored |
|---|---|---|---|---|
| paradigm-exact (G1, q5.py `Q5`) | hemi_exact.py | 33 lines | identical | identical |
| paradigm-exact (G1) | scutoid_exact.py all | 41 lines | identical | identical |
| platonic-fans-law (G2, qf.py `QF`, class-level field) | fans_law.py, 389 solids | 106 lines + fans-law.json (2.9 MB) | identical, both | log identical; JSON equal as data* |
| ocd-octet (G3, pair q5.py via exactpoly.py) | step12_exact_faces.py | 13 lines + step12-faces.json | identical, both | identical, both (no masking needed) |

\* The stored fans-law.json has the same content but different whitespace (1.92 MB against 2.91 MB): it was rewritten
with other formatting after the run. The re-run original gives the same bytes as the kernel (data/fans-law-json-check.txt).

In the paradigm-exact shim, the polytope tools (facets, Body, disjoint, …) are the original module's text, unchanged.
`diff` confirms this. They belong to stage 2.

## 4. What stage 1 proper would take

- **Fields still to add to the kernel:**
  - the four-term field K = Q(√2, √5): 6 copies;
  - the golden basis a + b·φ: mixlib.py;
  - Z[φ] in zsurf.py: 2 copies;
  - the cubic fields and RF of exactlib.py: 2 copies.
  These need a general number-field element: a tower of quadratic fields, or polynomial arithmetic modulo a minimal
  polynomial, with exact sign by isolating intervals.
- **Inline arithmetic:** the remaining Q(√2)/Q(√3) code inside single scripts, found by a wider scan (functions such as
  `conj2`, `conj5`, `sqrtQ`, `exact_volume` and `faces_exact` in the code map).
- **Switching the studies:**
  - 48 studies carry a copy from the three pilot groups. Each needs a shim of a few lines (style, hash, field) or one
    import line.
  - Studies that import a shared module copy (q5.py, qf.py, exactlib.py, cubes_lib.py) switch by replacing that one
    file. Scripts with an inline class need an edit at the class.
  - For finished studies, the pilot's method keeps this safe: leave the study files unchanged, and prove equivalence
    with the differential test, plus a replay wherever a stored log exists.
- **The outcome check:** extend `tests/test_differential.py` to every group, and replay every study that has a stored
  log and a run under 5 minutes.

## 5. Risks

- **Byte-identical replays depend on matching each copy's printed form and hash.** The kernel carries 26 styles for
  this. A cleaner kernel would print one form, but then old logs could not be re-checked byte for byte.
- **Floats are refused in arithmetic.** Copies that silently took a float (as its exact binary value) would now raise
  an error. This did not happen in the replays. It is deliberate: an error is better than a silent wrong value.
- **Mixed fields now raise an error.** Copies with a class-level `QF.D` reinterpret old elements when `D` changes; in
  the kernel an element keeps its own d. This gives the same results when a script does not mix fields; that was
  checked only in the replays and the differential test.
- **Library versions.** The replays agree with outputs stored under older numpy/scipy versions, but scripts that use
  float hulls could differ under future versions. That would come from the float filtering, not from the kernel.
- **Coverage.** The differential test only checks what each copy provides. The extra kernel functions (`digits`,
  `float_hp`, `parse`, negative powers) are covered by test_kernel.py alone.

## 6. LEADS

1. Four copies compare by object identity because they have no `__eq__`: dial_a5.py, polar_hafner_exact.py,
   gbpc_periodic_count.py and sri-yantra quadfield.py. Check whether their scripts use `==`, `in` or sets on these
   numbers. If they do, a result could be affected. Not yet checked.
2. The four-term field K = Q(√2, √5) (cubes_lib.py ×3 and 3 others) is the next group for the kernel.
3. The near-zero units (L_n − F_n√5 and Pell) are a ready test set for the cubic fields of stage 1 proper.
4. The float filter in fans_law.py takes the float sign above 10⁻⁶. `float_hp` makes a cancellation-free filter
   possible.

Files: `kernel/` (exact.py, pairs.py, vec.py), `tests/` (test_kernel.py, test_differential.py, mutants/),
`replay/` (setup.sh, replay.py, shims/, cases/), `scripts/inventory.py`, `data/` (logs and JSON). Nothing outside this
folder was changed. Nothing was committed or published.

Every script ends with a FINAL ok / FINAL FAIL line.

**LEAD 1 checked for the Yantra (18 Nov):** sri-yantra quadfield.py has no __eq__, but its one user, quadratic_family.py, tests zero with is_zero() and never compares QF values with == or uses them in sets/dict keys: #103 Theorem 1 checks are unaffected. The other three (dial_a5.py, polar_hafner_exact.py, gbpc_periodic_count.py) remain to check.
**LEAD 1 closed (18 Nov):** dial_a5.py tests its Q5 values with .z() (exact zero) and its == 0 tests act on Fractions only; polar_hafner_exact.py compares .a and .b explicitly; gbpc_periodic_count.py never compares the numbers. None of the four identity-equality copies affects a result.
