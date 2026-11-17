#!/usr/bin/env python3
"""Heptagonal Queen, part 3: cubic-symmetric 3D shadows and central sections vs the fair die and the cube-octahedron line.
Targets: P(mu) = [-1,1]^3 n {|x|+|y|+|z| <= mu}: Kelvin's truncated octahedron (3/2), cuboctahedron (2), truncated cube (1+sqrt2),
the fair die mu_f = 1 + sqrt(2 tan(pi/14) tan(2pi/7)); and the rhombic dodecahedron (RD).
Searched: the five faithful actions of S4 on 7 points (4+1+1+1, 4+2+1, 4+3, 6+1 edges, 6+1 C4-cosets: all, up to conjugacy);
for each, the unique 3D subspace W carrying a 3D irreducible of S4 (multiplicity 1, so W and the equivariant projection are
defined over Q); shadows (orthogonal projection onto W) and central sections (polytope n W) of A_h, B_h, +-A_h, +-B_h, Q_h.
3D hulls in floats (labelled computed); identification by face census and edge ratios.
Controls: the 600-cell's section by the S4-invariant 3-space of sum-zero R^5 (perpendicular to a cell centre) must be a
cuboctahedron (Coxeter, Regular Polytopes, Table V); the 24-cell's vertex-first shadow must be an RD; P(3/2), P(2),
P(1+sqrt2), P(mu_f) built directly must be recognised.
Usage: s3_shadows.py out.json"""
import sys, json, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hlib import *
from collections import Counter
from scipy.spatial import ConvexHull, HalfspaceIntersection
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}
MUF = 1 + (2*math.tan(math.pi/14)*math.tan(2*math.pi/7))**0.5

def classify(Y):
    Y = np.asarray(Y, float); H = ConvexHull(Y); V = H.vertices; Yv = Y[V]
    eq = H.equations; planes = {}
    for e in eq: planes.setdefault(tuple(np.round(e, 6)), e)
    faces = [frozenset(np.nonzero(np.abs(Yv @ e[:3] + e[3]) < 1e-6*max(1, np.abs(Yv).max()))[0].tolist()) for e in planes.values()]
    census = Counter(len(f) for f in faces)
    edges = {}
    for i in range(len(Yv)):
        for j in range(i + 1, len(Yv)):
            fs = [k for k, f in enumerate(faces) if i in f and j in f]
            if len(fs) == 2: edges[(i, j)] = tuple(sorted(len(faces[k]) for k in fs))
    L = {k: np.linalg.norm(Yv[k[0]] - Yv[k[1]]) for k in edges}
    nv = len(Yv); onesphere = np.ptp(np.linalg.norm(Yv - Yv.mean(0), axis=1)) < 1e-6*np.abs(Yv).max()
    cen = dict(sorted(census.items())); res = dict(vertices=nv, faces=cen, one_sphere=bool(onesphere))
    def lens(kind): v = [L[k] for k in edges if edges[k] == kind]; return (min(v), max(v)) if v else None
    eqe = np.ptp(list(L.values())) < 1e-6*max(L.values())
    res['equal_edges'] = bool(eqe)
    if nv == 12 and cen == {3: 8, 4: 6} and onesphere and eqe: res['name'] = 'cuboctahedron (mu = 2)'; res['mu'] = 2.0
    elif nv == 24 and cen == {4: 6, 6: 8} and onesphere:
        s, h = lens((4, 6)), lens((6, 6))
        if s and h and np.ptp(s) < 1e-6 and np.ptp(h) < 1e-6:
            b = s[0]/(s[0] + h[0]); res['mu'] = 1 + b; res['name'] = f'cube-octahedron line, chamber I, mu = {1 + b:.10f}'
    elif nv == 24 and cen == {3: 8, 8: 6} and onesphere:
        oo, ot = lens((8, 8)), lens((3, 8))
        if oo and ot and np.ptp(oo) < 1e-6 and np.ptp(ot) < 1e-6:
            r = oo[0]/(2**0.5*ot[0]); a = r/(1 + r); res['mu'] = 2 + a; res['name'] = f'cube-octahedron line, chamber II, mu = {2 + a:.10f}'
    elif nv == 14 and cen == {4: 12}:
        res['name'] = 'rhombic dodecahedron' if all(edges[k] == (4, 4) for k in edges) and np.ptp([L[k] for k in L]) < 1e-6 else 'twelve 4-gons, not equilateral'
    elif nv == 8 and cen == {4: 6} and eqe: res['name'] = 'cube (mu = 3)'; res['mu'] = 3.0
    elif nv == 6 and cen == {3: 8} and eqe: res['name'] = 'octahedron (mu = 1)'; res['mu'] = 1.0
    res.setdefault('name', 'other')
    res['targets'] = [t for t, m in (('Kelvin 3/2', 1.5), ('cuboctahedron 2', 2.0), ('truncated cube 1+sqrt2', 1 + 2**0.5), ('fair die mu_f', MUF)) if 'mu' in res and abs(res['mu'] - m) < 1e-7]
    if res['name'] == 'rhombic dodecahedron': res['targets'].append('RD')
    return res

