# Vacuus test of the golden twisted-silent sets (15 Nov 2026, pilot, floating point)

Ridges (2-faces) of the convex hull, and the central hyperplanes each ridge spans with the centre (the #105 Vacuus count).

| set | points | facets | ridges | distinct central hyperplanes |
|---|---|---|---|---|
| control: permutohedron n=5 (#105) | 120 | 30 | 150 | 65 (matches #105 Theorem 3) |
| golden 20-set, perms of (φ²,φ²,φ²,φ,0) | 20 | 10 | 30 | 30 |
| golden 30-set, perms of (φ²,φ²,1,1,0) | 30 | 20 | 80 | 80 |

Verdict (corrected 16 Nov with DICTO: "the non heart variety of vacuus"): both golden solids ARE Vacuus, built of central plates, one per ridge, of the NON-HEART kind: neither set is centrally symmetric (checked: 20-set and 30-set both fail x -> -x), so no plate carries an opposite ridge, no two ridges share a plate, and no full slices meet at a heart. The permutohedron is the heart kind (150 ridges on 65 plates; five central slices, each a DICTO 1:2 Truncated Octahedron, slotted in pairs along regular hexagons = the heart). The #105 definition, stated for centrally symmetric polytopes only, is too narrow: next version of #105 to define the Vacuus for any polytope with a centre (plates spanned by ridges), with heart and non-heart kinds.
Their hulls have the face counts of the truncated 5-cell (20, 10 facets, 30 ridges) and the cantellated 5-cell (30, 20 facets, 80 ridges), in golden proportions; congruence to the uniform ones not checked.
Floating point only (scipy ConvexHull); not yet exact.
