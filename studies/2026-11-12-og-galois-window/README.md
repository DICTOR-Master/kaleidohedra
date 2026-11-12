# The OG Galois-twin window test (12–13 Nov 2026)
DICTO, offered 11 Nov and queued 12 Nov: "Galois-twin window test: swap √5 → −√5 in the OG family; if the twin family stays bounded, it
behaves like a quasicrystal window."

**Conclusion: the twin family stays bounded (proved for every k), but it is not a window. It collapses to the centre, from radius
0.628 at D_0 to 4.9·10⁻³⁶ at D_33 (certified), and the decay is faster than geometric. That is the Pisot pattern (like the powers of φ),
not the model-set pattern (twins filling a fixed region such as the triacontahedron).**
Status: SETTLED (bounded, exact; collapse and shapes certified to k = 33; collapse for all k is numerical only).

## What is exact, what is certified, what is numerical
- **EXACT, every k (proof): Twin Step Lemma.** Let a face of D_k have normal n and plane n·x = d, and let a be any member of the face. Its
  foot point is p = (d/n·n) n. The Galois swap σ is a field automorphism of Q(√5), so σp = (σd/σn·σn) σn with σn·σa = σd. Here σn ≠ 0
  because n ≠ 0 and σ is injective. So σp is the orthogonal projection of σa onto the line through σn, and |σp| ≤ |σa| for every member a.
  Hence R_σ(D_{k+1}) ≤ R_σ(D_k) ≤ R_σ(OG), where R_σ(OG)² = (585 − 198√5)/361 (R_σ(OG) = 0.627748), at the twins of the 12 five-fold
  corners. **Every twin point of every D_k lies in that ball.** The proof uses only the hop's formula, so it holds for the hop of any
  polytope with coordinates in Q(√5).
- **EXACT, k ≤ 6:** the largest twin radius² in closed form, with the maximum and the lemma checked by exact sign tests:
  (585 − 198√5)/361, (153 − 54√5)/109, 14481/11881 − (26478/59405)√5, (15309 − 6561√5)/13448, 6561/6724 − (729/1681)√5, …
  (the rest are in data/og-window-33.json).
- **CERTIFIED, k = 7 … 33:** faces certified as in og-margin certified_orbit.py (the real side). The twins are carried in ball arithmetic
  with the conjugated group σ(I_h). σ(I_h) is again a group of orthogonal matrices, because g gᵀ = I is an identity over Q(√5). The
  twin radius at each level is a certified ball. The lemma check found 0 certified violations at every level.
- **NUMERICAL (float on certified points):** the hull shapes, orbit counts, covering ratios and nesting tests.

## Results (data/og-window-33.json, .log)
−log₁₀ R_σ(D_k), k = 0…33: 0.20 0.26 0.33 0.66 1.11 1.16 1.56 2.67 3.49 4.15 4.75 5.67 6.27 6.40 6.83 6.88 8.61 9.18 10.5 10.5 11.7
11.8 12.8 15.0 15.5 15.8 18.0 20.1 26.3 26.4 30.4 32.2 33.9 35.3.
- **Bounded:** yes (proved, see above). The twin radius never rises at any level (in line with the lemma).
- **Growth law (numerical):** the radius falls irregularly. Single steps range from ×0.95 (k = 19) down to ×6·10⁻⁷ (k = 28). On average
  it falls by ×0.35 per level over k = 0–10 and by ×0.047 per level over k = 10–33. The exponent −log R_σ grows about 2.5 times every ten
  levels (4.75, 11.7, 30.4 at k = 10, 20, 30), so the decay is faster than geometric. No closed rate was found. For comparison, the
  coordinates' digits grow from 4 to 1780 over k = 0–10, much faster still.
- **Fills a region densely: no.** The covering ratio is the largest empty gap inside the twin hull divided by its size. For the OG it
  stays between 0.24 and 0.62 at every level and does not fall as the point count grows (102 → 215 520). The twin points form a thin
  shell round the hull with a near-empty inside (smallest twin radius / largest: 0.985 at k = 0, below 10⁻⁴⁹ from k = 22). Measured the
  same way, the model sets fall steadily (0.0082 → 0.000025 for the Fibonacci chain; 0.435 → 0.102 for the icosahedral Z⁶ set).
