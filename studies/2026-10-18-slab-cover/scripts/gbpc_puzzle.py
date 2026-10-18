# DICTO 2026-10-17: "is a puzzler's brain not better suited to this than randomness?" -- a puzzler's search for G', one wedge at a time.
# Every piece goes in with its 24 copies under the symmetries the OCD shares with the bcc packing (Th), so the search solves one wedge of
# the 24 (DICTO: "dissect the solids into a few quadrants facing each other"). As a puzzler would:
#   * the gap with the FEWEST pieces that fit is filled first (a gap with one option is a forced move);
#   * a gap that still has free space but takes no piece is a dead end: undo and try the next option (backtracking);
#   * among the options at a gap, the charge (golden-conjugate volume) is kept on track first, then larger pieces first.
# Pieces: golden rhombohedra (3 sizes), the Bodhi pieces (2 sizes), and the halves of each rhombohedron cut on its own icosahedral mirror
# planes, allowed only flat against a mirror of the 24, where the mirror copy completes the whole piece. Exact overlap test on every copy.
# A gap ("anchor") is a corner of G' or of a placed piece; it is open while a small probe step from it in some symmetry direction is free.
# usage: NODES=20000 HOURS=6 python3 gbpc_puzzle.py MODE SEED OUT.json
# DICTO 2026-10-17: "build out from the faces of a single OCD and aim for a shape to integrate best in line with its symmetry".
# Symmetric growth of G' round one OCD (its golden envelope, the RT at the origin): every piece goes in with all its symmetric copies.
#   stage Ih  the OCD's own full symmetry (120): a golden onion, perfectly in line with it, as far as it fits;
#   stage Th  the 24 symmetries the OCD shares with the bcc packing (the most a repeating fill can keep): the seam;
#   stage 1   no symmetry, to finish (as the plain search).
# Anchors are taken nearest the OCD first (grow outwards); sizes largest first in each stage; among the pieces that fit, the charge
# (golden-conjugate volume) is kept on track first (CHARGE=2 of gbpc_search_charge.py). Exact overlap test as there, on every copy.
# usage: python3 gbpc_sym.py MODE SEED RESTARTS OUT.json
# Fable, GBPC pass 4 (2026-10-16): exact fill search for G' (golden region minus the 24 GBPCs per bcc cell), numpy + fractions only,
# so it runs on dicto-node. Input: data/gbpc-geom-exact.json (gbpc_export.py). Numbers a + b*sqrt5 are pairs of Fractions.
# Bodies: the uncut RTs on the bcc sites (G' = space minus their union, pass 1), golden rhombohedra (edges along five-fold axes),
# optionally the five Bodhi pieces. Overlap test: separating axes = all face normals and all cross products of edge directions of the
# bodies in play. All edge directions are symmetry axes (checked), so a fixed axis list makes the test exact and complete.
# Every placement is accepted only if, on some axis, the two projections are disjoint or touch EXACTLY (float only prefilters).
# Search: randomised greedy restarts. At each anchor (a corner of G' or of a placed body), try every body, every orientation, and every
# corner of the body at the anchor. Prefer the largest size that fits, then the most face contacts, ties at random. Periodic: each
# placed body stands for its whole lattice orbit.
# 2026-10-17 (DICTO: "positive and negative terminals"): charge-balance steering. Each body's charge is the golden conjugate of its
# volume (a + b√5 -> a - b√5); an exact fill must match G''s conjugate volume too (the count proof). Among the bodies that fit at an
# anchor, CHARGE=1 prefers contacts then the smallest running imbalance; CHARGE=2 prefers the imbalance first. Size order unchanged.
# (see gbpc_sym.py's own header below)
# usage: CHARGE=1 python3 gbpc_search_charge.py MODE SEED RESTARTS OUT.json   MODE: R (rhombohedra), RB (plus Bodhi), RX (plus sizes lam/phi, lam/phi^2)
import sys, os, json, itertools, random, time, numpy as np
from fractions import Fraction as Fr
S5 = 5 ** 0.5
def q(s): a, b = s.split('|'); return (Fr(a), Fr(b))
qa = lambda x, y: (x[0] + y[0], x[1] + y[1]); qs = lambda x, y: (x[0] - y[0], x[1] - y[1])
qm = lambda x, y: (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
qf = lambda x: float(x[0]) + float(x[1]) * S5
def qsgn(x):
    a, b = x
    if a == 0 and b == 0: return 0
    if a >= 0 and b >= 0: return 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a * a - 5 * b * b > 0 else (1 if b > 0 else -1)
Z = (Fr(0), Fr(0))
vadd = lambda u, v: [qa(a, b) for a, b in zip(u, v)]; vsub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
vmul = lambda u, k: [qm(a, k) for a in u]
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
cross = lambda u, w: [qs(qm(u[1], w[2]), qm(u[2], w[1])), qs(qm(u[2], w[0]), qm(u[0], w[2])), qs(qm(u[0], w[1]), qm(u[1], w[0]))]
vf = lambda v: np.array([qf(x) for x in v])
det3 = lambda a, b, c: dot(a, cross(b, c))
iszero = lambda v: all(x == Z for x in v)
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
G = json.load(open(os.path.join(STUDY, 'data', 'gbpc-geom-exact.json')))
dec = lambda v: [q(x) for x in v]
LB = [dec(v) for v in G['LB']]; RTV = [dec(v) for v in G['RT']]; CORN = [dec(v) for v in G['corners']]
AX5 = [dec(v) for v in G['AX5']]; AX3 = [dec(v) for v in G['AX3']]; AX2 = [dec(v) for v in G['AX2']]
GPV = q(G['GP_volume'])
phi = (Fr(1, 2), Fr(1, 2)); lam = qm(phi, (Fr(1, 9), Fr(0)))
MODE = sys.argv[1]; SEED = int(sys.argv[2]); RESTARTS = 1; OUT = sys.argv[3]
half = lambda x: qm(x, (Fr(1, 2), Fr(0))); iphi = (Fr(-1, 2), Fr(1, 2))   # 1/phi = phi - 1
SIZES = [lam, half(lam), half(half(lam))]
if MODE == 'RX': SIZES += [qm(lam, iphi), qm(qm(lam, iphi), iphi)]
SIZES.sort(key=lambda x: -qf(x))
# ---- shapes: (kind, size, vertices relative to vertex 0, volume)
def parallel(u, w): return iszero(cross(u, w))
shapes = []
for a, b, c in itertools.combinations(range(6), 3):
    gens = [AX5[a], AX5[b], AX5[c]]; d = det3(*gens); d = d if qsgn(d) > 0 else qs(Z, d)
    oblate = None
    for s in SIZES:
        W = [vadd(vadd(vmul(gens[0], qm(s, (Fr(i), Fr(0)))), vmul(gens[1], qm(s, (Fr(j), Fr(0))))), vmul(gens[2], qm(s, (Fr(k), Fr(0)))))
             for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        shapes.append(dict(kind='rh', size=s, W=W, vol=qm(qm(qm(s, s), s), d), det=d))
dets = sorted({qf(sh['det']) for sh in shapes});
for sh in shapes: sh['kind'] = 'oblate' if abs(qf(sh['det']) - dets[0]) < 1e-12 else 'prolate'
if MODE == 'RB':
    for bname, B in G['bodhi'].items():
        blk = [dec(c) for c in B['block']]
        # block-coordinate volume (exact): convex, so sum of |det| of fan triangles seen from the vertex mean, / 6
        cm = [qm(sum((c[t] for c in blk[1:]), blk[0][t]) if False else Z, Z) for t in range(3)]
        cm = [(sum(c[t][0] for c in blk) / len(blk), sum(c[t][1] for c in blk) / len(blk)) for t in range(3)]
        vb = Z
        for fc in B['faces']:
            for t in range(1, len(fc) - 1):
                d_ = det3(vsub(blk[fc[0]], cm), vsub(blk[fc[t]], cm), vsub(blk[fc[t + 1]], cm))
                vb = qa(vb, d_ if qsgn(d_) >= 0 else qs(Z, d_))
        vb = qm(vb, (Fr(1, 6), Fr(0)))
        print(f'{bname} volume in block-cube (prolate) units: {vb[0]}+{vb[1]}*sqrt5 = {qf(vb):.9f}', flush=True)
        for s in SIZES[:2]:
            for fr in G['faces']:
                e = [vmul(dec(v), s) for v in fr]
                W = [vadd(vadd(vmul(e[0], c[0]), vmul(e[1], c[1])), vmul(e[2], c[2])) for c in blk]
                fd = det3(*e); fd = fd if qsgn(fd) > 0 else qs(Z, fd)
                shapes.append(dict(kind=bname, size=s, W=W, vol=qm(vb, fd), faces=B['faces']))

def qinv(x): n = x[0] * x[0] - 5 * x[1] * x[1]; return (x[0] / n, -x[1] / n)
# mirror-cut halves of the rhombohedra (DICTO's dissection): cut on each of its mirror planes that is an icosahedral mirror (normal on a
# 2-fold axis), both sides kept; exact corners (the cut points of the edges), exactly half the volume
from scipy.spatial import ConvexHull as _CH
nh = 0
for sh in [x for x in shapes if x['kind'] in ('oblate', 'prolate')]:
    W = sh['W']; c = [(sum(w[t][0] for w in W) / 8, sum(w[t][1] for w in W) / 8) for t in range(3)]; Wk = {tuple(w) for w in W}
    for n in AX2:
        k2 = qm((Fr(2), Fr(0)), qinv(dot(n, n)))
        refl = lambda v: vsub(v, vmul(n, qm(dot(n, vsub(v, c)), k2)))
        if {tuple(refl(w)) for w in W} != Wk: continue
        for sg in (1, -1):
            side = [w for w in W if sg * qsgn(dot(n, vsub(w, c))) >= 0]
            pts = list(side)
            for u, v in itertools.combinations(W, 2):
                du, dv = dot(n, vsub(u, c)), dot(n, vsub(v, c))
                if qsgn(du) * qsgn(dv) < 0:
                    x = vadd(u, vmul(vsub(v, u), qm(du, qinv(qs(du, dv)))))
                    if tuple(x) not in {tuple(y) for y in pts}: pts.append(x)
            hv = sorted(set(_CH(np.array([vf(x) for x in pts])).vertices)); P = [pts[i] for i in hv]
            shapes.append(dict(kind=sh['kind'] + '-half', size=sh['size'], W=P, vol=qm(sh['vol'], (Fr(1, 2), Fr(0))), cut=(n, c))); nh += 1
print('halves', nh, flush=True)
# ---- axes
lines = AX5 + AX3 + AX2
def edges_of(sh):
    if sh['kind'] in ('oblate', 'prolate') or sh['kind'].endswith('-half'): return [AX5[0]]   # on symmetry lines (closed below)
    Wf = np.array([vf(v) for v in sh['W']]); E = set()
    for fc in sh['faces']:
        for t in range(len(fc)): E.add(tuple(sorted((fc[t], fc[(t + 1) % len(fc)]))))
    return [vsub(sh['W'][j], sh['W'][i]) for i, j in E]
dirs = list(AX5)
for sh in shapes:
    if sh['kind'] in ('oblate', 'prolate') or sh['kind'].endswith('-half'): continue
    for d in edges_of(sh):
        L = next((l for l in lines if parallel(d, l)), None)
        assert L is not None, 'Bodhi edge not on a symmetry axis'
        if not any(parallel(L, x) for x in dirs): dirs.append(L)
# symmetric growth: every symmetry line of each kind in use, so the overlap axes hold for every symmetric copy of every piece
dirs = [l for L in (AX5, AX3, AX2) if any(any(parallel(d, l) for l in L) for d in dirs) for l in L]
AXES = list(AX2)
for d1, d2 in itertools.combinations(dirs, 2):
    n = cross(d1, d2)
    if not iszero(n) and not any(parallel(n, x) for x in AXES): AXES.append(n)
NA = len(AXES); AXf = np.array([vf(n) for n in AXES])
# Bodhi face normals must be among the axes (they are golden): check
for sh in shapes:
    if 'faces' in sh:
        for fc in sh['faces']:
            i, j, k = fc[0], fc[1], fc[2]
            n = cross(vsub(sh['W'][j], sh['W'][i]), vsub(sh['W'][k], sh['W'][i]))
            assert any(parallel(n, x) for x in AXES), 'face normal missing'
        break
def proj(W):   # exact (lo, hi) lists over AXES and float arrays
    P = [[dot(n, w) for w in W] for n in AXES]
    lo = [min(p, key=qf) for p in P]; hi = [max(p, key=qf) for p in P]
    return lo, hi, np.array([qf(x) for x in lo]), np.array([qf(x) for x in hi])
# candidate placements per anchor: shape with vertex k at the anchor -> offsets
CANDS = []
for si, sh in enumerate(shapes):
    seen = set()
    for k, wk in enumerate(sh['W']):
        Wk = [vsub(w, wk) for w in sh['W']]
        lo, hi, lof, hif = proj(Wk)
        key_ = tuple(np.round(np.r_[lof, hif], 9))
        if key_ in seen: continue
        seen.add(key_)
        cen = np.mean([vf(w) for w in Wk], 0); rad = max(np.linalg.norm(vf(w) - cen) for w in Wk)
        CANDS.append(dict(si=si, k=k, lo=lo, hi=hi, lof=lof, hif=hif, cen=cen, rad=rad, Wk=Wk))
REACH = max(max(np.linalg.norm(vf(w)) for w in C['Wk']) for C in CANDS) + 1e-6
order_size = sorted({qf(sh['size']) for sh in shapes}, reverse=True)
# lattice and RTs
LATT = []
for m in itertools.product(range(-5, 6), repeat=3):
    c = vadd(vadd(vmul(LB[0], (Fr(m[0]), Fr(0))), vmul(LB[1], (Fr(m[1]), Fr(0)))), vmul(LB[2], (Fr(m[2]), Fr(0))))
    if np.linalg.norm(vf(c)) < 3.6: LATT.append(c)
LATTf = np.array([vf(c) for c in LATT]); TPf = LATTf @ AXf.T
TP = [[dot(n, c) for n in AXES] for c in LATT]
rlo, rhi, rlof, rhif = proj(RTV); RTrad = max(np.linalg.norm(vf(v)) for v in RTV)
Linv = np.linalg.inv(np.array([vf(b) for b in LB]).T); Lf = np.array([vf(b) for b in LB]).T
OFFS = [np.array(m) for m in itertools.product(range(-2, 3), repeat=3)]
def red(p):
    base = np.round(Linv @ vf(p)).astype(int)
    m = min((base + o for o in OFFS), key=lambda mm: np.linalg.norm(vf(p) - Lf @ mm))
    c = vadd(vadd(vmul(LB[0], (Fr(int(m[0])), Fr(0))), vmul(LB[1], (Fr(int(m[1])), Fr(0)))), vmul(LB[2], (Fr(int(m[2])), Fr(0))))
    r = vsub(p, c); assert np.linalg.norm(vf(r)) < 1.3; return r
CORN = [red(p) for p in CORN]
CHG = int(os.environ.get('CHARGE', '1'))
def cj(x): return float(x[0]) - float(x[1]) * 5 ** .5
CGPV = cj(GPV); FGPV = qf(GPV)

def qinv(x): n = x[0] * x[0] - 5 * x[1] * x[1]; return (x[0] / n, -x[1] / n)
def inv_cols(c):
    di = qinv(det3(c[0], c[1], c[2]))
    return [vmul(r, di) for r in (cross(c[1], c[2]), cross(c[2], c[0]), cross(c[0], c[1]))]
def qsum(xs):
    t = Z
    for x in xs: t = qa(t, x)
    return t
apply = lambda M, v: [dot(M[i], v) for i in range(3)]
S12 = AX5 + [vmul(a, (Fr(-1), Fr(0))) for a in AX5]; S12k = {tuple(v) for v in S12}
BI = inv_cols([AX5[0], AX5[1], AX5[2]]); d01, d02, d12 = dot(AX5[0], AX5[1]), dot(AX5[0], AX5[2]), dot(AX5[1], AX5[2])
IH, seen = [], set()
for u in S12:
    for v in S12:
        if dot(u, v) != d01: continue
        for w in S12:
            if dot(u, w) != d02 or dot(v, w) != d12: continue
            M = [[qsum(qm(U[i], BI[k][j]) for k, U in enumerate((u, v, w))) for j in range(3)] for i in range(3)]
            k_ = tuple(tuple(r) for r in M)
            if k_ in seen or not all(tuple(apply(M, a)) in S12k for a in AX5): continue
            seen.add(k_); IH.append(M)
LI = inv_cols(LB)
def keeps_lattice(M):
    for b in LB:
        for x in (dot(r, apply(M, b)) for r in LI):
            if x[1] != 0 or x[0].denominator != 1: return False
    return True
TH = [M for M in IH if keeps_lattice(M)]
ID = [[(Fr(1), Fr(0)) if i == j else Z for j in range(3)] for i in range(3)]
print(json.dumps(dict(Ih=len(IH), Th=len(TH), axes=NA)), flush=True)
assert len(IH) == 120, len(IH)
def body_of(W):
    lo, hi, lof, hif = proj(W); Wf = np.array([vf(w) for w in W]); cen = Wf.mean(0)
    return dict(lo=lo, hi=hi, lof=lof, hif=hif, cen=cen, rad=float(np.max(np.linalg.norm(Wf - cen, axis=1))), W=W)
def collides(B, placed, Pc, Prad):
    ids = [('rt', i) for i in range(len(LATTf)) if np.linalg.norm(B['cen'] - LATTf[i]) < B['rad'] + RTrad + 1e-9]
    if len(placed):
        D = np.linalg.norm(B['cen'][None, None, :] - Pc[:, None, :] - LATTf[None, :, :], axis=2)
        ids += [('pl', b, t) for b, t in zip(*np.where(D < B['rad'] + Prad[:, None] + 1e-9))]
    for idd in ids:
        if idd[0] == 'rt': blof, bhif = rlof + TPf[idd[1]], rhif + TPf[idd[1]]
        else: O = placed[idd[1]]; blof, bhif = O['lof'] + TPf[idd[2]], O['hif'] + TPf[idd[2]]
        g = np.maximum(blof - B['hif'], B['lof'] - bhif)
        if g.max() > 1e-9: continue
        if g.max() < -1e-9: return True
        sep = False
        for a in np.where(g >= -1e-9)[0]:
            if idd[0] == 'rt': blo, bhi = qa(rlo[a], TP[idd[1]][a]), qa(rhi[a], TP[idd[1]][a])
            else: O = placed[idd[1]]; blo, bhi = qa(O['lo'][a], TP[idd[2]][a]), qa(O['hi'][a], TP[idd[2]][a])
            if qsgn(qs(blo, B['hi'][a])) >= 0 or qsgn(qs(B['lo'][a], bhi)) >= 0: sep = True; break
        if not sep: return True
    return False
def orbit(W, group):
    out, keys = [], set()
    for M in group:
        W2 = [apply(M, w) for w in W]; Wf = np.array([vf(w) for w in W2])
        sh = Lf @ np.floor(Linv @ Wf.mean(0) + 1e-9); key = tuple(sorted(tuple(np.round(v - sh, 6)) for v in Wf))
        if key not in keys: keys.add(key); out.append(W2)
    return out

def cj(x): return float(x[0]) - float(x[1]) * 5 ** .5
CGPV = cj(GPV); FGPV = qf(GPV)
NODES = int(os.environ.get('NODES', '20000')); HOURS = float(os.environ.get('HOURS', '6'))
CLOF = np.array([C['lof'] for C in CANDS]); CHIF = np.array([C['hif'] for C in CANDS])
CSZ = np.array([qf(shapes[C['si']]['size']) for C in CANDS])
PROBE = [vf(v) / np.linalg.norm(vf(v)) for L in (AX5, AX3, AX2) for v in L]; PROBE = np.array(PROBE + [-x for x in PROBE]) * 0.006
def okey(Wf):
    sh = Lf @ np.floor(Linv @ Wf.mean(0) + 1e-9); return tuple(sorted(tuple(np.round(v - sh, 6)) for v in Wf))
def near_bodies(pf, placed, Pc, Prad, r):
    rt = [i for i, cf in enumerate(LATTf) if np.linalg.norm(pf - cf) < r + RTrad]
    pl = list(zip(*np.where(np.linalg.norm(pf[None, None, :] - Pc[:, None, :] - LATTf[None, :, :], axis=2) < r + Prad[:, None]))) if len(placed) else []
    lo = np.array([rlof + TPf[i] for i in rt] + [placed[b]['lof'] + TPf[t] for b, t in pl]).reshape(-1, NA)
    hi = np.array([rhif + TPf[i] for i in rt] + [placed[b]['hif'] + TPf[t] for b, t in pl]).reshape(-1, NA)
    return lo, hi
def status(p, placed, Pc, Prad):
    """(open, indices of the candidate placements that pass the float prefilter at anchor p)"""
    pf = vf(p); lo, hi = near_bodies(pf, placed, Pc, Prad, REACH)
    X = (pf[None, :] + PROBE) @ AXf.T
    inside = np.any(np.all((X[:, None, :] > lo[None] + 1e-9) & (X[:, None, :] < hi[None] - 1e-9), axis=2), axis=1)
    if inside.all(): return False, []
    ppf = np.array([qf(dot(n, p)) for n in AXES])
    ok = np.ones(len(CANDS), bool)
    for j in range(0, len(lo), 16):
        g = np.maximum(lo[None, j:j + 16] - (ppf + CHIF)[:, None, :], (ppf + CLOF)[:, None, :] - hi[None, j:j + 16]).max(axis=2)
        ok &= ~np.any(g < -1e-9, axis=1)
    return True, list(np.where(ok)[0])
def try_place(p, ci, placed, Pc, Prad):
    """the 24 copies of candidate ci at anchor p, if they all fit (exact); halves only flat on a mirror of the 24"""
    C = CANDS[ci]; sh = shapes[C['si']]; W = [vadd(p, w) for w in C['Wk']]
    copies = [body_of(Wc) for Wc in orbit(W, TH)]
    if 'cut' in sh:
        n, c = sh['cut']; q0 = vadd(p, vsub(c, sh['W'][C['k']])); k2 = qm((Fr(2), Fr(0)), qinv(dot(n, n)))
        twin = np.array([vf(vsub(v, vmul(n, qm(dot(n, vsub(v, q0)), k2)))) for v in W])
        if okey(twin) not in {okey(np.array([vf(w) for w in B['W']])) for B in copies}: return None
    tmp, tPc, tPr = list(placed), Pc, Prad
    for B in copies:
        if collides(B, tmp, tPc, tPr): return None
        tmp.append(B); tPc = np.vstack([tPc, B['cen']]); tPr = np.r_[tPr, B['rad']]
    for B in copies: B['ci'] = ci
    return copies
rng = random.Random(SEED); t0 = time.time()
placed = []; Pc = np.zeros((0, 3)); Prad = np.zeros(0); anchors = {}
for p in CORN: anchors[tuple(np.round(vf(p), 9))] = p
vol = Z; cvol = 0.0; cache = {}; stack = []; nodes = 0; backs = 0; best = (0.0, None)
def options(ak):
    if ak not in cache: cache[ak] = status(anchors[ak], placed, Pc, Prad)
    return cache[ak]
def pick():
    """the open gap with the fewest options; (key, opts) or (None, None) when no gap is open; opts == [] means a dead end"""
    bestk, besto = None, None
    for ak in list(anchors):
        op, opts = options(ak)
        if not op: continue
        if not opts: return ak, []
        if besto is None or len(opts) < len(besto): bestk, besto = ak, opts
    return bestk, besto
def order(opts):
    sc = []
    for ci in opts:
        pv = shapes[CANDS[ci]['si']]['vol']; n_ = 24
        sc.append((round(abs(cvol + n_ * cj(pv) - CGPV * (qf(vol) + n_ * qf(pv)) / FGPV), 9), -CSZ[ci], rng.random(), ci))
    return [x[-1] for x in sorted(sc)]
def apply_(copies):
    global placed, Pc, Prad, vol, cvol
    new = []; changed = {}
    for B in copies:
        placed.append(B); Pc = np.vstack([Pc, B['cen']]); Prad = np.r_[Prad, B['rad']]
        vol = qa(vol, shapes[CANDS[B['ci']]['si']]['vol']); cvol += cj(shapes[CANDS[B['ci']]['si']]['vol'])
        for w in B['W']:
            r = red(w); kk = tuple(np.round(vf(r), 9))
            if kk not in anchors: anchors[kk] = r; new.append(kk)
    cen = np.array([B['cen'] for B in copies]); rmax = max(B['rad'] for B in copies)
    for ak in list(cache):
        af = np.array(ak)
        if np.min(np.linalg.norm(af[None, None, :] - cen[:, None, :] - LATTf[None, :, :], axis=2)) < rmax + REACH + 1e-6: changed[ak] = cache.pop(ak)
    return new, changed, cen, rmax
def undo(n_before, new, changed, vol_b, cvol_b, cen, rmax):
    global placed, Pc, Prad, vol, cvol
    placed = placed[:n_before]; Pc = Pc[:n_before]; Prad = Prad[:n_before]; vol = vol_b; cvol = cvol_b
    for kk in new: anchors.pop(kk, None); cache.pop(kk, None)
    for ak in list(cache):   # every gap near the undone copies goes back to its old state (or is worked out again)
        if ak not in anchors or np.min(np.linalg.norm(np.array(ak)[None, None, :] - cen[:, None, :] - LATTf[None, :, :], axis=2)) < rmax + REACH + 1e-6: cache.pop(ak)
    cache.update(changed)
def save(tag):
    json.dump(dict(mark='DICTO · dictospheres.com', mode=MODE, seed=SEED, tag=tag, fill_float=qf(vol) / qf(GPV), volume_exact=f'{vol[0]}|{vol[1]}',
                   nodes=nodes, backtracks=backs, seconds=time.time() - t0, counts=counts(),
                   bodies=[dict(kind=shapes[CANDS[B['ci']]['si']]['kind'], vertices=[[f'{x[0]}|{x[1]}' for x in w] for w in B['W']]) for B in placed]), open(OUT, 'w'))
def counts():
    c = {}
    for B in placed:
        sh = shapes[CANDS[B['ci']]['si']]; k = f"{sh['kind']} {qf(sh['size']) / qf(lam):.3f} lam"; c[k] = c.get(k, 0) + 1
    return c
# depth-first: each frame = (anchor, ordered options, next index, undo record of the option in place)
ak, opts = pick(); done = ak is None
if not done: stack.append([ak, order(opts), 0, None])
while stack and not done and nodes < NODES and time.time() - t0 < HOURS * 3600:
    fr = stack[-1]
    if fr[3] is not None: undo(*fr[3]); fr[3] = None
    placedit = False
    while fr[2] < len(fr[1]):
        ci = fr[1][fr[2]]; fr[2] += 1
        copies = try_place(anchors[fr[0]], ci, placed, Pc, Prad)
        if copies is None: continue
        rec = (len(placed), None, None, vol, cvol); new, changed, cen, rmax = apply_(copies); fr[3] = (rec[0], new, changed, rec[3], rec[4], cen, rmax); nodes += 1; placedit = True
        f = qf(vol) / qf(GPV)
        if f > best[0] + 1e-9:
            best = (f, len(placed)); save('best')
            print(json.dumps(dict(best_fill=f, tiles=len(placed), depth=len(stack), nodes=nodes, backtracks=backs, sec=round(time.time() - t0), counts=counts())), flush=True)
        break
    if not placedit:
        stack.pop(); backs += 1
        if backs % 200 == 0: print(json.dumps(dict(backtracks=backs, nodes=nodes, depth=len(stack), sec=round(time.time() - t0))), flush=True)
        continue
    ak, opts = pick()
    if ak is None: done = True; break
    stack.append([ak, order(opts) if opts else [], 0, None])
print(json.dumps(dict(finished=bool(done), complete_fill=bool(done), best_fill=best[0], nodes=nodes, backtracks=backs, sec=round(time.time() - t0))), flush=True)
if done: save('complete')
