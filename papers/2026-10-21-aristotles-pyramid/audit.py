# DICTO 2026-10-21: number audit of "Aristotle's Pyramid" (#44) against the study logs, the cited sources and arithmetic.
#   python3 audit.py <kres>      (the repository root: studies/ and papers/ are read)
import sys, os, re, math
from fractions import Fraction as F
K = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'paper.src.html')).read(); txt = re.sub(r'<[^>]+>', ' ', src); txt = re.sub(r'\s+', ' ', txt)
rd = lambda p: open(os.path.join(K, p)).read()
inn = lambda s: s in txt
bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
ST = 'studies/2026-10-21-aristotle-pyramids/'
L, A = rd(ST + 'pyramid-checks.log'), rd(ST + 'angle-relations.log')
# 1. the exact log
chk(L.count('\nPASS') + L.startswith('PASS') == 46 and 'FAIL' not in L and L.strip().endswith('ALL PASS') and inn('46 PASS, no FAIL'), 'pyramid-checks.log: 46 PASS, no FAIL, quoted')
chk(A.count('integer relation: None') == 4 and inn('PSLQ'), 'angle-relations.log: no integer relation (4 searches)')
# 2. Table 1 angles against the logs and arithmetic
a, tD, tI = math.acos(1 / 3), math.acos(-1 / 5 ** .5), math.acos(-5 ** .5 / 3)
for nm, b, s in [('cube', 45.0, 120), ('tetrahedron', math.degrees(a) / 2, 120), ('octahedron', 90 - math.degrees(a) / 2, 90), ('dodecahedron', math.degrees(tD) / 2, 120), ('icosahedron', math.degrees(tI) / 2, 72)]:
    chk(f'{nm} pyramid: ' in L and f'beta = theta/2 = {b:.4f} deg' in L and f'angle 360/' in L and (f'{b:.2f}°' in txt or b == 45.0), f'{nm}: base {b:.2f}, side {s}')
    chk(f'= {s:g} deg exactly' in L.split(f'{nm} pyramid: ')[2] if L.count(f'{nm} pyramid: ') >= 2 else False, f'{nm}: side edge {s} in log')
