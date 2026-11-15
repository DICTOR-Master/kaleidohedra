"""2D curvature-driven grain growth on a torus: a curved-boundary vertex (front-tracking) model.
GRAINS stream of "One tissue, three scales" (DICTO, 15 Nov 2026: "metamorphic rocks and mineral aggregates, polycrystalline materials").

Physics: every grain boundary moves with normal velocity = mobility x tension x curvature (Mullins 1956; M = gamma = 1); triple
junctions are free. In 2D this gives the von Neumann-Mullins law dA/dt = (pi/3)(n - 6) (von Neumann 1952; Mullins 1956), which is
measured in every run (internal control).
Scheme (the virtual-vertex idea of Weygand, Brechet & Lepinoux, Phil. Mag. B 78 (1998) 329, and of Kawasaki-type vertex models;
the code is written here from scratch): each boundary is a polyline with K interior points; an interior point moves with the
discrete curvature vector 2(t+ - t-)/(l- + l+); a triple junction moves with 2 (sum of its three unit tangents) / (sum of its three
segment lengths); interior points are re-spaced to equal arc length. Topological events are explicit and exact:
  T1 (swap): a boundary shorter than delta is replaced by a perpendicular one of length 2 delta (hysteresis);
  T2 (death): a three-sided grain with area < amin <A>, or with a side shorter than delta, shrinks to a point;
  lens: a two-sided grain (made only by a neighbour's T2) closes; logged separately (expected rare).
delta = eps <boundary length>, so the rule scales with the structure. Boundaries shorter than lamf*delta (default 4) are kept
straight (junctions feel the chord), which keeps the time step near delta^2.
Output (OUTDIR): frames.jsonl (logger format, surface "patch", junctions given; one frame each time rec_frac*N events have
happened), events.jsonl (exact event list), stats.jsonl (per-frame statistics), final.json (von Neumann regression, sides of
vanishing grains at fixed small areas, anomalies, status).
Usage: vertex2d.py OUTDIR N0=10000 Nend=1000 K=3 eps=0.05 amin=0.002 seed=1 rec_frac=0.005 maxwall=SECONDS frames=1"""
import sys, os, json, time, math
import numpy as np
from scipy.spatial import Voronoi

args = dict(a.split('=') for a in sys.argv[2:])
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
N0 = int(args.get('N0', 10000)); NEND = int(args.get('Nend', 1000)); K = int(args.get('K', 3))
EPS = float(args.get('eps', 0.05)); AMIN = float(args.get('amin', 0.002)); SEED = int(args.get('seed', 1))
REC = float(args.get('rec_frac', 0.005)); MAXWALL = float(args.get('maxwall', 1e9)); CFL = float(args.get('cfl', 0.15))
RESAMPLE = int(args.get('resample', 2)); LAMF = float(args.get('lamf', 4.0)); WRITE_FRAMES = int(args.get('frames', 1))
THR = (0.02, 0.05, 0.1, 0.2)                      # fixed small areas (fractions of <A>) at which a shrinking grain's sides are read
rng = np.random.default_rng(SEED)
L = math.sqrt(N0)
T0 = time.time()

def mi(d):                                         # minimum image
    return d - L * np.round(d / L)

# ---------------------------------------------------------------- initial periodic Voronoi (9 images)
pts = rng.random((N0, 2)) * L
shifts = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
imgs = np.concatenate([pts + L * np.array(s) for s in shifts])
c0 = shifts.index((0, 0)) * N0
vor = Voronoi(imgs)
own = np.arange(len(imgs)) % N0
vpts = {}
for (i, j), rv in zip(vor.ridge_points, vor.ridge_vertices):
    for v in rv:
        if v >= 0: vpts.setdefault(v, set()).update((own[i], own[j]))
tjkey, tjpos = {}, []
def tjid(v):
    k = tuple(sorted(vpts[v]))
    if k not in tjkey: tjkey[k] = len(tjpos); tjpos.append(np.mod(vor.vertices[v], L))
    return tjkey[k]
B_t, B_g, B_P = [], [], []
for (i, j), rv in zip(vor.ridge_points, vor.ridge_vertices):
    if -1 in rv: continue
    v0, v1 = vor.vertices[rv[0]], vor.vertices[rv[1]]
    m = (v0 + v1) / 2
    if not (0 <= m[0] < L and 0 <= m[1] < L): continue
    d = v1 - v0
    left = i if d[0] * (imgs[i][1] - v0[1]) - d[1] * (imgs[i][0] - v0[0]) > 0 else j
    right = j if left == i else i
    B_t.append((tjid(rv[0]), tjid(rv[1]))); B_g.append((own[left], own[right]))
    B_P.append(v0[None, :] + np.linspace(0, 1, K + 2)[:, None] * d[None, :])
