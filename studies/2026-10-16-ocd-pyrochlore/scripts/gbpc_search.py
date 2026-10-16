# Fable, GBPC pass 4 (2026-10-16): exact fill search for G' (golden region minus the 24 GBPCs per bcc cell), numpy + fractions only,
# so it runs on dicto-node. Input: data/gbpc-geom-exact.json (gbpc_export.py). Numbers a + b*sqrt5 are pairs of Fractions.
# Bodies: the uncut RTs on the bcc sites (G' = space minus their union, pass 1), golden rhombohedra (edges along five-fold axes),
# optionally the five Bodhi pieces. Overlap test: separating axes = all face normals and all cross products of edge directions of the
# bodies in play. All edge directions are symmetry axes (checked), so a fixed axis list makes the test exact and complete.
# Every placement is accepted only if, on some axis, the two projections are disjoint or touch EXACTLY (float only prefilters).
# Search: randomised greedy restarts. At each anchor (a corner of G' or of a placed body), try every body, every orientation, and every
# corner of the body at the anchor. Prefer the largest size that fits, then the most face contacts, ties at random. Periodic: each
# placed body stands for its whole lattice orbit.
# usage: python3 gbpc_search.py MODE SEED RESTARTS OUT.json   MODE: R (rhombohedra), RB (plus Bodhi), RX (plus sizes lam/phi, lam/phi^2)
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
MODE = sys.argv[1]; SEED = int(sys.argv[2]); RESTARTS = int(sys.argv[3]); OUT = sys.argv[4]
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
# ---- axes
lines = AX5 + AX3 + AX2
def edges_of(sh):
    if sh['kind'] in ('oblate', 'prolate'): return [AX5[0]]   # five-fold only
    Wf = np.array([vf(v) for v in sh['W']]); E = set()
    for fc in sh['faces']:
        for t in range(len(fc)): E.add(tuple(sorted((fc[t], fc[(t + 1) % len(fc)]))))
    return [vsub(sh['W'][j], sh['W'][i]) for i, j in E]
