"""Conserve or dissipate (DICTO 10 Nov: "just interested to see how geometry conserves or dissipates"). Shell after shell: the outer
surface of one shell is the core of the next. Shell 1 moves an edge set C of the truncated icosahedron (all 30 / six / one); every later
shell moves the edges made new in the shell before (the move undoes itself, so the cells return to the core's pattern). Every shell by
LP: middle edges parallel to their core edges, outer edges parallel to their source core edges (all faces flat), nearest to radial
scalings 1.18 / 1.42 of the current core. Measured per shell: distinct cell shapes; drift of the core from the regular solid
(best-fit scaled TI or TD, max corner deviation / radius). Usage: python scutoid_conserve.py all|six|one [shells]"""
import sys, itertools, json, numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def evenperm(v):
    return np.unique(np.round(np.array([(s0 * v[a], s1 * v[b], s2 * v[c]) for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
                                        for s0, s1, s2 in itertools.product([1, -1], repeat=3)], float), 12), axis=0)
P0 = np.vstack([evenperm((0, 1, 3 * phi)), evenperm((1, 2 + phi, 2 * phi)), evenperm((phi, 2, phi ** 3))]); P0 /= np.linalg.norm(P0[0])
def hull_faces(P):
    h = ConvexHull(P); G = {}
    for simp, eq in zip(h.simplices, h.equations): G.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
    out = []
    for eq, vs in G.items():
        nn = np.array(eq[:3]); vs = list(vs); c = P[vs].mean(0); e1 = P[vs[0]] - c; e1 /= np.linalg.norm(e1); e2 = np.cross(nn, e1)
        vs.sort(key=lambda v: np.arctan2((P[v] - c) @ e2, (P[v] - c) @ e1)); out.append(vs)
    return out
def edge_faces(F):
    E = {}
    for fi, f in enumerate(F):
        for k in range(len(f)): E.setdefault(frozenset((f[k], f[(k + 1) % len(f)])), []).append(fi)
    return E
def nb(f, x, not_):                                       # neighbour of x in cyclic face f other than not_
    k = f.index(x); a, b = f[(k - 1) % len(f)], f[(k + 1) % len(f)]; return b if a == not_ else a
def apply_moves(F, C):
    """T1 on each edge of C in turn, on the CURRENT faces. Returns new faces, source map new edge -> aligned core edge, new edges."""
    F = [list(f) for f in F]; src = {}
    for f in F:
        for k in range(len(f)): a, b = f[k], f[(k + 1) % len(f)]; src[(a, b)] = (a, b); src[(b, a)] = (b, a)
    new = []
    for e in C:
        u, w = tuple(e); E = edge_faces(F); A, B = E[frozenset((u, w))]
        Cf = next(fi for fi, f in enumerate(F) if u in f and fi not in (A, B)); Df = next(fi for fi, f in enumerate(F) if w in f and fi not in (A, B))
        q = nb(F[B], u, w); r = nb(F[A], w, u)
        F[A].remove(w); F[B].remove(u)
        L = F[Cf]; k = L.index(u); L.insert(k + 1 if L[(k + 1) % len(L)] == q else k, w)
        L = F[Df]; k = L.index(w); L.insert(k if L[(k - 1) % len(L)] == r else k + 1, u)
        src[(u, r)] = src[(w, r)]; src[(r, u)] = src[(r, w)]; src[(w, q)] = src[(u, q)]; src[(q, w)] = src[(q, u)]
        src[(u, w)] = ('new', A, B, Cf, Df); src[(w, u)] = ('wen', A, B, Cf, Df); new.append(frozenset((u, w)))
    assert all(len(v) == 2 for v in edge_faces(F).values()), 'surface not closed'
    return F, src, new
