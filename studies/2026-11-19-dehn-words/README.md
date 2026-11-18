# Dehn words: which pieces can be "said in cubes" (19 November 2026)

**Question (DICTO, shape language, "the perfect math of adding shapes together"; "Yes please run away"):** in the language whose words are pieces, whose grammar is face-to-face joining and whose meaning is what adds exactly (volume, solid angle, canonical form), the Dehn invariant splits the words: zero = scissors-congruent to a cube of the same volume (Dehn 1901, Sydler 1965); nonzero = an irreducible meaning of its own. Every space-filler has Dehn invariant zero (Debrunner 1980), so a nonzero word cannot fill space alone.

**Prior work (ledger read first):** studies/2026-11-04-dehn-screen (float tool `dehn.py`, OG family, HexOct, Admiral, Delian, TRD pyramids; paper "The Dehn Test Picks the Lone Tilers"). Only pieces not screened there are tested here.

**Method:** `scripts/dehn_mp.py`, the same algorithm at 80 digits from exact corners: AXE, CLEO, FUJI identified in Q(√5) from the 9-digit data of 2026-10-14-axe-cleo-fuji (each corner checked to 2e-9, then exact); the twelve fair dice of #111 from their 100-digit corner dumps. PSLQ among the distinct dihedrals and π (tol 1e-50, coefficients ≤ 2000). Zero claimed at |sum| < 1e-45, nonzero at > 1e-6; none fell between. Status: high-precision numerical (PSLQ relations are not certified symbolically).

**Calibration (11/11):** zero for cube, RD, TO, RT, both golden rhombohedra, RD centre pyramid (the float tool's logged fault, 5 Nov, is fixed here); nonzero for tetrahedron, octahedron, icosahedron, dodecahedron.

## Results (`data/dehn-words.log`, `data/dehn-words-cal-words-co.json`)

| word | Dehn | note |
|---|---|---|
| AXE | nonzero | 2 independent dihedrals mod π |
| CLEO | nonzero | |
| FUJI | nonzero | |
| fair dice tc 10, co 14 (Lucky 7), tr 16, td 16, cd 18, or 20, od 20, rdd 24, di 32, dt 42, it 50 | nonzero | none fills space alone |
| fair die cr 18 (cube ∩ RD) | **zero** | all its dihedrals (90°, 120°, 135°) are rational in π, so every cube ∩ RD solid is Dehn-zero, not only the fair one |
| GET A, GET B, Inchbald's solid | zero (by additivity) | each = RT − 4 golden oblate rhombohedra, all three Dehn-zero above; consistent with their proved tilings |

**Leads:** (1) does the fair 18-face cube ∩ RD die fill space? Dehn zero is necessary only; not tested. (2) AXE, CLEO, FUJI each nonzero; which sums of them cancel (sentences that are "said in cubes")? Their joins in the icosahedron's gaps are the natural first sentences.
