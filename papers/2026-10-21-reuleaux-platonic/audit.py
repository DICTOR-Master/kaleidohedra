# DICTO 2026-10-21: number audit of "The Reuleaux Platonic Solids" (#45) against the study logs, the library text and arithmetic.
#   python3 audit.py <kres>      (the repository root)
import sys, os, re, math
K = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'paper.src.html')).read(); txt = re.sub(r'<[^>]+>', ' ', src); txt = re.sub(r'\s+', ' ', txt)
rd = lambda p: open(os.path.join(K, p)).read()
inn = lambda s: s in txt
bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
ST = 'studies/2026-10-21-reuleaux-platonic/'
L, W = rd(ST + 'reuleaux-checks.log'), rd(ST + 'widths.log')
chk(len(re.findall(r'^PASS', L, re.M)) == 45 and 'FAIL' not in L and L.strip().endswith('ALL PASS') and inn('45 PASS, no FAIL'), 'reuleaux-checks.log: 45 PASS, quoted')
# widths
mx = {m.group(1): m.group(3) for m in re.finditer(r'balls on the (\w+)\): width ([\d.]+) \.\. ([\d.]+)', W)}
mn = {m.group(1): m.group(2) for m in re.finditer(r'balls on the (\w+)\): width ([\d.]+) \.\. ([\d.]+)', W)}
chk(all(v == '1.000000000000' for v in mn.values()) and len(mn) == 5, 'widths.log: minimum 1 for all five')
row = lambda nm: re.search(r'<tr><td>' + nm + r'</td>(.*?)</tr>', src).group(1)
LOOK = {'tetrahedron': 'Reuleaux tetrahedron', 'cube': 'Reuleaux octahedron', 'octahedron': 'Reuleaux cube', 'dodecahedron': 'Reuleaux icosahedron', 'icosahedron': 'Reuleaux dodecahedron'}
VOL = {m.group(1): float(m.group(2)) for m in re.finditer(r'Reuleaux (\w+)\s+volume at diameter 1: ([\d.]+)', L)}
DIA = {'tetrahedron': (6, 6), 'cube': (4, 14), 'octahedron': (3, 10), 'dodecahedron': (10, 38), 'icosahedron': (6, 22)}
COL = {'tetrahedron': 4, 'cube': 2, 'octahedron': 3, 'dodecahedron': 3, 'icosahedron': 4}
for solid, body in LOOK.items():
    r = re.sub(r'<[^>]+>', '|', row(body)); cells = [c for c in r.split('|') if c.strip()]
    m = re.search(rf'{body}: (\d+) faces, fewest colours with no two neighbours alike: (\d+)', L); a = re.search(rf'{body}: two faces meet along an arc exactly when .*?\((\d+) arcs\)', L)
    chk(cells[0] == solid and cells[1] == m.group(1) and cells[2] == a.group(1) and int(cells[4]) == COL[solid] == int(m.group(2)), f'{body}: on the {solid}, {m.group(1)} faces, {a.group(1)} arcs, {m.group(2)} colours')
    p, b = DIA[solid]; chk(cells[3] == f'{p} ({b})' and (f'{p} diametric pairs' in L), f'{body}: {p} diametric pairs ({b})')
    chk(cells[5] == f'1 .. {float(mx[solid]):.6f}', f'{body}: width 1 .. {float(mx[solid]):.6f}')
    v = VOL[body.split()[1]]; chk(cells[6] == f'{v:.5f}', f'{body}: volume {v:.5f}')
