# Reproductions (aiXiv), 12 November 2026: three papers by Tang

Author's published code rerun (kind A), every claim it checks; code read first (imports, file and network use); run on the compute machine.

| aiXiv | paper | code | result |
|---|---|---|---|
| 2611.00582 | Tang, Counting low-degree cluster variables in Grassmannians | github.com/tqyqiqi1509/grassmannian-low-degree-counts @78ca431, code/verify_all.py (python-flint 0.9.0) | PASS in 2.7 s: Gr(3,n) deg 4 coefficients 0/288/400/264/52 and Gr(4,n) deg 3 174/855/1285/693/123 (supports 8-12), equal to the paper's table; upper = lower sets exactly; 60,400 mutations replayed; 31 input hashes checked |
| 2611.01161 | Tang, Lusztig's Fourier matrix conjecture for finite noncrystallographic Coxeter groups (H3, H4) | package Lusztig_Fourier_Conjecture_Complete_Package.zip (repo tqyqiqi1509/lusztig-fourier-conjecture), source_package/verify.py | main chain PASS in 15 s: manifest, independent checks, residuals, label uniqueness, full 74 x 74 certificate (5476 entries, twist order 60, error < 3.4e-140, separation threshold met: S = F exactly). All 7 additional checks (his pinned numpy 2.3.5, scipy 1.17.0, python-flint 0.9.0, SymPy 1.14.0) exit 0 and their outputs are identical to his recorded runs (timings and paths aside): independent H4 words, independent small matrices, small formulae, ring and dimension, rank-2 parameter, fresh certificate checks (PASS), rebuilt missing actions (PASS). COMPLETE  Logs: lusztig-run/ (paths replaced by <workdir>). Package zip sha256 b529ae96...a18. |
| 2611.00157 | Tang, A counterexample to the equality characterization in Wahl's codimension-two conjecture | github.com/tqyqiqi1509/wahl-equality-counterexample @7c00a00, verify.py (standard library) | ALL EXACT CHECKS PASSED, exit 0, 0.09 s (run by DICTO in this session) |

Run by Claude Code (Opus) for DICTO.
