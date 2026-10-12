# Orientation-refined Dehn (Hadwiger-type) invariants for cuts into kit pieces in the 120 turns of the Lotus frame (2026-10-12).
#
# Setting: every solid here (kit pieces in the frame's 120 turns, at any size and position, the band, the hole) has its faces in a
# finite set of plane directions. For a line direction v, let C_v be the circle of directions perpendicular to v, and D_v the
# directions in C_v of every such face plane containing v (both sides). An edge of a solid parallel to v contributes its length times
# the arc of C_v that the solid fills round that edge. Along any segment inside a cut-up solid the arcs add to the full circle, and
# where the segment lies inside a face of the whole they add to a half circle. So any additive function mu on arcs (with ends in
# D_v) that is zero on every half circle bounded by a face plane, and unchanged by the turns of the frame that keep the line v,
# gives an invariant  H_mu(X) = sum over edges of X parallel to (a turn of) v of  length (in Q(sqrt5), exact) * mu(arc).
# H_mu is additive under every cut into pieces of these shapes (non face-to-face cuts included). The plain Dehn invariant is the
# case mu = angle (mod pi); here every admissible mu is used, so the test is at least as strong.
# The ring: H(R) = H(phi*P) - H(P) - H(P(1/phi) point-mirrored) = (phi - 1 - 1/phi) H(P) = 0 (the point mirror is in the frame group).
# A cut of R into kit pieces needs sum_i n_i H(piece_i) = 0 and sum_i n_i vol(piece_i) = vol(R), n_i >= 0 (one variable per piece
# type, turn and size phi^k). If that LP is infeasible, no such cut exists.
import sys, os, itertools, json, numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
import sympy as sp
rc.KIT.update(KIT); PHI = rc.PHI
src = open(os.path.join(rc.HERE, 'local_cover.py')).read()
exec(src[src.index('# the 120 frame symmetries'):src.index('pieces = {k')])
TYPES = os.environ.get('TYPES', 'AXE,CLEO,FUJI,J2,t1,t2,t3,t4,t5,t6,T2,I,J11,AP').split(',')
far = np.argmax(np.linalg.norm(KIT['I'] - KIT['I'][0], axis=1)); KIT['AP'] = np.delete(KIT['I'], [0, far], axis=0)
def nrm(x): return x / np.linalg.norm(x)
def canon_line(d):
    d = nrm(d); s = np.sign(d @ np.array([0.2718, 0.5772, 0.3141])); return d * s
def keyv(x): return tuple(np.round(x, 7))
# solids whose faces define the plane set: kit pieces in all turns, plus the J2 and FUJI rings' band and hole
solids0 = {k: KIT[k] for k in TYPES}
ringsolids = {}
for nm in ('J2', 'FUJI'):
    r = rc.ring(nm)
    ringsolids[nm] = {'big': np.vstack([r['floor'], r['apex'][None]]), 'tip': np.vstack([r['top'], r['apex'][None]]), 'hole': r['hole']}
normals, lines = {}, {}
def collect(V):
    for e in rc.planes(V): normals[keyv(canon_line(e[:3]))] = canon_line(e[:3])
    for i, j, l, d in rc.convex_edges(V): lines[keyv(canon_line(V[i] - V[j]))] = canon_line(V[i] - V[j])
for V in solids0.values():
    for g in G: collect(V @ g.T)
for d in ringsolids.values():
    for V in d.values(): collect(V)
N = np.array(list(normals.values())); Lns = np.array(list(lines.values()))
print(f'{len(N)} plane directions, {len(Lns)} edge line directions in the frame', flush=True)
# G-orbits of lines
orbit_of, reps = {}, []
for d in Lns:
    k = keyv(d)
    if k in orbit_of: continue
    reps.append(d); oi = len(reps) - 1
    for g in G: orbit_of[keyv(canon_line(g @ d))] = oi
