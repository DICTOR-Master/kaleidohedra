# cut_down.py, DICTO 12 Nov 2026 ("go ahead with cutting the 558 down"). Coarser markings of the RD bridge (bridge_count.py):
# each scheme keeps only part of what an RD sees of the chair tiling. Per scheme:
#   TYPES   number of marked RDs (labels up to the RD's 24 proper turns);
#   RECOVER can every RD's FULL label be read from its own coarse label and its 12 neighbours' (radius 1)? (a function, no clash)
#   TORI    SAT: with the face-to-face pair rules the scheme shows in hierarchical tilings (types, relative turn, direction), does a
#           PERIODIC filling of the fcc RD packing exist? Every site may take every type in every turn (no grid assumed); tori = all
#           sublattices of the fcc lattice of index <= IMAX (Hermite forms). SAT on a torus = the scheme allows a repeating filling
#           = FAILS. A scheme that passes every torus is a CANDIDATE (not yet a proof).
# Controls: FULL (558 types) must be UNSAT on every torus; PLAIN (one unmarked RD) must be SAT at index 1.
# Tori: row Hermite forms (a,0,0), (b,d,0), (c,e,f) with 0<=b,c<a, 0<=e<d, index a*d*f, in the fcc basis (1,1,0),(1,0,1),(0,1,1).
# usage: python3 cut_down.py <level k> <IMAX> <out.json> [schemes comma list]
import sys, os, json, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor'))
from chairN import Chair, apply, compose, inverse, make_group, det, vsub, vadd
from collections import defaultdict
t0 = time.time(); K = int(sys.argv[1]); IMAX = int(sys.argv[2]); OUT = sys.argv[3]
FR = {'0': (0, 1, 2), (0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
C = Chair(3, FR); ROT = [g for g in make_group(3) if det(g) == 1]; RI = {g: i for i, g in enumerate(ROT)}
NB = [d for d in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, d)) == 2]; assert len(NB) == 12
tiles = C.patch(K); owner = {}
for ti, (g, t) in enumerate(tiles):
    for ui, c in enumerate(C.cubes((g, t))): owner[c] = (ti, ui)
def cubes_of(x):
    if all(v % 2 for v in x): return [x]
    i = next(j for j in range(3) if x[j] % 2); out = []
    for a, b in itertools.product((1, -1), repeat=2):
        d = [a, b]; d.insert(i, 0); out.append(vadd(x, tuple(d)))
    return out
sites = {}
for c in owner:
    for x in [c] + [vadd(c, (0, a, b)) for a in (1, -1) for b in (1, -1)] + [vadd(c, (a, 0, b)) for a in (1, -1) for b in (1, -1)] + [vadd(c, (a, b, 0)) for a in (1, -1) for b in (1, -1)]:
        if x not in sites:
            cs = cubes_of(x)
            if all(cc in owner for cc in cs): sites[x] = cs
print(f'level {K}: chairs {len(tiles)}, complete sites {len(sites)} ({time.time()-t0:.0f}s)', flush=True)
# entry = (cube offset from site, chair frame, cell, chair id); a scheme maps the list of entries to a reduced list
def entries(x):
    ids = {}; return [(vsub(c, x), tiles[owner[c][0]][0], owner[c][1], ids.setdefault(owner[c][0], len(ids))) for c in sites[x]]
