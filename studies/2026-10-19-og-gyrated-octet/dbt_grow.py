# DICTO 2026-10-20 option 1: grow the DBT's rhombic triacontahedron (centred on the OG) by s and cut it flat where it meets its
# neighbours (the bisector planes of the gyrated octet's octahedron centres = its Voronoi cell; the twin planes are the pole cuts).
# Float: share of space, the leftover pieces (global, across cells), their volumes and sphericity, and the solid's faces.
import json, itertools, math, numpy as np, manifold3d as m3
from scipy.spatial import HalfspaceIntersection, ConvexHull
H = '/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
DB = np.array([[fq(c) for c in v] for v in json.load(open(H + 'dbt-exact.json'))['V']])
D = json.load(open(H + '../2026-10-18-ocd-octet/data/step1-ocd-exact.json')); R = fq(D['R'])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
sph = lambda mf: math.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / mf.surface_area()
n1 = np.ones(3) / 3 ** .5
E = ConvexHull(DB).equations; E = E[np.abs(np.abs(E[:, :3] @ n1) - 1) > 1e-6]          # drop the two pole planes -> the RT
uq = []
for e in E:
    if not any(np.allclose(e, u, atol=1e-9) for u in uq): uq.append(e)
E = np.array(uq); RT = HalfspaceIntersection(E, np.zeros(3)).intersections
RT = np.unique(np.round(RT, 9), axis=0); print('RT corners', len(RT), 'faces', len(E), 'volume', round(hull(RT).volume(), 6), 'inradius', round(-E[0, 3], 6))
MIR = np.eye(3) - 2 / 3 * np.ones((3, 3))
def mir(k): return (MIR, 2 * k * R / 3 * np.ones(3))
comp = lambda a, b: (a[0] @ b[0], a[0] @ b[1] + a[1])
LM = {0: (np.eye(3), np.zeros(3))}
for k in range(1, 4):
    for s in (1, -1): j = s * k; LM[j] = comp(mir(2 * j - s), LM[j - s])
cent0 = [np.array(c) * R for c in itertools.product(range(-4, 5), repeat=3) if sum(c) == 0]
bodies = []
for k, m in LM.items():
    for c in cent0:
        cc = m[0] @ c + m[1]
        if np.linalg.norm(cc) < 4.6 * R: bodies.append((m[0], cc))
C = np.array([b[1] for b in bodies]); print('octahedron centres', len(C))
def vor(i):
    c = C[i]; d = np.linalg.norm(C - c, axis=1); nb = C[(d > 1e-9) & (d < 2.2 * R)]
    hs = [np.r_[(p - c) / np.linalg.norm(p - c), -np.linalg.norm(p - c) / 2 - (p - c) / np.linalg.norm(p - c) @ c] for p in nb]
    return np.array(hs)
def solid(i, s):
    A, c = bodies[i]; P = (s * RT) @ A.T + c; hs = vor(i)
    V = HalfspaceIntersection(np.vstack([np.c_[E[:, :3] @ A.T, -(s * -E[:, 3]) - (E[:, :3] @ A.T) @ c], hs]), c).intersections
    return hull(V), hs
i0 = int(np.argmin(np.linalg.norm(C, axis=1)))
vc = hull(HalfspaceIntersection(vor(i0), C[i0]).intersections); print('Voronoi cell volume', round(vc.volume(), 6), '(cell 2.510263)', 'faces', len(vor(i0)))
near = [i for i in range(len(C)) if np.linalg.norm(C[i]) < 4.3 * R]
box = hull([[a, b, c] for a in (-2.4 * R, 2.4 * R) for b in (-2.4 * R, 2.4 * R) for c in (-2.4 * R, 2.4 * R)])
for s in [1.32, 1.34, 1.36, 1.38, 1.40, 1.43, 1.46, 1.5, 1.55, 1.6]:
    S0, hs = solid(i0, s); share = S0.volume() / vc.volume()
    # faces of S0: which Voronoi planes it touches, how many RT planes remain
    Vs = np.asarray(S0.to_mesh().vert_properties[:, :3]); A, c = bodies[i0]
    onv = sum(np.any(np.abs(Vs @ h[:3] + h[3]) < 1e-7) and np.sum(np.abs(Vs @ h[:3] + h[3]) < 1e-7) >= 3 for h in hs)
    En = np.c_[E[:, :3], -s * -E[:, 3]]
    onr = sum(np.sum(np.abs(Vs @ e[:3] - s * -E[0, 3]) < 1e-7) >= 3 for e in E)
    cellparts = [p for p in (vc - S0).decompose() if p.volume() > 1e-7]
    U = m3.Manifold.batch_boolean([solid(i, s)[0] for i in near], m3.OpType.Add)
    left = box - U; gl = [p for p in left.decompose() if p.volume() > 1e-7]
    def where(p):
        Q = np.asarray(p.to_mesh().vert_properties[:, :3]); c = Q.mean(0); return f'{(c.sum() / R):+.2f}'
    kinds = {}
    for p in cellparts: kinds.setdefault((round(p.volume(), 5), round(sph(p), 2)), []).append(where(p))
    print(f's {s:.2f}: share {share * 100:.2f}%  faces {onr} RT + {onv} cut; sph {sph(S0):.3f} | global leftover parts {len(gl)} (largest {max([q.volume() for q in gl] or [0]):.3f}) | in one Voronoi cell: ' +
          '; '.join(f'{len(v)}x {k[0]} sph {k[1]} at sum/R {sorted(set(v))}' for k, v in sorted(kinds.items(), key=lambda kv: -kv[0][0])), flush=True)
