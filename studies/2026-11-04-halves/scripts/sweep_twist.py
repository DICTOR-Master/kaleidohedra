import math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
a = np.array([1, 1, 1])/math.sqrt(3); z = np.array([0, 0, 1.]); v = np.cross(a, z); K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); Rz = np.eye(3) + K + K @ K*((1 - a @ z)/np.linalg.norm(v)**2)
CUBE = [(e, 1.0) for i in range(3) for e in (np.eye(3)[i], -np.eye(3)[i])]; OCT = [(np.array(s, float), 1.0) for s in itertools.product((1, -1), repeat=3)]
RDN = [np.array(p, float) for p in {tuple(s*x for s, x in zip(sg, q)) for q in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
def poly(pl):
    H = np.array([[*(Rz @ n), -c] for n, c in pl]); return np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 9), axis=0)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def twist(P):
    h = ConvexHull(P)
    def half(top):
        Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
    T, B = half(True), half(False); U = np.unique(np.round(np.vstack([T, B @ rz(math.pi/3).T]), 6), axis=0); hu = ConvexHull(U)
    fs = {}
    for eq, sm in zip(hu.equations, hu.simplices): fs.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
    return abs(hu.volume - h.volume) < 1e-6*h.volume, len(hu.vertices), sorted(len(x) for x in fs.values())
for name, fam, rng in (('cube ∩ μ·octahedron (octa 1, TO 3/2, CO 2, cube 3)', lambda m: CUBE + [(n, m) for n, c in OCT], np.linspace(1.01, 2.99, 199)),
                       ('CO ∩ μ·RD (RD 1, CO 2)', lambda m: CUBE + [(n, 2.0) for n, c in OCT] + [(n, m) for n in RDN], np.linspace(1.001, 1.999, 200))):
    rows = [(m, *twist(poly(fam(m)))) for m in rng]
    conv = [r[0] for r in rows if r[1]]
    print(name, '| twisted convex for μ in:', (round(min(conv), 3), round(max(conv), 3)) if conv else 'never', f'({len(conv)}/{len(rows)} samples)')
    runs = []; 
    for r in rows:
        if r[1] and (not runs or runs[-1][1] != r[0] - (rng[1] - rng[0])): runs.append([r[0], r[0]])
        elif r[1]: runs[-1][1] = r[0]
    print('   convex stretches:', [(round(a, 3), round(b, 3)) for a, b in runs][:6])
    for m in (1.5, 5/3, 2.0) if 'octahedron' in name else (1.001, 1.5, 1.999):
        c, nv, f = twist(poly(fam(m))); print(f'   μ={m:.3f}: convex {c}, corners {nv}, faces {f}')
