#!/usr/bin/env python3
"""Gap triage 2026-11-09: one table of every open Concordance gap -> gap-triage.json, README.md, papers/gap-triage/paper.html.
Desk triage only (no new mathematics). Data typed by hand from concordance.json (gaps.ranked, gaps.loose, gaps.weak, ledger
entries still OPEN/RUNNING/UNDECIDED) and the studies they name. Run: python3 build_triage.py (local, seconds)."""
import json, html, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.expanduser('~/k-research/papers/gap-triage')

CAT = {'A': 'closable now with existing tools', 'B': 'reduced to one named lemma', 'C': 'needs a new idea from DICTO',
       'D': 'belongs to the one-piece aim', 'E': 'not mathematics / housekeeping'}

# fields: id, list, src, what, status, cat, tool, step, size, lemma, question, hop, flag, boulder
G = []
def g(**k):
    base = dict(tool='', step='', size='', lemma='', question='', hop='no', flag='', boulder='')
    base.update(k); G.append(base)

# ---------------- ranked (concordance gaps.ranked; rows 0,1,2,4,7,8,10 are SETTLED/PROVED/ANSWERED/PUBLISHED and skipped)
g(id='R3', list='ranked 3', src='#91, #76', what='#91 Lemma 6 (120-cell cell rule) exact, so that the 600 × 120 result becomes a theorem',
  status='open, untouched (cross-link found 4 Nov: #76 edge-equalising cuts = #91 uniform stations)', cat='A',
  tool='exact Q(√5) hull builds; #76 exact constructions', step='build the three #76 stations (μ = (9+√5)/12, (11+3√5)/20, (15+8√5)/38) exactly and verify Lemma 6 there; then state Lemma 6 in general as the remaining lemma',
  size='medium', lemma='Lemma 6 for every μ (the general cell rule) stays a named lemma after the stations', hop='yes: sphere row, stations are walls of S(μ) = P ∩ μP*', boulder='B3')
g(id='R5', list='ranked 5 = loose 23', src='#66, #67, #84', what='Hexagonality Law for the Laves big atom on every stacking (exact to 6 layers)',
  status='open, untouched; the big atom reads three layer types, so the one-layer law does not reach it', cat='B',
  lemma='Three-layer Window Lemma: the big atom\'s neighbour counts are a linear function of the frequencies of c/h words of length 3, and the Swap-type combination of #84 makes them a line in h',
  tool='Window Law (#84) at g = 3; exact stackings to 6 layers', step='write the big atom counts as a function of length-3 window frequencies on the 42 exact stackings and solve for the linear form',
  size='medium', hop='partly: paraboloid row (weights), the law itself is a counting identity')
g(id='R6', list='ranked 6', src='#80, census scripts', what='Star and Star Halo of all classical solids: a full map of known and new stars and halos',
  status='open, untouched', cat='A', tool='star-cores census scripts + #80 exact gains; reference library for prior art',
  step='run the census on the 5 Platonic, 13 Archimedean, 13 Catalan solids exactly; list each star and halo with its gain; then library check',
  size='medium', hop='partly: the star chain is a growth slider with #80 gains as its eigenvalues', boulder='B5')
g(id='R9', list='ranked 9', src='#57, #93, studies 2026-11-04-trd', what='The TRD DICTOnode in a paper (TRD as the RD\'s h partner)',
  status='STUDIED (note The Turned Twin, read ok); clock positions of the turned node fixed today; paper not written', cat='E',
  tool='writing', step='draft the HexOct-volume chapter from the read-ok note and today\'s exact clock drawing', size='small')
g(id='R11', list='ranked 11 = loose 2', src='#48', what='Golden split in the other AXE networks (new convex pairs); printed keyed sets',
  status='open, untouched', cat='A', tool='#48 method and its uniqueness theorem; exact Q(√5) builds',
  step='list the AXE networks not treated in #48 and run the split at t = φ on each; printed sets go to the build list (E)',
  size='medium', hop='partly: the golden split is a metric event (linear edge-ratio factor) on the t slider', boulder='B5')
g(id='R12', list='ranked 12 = loose 14', src='#49', what='Archimedean stretches and caps; prior art for the five-fold stretch',
  status='open, untouched; the theorem covers every equal-edged solid, listing and prior art remain', cat='A',
  tool='Polyhedral Stretching Theorem (#49) + reference library', step='enumerate stretches of the 13 Archimedean solids by their axes; library check for the five-fold stretch (Johnson solids, near-misses)',
  size='medium', hop='partly: a stretch is a scale slider', boulder='B5')
