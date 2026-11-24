# OEIS checks for Entry 2 (4H h-site coordination sequence) and Sweep 1 (pyrochlore closed walks), 24 Nov 2026

Run on the compute host (Python 3, sympy, cypari2 = PARI/GP 2.19); outputs in data/. Result: data/compare-out.txt, FINAL ok.

- Study scripts rerun: oeis_checks.py (2026-11-07; output identical to its data-oeis-terms.txt except the C4 line, whose
  input file was not copied), pyrochlore.py (2026-11-18 sweep, FINAL ok), walks.py 30 (2026-11-08, FINAL ok);
  entry2_prog_as_written.py = the ENTRIES.md Entry 2 program with the length as an argument.
- Fresh second methods: fresh_4H_geometric.py (bonds found by exact distance in the ideal crystal, n <= 200, all four
  h-site atoms; c-site atoms equal the A008264 b-file to 200); fresh_pyrochlore_linegraph.py (diamond's bonds as sites,
  n <= 40).
- pari_checks.py, page_programs.py: every program printed on the working pages, run as printed.
- gf_facts.py: entry 2 g.f. reduced, recurrence from n = 11, a(8m+k) forms; data-line lengths.
- compare.py: term-by-term comparison; writes the b-files to papers/oeis-submissions/working/.
