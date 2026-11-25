# Copy from study 2026-11-24-aequi-certify-extend, used unchanged except where marked 'study 2026-11-25' (groups.py here: the five-cube directions; mixed = RD directions from two or more cubes).
# Refine each double-precision solution to 80 digits (mpmath; corners by Cramer's rule from the face triples, as in
# study 2026-11-19-aequus-rd-ico), confirm |Ω - 4π/N| < 1e-50 on every face and the corner incidences to 1e-50,
# then compute in floats from the refined depths: centroid, full symmetry group (every isometry fixing the centroid
# that maps the face planes onto themselves), face orbits under it, sides, corners.
# usage: exact.py dice.json SLICE_I[,SLICE_I...] SLICE_N NPROC out.jsonl   (refines every Aequus: centroid at the centre, >= 2 face orbits)
import json, sys, itertools, os, time, numpy as np
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS, DFAM, schoenflies
from scipy.spatial import HalfspaceIntersection
from mpmath import mp, mpf, sqrt, atan2, pi, findroot, nstr
DPS = 80
def mpdirs():
    mp.dps = DPS + 20; ph = (1 + sqrt(5)) / 2
    cand = []
    for t in [(1, 0, 0), (1, 1, 1), (1, 1, 0), (0, ph, 1), (0, 1 / ph, ph), (1, ph, 1 / ph), (0, 1, ph), (0, ph, 1 / ph), (ph, 1, 1 / ph)]:
        for s in itertools.product((1, -1), repeat=3):
            q = [a * b for a, b in zip(s, t)]
            for k in range(3): cand.append(q[-k:] + q[:-k] if k else q)
    out = []
    for v in DIRS:
        for q in cand:
            n = sqrt(sum(c * c for c in q)); w = [c / n for c in q]
            if max(abs(float(a) - b) for a, b in zip(w, v)) < 1e-9: out.append(w); break
    assert len(out) == len(DIRS)
    return out
MD = None
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def un(v): n = sqrt(dot(v, v)); return [c / n for c in v]
def tri(a, b, c): return 2 * atan2(abs(dot(a, cross(b, c))), 1 + dot(a, b) + dot(b, c) + dot(c, a))
def combinatorics(Nrm, D):
    hs = HalfspaceIntersection(np.hstack([Nrm, -D[:, None]]), np.zeros(3)); V = hs.intersections
    U = []                       # merge corners closer than 1e-8 (one corner where four or more planes meet)
    for v in V:
        if not any(np.abs(v - w).max() < 1e-8 for w in U): U.append(v)
    V = np.array(U)
    inc = [np.where(np.abs(Nrm @ v - D) < 1e-8)[0] for v in V]
    trip = []
    for I in inc:
        for t in itertools.combinations(I, 3):
            if abs(np.linalg.det(Nrm[list(t)])) > 1e-6: trip.append(t); break
        else: raise RuntimeError('no triple')
    faces = []
    for f in range(len(D)):
        vi = [i for i, I in enumerate(inc) if f in I]; P = V[vi]; c = P.mean(0)
        e1 = P[0] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(Nrm[f], e1)
        faces.append([vi[j] for j in np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))])
    return V, inc, trip, faces
def refine(rec):
    global MD
    if MD is None: MD = mpdirs()
    mp.dps = DPS + 20
    idx = rec['idx']; sizes = rec['sizes']; m = len(sizes); N = len(idx)
    Nrm = DIRS[idx]; D0 = np.repeat(rec['depths'], sizes)
    V, inc, trip, faces = combinatorics(Nrm, D0)
    n = [MD[j] for j in idx]; T = 4 * pi / N
    cut = np.cumsum([0] + sizes)
    def verts(dep):
        d = [dep[k] for k in range(m) for _ in range(sizes[k])]
        out = []
        for (i, j, k) in trip:
            a, b, c = n[i], n[j], n[k]; bc, ca, ab = cross(b, c), cross(c, a), cross(a, b); Dt = dot(a, bc)
            out.append([(d[i] * bc[t] + d[j] * ca[t] + d[k] * ab[t]) / Dt for t in range(3)])
        return out, d
    def oms(dep):
        Vm, d = verts(dep); res = []
        for f in range(N):
            P = [un(Vm[i]) for i in faces[f]]
            c = un([sum(Vm[i][t] for i in faces[f]) for t in range(3)])
            res.append(sum(tri(c, P[i], P[(i + 1) % len(P)]) for i in range(len(P))))
        return res, Vm, d
    def F(*x):
        o = oms([mpf(1)] + list(x))[0]
        return [sum(o[cut[k]:cut[k + 1]]) / sizes[k] - T for k in range(1, m)]
    x0 = [mpf(v) for v in rec['depths'][1:]]
    xs = findroot(F, x0, tol=mpf(10) ** (-2 * DPS + 20), maxsteps=60)
    xs = [xs[i] for i in range(m - 1)] if hasattr(xs, 'rows') else [xs]
    dep = [mpf(1)] + xs
    o, Vm, d = oms(dep)
    res_om = max(abs(w - T) for w in o)
    # incidences exact and every corner inside every half-space
    res_inc = max(abs(dot(n[f], Vm[i]) - d[f]) for i, I in enumerate(inc) for f in I)
    viol = max(dot(n[f], v) - d[f] for v in Vm for f in range(N))
    ok = res_om < mpf(10) ** -50 and res_inc < mpf(10) ** -50 and viol < mpf(10) ** -50
    return dict(depths60=[nstr(x, 60) for x in dep], res_omega=nstr(res_om, 3), res_inc=nstr(res_inc, 3),
                max_violation=nstr(viol, 3), exact_ok=bool(ok), corners=len(Vm),
                faces=faces, verts=[[float(c) for c in v] for v in Vm])