bt = np.array(B_t, dtype=np.int64); bg = np.array(B_g, dtype=np.int64); P = np.array(B_P)
tj = np.array(tjpos); nB, nT = len(bt), len(tj)
balive = np.ones(nB, bool); talive = np.ones(nT, bool); galive = np.ones(N0, bool)
assert nT == 2 * N0 and nB == 3 * N0, (nT, nB, N0)     # torus Euler with all junctions triple
deg = np.bincount(bt.ravel(), minlength=nT); assert (deg == 3).all()

def inc(t):
    return np.nonzero(balive & ((bt[:, 0] == t) | (bt[:, 1] == t)))[0]
def gbound(g):
    return np.nonzero(balive & ((bg[:, 0] == g) | (bg[:, 1] == g)))[0]
def nsides_of(g):
    return len(gbound(g))
def other(b, g):
    return bg[b, 1] if bg[b, 0] == g else bg[b, 0]

def resample_rows(Q):                              # Q (n, m, 2) -> (n, K+2, 2) equal arc length, ends kept
    S = np.diff(Q, axis=1); ls = np.sqrt((S ** 2).sum(-1)) + 1e-300
    c = np.concatenate([np.zeros((len(Q), 1)), np.cumsum(ls, 1)], 1)
    s = c[:, -1:] * (np.arange(1, K + 1) / (K + 1))[None, :]
    idx = np.clip((c[:, :, None] <= s[:, None, :]).sum(1) - 1, 0, Q.shape[1] - 2)
    r = np.arange(len(Q))[:, None]
    f = (s - c[r, idx]) / ls[r, idx]
    mid = Q[r, idx] + f[..., None] * S[r, idx]
    return np.concatenate([Q[:, :1], mid, Q[:, -1:]], 1)

def set_ends():
    P[:, 0] = P[:, 1] + mi(tj[bt[:, 0]] - P[:, 1])
    P[:, K + 1] = P[:, K] + mi(tj[bt[:, 1]] - P[:, K])

def areas():
    ab = np.nonzero(balive)[0]
    ref = np.zeros((N0, 2)); ref[bg[ab, 0]] = P[ab, 0]; ref[bg[ab, 1]] = P[ab, 0]
    A = np.zeros(N0)
    for s, sign in ((0, 1.0), (1, -1.0)):
        g = bg[ab, s]; Q = mi(P[ab] - ref[g][:, None, :])
        cr = (Q[:, :-1, 0] * Q[:, 1:, 1] - Q[:, :-1, 1] * Q[:, 1:, 0]).sum(1) / 2
        A += sign * np.bincount(g, cr, minlength=N0)
    return A

events, anomalies = [], {'T1 R==S': 0, 'T2 shared outer': 0, 'lens X==Y': 0, 'lens loop': 0, 'one-sided': 0}
touched = set()
t = 0.0

def T2(G, Ab, A):
    bs = gbound(G)
    if len(bs) != 3: return False
    tset = sorted({int(x) for x in bt[bs].ravel()})
    if len(tset) != 3: anomalies['T2 shared outer'] += 1; return False
    outer = {}
    for ti in tset:
        o = [b for b in inc(ti) if b not in bs]
        if len(o) != 1: anomalies['T2 shared outer'] += 1; return False
        outer[ti] = o[0]
    if len({outer[x] for x in tset}) != 3 or any(bt[outer[x], 0] in tset and bt[outer[x], 1] in tset for x in tset):
        anomalies['T2 shared outer'] += 1; return False
    nb = sorted({int(other(b, G)) for b in bs})
    t1 = tset[0]
    cen = tj[t1] + (mi(tj[tset[1]] - tj[t1]) + mi(tj[tset[2]] - tj[t1])) / 3
    tj[t1] = np.mod(cen, L)
    for ti in tset[1:]:
        o = outer[ti]; e = 0 if bt[o, 0] == ti else 1; bt[o, e] = t1; talive[ti] = False
    balive[bs] = False; galive[G] = False
    events.append([t, 'T2', int(G), *nb, float(A[G]), Ab]); touched.update([int(G), *nb])
    return True

