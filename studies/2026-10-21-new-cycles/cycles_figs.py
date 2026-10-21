# DICTO 2026-10-21: pictures of the three new cycles (float copies of the exact boundaries in cleo-turned.json, og-up-polar.json,
# ott-turned.json), #18 standard: faces coloured by kind (triangles gold, four-sided purple, pentagons lilac, hexagons bronze,
# decagons pale; heptagons, which only the polar OTT has, grey-blue). Scenes: the boundary solids (each drawn to the same size),
# each shell's towers drawn apart (coloured by the kind of the inner face they stand on, the inner solid faint inside), and for A and
# C the polar boundary solids. Adapted from new_solids_figs.py / golden_figs.py (og-turned-out).
# usage: python3 cycles_figs.py <five-fold-octet dir> A|B|C
import sys, os, json, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
FIVE, WHICH = sys.argv[1], sys.argv[2]; HERE = os.path.dirname(os.path.abspath(__file__))
COL = {3: '#d9a441', 4: '#6b3fa0', 5: '#9a78c8', 6: '#8a5a24', 7: '#5f7f96', 10: '#f0d48a'}
SIDES = {3: 'triangles', 4: 'four-sided', 5: 'pentagons', 6: 'hexagons', 7: 'heptagons', 10: 'decagons'}
hull = lambda Q: m3.Manifold.hull_points(np.asarray(Q, float))
def faces(P):
    H = ConvexHull(P); G = {}
    for s, e in zip(H.simplices, H.equations): G.setdefault(tuple(np.round(e / np.linalg.norm(e[:3]), 7)), set()).update(s)
    out = []
    for ids in G.values():
        ids = list(ids); c = P[ids].mean(0); n = c / np.linalg.norm(c); u = P[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        ids.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append(ids)
    return out
def poly_part(P, F, a=1.0, edges=True):
    v, t, c = [], [], []
    for f in F:
        o = len(v); v += P[f].tolist(); t += [[int(o), int(o + k), int(o + k + 1)] for k in range(1, len(f) - 1)]; c += [COL.get(len(f), '#cccccc')] * (len(f) - 2)
    E = sorted({tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in F for k in range(len(f))}); o = len(v); v += P.tolist()
    return {'v': np.round(v, 5).tolist(), 't': t, 'c': c, 'e': [[int(o + a_), int(o + b_)] for a_, b_ in E] if edges else None, 'a': a}
def clean(P): P = np.asarray(P, float); return P[sorted(set(ConvexHull(P).vertices))]
def kinds_sub(P, F):
    from collections import Counter
    k = Counter(len(f) for f in F); return f'{len(P)} corners, {len(F)} faces: ' + ', '.join(f'{c} {SIDES.get(s, f"{s}-gons")}' for s, c in sorted(k.items()))
def solid_scene(title, P):
    P = clean(P); P = P / np.linalg.norm(P, axis=1).max(); F = faces(P); return {'title': title, 'sub': kinds_sub(P, F), 'parts': [poly_part(P, F)]}
def shell_scene(title, inner, outer):
    inner, outer = clean(inner), clean(outer); s = np.linalg.norm(outer, axis=1).max(); inner, outer = inner / s, outer / s
    O = hull(outer); R = 3.0; parts = []; n = 0
    for f in faces(inner):
        Fp = inner[f]; cone = hull(np.vstack([Fp * 1e-4, Fp / np.linalg.norm(Fp, axis=1)[:, None] * R]))
        tw = (cone ^ O) - hull(np.vstack([np.zeros(3), Fp]))
        if tw.is_empty() or tw.volume() < 1e-9: continue
        d = Fp.mean(0); d /= np.linalg.norm(d); me = tw.translate(list(d * 0.12)).to_mesh(); n += 1
        parts.append({'v': np.round(np.asarray(me.vert_properties[:, :3]), 5).tolist(), 't': np.asarray(me.tri_verts).tolist(), 'c': [COL.get(len(f), '#ccc')] * len(me.tri_verts), 'e': None, 'a': 1.0})
    parts.append(poly_part(inner, faces(inner), a=0.35, edges=False))
    return {'title': title, 'sub': f'{n} towers drawn apart, on the faces of the inner solid', 'parts': parts}
scenes, layout = [], []
if WHICH == 'A':
    R = json.load(open(os.path.join(HERE, 'cleo-turned.json'))); B = R['boundaries_float']; PB = R['polar']['boundaries_float']
    nm = {0: 'S0 = ID (CLEO sphere)', 1: 'S1 (FPD type)', 2: 'S2 (GTI type)', 4: 'S4 = (phi^8/10) ID', 7: 'S7 (RT type)'}
    for k in (0, 1, 2, 4, 7): scenes.append(solid_scene(nm[k], B[f'S{k}']))
    for a, b in ((0, 1), (1, 2), (2, 4), (4, 7)): scenes.append(shell_scene(f'Shell S{a} to S{b} ({b - a} beat{"s" if b - a > 1 else ""})', B[f'S{a}'], B[f'S{b}']))
    for k in (0, 1, 2, 4, 7): scenes.append(solid_scene(f'polar S{k} = phi^-{k} T^{k}(RT)', PB[f'polar S{k}']))
    layout = [[0, 1, 2, 3, 4], [5, 6, 7, 8, None], [9, 10, 11, 12, 13]]
    title, sub, out = 'CLEO turned out, golden step', 'S_k = phi^k P^k(ID): ID, FPD, GTI, RT, ID again (x phi^8/10) -- the UP cycle backwards; shells 1, 1, 2, 3 beats; bottom: the polars (UP on the RT, shrinking)', 'cleo-turned-out.jpg'
elif WHICH == 'B':
    R = json.load(open(os.path.join(HERE, 'og-up-polar.json'))); B = R['boundaries_float']; names = list(B)
    up = ['OG', 'KRE', 'PHE', 'TPP', 'DPHP']
    for k, n_ in enumerate(names): scenes.append(solid_scene(f'{n_.replace(" (Hecatodihedron)", " Hecatodihedron")} = polar {up[k]}', B[n_]))
    for s in R['shells']: scenes.append(shell_scene(f"Shell {s['inner']} to {s['outer']}".replace(' (Hecatodihedron)', ''), B[s['inner']], B[s['outer']]))
    layout = [[0, 1, 2, 3, 4], [5, 6, 7, 8, None]]
    title, sub, out = 'Polar of the OG upward family', 'P^k(Hecatodihedron) = polar(T^k OG); nested except P^4 H not inside P^3 H (TPP not inside DPHP); last shell P^4 H to P^2 H', 'og-up-polar.jpg'
else:
    R = json.load(open(os.path.join(HERE, 'ott-turned.json'))); B = R['boundaries_float']; PB = R['polar']['boundaries_float']
    nm = {0: 'S0 = DICTO OTT', 1: 'S1 = c phi ID', 2: 'S2 (FPD type)', 4: 'S4 (RT type)', 7: 'S7 (GTI type)'}
    for k in (0, 1, 2, 4, 7): scenes.append(solid_scene(nm[k], B[f'S{k}']))
    for a, b in ((0, 1), (1, 2), (2, 4), (4, 7)): scenes.append(shell_scene(f'Shell S{a} to S{b} ({b - a} beat{"s" if b - a > 1 else ""})', B[f'S{a}'], B[f'S{b}']))
    for k in (0, 1, 2, 4, 7): scenes.append(solid_scene(f'polar S{k}' + (' = polar OTT' if k == 0 else ''), PB[f'polar S{k}']))
    layout = [[0, 1, 2, 3, 4], [5, 6, 7, 8, None], [9, 10, 11, 12, 13]]
    title, sub, out = 'DICTO OTT turned out, golden step', 'S_k = phi^k P^k(OTT): icosahedral from beat 1 (P(OTT) = ID x (sqrt5 - 1)/3), then the CLEO cycle one beat behind; bottom: the polars', 'ott-turned-out.jpg'
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(FIVE, 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', f'cycles-{WHICH}.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump({'title': title, 'sub': sub, 'out': out, 'layout': layout, 'labels': [{'title': s['title'], 'sub': s['sub']} for s in scenes]}, open(os.path.join(HERE, 'renders', f'cycles-{WHICH}-labels.json'), 'w'), indent=1)
print(f'cycles-{WHICH}.html', len(scenes))
