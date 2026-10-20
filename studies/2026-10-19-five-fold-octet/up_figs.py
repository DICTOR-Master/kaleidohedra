# DICTO 2026-10-20: new figures for #38 Universal PiTet (V3), in the style of #39. Builds the exact solids and pieces of
# exact_inner.py and exact_cycle.py (same icosahedron frame), and writes renders/up.html (three.js, one scene per frame,
# window.show(i)) and renders/up-labels.json. Shots: shots.mjs; compose: up_compose.py.
#   cycle   the five stations ID, RT, GTI, FPD, ID x 10/phi^4, true relative size
#   shells  the four cycle shells: inner solid (pale) with its shell pieces on the faces round one five-fold axis
#   inner   stage 1 (Cleo star), stage 2 (Monkey Staff B on D'), stage 3 (ID -> RT fine cut), ID -> OG, OG -> RT (hexagonal Cleos),
#           the 12 five-sided Vajras on the icosahedron
#   pieces  one of each kind of piece, each to its own scale
#   mirror  the GTI inside the FPD with the mirror sphere (the GTI's circumsphere) between them
import json, os, textwrap
import numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'exact_inner.py')).read(); head, main = src.split("if __name__ == '__main__':")
exec(head)
body = textwrap.dedent(main.split("    json.dump(log")[0])
body = body.replace("check(", "_nocheck(").replace("log['og']['max_distance_to_study_OG_data'] = float(dev)", "")
def _nocheck(*a, **k): pass
exec(body)
GTI = step(RT)[0]; FPD = step(GTI)[0]; ID2 = step(FPD)[0]

def fl(P): return np.array([[x.f() for x in c] for c in P])
def solid_of(S):
    C, F = polytope(solid(S)); return {'v': fl(C), 'f': [list(o) for o, _ in F]}
def piece_of(p):
    return {'v': fl(p['C']), 'f': [list(o) for o, _ in p['F']], 'minus': None if p['minus'] is None else fl(p['minus']['C'])}
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))

COL = {3: ['#e0ae2c', '#f3d77a'], 4: ['#3f9a5b', '#a5d9ae'], 5: ['#2f6fb0', '#79a6db'], 6: ['#c4553a', '#f0a68f'], 10: ['#7a4fa0', '#c2a3dc']}
def shape_key(V, o): return (len(o), tuple(sorted(round(float(np.linalg.norm(V[o[(i + 1) % len(o)]] - V[o[i]])), 5) for i in range(len(o)))))
def faces_mesh(sd, alpha=1.0, solid_col=None):
    from collections import Counter
    V = sd['v']; cnt = Counter(shape_key(V, o) for o in sd['f']); shade = {}
    for key, _ in sorted(cnt.items(), key=lambda kv: (kv[0][0], -kv[1], kv[0][1])):
        n = sum(1 for k in shade if k[0] == key[0]); shade[key] = COL.get(key[0], ['#999999'])[min(n, 1)]
    tris, cols, edges = [], [], []
    for o in sd['f']:
        c = solid_col or shade[shape_key(V, o)]
        for a, b in zip(o[1:-1], o[2:]): tris.append([o[0], a, b]); cols.append(c)
        edges += [[o[i], o[(i + 1) % len(o)]] for i in range(len(o))]
    return {'v': np.round(V, 6).tolist(), 't': tris, 'c': cols, 'e': edges, 'a': alpha}
def mf_mesh(mf, col, alpha=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 6).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': alpha}
def piece_mesh(pc, col):
    if pc['minus'] is None: return faces_mesh({'v': pc['v'], 'f': pc['f']}, 1.0, col)
    return mf_mesh(hull(pc['v']) - hull(pc['minus']), col)
def apart(pc, k=0.16):                         # move a piece outward along its own direction (pulled-apart view)
    c = pc['v'].mean(0); dv = k * c / np.linalg.norm(c); return dict(pc, v=pc['v'] + dv, minus=None if pc['minus'] is None else pc['minus'] + dv)
def sphere(r, col='#6f9fc4', alpha=0.24): return {'sphere': r, 'col': col, 'a': alpha}

AX = np.array([0.0, 1.0, (1 + 5 ** .5) / 2]); AX /= np.linalg.norm(AX)
def _rx(a): return np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
def _ry(a): return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
CAM = _ry(0.22) @ _rx(0.30) @ AX; CAM /= np.linalg.norm(CAM)               # the camera direction of the page (as in the JS)
def tilt(c):                                   # rotation taking the piece's radial direction c to "up, leaning 30 deg toward the camera"
    up = np.array([0, 1.0, 0]); up = up - (up @ CAM) * CAM; up /= np.linalg.norm(up); t = np.cos(np.radians(60)) * CAM + np.sin(np.radians(60)) * up
    a = c / np.linalg.norm(c); v = np.cross(a, t); s_, c_ = np.linalg.norm(v), a @ t
    if s_ < 1e-12: return np.eye(3)
    k = v / s_; Kx = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]); R1 = np.eye(3) + s_ * Kx + (1 - c_) * Kx @ Kx
    Kt = np.array([[0, -t[2], t[1]], [t[2], 0, -t[0]], [-t[1], t[0], 0]]); a2 = 0.45                    # then a quarter-ish turn about t
    return (np.eye(3) + np.sin(a2) * Kt + (1 - np.cos(a2)) * Kt @ Kt) @ R1