g(id='R13', list='ranked 13 = loose 3', src='#35, #91, #34', what='Closing solid for the loose step O ⊂ rTI (Vajrayana cycle); the 9/φ⁴ coincidence; a physical build',
  status='open, untouched; ranked note: a golden-cut station of #91 may fit (unsure)', cat='A',
  tool='#91 golden-cut station list + exact containment test (#43 t_min)', step='test every #88/#91 golden-cut station S for O ⊂ S ⊂ rTI exactly and for tightness; 9/φ⁴ = #34\'s tightest cycle, cite rather than explain; the build goes to E',
  size='medium', hop='partly: containment constants are the sphere row (t_min)')
g(id='R14', list='ranked 14', src='#89 §7, #93, #47', what='Join the fill thread to the cuts and the sweep (#47 questions 1 and 3)',
  status='open; #47 question 1 ANSWERED 6 Nov (C + T + O without connectors); question 3 (periodic in three directions) open', cat='E',
  tool='Concordance tagging', step='tag #89 §7 and #93 as fill papers; the remaining #47 question goes with loose 13', size='small')

# ---------------- residuals of rows marked settled
g(id='R8r', list='ranked 8 residual; ledger 19', src='#93, studies 2026-11-04-rt-pyramids', what='Do the rhombic triacontahedron\'s centre pyramids tile space? (the one Dehn-zero isohedral case left)',
  status='UNDECIDED since 4 Nov; the overnight search result was never read', cat='D',
  tool='SAT tiling test on skewed tori; aperiodic-monotile clue checklist', step='read the 4 Nov overnight log; if alive, rerun as SAT exact cover on periodic boxes; a "no periodic, yes patches" answer makes it a monotile candidate',
  size='medium', hop='no', flag='stale: a result exists unread', boulder='B4')
g(id='R10r', list='ranked 10 residual = loose 18', src='#53', what='#53 Observation 3: a closed rule that reads the walk type off the sites',
  status='PARTIAL: Prop. D gives the type as the sign of τ_A + τ_B (one linear programme per like pair); midpoint rule for centrosymmetric pairs', cat='B',
  lemma='Symmetry Rule: the sign of τ_A + τ_B is fixed by the site symmetry (hole type) of the like pair',
  tool='switch theorem, Prop. D, likebirth.py', step='tabulate τ_A + τ_B against site symmetry on all twelve networks', size='small',
  hop='yes: paraboloid row; step vs jump is exactly this sign')

# ---------------- loose
g(id='L0', list='loose 0', src='#92, #93', what='Centre-pyramid leftovers: tilings not face to face (#93: 7 edge and 3 face combinations); TRD centre pyramids; octahedron pyramids conjecture',
  status='partly done: reversed neighbour SETTLED, #92 Table 2 complete, RD non-face-to-face SETTLED (uncountably many); TRD trapezoid pyramid tiles alone (SAT, 5 Nov), twisted control and prior art pending', cat='A',
  tool='SAT tiling tests (skewed tori); exact contact polygons', step='finish the TRD control and prior art (small); run the 10 non-face-to-face combinations of #93 as SAT tests',
  size='medium', lemma='octahedron pyramids: a sliding-edge lemma as #92 Cor. 9 (B part)',
  flag='stale wording: three of its four items are settled', boulder='B4')
g(id='L4', list='loose 4', src='#36', what='Golden fill G′ of the bcc gap (10.22%)', status='paused',
  cat='C', question='What counts as the golden fill of the 10.22% bcc leftover: golden rhombohedra only, or any pieces whose corners are golden?')
g(id='L5', list='loose 5', src='#36', what='Golden Bull-horns adaptor; rhombic division of the 72-piece gap; Cleo-Ico adapters; oblique layers at the seams',
  status='open', cat='A', tool='hole_piece_cut.py (Voronoi cell minus pieces), exact Q(√5) builds',
  step='check whether 2026-11-05-og-pentagons (Bull-horns adaptor for the cut OG, calibrated 0.111898) already is the golden adaptor; then the rhombic division of the 72-piece gap',
  size='medium', flag='possibly done: og-pentagons computed a Bull-horns adaptor for the cut (golden) OG')
