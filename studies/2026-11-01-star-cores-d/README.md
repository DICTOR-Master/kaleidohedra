# 2026-11-01 Star Cores paper D: eccentric pieces (the valley law)

Conclusion: the valley law holds. At an edge of dihedral angle δ = α + α′ the k-th full spike meets the edge at
tan γ_k = (t − 1)^k tan α; both spikes of step k fit only if β_k = 360° − δ − Σ(γ_j + γ′_j) ≥ 0; a closed valley never grows
again. At t = 2: step k needs (k + 1)δ ≤ 360°. The sharpest dihedral angle (≤ 120° or not) splits the 44 convex shapes of the
#79 valley runs exactly: 14 sharp shapes keep growing (≥ 16.5 % at step 3), 30 round ones add ≤ 4.2 %. Status: draft paper D
(papers/star-cores-d), not published.

Run on dicto-big-brother (~/kres-tmp/star-cores-d, ~/geom/bin/python, 4 processes, float64), dataset DICTO Solids v6.
- scripts/valley_law.py: part 1, α, α′, δ (checked against the face normals, max error 0) and β_k for every edge of the 50 shapes
  of star-valley.json, against its full-spike counts (data/valley-law-predict.json; bound check: 0 violations in 100 runs);
  part 2, the valley rule rebuilt and instrumented for the seven pieces + D7, D29, D40, D41, D89 at t = 2 and φ
  (data/valley-law-run.json, valley-law.log): formula error ≤ 4.4e-15 rad, closed-yet-full 0, regrown after closing 0.
- scripts/valley_law_extra.py: the same for D1–D3 (valley-law-run-extra.json, valley-law-extra.log).
- scripts/figs_paper_d.py: Figures 1 (valley-law.png) and 2 (pieces.png) of the paper; data/figs-info-*.json.
Imports star_core.py, star_valley.py, figs_paper_a.py from studies/2026-10-30-star-cores/scripts.
