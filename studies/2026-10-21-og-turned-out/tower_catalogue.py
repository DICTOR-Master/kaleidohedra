# DICTO 2026-10-21 ("the beat shells look new configurations too" -> catalogue figure in #43): one picture of every tower shape of
# the OG turned out (shells 1-4) and of the polar Hecatodihedron sequence (shells 1-3). Towers = cone from the centre over each face
# of the inner solid, cut by the outer solid (as in the exact shell checks); faces grouped into shapes by tower volume (one shape per
# group, as the exact logs show). Coloured by role (DICTO: 'would colouring help'): base on the inner solid bronze, top on the outer
# solid pale gold, side walls (through the centre) purple; polar towers lilac sides. Float copies of the exact boundaries. Each tower turned so its base faces down, the same view for all.
import os, json, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); phi = (1 + 5 ** .5) / 2
G = json.load(open(os.path.join(HERE, 'golden-exact.json')))['boundaries_float']; S4 = json.load(open(os.path.join(HERE, 'shell4-exact.json')))['boundaries_float']
PL = json.load(open(os.path.join(HERE, 'polar-turned.json')))['boundaries_float']
A = lambda x: np.array(x, float)
GOLD = [('Shell 1', A(G['OG']), A(G['phi TPH'])), ('Shell 2', A(G['phi TPH']), A(G['phi^2 TQH'])), ('Shell 3', A(G['phi^2 TQH']), A(G['phi^4 TQHD'])),
        ('Shell 4', A(S4['beat 4']), A(S4['beat 7']))]
POL = [('Polar shell 1', A(PL['polar S1']), A(PL['polar S0'])), ('Polar shell 2', A(PL['polar S2']), A(PL['polar S1'])), ('Polar shell 3', A(PL['polar S4']), A(PL['polar S2']))]
hull = lambda Q: m3.Manifold.hull_points(np.asarray(Q, float))
WORD = {3: 'triangle', 4: 'four-sided face', 5: 'pentagon', 6: 'hexagon', 10: 'decagon'}
def faces(P):
    H = ConvexHull(P); Gf = {}
    for s, e in zip(H.simplices, H.equations): Gf.setdefault(tuple(np.round(e, 7)), set()).update(s)
    return [list(v) for v in Gf.values()]
def catalogue(shells, col):
    out = []
    for name, inner, outer in shells:
        Hout = ConvexHull(outer).equations; O = hull(outer); R = np.linalg.norm(outer, axis=1).max() * 3; seen = {}
        for f in faces(inner):
            F = inner[f]; cone = hull(np.vstack([F * 1e-4, F / np.linalg.norm(F, axis=1)[:, None] * R]))
            nf = np.cross(F[1] - F[0], F[2] - F[0]); nf /= np.linalg.norm(nf); nf = nf if nf @ F[0] > 0 else -nf
            t = (cone ^ O).trim_by_plane(list(nf), float(nf @ F[0])); key = (len(f), round(t.volume() / O.volume(), 7))
            if key not in seen: seen[key] = (t, F)
        for (n, _), (t, F) in sorted(seen.items(), key=lambda kv: (kv[0][0], kv[0][1])):
            me = t.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); nrm = F.mean(0) / np.linalg.norm(F.mean(0))
            T = np.asarray(me.tri_verts); X = P[T].mean(1); dB = abs(X @ nrm - F.mean(0) @ nrm); tol = 2e-4 * np.linalg.norm(outer, axis=1).max()
            onT = np.min(np.abs(X @ Hout[:, :3].T + Hout[:, 3]), axis=1) < tol
            cols = ['#8a5a24' if b < tol else '#f0d48a' if o else col for b, o in zip(dB, onT)]
            z = np.array([0, 0, 1.]); v = np.cross(nrm, z); s, c = np.linalg.norm(v), nrm @ z
            Rm = np.eye(3) if s < 1e-9 else np.eye(3) + (K := np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])) + K @ K * ((1 - c) / s ** 2)
            P = (P - P.mean(0)) @ Rm.T
            same = sum(1 for k in seen if k[0] == n)
            out.append({'title': f'{name} · on a {WORD.get(n, f"{n}-gon")}', 'sub': f'{n}-sided base' + (' (one of two shapes)' if same > 1 else ''),
                        'parts': [{'v': np.round(P, 5).tolist(), 't': np.asarray(me.tri_verts).astype(int).tolist(), 'c': cols, 'e': None, 'a': 1.0}]})
    return out
scenes = catalogue(GOLD, '#6b3fa0') + catalogue(POL, '#9a78c8')
for s in scenes:
    pts = np.array(s['parts'][0]['v']); s['E'] = round(float(np.linalg.norm(pts, axis=1).max()) * 1.08, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.55, 0.35, 0.75); const _unused = new THREE.Vector3(')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'towers-cat.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
for s in scenes:
    if s['title'] == 'Polar shell 3 · on a pentagon' and np.ptp(np.array(s['parts'][0]['v']), axis=0).min() < 0.02: s['sub'] = 'almost flat: exact volume 0.0000077'
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'towers-cat-labels.json'), 'w'), indent=1)
print('towers-cat.html', len(scenes), [s['title'] for s in scenes])
