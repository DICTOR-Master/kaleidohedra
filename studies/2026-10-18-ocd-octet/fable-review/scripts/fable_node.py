# Fable review 2026-10-18 -- dicto-node job (numpy + manifold3d): (1) dense float sampling of one fundamental cell for BOTH kits,
# uniform points plus points pushed close to piece faces; (2) solid meshes of every piece: parts, genus, volume, area, sphericity;
# (3) mirror/rotation tests of the dented and notched tetrahedra; (4) sphericity of two improvement variants:
#     A = keys cut down to the hexagonal prism over the joint hexagon,  B = full kit without keys (OCD bare, M0 = H - two OCDs).
# usage: python3 fable_node.py fable-input.json fable-node.json      (export the input locally: python3 fable_node.py export fable-input.json)
import sys, json, itertools, time, numpy as np
if sys.argv[1] == 'export':
    import os; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
    from q5 import *
    S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
    f = lambda v: [qf(q(x)) for x in v]
    V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R'])
    l1 = lambda v: qa(qa(*[x if sgn(x) >= 0 else qn(x) for x in v[:2]]), v[2] if sgn(v[2]) >= 0 else qn(v[2]))
    hexes = {''.join('+' if si > 0 else '-' for si in s): [i for i, v in enumerate(V) if l1(v) == R and all(sgn(x) == si for x, si in zip(v, s))] for s in itertools.product([1, -1], repeat=3)}
    json.dump(dict(V=[f(v) for v in S1['V']], faces=S1['faces'], R=qf(R), Tp=[f(v) for v in S2['Tplus']], L=[f(v) for v in S2['lattice']],
                   keys={k: [f(p) for p in K] for k, K in S5['keys'].items()}, hexes=hexes), open(sys.argv[2], 'w')); sys.exit()
import manifold3d as m3
from scipy.spatial import ConvexHull
t0 = time.time(); D = json.load(open(sys.argv[1])); V = np.array(D['V']); R = D['R']; Tp = np.array(D['Tp']); L = np.array(D['L']); faces = D['faces']
PHI = (1 + 5 ** .5) / 2; OUT = {}
eq = lambda P: ConvexHull(np.asarray(P, float)).equations            # rows (n, -d): n.x + e <= 0 inside
ins = lambda X, E, tol=1e-12: np.all(X @ E[:, :3].T + E[:, 3] <= tol, axis=1)
E_ocd = eq(V); keys = {k: np.array(K) for k, K in D['keys'].items()}; E_key = {k: eq(K) for k, K in keys.items()}
E_tp = eq(Tp); E_tm = eq(-Tp)
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
def H_pts(i):
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in faces if i in f for j in f})]
    return np.vstack([star, o - star]), o, star
def prism_planes(i):
    """the central thick-rhombus prism at corner i (step 13 construction, float): side planes (n, -d) with n.x - d <= 0 inside"""
    P, o, star = H_pts(i); c1 = V[i]; c2 = o - c1; a = c1 / np.linalg.norm(c1)
    proj = lambda v: v - np.outer(v @ a, a) if v.ndim == 2 else v - (v @ a) * a
    rel = proj(star - c1); rr = np.linalg.norm(rel, axis=1); tips = rel[rr > rr.max() - 1e-9]; d = proj(c2 - c1)
    pair = [(p, q_) for p in range(5) for q_ in range(p + 1, 5) if np.allclose((tips[p] + tips[q_]) / PHI, d, atol=1e-9)]
    assert len(pair) == 1, pair
    p, q_ = pair[0]; rh = np.array([c1, c1 + tips[p] / PHI, c1 + d, c1 + tips[q_] / PHI]); cen = rh.mean(0); E = []
    for k in range(4):
        n = np.cross(rh[(k + 1) % 4] - rh[k], a); n /= np.linalg.norm(n); dd = n @ rh[k]
        if n @ cen > dd: n, dd = -n, -dd
        E.append([*n, -dd])
    return np.array(E), rh, a
Hs = {}; PR = {}
for i in five:
    P, o, star = H_pts(i); Hs[i] = (eq(P), o, P); PR[i] = prism_planes(i)
# cones: +z cone planes x - z <= 0 etc.
def cone_E(ax, sg):
    rows = []
    for k in range(3):
        if k == ax: continue
        for s in (1, -1):
            n = np.zeros(3); n[k] = s; n[ax] = -sg; rows.append([*n, 0.0])
    return np.array(rows)
