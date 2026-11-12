# keysearch.py, 13 Nov 2026 (aim 3, lead 2 of the hopeful-piece hunt): a DIRECTED search among keyed RDs with no symmetry assumed.
# Keying of the old H-schemes stays suspended; this hunts for a new single piece only (shape: bumps and dents, no labels).
# Piece = height field H on the 48 face points (hunt.py, family K), heights in {-A..A}. Instead of sampling, one SAT model asks
# for the piece AND a filling of the ball of radius RB round a site at once, and learns from every periodic filling it meets
# (counterexample-guided search):
#   - e(a, b) <-> H[a] = -H[b]  (points a, b of the piece meet flush);
#   - ball: orientation o[i, g] per site, world height W[i, p] = H[g^-1 p], neighbours flush (centre fixed to the identity: the ball
#     is O_h-symmetric, so this loses nothing);
#   - no period of index 1 or 2: complete clauses (every orientation pattern on every torus of index 1, 2, one per O_h orbit);
#   - every candidate goes through hunt.py's kill test (arc consistency, tori to IMAX, balls R3..RMAX). A torus filling gives a
#     witness: the set W of point pairs that meet in it; the clause "some pair of W does not meet" is TRUE of every piece without
#     that period-pattern, so it is added (with its 48 relabellings, which are the same piece turned). An untileable or surviving
#     piece is blocked exactly (its 96 congruent copies).
#   - WLOG H[0] = +1 (a non-flat piece has a turned, possibly bump<->dent copy with a bump at point 0; the flat piece is the plain RD).
# Cubes: the heights of points 1..CK are fixed by assumptions; each shard takes cubes k = SHARD mod NSHARDS. A cube that ends UNSAT
# is EXHAUSTED: every keyed RD in it (alphabet -A..A) is untileable at RB, periodic with one of the found patterns, or blocked.
# usage: keysearch.py ctl A RB IMAX
#        keysearch.py run A RB IMAX RMAX CK SHARD/NSHARDS HOURS out.json
import sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = ['hunt.py', 'none']
exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
sys.argv = _argv
def sat_fill_w(F, st, nbr):
    """as hunt.sat_fill, but returns the orientation of every site (or None)"""
    m = len(st); n = len(nbr); var = lambda i, a: 1 + i * m + a
    Fs = F[np.ix_(st, range(12), st)]; succ = [[(np.nonzero(Fs[a, d])[0] + 1).tolist() for d in range(12)] for a in range(m)]
    s = Cadical153(); top = n * m
    for i in range(n):
        lits = [var(i, a) for a in range(m)]; s.add_clause(lits)
        if m > 1:
            enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for cl in enc.clauses: s.add_clause(cl)
    for i in range(n):
        for d in range(12):
            j = nbr[i][d]
            if j < 0: continue
            for a in range(m): s.add_clause([-var(i, a)] + [j * m + b for b in succ[a][d]])
    if not s.solve(): s.delete(); return None
    mod = set(l for l in s.get_model() if l > 0); s.delete()
    return [st[next(a for a in range(m) if var(i, a) in mod)] for i in range(n)]
def witness_pairs(orient, nbr):
    P = set()
    for i, g in enumerate(orient):
        for d in range(12):
            j = nbr[i][d]
            if j < 0: continue
            h = orient[j]
            for k in range(4): a, b = int(ACTINV[g, MA[d, k]]), int(ACTINV[h, MB[d, k]]); P.add((min(a, b), max(a, b)))
    return P
def judge_w(H, imax, rmax, tor):
    """hunt.judge with the witness: ('untileable AC'|'untileable Rk'|'SURVIVOR', None) or ('killed n', pairs)"""
    F = fit_table(H); v = arc(F); st = np.nonzero(v)[0].tolist()
    if not st: return 'untileable AC', None
    for s_ in st:
        if all(F[s_, d, s_] for d in range(12)): return 'killed 1', {(min(int(ACTINV[s_, MA[d, k]]), int(ACTINV[s_, MB[d, k]])), max(int(ACTINV[s_, MA[d, k]]), int(ACTINV[s_, MB[d, k]]))) for d in range(12) for k in range(4)}
    for n, M, c, nbr in tor:
        if n == 1: continue
        o = sat_fill_w(F, st, nbr)
        if o is not None: return f'killed {n}', witness_pairs(o, nbr)
    for R in range(3, rmax + 1):
        if not sat_fill(F, st, BALLS[R]): return f'untileable R{R}', None
    return 'SURVIVOR', None
