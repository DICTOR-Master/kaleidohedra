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

## 2026-11-01 (later) Kagemusha's notches: is its growth the valley law at the reflex edges?

Conclusion: no. The law applies unchanged at the five reflex edges and shuts them at step one; more than that, the ten faces next to
them never take a spike at all (0 % of the growth at every step, notch open at exactly 360° − δ = 158.38° throughout). Kagemusha
grows on its other 20 faces: by cut-back spikes in its convex 138.19° valleys (t = 2), at φ also in the law's own open valleys
(step two), and at step three mostly on the ridges of its cap spikes. Corollary for non-convex pieces: a notch whose two centre
feet lie beyond the edge (α, α′ > 90°) and with β₁ < 0 stays empty for ever. Status: study note; paper D not edited.

Run on dicto-big-brother (~/kres-tmp/star-cores-d, ~/geom/bin/python, one process), dataset DICTO Solids v7 (dicto-shadow-17.json).
- scripts/kagemusha_notches.py → data/kagemusha-notches.json, kagemusha-notches.log. Part 1 exact (sympy, Q(√5)); part 2 the valley
  rule of star_valley.py rebuilt with every spike's volume put to its site; Σ spike volumes = volume gained at every step (to 1e-12).

1. Edges (exact; centre O = corner centroid = pentagon centre; δ = α + α′ checked against the face normals at all 45 edges).

| edges | δ | tan α, tan α′ | α, α′ | β₁, β₂, β₃ at t = 2 | at t = φ |
|---|---|---|---|---|---|
| 5 reflex (notch 158.38°) | 201.62°, cos δ = −(5 + 4√5)/15 | −(3 + √5), −(3 + √5) | 100.81°, 100.81° | −43.25, −244.87, −446.50 | −55.97, −289.10, −547.05 |
| 10 convex "A" | 138.19°, cos δ = −√5/3 | φ², φ² | 69.09°, 69.09° | 83.62, −54.57, −192.76 | 105.25, **+15.25**, −48.19 |
| 10 convex "B" | 138.19° | (18 + 2√5)/19, 18 + 8√5 | 49.79°, 88.40° | 83.62, −54.57, −192.76 | 98.23, −11.91, −110.78 |
| 20 convex "C" (beside a notch face) | 138.19° | (6 + 4√5)/11, 6 + 2√5 | 53.64°, 84.55° | 83.62, −54.57, −192.76 | 100.58, −2.81, −88.57 |

   Does the derivation carry over to a notch? Yes: it uses only e and the two face pyramids; the plane (O, e) is the pentagon plane,
   inside the solid, so α + α′ = δ holds and β₀ = 360° − δ is the notch angle. The law gives β₁ < 0: no two full spikes even at step one.
   Where a notch differs: ρ < 0 on both faces (the foot of O lies beyond e, since α > 90°). Then the spike's angle at e,
   γ(s) = atan2((s − 1)d, ρ), RISES towards 180° as the spike is shortened (s → 1), so shortening never makes room:
   γ(s) + γ′(s) ≥ γ(t) + γ′(t) = 360° − δ − β₁ > 360° − δ for every s in (1, t]. The two spikes cross at every common height, the
   rule's pair shortening ends at flat, and a flat face has the same base and partner next step: flat for ever. (At a convex edge ρ > 0,
   γ(s) → 0 as s → 1, so a cut-back height always exists.) Run check: at s = t the notch spike is free of the old pieces; near s = 1 it
   meets the mirror face's pyramid; the pair rule flattens it.
2. Prediction per step: notches shut at step 1 and empty at steps 1–3, both t. Convex edges: none open at step 2 at t = 2; at φ the ten
   A edges stay open through step 2 (β₂ = +15.25°; 138.19° < 142.08°, the equal-sided bound for step 2), none through step 3. The C
   valleys are one-sided (the notch face never spikes), so the two-sided β does not bound them.
3. Measured (share of the volume gained; full / cut / flat spikes):