CONES = [(ax, sg, cone_E(ax, sg)) for ax in range(3) for sg in (1, -1)]
shifts = [np.array(ijk) @ L for ijk in itertools.product(range(-2, 3), repeat=3)]
near = lambda c, rad: [s for s in shifts if np.linalg.norm(s + c) < rad]
# distinct middle hulls near the cell: dedupe by midpoint
Mlist = {}
for s in shifts:
    for i in five:
        E, o, P = Hs[i]; m = tuple(np.round(o / 2 + s, 6))
        if np.linalg.norm(o / 2 + s - L.sum(0) / 2) < 2.4 and m not in Mlist: Mlist[m] = (i, s)
print('middle hulls', len(Mlist), flush=True)
# ------------------------------------------------------------------ (1) sampling
def classify(P):
    n = len(P)
    cKO = np.zeros(n, int); anyK = np.zeros(n, bool); anyOCD = np.zeros(n, bool)
    cCAP = np.zeros(n, int); cNCAP = np.zeros(n, int); cDT = np.zeros(n, int); cNT = np.zeros(n, int)
    cM = np.zeros(n, int); cCORE = np.zeros(n, int); cREST = np.zeros(n, int); cM0 = np.zeros(n, int)
    inOCD = {}; inKEY = {}
    for si, s in enumerate(shifts):
        X = P - s
        io = ins(X, E_ocd); ik = np.zeros(n, bool)
        for k, E in E_key.items(): ik |= ins(X, E)
        inOCD[si] = io; inKEY[si] = ik; anyK |= ik; anyOCD |= io; cKO += (io | ik)
    anyH = np.zeros(n, bool); Hmem = {}
    for m, (i, s) in Mlist.items():
        E, o, Pp = Hs[i]; h = ins(P - s, E); Hmem[m] = h; anyH |= h
    KOany = anyK | anyOCD
    for m, (i, s) in Mlist.items():
        h = Hmem[m] & ~KOany; cM += h; cM0 += Hmem[m] & ~anyOCD
        Ep, rh, a = PR[i]; inpr = ins(P - s, Ep); cCORE += h & inpr; cREST += h & ~inpr
    for si, s in enumerate(shifts):
        X = P - s; io = inOCD[si]
        octa = np.abs(X).sum(1) <= R + 1e-12
        for ax, sg, Ec in CONES:
            c = octa & ins(X, Ec) & ~io; cCAP += c; cNCAP += c & ~anyH
        for E in (E_tp, E_tm):
            t = ins(X, E) & ~anyK; cDT += t; cNT += t & ~anyH
    keyed_total = cKO + cCAP + cDT; full_total = cKO + cNCAP + cM + cNT; full_split_total = cKO + cNCAP + cCORE + cREST + cNT
    # kit B (no keys): OCD + notched caps + M0 + tets notched by M0 (tets - anyH, no dents)
    cNT_B = np.zeros(n, int)
    for si, s in enumerate(shifts):
        X = P - s
        for E in (E_tp, E_tm): cNT_B += ins(X, E) & ~anyH
    noKey_total = sum(inOCD.values()) + cNCAP + cM0 + cNT_B
    return dict(keyed=keyed_total, full=full_total, full_split=full_split_total, noKey=noKey_total, Moverlap=cM, Hmem=anyH)
rng = np.random.default_rng(2026); N = int(sys.argv[3]) if len(sys.argv) > 3 else 2_000_000
cell_origin = np.zeros(3)
def sample_uniform(k): return rng.random((k, 3)) @ L
# all piece planes near the cell, for boundary-biased points
planes = []
for s in shifts:
    if np.linalg.norm(s - L.sum(0) / 2) > 2.6: continue
    for E in [E_ocd, E_tp, E_tm] + list(E_key.values()):
        planes.append(np.c_[E[:, :3], E[:, 3] - E[:, :3] @ s])
    planes.append(np.array([[a, b, c, -R - np.array([a, b, c]) @ s] for a in (1, -1) for b in (1, -1) for c in (1, -1)], float))
    for ax, sg, Ec in CONES: planes.append(np.c_[Ec[:, :3], Ec[:, 3] - Ec[:, :3] @ s])
for m, (i, s) in Mlist.items():
    E, o, Pp = Hs[i]; planes.append(np.c_[E[:, :3], E[:, 3] - E[:, :3] @ s]); Ep, rh, a = PR[i]; planes.append(np.c_[Ep[:, :3], Ep[:, 3] - Ep[:, :3] @ s])