g(id='L6', list='loose 6', src='#30', what='Fibonacci spine as a thinned cut-and-project chain; seams as model sets; off-plane core rings; other solids with five inscribed cubes',
  status='open', cat='A', tool='approximant ladder (cut-and-project rungs), Fibonacci stacking spectrum',
  step='project the spine from the approximant-ladder lattice and find the thinning window; five inscribed cubes: check the icosahedral solids of the library',
  size='medium', lemma='seams as model sets: a window lemma (B part)', hop='partly: the outline predicts aperiodic order = polar line at irrational slope')
g(id='L7', list='loose 7', src='#40', what='Space the DBT and OTT leave on mixed stackings; OG on aperiodic stackings with diffraction',
  status='open', cat='A', tool='Fibonacci stacking spectrum (pure-point c/h word, exact amplitudes); exact stackings', step='compute the leftover volume per layer type on the 42 exact stackings (linear in h if the window law holds), then the Fibonacci diffraction',
  size='medium', hop='partly')
g(id='L8', list='loose 8', src='#41', what='Third level of Hexas; physical puzzle', status='queued', cat='C',
  question='What makes a Hexa of the third level: Hexas built again from Hexas (at which scale), or a new kind of join?', lemma='', step='physical puzzle: build list (E)')
g(id='L10', list='loose 10', src='#43', what='Conjecture 1 (OG margin t_min(D_k) ≤ 3/φ²); shell 5 exact; the full flip',
  status='Conjecture 2 PROVED (#43 v2); Conjecture 1 REDUCED: exact for k ≤ 11, base r(D_12) exact; monotonicity of r is false', cat='B',
  lemma='New-Face Lemma: every new face of D_j (j ≥ 13) stays at distance at least (φ²/3)·R(D_{j−1}) from the centre',
  tool='Lemma G (og-gnomon), exact Q(√5) builds', step='prove the lemma for the five-fold faces first (the only ones that dip); shell 5 exact and the full flip are small exact builds (A)',
  size='large', hop='partly: sphere row; invariant-polynomial certificates proved insufficient (cover 0.7947, need 0.92)',
  flag='stale wording: Conjecture 2 is proved')
g(id='L11', list='loose 11', src='#43', what='Shell ratios against Tsai clusters and virus capsids', status='queued', cat='A',
  tool='reference library', step='take published Tsai shell radii (Takakura et al.) and capsid T-number radii; compare with the exact #43 ratios', size='small')
g(id='L12', list='loose 12', src='#45', what='Conjecture 1: the symmetry axes give the largest width of the Reuleaux Platonic bodies',
  status='open; numerical evidence from 3000 directions', cat='A',
  tool='stationary events (Hopscotch type 3) + spherical-design certificates', step='write the width w(u) = h(u) + h(−u) piecewise on the fundamental triangle and list its critical points exactly; compare values',
  size='medium', hop='partly: a stationary event of the width on the sphere')
g(id='L13', list='loose 13', src='#47', what='Smallest kit; face to face; periodic in three directions',
  status='open (C + T + O with no connector ANSWERED 6 Nov: yes, never face to face)', cat='A',
  tool='SAT tiling tests on skewed tori', step='SAT: fewest piece kinds that fill face to face, then a 3-periodic test on tori of growing size',
  size='medium', boulder='B4')
g(id='L15', list='loose 15', src='#50', what='Catalogue of perfect points; which dissection fillers (Hill, Sommerville, Goldberg) the lattice moves reach',
  status='open', cat='A', tool='switch theorem walls + Goldberg/Sommerville lists in the library', step='list the perfect points as walls of the move sliders; match each filler of the three classical lists against the reached solids',
  size='medium', hop='yes: perfect points are events on the move sliders')
g(id='L16', list='loose 16', src='#51', what='One solid per bond that fills space alone; printed Samson and Delilah',
  status='open', cat='A', tool='Dehn screen (exact) + SAT tiling', step='screen each bond\'s pieces for Dehn zero (O(t) is nonzero for t > 0 except the RD, 4 Nov); SAT only on the survivors; prints to E',
  size='small')
g(id='L17', list='loose 17', src='#52', what='Scale anomaly; web of the keyed bond', status='open', cat='C',
  question='For the web of the keyed bond: should the keys appear as a second colour of bond in one network, or as their own network beside the Web of Bonds?',
  step='scale anomaly: physics inputs, already read in studies 2026-10-25-scale-anomalies (E)')