def centroid(V, faces, Nrm, D):
    # volume-weighted centroid by tetrahedra from an interior point
    o = V.mean(0); vol = 0; c = np.zeros(3)
    for f in faces:
        P = V[f]
        for i in range(1, len(P) - 1):
            w = abs(np.dot(P[0] - o, np.cross(P[i] - o, P[i + 1] - o))) / 6
            vol += w; c += w * (o + P[0] + P[i] + P[i + 1]) / 4
    return c / vol, vol
def symmetry(Nrm, D, cen):
    Dc = D - Nrm @ cen; feet = Nrm * Dc[:, None]
    i1 = 0; i2 = next(j for j in range(len(D)) if abs(np.dot(Nrm[0], Nrm[j])) < 0.999)
    def frame(a, b):
        e1 = a / np.linalg.norm(a); e2 = b - e1 * np.dot(e1, b); e2 /= np.linalg.norm(e2); return np.array([e1, e2, np.cross(e1, e2)]).T
    F0 = frame(feet[i1], feet[i2]); G = []
    for j1 in range(len(D)):
        if abs(Dc[j1] - Dc[i1]) > 1e-8: continue
        for j2 in range(len(D)):
            if abs(Dc[j2] - Dc[i2]) > 1e-8 or abs(np.dot(feet[j1], feet[j2]) - np.dot(feet[i1], feet[i2])) > 1e-8 or j2 == j1: continue
            F1 = frame(feet[j1], feet[j2])
            for s in (1, -1):
                R = F1 @ np.diag([1, 1, s]) @ F0.T
                img = feet @ R.T
                dmin = np.min(np.linalg.norm(img[:, None, :] - feet[None, :, :], axis=2), axis=1)
                if dmin.max() < 1e-7 and not any(np.allclose(R, g, atol=1e-7) for g in G): G.append(R)
    perms = [np.argmin(np.linalg.norm((feet @ R.T)[:, None, :] - feet[None, :, :], axis=2), axis=1) for R in G]
    seen = set(); orbs = []
    for f in range(len(D)):
        if f in seen: continue
        O = sorted({int(p[f]) for p in perms}); seen |= set(O); orbs.append(O)
    return G, orbs
def work(rec):
    try:
        ex = refine(rec)
    except Exception as e:
        return dict(rec, exact_ok=False, error=repr(e))
    idx = rec['idx']; Nrm = DIRS[idx]; D = np.array([float(x) for x in np.repeat([mpf(v) for v in ex['depths60']], rec['sizes'])])
    V = np.array(ex['verts']); faces = ex['faces']
    cen, vol = centroid(V, faces, Nrm, D)
    G, orbs = symmetry(Nrm, D, cen)
    out = dict(rec); out.update({k: v for k, v in ex.items() if k not in ('verts',)})
    out.update(centroid=cen.tolist(), centroid_at_origin=bool(np.abs(cen).max() < 1e-9), volume=vol,
               sym_order=len(G), sym_group=schoenflies(G), chiral=bool(all(np.linalg.det(g) > 0 for g in G)),
               face_orbits=orbs, sides=[len(f) for f in faces], verts=ex['verts'],
               mirrors=[np.linalg.eigh(g)[1][:, 0].tolist() for g in G if np.linalg.det(g) < 0 and np.allclose(g @ g, np.eye(3), atol=1e-8)
                        and not np.allclose(g, -np.eye(3), atol=1e-8)])
    return out
if __name__ == '__main__':
    src, si, sn, npr, out = sys.argv[1], {int(x) for x in sys.argv[2].split(',')}, int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    allr = json.load(open(src))['dice']
    recs = [dict(sid=d['sid'], idx=d['idx'], sizes=d['sizes'], depths=d['depths']) for d in allr
            if d['centroid_at_origin'] and not d['face_transitive']]
    recs = [r for k, r in enumerate(recs) if k % sn in si]   # SLICE_I may be a comma list of residues
    done = set()
    if os.path.exists(out):
        for L in open(out):
            try: done.add(json.loads(L)['sid'])
            except Exception: pass
    recs = [r for r in recs if r['sid'] not in done]
    print('to refine', len(recs), flush=True); t0 = time.time()
    with Pool(npr) as pool, open(out, 'a') as fo:
        for r in pool.imap_unordered(work, recs):
            fo.write(json.dumps(r) + '\n'); fo.flush()
    print('done in', round(time.time() - t0, 1), 's; FINAL ok', flush=True)
