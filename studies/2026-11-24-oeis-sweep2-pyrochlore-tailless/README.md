# Sweep 2 for OEIS: closed tailless walks per pyrochlore site (24 Nov 2026)

DICTO · checks for the OEIS working page papers/oeis-submissions/working/sweep2-pyrochlore-tailless.md.

**Result.** a(n) = the number of closed cyclically non-backtracking (tailless) walks of length n at a site of the pyrochlore
network, n = 1..40. Two independent methods give the same terms, and the terms match #102, Corollary 2 (a(1..8) printed).
Not in the OEIS (searched 24 Nov).

**Methods.**
- `scripts/direct_count.py`: the network is built as the line graph of diamond, and the walks are counted by dynamic
  programming over (site, previous site). No formula is used. Output: `data/direct-n40.txt`.
- `scripts/formula_check.py`: exact rational power series for two formulas. Both equal the direct count for n = 1..40.
  - The log form: Ihara–Bass for a 6-regular net (Bass 1992; Ihara 1966), with the pyrochlore spectrum −2 (weight 1/2) and
    2 + μ (weight 1/2), where μ runs over diamond's spectrum with even moments A002895.
  - The ordinary g.f. in A402231's shape.
- `scripts/prog_check.py`: the proposed %o program, run as written. It equals the direct count.

**Files.** `data/b-sweep2.txt` (b-file, n = 1..40), `data/formula-check.txt`, `data/prog-out.txt`.

**Sources checked.** #102 (released PDF, Corollary 2 and its proof); OEIS A400949 and A402231 (model entries); OEIS search.