g(id='L18', list='loose 18', src='#53', what='Exact walks of three-kind networks (Observation 3 has its own row)',
  status='Obs 1, 2, 4 PROVED; quadrilateral version of Obs 1 DISPROVED; the common reason is Theorem A; three-kind walks open', cat='A',
  tool='switch theorem / flip formula with two weights', step='walls become lines S₀ = λ₁S_A + λ₂S_B in the weight plane; run the #57 census engine on one three-kind network (perovskite)',
  size='medium', hop='yes: paraboloid row, one determinant linear in each weight', flag='stale wording: most of the row is proved', boulder='B2')
g(id='L19', list='loose 19', src='#54', what='A shorter run as a classical gnomon; capped cubes at other sizes',
  status='open', cat='A', tool='exact hull builds; gnomon criterion (og-gnomon)', step='apply the gnomon criterion of og-gnomon to runs of length 1 and 2; cap cubes at sizes 2..6 exactly', size='small')
g(id='L20', list='loose 20', src='#55', what='Weight walks of σ, Z, C15 and other Frank–Kasper phases; 4D two-kind walks',
  status='partly queued', cat='A', tool='#57 census engine + switch theorem', step='feed σ, Z, C15 site lists to the census engine; flips by the flip formula',
  size='medium', hop='yes: paraboloid row', boulder='B2')
g(id='L21', list='loose 21', src='#56, #57', what='Self-keyed Blockhead; three-kind walk; keyed Chucky and Fang',
  status='open', cat='A', tool='SAT tiling; the three-kind walk engine', step='the three-kind walk joins the #53 three-kind walks; SAT for a key on the Blockhead faces that lets it fill only with itself',
  size='medium', hop='partly (the walk)', boulder='B2')
g(id='L22', list='loose 22', src='#61', what='Swap Rule for s < 1/4 (pieces reaching two gaps)',
  status='open; the splash proof covers s ≥ 1/4', cat='A', tool='splash-determinants circuit lines in (λ, s)',
  step='extend the circuit list to pieces reaching two gaps at s = 1/6 and check the window ends as circuit lines',
  size='medium', hop='yes: the window ends are already verified as circuit lines', boulder='B1')
g(id='L24', list='loose 24', src='#74', what='Loop Equality for all lengths', status='listed open', cat='E',
  step='mark CLOSED: proved for every length and every stacking in #102 (7 Nov)', size='small', flag='CONTRADICTED: #102 proved it (Nagle 1966, Thorpe 1972 credited)')
g(id='L25', list='loose 25', src='#76', what='Exact atlas in Q(√5); proof of part (3)', status='open', cat='A',
  tool='exact Q(√5) hull builds', step='rebuild the atlas stations exactly (they are #91\'s uniform stations, cross-link 3) and prove part (3) station by station',
  size='medium', hop='yes: sphere row', boulder='B3')
g(id='L26', list='loose 26', src='#78', what='Why the prime 89; matching the dodecahedra to the Red Queen\'s nine layers',
  status='open', cat='C', question='When you match the TI Star\'s dodecahedra to the Red Queen\'s nine layers, do you mean layers by distance from the centre, one dodecahedron per layer?',
  flag='CONTRADICTED in part: #80 shows 89 is a prime the number field allows, typical, not special (the "why 89" half is answered)')
g(id='L27', list='loose 27', src='#80', what='Proof that Archimedean chains close in four steps; omnitruncates; the quasi-regular formula',
  status='open (the gains are exact solid by solid)', cat='B',
  lemma='Two-Orbit Gain Lemma: on a solid with two face orbits the growth map acts linearly on the two depths, and its square is a scalar (period 2 or 4)',
  tool='#80 exact gains', step='write the growth map as a 2 × 2 matrix in the two depths and check M² = g·I on the closed cases; omnitruncates have three orbits, which is why they spread', size='medium',
  hop='partly: the turn of a two-orbit line')
g(id='L28', list='loose 28', src='#80, #81', what='Exact edges of the open windows (cube s 49/80–59/80; dodecahedron 87/80–99/80)',
  status='open', cat='A', tool='Hopscotch: events = determinant roots; exact chain with s symbolic',
  step='run the T chain with s as a symbol and find where the face structure of the third step changes; the window edges are among those roots',
  size='medium', hop='yes: incidence events on the s slider', boulder='B1')