print(f'{len(reps)} classes of edge lines under the 120 turns', flush=True)
# per class: circle, points, elementary arcs, admissible mu basis
CL = []
for v in reps:
    a = nrm(np.cross(v, [1, 0, 0] if abs(v[0]) < .9 else [0, 1, 0])); b = np.cross(v, a)
    pts = []
    for n in N:
        if abs(n @ v) < 1e-9:
            w = nrm(np.cross(v, n))
            for s in (w, -w): pts.append(np.arctan2(s @ b, s @ a) % (2 * np.pi))
    pts = np.array(sorted(set(np.round(pts, 10))))
    m = len(pts)
    def arc_vec(t1, t2):
        """elementary arcs from angle t1 counter-clockwise to t2 (t1, t2 in pts)"""
        i, j = int(np.argmin(np.abs(pts - t1 % (2 * np.pi)))), int(np.argmin(np.abs(pts - t2 % (2 * np.pi))))
        for t, ix in ((t1, i), (t2, j)):
            dd = abs(pts[ix] - t % (2 * np.pi)); dd = min(dd, 2 * np.pi - dd)
            if dd > 1e-7: raise ValueError(f'arc end {t % (2 * np.pi):.9f} not among the circle points (nearest off by {dd:.2e}); points {np.round(pts, 4)}')
        vec = np.zeros(m, int); k = i
        while k != j: vec[k] = 1; k = (k + 1) % m
        return vec
    rel = []
    for t in pts:
        rel.append(arc_vec(t, t + np.pi))                     # half circles (each point has its antipode: planes come in +-)
    stab = [g for g in G if abs(abs((g @ v) @ v) - 1) < 1e-9]
    for g in stab:
        # image of elementary arc k (from pts[k] to pts[k+1]) under g: arc between the images of its ends, oriented as the circle
        sgn = np.sign((g @ v) @ v)
        for k in range(m):
            p0 = np.cos(pts[k]) * a + np.sin(pts[k]) * b; p1 = np.cos(pts[(k + 1) % m]) * a + np.sin(pts[(k + 1) % m]) * b
            q0, q1 = g @ p0, g @ p1
            t0, t1 = np.arctan2(q0 @ b, q0 @ a), np.arctan2(q1 @ b, q1 @ a)
            img = arc_vec(t0, t1) if sgn * np.linalg.det(g) > 0 else arc_vec(t1, t0)
            e = np.zeros(m, int); e[k] = 1; rel.append(e - img)
    A = sp.Matrix(np.array(rel))
    basis = A.nullspace()            # mu with A mu = 0
    MU = np.array([[float(x) for x in b_] for b_ in basis]) if basis else np.zeros((0, m))
    # make rational basis exact
    MUq = [[Fraction(str(x)) for x in b_] for b_ in basis]
    CL.append(dict(v=v, a=a, b=b, pts=pts, m=m, arc_vec=arc_vec, MU=MU, MUq=MUq, stab=len(stab)))
print('admissible arc functionals per line class (dim):', [len(c['MU']) for c in CL], flush=True)
# length units per class: lengths along a class are in Q(sqrt5) times a class unit; snap
def gsnap(x, tol=1e-8):
    for den in (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 60):
        for q in range(-400, 401):
            p = x * den - q * PHI
            if abs(p - round(p)) < tol * den: return Fraction(round(p), den), Fraction(q, den)
    raise ValueError(x)
