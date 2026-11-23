# Certifying and extending the Aequi (24 November 2026)

**Status (work in progress):** Part 1 done: all 1232 certified (1229 by Krawczyk on a box of constant type, 3 by a split box across a change of type). Part 2 and Part 3 running. Resume: see "Resume" at the end.

Part 1 counts: data/certify-summary.md; per die: data/certify-table.csv.

## Resume
Scripts in scripts/; Part 1 reruns in under a minute on 22 cores: `certify.py data/certify-pass1.jsonl 22`, `accidental.py data/accidental.json`, `structural.py data/certify-pass1.jsonl data/structural.json`, `line504.py`, `summarize1.py` (python with python-flint, scipy, sympy).
