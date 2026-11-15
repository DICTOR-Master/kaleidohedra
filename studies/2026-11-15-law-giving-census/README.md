# Law-giving census: every law-giving shape in the Wythoff universe (15 Nov 2026)

**Verdict (15 Nov 2026): inside the universe searched, no NEW law-giving shape exists. Every law-giving point found is either a known shape with a classical mechanism or one of DICTO's known stations, and all of them were re-found: the uniform members that are fixed by a diagram automorphism (10 families, laws forced by evenness and by the extra symmetry of the larger group), Kelvin's truncated octahedron and the 24-cell (site swaps of the cube–cross-polytope lines), Icosaxes (#94, forced by its two icosahedral halves), and the turn's fixed point √3. That "nothing new" is a theorem for the forced kind: in the seed space of a finite reflection group, every similarity between two members comes from a diagram automorphism, so every fixed point of a family involution sits on the automorphism-fixed locus, where the members are uniform or have the larger group's symmetry. The census also turned up two coincidences that no symmetry explains, and they are the one new thing it found: two golden members of the 5-cell (A4) families are silent in two degrees at once. They are not law-giving under the definition, because nothing is shown to force them. Both corner sets lie inside a 600-cell. They are NEW CANDIDATES, and the mechanism behind them is open. The seed-space sub-study then found a curve of joint zeros through the second of them (numeric), which makes it an edge coincidence. The first (T₅ = T₇ = 0) remains open.**

DICTO asked on 15 Nov 2026: "How many rule-making shapes are still out there undiscovered … prioritise finding any and all." This study continues studies/2026-11-13-swaps-and-fixed-points, 2026-11-14-forced-fixed-points and 2026-11-15-whats-missing. They tested a short list of candidates. This study sweeps one stated, finite universe completely. Computation, proofs and drafting were done with Claude (Anthropic).

## 1. The definition (one, operational)

A **law-giving shape** is a member S(x*) of a one-parameter family of convex polytopes S(x) at which an exact law is **forced**, proved exactly, with the controls passing. Forced means one of the following:

- **(P) parity.** A geometric involution s of the family fixes x*, and a battery quantity Q is odd under s (Q∘s = −Q). Then Q(x*) = 0.
- **(E) evenness.** A geometric involution s fixes x*, and Q is even and differentiable. Then Q′(x*) = 0, which is a maximum if Q is concave and a minimum if Q is convex (Palais 1979; Lindelöf 1869 in the classical case).
- **(X) extra symmetry.** The member at x* has a symmetry its neighbours lack, either of the whole shape or of each piece of a canonical splitting of its corners into orbits. Then every tone that the larger group has no invariant for vanishes. #94 is of this kind.

Geometric involutions are similarities, polarity, site swaps in a tiling and the turn μ ↦ c/μ. Every point is fixed by some abstract involution, so only geometric ones count. The **battery** is: the corner tones T_k for every degree k ≤ 20, the canonical form at the centre (equivalently the Mahler product vol·vol(polar)), the isoperimetric quotient V^(d−1)/A^d, the Dehn invariant (3D), extra symmetry, self-duality, and the involution test. A zero or critical point that nothing forces is a **crossing**, and a crossing is not law-giving. A crossing where two independent quantities vanish at once is a **coincidence**. In a one-parameter family that is a codimension-2 event, so it is the signature of a hidden law and gets examined one by one.

Two tests DICTO's list names discriminate nothing in this universe, and the reason is stated rather than computed:

- **The canonical-form residue test** holds for every convex polytope, because every convex polytope is a positive geometry (Arkani-Hamed, Bai and Lam 2017). DICTO's solids all passed it in studies/2026-11-12-solids-canonical.
- **Euler, balance and swap counts** depend only on the combinatorial type, which is constant on each open family.

## 2. The universe and its coverage

**U1, Wythoff families.** For each finite reflection group G ∈ {A3, B3, H3, A4, B4, D4, F4, H4}, take the polytopes P(c) = conv(G·v), with v = Σ c_j w_j over unit simple roots, so that 2c_j are the edge lengths. A family is an edge-length pattern c ∈ {0, 1, t}^r with at least one 1 and at least one t, where t > 0. Patterns are taken up to t ↔ 1/t and the diagram automorphisms. **104 families (286 raw patterns)**, plus every station c ∈ {0,1}^r (the uniform polytopes, which are the t = 1 members and the endpoints). On an open family the combinatorial type, the facet normals and the dihedral angles are constant, so every battery quantity is an exact algebraic function of t. These families contain:

- every polar sweep P ∩ μP* of a regular polytope in 3D and 4D (each is two edge families meeting at the rectified station), which includes the cube–octahedron and icosahedron–dodecahedron lines;
- every truncation sweep and every Wythoff ring pattern;
- the permutohedron of every group (the all-ones station) and the omnitruncated families;
- the zonotope families of B3, B4 and F4, for example (1, 1, t), the silent-zonohedron line;
- the golden members that lie on these lines, such as Icosaxes.

**Coverage of U1.** All 104 families × (tones k = 1…20, Mahler, isoperimetric quotient, involution test, extra symmetry, f-vector self-duality screen) were computed exactly: **0 FAIL in 284 in-run checks**. The Dehn invariant was computed for all 16 three-dimensional families. It is proved for A3 and B3, where every angle has the form pπ + qβ with β = arctan(1/√2), shown exactly. For H3 it rests on angle relations found by PSLQ, whose completeness is not proved. The Dehn invariant in 4D was not computed (see section 6). The extra symmetry was computed for every family of A3, A4, B4, D4 and F4. For B3, H3 and H4 it is impossible (section 3).

**Beyond the {0,1,t} lines (proved, not computed).** For the forced kind, coverage extends to every curve in every seed space by the theorem of section 3. For crossings it does not: the full seed spaces (2 parameters in 3D, 3 in 4D) are searched for silent coincidences in the companion study silent/ (section 5).

**U2, the turn on polar lines.** This is a control only. Ledger [71] settled the Turn Theorem for every regular polar line, and [199] settled the near-but-never-on question.

**U3, site-swap lines.** On the cube–cross-polytope line in every dimension d, the swap μ ↦ d − μ pairs a cell with its complementary cell in the two-cell tiling, so the Dehn invariant is odd and vanishes at μ = d/2. That point is the Voronoi cell of the body-centred lattice: Kelvin's cell for d = 3 and the 24-cell for d = 4. This was checked exactly in 3D, and the 24-cell's corners were checked exactly in 4D. The zinc blende and rock salt swaps are cited from ledger [225].

**U4, stackings (c/h words).** These are covered by the proof in whats-missing, Part 1: every Window-Law quantity is affine in the word shares, and reversal and c ↔ h only permute them, so they force invariance and single out no word. Nothing was recomputed.

**What fraction is covered.** Of the family classes on DICTO's list, these are covered completely in U1 and U3: polar sweeps, Wythoff seeds with their truncation sweeps, the cube–octahedron and icosahedron–dodecahedron lines, the permutohedra and the root-system zonotopes. The turn is covered as a control. The stackings are covered by an earlier proof. Golden-cut families are covered only where they lie on Wythoff lines. Of the battery in U1, 5 of 6 test types run on every family. The sixth, Dehn, runs on 16 of 104 families (all of 3D).

## 3. Why nothing NEW can be forced in U1 (theorem)

Take two members of the same pattern, P(c₁) and P(c₂), related by a similarity f. Generically both have symmetry group exactly G (extra symmetry is classified below), so f conjugates G to itself and lies in the normaliser of G in O(d) times scalars. The normaliser of a finite irreducible reflection group is G extended by the diagram automorphisms that are realised as isometries, together with −I. With unit roots every diagram automorphism σ is an isometry, because it preserves the Gram matrix. So c₂ ∝ σ(c₁). On a {0,1,t} family the edge lengths are {2, 2t}, so a similarity between two different members must have ratio t and exchange the 1-edges with the t-edges. The only possible involution is therefore t ↦ 1/t, and it exists exactly when σ(p) = swap(p).

This was tested independently on every family. The identity T_k(t) ≡ T_k(1/t) for all k (an O(d)-invariant necessary condition for similarity) holds on exactly the 10 families with such a σ and fails on the other 94, at the first differing degree. Every such check passed.

Extra symmetry has three sources:

- A3 → B3, A4 → A4 × {±1}, and D4 → B4 and F4. These are the automorphisms themselves, so the extra symmetry sits exactly at σ-fixed seeds. This was checked on every family by solving h·r·v(t) = v(t) over all h ∈ G (exact). The extra symmetry appears at t = 1, or along the whole family when the pattern itself is symmetric.
- B4 → F4, the only accidental case. It was found only at t = 1, or along whole families (6 B4 families are F4 families in disguise). No non-uniform B4 member has F4 symmetry.
- B3, H3 and H4 cannot gain symmetry. Between them, the orbit sizes and the inclusions of the finite groups exclude every candidate: T_d ⊄ I_h, no B3 orbit is I_h-invariant, and 120 does not divide 192, 384 or 1152, so no D4, B4 or F4 orbit is H4-invariant. The free A4 orbit is the omnitruncated 5-cell, which is combinatorially not the 600-cell.

**Hidden symmetry of halves in 3D (complete).** Suppose a G-orbit splits into K-orbits that are K′-orbits for a group K′ ⊄ G. A tone is killed only if K′ lacks an invariant in a degree where G has one. Among polyhedral groups only I and I_h lack degrees 4 and 8, and every polyhedral group has invariants of degree 6 and 10. So the only case is B3 (and A3) with K = T_h or T and K′ = I_h or I. Transitivity on the 12 corners of an icosahedron forces v ∝ (0, 1, φ). **The unique such point is Icosaxes.** The census found exactly this: T₄ = T₈ = T₁₄ = 0 at t = φ on the B3 truncated-octahedron line, and at t = 1/φ on its A3 copy. T₁₄ = 0 was predicted before it was checked, and T₆, T₁₀ and T₁₂ are rightly nonzero.

## 4. Every law-giving shape in the universe

| # | shape | family / involution | forced law (exact) | mechanism | class |
|---|---|---|---|---|---|
| 1 | cuboctahedron | A3 x3o3t, t ↦ 1/t (diagram reversal) | odd tones T₃, T₇ … T₁₉ = 0; T₄ min, T₆ … T₂₀ max; Mahler max | (X) central symmetry + (E) | KNOWN |
| 2–5 | four uniform 5-cell relatives: o3x3x3o (bitruncated 5-cell), x3o3o3x (runcinated), x3x3x3x (omnitruncated, two families) | A4, reversal | all odd tones T₃ … T₁₉ = 0; even tones critical; Mahler max | (X) −I + (E) | KNOWN |
| 6 | o3o3x *b3x (D4 member with B4 symmetry) | D4, transposition | tones critical (none killed); Mahler max | (E) | KNOWN |
| 7–10 | four F4 uniform members: o3x4x3o (bitruncated 24-cell), x3o4o3x (runcinated 24-cell), x3x4x3x (omnitruncated, two families) | F4, reversal | T₆ = T₁₄ = 0 (the extended group [[3,4,3]] kills them); even tones critical; Mahler max | (X) + (E) | KNOWN (ledger [212]) |
| 11 | Kelvin's truncated octahedron | B3 truncated-octahedron line, CsCl site swap μ ↦ 3 − μ (t ↦ 1/t, not a similarity) | Dehn = 24√2(2μ − 3) ⊗ β, odd: zero at 3/2 | (P) | KNOWN (Kelvin 1887; DICTO #100 parity) |
| 12 | 24-cell | tesseract–16-cell line, swap μ ↦ 4 − μ | Dehn zero (two-cell tiling); tiles | (P) | KNOWN |
| 13 | Icosaxes (octahedron truncated at 1/φ² of each edge) | B3 x3t4o at t = φ; A3 x3t3x at 1/φ | T₄ = T₈ = T₁₄ = 0 | (X) two icosahedral halves | DICTO-known (#94); mechanism Delsarte–Goethals–Seidel 1977 |
| 14 | turn fixed point √3 (cube–octahedron line) | turn μ ↦ 3/μ | t_min = 5 − μ − 3/μ even, maximum 5 − 2√3 | (E) | DICTO-known (#81) |

Also forced, but holding along the whole family, so no point is singled out:

- 1 A3, 1 A4, 1 F4 and 6 D4 families are pointwise symmetric under an automorphism. They are copies of families of the larger group.
- 6 B4 families carry F4 symmetry along their whole length.
- The B3 zonohedron family (1, 1, t) has Dehn 0 at every t.

At t = 1, 11 further families have no involution, but their uniform member is automorphism-symmetric, so the tones of the larger group are killed there by (X): A3 x3x3t; A4 111t and 11t1; B4 10t0, 11t0 and 1tt0 with F4 (T₄ = T₁₀ = 0); D4 101t, 111t and 11tt; F4 111t and 11t1. These are uniform polytopes, so they are KNOWN.

No open family contains a self-dual member: f₀ ≠ f_(d−1) on all 104.

## 5. Crossings and coincidences (not law-giving; where more could hide)

Positive real crossings found and certified:

| group | tone zeros (degrees ≤ 20) | Mahler critical points | IQ critical points | Dehn zeros (3D) |
|---|---|---|---|---|
| A3 | 89 | 4 | 3 | t = 2 on o3x3t (truncated tetrahedron), t = 1 on x3x3t and x3t3x |
| B3 | 44 | 6 | 5 | t = 1 on x3t4o (Kelvin), x3t4x, x3t4t; whole zonohedron family x3x4t |
| H3 | 55 | 5 | 4 | t = 1 on the three omnitruncated families (PSLQ-conditional) |
| A4 | 107 | 15 | 13 | — |
| B4 | 68 | 23 | 17 | — |
| D4 | 24 | 8 | 6 | — |
| F4 | 64 | 14 | 13 | — |
| H4 | 35 (T₁₂: 10, T₂₀: 19) | 18 | 11 | — |

Tone zeros come from exact rational norms, factored over Q, with roots isolated by arb balls. A root is certified genuine when the conjugate branch excludes 0. For A3 and B3 a Dehn zero is a rational t, because Dehn = 1 ⊗ X + t ⊗ Y. The IQ critical points come from resultants over all the square roots. Most are certified as genuine branches, and the rest are roots of the exact norm that agree to 120 digits.

**Coincidences (two quantities zero or critical at the same member).** There are 416 in all. 408 lie at t = 1 at members with extra symmetry, where every one is explained by (X) and (E). This was checked family by family. The remaining 8 are:

- 6 are Icosaxes (B3 and A3; T₄, T₈, T₁₄): explained.
- **2 are unexplained (NEW CANDIDATES):**
  - **A4 o3o3x3t at t = φ.** The 20 corners are the permutations of (φ², φ², φ², φ, 0), centred. T₅ = T₇ = 0 exactly, while T₃ ≠ 0 and T₄ ≠ 0 (tone zeros up to degree 24: 1, 2, 5, 7).
  - **A4 o3x3o3t at t = 1/φ.** The 30 corners are the permutations of (φ², φ², 1, 1, 0). T₃ = T₆ = 0 exactly (zeros: 1, 2, 3, 6).

  What is proved about them (`golden_a4*.py`, logs `data/golden-a4*.log`):
  - Their symmetry group is exactly S5, of order 120, the generic order (automorphisms of the exact Gram matrix). The control member t = 2 also has order 120 and no extra zeros.
  - Every cosine between their corners lies in the 600-cell set {0, ±1/2, ±φ/2, ±1/(2φ), ±1}. The 20-set closes under reflection in its own members to exactly 120 points, so it lies in a 600-cell (exact). That 600-cell splits into S5-orbits of sizes 20, 20, 20, 30, 30. A float screen shows that the 30-set lies in the same 600-cell.
  - None of the 156 subgroups of S5 splits the 20-set into pieces that are each silent in degrees 5 and 7. Under the Frobenius group F20, the 30-set splits into a 10-piece and a 20-piece, each silent in degrees 3 and 6. That is a partial piecewise reduction, but the reason the pieces are silent is not shown.

  These are the census's real finding: two golden 5-cell-family shapes inside the 600-cell whose double silence is forced by nothing found so far. **Prior art:** none found. Sources checked: Wikipedia "600-cell"; errorcorrectionzoo.org pages for the 600-cell and spherical designs; Cohn and Kumar, "Universally optimal distribution of points on spheres" (arXiv math/0607446), which notes that harmonics of degrees 13–19 sum to zero over the 600-cell; Delsarte, Goethals and Seidel 1977; and two web searches (standard; queries on "600-cell A4 coordinates S5" and "spherical design S5 orbit golden truncated 5-cell"). The free library copy of Goethals and Seidel 1981 was not read.

**Seed-space silent census** (`silent/README.md`, the lead of ledger [223]). This sub-study searched the full 2-parameter (3D) and 3-parameter (4D) seed spaces for over-determined silent points, meaning more tone zeros than parameters. Its results:

- **3D, exact and complete (degree pairs up to 16):**
  - B3 has exactly one 48-point 7-design (T₄ = T₆ = 0), with T₈ ≠ 0 there.
  - H3 has no 11-design anywhere.
  - Every over-determined 3D point is explained by symmetry: Icosaxes, or the centrally symmetric A3 seeds.
- **4D, exact by Gröbner bases in orbit-space coordinates:**
  - None of these exists: B4 9-designs, F4 13-designs, H4 29-designs, D4 9-designs.
  - The B4 7-designs and F4 11-designs lie on curves.
  - Every D4 5-design found is triality-fixed (F4, explained).
  - A4 has a single 5-design orbit, which is centrally symmetric.
  - H4 T₁₂ = T₂₀ = 0: no real seed was found in 300 starts (numeric only).
- **The two A4 golden members:**
  - Permutations of (φ², φ², 1, 1, 0), T₃ = T₆ = 0: a numerical continuation follows a curve of joint zeros from this edge point into the interior. So it is where an ordinary curve meets the edge, a coincidence on the edge only. This weakens it as a candidate (numeric).
  - Permutations of (φ², φ², φ², φ, 0), T₅ = T₇ = 0: the continuation failed, so this one is unsettled. **It stays the one open candidate.**

**Settled the same day (studies/2026-11-15-golden-a4-candidate):** both golden members are S5-orbits of one 600-cell (twisted conjugacy classes of the binary icosahedral group). On the 600-cell, degrees 5 and 7 see one invariant function, and integrality of the twisted character table (2u + 3v = 6 in whole numbers) forces it to vanish on one orbit type. This is a law forced by representation theory (new kind (R)), and with it all 416 coincidences are explained.

The sub-study did not cover H4, D4 and F4 on the faces, edges and vertices of the seed simplex, nor a full sweep of all triples in 4D.

## 6. Outside the universe (where more could hide) and how to search next

1. **The mechanism of the two A4 golden coincidences.** Next, compute the signed contents of the S5-invariant harmonics of degrees 3, 5, 6 and 7 for each of the five S5-orbits of the 600-cell (20, 20, 20, 30, 30), and look for a relation forced by the H4 element that normalises S5, or by √5 ↦ −√5. If one is found, the two members become law-giving of type (X)/(P). If none is found, they are a new kind.
2. **Golden members of B4, F4 and D4 lines by the same test.** The census found none there. Search the hidden symmetry of halves in 4D, with subgroups shared with H4 such as [3⁺,4,3], by the method of section 3 (orbit sizes rule out H4 for whole orbits only).
3. **The Dehn invariant in 4D** on all 88 four-dimensional families, using 2-face areas ⊗ dihedral angles with exact angle relations. Only the site-swap lines are settled.
4. **Non-Wythoff families:** truncated tetrahedra with unequal corner cuts (DICTO's golden Dehn-zero list, ledger [4] and [26]), the OG family, Narcissus twists, and yantra cones. They were covered one by one in earlier studies, not by a census.
5. **Polar (Catalan-type) families.** Their dihedral angles vary with t, so a Dehn zero needs angle relations that vary as well. The direction tones of their corners are constant on each family.
6. **General lines and curves in seed space** (crossings only; the forced kind is closed by section 3).
7. **Star polytopes and Galois twins.** The turn's leads ([71]) and Galois conjugation map the convex families to star families, which this census leaves out.

## 7. Controls (`scripts/controls.py`, `data/controls.log`: 26 checks, 0 FAIL)

| control | result |
|---|---|
| turn √3: t_min = 5 − μ − 3/μ (recomputed from the corners at μ = 8/5, 7/4, 19/10), even, t″ = −2√3/3 | qualifies |
| Kelvin 3/2: census Dehn 1 ⊗ (−48β) + t ⊗ 48β gives Dehn(μ) = 24√2(2μ − 3)β, odd under μ ↦ 3 − μ | qualifies |
| cube: truncated-cube family Dehn = 1 ⊗ 48β, which vanishes only as the 1-edges shrink (the cube end) | re-found |
| rhombic dodecahedron: all dihedral angles 120° | Dehn 0, re-found |
| Icosaxes: B3 orbit of (φ, 1, 0) = two regular icosahedra (exact); T₄ = T₈ = T₁₄ = 0 at φ | re-found, T₁₄ predicted |
| DICTO silent zonohedron: T₄ = 0 on (1, 1, t) exactly at t = √2·a* | re-found |
| 24-cell = [−1,1]⁴ ∩ 2·cross-polytope, the fixed point of μ ↦ 4 − μ | re-found |
| random μ = 8/5 | fails to qualify, as required |
| wrong claims: a similarity involution on the B3 truncated-octahedron line; a Dehn zero at 8/5; Kelvin silent in degree 4; T₆, T₁₀, T₁₂ zero at Icosaxes | all rejected |

The in-run checks (284, 0 FAIL) are:

- on every family, the involution test agrees with the diagram;
- extra symmetry appears exactly where the seed is automorphism-fixed (A3, A4, F4);
- tones and the Mahler product are critical at every fixed point;
- every A3 and B3 dihedral angle is proved of the form pπ + qβ.

## Method, files, runs

- `scripts/exact.py`: Q(√D) and Q(√D)[t] on python-flint, with certified roots.
- `scripts/groups.py`: unit roots, dual weights and group elements (H4 is found among the 120 unit icosians).
- `scripts/census.py`: the battery. It covers the tones by pair sums over G of Gegenbauer polynomials, the volume by the chamber-cone decomposition vol = |G|·√det(Gram_w)/d!·Σ over chains |det|, and Ω(0) = d!·vol(polar) = |G|·√det(Gram_w)/Π⟨w_i, v⟩. It also computes the isoperimetric quotient, Dehn, extra symmetry and the similarity test.
- `scripts/dehn.py`, `scripts/controls.py`, `scripts/summarize.py`, `scripts/golden_a4.py`, `golden_a4b.py`, `golden_a4c.py`.
- Data: `data/census-*.json` and `.log`, `data/summary.json`, `data/tables.md`, `data/controls.log`, `data/golden-a4*.log`, `data/pilot-*.log`.

Runs went through the job gate on the two compute hosts:

- pilot lgc-pilot: FINAL ok;
- full runs lgc-1 (A3, B3, H3, B4, F4, H4; 8 workers; H4 807 s) and lgc-2 (A4, D4): both FINAL ok;
- controls lgc-ctl: FINAL ok.

The whole Wythoff universe is computationally small, because exact closed forms replace hulls. The time went into the H4 isoperimetric resultants. Nothing is left running.

Credits at the point of use: Palais 1979 (symmetric criticality); Delsarte, Goethals and Seidel 1977 (designs); Arkani-Hamed, Bai and Lam 2017 (positive geometries); Kelvin 1887; Coxeter (uniform polytopes, normalisers of reflection groups); the polytope Wythoff construction; arb and FLINT (python-flint) for certified arithmetic.

## Ledger line

Concordance ledger entry of 15 Nov 2026, "law-giving census over the Wythoff universe". The forced kind is closed in U1 by the normaliser theorem. All 14 law-giving points are known and re-found. The two A4 golden double-silent members are new candidates with no known mechanism. Retry: only the leads of section 6.

DICTO · dictospheres.com
