# DICTO · dictospheres.com — Fable pass 5: systematic local backtracking (large-neighbourhood search) on G'
# usage: python3 gbpc_lns.py SEED_JSON SEED OUT.json DEADLINE_EPOCH
# Loads a periodic build (e.g. RB-22), then repeats: remove every body within a random ball (local backtrack),
# refill the hole with a beam of K randomised exhaustive greedy refills (largest volume first), keep the best
# refill if its exact volume is >= the removed volume. Every placement uses the exact separating-axis test of
# gbpc_search.py (15 golden normals + edge cross products, ties decided in Q(sqrt5)). Mode RB (rhombohedra lam, lam/2, lam/4 + Bodhi).
import sys, os, json, time, random
SEEDJ, SEEDN, OUTJ, DEADLINE = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gbpc_search.py')).read().split('def run(rng, staged):')[0]
sys.argv = ['gbpc_search.py', 'RB', str(SEEDN), '1', OUTJ]
exec(src)
VOLK = {(sh['kind'], sh['size']): sh['vol'] for sh in shapes}
SIK = {}
for si, sh in enumerate(shapes): SIK.setdefault((sh['kind'], sh['size']), si)
def mkbody(V, si, p):
    lo, hi, lof, hif = proj(V); cen = np.mean([vf(w) for w in V], 0)
    return dict(lo=lo, hi=hi, lof=lof, hif=hif, cen=cen, rad=max(np.linalg.norm(vf(w) - cen) for w in V), si=si, p=p, V=V)
D = json.load(open(SEEDJ))
placed = []
for b in D['bodies']:
    V = [tuple(q(x) for x in w) for w in b['vertices']]; si = SIK[(b['kind'], q(b['size']))]
    placed.append(mkbody(V, si, V[0]))
vol = Z
for B in placed: vol = qa(vol, shapes[B['si']]['vol'])
rt_lo = [[qa(rlo[a], TP[i][a]) for a in range(NA)] for i in range(len(LATT))]
rt_hi = [[qa(rhi[a], TP[i][a]) for a in range(NA)] for i in range(len(LATT))]
def near(pf, bodies, Pc, Prad, extra):
    if not len(bodies): return []
    Dd = np.linalg.norm(pf[None, None, :] - Pc[:, None, :] - LATTf[None, :, :], axis=2)
    return list(zip(*np.where(Dd < extra + Prad[:, None])))
def feasible(p, bodies, Pc, Prad, sizes):
    pf = vf(p); pp = [dot(n, p) for n in AXES]; ppf = np.array([qf(x) for x in pp])
    rt_ids = [i for i, cf in enumerate(LATTf) if np.linalg.norm(pf - cf) < REACH + RTrad]
    pl_ids = near(pf, bodies, Pc, Prad, REACH)
    Blo = np.array([rlof + TPf[i] for i in rt_ids] + [bodies[b]['lof'] + TPf[t] for b, t in pl_ids])
    Bhi = np.array([rhif + TPf[i] for i in rt_ids] + [bodies[b]['hif'] + TPf[t] for b, t in pl_ids])
    ids = [('rt', i) for i in rt_ids] + [('pl', b, t) for b, t in pl_ids]
    out = []
    for ci, C in enumerate(CANDS):
        if qf(shapes[C['si']]['size']) not in sizes: continue
        clo = ppf + C['lof']; chi = ppf + C['hif']
        g = np.maximum(Blo - chi[None, :], clo[None, :] - Bhi); gm = g.max(axis=1)
        if np.any(gm < -1e-9): continue
        ok = True
        for bi in np.where(np.abs(gm) <= 1e-9)[0]:
            idd = ids[bi]
            if idd[0] == 'rt': blo, bhi = rt_lo[idd[1]], rt_hi[idd[1]]
            else:
                B = bodies[idd[1]]; blo = [qa(B['lo'][a], TP[idd[2]][a]) for a in range(NA)]; bhi = [qa(B['hi'][a], TP[idd[2]][a]) for a in range(NA)]
            if not any(qsgn(qs(blo[a], qa(pp[a], C['hi'][a]))) >= 0 or qsgn(qs(qa(pp[a], C['lo'][a]), bhi[a])) >= 0
                       for a in np.where(g[bi] >= -1e-9)[0]): ok = False; break
        if ok: out.append((qf(shapes[C['si']]['vol']), int(np.sum(np.abs(g) <= 1e-9)), ci))
    return out
def arrays(bodies):
    return (np.array([B['cen'] for B in bodies]).reshape(-1, 3), np.array([B['rad'] for B in bodies]))