- **Shape and symmetry:** every twin hull is symmetric under σ(I_h) (checked at every level). From k = 7 its corners are ONE σ(I_h)
  orbit, except k = 9, 18 and 22, where there are two. So each twin hull is an orbit polytope. Corner counts over the 34 levels: 60 (16 times), 20 (6),
  120 (5), 12 (2), 180 (2), 102, 90 and 240 (once each). The regular icosahedron (k = 2, 32) and the regular dodecahedron (k = 3, 7, 15,
  25, 27, 29) recur, as do the rhombicosidodecahedron, truncated-icosahedron and truncated-icosidodecahedron types (the shapes of the
  11 Nov Angeli study, now to k = 33). Twin hulls are nested in the previous level's hull at every step except 18 → 19 (float test).
- **Against the triacontahedron:** the window of the 6D icosahedral lattice (Ammann–Kramer) is the rhombic triacontahedron: 32 corners
  in two orbits (12 + 20), 30 rhombi, support on the 5:3:2-fold axes 1 : 0.9106 : 0.8507. No OG twin hull has 32 corners or rhombic
  faces, and none is a fixed region. The family moves between orbit polytopes of shrinking size.
- **Against E8/H4:** the Elser–Sloane window (study 2026-11-12-e8-canonical) is a fixed 4D polytope of volume 5φ³/6, the shadow of the E8
  Voronoi cell, and it carries the density law. The OG twin hulls have volume → 0, so the OG family is no section of that picture either.
  The OG's unbounded denominators already ruled out a model set of one lattice (og-margin §28); this test shows the twin side gives no
  window even in a looser sense.

## Controls (scripts/window_controls.py, data/window-controls.json; all passed in the main run)
P1 Fibonacci chain → WINDOW (window length 1.617993, φ = 1.618034); P2 Fibonacci cube → WINDOW (twin hull 8 corners, 6 squares);
P3 icosahedral model set from Z⁶ with the triacontahedron window → WINDOW, twin hull 32 corners, 30 rhombi (matches the window);
N1 n·φ → UNBOUNDED (twin −n/φ); N2 φⁿ (Pisot) → COLLAPSE. The OG family was classed COLLAPSE, with the Pisot control.
OG validation: k ≤ 10 matches the exact 11 Nov run (og-twin-10.json: corner counts, twin max/min to 1e-9). Real t_min(D_k) matches
certified-family-30 for k = 10–31.

## Runs (the compute machine, watched jobs)
- ogwin-pilot, ogwin-pilot2: stopped by their own checks (P3 patch too small for the covering test; a relative-radius check divided
  by exactly-zero coordinates). Both were fixed. ogwin-pilot3 (k ≤ 14, 9 s): FINAL ok (data/og-window-pilot.*).
- ogwin-main (600-bit balls): k = 0–31 certified, then the precision guard stopped it at D_32 (twin balls kept only 19 digits, because the
  twin triangles become nearly collinear). Kept as data/og-window-run1-600bit.*; its values for k ≤ 31 agree exactly with the final run.
- ogwin-main2 (2400-bit balls, 863 s, peak about 1.5 GB): k = 0–33, FINAL ok. Its log prints the relative twin ball radius as 0.0 from
  k = 32, because the value underflows the float (below 1e−308).
Scripts: og_window.py (reuses certified_orbit.py's certified face tools unchanged), window_tools.py (detector), window_controls.py.

## LEADS
1. Prove R_σ(D_k) → 0. A route: the lemma's projection loses the factor |cos ∠(σa, σn)|. Show that the twin face planes come
   uniformly close to the centre (og-margin §28a found medians of 0.08–0.12 of the face size).
2. The faster-than-geometric decay against the cut fraction and the digit growth: a law for −log R_σ(D_k)? (ledger retry of 11 Nov:
   "does twin contraction track the cut fraction?" — still open.)
3. The upward family X_k (polars) has its own twin family. By the same lemma applied to polars, its twin INRADIUS should grow. Test
   whether it is unbounded and at what exact rate.
4. A window needs a fixed lattice. A rescaled family φ^{m_k}·D_k with m_k chosen to keep the twin radius near 1 might show a limiting
   twin shape. Check whether the shapes settle on one orbit polytope (dodecahedron and 60-corner types dominate).
