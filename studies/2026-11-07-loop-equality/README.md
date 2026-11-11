# Loop Equality as a theorem (paper #102, 7 November 2026)
DICTO's Loop Equality (#74, conjecture) proved: closed non-backtracking loops per site are the same at every site of every
close-packed tetrahedral stacking (periodic or not), every length; corollaries for the pyrochlore network and close-packed spheres.
Paper: papers/2026-11-07-loop-equality/paper.html. Prior art: closed walks equal = Nagle 1966 (ice), Thorpe 1972 (all polytypes).
- loop_checks.py: exact integer checks on 42 stackings (686 sites); run on compute-host as two parts:
  `loop_checks.py 30 24 14 12 tetra` (88 s) and `... other` (122 s); outputs concatenated in data-loop-checks.txt; both FINAL ok.
- fig102.py data-loop-checks.txt OUTDIR: figures fig1-proof.png, fig2-every-site.png.
CONCLUSION: theorem proved (Fourier over layers + reduction of NB loops to walks between bond ends); checks all agree.
LEADS: update #74 and HexOct ch. 13 / open problem (1); credit Nagle and Thorpe there; OEIS candidates 1, 2a, 2b can cite #102.
