# DICTO · partial Vacuus 1b: exact render scenes of the twelve special depths (26 Nov 2026). With Claude (Anthropic).
# Per depth: the excavated body (see-through) and its core, the solid bounded by ALL the pit-wall planes (scipy halfspace
# intersection about O); at a special depth this core is the scaled core solid Q (checked: its face count = Q's).
# 26 Nov (DICTO: "the second fig is no good"): fig-1 style. Only the eleven exact special sizes (exact_check.py; octahedron /
# triakis tetrahedron is a correction, not special), in D·I·C·T·O order of P; camera from the circumradius so every cell has the
# same framing as fig 1; core in its app colour where it is a Platonic solid, else a neutral stone; core edges drawn as tubes.
# Usage: python special_scenes.py <out.html>
import sys, os, json
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); OUTH = sys.argv[1]; sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
EX = [e for e in json.load(open(os.path.join(HERE, '../data-exact-forms.json'))) if e.get('special')]
ORD = ['dodecahedron', 'icosahedron', 'rhombic triacontahedron', 'triakis icosahedron', 'cube', 'tetrahedron', 'octahedron']
QF = ['icosahedron', 'dodecahedron']   # within each P, the classic (its polar as core) first
EX.sort(key=lambda e: (ORD.index(e['P']) if e['P'] in ORD else 99, e['Q'] not in QF, e['s']))
COL = {'icosahedron': '#3a70cd', 'dodecahedron': '#8a5cc4', 'cube': '#488e48', 'octahedron': '#e8c852', 'tetrahedron': '#cd3e28'}
POLY = {p['name']: p for p in json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json')))}
scenes, caps, insets = [], [], []
def cedges(C):
    # edges of the core's true faces: a hull edge whose two triangles lie on different planes
    eq = [tuple(np.round(q, 6)) for q in C.equations]; own = {}
    for k, sm in enumerate(C.simplices):
        for a, b in ((sm[0], sm[1]), (sm[1], sm[2]), (sm[2], sm[0])): own.setdefault(tuple(sorted((int(a), int(b)))), []).append(eq[k])
    return [[a, b, '#2b261e', None] for (a, b), qs in own.items() if len(set(qs)) > 1]
for e in EX:
    V, F, N, D = S[e['P']]; s = e['s']; A = s * D[:, None] * N
    verts, T, tubes, H = [], [], [], []
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            k = len(verts); verts += [V[a].tolist(), V[b].tolist(), A[fi].tolist()]; T.append([k, k + 1, k + 2])
            tubes += [[k, k + 1, '#2b261e', None], [k + 1, k + 2, '#5a5248', None], [k + 2, k, '#5a5248', None]]
            n = np.cross(V[b] - V[a], A[fi] - V[a]); n /= np.linalg.norm(n); d = n @ V[a]
            if d < 0: n, d = -n, -d
            H.append(list(n) + [-d])
    hs = HalfspaceIntersection(np.array(H), np.zeros(3)); Cw = ConvexHull(hs.intersections)
    nf = len({tuple(np.round(eq, 6)) for eq in Cw.equations}); nq = len(POLY[e['Q']]['faces'])
    # the core drawn is lam*Q itself (one rotation M, one lam: every wall on a face plane of lam*Q, as exact_check.py proves)
    VQ, FQ, NQ, DQ = S[e['Q']]; Hn = np.array(H); core_v = None
    for M in FRAME:
        NM = NQ @ M.T; lams = []
        for h in Hn:
            j = np.argmax(NM @ h[:3])
            if NM[j] @ h[:3] < 1 - 1e-7: break
            lams.append(-h[3] / DQ[j])
        if len(lams) == len(Hn) and np.ptp(lams) < 1e-6: core_v = lams[0] * VQ @ M.T; break
    assert core_v is not None, 'no lam*Q found'
    C = ConvexHull(core_v)
    R = np.linalg.norm(V, axis=1).max()
    body = {'v': np.round(np.array(verts), 6).tolist(), 't': T, 'c': ['#e9e4da'] * len(T), 'a': 0.35, 'tubes': tubes, 'rad': 0.006 * R, 'balls': []}
    core = {'v': np.round(C.points, 6).tolist(), 't': [[int(x) for x in sm] for sm in C.simplices], 'c': [COL.get(e['Q'], '#6f675c')] * len(C.simplices), 'a': 0.95, 'tubes': cedges(C), 'rad': 0.004 * R, 'balls': []}
    scenes.append({'E': float(1.62 * R), 'dir': [0.55, 0.35, 1.0], 'parts': [body, core]})
    rc = np.linalg.norm(core_v, axis=1).max()   # inset: the core alone, same view, enlarged (scenes 11..21)
    insets.append({'E': float(1.62 * rc), 'dir': [0.55, 0.35, 1.0], 'parts': [dict(core, a=1.0, rad=0.012 * rc)]})
    caps.append(dict(P=e['P'], Q=e['Q'], s=e['closed'], core_faces=nf, Q_faces=nq))
    print(e['P'], 'on', e['Q'], 's =', e['closed'], 'walls bound', nf, 'faces; Q has', nq, '(whole core)' if nf == nq else '(planes only)', flush=True)
R3.write(OUTH, scenes + insets); json.dump(caps, open(OUTH.replace('.html', '.json'), 'w'), indent=1)
print('FINAL ok' if len(caps) == 11 and sum(c['core_faces'] == c['Q_faces'] for c in caps) == 8 else 'FINAL FAIL (expected 11 sizes, 8 whole cores)')