unit = {}
def H(V, interior_sign=+1):
    """invariant of convex solid V: dict (class, mu index) -> (p, q) rational coefficients of 1 and phi"""
    out = {}
    E = rc.planes(V); on = [set(np.where(np.abs(V @ f[:3] + f[3]) < 1e-7)[0]) for f in E]; c0 = V.mean(0)
    for fa, fb in itertools.combinations(range(len(E)), 2):
        s = sorted(on[fa] & on[fb])
        if len(s) < 2: continue
        d = np.cross(E[fa][:3], E[fb][:3]); pr = V[s] @ d; i, j = s[int(np.argmin(pr))], s[int(np.argmax(pr))]
        L = np.linalg.norm(V[i] - V[j]); dl = canon_line(V[i] - V[j])
        oi = orbit_of[keyv(dl)]; cl = CL[oi]
        if len(cl['MU']) == 0: continue
        g = next(g for g in G if np.linalg.norm(canon_line(g @ dl) - cl['v']) < 1e-7)   # turn taking this edge's line to the class line
        mid = (V[i] + V[j]) / 2
        # the two half-plane directions (into each face, perpendicular to the edge), and the interior direction
        ws = []
        for f in (fa, fb):
            w = np.cross(dl, E[f][:3]); w = nrm(w)
            if (c0 - mid) @ w < 0 and False: pass
            # choose the sign pointing into the face: towards the face's other corners
            other = [V[k] for k in on[f] if k not in (i, j)]
            if not other: other = [V[k] for k in on[f]]
            if np.mean([(o - mid) @ w for o in other]) < 0: w = -w
            ws.append(g @ w)
        inner = g @ nrm((c0 - mid) - ((c0 - mid) @ dl) * dl)
        ang = [np.arctan2(w @ cl['b'], w @ cl['a']) for w in ws]; ai = np.arctan2(inner @ cl['b'], inner @ cl['a'])
        # the arc from ang[0] to ang[1] counter-clockwise contains the interior direction? else swap
        span = (ang[1] - ang[0]) % (2 * np.pi); pos = (ai - ang[0]) % (2 * np.pi)
        t1, t2 = (ang[0], ang[1]) if pos < span else (ang[1], ang[0])
        vec = cl['arc_vec'](t1, t2)
        if oi not in unit: unit[oi] = L
        p, q = gsnap(L / unit[oi])
        for k, mu in enumerate(cl['MUq']):
            val = sum(mu[t] for t in range(cl['m']) if vec[t])
            if val == 0: continue
            o = out.get((oi, k), (Fraction(0), Fraction(0))); out[(oi, k)] = (o[0] + p * val, o[1] + q * val)
    return out
def addH(A, B, s=1):
    out = dict(A)
    for k, (p, q) in B.items():
        o = out.get(k, (Fraction(0), Fraction(0))); out[k] = (o[0] + s * p, o[1] + s * q)
    return {k: v for k, v in out.items() if v != (0, 0)}
def scaleH(A, k):
    """multiply by phi^k: (p + q phi) phi = q + (p + q) phi"""
    out = {}
    for key, (p, q) in A.items():
        for _ in range(abs(k)):
            if k > 0: p, q = q, p + q
            else: p, q = q - p, p                    # / phi: (p + q phi)/phi = (p + q phi)(phi - 1) = q + (p - q)... see check below
        out[key] = (p, q)
    return out
# check the /phi rule numerically
x = (Fraction(3), Fraction(5)); y = scaleH({0: x}, -1)[0]; assert abs((float(y[0]) + float(y[1]) * PHI) - (3 + 5 * PHI) / PHI) < 1e-12
# the rings
for nm, d in ringsolids.items():
    Hr = addH(addH(H(d['big']), H(d['tip']), -1), H(d['hole']), -1)
    print(f'{nm} ring: invariant components nonzero: {len(Hr)}  (expected 0)', flush=True)
    HP = H(KIT[nm]); print(f'   {nm} itself: {len(HP)} nonzero components; plain check H(big) = phi H(P): {addH(H(d["big"]), scaleH(HP, 1), -1) == {}}', flush=True)
# pieces in all turns
rows = {}
for nm in TYPES:
    seen = set()
    for gi, g in enumerate(G):
        V = KIT[nm] @ g.T; kk = tuple(sorted(map(keyv, V - V.mean(0))))
        if kk in seen: continue
        seen.add(kk); rows[(nm, gi)] = H(V)
print(f'{len(rows)} distinct piece turns', flush=True)
json.dump({'classes': len(CL), 'dims': [len(c['MU']) for c in CL],
           'rows': {f'{k[0]}|{k[1]}': {f'{a}|{b}': [str(p), str(q)] for (a, b), (p, q) in v.items()} for k, v in rows.items()},
           'volumes': {k: rc.vol(KIT[k]) for k in TYPES}}, open(os.path.join(rc.HERE, '../data/hadwiger-rows.json'), 'w'))
print('wrote data/hadwiger-rows.json', flush=True)