def line_member(mu):
    pts = set()
    for s in itertools.product((-1, 1), repeat=3):
        if mu <= 2: b = mu - 1; base = [(1, b, 0), (1, 0, b)]
        else: a = mu - 2; base = [(1, 1, a)]
        for bb in base:
            for p in set(itertools.permutations(bb)): pts.add(tuple(si*pi for si, pi in zip(s, p)))
    return np.array(sorted(pts))
# ---- field degrees of the targets (exact) ----
import sympy as sp
bb, xx = sp.symbols('b x')
Tm = xx**3 - 9*xx**2 - xx + 1   # minimal polynomial of T = tan(pi/14) tan(2pi/7) (gods-dice study)
C(sp.Poly(Tm, xx).is_irreducible and abs(float(sp.Poly(Tm, xx).eval(math.tan(math.pi/14)*math.tan(2*math.pi/7)))) < 1e-9, 'T = tan(pi/14)tan(2pi/7) is a root of x^3 - 9x^2 - x + 1 (irreducible)')
bpol = sp.Poly(Tm.subs(xx, bb**2/2), bb)*8
C(sp.Poly(bpol, bb).is_irreducible and sp.Poly(bpol, bb).degree() == 6, f'die: b = mu_f - 1 = sqrt(2T) has degree 6 ({sp.Poly(bpol, bb).as_expr()}); b/(1-b) generates the same field, so it is in no cubic field')
C(sp.Poly(bb**2 - 2*bb - 1, bb).is_irreducible, 'truncated cube: a = sqrt2 - 1 has degree 2; a cubic field has no element of degree 2')
# ---- classifier controls ----
for mu, want in ((1.5, 'Kelvin 3/2'), (2.0, 'cuboctahedron 2'), (1 + 2**0.5, 'truncated cube 1+sqrt2'), (MUF, 'fair die mu_f')):
    r = classify(line_member(mu)); C(want in r['targets'], f'classifier control P({mu:.6f}) -> {r["name"]}')
RD = np.array([p for p in itertools.product((-1, 1), repeat=3)] + [tuple(2*s*(i == k) for i in range(3)) for k in range(3) for s in (-1, 1)], float)
r = classify(RD); C('RD' in r['targets'], f'classifier control RD -> {r["name"]}')
Tb = np.array([p for p in set(itertools.permutations((0, 1, 1, 3)))], float); Tb = (Tb - Tb.mean(1, keepdims=True)) @ np.linalg.qr(np.array([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]], float).T)[0]
r = classify(Tb); C(r['name'] == 'other', f'classifier control: perms(0,1,1,3) (12 corners, 8 triangles + 6 rectangles, unequal edges) is not taken for a cuboctahedron')
r = classify(line_member(1.6)); C(r['targets'] == [] and abs(r['mu'] - 1.6) < 1e-9, f'classifier control P(1.6) is no target, mu read back {r["mu"]:.6f}')

def section(Xf, eqs7, U):
    hs = np.hstack([eqs7[:, :-1] @ U, eqs7[:, -1:]])
    nz = np.linalg.norm(hs[:, :-1], axis=1) > 1e-12
    return HalfspaceIntersection(hs[nz], np.zeros(U.shape[1])).intersections

def hull_eqs7(Xf):
    d = Xf.shape[1]; Q, _ = np.linalg.qr((np.eye(d)[:d-1] - 1/d).T); Bs = Q[:, :d-1]
    H = ConvexHull(Xf @ Bs, qhull_options='Qt'); e = H.equations
    return np.hstack([e[:, :-1] @ Bs.T, e[:, -1:]])

