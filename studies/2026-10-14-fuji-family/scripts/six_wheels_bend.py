# Six equal hexagonal wheels that may bend (DICTO, 2026-10-14: "maybe the structure flattened some more than others"). Each wheel
# keeps its six spokes at 60° in its plane (plane square to a five-fold axis, turned by theta_i), but each spoke may lengthen or
# shorten (radius rho_ik, 1 = regular). Rims are straight between spoke ends. Wheels must meet where their planes cross. We find
# the turns and spoke lengths that meet everywhere with the least bending (sum of (rho - 1)^2), and report how much each wheel
# flattens (longest / shortest spoke). DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
N = [v / np.linalg.norm(v) for v in ico if v @ np.array([1e-3, 2e-3, 3e-3]) > 0]
F = []
for n in N:
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); F.append((a, np.cross(n, a)))
LINES = {}
for i, j in itertools.combinations(range(6), 2):
    d = np.cross(N[i], N[j]); LINES[(i, j)] = d / np.linalg.norm(d)
def rim(rho, th, ang):
    # distance from centre to the wheel's rim along in-plane direction ang (and along ang + pi): spokes at th + k*60deg, radii rho[k]
    out = []
    for a in (ang, ang + math.pi):
        x = (a - th) % (2 * math.pi); k = int(x // (math.pi / 3)); t = x - k * math.pi / 3
        r1, r2 = rho[k % 6], rho[(k + 1) % 6]
        # line through P1 = r1 (1,0) and P2 = r2 (cos60, sin60); intersect with ray at angle t
        P1 = np.array([r1, 0]); P2 = np.array([r2 * .5, r2 * math.sqrt(3) / 2]); dvec = np.array([math.cos(t), math.sin(t)])
        M = np.array([dvec, P1 - P2]).T; s = np.linalg.solve(M, P1)[0]; out.append(s)
    return out
def unpack(x): return x[:6], x[6:].reshape(6, 6)
def gaps(x):
    th, R = unpack(x); g = []
    for (i, j), d in LINES.items():
        ai = math.atan2(d @ F[i][1], d @ F[i][0]); aj = math.atan2(d @ F[j][1], d @ F[j][0])
        ri = rim(R[i], th[i], ai); rj = rim(R[j], th[j], aj); g += [ri[0] - rj[0], ri[1] - rj[1]]
    return np.array(g)
best = None; rng = np.random.default_rng(11)
for trial in range(60):
    x0 = np.concatenate([rng.uniform(0, math.pi / 3, 6), np.ones(36)])
    cons = {'type': 'eq', 'fun': gaps}
    r = minimize(lambda x: ((x[6:] - 1) ** 2).sum(), x0, constraints=[cons], method='SLSQP', options=dict(maxiter=500, ftol=1e-12))
    if r.success and abs(gaps(r.x)).max() < 1e-7 and (best is None or r.fun < best.fun): best = r
th, R = unpack(best.x)
out = dict(total_bending=float(best.fun), max_gap=float(abs(gaps(best.x)).max()),
           wheels=[dict(turn_deg=round(math.degrees(t) % 60, 3), spokes=[round(v, 4) for v in R[i]], flattening=round(R[i].max() / R[i].min(), 4)) for i, t in enumerate(th)])
json.dump(out, open(os.path.join(ROOT, 'six-wheels-bend.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