class Model:
    def __init__(self, A, RB, tor2):
        self.A = A; self.V = list(range(-A, A + 1)); nv = len(self.V); self.top = 0; self.s = Cadical153(); self.ncl = 0
        def new(): self.top += 1; return self.top
        self.new = new
        self.H = [[new() for _ in self.V] for _ in range(48)]
        for p in range(48): self.add(self.H[p]); [self.add([-self.H[p][x], -self.H[p][y]]) for x in range(nv) for y in range(x + 1, nv)]
        self.add([self.H[0][self.V.index(1)]])
        self.E = {}
        # ball of radius RB: orientation per site, world heights, flush neighbours
        nb = BALLS[RB]; ns = len(nb); self.o = [[new() for _ in range(48)] for _ in range(ns)]
        for i in range(ns):
            self.add(self.o[i]); [self.add([-self.o[i][x], -self.o[i][y]]) for x in range(48) for y in range(x + 1, 48)]
        self.add([self.o[0][IDG]])
        Wv = [[[new() for _ in self.V] for _ in range(48)] for _ in range(ns)]
        for i in range(ns):
            for g in range(48):
                og = self.o[i][g]
                for p in range(48):
                    q = int(ACTINV[g, p])
                    for x in range(nv): self.add([-og, -self.H[q][x], Wv[i][p][x]]); self.add([-og, -Wv[i][p][x], self.H[q][x]])
        for i in range(ns):
            for d in range(12):
                j = nb[i][d]
                if j < 0: continue
                for k in range(4):
                    a, b = int(MA[d, k]), int(MB[d, k])
                    for x in range(nv): self.add([-Wv[i][a][x], Wv[j][b][nv - 1 - x]])
        # no period of index 1 or 2 (complete)
        for g in range(48): self.block_pairs({(min(int(ACTINV[g, MA[d, k]]), int(ACTINV[g, MB[d, k]])), max(int(ACTINV[g, MA[d, k]]), int(ACTINV[g, MB[d, k]]))) for d in range(12) for k in range(4)}, images=False)
        self.n2 = 0
        for n, M, c, nbr in tor2:
            if n != 2: continue
            for g0 in range(48):
                for g1 in range(48): self.block_pairs(witness_pairs([g0, g1], nbr), images=False); self.n2 += 1
    def add(self, cl): self.s.add_clause(cl); self.ncl += 1
    def e(self, a, b):
        if (a, b) in self.E: return self.E[(a, b)]
        v = self.new(); self.E[(a, b)] = v; nv = len(self.V)
        for x in range(nv):
            y = nv - 1 - x
            self.add([-self.H[a][x], -self.H[b][y], v]); self.add([-v, -self.H[a][x], self.H[b][y]])
        return v
    def block_pairs(self, P, images=True):
        maps = range(48) if images else [IDG]
        for g in maps:
            cl = sorted({-self.e(*sorted((int(ACT[g, a]), int(ACT[g, b])))) for a, b in P}); self.add(cl)
    def block_H(self, H):
        for g in range(48):
            Hg = H[ACT[g]]
            for sg in (1, -1): self.add([-self.H[p][self.V.index(int(sg * Hg[p]))] for p in range(48)])
    def solve(self, assum):
        if not self.s.solve(assumptions=assum): return None
        mod = self.s.get_model(); pos = set(l for l in mod if l > 0)
        return np.array([self.V[next(x for x in range(len(self.V)) if self.H[p][x] in pos)] for p in range(48)])
    def fixH(self, H): return [self.H[p][self.V.index(int(H[p]))] for p in range(48)]
def bump0(H):
    """a congruent copy (turned, maybe bump<->dent) with H[0] = +1, or None for the flat piece"""
    nz = [p for p in range(48) if H[p] != 0]
    if not nz: return None
    p = nz[0]; sg = 1 if H[p] > 0 else -1; g = next(g for g in range(48) if ACT[g, 0] == p); H2 = sg * H[ACT[g]]; assert H2[0] == 1; return H2