chk(all(f'fewer than 2m - 2 = {b}' in L for s, (p, b) in DIA.items() if s != 'tetrahedron') and '6 diametric pairs = 2m - 2' in L, 'diametric pair bounds in log')
chk(L.count("each corner lies on exactly 1 of the other balls' spheres") == 4, 'corners not vertices (4 solids)')
# exact width forms
chk('cube and octahedron share (r/R)^2 = 1/3' in L and 'dodecahedron and icosahedron share (r/R)^2 = (5 + 2 sqrt5)/15' in L and inn('(r/R)² = 1/3') and inn('(5 + 2√5)/15 for the dodecahedron'), 'r/R shared')
chk('A = sqrt30/3, B = sqrt3/3, so w = (sqrt30 - sqrt3)/3' in L and inn('(√30 − √3)/3 ≈ 1.248392') and f'{(30 ** .5 - 3 ** .5) / 3:.6f}' == '1.248392', 'cube/oct closed form')
chk('A^2 = (50 + 2 sqrt5)/15, B^2 = (5 + 2 sqrt5)/15' in L and inn('(√(50 + 2√5) − √(5 + 2√5))/√15 ≈ 1.110989') and f'{((50 + 2 * 5 ** .5) ** .5 - (5 + 2 * 5 ** .5) ** .5) / 15 ** .5:.6f}' == '1.110989', 'icosahedral closed form')
chk(inn('r² = (5 + 2√5)/60') and abs((5 + 2 * 5 ** .5) / 15 / 4 - (5 + 2 * 5 ** .5) / 60) < 1e-15 and inn('r² = 1/12'), 'r^2 values')
chk(inn('1.248391589161') and inn('1.110988655456') and inn('1.024944026382') and mx['cube'] == mx['octahedron'] == '1.248391589161' and mx['dodecahedron'] == mx['icosahedron'] == '1.110988655456' and mx['tetrahedron'] == '1.024944026382', 'numerical maxima quoted')
chk('sqrt3 - sqrt2/2 = 1.024944026382 = the largest width' in L and inn('√3 − √2/2'), 'tetrahedron sqrt3 - sqrt2/2')
chk('face-axis width 1.248391589161 = the largest width' in L and 'face-axis width 1.110988655456 = the largest width' in L, 'face-axis = max (numerical)')
chk(inn('is therefore numerical') and inn('not proved'), 'global maximum flagged numerical')
chk("along a face axis every corner has height >= -r, with equality exactly at the" in L, 'corner heights >= -r (exact)')
chk(inn('3000 random directions') and 'U = rng.normal(size=(3000, 3))' in rd(ST + 'widths.py'), '3000 directions')
# volume vs literature
harb = 8 * math.pi / 3 + 2 ** .5 / 4 - 27 / 4 * math.acos(1 / 3)
m = re.search(r'Reuleaux tetrahedron volume ([\d.]+) = .*?to ([\d.e+-]+)', L)
chk(m and abs(float(m.group(1)) - harb) < 1e-7 and inn('0.4221577') and inn('1.1 × 10 −8') and m.group(2) == '1.1e-08', f'tetrahedron volume {m.group(1)} vs Harbourne {harb:.7f}')
H = open(os.path.expanduser('~/Documents/kaleidohedra-references/papers/Hynd-2023-Perimeter-volume-Reuleaux-polyhedron.pdf'), 'rb').read()
chk(len(H) > 0 and inn('8π/3 + √2/4 − (27/4) arccos(1/3)'), 'Harbourne formula stated (Hynd, library)')
vols = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in re.finditer(r'Reuleaux (\w+)\s+volume at diameter 1: ([\d.]+) \(N = 2000; N = 1000 gives ([\d.]+)\)', L)}
chk(max(abs(a - b) for a, b in vols.values()) < 6e-7 and inn('agree to within 6 × 10 −7'), 'quadrature N=1000/2000 agree within 6e-7')
chk(inn('7200 points') and '7200' in rd(ST + 'reuleaux_checks.py') and inn('margin 10 −9'), 'arc sampling')
# figure labels (drawn by reuleaux_platonic.py at edge 1): radius = diameter
P = rd(ST + 'reuleaux_platonic.py'); chk("radius {D:.3f}" in P and 'V /= E' in P and inn("their radius, which is the solid's diameter"), 'figure labels: radius = diameter at edge 1')
chk(inn('4, 2, 3, 3, 4') and inn('4, 2, 3, 3 and 4'), 'colours 4/2/3/3/4')
# library text facts
LT = {}
import subprocess, unicodedata
for f in ['Hynd-2023-Perimeter-volume-Reuleaux-polyhedron.pdf', 'Montejano-Roldan-Pensado-2017-Meissner-polyhedra.pdf', 'Bezdek-Langi-Naszodi-Papez-2007-Ball-polyhedra.pdf']:
    LT[f] = unicodedata.normalize('NFC', subprocess.run(['pdftotext', '-q', os.path.expanduser('~/Documents/kaleidohedra-references/papers/' + f), '-'], capture_output=True, text=True).stdout)
chk('By a theorem of Pál' in LT['Montejano-Roldan-Pensado-2017-Meissner-polyhedra.pdf'] and inn("Pál's theorem, as cited in [2]"), "Pal's theorem in Montejano-Roldan-Pensado")
chk('2m − 2 diametric pairs' in LT['Hynd-2023-Perimeter-volume-Reuleaux-polyhedron.pdf'] and 'Grünbaum [5],' in LT['Hynd-2023-Perimeter-volume-Reuleaux-polyhedron.pdf'], 'Vazsonyi bound in Hynd')
for f, t in LT.items():
    hits = [w for w in ['octahedr', 'icosahedr', 'dodecahedr', 'Platonic'] if w.lower() in t.lower()]
    chk(hits == [], f'{f[:20]}: no octahedron/icosahedron/dodecahedron/Platonic in its text')
# words, credits, library
chk('proposal' not in txt.lower() and 'proposed' not in txt.lower(), 'no "proposal"/"proposed"')
chk(inn("are DICTO's idea") and inn('drafting with Claude (Anthropic)'), 'credit line')
rows = open(os.path.join(HERE, 'lib-rows.html')).read().count('<tr>')
chk(rows == 81 and inn('81 library sources with a text layer') and inn('267 entries, of which 94 have a local file') and inn('173 link-only'), f'library rows {rows}, counts')
chk(inn('Version 1 · 21 October 2026') and inn('Licence CC BY-SA 4.0'), 'version, date, licence')
print('ALL PASS' if bad == 0 else f'{bad} FAIL')