near = lambda P, deg: (lambda c: c @ AX / np.linalg.norm(c) >= np.cos(np.radians(deg)))(np.asarray(P).mean(0))
scenes = []
def add(title, parts, E=None, group=None, sub=''): scenes.append({'title': title, 'sub': sub, 'parts': parts, 'E': E, 'group': group})

# 1. the cycle
cyc = [('ID', 'icosidodecahedron', ID), ('RT', 'rhombic triacontahedron', RT), ('DICTO GTI', 'Golden Truncated Icosahedron', GTI),
       ('DICTO FPD', 'Flat Pentakis Dodecahedron', FPD), ('ID × 10/φ⁴', 'the icosidodecahedron again', ID2)]
SOL = {k: solid_of(S) for k, _, S in cyc}
for k, sub, _ in cyc: add(k, [faces_mesh(SOL[k])], group='cycle', sub=sub)
# 2. the cycle shells
PAL = ['#2f6fb0', '#c4553a', '#3f9a5b', '#7a4fa0', '#e0ae2c']
for (a, _, Sa), (b, _, Sb) in zip(cyc, cyc[1:]):
    Vi = SOL[a]['v']; Hout = hull(SOL[b]['v']); Hin = hull(Vi); parts = [faces_mesh(SOL[a], 1.0, '#d8d2c4')]; kinds = {}
    for o in SOL[a]['f']:
        if not near(Vi[o], 40): continue
        pc = (hull(np.vstack([np.zeros(3), 3 * Vi[o]])) ^ Hout) - Hin; key = (len(o), round(pc.volume(), 6))
        kinds.setdefault(key, PAL[len(kinds) % len(PAL)]); parts.append(mf_mesh(pc, kinds[key]))
    add(f'{a} → {b}', parts, group='shells', sub=f'{len(SOL[a]["f"])} pieces')
# 3. the inner stages
K = {'cleo': '#e0ae2c', 'spike': '#e07b39', 'ipyr': '#2f6fb0', 'valley': '#3f9a5b', 'frustum': '#7a4fa0', 'pyr5': '#2f6fb0', 'pyr3': '#c4553a',
     'vtet': '#3f9a5b', 'low': '#2f6fb0', 'hexc': '#e9c13a', 'cap': '#2a9d9a', 'tet': '#3f9a5b', 'vajra': '#7a4fa0', 'core': '#d9a521'}
pl = lambda L, deg: [piece_of(p) for p in L if near(fl(p['C']), deg)]
Ipc = solid_of(I)
add('Stage 1: the Cleo star', [faces_mesh(Ipc, 1.0, K['cleo'])] + [piece_mesh(piece_of(p), K['spike']) for p in spikes] + [faces_mesh(solid_of(Dp['C']), 0.16, '#bfc7cc')],
    group='inner', sub="the icosahedron's 20 Cleo-Icos with 20 spikes, inside D′ (glass)")
add('Stage 2: Monkey Staff B', [faces_mesh(solid_of(Dp['C']), 1.0, '#d8d2c4')] + [piece_mesh(p, K['frustum'] if near(p['v'], 20) else '#b58fd6') for p in pl(fr, 70)], group='inner', sub="12 twisted frusta, D′ → ID")
fine5 = [p for p in fine if len(p['C']) == 6]; fine3 = [p for p in fine if len(p['C']) == 4 and any(c in A3 for c in p['C']) and sum(c in A5 for c in p['C']) == 0]
fineV = [p for p in fine if p not in fine5 and p not in fine3]
SIDE = np.cross(AX, CAM); SIDE /= np.linalg.norm(SIDE)
half = lambda L: [p for p in L if p['v'].mean(0) @ SIDE > 0.05]
add('Stage 3: ID → RT', [faces_mesh(SOL['ID'], 1.0, '#d8d2c4')] + [piece_mesh(p, K['pyr5']) for p in pl(fine5, 40)] + [piece_mesh(p, K['pyr3']) for p in pl(fine3, 50)] +
    [piece_mesh(p, K['vtet']) for p in half(pl(fineV, 55))], group='inner', sub='12 five-sided and 20 three-sided pyramids; 60 valley tetrahedra (one side shown)')
kpyr = []                                   # the 60 kite pyramids of OG -> RT (#38 §5), apex at the RT five-fold corner over each OG kite
for o, i in OGh['F']:
    if len(o) != 4: continue
    n, d = OGh['H'][i]; kpyr.append(piece([OGh['C'][j] for j in o] + [max(A5, key=lambda v: dot(n, v).f())]))
