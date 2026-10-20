# DICTO 2026-10-20: pictures of the OG core of 80 spires (float copies of the exact corners of step1-ocd-exact.json), in the #18 standard:
# dark ground, hexagonal spires gold, kite spires purple. Scenes: the OG; the spires drawn out from the centre; one half cut open to show
# the apexes meeting; one hexagonal and one kite spire. Writes renders/og-spires.html; shots jewel-shots.mjs; compose og_spires_compose.py.
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(sys.argv[1]))
qf = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
V = np.array([[qf(x) for x in p] for p in D['V']])
GOLD, PURPLE = '#d9a334', '#a77be0'
def cyc(f):
    P = V[f]; c = P.mean(0); n = np.cross(P[1] - c, P[0] - c); u = P[0] - c; w = np.cross(n, u)
    return [i for _, i in sorted(zip([math.atan2((V[i] - c) @ w, (V[i] - c) @ u) for i in f], f))]
F = [cyc(f) for f in D['faces']]
def spire(f, push=0.0):
    P = V[f]; c = P.mean(0); d = c / np.linalg.norm(c) * push
    pts = np.vstack([P + d, d]); n = len(f); tris = [[0, k, k + 1] for k in range(1, n - 1)] + [[k, (k + 1) % n, n] for k in range(n)]
    edges = [[k, (k + 1) % n] for k in range(n)] + [[k, n] for k in range(n)]
    col = GOLD if n == 6 else PURPLE
    return {'v': np.round(pts, 5).tolist(), 't': tris, 'c': [col] * len(tris), 'e': edges, 'a': 1.0}
scenes = []
add = lambda t, s, parts: scenes.append({'title': t, 'sub': s, 'parts': parts})
add('The DICTO OG', '20 regular hexagons and 60 kites', [spire(f) for f in F])
add('80 spires, drawn out', 'every apex at the centre', [spire(f, 0.18) for f in F])
half = [f for f in F if V[f].mean(0) @ np.array([0.3, 0.5, 0.8]) < 0]
add('Half, opened', 'the spires meet in the middle', [spire(f) for f in half])
h = next(f for f in F if len(f) == 6); k = next(f for f in F if len(f) == 4)
add('Hexagonal spire', '20 of them, one shape', [spire(h)]); add('Kite spire', '60 of them, one shape', [spire(k)])
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'og-spires.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'og-spires-labels.json'), 'w'), indent=1)
print('og-spires.html', len(scenes))
