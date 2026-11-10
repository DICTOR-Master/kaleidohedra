# Aim 2, chunk 2: the canonical form along the cube–octahedron sweep (10 Nov 2026; DICTO "yes 1 then 2")
S(μ) = cube [-1,1]^3 ∩ μ·octahedron (|x|+|y|+|z| <= 1); Hopscotch walls μ = 1, 2, 3; the turn μ ↦ 3/μ (fixed point √3).
scripts/canon_sweep.py (exact, sympy; dicto-big-brother) - FINAL ok.

1. BRIDGE CHECKED: the canonical form of S(μ) (positive-geometry formula: sum over a triangulation of the simplex forms
   <Z0Z1Z2Z3>^3 / prod <Y ...>, every simplex positively oriented) equals 3!·vol of the polar of S(μ) about the same point, exactly,
   at a generic point near the centre (1/97, 1/89, 1/83), in every chamber (7 samples). (Two faults fixed on the way: inner
   triangulation faces through the centre gave 0/0 - evaluate at a generic point; unoriented simplices gave a wrong sum.)
2. THE CANONICAL FORM AT THE CENTRE is one power of μ per chamber; the degree drops by one at each wall:
   Ω(S(μ); 0) = 3!·vol(S*) = 48/μ^3 (0<μ<1), 48/μ^2 (1<μ<2), 24/μ (2<μ<3), 8 (μ>3).
   Continuous, a KINK exactly at every Hopscotch wall and nowhere else; continued, no piece has a pole except μ = 0.
   So the walls of the sweep are exactly the non-smooth points of its canonical form: here the "poles meet the walls" in the form of
   kinks; the only pole is at μ = 0 (the collapsed octahedron).
3. vol(S)·vol(S*) (Mahler volume): 32/3 at both ends (the cube/octahedron equality case), 32(−2μ^3+9μ^2−9μ+3)/(3μ^2) on (1,2),
   16(μ^3−9μ^2+27μ−21)/(3μ) on (2,3); maximum at the root of 2μ^3 − 9μ + 6 = 0, μ = 1.631223, value 14.375086; NOT at the turn's
   √3 (14.290624); not symmetric under μ ↦ 3/μ (M(3/2) = 128/9, M(2) = 40/3). The turn does not act on these volumes.
DICTO 10 Nov during this step: "is it possible that the paradigm has the shape of a polyhedra"; "walls could be cell walls":
the #61 walls in the (s, λ) plane are lines (λ = −9s/8, −5s/8, −s/8, 3s/8 through the origin, and λ = −(4−s)/24): its chambers are
polygons - cells of a fan. NEXT: figure of the #61 chamber map; chunk 3 (the turn in canonical-form language); the icosahedral sweep.