planes = np.vstack(planes); planes = planes / np.linalg.norm(planes[:, :3], axis=1)[:, None]
def sample_boundary(k):
    """uniform points moved onto a random piece plane within reach, then pushed off it by delta in [1e-6, 1e-2] (log-uniform)"""
    P = sample_uniform(k); idx = rng.integers(0, len(planes), k); pl = planes[idx]
    dist = (P * pl[:, :3]).sum(1) + pl[:, 3]; P = P - dist[:, None] * pl[:, :3]
    delta = 10 ** rng.uniform(-6, -2, k) * rng.choice([-1, 1], k); P = P + delta[:, None] * pl[:, :3]
    # keep inside the cell: wrap by lattice (fold back)
    U = np.linalg.solve(L.T, P.T).T; U -= np.floor(U); return U @ L
res = {'uniform': {}, 'boundary': {}}
for kind, fn in (('uniform', sample_uniform), ('boundary', sample_boundary)):
    tot = {k: np.zeros(3, int) for k in ('keyed', 'full', 'full_split', 'noKey')}; movl = 0; cnt = 0
    for c in range(0, N, 100000):
        P = fn(min(100000, N - c)); out = classify(P); cnt += len(P)
        for k in tot:
            v = out[k]; tot[k] += [int((v == 0).sum()), int((v == 1).sum()), int((v >= 2).sum())]
        movl += int((out['Moverlap'] >= 2).sum())
    res[kind] = {k: dict(points=cnt, none=int(t[0]), exactly_one=int(t[1]), two_or_more=int(t[2])) for k, t in tot.items()}
    res[kind]['middle_pieces_overlapping'] = movl
    print(kind, res[kind], round(time.time() - t0), 's', flush=True)
OUT['sampling'] = res
# ------------------------------------------------------------------ (2) meshes
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float)); U = lambda ms: m3.Manifold.batch_boolean(ms, m3.OpType.Add)
OCD = hull(V); KEYS = {k: hull(K) for k, K in keys.items()}; keyed = U([OCD] + list(KEYS.values()))
nearS = [s for s in shifts if np.linalg.norm(s) < 2.3]
allkeyed = U([keyed.translate(s) for s in nearS]); allOCD = U([OCD.translate(s) for s in nearS])
def M_of(i, keyed_body):
    P, o, star = H_pts(i); return hull(P) - keyed_body - keyed_body.translate(o)
Mb = {i: M_of(i, keyed) for i in five}; Mall = U([Mb[i].translate(s) for s in nearS for i in five])
Mb0 = {i: M_of(i, OCD) for i in five}; Mall0 = U([Mb0[i].translate(s) for s in nearS for i in five])
i1 = [i for i in five if abs(V[i, 0]) < 1e-9 and V[i, 1] > 0 and V[i, 2] > 0][0]
Ep, rh, a = PR[i1]; prism = hull(np.vstack([rh - a, rh + a]))
M1 = Mb[i1]; core = M1 ^ prism; rest = M1 - prism
corner = hull([[0, 0, 0], [0, 0, R], [R/2, 0, R/2], [-R/2, 0, R/2], [0, R/2, R/2], [0, -R/2, R/2]] + [[x*R/3, y*R/3, R/3] for x in (1, -1) for y in (1, -1)])
cap = corner - OCD; ncap = cap - Mall
T = hull(Tp); Tm = hull(-Tp); DTp = T - allkeyed; DTm = Tm - allkeyed; NTp = DTp - Mall; NTm = DTm - Mall
# variant A: hexagon-trimmed keys
def hex_prism(k):
    H = V[D['hexes'][k]]; s = np.array([1 if ch == '+' else -1 for ch in k], float); nrm = s / 3 ** .5
    return hull(np.vstack([H - 0.5 * nrm, H + 0.5 * nrm]))
KEYS_A = {k: KEYS[k] ^ hex_prism(k) for k in keys}; keyed_A = U([OCD] + list(KEYS_A.values()))
allkeyed_A = U([keyed_A.translate(s) for s in nearS]); DTp_A = T - allkeyed_A
# variant B: no keys; M0; tets notched by M0 only
NTp_B = T - Mall0; M0 = Mb0[i1]; core_B = M0 ^ prism; rest_B = M0 - prism
from collections import Counter
def clean_area(mf):
    """surface area with zero-volume boolean sheets removed: coincident triangle pairs (same 3 vertices, rounded) cancel"""
    m = mf.to_mesh(); v = m.vert_properties[:, :3]; t = m.tri_verts
    key = [tuple(sorted(map(tuple, np.round(v[tri], 8)))) for tri in t]; c = Counter(key)
    ar = 0.5 * np.linalg.norm(np.cross(v[t[:, 1]] - v[t[:, 0]], v[t[:, 2]] - v[t[:, 0]]), axis=1)
    keep = np.array([c[k] == 1 for k in key]); return float(ar[keep].sum()), int((~keep).sum())