# ---- geometric controls ----
K = GOLD; z, one, ph, ph2 = K.el(0), K.el(1), K.el(0, 1), K.el(1, 1)
A = centre(canon_orbit([z, ph, ph2, ph2, ph2], K)); B = centre(canon_orbit([z, one, one, ph2, ph2], K))
R = centre(canon_orbit([ph, z, z, z, -ph], K)); P600 = K.f(uniq_pts(np.concatenate([A, -A, B, -B, R])))/5
W5 = np.eye(5)[:, :4] - np.eye(5)[:, :4].mean(0)  # S4 on coords 0..3 fixing 4: std = sum-zero vectors on 0..3
W5[4] = 0; W5 = W5 - 0; Q5_, _ = np.linalg.qr(np.array([[1, -1, 0, 0, 0], [1, 1, -2, 0, 0], [1, 1, 1, -3, 0]], float).T); U5 = Q5_
ax = np.array([1, 1, 1, 1, -4.]); h = P600 @ ax; mid = P600[np.abs(h) < 1e-9]
r = classify(mid @ U5); C(len(mid) == 12 and 'cuboctahedron 2' in r['targets'], f'control: the 600-cell corners in the central hyperplane perpendicular to the cell centre (1,1,1,1,-4): {len(mid)} corners -> {r["name"]} (Coxeter, Table V)')
r = classify(section(P600, hull_eqs7(P600), U5)); out['control_600_solid_central_section'] = r
C(r['name'] == 'other', f'note: the solid central section there is not a cuboctahedron ({r["vertices"]} vertices, faces {r["faces"]}); Coxeter Table V lists vertex layers')
r2 = classify(P600 @ U5); out['control_600_cellfirst_shadow'] = r2
D24 = np.array(sorted({tuple(s1*(i == a) + s2*(i == b) for i in range(4)) for a in range(4) for b in range(a + 1, 4) for s1 in (-1, 1) for s2 in (-1, 1)}), float)
Qv, _ = np.linalg.qr(np.array([[1, 1, 0, 0], [1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], float).T)
r = classify(D24 @ Qv[:, 1:]); C('RD' in r['targets'], f'control: 24-cell vertex-first shadow -> {r["name"]}')
out['controls'] = 'passed'

# ---- the five S4 actions on 7 points ----
S4 = list(itertools.permutations(range(4)))
def comp(p, q): return tuple(p[q[i]] for i in range(4))
def coset_action(H):
    H = set(H); cos = []
    for g in S4:
        c = frozenset(comp(g, h) for h in H)
        if c not in cos: cos.append(c)
    return [tuple(cos.index(frozenset(comp(g, h) for h in c)) for c in cos) for g in S4]
def gen(gs):
    S = {tuple(range(4))}; fr = list(S)
    while fr:
        nw = []
        for a in fr:
            for g in gs:
                c = comp(g, a)
                if c not in S: S.add(c); nw.append(c)
        fr = nw
    return S
S3 = gen([(1, 0, 2, 3), (1, 2, 0, 3)]); A4 = [p for p in S4 if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
D8 = gen([(1, 2, 3, 0), (2, 1, 0, 3)]); V4p = gen([(1, 0, 2, 3), (0, 1, 3, 2)]); C4 = gen([(1, 2, 3, 0)]); TRIV = [tuple(range(4))]; S4all = S4
assert len(S3) == 6 and len(A4) == 12 and len(D8) == 8 and len(V4p) == 4 and len(C4) == 4
EMB = {'4+1+1+1': [S3, S4all, S4all, S4all], '4+2+1': [S3, A4, S4all], '4+3': [S3, D8], '6+1 (edges)': [V4p, S4all], '6+1 (C4 cosets)': [C4, S4all]}
def ctype(p):
    seen, cyc = set(), []
    for i in range(4):
        if i in seen: continue
        j, l = i, 0
        while j not in seen: seen.add(j); j = p[j]; l += 1
        cyc.append(l)
    return tuple(sorted(cyc))
CHI = {'std': {(1, 1, 1, 1): 3, (1, 1, 2): 1, (2, 2): -1, (1, 3): 0, (4,): -1}, 'std x sgn': {(1, 1, 1, 1): 3, (1, 1, 2): -1, (2, 2): -1, (1, 3): 0, (4,): 1}}
def emb_perms(blocks):
    acts = [coset_action(H) for H in blocks]; res = []
    for gi in range(24):
        p, off = [], 0
        for a in acts: p += [off + x for x in a[gi]]; off += len(a[0])
        res.append(p)
    assert off == 7 and len({tuple(r) for r in res}) == 24, 'faithful'
    return res
K = HEPT; z = K.el(0); one = K.el(1); rho = K.el(0, 1); sig = K.el(-1, 0, 1)
rho2, sig2, rs = K.mul(rho, rho), K.mul(sig, sig), K.mul(rho, sig)
Ah = centre(canon_orbit([z, rho, rs, sig2, sig2, sig2, sig2], K)); Bh = centre(canon_orbit([z, one, one, rho2, rho2, sig2, sig2], K))
SETS = {'A_h': Ah, 'B_h': Bh, '+-A_h': np.concatenate([Ah, -Ah]), '+-B_h': np.concatenate([Bh, -Bh]), 'Q_h': np.concatenate([Ah, -Ah, Bh, -Bh])}
SF = {k: K.f(v)/7 for k, v in SETS.items()}; HE = {k: hull_eqs7(v) for k, v in SF.items()}
rows = []; lay = []; nlay = {}; found = Counter()
for en, blocks in EMB.items():
    perms = emb_perms(blocks); mult = {}
    for ch, chi in CHI.items():
        Pm = np.zeros((7, 7))
        for gi, g in enumerate(S4):
            M = np.zeros((7, 7)); M[perms[gi], range(7)] = 1; Pm += chi[ctype(g)]*M
        Pm *= 3/24; mult[ch] = int(round(np.trace(Pm)))//3
        if mult[ch] == 0: continue
        Uw, sv, _ = np.linalg.svd(Pm); U = Uw[:, :3]
        C(mult[ch] == 1 and np.allclose(U.sum(0), 0), f'{en}: irreducible {ch} has multiplicity 1 in sum-zero R^7 (unique W, defined over Q)')
        for nm, Xf in SF.items():
            for mode in ('shadow', 'section'):
                Y = Xf @ U if mode == 'shadow' else section(Xf, HE[nm], U)
                r = classify(Y); rows.append(dict(embedding=en, irrep=ch, set=nm, mode=mode, **r))
                for tg in r['targets']: found[tg] += 1
            # vertex layers parallel to W (Coxeter-style sections of the corner set): group corners by their exact component in W-perp
            P8 = np.rint(8*Pm).astype(np.int64); assert np.allclose(P8, 8*Pm)
            X = SETS[nm]; perpk = keyrows(8*X - np.einsum('ij,njk->nik', P8, X))
            groups = {}
            for i, k in enumerate(perpk): groups.setdefault(k, []).append(i)
            nl = 0
            for k, idx in groups.items():
                Y = Xf[idx] @ U
                if len(idx) < 4 or np.linalg.matrix_rank(Y - Y[0], tol=1e-9) < 3: continue
                r = classify(Y); nl += 1; lay.append(dict(embedding=en, set=nm, central=bool(np.allclose(Xf[idx].mean(0), 0, atol=1e-9)), **r))
                for tg in r['targets']: found[tg] += 1
            nlay[(en, nm)] = nl
    C(sum(mult.values()) == 1, f'{en}: exactly one 3D irreducible occurs ({mult})')
for r in rows: print(f"  {r['embedding']:16s} {r['irrep']:9s} {r['set']:6s} {r['mode']:7s} v={r['vertices']:4d} faces={r['faces']} sphere={r['one_sphere']} -> {r['name']}{'  TARGET ' + str(r['targets']) if r['targets'] else ''}")
lc = Counter((l['embedding'], l['vertices'], tuple(sorted(l['faces'].items())), l['name']) for l in lay)
for k, v in sorted(lc.items(), key=str): print('  layers', k, 'x', v)
out['rows'] = rows; out['layers'] = lay; out['found'] = dict(found)
C(True, f'vertex layers parallel to W with full 3D extent: {len(lay)} in all ({sum(1 for l in lay if l["targets"])} on a target)')
C(len(rows) == 5*5*2, f'searched {len(rows)} shadows/sections (5 actions x 5 sets x 2 modes)')
C(found['fair die mu_f'] == 0 and found['truncated cube 1+sqrt2'] == 0, 'no shadow or section is the fair die or the truncated cube (as the field degree requires)')
print('targets found:', dict(found))
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final(); print(f'time {time.time() - t0:.1f} s')
