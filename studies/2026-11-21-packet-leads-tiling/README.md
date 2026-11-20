# Packet leads 1 and 2: can they fill space? (21 Nov 2026)

**DICTO's question:** "continue with search for leads one and two". The packet screen (studies/2026-11-21-packet-screen)
found two icosahedral pairs whose packets cancel exactly:
1. dodecahedron centre pyramids + truncated icosahedra, 12:1, equal edges (packets 5 and −60 on arctan φ);
2. icosahedron centre pyramids + truncated dodecahedra, 20:1, equal edges (packets −3 and 60 on arccos(1/√6)).

Cancelling packets are necessary for a mixed filling, not sufficient. Can these pieces fill space? Second question: can they
with the help of copies of the full dodecahedron or icosahedron, or other zero-packet neutral pieces?

**Conclusion.** No, for both leads. Both answers are theorems, proved exactly. They hold for every tiling, face-to-face or
not. Mirror images are allowed. Each piece may be used at finitely many scales. The proof is the local angle count at the
edges, as in the 4 Nov proof that the B3 permutohedron does not tile (studies/2026-11-04-rt-pyramids).
- The packets cancel globally, but the smallest ring of angles in which the irrational parts cancel adds up to 3π. A ring
  around an edge must add up to exactly 2π, or π if the point lies inside another piece's face, so it never closes. The
  3π ring uses the pieces in the packet proportions: two pyramid base edges, two pentagon–hexagon (or triangle–decagon) edges
  and one more truncated-solid edge.
- The same holds with any of these helpers added: the full dodecahedron, the full icosahedron, the truncated octahedron, the
  truncated cuboctahedron, the truncated icosidodecahedron, and any convex pieces whose dihedral angles are all rational
  multiples of π. That last class includes cubes, every prism, the rhombic dodecahedron, the rhombic triacontahedron and the
  centre pyramids of these.
- The constructive search (step B) was not needed. Nothing survives step A.

## Status box
- Study note, not published. Run on the compute host (~/venvs/indep/bin/python: sympy, mpmath). Foreground runs only, each
  under 280 s. No background jobs.
- Exact: every dihedral angle (coordinates proved exactly) and the independence of π, α, β, γ over Q (proved). Every
  verdict follows from these by finite exact arithmetic with fractions. Floating point is used only to bound the search: a
  ring is at most 2π.
- Not covered: helpers outside the list above, for example the icosidodecahedron, the rhombicosidodecahedron, or centre
  pyramids of other icosahedral solids. See LEADS.

## The angles (data/angles.json, logs/angles.log)
Basis: α = arctan φ (58.2825°, half the dodecahedron dihedral), β = arccos(1/√6) (65.9052°), γ = arccos(√(2/3)) (35.2644°).

| piece | edge | count | dihedral | degrees |
|---|---|---|---|---|
| dodecahedron centre pyramid | base–side | 5 | α | 58.2825 |
| dodecahedron centre pyramid | side–side | 5 | 2π/3 | 120 |
| truncated icosahedron | hexagon–hexagon | 30 | 3π/2 − 2β | 138.1897 |
| truncated icosahedron | pentagon–hexagon | 60 | 3π/4 − α + β | 142.6226 |
| icosahedron centre pyramid | base–side | 3 | 3π/4 − β | 69.0948 |
| icosahedron centre pyramid | side–side | 3 | 2π/5 | 72 |
| truncated dodecahedron | decagon–decagon | 30 | 2α | 116.5651 |
| truncated dodecahedron | triangle–decagon | 60 | 3π/4 − α + β | 142.6226 |
| dodecahedron | | 30 | 2α | 116.5651 |
| icosahedron | | 30 | 3π/2 − 2β | 138.1897 |
| truncated icosidodecahedron | square–hexagon / square–decagon / hexagon–decagon | 60 each | 5π/4 − β / π/2 + α / 3π/4 − α + β | 159.0948 / 148.2825 / 142.6226 |
| truncated octahedron | square–hexagon / hexagon–hexagon | 24 / 12 | π/2 + γ / π − 2γ | 125.2644 / 109.4712 |
| truncated cuboctahedron | square–hexagon / square–octagon / hexagon–octagon | 24 each | π − γ / 3π/4 / π/2 + γ | |
| cube, tetrahedron, octahedron, B3 permutohedron (controls) | | | π/2; 2γ; π − 2γ; 3π/4, π − γ, π/2 + γ | |

