# DICTO 2026-10-20: data for the side-by-side 3D page of the DBT kit and the 8-cut kit (float meshes from the exact solids).
# Kits: DBT on the gyrated octet (+ grown bipyramid); 8-cut on the gyrated octet (+ grown bipyramid); 8-cut on the octet
# (+ grown tetrahedra, the step-27 cubes minus the solids). For each: the solid, its fill pieces, and a cluster = the solid at the
# origin with every fill piece that touches it (and the neighbouring solids' count). -> renders/kits-data.json
import json, itertools, math, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
R = fq(json.load(open(H + '../2026-10-18-ocd-octet/data/step1-ocd-exact.json'))['R'])
SOL = {k: np.array([[fq(c) for c in v] for v in json.load(open(H + f))['V']]) for k, f in (('dbt', 'dbt-exact.json'), ('cut8', 'cut8-exact.json'))}
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
sph = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
MIR = np.eye(3) - 2 / 3 * np.ones((3, 3)); mir = lambda k: (MIR, 2 * k * R / 3 * np.ones(3)); comp = lambda a, b: (a[0] @ b[0], a[0] @ b[1] + a[1])
def maps(stack):
    LM = {0: (np.eye(3), np.zeros(3))}
    for k in range(1, 4):
        for s in (1, -1): j = s * k; LM[j] = comp(mir(2 * j - s), LM[j - s]) if stack == 'gyrated' else (np.eye(3), np.array([1, 1, 0]) * R * j)
    return LM
cent0 = [np.array(c) * R for c in itertools.product(range(-4, 5), repeat=3) if sum(c) == 0]
pts = [np.array(c) * R for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2]
def sites(stack):
    if stack == 'octet': return np.array([np.array(c) * R / 2 for c in itertools.product(range(-5, 6, 2), repeat=3)])
    e2 = 2 * R * R; sl = [p for p in pts if abs(abs(p.sum()) - R) < 1e-9 and np.linalg.norm(p) < 2.6 * R]; T0 = []
    for q in itertools.combinations(range(len(sl)), 4):
        Q = [sl[i] for i in q]
        if all(abs(np.dot(a - b, a - b) - e2) < 1e-9 for a, b in itertools.combinations(Q, 2)): T0.append(np.mean(Q, 0))
    base = []
    for t in T0:
        k = 1 if t.sum() > 0 else -1; f = t + ((k * R - t.sum()) / 3) * np.ones(3)
        base += [f + i * np.array([1, -1, 0]) * R + j * np.array([0, 1, -1]) * R for i in range(-4, 5) for j in range(-4, 5)]
    out = []
    for k, m in maps('gyrated').items():
        for b in base:
            c = m[0] @ b + m[1]
            if np.linalg.norm(c) < 3.6 * R: out.append(c)
    return np.unique(np.round(out, 9), axis=0)
def vor(S, c):
    d = np.linalg.norm(S - c, axis=1); nb = S[(d > 1e-9) & (d < 2.6 * R)]
    hs = [np.r_[(p - c) / np.linalg.norm(p - c), -((p - c) / np.linalg.norm(p - c)) @ (p + c) / 2] for p in nb]
    return hull(HalfspaceIntersection(np.array(hs), c).intersections)
def mesh(mf, nd=5):
    me = mf.to_mesh(); return dict(v=np.round(np.asarray(me.vert_properties[:, :3], float), nd).tolist(), t=np.asarray(me.tri_verts).tolist())
out = dict(R=R, kits={})
for key, sol_k, stack in (('dbt-gyr', 'dbt', 'gyrated'), ('cut8-gyr', 'cut8', 'gyrated'), ('cut8-oct', 'cut8', 'octet')):
    sol = hull(SOL[sol_k]); bodies = []; twins = []
    for k, m in maps(stack).items():
        for c in cent0:
            cc = m[0] @ c + m[1]
            if np.linalg.norm(cc) < 4.2 * R: bodies.append(sol.transform(np.hstack([m[0], cc[:, None]])))
    ALL = m3.Manifold.batch_boolean(bodies, m3.OpType.Add); S = sites(stack)
    near = [c for c in S if np.linalg.norm(c) < 1.9 * R]
    fills = []
    for c in near:
        P = vor(S, c) - ALL
        if (P ^ sol.transform(np.hstack([np.eye(3) * 1.02, np.zeros((3, 1))]))).volume() < 1e-6: continue   # does not touch the origin solid
        hand = 0
        if stack == 'octet': hand = int(np.sign(np.prod(np.sign(c))))      # step 27: left at sign product +, right at -
        fills.append(dict(c=np.round(c, 6).tolist(), hand=hand, **mesh(P)))
    P0 = vor(S, near[0]) - ALL
    out['kits'][key] = dict(solid=mesh(sol), stack=stack, fills=fills, share=sol.volume() / 2.510263, solid_vol=sol.volume(), fill_vol=P0.volume(),
                            solid_sph=sph(sol), fill_sph=sph(P0))
    print(key, 'fill pieces touching the solid', len(fills), 'solid', round(sol.volume(), 6), 'fill', round(P0.volume(), 6), round(sph(P0), 3), flush=True)
json.dump(out, open(H + 'renders/kits-data.json', 'w'), separators=(',', ':'))
import os; print('bytes', os.path.getsize(H + 'renders/kits-data.json'))