g(id='L29', list='loose 29', src='#86', what='Tower move: proof over whole stretches (exact at 402 weights)',
  status='open', cat='A', tool='Hopscotch: between walls the face structure is constant and corners are linear in λ',
  step='take the break points as the walls; on each stretch check the move with λ symbolic (linear corners) at one interior point plus the walls',
  size='small', hop='yes: weight slider, walls already known', boulder='B1')
g(id='L30', list='loose 30', src='#87', what='Vacuus: other centres for solids of low symmetry', status='open', cat='C',
  question='For a solid with no single centre, which point should the Vacuus be built around: the centre of mass, the centre of the largest ball inside, or a point you choose?')
g(id='L31', list='loose 31', src='#87', what='Cardboard sheets for the other solids', status='queued', cat='E', step='build sheets from the existing nets', size='small')
g(id='L32', list='loose 32', src='#91', what='Off-base prism sections; exact stations of the tilted slice; TRD outside the cubic sweep; the factor 2 between 342 and 171 (Lemma 6 has its own row)',
  status='open', cat='A', tool='exact Q(√5) builds; dual-sweeps two-orbit theorem',
  step='factor 2: count orbits exactly (small); tilted-slice stations exactly; TRD: restate as a point of the two-depth plane (dual-sweeps) rather than of a sweep line',
  size='medium', hop='yes: sphere row', flag='premise to restate: dual-sweeps shows two-orbit solids live on a plane of cuts, not on one sweep line', boulder='B3')
g(id='L33', list='loose 33', src='#89, #91', what='Sections of the ten Schläfli–Hess star polytopes', status='queued', cat='A',
  tool='4D section scripts (2026-11-03-4d-sections)', step='load the ten star polytopes (exact Q(√5) corners) and slice at the #89 heights', size='large', hop='yes: height slider')
g(id='L34', list='loose 34', src='#90', what='Structure over Q(√2, √5) beyond natural projections', status='open', cat='C',
  question='Beyond the shadows, which picture do you want: golden and silver cuts mixed on one solid, or one higher-dimensional lattice that casts both?')
g(id='L35', list='loose 35', src='#8', what='Database search for the 1b + 12j point set', status='open', cat='E',
  step='search the crystal databases (Wyckoff 1b + 12j, space group Pm3̄) by hand', size='small')
g(id='L36', list='loose 36', src='#62', what='Six all-triangle 600-cell slices (28, 30, 32, 42, 48, 72 corners); equilateral forms of five patterns',
  status='open', cat='A', tool='600-cell slice scripts; exact Q(√5) heights', step='solve for the exact heights where every face is a triangle (incidence events on the height slider)',
  size='medium', hop='yes: height slider, events are plane determinants', boulder='B3')

# ---------------- weak (gaps.weak)
g(id='W0', list='weak 0', src='#84, #86, #83, #87, #90, #49, #50', what='Concepts in one paper only (Window Law, tower move, knitting slice, Vacuus, field obstruction, stretching, lattice moves)',
  status='open', cat='E', step='tag each concept where it is used again (Window Law → Laves big atom; tower move → #86 stretches)', size='small')
g(id='W1', list='weak 1', src='#48↔#55, #89/#91↔#51/#53/#57, #43↔#80, #12↔#38a', what='Cross-links still only suggestive',
  status='open', cat='E', step='drop #43 ↔ #80 (now a theorem); check #48 ↔ #55 at t = φ, φ², 2 exactly (A, small)', size='small',
  flag='CONTRADICTED in part: #43 Conjecture 2 ↔ #80 is proved (#43 v2 Theorem 4), no longer suggestive')
g(id='W2', list='weak 2', src='fill thread', what='Threads that share no paper: the fill thread is isolated', status='open', cat='E',
  step='same as the fill-thread row (tagging)', size='small')

# ---------------- ledger entries still open (ledger.entries[i])
g(id='Q8', list='ledger 8, 23, 27', src='tetra-sweep census', what='Census rest: n = 4 (2,2,0,0), (3,1,0,0); n = 5 others; n = 8 golden approximants',
  status='RUNNING since 4 Nov (entry 23); results not read', cat='E', step='read the SAT census log and update the ledger', size='small', flag='stale RUNNING entry')
