DICTO · dictospheres.com

# Gnomon shapes: what each step of the twelve-station golden cycle adds (DICTO 2026-10-25)

**Question (DICTO, on draft #54).** #54 measured only the *volume* each step adds. A gnomon in the classical sense is about *shape*:
Euclid, *Elements* II Def. 2 (for parallelograms) and Heron, *Definitions* (generally): the gnomon is the figure which, added to a figure,
makes the whole **similar** to the original. Júlia Pimentel's square method, n² + n + (n + 1) = (n + 1)² (news reports: mixvale.com.br
2026-06-22, portaltela.com 2026-05-12; journal not named), is exactly the classical gnomon of the square: the L-strip n + (n + 1) turns
the n-square into the (n + 1)-square, and the whole stays a square. Here, for each step station_k → station_k+1 of the cycle
I ⊂ Cleo star ⊂ D′ ⊂ ID ⊂ OG ⊂ rTI ⊂ TI ⊂ H ⊂ jtI ⊂ RT ⊂ M ⊂ I·φ³, we state exactly: what the added region (the "strip") is made of,
whether the new whole is similar to an earlier station (then the step is a classical gnomon, with its ratio), and the size ratios.

**Method (exact, Q(√5)).** `dump_stations.py` builds all twelve stations with exact corners from the published construction scripts of
Progenitors #34 / Vajrayana #35 (studies/2026-10-16-progenitors; no float snapping) → `stations-exact.json`. `gnomon_shapes.py` (`qs.py`:
exact a + b√5 arithmetic, exact signs and square roots): each convex layer A ⊂ B is cut as in Inverted Shells / Vajrayana §3, one piece
per face of A (B ∩ cone over the face, outside its plane; faces of A lying in a face plane of B give none); every piece corner is solved
from three exact planes and checked against all half-spaces; volumes are exact determinant sums; the pieces of each step add up exactly
to the layer. Step 1 is the 20 spikes; step 2 is DICTO's published fill (#35 Table 2). Similarity is tested exactly on *all* squared
corner distances (a full corner-to-corner correspondence, mirror allowed; handedness reported) — between all piece kinds of all steps,
between pieces and stations, and between all stations. Run on dicto-big-brother → `gnomon-shapes.txt`, `pieces.json`;
figure `fig_steps.py` → `gnomon-shapes.png`.

## Results (volumes as multiples of the volume of I)

| step | station → station | what the step adds (pieces, all of a kind congruent) | region | added / I | new whole similar to an earlier station? |
|---|---|---|---|---|---|
| 1 | I → Cleo star | 20 Cleo-Ico (spikes), each 1/20 | 20 parts (meet only along I's edges) | 1 | no |
| 2 | Cleo star → D′ | 12 inward pentagonal pyramids + 30 valley tetrahedra (#35) | one connected gap (#35) | 2/9 + (44/45)√5 | no |
| 3 | D′ → ID | 12 pieces over D′'s pentagons: 15 corners, 5 triangles + 7 pentagons (unnamed; DICTO decides) | 1 | 353/72 + (791/360)√5 | no |
| 4 | ID → OG | 12 pieces over ID's pentagons: 11 corners, 1 pentagon + 5 quadrilaterals + 5 triangles (unnamed; DICTO decides) | 12 | 207/152 + (457/760)√5 | no |
| 5 | OG → rTI | 60 pieces over OG's quadrilaterals: 8 corners, 5 quadrilaterals + 2 triangles; 20 over OG's hexagons: two parallel hexagons (not translates) + 6 quadrilaterals (both unnamed; DICTO decides) | 1 | 2187/152 − (2129/760)√5 | no |
| 6 | rTI → TI | 60 corner tetrahedra of TI (over rTI's triangles), each (1/80)φ⁻² (unnamed; DICTO decides) | 60 | (3/4)φ⁻² | no |
| 7 | TI → H | 20 Shields (hexagonal pyramids), each (9/10)φ⁻⁴ | 20 | 18φ⁻⁴ | no |
| 8 | H → jtI | 12 pentagonal pyramids over H's pentagons (unnamed; DICTO decides) | 12 | 15/38 + (21/190)√5 | no |
| 9 | jtI → RT | 60 quadrilateral pyramids over jtI's quadrilaterals (unnamed; DICTO decides) | 12 (5 round each five-fold corner of RT) | 648/19 − (270/19)√5 | no |
| 10 | RT → M | 30 pieces over RT's rhombi: 6 corners, 1 rhombus + 6 triangles (#35 §3; unnamed; DICTO decides) | 1 | −98 + 51√5 | no |
| 11 | M → I·φ³ | 60 triangular bipyramids (6 triangles), each φ⁷/60 (#35 §3; unnamed; DICTO decides) | 1 | φ⁷ | **yes: I·φ³ ~ I, linear ratio φ³** |
| (12) | I·φ³ → Cleo star·φ³ | step 1 scaled by φ³ | | φ⁹ | no (as step 1) |

**Classical check (Euclid II Def. 2; Heron).** Exactly one step of a turn is a gnomon in the classical sense: step 11, M → I·φ³, whose
whole is similar to the first station I (linear ratio φ³ = 2 + √5, volume φ⁹). Equivalently, the whole turn I·φ³ − I is a classical
gnomon of I. For steps 1–10 the new whole is similar to no station of the cycle (only Cleo star, RT, M share a corner count, 32, and are
tested exactly not similar; all other stations differ in corner count), so they are not gnomons in the classical sense.

**Shapes across the cycle (proved facts only).** No piece kind of one step is similar to a piece kind of another step (exact test over all
16 kinds, incl. the 20 core Cleo-Icos of I); the only similar pair is the spike and the core Cleo-Ico (congruent, k = 1, as #35 states).
No piece is similar to a station (only the OG → rTI hexagon piece shares a corner count, 12, with I; not similar). The added region of
each step is a shell around the earlier station (or, in steps 1, 4, 6–9, a set of separate pieces), not similar to any station. Pieces
recur only as *types* (pyramids in steps 1, 2, 7, 8, 9; tetrahedra in 1, 2, 6), never as the same shape at another size. Four steps have
pieces of volume rational × φᵏ × I (1, 6, 7, 11), as #54 found for whole steps.

**Size growth of the whole (exact; `gnomon-shapes.txt` §1, §6).** Corner radius ratio R_k+1/R_k lies in Q(√5) only where it is 1
(Cleo star → D′: tips are D′'s corners; H → jtI); inradius ratio is 3/2 at D′ → ID, 3φ⁻² at OG → rTI, 1 at rTI → TI and jtI → RT;
all other ratios are square roots of numbers in Q(√5) (listed exactly). Clean single values: r²(I) = φ²/12, R²(Cleo star) = R²(D′) = φ²/3,
R²(ID) = φ⁴/4, r²(OG) = φ⁶/12, R²(rTI) = r²(jtI) = r²(RT) = 9/4, R²(H) = R²(jtI) = (27/4)φ⁻², R²(M) = r²(I·φ³) = φ⁸/12.

**Checks: 63 PASS, 0 FAIL** (`gnomon-shapes.txt`): all twelve volumes equal #54 Table 1; every nesting exact; every step's pieces sum to
the layer exactly; all pieces of each kind congruent; #35's fill of D′ exact; spike = core Cleo-Ico; I·φ³ ~ I (φ³) is the only similar
pair of stations.

Figure: `gnomon-shapes.png` (front half cut away, pieces pulled apart 10 %, colours = kinds within a step); copy in
~/Documents/papers-to-read/gnomon-shapes/.