SCHEMES = {
 'FULL':        lambda E: [(o, g, u, i) for o, g, u, i in E],
 'PLAIN':       lambda E: [],
 'CELL':        lambda E: [(o, None, u, None) for o, g, u, i in E] if len(E) == 1 else [],                 # centre: cell; edge: nothing
 'CELL+ECELLS': lambda E: [(o, None, u, None) for o, g, u, i in E],                                        # every RD: the cells round it
 'CELL+EPART':  lambda E: [(o, None, u, None) for o, g, u, i in E] if len(E) == 1 else [(o, None, None, i) for o, g, u, i in E],  # edge: which cubes share a chair
 'CELL+EPC':    lambda E: [(o, None, u, i) for o, g, u, i in E],                                           # cells + which share a chair
 'FRAME':       lambda E: [(o, g, None, None) for o, g, u, i in E] if len(E) == 1 else [],                 # centre: chair frame only
 'FRAME+EFR':   lambda E: [(o, g, None, i) for o, g, u, i in E],                                           # frames + sharing, no cells
 'CF+ECELL':    lambda E: [(o, g, u, None) for o, g, u, i in E] if len(E) == 1 else [(o, None, u, i) for o, g, u, i in E],   # edge: sharing + cells
 'CF+EFRAME':   lambda E: [(o, g, u, None) for o, g, u, i in E] if len(E) == 1 else [(o, g, None, i) for o, g, u, i in E],   # edge: sharing + chair turns
 'CELLFRAME':   lambda E: [(o, g, u, None) for o, g, u, i in E] if len(E) == 1 else [(o, None, None, i) for o, g, u, i in E],
}
def _close(gens):
    S = {C.id}; fr = [C.id]
    while fr:
        a = fr.pop(); 
        for b in gens:
            c = compose(a, b)
            if c not in S: S.add(c); fr.append(c)
    return frozenset(S)
SUBGROUPS = sorted({_close([a, b]) for a in ROT for b in ROT}, key=lambda H: (len(H), sorted(H)))
assert len(SUBGROUPS) == 30, len(SUBGROUPS)
def _coset(g, H): return tuple(sorted(compose(g, h) for h in H))
for _k, _H in enumerate(SUBGROUPS):    # centre: full chair frame + sharing; edge: sharing + chair frame known only up to H
    SCHEMES[f'H{_k:02d}'] = (lambda H: (lambda E: [(o, g, None, i) for o, g, u, i in E] if len(E) == 1 else [(o, _coset(g, H), None, i) for o, g, u, i in E]))(_H)
want = sys.argv[4].split(',') if len(sys.argv) > 4 else list(SCHEMES)
def is_coset(g): return isinstance(g, tuple) and len(g) > 0 and isinstance(g[0], tuple) and len(g[0]) > 0 and isinstance(g[0][0], tuple)
def rot_frame(R, g):
    """R applied to a frame, or to a coset gH stored as a sorted tuple of frames (12 Nov: coarse frames for the 12-90 search)"""
    if g is None: return None
    if is_coset(g): return tuple(sorted(compose(R, x) for x in g))
    return compose(R, g)
def canon(L):
    """min over turns R of the R-image of the entry list; returns (label, list of R achieving it). Frames written relative: R*g.
    Chair ids are renumbered by first appearance after sorting by cube offset (fixed 12 Nov: ids had followed the world order of
    the cubes, so one configuration could give two labels)."""
    best = None; arg = []
    for R in ROT:
        rows = sorted(((apply(R, o), rot_frame(R, g), u, i) for o, g, u, i in L), key=lambda r: r[0])
        ren = {}
        key = tuple((o, g, u, None if i is None else ren.setdefault(i, len(ren))) for o, g, u, i in rows)
        if best is None or key < best: best, arg = key, [R]
        elif key == best: arg.append(R)
    return best, arg