def refill(kept, anchors, rng):
    bodies = list(kept); Pc, Prad = arrays(bodies); added = []; addvol = Z
    pending = list(anchors.keys()); rng.shuffle(pending); tries = {}
    allsz = set(order_size)
    while pending:
        ak = pending.pop(); p = anchors[ak]
        fits = feasible(p, bodies, Pc, Prad, allsz)
        if not fits: continue
        # largest volume first; among those, a randomised pick weighted to more contacts
        vmax = max(f[0] for f in fits); top = [f for f in fits if f[0] > vmax - 1e-12]
        top.sort(key=lambda f: -f[1] - 2 * rng.random()); C = CANDS[top[0][2]]
        V = [vadd(p, w) for w in C['Wk']]; B = mkbody(V, C['si'], p)
        bodies.append(B); added.append(B); Pc = np.vstack([Pc, B['cen']]); Prad = np.r_[Prad, B['rad']]
        addvol = qa(addvol, shapes[C['si']]['vol'])
        for w in V:
            r = red(w); k = tuple(np.round(vf(r), 9))
            if k not in anchors: anchors[k] = r; pending.insert(rng.randrange(len(pending) + 1), k)
        pending.append(ak)
    return added, addvol
def dump(path):
    res = dict(mark='DICTO · dictospheres.com', mode='RB-LNS', seed_file=os.path.basename(SEEDJ), seed=SEEDN,
               fill_float=qf(vol) / qf(GPV), volume_exact=f'{vol[0]}|{vol[1]}', gap_volume_exact=f'{qs(GPV, vol)[0]}|{qs(GPV, vol)[1]}',
               counts=counts(), bodies=[dict(kind=shapes[B['si']]['kind'], size=f"{shapes[B['si']]['size'][0]}|{shapes[B['si']]['size'][1]}",
                       vertices=[[f'{x[0]}|{x[1]}' for x in w] for w in B['V']]) for B in placed])
    json.dump(res, open(path + '.tmp', 'w')); os.replace(path + '.tmp', path)
def counts():
    c = {}
    for B in placed:
        sh = shapes[B['si']]; k = f"{sh['kind']} {qf(sh['size']) / qf(lam):.4f} lam"; c[k] = c.get(k, 0) + 1
    return c
rng = random.Random(SEEDN); K = 4; it = 0; acc = 0; t0 = time.time()
print(json.dumps(dict(start=True, bodies=len(placed), fill=qf(vol) / qf(GPV))), flush=True)
while time.time() < DEADLINE:
    it += 1; ts = time.time()
    Pc, Prad = arrays(placed)
    # ball centre: a random body vertex (reduced), radius 0.5..1.2 x REACH
    B0 = rng.choice(placed); c = red(rng.choice(B0['V'])); cf = vf(c); R = rng.uniform(0.5, 1.2) * REACH
    rem = {b for b, t in near(cf, placed, Pc, np.zeros(len(placed)), R)}
    kept = [B for i, B in enumerate(placed) if i not in rem]
    remvol = Z
    for i in rem: remvol = qa(remvol, shapes[placed[i]['si']]['vol'])
    anchors = {}
    for p in CORN:
        if np.linalg.norm(vf(p) - cf) < R + 2 * REACH: anchors[tuple(np.round(vf(p), 9))] = p
    for i in rem:
        for w in placed[i]['V']: r = red(w); anchors[tuple(np.round(vf(r), 9))] = r
    Kc, Kr = arrays(kept)
    for b, t in near(cf, kept, Kc, Kr, R + REACH):
        for w in kept[b]['V']: r = red(w); anchors[tuple(np.round(vf(r), 9))] = r
    best = None
    for k in range(K):
        added, addvol = refill(kept, dict(anchors), rng)
        if best is None or qsgn(qs(addvol, best[1])) > 0: best = (added, addvol)
    d = qs(best[1], remvol); s = qsgn(d)
    if s >= 0:
        placed = kept + best[0]; vol = qa(qs(vol, remvol), best[1]); acc += 1
        if s > 0: dump(OUTJ)
    print(json.dumps(dict(it=it, removed=len(rem), added=len(best[0]), delta=qf(d), accepted=s >= 0, fill=qf(vol) / qf(GPV),
                          bodies=len(placed), sec=round(time.time() - ts, 1))), flush=True)
dump(OUTJ)
print(json.dumps(dict(done=True, iterations=it, accepted=acc, fill=qf(vol) / qf(GPV), gap_exact=f'{qs(GPV, vol)[0]}|{qs(GPV, vol)[1]}', counts=counts())), flush=True)
