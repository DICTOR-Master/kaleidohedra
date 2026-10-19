# DICTO 2026-10-20 "size for this solid ... ideal?": the triacontahedron scaled by s about the OG centre, cut by its octahedron (8 cuts).
# Float scan: share, corners, faces, sphericity of the solid; the octahedron's corner spaces (parts, sphericity); the fill pieces
# (leftover given to the nearest bipyramid in the gyrated octet, to the nearest tetrahedron in the octet).
import sys, json, itertools, math, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection, ConvexHull
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
DB = np.array([[fq(c) for c in v] for v in json.load(open(H + 'dbt-exact.json'))['V']])
R = fq(json.load(open(H + '../2026-10-18-ocd-octet/data/step1-ocd-exact.json'))['R'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
sph = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
n1 = np.ones(3) / 3 ** .5
E = ConvexHull(DB).equations; E = E[np.abs(np.abs(E[:, :3] @ n1) - 1) > 1e-6]; uq = []
for e in E:
    if not any(np.allclose(e, u, atol=1e-9) for u in uq): uq.append(e)
E = np.array(uq); RT = np.unique(np.round(HalfspaceIntersection(E, np.zeros(3)).intersections, 9), axis=0)
OCT = np.array([[s * R if k == j else 0 for j in range(3)] for k in range(3) for s in (1, -1)]); octa = hull(OCT)
MIR = np.eye(3) - 2 / 3 * np.ones((3, 3)); mir = lambda k: (MIR, 2 * k * R / 3 * np.ones(3)); comp = lambda a, b: (a[0] @ b[0], a[0] @ b[1] + a[1])
def maps(stack):
    LM = {0: (np.eye(3), np.zeros(3))}
    for k in range(1, 4):
        for s in (1, -1): j = s * k; LM[j] = comp(mir(2 * j - s), LM[j - s]) if stack == 'gyrated' else (np.eye(3), np.array([1, 1, 0]) * R * j)
    return LM
cent0 = [np.array(c) * R for c in itertools.product(range(-4, 5), repeat=3) if sum(c) == 0]
def vor(S, c):
    d = np.linalg.norm(S - c, axis=1); nb = S[(d > 1e-9) & (d < 2.6 * R)]
    hs = [np.r_[(p - c) / np.linalg.norm(p - c), -((p - c) / np.linalg.norm(p - c)) @ (p + c) / 2] for p in nb]
    return hull(HalfspaceIntersection(np.array(hs), c).intersections)
tetc = {'octet': np.array([[a, b, c] for a in (-.5, .5) for b in (-.5, .5) for c in (-.5, .5)]) * R}
ST = {'gyrated': np.array([[-2 / 3, -2 / 3, 1 / 3]]) * R, 'octet': np.array([[.5, .5, .5]]) * R}
def site_sets():
    out = {}
    pts = [np.array(c) * R for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2]
    # gyrated bipyramid centres: face centres on twin planes of tetrahedra; octet tetrahedron centres: R/2 (odd, odd, odd)
    out['octet'] = np.array([np.array(c) * R / 2 for c in itertools.product(range(-5, 6, 2), repeat=3)])
    LM = maps('gyrated'); bp = []; e2 = 2 * R * R
    sl = [p for p in pts if abs(abs(p.sum()) - R) < 1e-9 and np.linalg.norm(p) < 2.6 * R]; T0 = []
    for q in itertools.combinations(range(len(sl)), 4):
        Q = [sl[i] for i in q]
        if all(abs(np.dot(a - b, a - b) - e2) < 1e-9 for a, b in itertools.combinations(Q, 2)): T0.append(np.mean(Q, 0))
    base = []
    for t in T0:   # the tetrahedron's face centre on its twin plane (sum +-R), repeated in the layer
        k = 1 if t.sum() > 0 else -1; f = t + ((k * R - t.sum()) / 3) * np.ones(3)
        base += [f + i * np.array([1, -1, 0]) * R + j * np.array([0, 1, -1]) * R for i in range(-4, 5) for j in range(-4, 5)]
    for k, m in LM.items():
        for b in base:
            c = m[0] @ b + m[1]
            if np.linalg.norm(c) < 3.6 * R: bp.append(c)
    out['gyrated'] = np.unique(np.round(bp, 9), axis=0)
    return out
SS = site_sets()
for s in [float(x) for x in sys.argv[1:]] or [1.0, 1.03, 1.06, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5]:
    sol = hull(s * RT) ^ octa; V = np.asarray(sol.to_mesh().vert_properties[:, :3])
    Vu = np.unique(np.round(V, 6), axis=0); rtc = sum(1 for v in Vu if np.min(np.linalg.norm(s * RT - v, axis=1)) < 1e-6)
    cs = [p for p in (octa - sol).decompose() if p.volume() > 1e-8]
    line = f's {s:.3f}: share {sol.volume() / 2.510263 * 100:.2f}%  corners {len(Vu)} ({rtc} RT corners)  sph {sph(sol):.3f} | corner spaces {len(cs)}x {cs[0].volume() if cs else 0:.5f} sph {sph(cs[0]) if cs else 0:.3f}'
    for stack in ('gyrated', 'octet'):
        LM = maps(stack); bodies = []
        for k, m in LM.items():
            for c in cent0:
                cc = m[0] @ c + m[1]
                if np.linalg.norm(cc) < 4.2 * R: bodies.append(sol.transform(np.hstack([m[0], cc[:, None]])))
        ALL = m3.Manifold.batch_boolean(bodies, m3.OpType.Add)
        S = SS[stack]; c0 = ST[stack][0]
        if stack == 'gyrated': c0 = S[np.argmin(np.linalg.norm(S - c0, axis=1))]
        P = vor(S, c0) - ALL; parts = [p for p in P.decompose() if p.volume() > 1e-7]
        assert abs(vor(S, c0).volume() - (2.510263 if stack == 'gyrated' else 1.255131)) < 1e-4, vor(S, c0).volume()
        line += f' | {stack} fill {P.volume():.5f} parts {len(parts)} sph {sph(max(parts, key=lambda q: q.volume())):.3f}'
    print(line, flush=True)
