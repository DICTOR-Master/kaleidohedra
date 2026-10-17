# DICTO 2026-10-18 octet study -- STEP 10: the pieces as solid meshes (manifold3d booleans; run on dicto-node, ~/plotenv).
# keyed OCD = OCD + 8 keys; M = hull(two stars) - both OCDs - their keys; cap (+z corner) = corner region of the octahedron - OCD -
# the Ms there; tetrahedron T+ = T+ - its 4 keys (step 5) and - its 6 Ms (step 8). Volumes from the meshes cross-check steps 2/5/8.
# usage: python3 step10_piece_meshes.py IN.json OUT.json  (IN = float geometry written by the export block below when run locally)
import sys, json, itertools, numpy as np
if sys.argv[1] == 'export':                                   # local: write float inputs from the exact study data
    from q5 import *
    S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
    f = lambda v: [qf(q(x)) for x in v]
    json.dump(dict(V=[f(v) for v in S1['V']], faces=S1['faces'], R=qf(q(S1['R'])), Tp=[f(v) for v in S2['Tplus']], L=[f(v) for v in S2['lattice']],
                   keys={k: [f(p) for p in K] for k, K in S5['keys'].items()}), open(sys.argv[2], 'w')); sys.exit()
import manifold3d as m3
D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; Tp = np.array(D['Tp']); L = np.array(D['L'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
OCD = hull(V); keys = [hull(K) for K in D['keys'].values()]
union = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
keyed = union([OCD] + keys)
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
shifts = [np.array(ijk) @ L for ijk in itertools.product(range(-2, 3), repeat=3)]
def M_of(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in D['faces'] if i in f for j in f})]
    return hull(np.vstack([star, o - star])) - keyed - keyed.translate(o), o
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
M1, o1 = M_of(i1)
# all Ms of the build near the origin cell (each corner of each nearby OCD; duplicates are harmless for subtraction)
allM = []
for s in shifts:
    if np.linalg.norm(s) > 2.3: continue
    for i in five:
        Mi, _ = M_of(i) if s is shifts[0] and False else (None, None)
Mbase = {i: M_of(i)[0] for i in five}
for s in shifts:
    if np.linalg.norm(s) > 2.3: continue
    allM += [Mbase[i].translate(s) for i in five]
Mall = union(allM)
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[a*R/3, b*R/3, R/3] for a in (1, -1) for b in (1, -1)])
cap = corner - OCD - Mall
allkeys = union([keyed.translate(s) for s in shifts if np.linalg.norm(s) < 2.3]) 
T = hull(Tp); Tdent = T - allkeys; Tnotch = Tdent - Mall
pieces = dict(keyed_OCD=keyed, middle=M1, cap=cap, tet_dented=Tdent, tet_notched=Tnotch, tet_left=Tnotch, cap_unnotched=corner - OCD)
out = {}
for k, mf in pieces.items():
    mesh = mf.to_mesh(); out[k] = dict(volume=mf.volume(), genus=mf.genus(), parts=len(mf.decompose()), v=np.round(mesh.vert_properties[:, :3], 6).tolist(), t=mesh.tri_verts.tolist())
    print(k, 'volume %.6f' % mf.volume(), 'parts', len(mf.decompose()), 'genus', mf.genus(), 'tris', len(mesh.tri_verts), flush=True)
out['cap_parts'] = sorted([p.volume() for p in cap.decompose()], reverse=True); print('cap parts', out['cap_parts'])
del out['tet_left']; out['centres'] = dict(middle_m=(o1 / 2).tolist(), tet=Tp.mean(0).tolist())
json.dump(out, open(sys.argv[2], 'w'))
