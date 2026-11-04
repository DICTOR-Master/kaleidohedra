"""For cuts (a,b,c,0): solve the torus L = B·diag(b+c, a+c, a+b) by SAT and print the two placements (orientation matrix, translation)."""
import sys, json, itertools, numpy as np
ARGS = list(sys.argv); sys.argv = [ARGS[0], '0', '0', '0', '[]']; exec(open('scripts/census.py').read().split("\nres = []\n")[0])
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def solve_place(orients, H):
    L = B @ H; Li = np.linalg.inv(L)
    def key(kind, x): z = Li @ np.asarray(x, float); return (kind, tuple(np.round(z - np.floor(z + 1e-9), 6) % 1))
    reps = [B @ np.array(v, float) for v in itertools.product(*[range(int(H[k, k])) for k in range(3)])]
    idx = {c: i for i, c in enumerate(sorted({key(k, np.array(p) + r) for r in reps for k, p in [('O', (1, 0, 0)), ('T', (.5, .5, .5)), ('T', (-.5, -.5, -.5))]}))}
    rows, meta = [], []
    for oi, (kinds, P) in enumerate(orients):
        for r in reps:
            ks = [idx.get(key(k, p + r)) for k, p in zip(kinds, P)]
            if None in ks or len(set(ks)) != len(ks): continue
            t = tuple(sorted(ks))
            if t not in rows: rows.append(t); meta.append((oi, r))
    cov = {}
    for i, r in enumerate(rows):
        for j in r: cov.setdefault(j, []).append(i + 1)
    cnf = []; top = len(rows)
    for lits in cov.values():
        e = CardEnc.equals(lits, 1, top_id=top, encoding=EncType.seqcounter); top = max(top, e.nv); cnf += e.clauses
    with Cadical153(bootstrap_with=cnf) as S:
        if not S.solve(): return None
        m = S.get_model(); return [meta[i] for i in range(len(rows)) if m[i] > 0]
for n, k in json.loads(ARGS[1]):
    a, b, c, d = k; cl = piece(n, tuple(k)); ors = orients_of(cl); H = np.diag([b + c, a + c, a + b]).astype(float)
    pl = solve_place(ors, H)
    if pl is None: print(n, k, 'diag torus: NO'); continue
    out = []
    for oi, r in pl:
        kinds, P = ors[oi]; X0 = np.array([q for _, q in cl]); Mx = np.round(np.linalg.lstsq(X0, P, rcond=None)[0].T).astype(int)
        assert np.allclose(X0 @ Mx.T, P)
        out.append({'M': Mx.tolist(), 'r': np.round(r, 6).tolist()})
    print(json.dumps({'n': n, 'k': k, 'L_diag': [b + c, a + c, a + b], 'placements': out}))