def lens(H):
    bs = gbound(H)
    if len(bs) != 2: anomalies['one-sided'] += 1; return False
    x, y = bs; X, Y = other(x, H), other(y, H)
    if X == Y: anomalies['lens X==Y'] += 1; return False
    u, v = bt[x]
    zu = [b for b in inc(u) if b not in bs]; zv = [b for b in inc(v) if b not in bs]
    if len(zu) != 1 or len(zv) != 1 or zu[0] == zv[0]: anomalies['lens loop'] += 1; return False
    zu, zv = zu[0], zv[0]
    Qu = P[zu] if bt[zu, 1] == u else P[zu][::-1]          # oriented ending at u
    gu = bg[zu] if bt[zu, 1] == u else bg[zu][::-1]
    w1 = bt[zu, 0] if bt[zu, 1] == u else bt[zu, 1]
    Qv = P[zv] if bt[zv, 0] == v else P[zv][::-1]          # oriented starting at v
    w2 = bt[zv, 1] if bt[zv, 0] == v else bt[zv, 0]
    if w1 == w2: anomalies['lens loop'] += 1; return False
    Qv = Qv - Qv[0] + Qu[-1] + mi(tj[v] - tj[u])
    Q = np.concatenate([Qu, Qv])[None]
    P[zu] = resample_rows(Q)[0]; bt[zu] = (w1, w2); bg[zu] = gu
    balive[[x, y, zv]] = False; talive[[u, v]] = False; galive[H] = False
    events.append([t, 'lens', int(H), int(X), int(Y)]); touched.update([int(H), int(X), int(Y)])
    return True

def T1(b, delta, Ab, A):
    a, c = bt[b]; Pg, Qg = bg[b]
    ia = [x for x in inc(a) if x != b]; ic = [x for x in inc(c) if x != b]
    if len(ia) != 2 or len(ic) != 2: return False
    baP = [x for x in ia if Pg in bg[x]]; baQ = [x for x in ia if Qg in bg[x]]
    bcP = [x for x in ic if Pg in bg[x]]; bcQ = [x for x in ic if Qg in bg[x]]
    if not (len(baP) == len(baQ) == len(bcP) == len(bcQ) == 1): return False
    baP, baQ, bcP, bcQ = baP[0], baQ[0], bcP[0], bcQ[0]
    R = other(baP, Pg); S = other(bcP, Pg)
    if R == S or R in (Pg, Qg) or S in (Pg, Qg): anomalies['T1 R==S'] += 1; return False
    pa = tj[a]; pc = pa + mi(tj[c] - pa); m = (pa + pc) / 2; d = pc - pa
    nd = np.hypot(*d)
    d = d / nd if nd > 1e-12 else np.array([1.0, 0.0])
    n = np.array([-d[1], d[0]])                     # left of a->c: the P side
    h = delta
    pa2, pc2 = m + n * h, m - n * h
    tj[a] = np.mod(pa2, L); tj[c] = np.mod(pc2, L)
    e = 0 if bt[bcP, 0] == c else 1; bt[bcP, e] = a
    e = 0 if bt[baQ, 0] == a else 1; bt[baQ, e] = c
    bt[b] = (a, c); bg[b] = (S, R)
    P[b] = pa2[None, :] + np.linspace(0, 1, K + 2)[:, None] * (pc2 - pa2)[None, :]
    events.append([t, 'T1', int(Pg), int(Qg), int(R), int(S), float(A[Pg]), float(A[Qg]), Ab])
    touched.update([int(Pg), int(Qg), int(R), int(S)])
    return True

def topology(delta, Ab, A):
    ab = np.nonzero(balive)[0]
    S = np.diff(P[ab], axis=1); blen = np.sqrt((S ** 2).sum(-1)).sum(1)
    short = ab[np.argsort(blen)][: (blen < delta).sum()]
    ns = np.bincount(bg[ab].ravel(), minlength=N0)
    small3 = np.nonzero(galive & (ns == 3) & (A < AMIN * Ab))[0]
    for G in small3:
        if galive[G] and nsides_of(G) == 3: T2(G, Ab, A); cascade()
    for b in short:
        if not balive[b]: continue
        Sb = np.diff(P[b], axis=0); lb = np.sqrt((Sb ** 2).sum(-1)).sum()
        if lb >= delta: continue
        Pg, Qg = bg[b]; nP, nQ = nsides_of(Pg), nsides_of(Qg)
        if nP <= 3 or nQ <= 3:
            G = Pg if (nP <= 3 and (nQ > 3 or A[Pg] <= A[Qg])) else Qg
            T2(G, Ab, A); cascade()
        else:
            T1(b, delta, Ab, A)

