# Polyhedraverse claims audit (2026-10-31)

DICTO's request: check every statement made in his name or about his work in ~/polyhedraverse
(github.com/DICTOR-Master/polyhedraverse, archived; text mostly written by Claude Sonnet in September 2026)
for overclaims, and flag his legal name in public text.

**Conclusion:** 88 claims checked: 41 accurate (A), 28 overclaims (B), 19 not checkable as written (C).
The 4D write-up (docs/radial-cell-projection.md) was already corrected on 24 Sep. What is left there is
test coverage ("every adjacent pair" is checked on one pair), the Schläfli credit for the tetrahedron's three
closures, and a dated provenance naming DICTO's fold (11 Sep), the name RCP (15 Sep) and RCP-C2B (16 Sep).
The serious overclaims: "DICTO's Zometool discoveries" covering classical stellations; RVCMG set apart from
edge collapse without citing Hoppe 1996; "proved" for a finite check (composite-seed REPORT); "uniquely, in four";
"duoprism" for a polyhedral prism.
**Status:** report done (report.html, PDF in ~/Documents/papers-to-read/pv-claims-audit.pdf); nothing in
~/polyhedraverse changed. Legal name: 12 occurrences fixed locally in 567b37f, not public (repository archived);
jamesbaker08@gmail.com still in PRIVACY/SECURITY/TERMS/CODE_OF_CONDUCT; git history (cd847fb, 556a536, dee53eb, 16ddf9d) unchanged.

## How
Read the files listed in report section 11, read the engine and test code, and ran
verify:radial-projection, verify:rcp-build and verify:stellations on dicto-node (all passed).
Printed with `~/kres-print/print.mjs` on dicto-node (the report is copied to paper.html there).