FULLC = {x: canon(SCHEMES['FULL'](entries(x))) for x in sites}
print(f'full labels done ({time.time()-t0:.0f}s)', flush=True)
def sublattices(imax):
    B = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    out = []
    for n in range(1, imax + 1):
        for a in range(1, n + 1):
            if n % a: continue
            for d in range(1, n // a + 1):
                if (n // a) % d: continue
                f = n // a // d
                for b in range(a):
                    for c_ in range(a):
                        for e in range(d):
                            M = [(a, 0, 0), (b, d, 0), (c_, e, f)]   # rows: generators in the B basis (lower-triangular Hermite form)
                            out.append((n, [tuple(sum(r[k] * B[k][j] for k in range(3)) for j in range(3)) for r in M]))
    return out
def torus_sites(gens):
    import numpy as np
    G = np.array(gens, float).T; Gi = np.linalg.inv(G)
    def red(v):
        f = Gi @ np.array(v, float); f = f - np.floor(f + 1e-9); return tuple(np.round(f, 6))
    reps = {}
    for x in itertools.product(range(-4, 5), repeat=3):
        if sum(x) % 2 == 1: reps.setdefault(red(x), x)
    return list(reps.values()), red
res = {}
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
for name in want:
    f = SCHEMES[name]; lab = {}; tid = {}
    for x in sites:
        L, arg = canon(f(entries(x))); lab[x] = (tid.setdefault(L, len(tid)), tuple(sorted(RI[R] for R in arg)))
    ntypes = len(tid)
    # RECOVER radius 1
    key2full = {}; clash = 0; memo_k = {}
    for x in sites:
        nbs = [vadd(x, d) for d in NB]
        if not all(y in lab for y in nbs): continue
        ck = (lab[x], tuple(lab[vadd(x, d)] for d in NB))
        best = memo_k.get(ck)
        if best is None:
            for r in lab[x][1]:
                R = ROT[r]
                k = tuple(sorted((apply(R, d), lab[vadd(x, d)][0], min(RI[compose(ROT[q], inverse(R))] for q in lab[vadd(x, d)][1])) for d in NB))
                if best is None or k < best: best = k
            memo_k[ck] = best
        k = (lab[x][0], best); fl = FULLC[x][0]
        if key2full.setdefault(k, fl) != fl: clash += 1
    # pair rules: (a, b, local direction R(d), relative turn Ry R^-1)
    allowed = defaultdict(set); seen = set()
    for x in sites:
        for d in NB:
            y = vadd(x, d)
            if y not in lab or (lab[x], lab[y], d) in seen: continue
            seen.add((lab[x], lab[y], d)); (a, Ra), (b, Rb) = lab[x], lab[y]
            for r in Ra:
                R = ROT[r]
                for q in Rb: allowed[(a, apply(R, d))].add((b, RI[compose(ROT[q], inverse(R))]))
    tori = []; per = None
    for n, gens in sublattices(IMAX):
        S, red = torus_sites(gens); idx = {red(x): i for i, x in enumerate(S)}
        s = Cadical153(); var = lambda i, a, r: 1 + (i * ntypes + a) * 24 + r
        top = var(len(S), 0, 0)
        for i in range(len(S)):
            lits = [var(i, a, r) for a in range(ntypes) for r in range(24)]
            s.add_clause(lits)                                                     # each site: at least one marked RD in one turn
            enc = CardEnc.atmost(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)   # (a one-literal list returns nv 0)
            for cl in enc.clauses: s.add_clause(cl)                                # ... and at most one (fixed 12 Nov: was missing)
        for i, x in enumerate(S):
            for d in NB:
                j = idx[red(vadd(x, d))]
                for a in range(ntypes):
                    for r in range(24):
                        R = ROT[r]; ok = allowed.get((a, apply(R, d)), ())
                        s.add_clause([-var(i, a, r)] + [var(j, b, RI[compose(ROT[q], R)]) for b, q in ok])
        sat = s.solve(); s.delete(); tori.append((n, sat))
        if sat: per = (n, gens); break
    verdict = f'PERIODIC (torus index {per[0]})' if per else f'CANDIDATE (no torus up to index {IMAX})'
    res[name] = dict(types=ntypes, recover_r1=(clash == 0), clashes=clash, tori_tested=len(tori), verdict=verdict)
    print(f'{name:12s} types {ntypes:5d}  recover(r=1) {"yes" if clash == 0 else "NO (" + str(clash) + " clashes)"}  {verdict}  ({len(tori)} tori, {time.time()-t0:.0f}s)', flush=True)
ok = ('FULL' not in res or res['FULL']['verdict'].startswith('CAND')) and ('PLAIN' not in res or res['PLAIN']['verdict'].startswith('PERIODIC'))
json.dump(res, open(OUT, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: controls', flush=True)