def cascade():
    while True:
        ab = np.nonzero(balive)[0]
        ns = np.bincount(bg[ab].ravel(), minlength=N0)
        bad = np.nonzero(galive & (ns <= 2))[0]
        if not len(bad): return
        done = False
        for H in bad:
            if ns[H] == 2: done |= lens(H)
            else: anomalies['one-sided'] += 1; galive[H] = False; done = True
        if not done: return

# ---------------------------------------------------------------- recording
ffr = open(os.path.join(OUT, 'frames.jsonl'), 'w') if WRITE_FRAMES else None
fst = open(os.path.join(OUT, 'stats.jsonl'), 'w')
vn = {}                                            # n -> [count, sum dA/dt, sum sq]
prev = None
small_sides = {th: {} for th in THR}               # threshold -> grain -> sides when area first fell below th*<A>
nframes = 0
euler_fail = 0

def record(A):
    global prev, nframes, euler_fail
    ab = np.nonzero(balive)[0]; at = np.nonzero(talive)[0]; ag = np.nonzero(galive)[0]
    ns = np.bincount(bg[ab].ravel(), minlength=N0)
    chi = len(at) - len(ab) + len(ag)
    if chi != 0: euler_fail += 1
    # junctions: grains round each triple junction
    tt = np.concatenate([bt[ab, 0], bt[ab, 0], bt[ab, 1], bt[ab, 1]])
    gg = np.concatenate([bg[ab, 0], bg[ab, 1], bg[ab, 0], bg[ab, 1]])
    key = np.unique(tt * (N0 + 1) + gg); jt, jg = key // (N0 + 1), key % (N0 + 1)
    cnt = np.bincount(jt, minlength=len(talive))
    trip = (cnt[at] == 3).all()
    if ffr is not None:
        order = np.argsort(jt, kind='stable'); jg2 = jg[order].reshape(-1, 3) if trip else None
        fr = dict(t=round(t, 9), dim=2, surface='patch', cells=[str(g) for g in ag],
                  boundaries=[[str(x), str(y)] for x, y in bg[ab]])
        if trip: fr['junctions'] = [[str(x) for x in r] for r in jg2]
        ffr.write(json.dumps(fr) + '\n')
    n = ns[ag]; Ab = A[ag].mean()
    pn = np.bincount(n, minlength=16)[:16] / len(ag)
    lewis = {int(k): float(A[ag][n == k].mean() / Ab) for k in range(3, 13) if (n == k).sum() >= 5}
    # Aboav: mean sides of the neighbours of n-sided grains
    sn = np.bincount(bg[ab, 0], ns[bg[ab, 1]], minlength=N0) + np.bincount(bg[ab, 1], ns[bg[ab, 0]], minlength=N0)
    m = sn[ag] / np.maximum(n, 1)
    aboav = {int(k): float(m[n == k].mean()) for k in range(3, 13) if (n == k).sum() >= 5}
    st = dict(t=t, N=int(len(ag)), Abar=float(Ab), mean_n=float(n.mean()), mu2=float(((n - 6.0) ** 2).mean()),
              p=[float(x) for x in pn], lewis=lewis, aboav=aboav, euler=int(chi), all_triple=bool(trip),
              events=len(events), wall=time.time() - T0)
    fst.write(json.dumps(st) + '\n'); fst.flush()
    if prev is not None:
        tp, Ap, nsp = prev
        dt_ = t - tp
        if dt_ > 0:
            ok = galive & (nsp == ns) & (Ap > 0)
            for g in np.nonzero(ok)[0]:
                if int(g) in touched: continue
                r = (A[g] - Ap[g]) / dt_; k = int(ns[g])
                s = vn.setdefault(k, [0, 0.0, 0.0]); s[0] += 1; s[1] += r; s[2] += r * r
    touched.clear()
    prev = (t, A.copy(), ns.copy())
    nframes += 1