g(id='Q26', list='ledger 26, 37', src='tetra-sweep', what='Conjecture: a truncated tetrahedron minus corners tiles iff its Dehn invariant is zero; the golden real cuts',
  status='OPEN / RUNNING since 4 Nov', cat='D', lemma='Uniform Mirror-Pair Lemma: every Dehn-zero cut vector has a piece + point-inverse tiling, continuous in the cuts',
  tool='SAT periodic test', step='read entry 37\'s scan; a golden piece with no periodic tiling would be a monotile candidate', size='medium', flag='stale RUNNING entry')
g(id='Q34', list='ledger 34, 40', src='Narcissus', what='Two Narcissus glued on the hexagon with a 60° turn: what solid, does it tile; common dissection of Narcissus and the cube',
  status='OPEN; entry 40 RUNNING since 4 Nov', cat='D', tool='library identification + SAT', step='identify the glued solid (Goldberg tables); read common.log', size='small', flag='stale RUNNING entry')
g(id='Q38', list='ledger 38', src='halves', what='Halves (ortho/gyro) as a test on every family', status='RUNNING since 4 Nov', cat='E',
  step='read the census and log the result', size='small', flag='stale RUNNING entry')
g(id='Q52', list='ledger 52, 55', src='#43', what='Conjecture 1 (see the #43 Conjecture 1 row)', status='UNDECIDED', cat='B', lemma='New-Face Lemma (see the #43 Conjecture 1 row)', step='see the #43 Conjecture 1 row', size='large', hop='partly')
g(id='Q59', list='ledger 59', src='Hopscotch coverage', what='Events the coverage map leaves unexplained: CO ∩ μRD Dehn zero at 5/3; Ammann–Beenker wall circuits; yantra viewpoint events',
  status='open', cat='A', tool='splash-determinants (metric factor type); Hopscotch row 1', step='write 5/3 as the root of the Dehn coefficient (a metric linear factor, as the golden cuts); then the Ammann–Beenker walls as circuits',
  size='small', hop='yes: this is the Hopscotch\'s own coverage list')
g(id='Q1P', list='one-piece aim (ledger 49, 50, 56; study 2026-11-05)', src='one-piece aim', what='Route 3 (in-plane key, Socolar–Taylor setting) and route 4 (vertical-plane Ammann system) for a single RD/TRD-cross piece',
  status='OPEN; hat route and ABC waveform SETTLED (closed) 9 Nov', cat='D', tool='SAT tiling tests with skewed tori', step='route 4: straddling piece over two layers, SAT on skewed tori at the smallest period that the Ammann bars allow', size='large',
  hop='partly: outline predicts aperiodic stacking = polar line at irrational slope (to verify)')

# ---------------- plan
TOP = ['L29', 'L28', 'L22', 'R3', 'L25', 'L0', 'L18', 'L20', 'R13', 'L36']
BOULDERS = {
 'B1': ('Walls along the sliders, exactly', 'One study: take each slider whose events are already located in floats, make the slider a symbol, and read the walls as determinant roots (Hopscotch incidence events). Closes #86 (whole stretches), #80/#81 window edges, #61 Swap Rule for s < 1/4.', ['L29', 'L28', 'L22']),
 'B2': ('Weight walks with more kinds', 'One engine run: the flip formula with two weights turns every wall into a line in the weight plane. Closes the three-kind walks of #53 and #56/#57 and the Frank–Kasper walks of #55.', ['L18', 'L21', 'L20']),
 'B3': ('Exact golden 4D stations', 'One set of exact Q(√5) builds of the #76/#91 stations serves #91 Lemma 6 at the stations, #76 part (3), #91\'s factor 2 and tilted slice, and the all-triangle 600-cell slices of #62.', ['R3', 'L25', 'L32', 'L36']),
 'B4': ('Pyramid tilings by SAT', 'One SAT batch on skewed tori: TRD pyramid control, #93\'s ten non-face-to-face combinations, #47\'s smallest face-to-face kit, and the RT pyramids (unread result first).', ['L0', 'L13', 'R8r']),
 'B5': ('Censuses with prior art', 'Desk censuses with the existing scripts plus a library check each: Star and Star Halo of the classical solids, Archimedean stretches, golden split in the other AXE networks.', ['R6', 'R12', 'R11']),
}

def by(i): return next(x for x in G if x['id'] == i)
cnt = collections.Counter(x['cat'] for x in G)
flags = [dict(id='R1', list='ranked 1 (settled)', src='#89, #91', flag='CONTRADICTED and already corrected today (dual-sweeps): #89\'s golden rhombic cuts are not on the second dual sweeps; #91\'s theorem covers regular P only')] + [x for x in G if x['flag']]
Cq = [x for x in G if x['cat'] == 'C']

