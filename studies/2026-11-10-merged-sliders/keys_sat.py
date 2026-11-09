"""Rhombus keys, fast version (DICTO 10 Nov 2026). The geometry (which feature of which placement meets which feature of the
neighbour's placement, at every contact) does not depend on the keys: computed ONCE per stacking word from rhombus_keys.py's model.
Each key pattern then becomes a SAT instance: one variable per (half, placement), exactly one placement per half, and for every
contact a clause forbidding each placement pair whose meeting features carry the same nonzero sign. Glucose (pysat).
Sanity as before (unmarked: every word; alternating hexagon key: c only), then the search. usage: python -u keys_sat.py"""
import itertools, random, sys, time
import numpy as np
from multiprocessing import Pool
import rhombus_keys as RK
from pysat.solvers import Glucose4
from pysat.card import CardEnc
def meetings(word, N=3):
    dom, cons, cells = RK.solve(word, {'rh': {}, 'hx': [0] * 6}, N)
    keys = sorted(dom); vid = {(k, a): 1 + i * 6 + a for i, k in enumerate(keys) for a in range(6)}
    M = []
    for c in cons:
        kind, x, y, data = c; table = {}
        for a in range(6):
            Mx, tx = dom[x][a]
            for b in range(6):
                My, ty = dom[y][b]; pairs = []
                if kind == 'hx':
                    for k in range(6):
                        pw = Mx @ RK.HT[k] + tx
                        k2 = [j for j in range(6) if np.allclose(My @ RK.HT[j] + ty, pw, atol=1e-6)]
                        if len(k2) != 1: raise RuntimeError('hexagon triangle not matched')
                        pairs.append((('hx', k), ('hx', k2[0])))
                else:
                    pos, tgt, zz = data
                    nrm = (tgt - pos) / np.linalg.norm(tgt - pos); mid = (pos + tgt) / 2
                    fx = RK.face_of(Mx, tx, mid, nrm); fy = RK.face_of(My, tgt, mid, nrm)
                    for cn, p in RK.RH[fx].items():
                        w = Mx @ p + tx
                        c2 = [cc for cc, p2 in RK.RH[fy].items() if np.allclose(My @ p2 + tgt, w, atol=1e-6)]
                        if len(c2) != 1: raise RuntimeError('corner not matched')
                        pairs.append((('rh', (fx, cn)), ('rh', (fy, c2[0]))))
                table[(a, b)] = pairs
        M.append((x, y, table))
    return keys, vid, M
def sign(K, f):
    kind, key = f
    return K['hx'][key] if kind == 'hx' else K['rh'].get(key, 0)
def fits(G, K):
    keys, vid, M = G; s = Glucose4()
    for k in keys:
        lits = [vid[(k, a)] for a in range(6)]
        for cl in CardEnc.equals(lits=lits, bound=1, top_id=6 * len(keys) + 10 ** 6 + len(keys) * 100).clauses: s.add_clause(cl)
    for x, y, table in M:
        for (a, b), pairs in table.items():
            if any(sign(K, f1) and sign(K, f1) == sign(K, f2) for f1, f2 in pairs): s.add_clause([-vid[(x, a)], -vid[(y, b)]])
    r = s.solve(); s.delete(); return r
WORDS = RK.WORDS
GEO = {}
def init():
    for w, s in WORDS.items(): GEO[w] = meetings(s)
def classify(kp):
    kind, rh = kp; K = {'rh': rh, 'hx': [0] * 6}
    return tuple(w for w in WORDS if fits(GEO[w], K))
if __name__ == '__main__':
    T0 = time.time(); init(); print(f'geometry for {len(WORDS)} words in {time.time()-T0:.0f} s', flush=True)
    Z = {'rh': {}, 'hx': [0] * 6}; Kc = {'rh': {}, 'hx': [1, -1, 1, -1, 1, -1]}
    s1 = {w: fits(GEO[w], Z) for w in WORDS}; s2 = {w: fits(GEO[w], Kc) for w in WORDS}
    print('sanity unmarked:', s1); print('sanity hexagon c-key:', s2, flush=True)
    sane = all(s1.values()) and s2['c (ABC)'] and not any(v for w, v in s2.items() if w != 'c (ABC)')
    cn = ['T', 'O', 'A1', 'A2']; pats = []
    for sg in itertools.product((-1, 0, 1), repeat=4):
        if any(sg): pats.append(('same', {(r, cn[k]): sg[k] for r in RK.RH for k in range(4) if sg[k]}))
    random.seed(1); names = sorted(RK.RH)
    for _ in range(2000):
        sg = [random.choice((-1, 0, 1)) for _ in range(12)]
        if any(sg): pats.append(('mixed', {(names[ri], cn[k]): sg[ri * 4 + k] for ri in range(3) for k in range(4) if sg[ri * 4 + k]}))
    with Pool(20, initializer=init) as pool:
        res = pool.map(classify, pats, chunksize=20)
    summary = {}
    for (kind, rh), allowed in zip(pats, res): summary.setdefault((kind, allowed), []).append(rh)
    for (kind, allowed), lst in sorted(summary.items(), key=lambda z: (z[0][0], -len(z[1]))):
        print(f'{kind:5s} {len(lst):4d} patterns allow {list(allowed)}  e.g. {lst[0]}', flush=True)
    h_only = [(k, len(v)) for k, v in summary.items() if k[1] and not any(w.startswith('c') for w in k[1])]
    mixed_only = [(k, len(v)) for k, v in summary.items() if k[1] and all(w.startswith(('chh', 'cchh')) for w in k[1])]
    print('patterns that forbid pure c but allow h-words:', h_only)
    print('patterns that allow only the mixed words:', mixed_only)
    print(f'total {time.time()-T0:.0f} s')
    print('FINAL ok' if sane else 'FINAL FAIL: sanity')