for t in ['α/2 ≈ 35.26°', '(π − α)/2 ≈ 54.74°', 'θ D /2 ≈ 58.28°', 'θ I /2 ≈ 69.09°', '45° = π/4', '90° (4 faces)', '72° (5 faces)']: chk(inn(t), f'Table 1: "{t}"')
chk(f'{360 - 5 * math.degrees(a):.2f}' == '7.36' and inn('7.36°'), 'five tetrahedra round an edge leave 7.36 deg')
chk(f'{math.degrees(a):.2f}' == '70.53' and inn('≈ 70.53°'), 'alpha = 70.53 deg')
# 3. Lemma 2 facts
for t in ['cos² α = 1/9', 'cos² θ D = 1/5', 'cos² θ I = 5/9', 'tan α = 2√2', 'tan θ D = −2', 'tan θ I = −2/√5', '4/9, 4/5 and 20/9']: chk(inn(t), f'Lemma 2: "{t}"')
for t in ['cos^2 = 1/9, tan^2 = 8', 'cos^2 = 1/5, tan^2 = 4', 'cos^2 = 5/9, tan^2 = 4/5', '(2 cos)^2 = 4/9', '(2 cos)^2 = 4/5', '(2 cos)^2 = 20/9', 'square-free part 2', 'square-free part 1', 'square-free part 5']: chk(t in L, f'log: {t}')
chk(abs(math.tan(a) - 2 * 2 ** .5) < 1e-12 and abs(math.tan(tD) + 2) < 1e-12 and abs(math.tan(tI) + 2 / 5 ** .5) < 1e-12, 'tangents (float)')
# 4. Theorem 1 / counting over 31 sets
chk("sets not excluded by h (of 31): [('cube',), ('tetrahedron', 'octahedron'), ('cube', 'tetrahedron', 'octahedron')]" in L and inn('all 31 non-empty sets') and 2 ** 5 - 1 == 31, '31 sets, 3 pass')
chk(inn('only {cube}, {tetrahedron, octahedron} and {cube, tetrahedron, octahedron} pass'), 'the three sets named')
chk('dodecahedron and icosahedron pyramids (Cleo-Icos) are still excluded' in L, 'all five: D and I excluded')
# 5. the octet
chk('octahedron 4/3 + 2 tetrahedra 1/3 = rhombohedron 2' in L and inn('the octahedron is 4/3, each tetrahedron 1/3 and the cell 2') and F(4, 3) + 2 * F(1, 3) == 2, 'octet cell volumes')
chk('8 octahedron pyramids and 8 tetrahedron pyramids per cell' in L and inn('8 octahedron pyramids and 8 tetrahedron pyramids'), '8 + 8 pyramids')
chk('4 x alpha/2 + 4 x (pi - alpha)/2 = 2 pi' in L and inn('4 × α/2 + 4 × (π − α)/2 = 2π'), 'edge sum 2 pi')
chk(inn('(1, 1, 0), (1, 0, 1), (0, 1, 1)'), 'lattice vectors')
chk('3 x (+1/2) + 3 x (-1/2) = 0' in L and inn('3 × a × ½') and inn('3 × b × (−½)'), 'Proposition 2 weights')
chk('octet patch (112 octahedron and 32 tetrahedron pyramids): every face pyramid lies in a slab' in L and inn('112 octahedron and 32 tetrahedron pyramids') and inn('k ≤ z ≤ k + 1'), 'slabs: {C, T, O} fills')
chk(inn('Main theorem.') and src.index('<h2>1. The theorem') < src.index('<h2>2. Proof') < src.index('<h2>3. Corollaries') < src.index('<h2>4. Conjectures') < src.index('<h2>7. Conclusion') < src.index('<h2>8. Prior art') < src.index('Appendix'), 'theorem-first order')
chk(inn('{C}, {T, O} or {C, T, O}') and inn('Proved in general') and inn('Proved for the cases built') and inn('Observed numerically'), 'statement and status classes')
# 6. Cleo-Icos and Antonius (#20 and the log)
f20 = rd('studies/2026-10-14-fuji-family/paper/paper.md')
chk('arccos(1/sqrt5) = 63.43 deg' in L and inn('arccos(1/√5) ≈ 63.43°') and 'arccos(1/√5) = 63.43°' in f20, '63.43 deg')
chk('Antonius 4 x that, rhombohedron 6 x that' in L and inn('exactly 4 times the Cleo-Icos\'s volume (the rhombohedron is 6 times)') and 'exactly **four times the Cleo-Icos\'s volume**' in f20, 'volumes 4x, 6x')
chk('pi - theta_I/2 = 110.91 deg' in L and inn('π − θ I /2 ≈ 110.91°') and '110.91°' in f20 and f'{180 - math.degrees(tI) / 2:.2f}' == '110.91', 'Antonius 110.91 deg')
chk('72 and 108 deg' in L and inn('72° and 108°'), 'side edges 72/108')
chk('Antonius = -2 x Cleo-Icos' in L and inn('3 × ½ and Antonius 6 × (−½), −2 times') and "exactly −2 times the Cleo-Icos's" in f20, 'Dehn ratio -2')
chk('2,187 pieces' in f20 and inn('2,187-piece patch'), '2,187-piece patch (#20)')
chk('Antonius: 6 corners, 8 faces, 12 edges' in L and inn('trigonal antiprism'), 'Antonius antiprism')
chk('for the rhombohedron of 60° it gives the regular tetrahedra and octahedron' in f20, '#20: the 60-degree rhombohedron remark')
# 7. Table 2 against the sources
SS = rd('papers/2026-10-20-dicto-sunstar/paper.src.html')
chk('the dodecahedra take (5 + √5)/8 of it' in SS and inn('(5 + √5)/8 ≈ 90.45%') and f'{(5 + 5 ** .5) / 8 * 100:.2f}' == '90.45', 'Sunstar: (5 + sqrt5)/8 = 90.45%')
chk('alternate cubes of a cubic lattice' in SS and inn('alternate cubes of a cubic lattice') and 'stellation 8' in SS, 'Sunstar lattice, Hart stellation 8')
D = open('/home/dicto/kaleidohedra/DISCOVERIES.md').read() if os.path.exists('/home/dicto/kaleidohedra/DISCOVERIES.md') else rd('DISCOVERIES.md')
f21 = D[D.index('## F21.'):D.index('## F21.') + 4000]
chk('(175 − 75√5)/12 = 60.79%' in f21 and inn('(175 − 75√5)/12 ≈ 60.79%') and f'{(175 - 75 * 5 ** .5) / 12 * 100:.2f}' == '60.79', 'F21: 60.79%')
chk('one of edge **1/2** + 4 corner' in f21 and 'is the regular octahedron' in f21 and inn('icosahedra of edge 1/2 with corner and edge caps'), 'F21: edge 1/2, caps, regular octahedron')
chk('10.5281/zenodo.23284390' in f21 and 'v2026.10.11-octet' in f21 and inn('DICTO DOI: 10.5281/zenodo.23284390') and inn('v2026.10.11-octet'), 'F21 DOI and release')
chk('"the same principle as the dodecahedron and roofs, but with six"' in D and inn('"the same principle as the dodecahedron and roofs, but with six"'), 'F21 quote')
chk('Pacioli; Fuller\'s Jitterbug' in D and inn('(Pacioli; Fuller\'s Jitterbug)'), 'Pacioli / Jitterbug credit')
chk(inn('exact (released finding F21; not a separate paper)'), 'F21 status wording')
# 8. history (Lagarias-Zong text in the library)
chk(inn('306b') and inn('Guthrie') and inn('1540–1549') and inn('Maurolico (1529)'), 'Aristotle quotation and source details')
# 9. DOIs (as in the Collected Works and the Sunstar record)
C = rd('papers/collected/collected.html')
for n, d in [('#19', '23351291'), ('#20', '23357896')]: chk(re.search(n + r'\b.*?' + d, re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', C))) is not None and inn(f'{n}, DICTO DOI: 10.5281/zenodo.{d}'), f'{n} DOI {d}')
chk('"conceptrecid": "23497702"' in rd('papers/2026-10-20-dicto-sunstar/zenodo-state.json') and inn('#42, DICTO DOI: 10.5281/zenodo.23497702'), '#42 DOI 23497702')
# 10. words, library
chk('proposal' not in txt.lower() and 'proposed' not in txt.lower(), 'no "proposal"/"proposed"')
chk(inn("The question, whether Aristotle could have meant the Cleo-Icos, is DICTO's") and inn('drafting with Claude (Anthropic)'), 'credit line')
rows = open(os.path.join(HERE, 'lib-rows.html')).read().count('<tr>')
chk(rows == 81 and inn('81 library sources with a text layer') and inn('267 entries, of which 94 have a local file') and inn('13 page images') and inn('173 link-only'), f'library rows {rows}, counts')
chk(267 - 94 == 173, 'link-only = 267 - 94')
for t in ['On angles whose squared trigonometric functions are rational', 'Ball-polyhedra', 'Meissner polyhedra', 'The perimeter and volume of a Reuleaux polyhedron']: chk(t in open(os.path.join(HERE, 'lib-rows.html')).read(), f'library row: {t}')
chk(inn('Version 1 · 21 October 2026') and inn('Licence CC BY-SA 4.0'), 'version, date, licence')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
