# Tetrapods (DICTO, 2026-10-14): which shapes close exactly (a) four meeting at a point, (b) four round one. Every Polyhedraverse shape.
# (a) A corner of solid angle exactly π (a quarter of the space round a point). For a three-faced corner this suffices: a spherical
#     triangle with angle sum 2π tiles the sphere four times by half-turns about its side midpoints (the pattern of a disphenoid).
#     Corners with more faces are listed for a direct check. Near misses: within 3%.
# (b) A centre shape with four congruent faces whose normals point to a regular tetrahedron's corners; another shape attached face to
#     face on all four, by the centre's own tetrahedral rotations; exact = the four outer pieces do not overlap (convex hulls; a
#     non-convex piece is judged by its hull, so it can only be rejected wrongly, never accepted wrongly). Recorded too: whether
#     neighbouring outer pieces touch (share a face or an edge), i.e. whether the tetrapod closes up. DICTO · dictospheres.com
import itertools, json, math, os, sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(sys.argv[1]))
TET = math.acos(-1 / 3)
def unit(v): return v / np.linalg.norm(v)
def outward(V, F):
    c = V.mean(0); out = []
    for f in F:
        P = V[f]; n = np.zeros(3)
        for k in range(len(f)): n += np.cross(P[k], P[(k + 1) % len(f)])
        n = unit(n)
        out.append(n)
    # orient consistently outward for convex shapes; for others trust the stored winding but flip all if the volume is negative
    vol = sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
    return [(-n if vol < 0 else n) for n in out], abs(vol)
def is_convex(V, F):
    try: h = ConvexHull(V); return abs(h.volume - outward(V, F)[1]) < 1e-6 * max(1, h.volume)
    except Exception: return False
def corner_solid_angle(V, F, N, i):
    fs = [k for k, f in enumerate(F) if i in f]
    # dihedral angles at the edges through vertex i, inside the solid
    edges = {}
    for k in fs:
        f = F[k]; j = f.index(i)
        for nb in (f[j - 1], f[(j + 1) % len(f)]): edges.setdefault(nb, []).append(k)
    dih = []
    for nb, ks in edges.items():
        if len(ks) != 2: return None, None
        a, b = N[ks[0]], N[ks[1]]; dih.append(math.pi - math.acos(np.clip(a @ b, -1, 1)))
    return sum(dih) - (len(fs) - 2) * math.pi, len(fs)
res_a, near_a, res_b = [], [], []
for sid, s in S.items():
    V = np.array(s['v'], float); F = s['f']
    if len(V) < 4: continue
    N, vol = outward(V, F)
    if not is_convex(V, F): continue          # corners of convex shapes only (the formula assumes convex corners)
    seen = set()
    for i in range(len(V)):
        om, k = corner_solid_angle(V, F, N, i)
        if om is None: continue
        key = (round(om, 6), k)
        if key in seen: continue
        seen.add(key)
        if abs(om - math.pi) < 1e-6: res_a.append(dict(shape=sid, name=s['n'], corner_faces=k, solid_angle=om, exact_by='three-faced: half-turns' if k == 3 else 'more faces: check'))
        elif abs(om - math.pi) / math.pi < 0.03: near_a.append(dict(shape=sid, name=s['n'], corner_faces=k, off_percent=round(100 * (om - math.pi) / math.pi, 2)))
# (b) four round one
def faces_tetrahedral(V, F, N):
    out = []
    for quad in itertools.combinations(range(len(F)), 4):
        ns = [N[q] for q in quad]
        if all(abs(ns[a] @ ns[b] + 1 / 3) < 1e-6 for a, b in itertools.combinations(range(4), 2)):
            L = [sorted(round(float(np.linalg.norm(V[F[q][k]] - V[F[q][(k + 1) % len(F[q])]])), 6) for k in range(len(F[q]))) for q in quad]
            if all(l == L[0] for l in L) and all(len(F[q]) == len(F[quad[0]]) for q in quad): out.append(quad)
    return out
def kabsch(A, B):
    a, b = A.mean(0), B.mean(0); U, _, Wt = np.linalg.svd((B - b).T @ (A - a)); R = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Wt))]) @ Wt
    return R, b - a @ R.T