| t, step | volume × | notch faces | A valleys | B valleys | C valleys | ridges of cap spikes |
|---|---|---|---|---|---|---|
| 2, 1 | 1.7405 | 0 (10 flat) | — | — | — | — (20 cap faces full: 100 %) |
| 2, 2 | 1.3115 | 0 (flat) | 52.9 % (0/20/0) | 15.3 % (0/20/0) | 31.8 % (0/9/11) | — |
| 2, 3 | 1.1227 | 0 (flat) | 0 | 0 | 39.9 % | 60.1 % |
| φ, 1 | 1.4577 | 0 (10 flat) | — | — | — | — (20 cap faces full: 100 %) |
| φ, 2 | 1.5045 | 0 (flat) | 43.6 % (20/0/0) | 23.1 % (0/20/0) | 33.3 % (20/0/0) | — |
| φ, 3 | 1.1889 | 0 (flat) | 0 | 0 | 6.8 % | 93.2 % |

   Steps 2–3: ×1.472 at t = 2, ×1.789 at φ (paper D's ×1.47, ×1.79). The reflex opening is 158.375° after every step. Fits the
   prediction: notches empty; A full at φ step 2 and shut at step 3; B never full; 0 full at t = 2 step 2.
4. One line: the notch hypothesis fails (notches add nothing); Kagemusha's growth is cut-back spikes in its 138.19° valleys, the law's
   open A valleys at φ step 2, the one-sided C valleys beside the dead notch faces, and at step 3 the ridges of its cap spikes.
   Note for paper D (not edited): "the law does not explain its growth" is too strong at φ step 2, where the law predicts the ten open
   A valleys; the step-3 ridge growth is the open point the paper already lists (ridges of the stars).
- The other six eccentric pieces (Lahdeli, Chucky, Triskelion Tetrahedron, Dodeca-13 Wedge, Samson, Fang): convex, 0 reflex edges
  (normals check, v7 flags agree); the corollary concerns Kagemusha only.

## 2026-11-01 (evening) Kagemusha's notches filled: conjoined spikes and sloping bases (DICTO's proposal)

Conclusion: both variants fill the five notches at step one (no notch piece meets the solid or another piece; every surface closed,
Euler 2, volumes add up exactly). Conjoined spikes make Kagemusha grow more (×3.058 after three steps at t = 2, against ×2.563 with
today's rule) and it keeps growing at both t. With sloping bases it grows less at t = 2 and FREEZES there at step three (×1.000000000),
while at t = φ it grows most (×2.715 against ×2.607). Neither notch piece is a named shape: the conjoined piece is an irregular
combinatorial octahedron, the sloping pair an irregular triangular dipyramid. Status: study only (variants of the rule, not in paper D).

Run on dicto-big-brother (~/kres-tmp/star-cores-d, ~/geom/bin/python, one process, float64), DICTO Solids v7.
- scripts/kagemusha_variants.py → data/kagemusha-variants.json (+ step-1 surfaces), kagemusha-variants.log;
  scripts/kagemusha_variants_fig.py → data/kagemusha-variants.png (step-1 surfaces; gold solid, violet cap spikes, teal notch pieces).
- Notch e = (a, b), notch faces (a, b, c), (a, b, c′), full step-1 tips T, T′. (a) Conjoined: one piece hull(a, b, c, c′, T, T′) per
  notch; it lies outside the solid, so no clipping was needed. (b) Sloping bases (DICTO's sloping-base rule read for a notch: pyramids
  whose sloping sides meet at a shared point): each notch face keeps a pyramid with apex X, where the line c → T meets the notch's mirror
  plane (the pentagon plane); the two pyramids meet face to face on (a, b, X) (X = X′ to 0). The 20 cap faces: valley-rule spikes,
  all full at step one in every run. Steps 2–3: the valley rule unchanged.

| variant, t | step 1 × | step 2 × | step 3 × | after 3 steps | surface after step 1 (V, E, F) | notch piece |
|---|---|---|---|---|---|---|
| today's rule, 2 | 1.7405 | 1.3115 | 1.1227 | 2.563 | 37, 105, 70 | none (flat) |
| conjoined, 2 | 2.0354 | 1.3216 | 1.1368 | 3.058 | 47, 135, 90 | octahedron (6 corners, 8 triangles), vol 0.2218 |
| sloping, 2 | 1.9404 | 1.3102 | 1.0000 | 2.542 | 42, 120, 80 | 2 tetrahedra = triangular dipyramid, 2 × 0.0752 |
| today's rule, φ | 1.4577 | 1.5045 | 1.1889 | 2.607 | 37, 105, 70 | none (flat) |
| conjoined, φ | 1.6236 | 1.4830 | 1.1032 | 2.656 | 47, 135, 90 | octahedron, vol 0.1248 |
| sloping, φ | 1.5869 | 1.4521 | 1.1784 | 2.715 | 42, 120, 80 | triangular dipyramid, 2 × 0.0486 |

  (Kagemusha's own volume = 1; "after 3 steps" = volume over the solid.) Full / cut / flat spikes, steps 2 and 3: conjoined t = 2
  10/80/0, 20/20/230; conjoined φ 30/60/0, 40/70/160; sloping t = 2 0/80/0, 0/10/230; sloping φ 20/40/20, 40/70/90.
- Chain: over three steps no variant closes except sloping bases at t = 2, which freezes at step three (its 10 cut spikes add nothing
  measurable); the other three keep growing. The core-turn cycle of the new solids was not computed.
- Named or new: no known name fits; the conjoined octahedron has outer edges 0.507, 0.764, 0.851, 1 (t = 2), the dipyramid 0.729,
  0.927, 1 (t = 2). Placeholder names: Notch Octahedron (conjoined piece), Notch Dipyramid (sloping pair); DICTO to confirm.