dirs = list(AX5)
for sh in shapes:
    if sh['kind'] in ('oblate', 'prolate'): continue
    for d in edges_of(sh):
        L = next((l for l in lines if parallel(d, l)), None)
        assert L is not None, 'Bodhi edge not on a symmetry axis'
        if not any(parallel(L, x) for x in dirs): dirs.append(L)
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
def run(rng, staged):
    placed = []   # dict(lo, hi exact lists, lof, hif, cen, rad, ci, p)
    Pc = np.zeros((0, 3)); Prad = np.zeros(0)
    anchors = {}; dead = {}
    for p in CORN: anchors[tuple(np.round(vf(p), 9))] = p
    vol = Z
    stages = [[sz] for sz in order_size] if staged else [order_size]
    for allowed in stages:
      pending = list(anchors.keys()); rng.shuffle(pending)
      while pending:
          ak = pending.pop(); p = anchors[ak]
          pf = vf(p); pp = [dot(n, p) for n in AXES]; ppf = np.array([qf(x) for x in pp])
          # bodies near the anchor: RT translates and placed translates
          reach = REACH
          rt_ids = [i for i, cf in enumerate(LATTf) if np.linalg.norm(pf - cf) < reach + RTrad]
          if len(placed):
              Dd = np.linalg.norm(pf[None, None, :] - Pc[:, None, :] - LATTf[None, :, :], axis=2)
              pl_ids = list(zip(*np.where(Dd < reach + Prad[:, None])))
          else: pl_ids = []
          Blo = np.array([rlof + TPf[i] for i in rt_ids] + [placed[b]['lof'] + TPf[t] for b, t in pl_ids])
          Bhi = np.array([rhif + TPf[i] for i in rt_ids] + [placed[b]['hif'] + TPf[t] for b, t in pl_ids])
          ids = [('rt', i) for i in rt_ids] + [('pl', b, t) for b, t in pl_ids]
          best = None
          for sz in allowed:
              fits = []
              for ci, C in enumerate(CANDS):
                  if abs(qf(shapes[C['si']]['size']) - sz) > 1e-12: continue
                  clo = ppf + C['lof']; chi = ppf + C['hif']
                  g = np.maximum(Blo - chi[None, :], clo[None, :] - Bhi)   # per body, per axis: > 0 means separated on that axis
                  gm = g.max(axis=1)
                  if np.any(gm < -1e-9): continue
                  amb = np.where(np.abs(gm) <= 1e-9)[0]; ok = True
                  for bi in amb:   # exact: some axis with exact touching or separation
                      idd = ids[bi]
                      if idd[0] == 'rt': blo = [qa(rlo[a], TP[idd[1]][a]) for a in range(NA)]; bhi = [qa(rhi[a], TP[idd[1]][a]) for a in range(NA)]
                      else:
                          B = placed[idd[1]]; blo = [qa(B['lo'][a], TP[idd[2]][a]) for a in range(NA)]; bhi = [qa(B['hi'][a], TP[idd[2]][a]) for a in range(NA)]
                      sep = False
                      for a in np.where(g[bi] >= -1e-9)[0]:
                          if qsgn(qs(blo[a], qa(pp[a], C['hi'][a]))) >= 0 or qsgn(qs(qa(pp[a], C['lo'][a]), bhi[a])) >= 0: sep = True; break
                      if not sep: ok = False; break
                  if not ok: continue
                  contacts = int(np.sum(np.abs(g) <= 1e-9))
                  fits.append((contacts, rng.random(), ci))
              if fits: best = max(fits); break
          if best is None: continue
          C = CANDS[best[2]]
          body = dict(lo=[qa(pp[a], C['lo'][a]) for a in range(NA)], hi=[qa(pp[a], C['hi'][a]) for a in range(NA)],
                      lof=ppf + C['lof'], hif=ppf + C['hif'], cen=pf + C['cen'], rad=C['rad'], ci=best[2], p=p)
          placed.append(body); Pc = np.vstack([Pc, body['cen']]); Prad = np.r_[Prad, body['rad']]
          vol = qa(vol, shapes[C['si']]['vol'])
          for w in C['Wk']:
              r = red(vadd(p, w)); k = tuple(np.round(vf(r), 9))
              if k not in anchors: anchors[k] = r; pending.insert(rng.randrange(len(pending) + 1), k)
          pending.append(ak)   # the same anchor may take another body
    return placed, vol
rng = random.Random(SEED); best = None; log = []
for r in range(RESTARTS):
    t0 = time.time(); staged = (r % 2 == 0); placed, vol = run(rng, staged)
    frac = qf(vol) / qf(GPV)
    cnt = {}
    for B in placed:
        sh = shapes[CANDS[B['ci']]['si']]; k = (sh['kind'], f"{qf(sh['size']) / qf(lam):.6f} lam"); cnt[k] = cnt.get(k, 0) + 1
    log.append(dict(restart=r, staged=staged, fill=frac, tiles=len(placed), counts={f'{a} {b}': n for (a, b), n in cnt.items()}, seconds=time.time() - t0))
    print(json.dumps(log[-1]), flush=True)
    if best is None or frac > best[0]: best = (frac, placed, vol, cnt)
frac, placed, vol, cnt = best
res = dict(mark='DICTO · dictospheres.com', mode=MODE, seed=SEED, restarts=log, best_fill_float=frac,
           best_volume_exact=f'{vol[0]}|{vol[1]}', gap_volume_exact=f'{qs(GPV, vol)[0]}|{qs(GPV, vol)[1]}',
           counts={f'{a} {b}': n for (a, b), n in cnt.items()}, n_axes=NA,
           bodies=[dict(kind=shapes[CANDS[B['ci']]['si']]['kind'], size=f"{shapes[CANDS[B['ci']]['si']]['size'][0]}|{shapes[CANDS[B['ci']]['si']]['size'][1]}",
                        vertices=[[f'{x[0]}|{x[1]}' for x in vadd(B['p'], w)] for w in CANDS[B['ci']]['Wk']],
                        faces=shapes[CANDS[B['ci']]['si']].get('faces')) for B in placed])
json.dump(res, open(OUT, 'w'))
print('best', frac, len(placed), cnt)