mode = sys.argv[1]
if mode == 'ctl':
    A, RB, IMAX = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); ok = True
    tor, _ = tori(IMAX, list(range(48))); t0 = time.time()
    M = Model(A, RB, tor); log(f'model: vars {M.top}, clauses {M.ncl}, index-2 patterns {M.n2}, built in {time.time() - t0:.0f}s')
    # random symmetric pieces (|G| = 4 classes, as hp-main A) through judge and the model with H fixed
    rng = np.random.default_rng(5); cls = [G for G in subgroups() if len(G) == 4]; seen = {}; tried = 0; agree = 0
    want = {'killed 1': 3, 'killed 2': 3, 'killed 4': 3, 'killed 8': 2, 'untileable AC': 20}
    while any(seen.get(k, 0) < v for k, v in want.items()) and tried < 200000:
        G = cls[int(rng.integers(len(cls)))]; pt = np.zeros(48, int)
        for oi, o in enumerate(orbits_on_points(G)): pt[o] = oi
        H = rng.integers(-1, 2, size=12)[pt]; tried += 1; H = bump0(H)
        if H is None: continue
        F = fit_table(H); vj = judge(F, IMAX, 2, list(range(48)))
        if seen.get(vj, 0) >= want.get(vj, 0): continue
        seen[vj] = seen.get(vj, 0) + 1
        ballfill = sat_fill(F, list(range(48)), BALLS[RB]) is True
        got = M.solve(M.fixH(H)) is not None
        exp = ballfill and vj not in ('killed 1', 'killed 2')
        agree += got == exp; ok &= got == exp
        log(f'control piece {vj:14s} ball R{RB} fills {ballfill}; model SAT {got} (expected {exp})')
        if vj in ('killed 4', 'killed 8') and got:
            # pilot 13 Nov: blocking in the shared model also (rightly) blocked LATER control pieces with the same period pattern,
            # so each blocking test now runs in a fresh model
            vw, P = judge_w(H, IMAX, 2, tor); M2 = Model(A, RB, tor); M2.block_pairs(P); again = M2.solve(M2.fixH(H)) is not None
            log(f'   witness {vw}, {len(P)} pairs; after blocking it the model is SAT {again} (expected False)'); ok &= vw == vj and not again
    log(f'controls: {sum(seen.values())} pieces from {tried} draws, {agree} agree; seen {seen}'); ok &= all(seen.get(k, 0) >= v for k, v in want.items())
    print('FINAL ok' if ok else 'FINAL FAIL: a control failed', flush=True)
elif mode == 'deep':
    # deep check of keyed-RD survivors: every torus up to index IMAX2 (first killing index), then ball R5
    J, IMAX2 = sys.argv[2], int(sys.argv[3]); S = []
    for f in J.split(','): S += json.load(open(f))['survivors']
    tor, tot = tori(IMAX2, list(range(48))); log(f'{len(S)} survivors; {len(tor)} torus orbits to index {IMAX2} ({tot} tori)')
    BALLS[5] = ball(5); out = []
    for si, H in enumerate(S):
        H = np.array(H); v, P = judge_w(H, IMAX2, 5, tor); out.append([H.tolist(), v]); log(f'survivor {si}: {v}')
        print(f'PROGRESS {(si + 1) / len(S):.3f} deep {si + 1}/{len(S)}', flush=True)
    json.dump(out, open(J.split(',')[0].replace('.json', '') + f'_deep{IMAX2}.json', 'w')); print('FINAL ok', flush=True)
