# Aim 2, chunk 5b: the DICTO Yantra cones as positive geometries (12 Nov 2026; `scripts/yantra_cones.py`, log `data/yantra-cones.log`, 126 checks, FINAL ok)

**Conclusion.** A whole DICTO Yantra cone is NOT a positive geometry with a nonzero form: its canonical form is 0, because its
boundary circles have no end points (the same holds for every solid of revolution built from the nine cones and level planes). Cut
along the yantra's own plane it becomes one: the half-cone's form is 2wh²/(Q·B·y), and its residue on the yantra plane is exactly the
flat yantra triangle's form (the cone restricted to that plane splits into the triangle's two legs), so the flat DICTO Yantra is the
residue of its half-spun cones. The degree-160 numbers drop out of every invariant of a single cone (all nine are affine images of one
half-cone: least point at a quarter of the height, Ω_min·vol/3! = 64√3π/81 for each). The bridge "Ω = volume of the polar" of chunk 2
fails for these curved solids; it holds with Mazzucchelli and Raman's arctan weight (checked numerically only, 20 digits).

**Question.** Chunk 5 (studies/2026-11-12-solids-canonical) showed DICTO's polyhedral solids are positive geometries and left the DICTO
Yantra cones: #103 Proposition 4 spins each of the nine triangles of the DICTO Yantra about the axis into a solid circular cone (apex
on the axis, level base disc). Their boundaries are curved (quadric cones) and their slopes are algebraic of degree 160 (#103,
Theorem 9). Do these cones have canonical forms, what are they, and what do they say?

