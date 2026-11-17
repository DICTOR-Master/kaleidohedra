#!/usr/bin/env python3
"""The decorated lattice as an exact local rule (correction of the density shortcut: a non-periodic packing of density 1 can
still leave holes, so the face condition is imposed locally).
A configuration f: L -> S (S and the exact forbidden pairs from decorated_lattice.py) is a face-to-face tiling iff
  (P) no forbidden pair occurs, and
  (F) every face of every tile is matched by the opposite face of some tile.
(F) is local: for a tile s at p and its face phi, the tiles that could carry the opposite face are (s', p + lambda) with
s' + lambda having that face; the list is computed exactly. All allowed contacts were checked face to face exactly
(decorated_lattice.py), so a face can only be covered by an identical opposite face.
Uses: (1) torus counts with (P) and (F) (equal to the counts without (F), as density 1 forces covering for periodic packings);
(2) co-occurrence: can shape s at 0 and shape s' at lambda (s != s') occur together in a tiling? UNSAT in a box of radius 4 with
(P) everywhere and (F) at every point within radius 2 is an exact proof that they cannot.
Usage: decorated_sft.py <k10 dir> <inchbald json> <decorated json> <out json>"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2]); D = json.load(open(sys.argv[3]))
S = [(s[0], s[1], tuple(s[2])) for s in D['S']]; m = len(S)
BL = np.array(sol['A']['basis'])
forb = {(i, j, tuple(c)) for i, j, c in D['forbidden']}
def coords_L(v):
    c, *_ = np.linalg.lstsq(BL.T.astype(float), np.array(v, float), rcond=None); r = np.round(c).astype(int)
    return tuple(int(x) for x in r) if (r @ BL == np.array(v)).all() else None
FS = [tfaces(sol[Y]['faces'], g, w) for Y, g, w in S]
# face options
opts = {}
for i in range(m):
    for f, s in FS[i].items():
        lst = []
        for j in range(m):
            for g, s2 in FS[j].items():
                if g[1:] != f[1:] or s2 != -s: continue
                lam = coords_L(vsub(f[0], g[0]))
                if lam is None or lam == (0, 0, 0): continue
                if (i, j, lam) in forb: continue
                lst.append((j, lam))
        opts[(i, f)] = lst
print('face options per (shape, face): min', min(len(v) for v in opts.values()), 'max', max(len(v) for v in opts.values()), flush=True)
def model(sub, box, inner_r, torus=None):
    """clauses over points of the box (or torus), shapes restricted to sub"""
    if torus: pts = list(itertools.product(*[range(k) for k in torus]))
    else: pts = list(itertools.product(range(-box, box + 1), repeat=3))
    idx = {p: k for k, p in enumerate(pts)}; subs = list(sub)
    def V(p, s):
        if torus: p = tuple(p[k] % torus[k] for k in range(3))
        if p not in idx: return None
        return idx[p]*m + s + 1
    cl = []; top = len(pts)*m
    for p in pts:
        for s in range(m):
            if s not in sub: cl.append([-V(p, s)])
        enc = CardEnc.equals(lits=[V(p, s) for s in subs], bound=1, top_id=top, encoding=EncType.pairwise); cl += enc.clauses
    for p in pts:
        for i, j, c in forb:
            if i not in sub or j not in sub: continue
            q = tuple(p[k] + c[k] for k in range(3)); vq_ = V(q, j)
            if vq_ is None: continue
            if vq_ == V(p, i): cl.append([-V(p, i)]); continue
            cl.append([-V(p, i), -vq_])
        if torus or max(abs(x) for x in p) <= inner_r:
            for i in sub:
                for f in FS[i]:
                    lits = [V(tuple(p[k] + lam[k] for k in range(3)), j) for j, lam in opts[(i, f)] if j in sub]
                    lits = [x for x in lits if x is not None]
                    cl.append([-V(p, i)] + lits)
    return cl, V
def count(sub, torus, cap=20000):
    cl, V = model(sub, 0, 0, torus); pts = list(itertools.product(*[range(k) for k in torus])); n = 0
    with Cadical153(bootstrap_with=cl) as Sv:
        while n < cap and Sv.solve():
            md = set(x for x in Sv.get_model() if x > 0); n += 1
            Sv.add_clause([-V(p, s) for p in pts for s in sub if V(p, s) in md])
    return n, n < cap
res = {'torus': {}, 'cooccur': {}}
subs = {'A, B (identity)': [k for k, s in enumerate(S) if s[1] == IDENT and s[0] in 'AB'],
        'A only': [k for k, s in enumerate(S) if s[0] == 'A'], 'B only': [k for k, s in enumerate(S) if s[0] == 'B'],
        'C only': [k for k, s in enumerate(S) if s[0] == 'C'], 'A, B, C (all 11)': list(range(m))}
for nm, sub in subs.items():
    for tor in ((2, 2, 2), (3, 3, 3)):
        c, comp = count(sub, tor)
        res['torus'][f'{nm} {tor}'] = [c, comp]
        print(f'torus {tor} {nm}: tilings {c}{"" if comp else " (capped)"}', flush=True)
# co-occurrence
R, RI = 4, 2
lams = [c for c in itertools.product(range(-2, 3), repeat=3) if c != (0, 0, 0)]
for nm, sub in subs.items():
    if nm.startswith('A, B, C'): continue
    cl, V = model(set(sub), R, RI)
    out = {}
    with Cadical153(bootstrap_with=cl) as Sv:
        for i in sub:
            for j in sub:
                if i == j: continue
                ok = [lam for lam in lams if Sv.solve(assumptions=[V((0, 0, 0), i), V(lam, j)])]
                out[f'{i}->{j}'] = ok
    res['cooccur'][nm] = out
    tot = sum(len(v) for v in out.values())
    print(f'co-occurrence {nm}: shape pairs {len(out)}, locally possible (shape, lambda) pairs {tot} of {len(out)*len(lams)}', flush=True)
    for k, v in out.items():
        print(f'   {k}: {len(v)} possible lambdas; impossible ones: {sorted(set(lams) - set(v))[:30]}{" ..." if len(lams) - len(v) > 30 else ""}')
    print(f'   t={time.time()-t0:.0f}s', flush=True)
json.dump(res, open(sys.argv[4], 'w'))
print('FINAL ok' if res['torus'] else 'FINAL FAIL')
