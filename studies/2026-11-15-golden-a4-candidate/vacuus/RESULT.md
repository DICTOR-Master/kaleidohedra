# Vacuus test of the golden twisted-silent sets (15 Nov 2026, pilot, floating point)

Ridges (2-faces) of the convex hull, and the central hyperplanes each ridge spans with the centre (the #105 Vacuus count).

| set | points | facets | ridges | distinct central hyperplanes |
|---|---|---|---|---|
| control: permutohedron n=5 (#105) | 120 | 30 | 150 | 65 (matches #105 Theorem 3) |
| golden 20-set, perms of (φ²,φ²,φ²,φ,0) | 20 | 10 | 30 | 30 |
| golden 30-set, perms of (φ²,φ²,1,1,0) | 30 | 20 | 80 | 80 |

Verdict: no ridges share a central hyperplane, so the golden sets have no Vacuus coincidences (unlike the permutohedron, 150 → 65).
Their hulls have the face counts of the truncated 5-cell (20, 10 facets, 30 ridges) and the cantellated 5-cell (30, 20 facets, 80 ridges), in golden proportions; congruence to the uniform ones not checked.
Floating point only (scipy ConvexHull); not yet exact.