elif mode == 'deep2':
    # second deep check: survivors of 'deep' (no torus <= 48, fill R5), one per congruence class, on tori of index IMIN+1..IMAX2
    # and balls R6..RB2
    J, IMIN, IMAX2, RB2, SH = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]; k_sh, n_sh = map(int, SH.split('/'))
    S = []
    for f in J.split(','): S += [H for H, v in json.load(open(f)) if v == 'SURVIVOR']
    cls = {}
    for H in S: cls.setdefault(canon(np.array(H)), H)
    reps = list(cls.values()); mine = reps[k_sh::n_sh]
    tor, tot = tori(IMAX2, list(range(48))); tor = [t for t in tor if t[0] > IMIN]
    log(f'{len(S)} survivors, {len(reps)} up to congruence, this part {len(mine)}; {len(tor)} torus orbits of index {IMIN + 1}..{IMAX2}')
    for R in range(5, RB2 + 1): BALLS[R] = ball(R)
    out = []
    for si, H in enumerate(mine):
        H = np.array(H); F = fit_table(H); st = np.nonzero(arc(F))[0].tolist(); verdict = None
        for R in range(6, RB2 + 1):                                   # balls first: an untileable piece is out at once
            if not sat_fill(F, st, BALLS[R]): verdict = f'untileable R{R}'; break
            print(f'PROGRESS {si / len(mine):.3f} part {SH} survivor {si} fills R{R}', flush=True)
        if verdict is None:
            for i, (n, M, c, nbr) in enumerate(tor):
                if sat_fill(F, st, nbr): verdict = f'fills R{RB2}; killed {n}'; break
                if i % 200 == 0: print(f'PROGRESS {(si + i / len(tor)) / len(mine):.3f} part {SH} survivor {si} torus {i}/{len(tor)} index {n}', flush=True)
        if verdict is None: verdict = f'fills R{RB2}; no torus to {IMAX2}'
        log(f'survivor {si} (viable orientations {len(st)}): {verdict}'); out.append([H.tolist(), len(st), verdict])
    json.dump(out, open(J.split(',')[0].replace('.json', '') + f'_deep2_{k_sh}.json', 'w')); print('FINAL ok', flush=True)
elif mode == 'run':
    A, RB, IMAX, RMAX, CK = map(int, sys.argv[2:7]); SH, HOURS, OUT = sys.argv[7], float(sys.argv[8]), sys.argv[9]
    k_sh, n_sh = map(int, SH.split('/')); dead = time.time() + 3600 * HOURS; nv = 2 * A + 1
    tor, _ = tori(IMAX, list(range(48))); M = Model(A, RB, tor); log(f'model: vars {M.top}, clauses {M.ncl}, index-2 patterns {M.n2}')
    allc = [np.unravel_index(c, [nv] * CK) for c in range(nv ** CK)]; mine = [c for i, c in enumerate(allc) if i % n_sh == k_sh]
    cnt = {}; surv = []; done = []; t_last = time.time(); fault = None; ncand = 0
    for ci, cube in enumerate(mine):
        assum = [M.H[1 + j][int(x)] for j, x in enumerate(cube)]
        while time.time() < dead:
            H = M.solve(assum)
            if H is None: done.append([int(x) for x in cube]); break
            v, P = judge_w(H, IMAX, RMAX, tor); ncand += 1; cnt[v] = cnt.get(v, 0) + 1
            if v in ('killed 1', 'killed 2'): fault = f'model let a period {v} through: {H.tolist()}'; break
            if P is not None: M.block_pairs(P)
            else: M.block_H(H)
            if v == 'SURVIVOR': surv.append(H.tolist()); log('SURVIVOR keyed RD', H.tolist())
            if time.time() - t_last > 60:
                t_last = time.time(); print(f'PROGRESS {(len(done) + 0.5) / len(mine):.3f} shard {SH} cubes {len(done)}/{len(mine)} candidates {ncand} {json.dumps(cnt)} clauses {M.ncl}', flush=True)
        if fault or time.time() >= dead: break
        print(f'PROGRESS {len(done) / len(mine):.3f} shard {SH} cubes {len(done)}/{len(mine)} candidates {ncand} {json.dumps(cnt)}', flush=True)
    json.dump(dict(A=A, RB=RB, IMAX=IMAX, RMAX=RMAX, CK=CK, shard=SH, cubes_total=len(mine), cubes_exhausted=done, candidates=ncand,
                   counts=cnt, survivors=surv, fault=fault, timed_out=time.time() >= dead), open(OUT, 'w'))
    log('COUNTS', SH, f'cubes exhausted {len(done)}/{len(mine)}', json.dumps(cnt), 'survivors', len(surv))
    print('FINAL ok' if fault is None else 'FINAL FAIL: ' + fault, flush=True)