def hull_eq(P):
    h = ConvexHull(P); return h.equations
def overlap(P, Q):
    A = np.r_[hull_eq(P), hull_eq(Q)]
    r = linprog(c=[0, 0, 0, -1], A_ub=np.c_[A[:, :3], np.ones(len(A))], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(None, 1)])
    return r.status == 0 and r.x[3] > 1e-7
def touch(P, Q):
    d = min(np.linalg.norm(p - q) for p in P for q in Q)
    shared = sum(1 for p in P if any(np.linalg.norm(p - q) < 1e-6 for q in Q))
    return shared
centres = []
for sid, s in S.items():
    V = np.array(s['v'], float); F = s['f']
    if len(F) > 40 or len(V) < 4: continue
    N, vol = outward(V, F)
    if not is_convex(V, F): continue
    q = faces_tetrahedral(V, F, N)
    if q: centres.append((sid, V, F, N, q[0]))
print('centres with four tetrahedral faces:', [c[0] for c in centres], flush=True)
lib = []
for sid, s in S.items():
    V = np.array(s['v'], float); F = s['f']
    if len(V) < 4: continue
    N, vol = outward(V, F)
    lib.append((sid, V, F, N))
for cid, CV, CF, CN, quad in centres:
    f0 = CF[quad[0]]; T0 = CV[f0]; L0 = [round(float(np.linalg.norm(T0[k] - T0[(k + 1) % len(f0)])), 6) for k in range(len(f0))]
    cc = CV.mean(0)
    # the centre's rotations taking face quad[0] to each of the four (about its centre)
    rots = []
    for q in quad:
        Tq = CV[CF[q]]; got = None
        for r in range(len(f0)):
            for order in (Tq, Tq[::-1]):
                R, t = kabsch(T0 - cc, np.roll(order, r, axis=0) - cc)
                if np.abs((T0 - cc) @ R.T - (np.roll(order, r, axis=0) - cc)).max() < 1e-6 and np.linalg.det(R) > 0 and abs(np.linalg.norm(t)) < 1e-6:
                    got = R; break
            if got is not None: break
        rots.append(got)
    if any(r is None for r in rots): continue
    for pid, PV, PF, PN in lib:
        for fi, f in enumerate(PF):
            if len(f) != len(f0): continue
            Lp = [round(float(np.linalg.norm(PV[f[k]] - PV[f[(k + 1) % len(f)]])), 6) for k in range(len(f))]
            if sorted(Lp) != sorted(L0): continue
            Pf = PV[f]
            for r in range(len(f)):
                for order in (Pf, Pf[::-1]):
                    tgt = np.roll(order, r, axis=0)
                    R, t = kabsch(Pf, T0) if False else kabsch(tgt, T0)
                    if np.abs(tgt @ R.T + t - T0).max() > 1e-6: continue
                    P1 = PV @ R.T + t
                    if (P1.mean(0) - cc) @ CN[quad[0]] <= 1e-9: continue           # attached outside
                    outs = [(P1 - cc) @ Rq.T + cc for Rq in rots]
                    try: ov = overlap(outs[0], outs[1]) or overlap(outs[0], CV) 
                    except Exception: continue
                    if not ov:
                        res_b.append(dict(centre=cid, piece=pid, piece_name=S[pid]['n'], shared_corners_between_outer=touch(outs[0], outs[1])))
# dedupe
uniq = {}
for r in res_b: uniq.setdefault((r['centre'], r['piece']), r)
res_b = list(uniq.values())
out = dict(four_at_a_point=res_a, four_at_a_point_near=near_a, four_round_one=res_b)
json.dump(out, open(os.path.join(ROOT, 'tetrapods.json'), 'w'), indent=1)
print('A exact', len(res_a), 'near', len(near_a), 'B', len(res_b))
for r in res_a: print(' A', r['shape'], '|', r['name'][:60], r['corner_faces'], r['exact_by'])
for r in near_a[:30]: print(' A~', r['shape'], r['off_percent'], '%')
