# deep4.py (13 Nov 2026, DICTO's one exception to the paused RD hunt: "73 keyed jobs"). Deep check of the 73 keyed-RD classes that
# filled the ball R8 with no torus up to index 64 (hp-ksdeep2, data/ksdeep/e_*.log). No new search, no keying.
# Kill test: SAT on fcc tori of chosen indices above 64 (one torus per O_h orbit of sublattices, as hunt.py), and the balls R10, R12.
# Uses hunt.py's engine unchanged (exec of its part above "modes"); torus orbits are built per index (hunt.py builds all up to imax).
# usage: deep4.py list <ksdeep dir> out.json                   the 73 classes, rebuilt exactly as keysearch.py deep2 split them
#        deep4.py tori <indices, e.g. 65-80,96> out.pkl          torus orbits + neighbour tables (count check per index)
#        deep4.py ctl <classes.json> <heptomino s0.json>         controls (see README section "Deep check of the 73")
#        deep4.py pilot <classes.json> <tori.pkl>                timings: a sample of tori per index, balls R10, R12
#        deep4.py run <classes.json> <t1.pkl,t2.pkl,..> RB SHARD/NSHARDS out.jsonl   tiers; checkpoint per (class, tier), resumable
#        deep4.py struct <classes.json> <out1.jsonl,..> R            describe the ball fillings of the survivors (no claims)
import sys, os, json, time, pickle, re, glob
here = os.path.dirname(os.path.abspath(__file__)); ARGS = sys.argv[1:]
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
def sigma(n): return sum(d for d in range(1, n + 1) if n % d == 0)
def a3(n): return sum(d * sigma(d) for d in range(1, n + 1) if n % d == 0)       # sublattices of index n in Z^3 (independent count)
def orbits_index(n):
    """one representative per O_h orbit of the index-n sublattices of the fcc lattice, with orbit sizes"""
    allt = []
    for a in range(1, n + 1):
        if n % a: continue
        for d in range(1, n // a + 1):
            if (n // a) % d: continue
            f = n // a // d
            for b in range(a):
                for c_ in range(a):
                    for e in range(d): allt.append(((a, 0, 0), (b, d, 0), (c_, e, f)))
    assert len(allt) == a3(n), (n, len(allt), a3(n))
    keys = set(allt); reps = {}
    for M in allt:
        W = np.array(M) @ B3; best = None
        for g in range(48):
            k = hnf(np.rint((W @ np.array(OH[g]).T) @ B3I).astype(int).tolist()); assert k in keys
            if best is None or k < best: best = k
        reps[best] = reps.get(best, 0) + 1
    assert sum(reps.values()) == len(allt)
    return sorted((n, M, c) for M, c in reps.items())
def parse_idx(s):
    out = []
    for part in s.split(','):
        if '-' in part: a, b = map(int, part.split('-')); out += list(range(a, b + 1))
        else: out.append(int(part))
    return out
def ball_fill(F, st, nbr):
    """as sat_fill, but returns the orientation per site (or None)"""
    m = len(st); n = len(nbr); var = lambda i, a: 1 + i * m + a
    Fs = F[np.ix_(st, range(12), st)]; succ = [[(np.nonzero(Fs[a, d])[0] + 1).tolist() for d in range(12)] for a in range(m)]
    s = Cadical153(); top = n * m
    for i in range(n):
        lits = [var(i, a) for a in range(m)]; s.add_clause(lits)
        enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
        for cl in enc.clauses: s.add_clause(cl)
    for i in range(n):
        for d in range(12):
            j = nbr[i][d]
            if j < 0: continue
            for a in range(m): s.add_clause([-var(i, a)] + [j * m + b for b in succ[a][d]])
    if not s.solve(): s.delete(); return None
    pos = set(l for l in s.get_model() if l > 0); s.delete()
    return [st[next(a for a in range(m) if var(i, a) in pos)] for i in range(n)]
mode = ARGS[0]
if mode == 'list':
    E, OUT = ARGS[1], ARGS[2]
    J = sorted(glob.glob(os.path.join(E, 'd_*_deep48.json')))                      # same order as run_ksdeep2.sh (ls)
    S = []
    for f in J: S += [H for H, v in json.load(open(f)) if v == 'SURVIVOR']
    cls = {}
    for H in S: cls.setdefault(canon(np.array(H)), H)
    reps = list(cls.values()); out = []
    for k in range(8):
        mine = reps[k::8]
        for l in open(os.path.join(E, f'e_{k}.log')):
            m = re.match(r'survivor (\d+) \(viable orientations (\d+)\): (.*) \(\d+s\)$', l.strip())
            if m and 'no torus to 64' in m.group(3):
                out.append(dict(id=f'{k}.{m.group(1)}', H=mine[int(m.group(1))], verdict64=m.group(3)))
    log(f'{len(S)} deep48 survivors, {len(reps)} classes; {len(out)} classes fill R8 with no torus to 64')
    assert len({canon(np.array(c['H'])) for c in out}) == len(out)
    json.dump(out, open(OUT, 'w')); print('FINAL ok' if len(out) == 73 else f'FINAL FAIL: {len(out)} classes, expected 73', flush=True)
elif mode == 'tori':
    IDX, OUT = parse_idx(ARGS[1]), ARGS[2]; T = []
    for i, n in enumerate(IDX):
        t0 = time.time(); reps = orbits_index(n)
        T += [(n, M, c, torus_nbr(M).tolist()) for n, M, c in reps]
        log(f'index {n}: {a3(n)} sublattices, {len(reps)} O_h orbits ({time.time() - t0:.0f}s)')
        print(f'PROGRESS {(i + 1) / len(IDX):.3f} tori index {n}', flush=True)
    pickle.dump(T, open(OUT, 'wb')); log(f'{len(T)} torus orbits in all'); print('FINAL ok', flush=True)
elif mode == 'ctl':
    C, HEP = json.load(open(ARGS[1])), ARGS[2]; ok = True
    # (1) per-index orbits agree with hunt.py's tori() (all indices to 24 at once)
    ref, _ = tori(24, list(range(48))); refc = {}
    for n, M, c, nbr in ref: refc[n] = refc.get(n, 0) + 1
    mine = {n: len(orbits_index(n)) for n in range(1, 25)}; ok1 = mine == refc; ok &= ok1
    log(f'control 1: per-index O_h orbits = hunt.py tori() for every index 1..24: {ok1} (index 24: {mine[24]} orbits)')
    # (2) known kill (README, hp-deep): the heptomino killed at index 28 (no torus at 7, 14, 21), with per-index orbits
    P = tuple(map(tuple, json.load(open(HEP))['survivors'][0][1])); first = None
    for N in (7, 14, 21, 28):
        for n, M, c in orbits_index(N):
            W = np.array(M) @ B3; Gi = np.linalg.inv(W.T.astype(float))
            def red(v, Gi=Gi, W=W):
                f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.rint(f @ W).astype(int).tolist())
            S = sorted({red(x) for x in torus_points(M)}); assert len(S) == N
            if poly_sat(P, S, S, red): first = N; break
        print(f'PROGRESS {N / 28 * 0.3:.3f} control 2 heptomino index {N}', flush=True)
        if first: break
    ok2 = first == 28; ok &= ok2; log(f'control 2: heptomino {P}: first torus at index {first} (README: 28): {ok2}')
    # (3) keyed engine: plain RD fills a torus; all-bump RD fills no ball R1 (hunt.py controls)
    ok3 = bool(sat_fill(fit_table(np.zeros(48, int)), list(range(48)), torus_nbr(((1, 0, 0), (0, 1, 0), (0, 0, 5))).tolist()))
    ok3 &= not sat_fill(fit_table(np.ones(48, int)), list(range(48)), ball(1))
    ok &= ok3; log(f'control 3: plain RD fills a torus of index 5, all-bump RD fills no ball R1: {ok3}')
    print('FINAL ok' if ok else 'FINAL FAIL: a control failed', flush=True)
elif mode == 'pilot':
    C, T = json.load(open(ARGS[1])), pickle.load(open(ARGS[2], 'rb'))
    H = np.array(C[0]['H']); F = fit_table(H); st = np.nonzero(arc(F))[0].tolist()
    byn = {}
    for t in T: byn.setdefault(t[0], []).append(t)
    for n in sorted(byn):
        L = byn[n]; samp = L[::max(1, len(L) // 15)][:15]; t0 = time.time(); hit = 0
        for _, M, c, nbr in samp: hit += bool(sat_fill(F, st, nbr))
        dt = (time.time() - t0) / len(samp); log(f'index {n}: {len(L)} orbits; {dt:.3f} s per torus (sample {len(samp)}, {hit} fill) -> {dt * len(L):.0f} s per class')
    for R in (10, 12):
        t0 = time.time(); B = ball(R); r = sat_fill(F, st, B); log(f'ball R{R}: {len(B)} sites, fills {bool(r)} ({time.time() - t0:.0f}s)')
    print('FINAL ok', flush=True)
elif mode == 'run':
    # tiers: tier 0 = balls R10, R12, RB; tier k = the torus orbits of the k-th pkl file. Every class passes a tier before any class
    # starts the next one, so a stop at the cap leaves every class at one uniform, recorded level. Checkpoint line per (class, tier).
    C, PK, RB, (k_sh, n_sh), OUT = json.load(open(ARGS[1])), ARGS[2].split(','), int(ARGS[3]), map(int, ARGS[4].split('/')), ARGS[5]
    rec = {}
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l); rec[(r['id'], r['tier'])] = r
    mine = [c for i, c in enumerate(C) if i % n_sh == k_sh]; NTIER = 1 + len(PK); dead = set(r['id'] for r in rec.values() if not r['verdict'].startswith('alive'))
    log(f'part {k_sh}/{n_sh}: {len(mine)} classes; {NTIER} tiers (balls R10, R12, R{RB}; tori {PK}); {len(rec)} checkpoints before')
    for tier in range(NTIER):
        T = None if tier == 0 else pickle.load(open(PK[tier - 1], 'rb'))
        if tier == 0: BB = {R: ball(R) for R in sorted({10, 12, RB})}
        else: log(f'tier {tier}: {len(T)} torus orbits, indices {T[0][0]}..{T[-1][0]}')
        for si, c in enumerate(mine):
            if c['id'] in dead or (c['id'], tier) in rec: continue
            t0 = time.time(); H = np.array(c['H']); F = fit_table(H); st = np.nonzero(arc(F))[0].tolist(); v = None
            base = (tier + si / len(mine)) / NTIER
            if tier == 0:
                for R in sorted(BB):
                    print(f'PROGRESS {base:.4f} part {k_sh}/{n_sh} tier 0 class {c["id"]} ball R{R}', flush=True)
                    if not sat_fill(F, st, BB[R]): v = f'untileable R{R}'; break
                if v is None: v = f'alive: fills R{max(BB)}'
            else:
                for i, (n, M, cnt, nbr) in enumerate(T):
                    if i % 100 == 0: print(f'PROGRESS {base + i / len(T) / len(mine) / NTIER:.4f} part {k_sh}/{n_sh} tier {tier} class {c["id"]} torus {i}/{len(T)} index {n}', flush=True)
                    if sat_fill(F, st, nbr): v = f'killed {n}'; break
                if v is None: v = f'alive: no torus of index {T[0][0]}..{T[-1][0]} in this tier'
            r = dict(id=c['id'], tier=tier, verdict=v, viable=len(st), secs=round(time.time() - t0)); rec[(c['id'], tier)] = r
            with open(OUT, 'a') as fh: fh.write(json.dumps(r) + '\n')
            if not v.startswith('alive'): dead.add(c['id'])
            log(f'tier {tier} class {c["id"]}: {v}')
    print(f'PROGRESS 1.000 part {k_sh}/{n_sh} done', flush=True); print('FINAL ok', flush=True)
elif mode == 'struct':
    C, R, OUTJ = json.load(open(ARGS[1])), int(ARGS[3]), ARGS[2]
    R_ = [json.loads(l) for f in OUTJ.split(',') for l in open(f)]; deadc = {r['id'] for r in R_ if not r['verdict'].startswith('alive')}
    alive = {r['id'] for r in R_} - deadc
    S = [c for c in C if c['id'] in alive]; B = ball(R); xyz = ball_xyz(R)
    # site order of ball(R) = BFS order; rebuild coordinates in the same order
    Sd = {(0, 0, 0): 0}; fr = [(0, 0, 0)]
    for _ in range(R):
        nf = []
        for x in fr:
            for d in NB:
                y = tuple(a + b for a, b in zip(x, d))
                if y not in Sd: Sd[y] = len(Sd); nf.append(y)
        fr = nf
    X = sorted(Sd, key=Sd.get); inner = [i for i, x in enumerate(X) if max(max(map(abs, x)), sum(map(abs, x)) // 2) <= R - 1]
    from collections import Counter
    for si, c in enumerate(S):
        H = np.array(c['H']); F = fit_table(H); st = np.nonzero(arc(F))[0].tolist(); o = ball_fill(F, st, B)
        used = Counter(o); patch = Counter(tuple([o[i]] + [o[B[i][d]] for d in range(12)]) for i in inner)
        # translations t (fcc, |t|_inf <= 4) that keep the inner filling: o(x + t) = o(x) wherever both lie in the ball
        trans = []
        for t in itertools.product(range(-4, 5), repeat=3):
            if sum(t) % 2 or t == (0, 0, 0): continue
            pairs = [(Sd[x], Sd.get(tuple(a + b for a, b in zip(x, t)))) for x in X]
            pairs = [(i, j) for i, j in pairs if j is not None]
            if pairs and all(o[i] == o[j] for i, j in pairs): trans.append(t)
        log(f'class {c["id"]}: ball R{R} filling uses {len(used)} orientations; {len(patch)} distinct radius-1 patches in the core; '
            f'translations kept (|t| <= 4): {len(trans)} {trans[:6]}')
        print(f'PROGRESS {(si + 1) / max(1, len(S)):.3f} struct {si + 1}/{len(S)}', flush=True)
    print('FINAL ok', flush=True)
elif mode == 'witness':
    # independent check of a kill: the filling of the first SAT torus of the given index, verified point by point from the heights
    # (world height at each matched point pair must sum to 0), without the fit table; prints the period lattice
    C, T, IDS = json.load(open(ARGS[1])), pickle.load(open(ARGS[2], 'rb')), ARGS[3].split(','); ok = True
    for c in [c for c in C if c['id'] in IDS]:
        H = np.array(c['H']); F = fit_table(H); st = np.nonzero(arc(F))[0].tolist(); hit = None
        for i, (n, M, cnt, nbr) in enumerate(T):
            if i % 100 == 0: print(f'PROGRESS {IDS.index(c["id"]) / len(IDS):.3f} witness class {c["id"]} torus {i}/{len(T)}', flush=True)
            o = ball_fill(F, st, nbr)
            if o is not None: hit = (n, M, nbr, o); break
        if hit is None: log(f'class {c["id"]}: no torus fills (unexpected)'); ok = False; continue
        n, M, nbr, o = hit; bad = 0
        for i in range(n):
            for d in range(12):
                j = nbr[i][d]
                for k in range(4):
                    a, b = int(MA[d, k]), int(MB[d, k])       # world point a on site i's face d meets world point b of site j
                    if H[ACTINV[o[i], a]] + H[ACTINV[o[j], b]] != 0: bad += 1
        Wl = (np.array(M) @ B3).tolist()
        log(f'class {c["id"]}: torus index {n}, HNF {M}, period vectors (world) {Wl}; {len(set(o))} orientations used; '
            f'{n * 12 * 4} point contacts checked, {bad} mismatches')
        ok &= bad == 0
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