out = {'date': '2026-11-09', 'kind': 'desk triage, no new mathematics', 'categories': CAT, 'counts': dict(sorted(cnt.items())),
       'skipped_settled': ['ranked 0 (published #92 v2)', 'ranked 1 (SETTLED 9 Nov)', 'ranked 2 (SETTLED 4 Nov)', 'ranked 4 (PROVED 8 Nov)',
                           'ranked 7 (SETTLED 4 Nov)', 'ranked 8 (ANSWERED; RT residual kept as R8r)', 'ranked 10 (PROVED; Obs 3 kept as R10r)',
                           'loose 1 (#38a CLOSED)', 'loose 9 (#42 CLOSED)'],
       'gaps': G, 'top10': TOP, 'boulders': {k: {'name': v[0], 'why': v[1], 'gaps': v[2]} for k, v in BOULDERS.items()},
       'contradicted_or_stale': [{'id': x['id'], 'src': x['src'], 'flag': x['flag']} for x in flags],
       'questions_for_DICTO': [{'id': x['id'], 'src': x['src'], 'question': x['question']} for x in Cq]}
json.dump(out, open(os.path.join(HERE, 'gap-triage.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------- README
L = []
L.append('# Gap triage of the Concordance (study 2026-11-09)\n')
L.append(('**Conclusion.** %d open items triaged (ranked: 8 open rows + 2 residuals of settled rows; loose: 35 open of 37, four of them merged with their ranked twins, 2 closed today and skipped; weak: 3 rows; ledger: 7 groups still OPEN, RUNNING or UNDECIDED). '
         'Counts: ' + ', '.join('%s %d' % (k, cnt[k]) for k in 'ABCDE') + '. The ten best A-gaps fall into five boulders; four items are contradicted or answered by later results (loose 24, loose 26, weak 1, ranked 1 corrected today), and the ledger holds results from 4 Nov never read (entries 19, 23, 37, 38, 40).\n') % len(G))
L.append('**Status: DONE** (desk triage; no computation). DICTO\'s review of 9 Nov 2026 found the gaps not pushed to conclusion; this table is the plan to push them.\n')
L.append('Sources: concordance.json (gaps.ranked, gaps.loose, gaps.weak, ledger entries 0–59 via ledger-digest.txt), the studies of 4–9 Nov named per row, papers/polar-line-outline, #80 and #45 abstracts. Data: gap-triage.json (built by build_triage.py).\n')
L.append('Categories: ' + '; '.join('**%s** %s' % (k, v) for k, v in CAT.items()) + '.\n')
L.append('## Ranked plan: top 10 A-gaps by value/cost\n')
for n, i in enumerate(TOP, 1):
    x = by(i); L.append('%d. **%s %s** (%s, %s) — %s. First step: %s.' % (n, x['id'], x['src'], x['boulder'] or 'single', x['size'], x['what'], x['step']))
L.append('\n## Boulders\n')
for k, (nm, why, ids) in BOULDERS.items():
    L.append('- **%s %s**: %s Gaps: %s.' % (k, nm, why, ', '.join(ids)))
L.append('\n## Questions for DICTO (category C)\n')
for x in Cq: L.append('- **%s (%s)**: %s' % (x['id'], x['src'], x['question']))
L.append('\n## Contradicted or stale premises\n')
for x in flags: L.append('- **%s (%s)**: %s' % (x['id'], x['src'], x['flag']))
L.append('\n## Every gap\n')
L.append('| id | list | source | gap | status | cat | tool / lemma / question; first step | size | Hopscotch |')
L.append('|---|---|---|---|---|---|---|---|---|')
for x in G:
    det = x['question'] if x['cat'] == 'C' else '; '.join(s for s in [('lemma: ' + x['lemma']) if x['lemma'] else '', ('tool: ' + x['tool']) if x['tool'] else '', ('first step: ' + x['step']) if x['step'] else ''] if s)
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (x['id'], x['list'], x['src'], x['what'], x['status'], x['cat'], det.replace('|', '/'), x['size'], x['hop']))
L.append('\nSkipped as settled: ' + '; '.join(out['skipped_settled']) + '.\n')
L.append('LEADS: (1) mark loose 24 CLOSED (#102) and drop the #43 ↔ #80 weak link in the next Concordance version; (2) read the five stale RUNNING/UNDECIDED logs before any new test; (3) boulder B1 is the cheapest first study.\n')
open(os.path.join(HERE, 'README.md'), 'w').write('\n'.join(L))

# ---------------- paper.html (house style of papers/three-results)
e = html.escape
H = []
H.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Gap Triage</title><link rel="stylesheet" href="../paper.css">')
H.append('<style>table{break-inside:auto;page-break-inside:auto;border-collapse:collapse;width:100%;font-size:7.6pt;margin:2mm 0} td,th{border:0.3pt solid #999;padding:0.7mm 1mm;vertical-align:top;text-align:left} th{background:#eee} tr{break-inside:avoid} .c{font-weight:bold;text-align:center} ol li,ul li{margin-bottom:1mm}</style></head><body>')
H.append('<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">')
H.append('<h1>Gap Triage<br><span style="font-size:0.72em;font-weight:normal">every open gap of the Concordance, sorted for action, 9 November 2026</span></h1>')
H.append('<div class="meta"><b>DICTO</b> · dictospheres.com · 9 November 2026</div>')
H.append('<div class="status">For DICTO, not for publication: a desk triage (no new mathematics) of every open gap in the DICTO Concordance (ranked, loose, weak and the ledger entries still open), study 2026-11-09-gap-triage. DICTO\'s review of 9 November found that the gaps had not been pushed to conclusion; this is the plan to push them. Drafted with Claude (Anthropic).</div>')
H.append('<h2>1. The count</h2>')
H.append('<p>%d open items. <b>A</b> closable now with existing tools: %d. <b>B</b> reduced to one named lemma: %d. <b>C</b> needs a new idea from DICTO: %d. <b>D</b> belongs to the one-piece aim: %d. <b>E</b> housekeeping: %d. Skipped as already settled: 9 rows (ranked 0, 1, 2, 4, 7, 8, 10; loose 1 and 9), with the two leftovers of ranked 8 and 10 kept as their own items.</p>' % (len(G), cnt['A'], cnt['B'], cnt['C'], cnt['D'], cnt['E']))
H.append('<h2>2. The plan: ten gaps, five boulders</h2>')
H.append('<p>Ranked by value over cost. A boulder is one study that closes several gaps at once.</p><ol>')
for i in TOP:
    x = by(i); H.append('<li><b>%s</b> (%s, %s): %s. <i>First step:</i> %s.</li>' % (e(x['src']), e(BOULDERS[x['boulder']][0]) if x['boulder'] else 'on its own', e(x['size']), e(x['what']), e(x['step'])))
H.append('</ol><table><tr><th>Boulder</th><th>One study that</th><th>Gaps</th></tr>')
for k, (nm, why, ids) in BOULDERS.items():
    H.append('<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % (e(nm), e(why), e(', '.join(by(i)['src'] for i in ids))))
H.append('</table>')
H.append('<h2>3. Questions for DICTO</h2><ul>')
for x in Cq: H.append('<li><b>%s</b>: %s</li>' % (e(x['src']), e(x['question'])))
H.append('</ul>')
H.append('<h2>4. Premises already overtaken</h2><ul>')
for x in flags: H.append('<li><b>%s</b> (%s): %s</li>' % (e(x['src']), e(x['list']), e(x['flag'])))
H.append('</ul>')
H.append('<h2>5. Every gap</h2><table><tr><th>Source</th><th>Gap</th><th>Now</th><th>Cat</th><th>Tool, lemma or question; first step</th><th>Size</th></tr>')
for x in G:
    det = x['question'] if x['cat'] == 'C' else ' '.join(s for s in [('<b>Lemma:</b> ' + e(x['lemma'])) if x['lemma'] else '', ('<b>Tool:</b> ' + e(x['tool'])) if x['tool'] else '', ('<b>Step:</b> ' + e(x['step'])) if x['step'] else ''] if s)
    if x['cat'] == 'C': det = e(det)
    H.append('<tr><td>%s</td><td>%s</td><td>%s</td><td class="c">%s</td><td>%s</td><td>%s</td></tr>' % (e(x['src']), e(x['what']), e(x['status']), x['cat'], det, e(x['size'])))
H.append('</table></body></html>')
os.makedirs(PAPER, exist_ok=True)
open(os.path.join(PAPER, 'paper.html'), 'w').write('\n'.join(H))
print('items', len(G), dict(cnt), 'flags', len(flags), 'C', len(Cq))
