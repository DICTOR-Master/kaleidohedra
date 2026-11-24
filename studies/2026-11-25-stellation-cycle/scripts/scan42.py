"""Task 1, screen (double precision; every claim it suggests is proved exactly or rigorously elsewhere).
The 42 Aequi of data/aequi.json `coincidences`: for each die, at its catalogue depths,
  - its corners, faces and edges;
  - which edges lie in a mirror of the icosahedron group (placement A: mirror normals = the 15 two-fold axes C6 + RT24);
  - which corners lie on a rotation axis (C6, O8, I12, D12, RT24);
  - for every union S of orbits (S proper, non-empty): is the boundary of S (edges between an S face and a non-S face) all in
    mirrors with its corners on axes?  Then the central projection of S's faces is a union of the 120 mirror triangles, and the
    number k_S of triangles is printed with the target |S| * 120 / N; also which orbits' planes carry the boundary.
-> data/scan42.json"""
import json, os, sys, itertools, gzip
import numpy as np
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-exact-dice', 'scripts'))
from groups import DIRS, DFAM
F = np.array(DFAM)
AX = DIRS[np.isin(F, ['C6', 'O8', 'D12', 'I12', 'RT24'])]; MI = DIRS[np.isin(F, ['C6', 'RT24'])]
co = json.load(open(os.path.join(HERE, '..', 'data', 'aequi.json')))['coincidences']

def load(c):
    if c['src'] == '4553':
        import glob
        for f in glob.glob(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', '%04d-*.json' % int(c['id']))):
            d = json.load(open(f))
            if str(d['sid']) == str(c['id']):
                return dict(idx=d['face_directions'], sizes=d['orbit_sizes'], orbits=d['orbits'], depths=[float(x) for x in d['depths_60_digits']], N=int(d['N']))
    b = c['src'].split()[1]
    for d in json.load(open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', 'dice%s-new.json' % b))):
        if str(d['sid']) == str(c['id']):
            lab = d['label'].split(': ', 1)[1]
            ev = lambda x: eval(x) if isinstance(x, str) else x
            return dict(idx=ev(d['idx']), sizes=ev(d['sizes']), orbits=[o.strip() for o in lab.split(' + ')], depths=[float(x) for x in ev(d['depths'])], N=int(d['N']))
    raise KeyError(c)

def geom(idx, sizes, depths):
    U = DIRS[idx]; Dd = np.repeat(depths, sizes); orb = np.repeat(np.arange(len(sizes)), sizes)
    hs = HalfspaceIntersection(np.hstack([U, -Dd[:, None]]), np.zeros(3)); V = []
    for v in hs.intersections:
        if not any(np.abs(v - w).max() < 1e-8 for w in V): V.append(v)
    V = np.array(V); inc = [set(np.where(np.abs(U @ v - Dd) < 1e-8)[0].tolist()) for v in V]
    E = []
    for i, j in itertools.combinations(range(len(V)), 2):
        s = inc[i] & inc[j]
        if len(s) >= 2:
            # an edge iff the segment is an edge of the polytope: the two corners share exactly the two planes of one edge
            fs = sorted(s)
            for a, b in itertools.combinations(fs, 2):
                # segment lies on planes a, b; it is an edge if no other corner lies strictly between on both planes
                between = [k for k in range(len(V)) if k not in (i, j) and a in inc[k] and b in inc[k]
                           and 0 < (V[k] - V[i]) @ (V[j] - V[i]) < (V[j] - V[i]) @ (V[j] - V[i])]
                if not between and np.linalg.norm(np.cross(U[a], U[b])) > 1e-9: E.append((i, j, a, b))
    return U, orb, V, inc, E

def on_axis(v): n = v / np.linalg.norm(v); return np.abs(AX - n).max(1).min() < 1e-8
def in_mirror(v, w):
    n, m = v / np.linalg.norm(v), w / np.linalg.norm(w); return (np.abs(MI @ n) + np.abs(MI @ m)).min() < 1e-8
def face_area(U, V, inc, i):
    S = [v for v in range(len(V)) if i in inc[v]]; c = V[S].mean(0); e1 = V[S[0]] - c; e2 = np.cross(U[i], e1)
    S = sorted(S, key=lambda v: np.arctan2((V[v] - c) @ e2, (V[v] - c) @ e1)); tot = 0
    for k in range(1, len(S) - 1):
        a, b, cc = V[S[0]], V[S[k]], V[S[k + 1]]; la, lb, lc = map(np.linalg.norm, (a, b, cc))
        tot += 2 * np.arctan2(abs(np.linalg.det([a, b, cc])), la * lb * lc + (a @ b) * lc + (a @ cc) * lb + (b @ cc) * la)
    return tot

out = []
for c in co:
    d = load(c); U, orb, V, inc, E = geom(d['idx'], d['sizes'], d['depths']); m = len(d['sizes']); N = d['N']
    area = np.array([face_area(U, V, inc, i) for i in range(N)])
    assert abs(area - 4 * np.pi / N).max() < 1e-9, (c, abs(area - 4 * np.pi / N).max())
    emir = [in_mirror(V[i], V[j]) for i, j, a, b in E]
    rec = dict(src=c['src'], id=c['id'], label=c['label'], pair=c['best'][1:3], N=N, orbits=d['orbits'], sizes=d['sizes'],
               corners=len(V), edges=len(E), edges_in_mirrors=int(sum(emir)), corners_on_axes=int(sum(on_axis(v) for v in V)),
               corners_4plus=int(sum(len(s) >= 4 for s in inc)), shadow_unions=[])
    for r in range(1, m):
        for S in itertools.combinations(range(m), r):
            bd = [(e, ok) for e, ok in zip(E, emir) if (orb[e[2]] in S) != (orb[e[3]] in S)]
            if not bd: continue
            okm = all(ok for e, ok in bd); okc = all(on_axis(V[e[0]]) and on_axis(V[e[1]]) for e, ok in bd)
            if okm and okc:
                k = sum(area[i] for i in range(N) if orb[i] in S) / (4 * np.pi / 120)
                rec['shadow_unions'].append(dict(S=[d['orbits'][s] for s in S], k=round(float(k), 6), target=sum(d['sizes'][s] for s in S) * 120 / N,
                                                 boundary_orbits=sorted({d['orbits'][orb[e[2]]] for e, _ in bd} | {d['orbits'][orb[e[3]]] for e, _ in bd})))
    out.append(rec)
    print(rec['src'], rec['id'], rec['label'], 'pair', rec['pair'], 'V', rec['corners'], 'E', rec['edges'], 'mirrorE', rec['edges_in_mirrors'],
          'axisV', rec['corners_on_axes'], '4+', rec['corners_4plus'])
    for s in rec['shadow_unions']: print('    S', s)
json.dump(out, open(os.path.join(HERE, '..', 'data', 'scan42.json'), 'w'), indent=1)
print('FINAL ok' if len(out) == len(co) == 42 else 'FINAL FAIL')
