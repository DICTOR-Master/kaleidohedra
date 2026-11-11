"""Local edge-angle count (necessary for tiling) for rejoined solids, with coplanar facets merged (no phantom seam edges).
Dehn is zero for all of them by additivity (each half Dehn-zero)."""
import math, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('~/study-runs/2026-11-04-dehn-screen/scripts/halfcell.py').read().split('print("RD"')[0])
s3 = math.sqrt(3); Hh = math.sqrt(2/3)
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def dihedrals(P):
    h = ConvexHull(P); planes = []
    for eq in h.equations:
        if not any(np.allclose(eq, q, atol=1e-7) for q in planes): planes.append(eq)
    X = P[h.vertices]; out = []
    for a, b in itertools.combinations(range(len(planes)), 2):
        on = [x for x in X if abs(planes[a][:3] @ x + planes[a][3]) < 1e-7 and abs(planes[b][:3] @ x + planes[b][3]) < 1e-7]
        if len(on) >= 2: out.append(round(180 - math.degrees(math.acos(np.clip(planes[a][:3] @ planes[b][:3], -1, 1))), 4))
    return sorted(set(out)), len(planes)
def closes(angs):
    for i, a in enumerate(angs):
        if not any(ks[i] >= 1 and (abs(sum(k*x for k, x in zip(ks, angs)) - 360) < 1e-3 or abs(sum(k*x for k, x in zip(ks, angs)) - 180) < 1e-3)
                   for ks in itertools.product(range(7), repeat=len(angs))): return False, a
    return True, None
N = np.array([[0,0,0],[0,1/s3,-Hh/2],[0,1/s3,0],[.5,-1/(2*s3),-Hh/2],[.5,-1/(2*s3),0],[.5,1/(2*s3),-Hh],[.5,s3/2,0],[1,0,0],[1,1/s3,-Hh/2],[1,1/s3,0]]) - np.array([.5, 1/(2*s3), 0])
T = half(RD, True)
P0 = np.array(sorted({tuple(s*v for s, v in zip(sg, p)) for p in itertools.permutations((1, 2, 3)) for sg in itertools.product((1, -1), repeat=3)}), float)
a = np.array([1, 1, 1])/s3; z = np.array([0, 0, 1.]); v = np.cross(a, z); K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); Rz = np.eye(3) + K + K @ K*((1 - a @ z)/np.linalg.norm(v)**2)
PP = P0 @ Rz.T; hp = ConvexHull(PP)
from scipy.spatial import HalfspaceIntersection
def halfP(top):
    Hs = np.vstack([hp.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
cases = {'hybrid N + half-RD 0°': np.vstack([N, T]), 'hybrid N + half-RD 60°': np.vstack([N, T @ rz(math.pi/3).T]),
         'twisted B3 permutohedron': np.vstack([halfP(True), halfP(False) @ rz(math.pi/3).T]), 'Covenant (control: tiles)': np.vstack([N, (N*np.array([1, 1, -1])) @ rz(math.pi/3).T])}
for nm, U in cases.items():
    U = np.unique(np.round(U, 8), axis=0); angs, nf = dihedrals(U); ok, bad = closes(angs)
    print(f'{nm:28s}: faces {nf}, dihedrals {angs}, angle count {"PASSES" if ok else f"FAILS at {bad}°"}')
