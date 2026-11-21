#!/usr/bin/env python3
"""Exact SAT search for periodic tilings of a torus R^3 / Lambda by copies of one piece (Kaplan-style: Boolean variable per placement).
Search space S(kind, Lambda, R):
  * pieces: the templates of the kind (C6: the 6 cube centre pyramids; RD: the 12 RD centre pyramids; TET: the regular tetrahedron and its
    point reflection; GR: the acute golden rhombohedron in its 10 icosahedral orientations; RT: the 30 centre pyramids of one fixed RT =
    'class O', every piece parallel to a pyramid of the same RT), placed by translation only;
  * reference points (apexes) in one coset of the module M spanned by the vertex vectors (module coordinates n in Z^k, k = 3 or 6),
    one apex at the origin;
  * period lattice Lambda = the span of three given module vectors; a placement is (template, class of the apex in M / Lambda);
  * k = 6 (icosahedral module, dense in R^3): only apex classes of height h <= R are used, h = distance in Z^6 from n to the real span of
    Lambda (well defined on classes), reached from the origin by steps of single vertex vectors without leaving h <= R. k = 3: all classes.
Clauses (all necessary conditions of a tiling in S, so UNSAT is a proof that S holds no tiling):
  * every sample point lies in the closed piece of at least one chosen placement;
  * no sample point lies in the open interior of two chosen placements;
  * exactly N placements are chosen, N = vol(Lambda) / vol(piece) (exact; refused if not an integer);
  * some chosen placement has its apex at the origin.
Sample points start as the centroids of the placements. A model is checked exactly (pairwise interiors disjoint on the torus); an
overlap adds an interior point of the overlap as a new sample point and the solver runs again (counterexample loop). Non-overlap of N
pieces of total volume vol(Lambda) means a tiling of the torus, i.e. a periodic tiling of space. All geometric decisions are exact in
Z[phi] (floating arithmetic only to skip cases decided by more than 1e-9; every closer case is evaluated exactly).
Usage: tsat.py KIND 'l1;l2;l3' R2 TIMEOUT_S OUTPREFIX   (li = comma-separated module coordinates; R2 = R^2, integer)"""
import sys, os, json, time, itertools, threading
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import cKDTree, HalfspaceIntersection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def say(*a): print(*a, flush=True)

def exact_volume6(P):
    """6 * volume of piece P, exact in Z[phi] (fan from vertex 0 over hull triangles)"""
    from scipy.spatial import ConvexHull
    Vf = zf(P.V); h = ConvexHull(Vf); tot = np.zeros(2, np.int64)
    for s in h.simplices:
        if 0 in s: continue
        a, b, c = (P.V[i] - P.V[0] for i in s)
        d = zdet3(a, b, c); tot = tot + (d if zsign(d) > 0 else -d)
    return tot

def zdiv_int(x, y):
    """x / y if it is a rational integer, else None (x, y in Z[phi])"""
    r = zf(x)/zf(y); n = int(round(r))
    return n if np.array_equal(y*n, x) else None