def shell(P, F, C, rm=1.18, ro=1.42):
    n = len(P); Fo, src, new = apply_moves(F, C); Cs = set(C)
    kept = [e for e in edge_faces(F) if e not in Cs]; oe = list(edge_faces(Fo)); N = 3 * n; nt, ns = len(kept), len(oe); nv = 4 * N + nt + ns
    Aeq, beq, Aub, bub = [], [], [], []
    for e in Cs:
        a, b = tuple(e)
        for d in range(3): r_ = np.zeros(nv); r_[3 * a + d] = 1; r_[3 * b + d] = -1; Aeq.append(r_); beq.append(0)
    for i, e in enumerate(kept):
        a, b = tuple(e); dv = P[b] - P[a]
        for d in range(3): r_ = np.zeros(nv); r_[3 * b + d] = 1; r_[3 * a + d] = -1; r_[4 * N + i] = -dv[d]; Aeq.append(r_); beq.append(0)
    for i, e in enumerate(oe):
        a, b = tuple(e); s = src.get((a, b))
        if s[0] in ('new', 'wen'):                      # new edge: along the meeting line of its two faces' core planes, from the A side to the B side
            _, A_, B_, C_, D_ = s
            nrm = lambda fi: np.cross(P[F[fi][1]] - P[F[fi][0]], P[F[fi][2]] - P[F[fi][0]])
            dv = np.cross(nrm(C_), nrm(D_)); dv /= np.linalg.norm(dv)
            cA, cB = P[F[A_]].mean(0), P[F[B_]].mean(0)
            if dv @ (cB - cA) < 0: dv = -dv                 # u (kept by A) -> w (kept by B)
            if s[0] == 'wen': dv = -dv
        else: dv = P[s[1]] - P[s[0]]
        for d in range(3): r_ = np.zeros(nv); r_[N + 3 * b + d] = 1; r_[N + 3 * a + d] = -1; r_[4 * N + nt + i] = -dv[d]; Aeq.append(r_); beq.append(0)
    # least squares (unique, keeps every symmetry the problem has): minimise |M - rm P|^2 + |O - ro P|^2 subject to the parallel
    # conditions, with every NEW edge given the core's mean edge length (so the reopening really opens)
    from scipy.linalg import null_space, lstsq
    Lnew = LNEW * ro * np.mean([np.linalg.norm(P[a] - P[b]) for a, b in map(tuple, edge_faces(F))])
    Aeq2, beq2 = list(Aeq), list(beq)
    for i_, e in enumerate(oe):
        if src.get(tuple(e))[0] in ('new', 'wen'): r_ = np.zeros(nv); r_[4 * N + nt + i_] = 1; Aeq2.append(r_); beq2.append(Lnew)
    keep = list(range(2 * N)) + list(range(4 * N, nv)); A = np.array(Aeq2)[:, keep]; b = np.array(beq2, float); m_ = len(keep)
    x0 = lstsq(A, b)[0]; Nul = null_space(A)
    tgt = np.zeros(m_); tgt[:N] = rm * P.ravel(); tgt[N:2 * N] = ro * P.ravel(); Wd = np.zeros(m_); Wd[:2 * N] = 1
    z = lstsq(Nul * Wd[:, None], (tgt - x0) * Wd)[0]; sol = x0 + Nul @ z
    if RULE == 'edges':                                   # second rule: all edges of the middle and the outer surface as equal as possible
        from scipy.optimize import least_squares
        me = [tuple(e) for e in kept]; oep = [tuple(e) for e in oe]
        # vectorised cell volumes: every cell's faces as triangles indexing X = [P; M; O]
        T_, Cid = [], []
        def addpoly(ids, c):
            for k in range(1, len(ids) - 1): T_.append((ids[0], ids[k], ids[k + 1])); Cid.append(c)
        for fi in range(len(F)):
            f = F[fi]; g = Fo[fi]
            addpoly([u for u in f][::-1], fi); addpoly([2 * n + u for u in g], fi)
            for k in range(len(f)): u, w = f[k], f[(k + 1) % len(f)]; addpoly([u, w, n + w, n + u], fi)
            for k in range(len(g)): u, w = g[k], g[(k + 1) % len(g)]; addpoly([n + u, n + w, 2 * n + w, 2 * n + u], fi)
        T_ = np.array(T_); Cid = np.array(Cid)
        def allvols(Mx, Ox):
            X = np.vstack([P, Mx, Ox]); A_, B_, C_ = X[T_[:, 0]], X[T_[:, 1]], X[T_[:, 2]]
            return np.bincount(Cid, np.einsum('ij,ij->i', A_, np.cross(B_, C_)) / 6, minlength=len(F))
        VMIN = 0.03
        def resid(zz):
            x = x0 + Nul @ zz; Mx = x[:N].reshape(-1, 3); Ox = x[N:2 * N].reshape(-1, 3)
            lm = np.array([np.linalg.norm(Mx[b_] - Mx[a_]) for a_, b_ in me]); lo = np.array([np.linalg.norm(Ox[b_] - Ox[a_]) for a_, b_ in oep])
            sc_ = x[2 * N:]; bar = 50 * np.maximum(0, 0.15 - sc_)
            vols = allvols(Mx, Ox); bar = np.concatenate([bar, 200 * np.maximum(0, VMIN - vols)])          # barrier: no edge may shrink below 0.15 of its core edge or turn over
            return np.concatenate([lm - lm.mean(), lo - lo.mean(), 1e-3 * (zz - z), bar])
        z = least_squares(resid, z, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400).x; sol = x0 + Nul @ z
    class R: pass
    res = R(); res.x = np.zeros(nv); res.x[keep] = sol
    tt = sol[2 * N:2 * N + nt]; ss = sol[2 * N + nt:]
    print(f'   edge scales: middle {tt.min():.3f}..{tt.max():.3f}, outer {ss.min():.3f}..{ss.max():.3f}; residual {np.abs(A @ sol - b).max():.1e}', flush=True)
    assert tt.min() > 0.05 and ss.min() > 0.05, 'an edge collapsed or turned over'
    M = res.x[:N].reshape(-1, 3); O = res.x[N:2 * N].reshape(-1, 3)
    def svol(V, FF): return sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in FF for k in range(1, len(f) - 1)) / 6
    cells, worst, tot = [], 0.0, 0.0
    for fi, f in enumerate(F):
        pts, FF = [], []
        def idx(p):
            for q_, v in enumerate(pts):
                if np.allclose(v, p, atol=1e-10): return q_
            pts.append(p); return len(pts) - 1
        FF.append([idx(P[u]) for u in f][::-1])
        for k in range(len(f)): u, w = f[k], f[(k + 1) % len(f)]; FF.append(list(dict.fromkeys([idx(P[u]), idx(P[w]), idx(M[w]), idx(M[u])])))
        g = Fo[fi]
        for k in range(len(g)): u, w = g[k], g[(k + 1) % len(g)]; FF.append(list(dict.fromkeys([idx(M[u]), idx(M[w]), idx(O[w]), idx(O[u])])))
        FF.append([idx(O[u]) for u in g]); V = np.array(pts)
        for ff in FF:
            if len(ff) > 3:
                Q = V[ff]; nr = np.cross(Q[1] - Q[0], Q[2] - Q[0]); nr /= np.linalg.norm(nr); worst = max(worst, float(abs((Q - Q[0]) @ nr).max()))
        v = svol(V, FF); tot += v; cells.append({'V': V.tolist(), 'F': FF, 'kind': f'{len(f)}-{len(g)}', 'vol': v})
    gap = abs(tot - (svol(O, Fo) - svol(P, F)))
    return O, Fo, new, cells, worst, gap, min(c['vol'] for c in cells)
