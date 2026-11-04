# Galois twins of the golden cuts (2026-11-04) — Concordance gap 8
#88: each Platonic solid has two golden cuts, x1 = φ/(k + 2φ) (greater) and x2 = 1/(φk + 2) (lesser), k = corner-side factor 2 sin(face angle/2):
k = 1 (triangles: tetrahedron, octahedron, icosahedron), √2 (cube), φ (dodecahedron) — the one triangle's numbers again.
Galois swap σ: √5 -> −√5 and √2 -> −√2 together (DICTO's Double Vision; #90).
Results (sympy, exact):
- Always: x2 is x1 with φ replaced by 1/φ (reciprocal twins) — by construction of the two equations.
- CUBE only: σ(x1) = x2. The two Golden Cut Cubes are Galois twins (as #90 found for their sweep values). Reason: σ(√2) = −√2 and σ(φ) = −1/φ turn kx = φ(1−2x) into √2x = (1−2x)/φ.
- Dodecahedron: x1 = 1/3 exactly (rational), so the Greater Golden Cut Dodecahedron is its OWN twin; σ(x2) = (7 + √5)/22 is a real cut whose corner sides are φ³ times the original sides: the twin of the Lesser Golden Cut Dodecahedron is the φ³-cut dodecahedron.
- Triangle-faced (T, O, I): σ(x1) = φ² and σ(x2) = 1/2 + √5/10 both exceed 1/2 — the twins over-cut (corner triangles overlap): no solid.
So Double Vision pairs the cube's golden cuts with each other, fixes the dodecahedron's greater cut, sends its lesser cut to a φ³ cut, and has no solid partner for the triangle-faced solids.
Chapter material for The Golden Ladder (cuts thread). LEADS: the φ³-cut dodecahedron (φ³ = the golden cycle's step, #54); the RD/RT golden cuts of #89 under σ.