# ---------------------------------------------------------------- main loop
step = 0; last_rec_events = -1; status = 'running'
set_ends()
A = areas(); record(A); last_rec_events = 0
next_prog = time.time()
while True:
    ag = galive.sum()
    if ag <= NEND: status = 'done'; break
    if time.time() - T0 > MAXWALL: status = 'maxwall'; break
    set_ends()
    ab = np.nonzero(balive)[0]
    Pa = P[ab]
    S = np.diff(Pa, axis=1); ls = np.sqrt((S ** 2).sum(-1)); U = S / ls[..., None]
    vint = 2 * (U[:, 1:] - U[:, :-1]) / (ls[:, 1:, None] + ls[:, :-1, None])
    # short boundaries (length < LAMF * delta) are kept straight: their junctions feel the chord, and their interior points are
    # placed on it; this keeps the time step at about delta^2 instead of (delta/(K+1))^2
    blen = ls.sum(1); lbar = blen.mean(); sh = blen < LAMF * EPS * lbar
    if sh.any():
        ch = Pa[sh, -1] - Pa[sh, 0]; cl = np.sqrt((ch ** 2).sum(-1)) + 1e-300; cu = ch / cl[:, None]
        U[sh, 0] = cu; U[sh, -1] = cu; ls[sh, 0] = cl; ls[sh, -1] = cl; vint[sh] = 0
    F = np.zeros_like(tj); W = np.zeros(len(tj))
    np.add.at(F, bt[ab, 0], U[:, 0]); np.add.at(F, bt[ab, 1], -U[:, -1])
    np.add.at(W, bt[ab, 0], ls[:, 0]); np.add.at(W, bt[ab, 1], ls[:, -1])
    vt = 2 * F / np.maximum(W, 1e-300)[:, None]
    dt = CFL * min(ls[~sh].min() if (~sh).any() else np.inf, ls[sh, 0].min() if sh.any() else np.inf) ** 2
    P[ab, 1:K + 1] += dt * vint
    tj[talive] = np.mod(tj[talive] + dt * vt[talive], L)
    t += dt; step += 1
    set_ends()
    if sh.any():
        abs_ = ab[sh]; P[abs_] = P[abs_, :1] + np.linspace(0, 1, K + 2)[None, :, None] * (P[abs_, -1:] - P[abs_, :1])
    if step % RESAMPLE == 0:
        P[ab] = resample_rows(P[ab])
        P[ab] -= L * np.round((P[ab, 1:2] - tj[bt[ab, 0]][:, None, :]) / L)   # keep each polyline near its start junction
        set_ends()
    A = areas(); Ab = A[galive].mean()
    for th in THR:
        dct = small_sides[th]
        cand = np.nonzero(galive & (A < th * Ab))[0]
        if len(cand):
            nsall = np.bincount(bg[balive].ravel(), minlength=N0)
            for g in cand:
                if int(g) not in dct: dct[int(g)] = int(nsall[g])
    ne = len(events)
    topology(EPS * lbar, float(Ab), A)
    if len(events) - last_rec_events >= max(1, REC * ag):
        A = areas(); record(A); last_rec_events = len(events)
    if time.time() > next_prog:
        print(f'PROGRESS {math.log(N0 / ag) / math.log(N0 / NEND):.3f} N={ag} t={t:.4f} step={step} events={len(events)}', flush=True)
        next_prog = time.time() + 30
A = areas(); record(A)
if ffr: ffr.close()
fst.close()
with open(os.path.join(OUT, 'events.jsonl'), 'w') as f:
    for e in events: f.write(json.dumps(e) + '\n')
vnt = {k: dict(count=v[0], mean=v[1] / v[0], sd=math.sqrt(max(v[2] / v[0] - (v[1] / v[0]) ** 2, 0))) for k, v in sorted(vn.items()) if v[0] >= 20}
ks = np.array([k for k in vnt]); ys = np.array([vnt[k]['mean'] for k in ks]); ws = np.array([vnt[k]['count'] for k in ks])
slope, icpt = np.polyfit(ks, ys, 1, w=np.sqrt(ws)) if len(ks) >= 3 else (float('nan'), float('nan'))
ss = {}
for th, d in small_sides.items():
    bc = np.bincount(list(d.values()), minlength=8) if d else np.zeros(8, int)
    ss[str(th)] = {str(i): int(c) for i, c in enumerate(bc) if c}
cnt = {}
for e in events: cnt[e[1]] = cnt.get(e[1], 0) + 1
fin = dict(params=dict(N0=N0, Nend=NEND, K=K, eps=EPS, lamf=LAMF, amin=AMIN, seed=SEED, rec_frac=REC, cfl=CFL, resample=RESAMPLE),
           status=status, t=t, steps=step, N=int(galive.sum()), frames=nframes, euler_failures=euler_fail, events=cnt,
           anomalies=anomalies, von_neumann=dict(per_n=vnt, slope=float(slope), n0=float(-icpt / slope) if slope else None,
                                                expected_slope=math.pi / 3),
           sides_at_small_area=ss, wall=time.time() - T0)
json.dump(fin, open(os.path.join(OUT, 'final.json'), 'w'), indent=1)
print('VERTEX2D', status, json.dumps(dict(N=fin['N'], events=cnt, vn_slope=fin['von_neumann']['slope'], euler_fail=euler_fail,
                                           anomalies=anomalies)))