Solids come from the exact coordinates of the packet screen (data/inputs there). The centre pyramids have their apex at
the solid's centre. The B3 permutohedron (corners: all permutations of (±1, ±2, ±3)) is built in scripts/angles.py.

## Method
1. **scripts/angles.py.** For every edge, the exact dihedral cosine c is computed from the coordinates. PSLQ (60 digits)
   proposes θ = qπ + aα + bβ + cγ. Each proposal is then proved exactly: e^{iNθ}·e^{−iNX} = 1 is checked in sympy (minimal
   polynomial of the real part − 1 and of the imaginary part is x), and |Nθ − NX| < 2π. Here N clears the denominators of
   a, b, c.
2. **Independence (proved in scripts/angles.py).** Put x = e^{2iα} = (1+iφ)²/(1+φ²), y = e^{2iβ} = (−2+i√5)/3 and
   w = e^{2iγ} = (1+2√2 i)/3. These all lie in F = Q(i, √5, √2). Suppose aα + bβ + cγ = rπ with a, b, c integers and r
   rational, r = p/s. Then x^{as}y^{bs}w^{cs} = 1.
   - Take the norm from F down to Q(√−5). It gives N(x) = 1, N(w) = 1 and N(y) = y⁴, so y^{4bs} = 1.
   - So if b ≠ 0, β/π would be rational. Then 2cos β would be an algebraic integer, but its minimal polynomial is 3x² − 2.
     So b = 0.
   - The norm to Q(√−2) gives N(x) = N(y) = 1 and N(w) = w⁴. So c = 0, because 2cos γ has minimal polynomial 3x² − 8.
   - Then x^{as} = 1. So a = 0, because 2cos α has minimal polynomial 5x⁴ − 20x² + 16.
   So π, α, β, γ are linearly independent over Q, and a sum of dihedrals equals 2π exactly when its vector is (2, 0, 0, 0).
3. **scripts/angle_test.py: local angle count.** Take a generic point of an edge of a piece in a locally finite tiling.
   This avoids every corner and every crossing, which are only finitely many near the point. The pieces around the point
   fill the full turn. Each piece adds its dihedral angle there, or π if the point lies inside one of its faces (at most
   one piece can do this). So the dihedrals sum to 2π or π. All non-negative integer solutions are enumerated. The real sum
   bounds the search at ≤ 2π, and the check is exact, by vectors of fractions.
   - **Strict mode:** only the listed pieces.
   - **Rational mode:** any convex pieces whose dihedrals are all rational multiples of π may also be used. The test then
     becomes: irrational part 0 and rational part ≤ 2π. This gives these helpers the most room possible.
4. **Pruning.** A piece can occur in a tiling only if every one of its edges can close using pieces that can occur. Pieces
   are removed one by one until nothing changes. If a lead piece is removed, no tiling by the allowed pieces contains it.

## Controls (logs/angle_test.log; all pass)
- Octet (tetrahedron + octahedron) survives. At a tetrahedron edge the rings are 1+1 (with a face, π) and 2+2 (2π).
- Cube alone survives. Truncated octahedron alone survives. Truncated cuboctahedron + cube survives.
- B3 permutohedron alone is removed at its rectangle–octagon edge (3π/4). This agrees with the 4 Nov result.
- Dodecahedron alone is removed (2α). Regular tetrahedron alone is removed (2γ).

## Results

**Lead 1 (dodecahedron centre pyramid + truncated icosahedron).** Count the angles around a generic edge point:
n₁ times α, n₂ times 2π/3, n₃ times 3π/2 − 2β, n₄ times 3π/4 − α + β. By independence:
- the α part gives n₁ = n₄;
- the β part gives n₄ = 2n₃.

