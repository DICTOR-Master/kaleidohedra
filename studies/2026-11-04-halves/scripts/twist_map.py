#!/usr/bin/env python3
"""DICTO 4 Nov: "copy and build alternatives that can remain convex using resonance and fibonacci". Family S(μ, ν) = cube [-1,1]^3 ∩ {|x|+|y|+|z| <= μ}
∩ {RD planes |x_i| + |x_j| <= ν}, 3-fold axis (1,1,1). Grid over (μ, ν). For each: twisted (60° about the axis, halves through the centre) convex?
Dehn zero (solid and twist)? Harmonic Q4, Q6 of the corner set (resonance: sign changes along the grid lines). Golden / Fibonacci marks: μ, ν in
{φ, φ², 1/φ+1, 2/φ, F(n+1)/F(n)}. Output: data/twist-map.json (every grid point) and a list of candidate points (twist convex & Dehn zero)."""
import sys, json, math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.argv = [sys.argv[0], 'x', '8', '300']; exec(open('scripts/dehn.py').read().split("if __name__")[0])
sys.path.insert(0, 'scripts/_lib')
try: import methods as Mt
except Exception: Mt = None
a = np.array([1, 1, 1])/math.sqrt(3); z = np.array([0, 0, 1.]); v = np.cross(a, z); K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); Rz = np.eye(3) + K + K @ K*((1 - a @ z)/np.linalg.norm(v)**2)
CUBE = [np.eye(3)[i]*s for i in range(3) for s in (1, -1)]; OCT = [np.array(s, float) for s in itertools.product((1, -1), repeat=3)]
RDN = [np.array(p, float) for p in {tuple(s*x for s, x in zip(sg, q)) for q in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
def solid(mu, nu):
    pl = [(n, 1.0) for n in CUBE] + [(n, mu) for n in OCT] + [(n, nu) for n in RDN]
    H = np.array([[*(Rz @ n), -c] for n, c in pl]); return np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 9), axis=0)
def analyse(mu, nu):
    P = solid(mu, nu); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P)
    def half(top):
        Hs = np.vstack([h.equations, [0, 0, -1 if top else 1, 0]]); return HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
    T, B = half(True), half(False); U = np.unique(np.round(np.vstack([T, B @ rz(math.pi/3).T]), 6), axis=0); hu = ConvexHull(U)
    conv = abs(hu.volume - h.volume) < 1e-6*h.volume
    X, F = hull_faces(P); d0 = dehn(X, F)['dehn_zero']
    d1 = None
    if conv: Y, G = hull_faces(U[hu.vertices]); d1 = dehn(Y, G)['dehn_zero']
    q4 = float(Mt.Q3d(P, 4)) if Mt else None; q6 = float(Mt.Q3d(P, 6)) if Mt else None
    return {'mu': mu, 'nu': nu, 'corners': int(len(P)), 'twist_convex': bool(conv), 'dehn0': bool(d0), 'dehn0_twist': d1, 'Q4': q4, 'Q6': q6}
phi = (1 + 5**.5)/2; F = [1, 1]
for _ in range(10): F.append(F[-1] + F[-2])
MARKS = sorted({phi, phi**2, 1 + 1/phi**2, 2/phi, 3/phi, *[F[i + 1]/F[i] for i in range(1, 9)], 3/2, 5/3, 2.0})
mus = sorted(set(np.round(np.linspace(1.02, 2.98, 50), 4)) | {round(m, 6) for m in MARKS if 1 < m < 3})
nus = sorted(set(np.round(np.linspace(1.02, 1.98, 25), 4)) | {round(m, 6) for m in MARKS if 1 < m < 2})
rows = []
for mu in mus:
    for nu in nus:
        try: rows.append(analyse(float(mu), float(nu)))
        except Exception as e: pass
cand = [r for r in rows if r['twist_convex'] and r['dehn0'] and r['dehn0_twist']]
marked = [r for r in cand if any(abs(r['mu'] - m) < 1e-5 for m in MARKS) or any(abs(r['nu'] - m) < 1e-5 for m in MARKS)]
print('grid', len(rows), '| twist convex', sum(r['twist_convex'] for r in rows), '| solid Dehn 0', sum(r['dehn0'] for r in rows), '| candidates (twist convex, both Dehn 0)', len(cand), '| on golden/Fibonacci marks', len(marked))
for r in (marked or cand)[:15]: print(json.dumps(r))
json.dump({'rows': rows, 'candidates': cand, 'marks': MARKS}, open('data/twist-map.json', 'w'))