def shapes(cells):
    sp = lambda c: tuple(np.sort(np.round(np.linalg.norm(np.array(c['V'])[:, None] - np.array(c['V'])[None], axis=2).ravel() / np.cbrt(abs(c['vol'])), 4)))
    return len({sp(c) for c in cells})
TDref = np.vstack([evenperm((0, 1 / phi, 2 + phi)), evenperm((1 / phi, phi, 2 * phi)), evenperm((phi, 2, phi + 1))])
def drift(P, F):
    """distance of the surface from the regular solid of its pattern: faces' plane distances along the 12 + 20 axes, spread / mean"""
    d = []
    for f in F:
        c = P[f].mean(0); nrm = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); nrm /= np.linalg.norm(nrm); d.append((len(f), abs(c @ nrm)))
    out = []
    for k in sorted({x for x, _ in d}):
        vals = np.array([y for x, y in d if x == k]); out.append(f'{k}-gons {len(vals)} spread {np.ptp(vals) / vals.mean():.2e}')
    return '; '.join(out)
mode = sys.argv[1] if len(sys.argv) > 1 else 'one'; K = int(sys.argv[2]) if len(sys.argv) > 2 else 6; LNEW = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; RULE = sys.argv[4] if len(sys.argv) > 4 else 'radial'
P = P0.copy(); F = hull_faces(P); E = edge_faces(F)
hh = [e for e, fs in E.items() if all(len(F[x]) == 6 for x in fs)]
mid = lambda e: P[list(e)].mean(0)
C = hh if mode == 'all' else [e for e in hh if np.sum(np.abs(mid(e) / np.linalg.norm(mid(e))) > 0.999) == 1] if mode == 'six' else [max(hh, key=lambda e: mid(e)[2])]
ok = True; allcells = []
for s in range(1, K + 1):
    O, Fo, new, cells, worst, gap, vmin = shell(P, F, C)
    sc = np.linalg.norm(O, axis=1).mean(); O = O / sc                     # each core renormalised to mean radius 1 (shape only)
    from collections import Counter
    print(f'shell {s}: moves {len(C)}; cells {dict(Counter(c["kind"] for c in cells))}; distinct shapes {shapes(cells)}; flat {worst:.0e}; '
          f'volume check {gap:.0e}; min vol {vmin:.3f}', flush=True)
    print(f'   outer surface: {drift(O, Fo)}', flush=True)
    ok &= worst < 1e-8 and gap < 1e-8 and vmin > 0
    allcells.append(cells); P, F, C = O, Fo, new
json.dump(allcells, open(f'scutoid-conserve-{mode}.json', 'w'))
print('FINAL ok' if ok else 'FINAL FAIL')