assert len(kpyr) == 60 and all(p['V'] == Q5(Fr(1, 76), Fr(1, 684)) for p in kpyr), 'kite pyramid volume'
print('60 kite pyramids, each 1/76 + sqrt5/684 (exact)')
OGs = {'v': fl(OGh['C']), 'f': [list(o) for o, _ in OGh['F']]}
add('ID → OG', [faces_mesh(SOL['ID'], 1.0, '#d8d2c4')] + [piece_mesh(p, K['low']) for p in pl(low, 70)], group='inner', sub='12 pieces, one on each pentagon')
add('OG → RT: hexagonal Cleos', [faces_mesh(OGs, 1.0, '#d8d2c4')] + [piece_mesh(p, K['hexc']) for p in pl(hexc, 50)] + [piece_mesh(p, K['cap']) for p in pl(kpyr, 42)] +
    [piece_mesh(p, K['tet']) for p in half(pl(tets, 50))], group='inner', sub='20 hexagonal Cleos, 60 kite pyramids; 120 tetrahedra (one side shown)')
VJ = []
for a5 in A5:
    tI = max(I, key=lambda v: dot(v, a5).f() / np.linalg.norm([x.f() for x in v])); ip_ = next(p for p in pyr if tI in p['C'])
    f_ = max(fr, key=lambda p: sum(dot(c, a5).f() for c in p['C'])); o_ = next(p for p in fine if a5 in p['C'] and len(p['C']) == 6)
    VJ.append({'v': fl(hullH(ip_['C'] + f_['C'] + o_['C'])['C']), 'f': [list(o) for o, _ in hullH(ip_['C'] + f_['C'] + o_['C'])['F']], 'minus': None})
add('Five-sided Vajras', [mf_mesh(hull(fl(I)), K['core'])] + [piece_mesh(p, K['vajra'] if near(p['v'], 20) else '#b58fd6') for p in VJ if near(p['v'], 70)], group='inner', sub='6 of the 12, on the icosahedral core')
# 4. the pieces, one of each kind
one = [('Cleo-Ico', cleo[0], K['cleo']), ('spike', spikes[0], K['spike']), ('inward pyramid', pyr[0], K['ipyr']), ('valley tetrahedron', val[0], K['valley']),
       ('Monkey Staff B', fr[0], K['frustum']), ('five-sided pyramid', fine5[0], K['pyr5']), ('three-sided pyramid', fine3[0], K['pyr3']), ('valley tetrahedron (ID → RT)', fineV[0], K['vtet']),
       ('five-sided Vajra', None, K['vajra']), ('ID → OG piece', low[0], K['low']), ('hexagonal Cleo', hexc[0], K['hexc']), ('kite pyramid', kpyr[0], K['cap']), ('tetrahedron (OG → RT)', tets[0], K['tet'])]
for nm, p, col in one:
    pc = VJ[0] if p is None else piece_of(p); c = pc['v'].mean(0); M = tilt(-c if nm == 'inward pyramid' else c)   # the inward pyramid points in
    pc = dict(pc, v=(pc['v'] - c) @ M.T, minus=None if pc['minus'] is None else (pc['minus'] - c) @ M.T)
    add(nm, [piece_mesh(pc, col)], E=round(float(np.linalg.norm(pc['v'], axis=1).max()) * 1.12, 4), group='pieces')
# 5. the mirror: GTI inside the FPD, with the GTI's circumsphere (radius^2 = 10/phi^2 = 15 - 5 sqrt5)
r2 = 15 - 5 * 5 ** .5
add('The mirror', [faces_mesh(SOL['DICTO GTI']), sphere(r2 ** .5), faces_mesh(SOL['DICTO FPD'], 0.16, '#bfc7cc')], group='mirror', sub='the GTI inside the FPD; the sphere through the GTI’s corners swaps them')
R = max(float(np.linalg.norm(SOL[k]['v'], axis=1).max()) for k in SOL)
for s in scenes:
    if s['E'] is None: s['E'] = round((R if s['group'] in ('cycle',) else max(float(np.linalg.norm(np.array(p['v']), axis=1).max()) for p in s['parts'] if 'v' in p)) * 1.06, 4)
html = open(os.path.join(HERE, 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xffffff, 0xa89f8c, 0.46)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xffffff, 0.9)')
html = html.replace("if (d.dots) {", "if (d.sphere) { const m = new THREE.Mesh(new THREE.SphereGeometry(d.sphere, 64, 48), new THREE.MeshStandardMaterial({ color: d.col, transparent: true, opacity: d.a, depthWrite: false, roughness: 0.3 })); grp.add(m); continue; }\n    if (d.dots) {")
open(os.path.join(HERE, 'renders', 'up.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub'], 'group': s['group']} for s in scenes], open(os.path.join(HERE, 'renders', 'up-labels.json'), 'w'), indent=1, ensure_ascii=False)
print('up.html', len(scenes), 'scenes')