**Solids.** Cone i (i = 1..9): apex (0, 0, a_i), base disc of radius w_i at height b_i, h_i = b_i − a_i; Q_i = w_i²(z − a_i)² −
h_i²(x² + y²) ≥ 0, base plane B_i = (b_i − z)·sign(h_i) ≥ 0. Half-cone H_i = cone ∩ {y ≥ 0}: the half on one side of the yantra's
own plane (the plane through the axis in which the flat yantra is drawn). Sector S_i(d, d') = cone between the two half-planes through
the axis with unit directions d, d' (angle below 180°). The DICTO Yantra values (a_i, b_i, w_i) are taken to 40 digits from the
#103 study (figures/golden_family.json, GF1) and used as exact rationals: every identity below is proved for symbolic a, b, w, so
the rational instance only shows the formulas run on the actual nine cones; the degree-160 numbers themselves never need to be
handled (see the affine argument in the Method).

## Method (chosen before computing)
Sources: Arkani-Hamed, Bai, Lam, "Positive geometries and canonical forms" (2017), §5 (regions bounded by lines and conics: the
half-disc, the "pizza slice"; quadrics); Mazzucchelli and Raman, "Canonical forms as dual volumes" (arXiv 2509.02239, 2025; in the
reference library, gaps/): the canonical function of a positive geometry with a conic in its boundary is the Laplace transform of a
measure on the dual cone that is NOT the plain indicator (their (55), (61): the "half-pizza" bounded by one line and one conic, weight
1/2 + (1/π) arctan(...)). The rules used:

1. **Recursion by residues** (ABL definition): Ω(X) has simple poles only on the boundary components, and on each component C its
   residue is Ω(C); a 0-dimensional point has Ω = ±1. A full real conic (a circle) has no boundary points, so its form is a
   holomorphic 1-form on P¹, i.e. 0.
2. **Exact identities.** All forms are rational functions; every identity is checked in sympy as an identity of rational functions in
   symbolic a, b, w (and direction parameters), i.e. a proof, and again for the nine DICTO Yantra cones with rational parameters.
3. **Residues by Leray's formula.** On a plane: coordinates adapted to the plane (rotation, Jacobian 1). On the cone surface: polar
   coordinates x = ρC(m), y = ρS(m) with the rational circle C = (1 − m²)/(1 + m²), S = 2m/(1 + m²), dx∧dy = ρ·2/(1 + m²) dρ∧dm;
   Res_Q = (numerator)·ρ·(2/(1+m²)) / ((other factors)·∂Q/∂ρ) on ρ = w(z − a)/h.
4. **Ansatz + linear algebra** where the numerator is not known (sectors; the zero theorem for solids of revolution): the numerator is a
   general polynomial of the degree forced by projective weight (deg numerator = deg denominator − 4 in P³, − 3 in P²); residue
   conditions are linear; solved exactly.
5. **Affine covariance.** Ω(L·y)·|det L| = Ω(y). Every half-cone is an affine image of H0 = {x² + y² ≤ (1 − z)², 0 ≤ z ≤ 1, y ≥ 0},
   so every affine-invariant number of one cone (the point where Ω is least, Ω_min·vol) is the same for all nine: the degree-160
   numbers enter only where the cones sit relative to each other.
6. **Dual volume (bridge of chunk 2) for curved boundaries.** Ω(x) = ∫ over the dual cone of e^{−⟨x,y⟩} μ(y) dy. For polytopes μ = 1
   (Ω = volume of the polar). For the half-disc, μ is Mazzucchelli–Raman's (61) at a = 0. These integrals are transcendental-looking
   2D integrals: they are checked NUMERICALLY ONLY (mpmath, 20 digits), and claimed only at that level. The exact statement used for
   the cones is a factorisation: the half-cone's cone over P³ is linearly (det ±1) the half-disc's cone times a ray, so its measure is
   (half-disc measure) ⊗ 1; this factorisation is checked exactly.

## Checks planned
- Positive controls: ABL half-disc 2/((1 − x² − y²) y) (residues ±1 at (±1, 0), segment form on y = 0); Mazzucchelli–Raman (55) at
  a = 1/2 (constant √3) by the same residue code; numeric integrator: Lorentz cone ∫ e^{−⟨x,y⟩} = 2π/q(x)^{3/2} and a triangle cone
  (= the triangle's form); M–R measure (61) reproduces (55) at a = 1/2 and the half-disc at a = 0.
- Half-cones: Res on the yantra plane = the yantra triangle's form (Q restricted to the plane factors into the two legs); Res on the
  base = half-disc form; Res on the cone = (arc form) ∧ (segment form of the ruling), no pole at the apex other than the ruling's
  end; Ω > 0 inside.
- Sectors (pizza slices of the cone): numerator by ansatz; residues on both half-planes = the right triangles; base = pizza-slice form;
  additivity S(d1, d2) + S(d2, d3) = S(d1, d3); two quarter sectors = half-cone; sectors round the full circle (four, and the three
  120° sectors of the stella's three positions, #103 Prop. 4, with √3) sum to 0.
- Zero theorem: the full cone and solids of revolution bounded by cones and level planes (a ring between two DICTO cones) have Ω = 0:
  the residue-zero conditions leave only the zero numerator; H+ + H− = 0 identically.
- Universal invariant: least point of Ω(H0) and Ω_min·vol/3! exactly; the same at each of the nine DICTO cones.
- Negative controls: wrong constant (3wh² for 2wh²) fails the base residue; a level cut z = const (not through the apex) does not factor
  into lines (not a triangle); a mis-joined pair (H+ of a cone with H− of the cone with apex moved 1/7) leaves a pole on y = 0; the
  plain dual volume (μ = 1) does NOT give the half-disc's Ω; the measure with the arctan sign flipped fails.

Launch: compute machine, 4 cores, via the job gate; pilot 4 s, full run 16 s.

## Checks (126, all held)
- Positive controls: ABL half-disc (residue on the cut = 2/(1 − x²), end residues ±1); Mazzucchelli–Raman (55) at a = 1/2: the residue
  code returns c = √3; Lorentz cone and a triangle cone through the integrator (agree to 10⁻²¹); M–R measure (61) reproduces Ω at a = 1/2
  (2 points) and a = 0 (2 points) to 10⁻²¹ (numerical).
- Half-cone, symbolic a, h, w (a proof) and each of the nine DICTO cones (exact 40-digit rationals, apex up and apex down): A1 residue on
  the yantra plane = the yantra triangle's form; A1b Q there = product of the two legs; A2 residue on the base = half-disc form 2w/((w² −
  x² − y²)y); A3 residue on the cone = ±(dm/m) ∧ ruling-segment form (pole at the apex only as the ruling's end); A4 Ω > 0 inside; A5
  Ω(H) = w·Ω(half-disc)(x, y, w(z − a)/h)·1/(base form): half-disc cone times a ray, exactly.
- Slices (pizza slices of the cone), symbolic and cones 1, 3, 7: the numerator ansatz (linear) is solved uniquely by the two half-plane
  residues (right triangles); base residue = pizza slice of the disc (its circle residue = arc form, its radius residue = segment [0, w]);
  cone residue = arc form ∧ ruling form; joins S(d1, d2) + S(d2, d3) = S(d1, d3) (pole on the inner half-plane cancels); two quarters =
  half-cone; four quarters round the axis sum to 0; the three 120° slices of the stella's three positions (#103 Prop. 4) sum to 0 (with √3).
- Zero theorem: annulus and ring between DICTO cones 1 and 2: residue-zero conditions leave only the zero numerator (nullity 0); disc and
  full cone: numerator degree negative; H+ + H− = 0 identically.
- Universal invariant: H0's only interior critical point (0, √3/4, 1/4) is a minimum (Hessian minors 16/3, 256/3, 16384/9); Ω_min =
  256√3/9; at each DICTO cone the image point (0, w√3/4, b − h/4) is critical and Ω·vol/3! = 64√3π/81 exactly.
- Negative controls (all caught): constant 3wh² leaves residue −w/(y(x² + y² − w²)) on the base; a level cut is a circle (definite
  quadratic), not a triangle; halves with apexes 1/7 apart leave residue −110000/10101 on the yantra plane; the plain dual volume (weight
  1) misses Ω by 59%, 125%, 44%, 282% at the four points; the arctan sign flipped misses by 19%, 64%.

## Results
1. **Zero theorem.** Ω(full cone) = 0, and Ω = 0 for every solid of revolution bounded by cones about the axis and level planes (the
   spun yantra regions). Proof: each boundary piece is bounded by full circles; a circle has form 0 (a holomorphic 1-form on P¹), so
   discs, annuli and cone bands have form 0, so the solid's form has no poles, so it is 0. In the ABL definition (nonzero form) these are
   not positive geometries; they are the 3D analogue of the disc.
2. **Half-cones.** H = cone ∩ {y ≥ 0} is a positive geometry, Ω(H) = 2wh²/(Q·B·y); residues: yantra triangle, half-disc, and on the cone
   (arc) × (ruling). Ω(H+) + Ω(H−) = 0: the cut's pole cancels, the same join law as chunk 5. So the nine half-cones hand down the nine
   flat triangles as residues: Res_{y=0} Σ Ω(H_i) = Σ Ω(T_i).
3. **Slices.** Any slice of angle under 180° is a positive geometry (numerator linear, found by ansatz); slices add with pole
   cancellation and close up to 0 round the axis, including the three 120° slices of the stella positions.
4. **Universal number.** Least point of Ω on each half-cone: on the mid-plane x = 0 at a quarter of the height from the base (the
   centroid height of a solid cone) and at 1/√3 of the radius there; Ω_min·vol/3! = 64√3π/81 = 4.29938 for all nine cones (and any
   circular half-cone). This is not a Mahler product (Ω is not the polar volume here). The degree-160 data fix only where the nine cones sit.
5. **Bridge.** For curved boundaries Ω is the Laplace transform of a weighted dual: weight 1/2 + (1/π)·arctan(y2/√(y3² − y1² − y2²)) on
   the disc part, 1 on the rest (Mazzucchelli–Raman (61), a = 0), and by A5 the half-cone's weight is that times 1 along the ray. The plain
   polar volume (weight 1) is wrong for every Yantra cone. Numerical evidence only (20-digit quadrature); the exact part is A5.

**What this gives the aim.** Curvature with closed boundary curves kills the form: a round object hands out no poles. Laws come back only
when the object is cut by planes through the axis, and then the yantra plane's residue is the flat yantra. The polar-volume bridge needs a
weight on curved geometries (arctan, transcendental) where polytopes have weight 1.

**Faults fixed on the way.** (1) Pilot: the stereographic parameter of (1, 0) came out as float 0.0 (Python division), breaking the arc
checks; now exact. (2) Restricting a form to a face before cancelling the face's factor gave 0/0 (nan) or 0; every restriction now
cancels first, and the negative controls print their nonzero residues so a nan can never pass as "caught". (3) Full run: the a = 1/2
integrals agreed only to 10⁻¹⁰ because the weight jumps on the circle where y2 = a, which was not a quadrature split point; split
there, agreement 10⁻²¹ (tolerance unchanged).

Credit: positive geometries, the half-disc and pizza slice: Arkani-Hamed, Bai, Lam (2017); dual-volume measures for conic boundaries:
Mazzucchelli and Raman (2025). The DICTO Yantra, its cones (#103 Prop. 4) and the Cleo-Antonius are DICTO's.
NEXT: chunk 6 (Poincaré dodecahedral space along a Hopscotch line). Lead: the canonical form of the 2D DICTO Yantra's 43 odd regions
(valuation over the nine triangles, marma coordinates of degree 160).