class Torus:
    def __init__(self, kind, lat, R2):
        self.kind = kind; self.E, T = kind_data(kind); self.k = self.E.shape[0]
        self.T = T; self.P = [Piece(t, self.E, kind != 'TET') for t in T]
        self.L = np.array(lat, dtype=np.int64)                      # (3, k)
        self.B = to3(self.L, self.E)                                 # (3, 3, 2) real basis of Lambda
        self.Bf = zf(self.B); self.Binv = np.linalg.inv(self.Bf)
        detB = zdet3(self.B[0], self.B[1], self.B[2]); detB = detB if zsign(detB) > 0 else -detB
        v6 = exact_volume6(self.P[0])
        assert all(np.array_equal(exact_volume6(p), v6) for p in self.P)
        self.N = zdiv_int(6*detB, v6); self.detB, self.vol6 = detB, v6
        G = self.L @ self.L.T; self.G = G
        self.Gi = [[Fr(int(x)) for x in row] for row in G]
        self.Ginv = np.array(self.inv3(G), dtype=object)
        self.R2 = R2
        # steps: all vertex differences inside templates (module coordinates)
        st = set()
        for t in T:
            for a in t:
                for b in t:
                    if not np.array_equal(a, b): st.add(tuple(int(x) for x in a - b))
        self.steps = np.array(sorted(st), dtype=np.int64)
    @staticmethod
    def inv3(G):
        M = [[Fr(int(x)) for x in row] for row in G]; n = 3
        A = [row + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
        for c in range(n):
            p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
            pv = A[c][c]; A[c] = [x/pv for x in A[c]]
            for r in range(n):
                if r != c and A[r][c] != 0:
                    f = A[r][c]; A[r] = [x - f*y for x, y in zip(A[r], A[c])]
        return [row[n:] for row in A]
    def tcoords(self, n):
        v = [int(x) for x in self.L @ np.asarray(n)]
        return [sum(self.Ginv[i][j]*v[j] for j in range(3)) for i in range(3)]
    def rep(self, n):
        t = self.tcoords(n); fl = [x.numerator // x.denominator for x in t]
        return tuple(int(x) for x in np.asarray(n) - np.array(fl, dtype=np.int64) @ self.L)
    def h2(self, n):
        t = self.tcoords(n); n = [int(x) for x in n]
        return Fr(sum(x*x for x in n)) - sum(t[i]*sum(int(self.G[i][j])*t[j] for j in range(3)) for i in range(3))
    def classes(self, cap=200000):
        start = self.rep([0]*self.k); seen = {start}; fr = [start]
        while fr:
            nf = []
            for c in fr:
                for s in self.steps:
                    n = np.array(c) + s
                    if self.k == 6 and self.h2(n) > self.R2: continue
                    r = self.rep(n)
                    if r not in seen: seen.add(r); nf.append(r)
            fr = nf
            if len(seen) > cap: raise RuntimeError('class cap')
        cl = sorted(seen, key=lambda c: (c != start, c)); return cl
    def reduce3(self, X):
        """X (n,3,2) exact points -> (X - lam, lam_int) with X - lam in the fundamental cell (float decision; any lattice shift is exact)"""
        fr = zf(X) @ self.Binv; m = np.floor(fr + 1e-12).astype(np.int64)
        lam = np.einsum('nj,jcd->ncd', m, self.B); return X - lam, m

def build(tor, max_samples, rng):
    cl = tor.classes(); say(f'classes {len(cl)}')
    X = to3(np.array(cl), tor.E)                       # apex positions (exact)
    X, _ = tor.reduce3(X)
    nT = len(tor.P)
    # self-overlap: template o against its own Lambda translates
    rmax = max(np.linalg.norm(zf(p.V), axis=1).max() for p in tor.P)
    K = int(np.ceil(2*rmax*np.linalg.norm(tor.Binv, axis=0).max())) + 1
    shifts = np.array([m for m in itertools.product(range(-K, K + 1), repeat=3)], dtype=np.int64)
    lamS = np.einsum('nj,jcd->ncd', shifts, tor.B)
    nz = np.any(shifts != 0, axis=1)
    good_o = []
    for o, p in enumerate(tor.P):
        U, hi, lo = pair_axes(p, p)
        ok = not overlap_many(U, hi, lo, lamS[nz]).any(); good_o.append(ok)
    say(f'templates usable (no overlap with own translates): {sum(good_o)}/{nT}')
    plc = [(o, c) for o in range(nT) if good_o[o] for c in range(len(cl))]
    say(f'placements {len(plc)}')
    m = tor.P[0].m
    # sample points = centroids of placements (times m), reduced to the cell
    S = np.array([m*X[c] + tor.P[o].centroid_num for o, c in plc]) if plc else np.zeros((0, 3, 2), np.int64)
    if len(S) > max_samples: S = S[rng.choice(len(S), max_samples, replace=False)]
    return cl, X, plc, S, shifts, lamS

class Incidence:
    """for sample points (times m), which placements contain them (closed / open), on the torus"""
    def __init__(self, tor, X, plc, shifts, lamS):
        self.tor, self.X, self.plc = tor, X, plc; self.m = tor.P[0].m
        self.byo = {}
        for i, (o, c) in enumerate(plc): self.byo.setdefault(o, []).append((i, c))
        # tree over apex images X_c + lam (lam over shifts)
        Xf = zf(X); Lf = zf(lamS)
        self.img = (Xf[:, None, :] + Lf[None]).reshape(-1, 3); self.tree = cKDTree(self.img)
        self.nS = len(lamS); self.lamS = lamS
        self.cen = [zf(p.centroid_num)/p.m for p in tor.P]; self.rad = [np.linalg.norm(zf(p.V) - zf(p.centroid_num)/p.m, axis=1).max() for p in tor.P]
    def contain(self, s):
        """s: (3,2) exact point times m. Returns (closed_list, open_list) of placement indices"""
        tor = self.tor; m = self.m
        sf = zf(s)/m; fr = sf @ tor.Binv; mm = np.floor(fr + 1e-12).astype(np.int64)
        s = s - m*np.einsum('j,jcd->cd', mm, tor.B); sf = zf(s)/m
        closed, opn = [], []
        for o, lst in self.byo.items():
            P = tor.P[o]; idx = self.tree.query_ball_point(sf - self.cen[o], self.rad[o] + 1e-6)
            if not idx: continue
            idx = np.array(idx); ci = idx // self.nS; li = idx % self.nS
            cls = {c: i for i, c in lst}
            keep = [(cls[c], c, l) for c, l in zip(ci, li) if c in cls]
            if not keep: continue
            Y = np.array([s - m*(self.X[c] + self.lamS[l]) for _, c, l in keep])
            ref = P.V[0] if P.ref_is_vertex else to3(P.n[0], tor.E)   # reference point offset (zero here)
            cin = contains_many(P, Y, m); oin = contains_open(P, Y, m)
            for (i, c, l), a, b in zip(keep, cin, oin):
                if a: closed.append(i)
                if b: opn.append(i)
        return sorted(set(closed)), sorted(set(opn))

def contains_open(P, Y, scale, tol=1e-9):
    if len(Y) == 0: return np.zeros(0, bool)
    f = zf(Y) @ zf(P.N).T; offf = scale*zf(P.off); marg = offf[None] - f
    sure_out = (marg < -tol).any(1); sure_in = (marg > tol).all(1)
    res = sure_in.copy(); amb = np.where(~sure_out & ~sure_in)[0]
    if len(amb):
        val = scale*P.off[None] - zdot(P.N[None], Y[amb][:, None]); res[amb] = (zsign(val) > 0).all(1)
    return res

def check_tiling(tor, X, plc, chosen, shifts, lamS):
    """exact pairwise check on the torus; returns list of overlapping pairs (i, j, lam index)"""
    bad = []; axc = {}
    for a, b in itertools.combinations_with_replacement(chosen, 2):
        oa, ca = plc[a]; ob, cb = plc[b]
        key = (oa, ob)
        if key not in axc: axc[key] = pair_axes(tor.P[oa], tor.P[ob])
        U, hi, lo = axc[key]
        D = (X[cb] - X[ca])[None] + lamS
        if a == b: D = D[np.any(shifts != 0, axis=1)]
        ov = overlap_many(U, hi, lo, D)
        if ov.any(): bad.append((a, b, int(np.where(ov)[0][0]) if a != b else None, D[np.where(ov)[0][0]]))
    return bad

def witness_point(tor, X, plc, a, b, d):
    """an interior point of piece a intersect (piece b translated by d relative to a), exact, times m; None if not found"""
    oa, ca = plc[a]; ob, _ = plc[b]; A, Bp = tor.P[oa], tor.P[ob]; m = A.m
    Af = zf(A.V); Bf = zf(Bp.V) + zf(d)
    # Chebyshev centre via LP
    from scipy.optimize import linprog
    H = []
    for P, sh in ((A, np.zeros(3)), (Bp, zf(d))):
        Nf = zf(P.N); off = zf(P.off) + Nf @ sh
        for n_, o_ in zip(Nf, off): H.append((n_, o_))
    Aub = np.array([[*n_, np.linalg.norm(n_)] for n_, o_ in H]); bub = np.array([o_ for n_, o_ in H])
    r = linprog([0, 0, 0, -1], A_ub=Aub, b_ub=bub, bounds=[(None, None)]*3 + [(0, None)])
    if not r.success or r.x[3] < 1e-7: return None
    c = r.x[:3]
    # round c to a nearby exact point of (1/m) Z[phi]^3 with small coefficients: use a vertex average of A shrunk toward c
    best = None
    for den in (m, 2*m, 4*m, 8*m, 16*m, 32*m):
        # exact candidate: (den*c) approximated in Z[phi]: a + b phi ~ value; choose b = 0, a = round
        q = np.array([[int(round(den*x)), 0] for x in c], dtype=np.int64)
        Y = (q*1)                                 # point = q / den, relative to apex of a
        ok1 = contains_open(A, Y[None], den)[0]
        ok2 = contains_open(Bp, (Y - den*d)[None], den)[0]
        if ok1 and ok2: best = (q, den); break
    if best is None: return None
    q, den = best
    # express as absolute point times m? we keep (abs point * den): abs = X[ca] + q/den
    return den*X[ca] + q, den

def solve(kind, lat, R2, tmax, out, max_samples=4000, seed=1):
    t0 = time.time(); rng = np.random.default_rng(seed)
    tor = Torus(kind, lat, R2)
    res = {'kind': kind, 'lattice': lat, 'R2': R2, 'vol6_piece': tor.vol6.tolist(), 'det_lattice': tor.detB.tolist(), 'N': tor.N}
    say(f'== {kind} lattice {lat} R2 {R2}: det(Lambda) = {tor.detB.tolist()} (a + b phi), 6 vol(piece) = {tor.vol6.tolist()}, N = {tor.N}')
    if tor.N is None or tor.N <= 0:
        res['verdict'] = 'UNSAT (N not an integer: volume)'; say(res['verdict']); json.dump(res, open(out + '.json', 'w'), indent=1); return res
    cl, X, plc, S, shifts, lamS = build(tor, max_samples, rng)
    res.update(classes=len(cl), placements=len(plc))
    if not plc: res['verdict'] = 'UNSAT (no placement fits in the torus)'; say(f'RESULT {kind} lattice {lat} R2 {R2} N {tor.N}: ' + res['verdict']); json.dump(res, open(out + '.json', 'w'), indent=1); return res
    inc = Incidence(tor, X, plc, shifts, lamS)
    m = tor.P[0].m
    samples = [(s, m) for s in S]
    pool = IDPool(start_from=len(plc) + 1)
    sol = Solver(name='cd195')
    def add_point(s, den):
        # point = s / den (absolute). Convert to the m scale used by Incidence: need s/den*m exact: use den-scaled tests directly
        sm = s if den == m else None
        if sm is None:
            # scale everything by den instead
            old = inc.m; inc.m = den; cl_, op_ = inc.contain(s); inc.m = old
        else:
            cl_, op_ = inc.contain(s)
        if not cl_: return 'empty'
        sol.add_clause([i + 1 for i in cl_])
        if len(op_) > 1:
            enc = CardEnc.atmost(lits=[i + 1 for i in op_], bound=1, vpool=pool, encoding=EncType.seqcounter)
            sol.append_formula(enc.clauses)
        return len(op_)
    nlit = 0
    for j, (s, den) in enumerate(samples):
        r = add_point(s, den)
        if r == 'empty': raise RuntimeError('sample point covered by no placement (should not happen for centroids)')
        nlit += r
        if j % 500 == 0: say(f'PROGRESS 0.1 encoding sample {j}/{len(samples)} ({time.time() - t0:.0f} s)')
    enc = CardEnc.equals(lits=list(range(1, len(plc) + 1)), bound=tor.N, vpool=pool, encoding=EncType.kmtotalizer)
    sol.append_formula(enc.clauses)
    sol.add_clause([i + 1 for i, (o, c) in enumerate(plc) if c == 0])
    say(f'encoded: {len(plc)} placement variables, {len(samples)} sample points, {nlit} open-incidences ({time.time() - t0:.0f} s)')
    rounds = 0; verdict = None; tiling = None
    while True:
        rounds += 1
        left = tmax - (time.time() - t0)
        if left <= 0: verdict = 'UNDECIDED (time cap)'; break
        tm = threading.Timer(left, sol.interrupt); tm.start()
        r = sol.solve_limited(expect_interrupt=True); tm.cancel()
        if r is None: verdict = 'UNDECIDED (time cap)'; break
        if r is False: verdict = 'UNSAT'; break
        model = sol.get_model(); chosen = [i for i in range(len(plc)) if model[i] > 0]
        bad = check_tiling(tor, X, plc, chosen, shifts, lamS)
        say(f'round {rounds}: model with {len(chosen)} pieces, {len(bad)} overlapping pairs ({time.time() - t0:.0f} s)')
        if not bad:
            verdict = 'SAT'; tiling = chosen; break
        added = 0
        for a, b, li, d in bad[:50]:
            w = witness_point(tor, X, plc, a, b, d)
            if w is None:
                # forbid this pair directly (exactly checked overlap): a clause, still a necessary condition
                sol.add_clause([-(a + 1), -(b + 1)]) if a != b else sol.add_clause([-(a + 1)]); added += 1; continue
            s, den = w; rr = add_point(s, den); added += 1
        say(f'  added {added} constraints')
    res.update(verdict=verdict, rounds=rounds, seconds=round(time.time() - t0, 1), samples=len(samples))
    if tiling is not None:
        # independent float check: random points covered exactly once (interiors) and at least once (closed)
        pts = rng.random((3000, 3)) @ tor.Bf
        cover = np.zeros(len(pts), int); inner = np.zeros(len(pts), int); Lf = zf(lamS)
        for i in tiling:
            o, c = plc[i]; P = tor.P[o]; Nf = zf(P.N); off = zf(P.off)
            Y = pts[:, None, :] - (zf(X[c])[None] + Lf)[None]          # (npts, nS, 3)
            g = Y @ Nf.T - off                                          # (npts, nS, faces)
            cover += (g <= 1e-9).all(-1).sum(1); inner += (g < -1e-9).all(-1).sum(1)
        res['random_points_in_open_pieces_max'] = int(inner.max())
        res['random_point_cover_counts'] = {int(k): int(v) for k, v in zip(*np.unique(cover, return_counts=True))}
        res['tiling'] = [{'template': int(plc[i][0]), 'apex_module_coords': list(map(int, cl[plc[i][1]])), 'apex_xyz': zf(X[plc[i][1]]).round(6).tolist(),
                          'apex_exact_a_b_per_coord': X[plc[i][1]].tolist()} for i in tiling]
        res['volume_check'] = f'{len(tiling)} x vol(piece) = vol(Lambda): {np.array_equal(len(tiling)*tor.vol6, 6*tor.detB)}'
    say(f'RESULT {kind} lattice {lat} R2 {R2} N {tor.N}: {verdict}' + (f" closed-cover counts {res.get('random_point_cover_counts')}, max open-cover {res.get('random_points_in_open_pieces_max')}" if tiling is not None else ''))
    json.dump(res, open(out + '.json', 'w'), indent=1)
    return res

if __name__ == '__main__':
    kind = sys.argv[1]; lat = [[int(x) for x in v.split(',')] for v in sys.argv[2].split(';')]
    solve(kind, lat, int(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