So any ring that contains a base edge of the pyramid, or any edge of the truncated icosahedron, has n₃ ≥ 1 and
n₁ = n₄ = 2n₃ ≥ 2. Its sum is n₃·3π + n₂·2π/3 ≥ 3π. The cheapest such ring is 2·58.2825° + 2·142.6226° + 138.1897° = 540°.
Each extra helper fails in turn:
- The full dodecahedron (2α) and the full icosahedron (3π/2 − 2β) only add more of the same irrational parts. They are
  removed with the lead pieces.
- The truncated octahedron and truncated cuboctahedron carry only γ, which nothing else here can cancel. They remain as a
  tiling among themselves and with cubes, but no lead piece can join them.
- The truncated icosidodecahedron can close a pyramid base edge: α + (3π/4 − α + β) + (5π/4 − β) = 2π. But it cannot close
  its own square–decagon edge (π/2 + α) without the truncated icosahedron, which is removed first at its hexagon–hexagon
  edge. So it is removed too, and then the pyramid is removed.

**Theorem 1.** No tiling of space contains a dodecahedron centre pyramid or a truncated icosahedron if its pieces are
these two, plus any of: dodecahedra, icosahedra, truncated octahedra, truncated cuboctahedra, truncated icosidodecahedra,
and convex pieces with all dihedrals rational multiples of π. Each piece kind may come at finitely many scales; mirror
images are allowed, and the tiling need not be face-to-face.

**Lead 2 (icosahedron centre pyramid + truncated dodecahedron).** Count the angles around a generic edge point:
n₁ times 3π/4 − β, n₂ times 2π/5, n₃ times 2α, n₄ times 3π/4 − α + β. By independence:
- the β part gives n₁ = n₄;
- the α part gives n₄ = 2n₃.

The sum is n₃·3π + n₂·2π/5 ≥ 3π. The cheapest ring is 2·69.0948° + 2·142.6226° + 116.5651° = 540°. The helpers fail as in
lead 1. With the truncated icosidodecahedron, a pyramid base edge can close: (3π/4 − β) + (3π/4 − α + β) + (π/2 + α) = 2π.
But the truncated dodecahedron's decagon–decagon edge (2α) fails, then the truncated icosidodecahedron's square–hexagon
edge (5π/4 − β), and then the pyramid.

**Theorem 2.** Theorem 1 holds word for word with the icosahedron centre pyramid and the truncated dodecahedron in place
of the dodecahedron centre pyramid and the truncated icosahedron.

**Verdict.** Lead 1 cannot fill space. Lead 2 cannot fill space. This holds alone and with every helper listed.
The packet cancellation 12:1 and 20:1 is real, but it is global. No edge can be closed with it locally.

## Files
- scripts/angles.py: exact angles, proofs, independence → data/angles.json, logs/angles.log (FINAL ok)
- scripts/angle_test.py: controls, cheapest rings, pruning → data/angle_test.json, logs/angle_test.log (FINAL ok)
- Re-run: on the compute host, from this folder, `~/venvs/indep/bin/python scripts/angles.py ../2026-11-21-packet-screen/data/inputs`
  then `~/venvs/indep/bin/python scripts/angle_test.py`.

## LEADS
- **What a helper must do.** It must give a ring closing at 2π. All icosahedral angles found here lie in Qπ + Zα + Zβ. A
  helper with angles in the same span would have to make every ring through the pyramid base close below 3π. The truncated
  icosidodecahedron does this at the base edges but fails at its own edges. Next test (cheap, same scripts): add the
  icosidodecahedron (3π/4 − α + β), the rhombicosidodecahedron (5π/4 − β, π/2 + α) and the centre pyramids of all
  icosahedral solids. Run the pruning on the whole icosahedral family together. This is outside DICTO's two leads; it
  needs a word.
- **The cross-symmetry lead from the packet screen** (tetrakis hexahedron triangle pyramid + truncated icosahedron, 9:1)
  can be tested the same way, once the tetrakis pyramid's angles are written in an exact basis.
- **General rule worth stating in the packet paper:** the cancellation of packets is global. The local angle count asks
  for cancellation inside one ring of at most 2π. For these leads, the smallest cancelling ring is 3π.