def sph(mf):
    A, dup = clean_area(mf); return np.pi ** (1 / 3) * (6 * mf.volume()) ** (2 / 3) / A
def describe(mf):
    parts = sorted([p.volume() for p in mf.decompose()], reverse=True); A, dup = clean_area(mf)
    return dict(volume=mf.volume(), area_raw=mf.surface_area(), area_cleaned=A, duplicate_triangles_removed=dup, sphericity=sph(mf), genus=mf.genus(),
                parts_total=len(parts), parts_over_1e_9=len([p for p in parts if p > 1e-9]), part_volumes=parts[:6], tris=len(mf.to_mesh().tri_verts))
pieces = dict(bare_OCD=OCD, keyed_OCD=keyed, cap=cap, dented_tet_plus=DTp, dented_tet_minus=DTm, middle=M1, penrose_core=core, middle_rest=rest,
              notched_cap=ncap, notched_tet_plus=NTp, notched_tet_minus=NTm,
              A_key_hex=KEYS_A['+++'], A_keyed_OCD=keyed_A, A_dented_tet=DTp_A, B_middle_nokeys=M0, B_core=core_B, B_rest=rest_B, B_notched_tet_nokeys=NTp_B)
OUT['pieces'] = {}
for k, mf in pieces.items():
    OUT['pieces'][k] = describe(mf); d = OUT['pieces'][k]
    print(f"{k:22s} V {d['volume']:.6f} A {d['area_raw']:.4f}/{d['area_cleaned']:.4f} psi {d['sphericity']:.3f} parts {d['parts_total']} (>1e-9: {d['parts_over_1e_9']}) genus {d['genus']}", flush=True)
# ------------------------------------------------------------------ (3) handedness: is the dented / notched T+ invariant under improper symmetries of the tetrahedron?
C = Tp.mean(0)
def tet_maps():
    out = []
    for perm in itertools.permutations(range(4)):
        A = np.c_[Tp - C, np.ones(4)]; B = Tp[list(perm)] - C
        M, *_ = np.linalg.lstsq(A, B, rcond=None); G = M[:3].T; t = M[3]
        out.append((G, t + C - G @ C, np.linalg.det(G) < 0))
    return out
def symdiff(A, B): return (A - B).volume() + (B - A).volume()
hand = {}
for name, body in (('dented_tet', DTp), ('notched_tet', NTp), ('A_dented_tet', DTp_A), ('B_notched_tet_nokeys', NTp_B)):
    proper_bad = 0; improper_ok = 0; worst_improper = 1e9
    for G, t, improper in tet_maps():
        img = body.transform(np.c_[G, t]); sd = symdiff(img, body)
        if improper:
            if sd < 1e-9: improper_ok += 1
            worst_improper = min(worst_improper, sd)
        elif sd > 1e-9: proper_bad += 1
    hand[name] = dict(proper_maps_failing=proper_bad, improper_maps_that_are_symmetries=improper_ok, smallest_improper_symdiff_volume=worst_improper,
                      chiral=improper_ok == 0)
    print(name, hand[name], flush=True)
# T- equals the point reflection of T+ (then they are mirror images exactly when T+ is chiral)
hand['Tminus_is_point_reflection_of_Tplus_symdiff'] = symdiff(DTp.transform(np.c_[-np.eye(3), np.zeros(3)]), DTm)
hand['notched_Tminus_is_point_reflection_symdiff'] = symdiff(NTp.transform(np.c_[-np.eye(3), np.zeros(3)]), NTm)
OUT['handedness'] = hand
# cap symmetry: the notched cap under x->-x, y->-y and the 90-degree turn about z
cs = {}
for nm, G in (('mirror_x', np.diag([-1, 1, 1.0])), ('mirror_y', np.diag([1, -1, 1.0])), ('turn_90_z', np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1.0]])), ('mirror_xy_swap', np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1.0]]))):
    cs[nm] = symdiff(ncap.transform(np.c_[G, np.zeros(3)]), ncap)
OUT['notched_cap_symdiff'] = cs; print('cap', cs)
# meshes of a few pieces for drawings
def mesh_of(mf):
    m = mf.to_mesh(); return dict(v=np.round(m.vert_properties[:, :3], 6).tolist(), t=m.tri_verts.tolist())
OUT['meshes'] = {k: mesh_of(pieces[k]) for k in ('A_keyed_OCD', 'A_key_hex', 'B_middle_nokeys', 'dented_tet_plus')}
OUT['seconds'] = round(time.time() - t0, 1); OUT['mark'] = 'DICTO · dictospheres.com'
json.dump(OUT, open(sys.argv[2], 'w')); print('done', OUT['seconds'], 's')
