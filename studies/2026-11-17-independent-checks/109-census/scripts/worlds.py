"""The five universes: points (exact + float), symmetry group, quaternion-family data."""
import itertools, pickle, os
import numpy as np
from fractions import Fraction as Fr
from core import *
from engine import *
from universes import build_2I, galois_alpha_2I, build_2O_float, is_2T_float

CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')

class World:
    pass

def _h4(U):
    mats, labs = maps_matrices(U, U)
    G = PermGroup(mats, U)
    m = FastMatch(U)
    P_all = m.idx(np.einsum('gij,nj->gni', mats, U))
    ids = G.id_of(P_all)
    lab2id = np.zeros((len(U), len(U), 2), int)
    for (i, j, b), g in zip(labs, ids):
        lab2id[i, j, b] = g
    return G, lab2id

def world(name):
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, name + '.pkl')
    if os.path.exists(fn):
        return pickle.load(open(fn, 'rb'))
    W = World(); W.name = name
    D, U, mul, conj = build_2I()
    alpha = galois_alpha_2I(D, U)
    if name in ('600', '120', 'E8', 'snub'):
        G, lab2id = _h4(U)              # H4 acting on the 600-cell (faithful)
        W.qU, W.qmul, W.qconj, W.lab2id = U, mul, conj, lab2id
        W.qalpha = alpha
    if name == '600':
        W.G = G; W.n = 120; W.PU = G.P
        W.exact = D; W.kind = 'S3'
        W.twist_space = np.arange(120)   # twisted classes live in 2I itself
    elif name == '120':
        # cells: 4-cliques of the edge graph (cos = phi/2, i.e. <2x,2y> = 2 phi)
        n = 120
        ip = [[vdot(D[i], D[j]) for j in range(n)] for i in range(n)]
        edge = [[ip[i][j] == (0, 2) for j in range(n)] for i in range(n)]
        cells = []
        for a in range(n):
            nb = [b for b in range(a + 1, n) if edge[a][b]]
            for b, c, d in itertools.combinations(nb, 3):
                if edge[b][c] and edge[b][d] and edge[c][d]:
                    cells.append((a, b, c, d))
        assert len(cells) == 600, len(cells)
        cidx = {frozenset(c): i for i, c in enumerate(cells)}
        W.cells = cells
        W.exact = [tuple(qadd(qadd(D[a][t], D[b][t]), qadd(D[c][t], D[d][t])) for t in range(4))
                   for a, b, c, d in cells]
        PC = np.array([[cidx[frozenset(int(p[x]) for x in c)] for c in cells] for p in G.P], np.int32)
        W.G = G; W.n = 600; W.PU = PC; W.kind = 'S3'
    elif name == 'E8':
        W.G = G; W.n = 240
        W.PU = np.concatenate([G.P, G.P + 120], axis=1).astype(np.int32)
        W.kind = 'S7'
        W.exact = None  # Gram built from the form B below
    elif name == 'snub':
        T = np.where(is_2T_float(U))[0]; assert len(T) == 24
        Tm = np.zeros(120, bool); Tm[T] = True
        keep = np.array([Tm[G.P[g][T]].all() for g in range(G.N)])
        sub = np.where(keep)[0]; assert len(sub) == 576, len(sub)
        S = np.where(~Tm)[0]; pos = -np.ones(120, int); pos[S] = np.arange(96)
        W.G_h4 = G
        W.G = PermGroup(G.mats[sub], U)          # same reference (faithful)
        W.sub = sub
        W.n = 96; W.S = S
        W.PU = pos[W.G.P[:, S]].astype(np.int32); assert (W.PU >= 0).all()
        W.exact = [D[i] for i in S]; W.kind = 'S3'
        W.twist_space = S
    elif name == '24':
        O = build_2O_float()
        T = np.where(is_2T_float(O))[0]
        mats, labs = maps_matrices(O, O)
        m24 = FastMatch(O[T])
        keep = []
        for k, M in enumerate(mats):
            Y = O[T] @ M.T
            kk = rowkey(Y); pos = np.searchsorted(m24.k, kk); pos[pos >= 24] = 0
            keep.append(bool((m24.k[pos] == kk).all()))
        keep = np.array(keep)
        G = PermGroup(mats[keep], O[T]); assert G.N == 1152, G.N
        W.G = G; W.n = 24; W.PU = G.P
        # exact coordinates of 2T (doubled, integer pairs)
        W.exact = [tuple((int(round(2 * c)), 0) for c in O[t]) for t in T]
        W.kind = 'S3'
        mulO, conjO = unit_group_tables(O)
        W.qU, W.qmul, W.qconj = O, mulO, conjO
        P_all = m24.idx if False else None
        lab2id = -np.ones((48, 48, 2), int)
        PP = []
        for (i, j, b), M, kp in zip(labs, mats, keep):
            if kp:
                pass
        ids = G.try_id(np.array([FastMatch(O[T]).idx(O[T] @ M.T) if kp else np.zeros(24, int)
                                 for M, kp in zip(mats, keep)]))
        for (i, j, b), g, kp in zip(labs, ids, keep):
            if kp: lab2id[i, j, b] = g
        W.lab2id = lab2id
        W.twist_space = T   # indices into 2O of the 24-cell points
        W.Tidx = T
    # exact Gram codes
    if name == 'E8':
        D2 = D
        base = [[vdot(D2[i], D2[j]) for j in range(120)] for i in range(120)]  # = 4<x,y> as a+b phi
        vals = {}; codes = np.zeros((240, 240), np.int32)
        # <x,y> = (a + b phi)/4 ; phi^-1 scaling: shell B = phi^-1 * units
        phinv = (-1, 1)
        for i in range(240):
            for j in range(240):
                v = base[i % 120][j % 120]
                if (i >= 120) != (j >= 120): v = qmul(v, phinv)
                elif i >= 120: v = qmul(v, qmul(phinv, phinv))
                a, b = Fr(v[0], 4), Fr(v[1], 4)
                # a + b phi = (a + b/2) + (b/2) sqrt5 ; B = a + b/2 + b/2 = a + b
                B = a + b
                codes[i, j] = vals.setdefault(B, len(vals))
        cosv = [None] * len(vals)
        for B, k in vals.items(): cosv[k] = B
        assert set(cosv) <= {Fr(0), Fr(1, 2), Fr(-1, 2), Fr(1), Fr(-1)}, cosv
        assert all(codes[i, i] == vals[Fr(1)] for i in range(240))
        W.codes, W.cosv = codes, cosv
        W.T = ToneEngine(codes, cosv, 'S7')
    else:
        codes, cosv = exact_gram_codes(W.exact)
        W.codes, W.cosv = codes, cosv
        W.T = ToneEngine(codes, cosv, 'S3')
    # sanity: group preserves the exact Gram
    assert all((W.codes[np.ix_(p, p)] == W.codes).all() for p in W.PU[::max(1, len(W.PU) // 200)])
    pickle.dump(W, open(fn, 'wb'))
    return W
