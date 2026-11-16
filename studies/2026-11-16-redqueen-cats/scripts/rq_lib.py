#!/usr/bin/env python3
"""Shared tools for the 120-cell survey (DICTO, 16 Nov 2026): the 600-cell P and the 120-cell Q in sum-zero R^5 (S5 permutes
coordinates), W(H4) as permutations of P's 120 and Q's 600 corners together, the 10 inscribed 600-cells, the A4 reflection
subgroups (the S5s), congruent-copy search, plates (central hyperplanes of 2-faces) and exact 2D coverage of a face by fin cones.
Exact arithmetic: qlib (studies/2026-11-16-queens-construct/scripts), numbers a + b*phi with rational a, b.
Floats only PROPOSE (index matching); every claim used is re-checked exactly."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-16-queens-construct', 'scripts'))
from qlib import *   # noqa
import numpy as np

ONE = (Q5(1),)*5
def canon_dir(v):
    i = next(k for k in range(5) if not v[k].iszero()); return vkey(vscale(v[i].inv(), v))
def fkey(x): return tuple(np.round(x, 6) + 0.0)

class World:
    def __init__(s, log=print):
        P5, X, Y = build_600(); s.P5 = P5; s.X = X; s.Y = Y; n = len(P5)
        s.Pk = {vkey(p): i for i, p in enumerate(P5)}
        s.P4 = [to4(p) for p in P5]; s.PP = Poly(s.P4, '600-cell')
        s.Q4 = [tuple(sum((s.P4[i][c] for i in on), Q5())/4 for c in range(4)) for on, nn, d in s.PP.facets]
        s.Q5s = [to5(q) for q in s.Q4]; s.Qk = {vkey(q): i for i, q in enumerate(s.Q5s)}
        s.R2P = dot(P5[0], P5[0]); s.R2Q = dot(s.Q5s[0], s.Q5s[0])
        s.Pf = np.array([flt(p) for p in P5]); s.Qf = np.array([flt(q) for q in s.Q5s])
        s.antiP = np.array([s.Pk[vkey(vneg(p))] for p in P5]); s.antiQ = np.array([s.Qk[vkey(vneg(q))] for q in s.Q5s])
        s.axP = np.minimum(np.arange(120), s.antiP); s.axQ = np.minimum(np.arange(600), s.antiQ)
        # W(H4): reflections in P's corners, acting on P (0..119) and Q (120..719); generators checked exactly
        fk = {fkey(v): ('P', i) for i, v in enumerate(s.Pf)}; fk.update({fkey(v): ('Q', i) for i, v in enumerate(s.Qf)})
        gens = []; s.reflP = {}
        for a in sorted(set(s.axP.tolist())):
            m = s.Pf[a]; perm = []
            for i, v in enumerate(np.vstack([s.Pf, s.Qf])):
                r = v - 2*(v @ m)/(m @ m)*m; t, j = fk[fkey(r)]
                perm.append(j if t == 'P' else 120 + j)
            g = np.array(perm); gens.append(g); s.reflP[a] = g[:120]
        mm = s.R2P
        okx = True
        for a, g in zip(sorted(s.reflP), gens):
            m = P5[a]
            for i in range(0, 720, 37):
                v = P5[i] if i < 120 else s.Q5s[i - 120]
                r = vsub(v, vscale(2*dot(m, v)/mm, m)); j = g[i]
                okx &= vkey(r) == vkey(P5[j] if j < 120 else s.Q5s[j - 120])
        s.gen_exact = okx
        s.W = group_closure(gens)      # (14400, 720)
        s.mirror_axes = sorted(s.reflP)
        s.Mdir = {canon_dir(P5[a]): a for a in s.mirror_axes}
        s.Xdir = {canon_dir(s.Q5s[k]): k for k in sorted(set(s.axQ.tolist()))}

    def inscribed_600(s):
        Qf = s.Qf; m = 600; Rf = float(s.R2Q); fk = {fkey(Qf[i]): i for i in range(m)}; Gq = Qf @ Qf.T
        def fclosure(idx, cap_):
            S = set(idx); fr = set(idx)
            while fr:
                new = set()
                for a in S:
                    A = Qf[a]
                    for b in (S if a in fr else fr):
                        c = Qf[b] - 2*(A @ Qf[b])/(A @ A)*A; k = fkey(c)
                        if k not in fk: return None
                        j = fk[k]
                        if j not in S: new.add(j)
                S |= new; fr = new
                if len(S) > cap_: return None
            return frozenset(S)
        c36 = Rf*(1 + 5**.5)/4; found = set(); u = 0
        Wn = [w for w in range(m) if abs(Gq[u, w] - c36) < 1e-6]
        for a, b, c in itertools.combinations(Wn, 3):
            if abs(Gq[a, b] - c36) < 1e-6 and abs(Gq[a, c] - c36) < 1e-6 and abs(Gq[b, c] - c36) < 1e-6:
                S = fclosure([u, a, b, c], 120)
                if S is not None and len(S) == 120: found.add(S)
        GQ = s.W[:, 120:] - 120
        allS = set()
        for S in found:
            im = np.sort(GQ[:, sorted(S)], axis=1); allS |= {frozenset(r.tolist()) for r in np.unique(im, axis=0)}
        return sorted(allS, key=sorted)

    def exact_closed(s, S, pts=None):
        pts = pts or s.Q5s; L = [pts[i] for i in S]; K = {vkey(p) for p in L}; R2 = dot(L[0], L[0])
        return all(vkey(vsub(b, vscale(2*dot(a, b)/R2, a))) in K for a in L for b in L)

def find_copies(S, T, c, Tidx=None, first_target=None, maxn=None):
    """congruent copies of the exact point list S (scaled: inner products times c) among the exact points T (central, linear).
    Returns list of (frozenset of T indices, tuple image index per S point); each copy verified EXACTLY by the full Gram matrix.
    first_target: restrict S[0] -> that T index (use with a transitive symmetry of S)."""
    Sf = np.array([flt(p) for p in S]); Tf = np.array([flt(p) for p in T]); cf = float(c)
    Tidx = list(range(len(T))) if Tidx is None else list(Tidx)
    fk = {fkey(Tf[i]): i for i in Tidx}
    frame = [0]
    order = np.argsort(-(Sf @ Sf[0]))
    for j in order:
        if np.linalg.matrix_rank(Sf[frame + [j]], tol=1e-8) == len(frame) + 1: frame.append(int(j))
        if len(frame) == 4: break
    G = cf*(Sf[frame] @ Sf[frame].T); A = Sf[frame]
    GT = Tf @ Tf.T
    out = {}; starts = [first_target] if first_target is not None else Tidx
    Tset = np.array(Tidx)
    for q0 in starts:
        if abs(GT[q0, q0] - G[0, 0]) > 1e-6: continue
        c1 = Tset[np.abs(GT[q0, Tset] - G[0, 1]) < 1e-6]
        for q1 in c1:
            c2 = Tset[(np.abs(GT[q0, Tset] - G[0, 2]) < 1e-6) & (np.abs(GT[q1, Tset] - G[1, 2]) < 1e-6)]
            for q2 in c2:
                c3 = Tset[(np.abs(GT[q0, Tset] - G[0, 3]) < 1e-6) & (np.abs(GT[q1, Tset] - G[1, 3]) < 1e-6) & (np.abs(GT[q2, Tset] - G[2, 3]) < 1e-6)]
                for q3 in c3:
                    B = Tf[[q0, q1, q2, q3]]
                    M = np.linalg.lstsq(A, B, rcond=None)[0]   # rows: x A -> x B ; images = Sf @ M
                    im = Sf @ M; idx = []
                    for v in im:
                        j = fk.get(fkey(v))
                        if j is None: break
                        idx.append(j)
                    if len(idx) == len(S):
                        key = frozenset(idx)
                        if key not in out: out[key] = tuple(idx)
                        if maxn and len(out) >= maxn: break
    res = []
    for key, idx in out.items():
        ok = all(dot(T[idx[a]], T[idx[b]]) == c*dot(S[a], S[b]) for a in range(len(S)) for b in range(a, len(S)))
        assert ok, 'float copy failed the exact Gram check'
        res.append((key, idx))
    return res

def lin_map(src, dst):
    """exact linear map on sum-zero R^5 sending the 4 independent vectors src[k] to dst[k]; returns a function on 5-vectors"""
    A = [to4(v) for v in src]; B = [to4(v) for v in dst]
    # find 4x4 L with L a_k = b_k : solve for rows of L: for each output coord r, L[r] . a_k = b_k[r]
    L = [solve(A, [B[k][r] for k in range(4)]) for r in range(4)]
    def f(v):
        y = to4(v); return to5(tuple(dot(L[r], y) for r in range(4)))
    return f

def faces_of(poly):
    """2-faces of a Poly as dicts: pts (5D, cyclic order), normal n (5D) and its canonical direction key"""
    out = []
    for g in poly.two:
        es = poly.gedges[g]; adj = {}
        for e in es:
            a, b = tuple(e); adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        start = min(g); cyc = [start]; prev = None
        while len(cyc) < len(g):
            nx = [x for x in adj[cyc[-1]] if x != prev and x not in cyc][0]; prev = cyc[-1]; cyc.append(nx)
        pts = [to5(poly.P[i]) for i in cyc]
        n = cofactor_normal([pts[0], pts[1], pts[2], ONE])
        out.append({'pts': pts, 'n': n, 'dir': canon_dir(n), 'vidx': tuple(cyc)})
    return out

def kind_of(poly):
    """heart / inherited heart / non-heart, from 2-faces per plate and central symmetry"""
    fs = faces_of(poly); cnt = {}
    for f in fs: cnt[f['dir']] = cnt.get(f['dir'], 0) + 1
    K = {vkey(to5(p)) for p in poly.P}; csym = all(vkey(vneg(to5(p))) in K for p in poly.P)
    mx, mn = max(cnt.values()), min(cnt.values())
    kind = 'heart' if csym else ('inherited heart' if mx >= 2 else 'non-heart')
    return {'faces': len(fs), 'plates': len(cnt), 'faces_per_plate_min': mn, 'faces_per_plate_max': mx, 'central_symmetry': csym,
            'kind': kind}, cnt, fs

# ---------------- exact 2D coverage of a planar polygon F by fin cones ----------------
def cone_ineqs(f, finite):
    """fin cone over face f (dict with pts, n) as inequalities s.y >= 0 (and u.y <= d for the finite fin: -u.y + d >= 0)"""
    pts = f['pts']; n = f['n']; cen = tuple(sum((p[c] for p in pts), Q5()) for c in range(5)); ineq = []
    for k in range(len(pts)):
        a, b = pts[k], pts[(k + 1) % len(pts)]
        sv = cofactor_normal([ONE, n, a, b])
        if dot(sv, cen).sign() < 0: sv = vneg(sv)
        ineq.append((sv, Q5(0)))          # sv.y + 0 >= 0
    if finite:
        u = cofactor_normal([ONE, n, vsub(pts[1], pts[0]), vsub(pts[2], pts[0])]); d = dot(u, pts[0])
        if d.sign() < 0: u = vneg(u); d = -d
        ineq.append((vneg(u), d))         # -u.y + d >= 0
    return ineq

def _clip(poly, a, b, c):
    """keep a + b x + c y >= 0 of a convex 2D polygon (list of (x, y) Q5)"""
    out = []; m = len(poly)
    if m == 0: return out
    val = [a + b*p[0] + c*p[1] for p in poly]
    for k in range(m):
        p, q = poly[k], poly[(k + 1) % m]; vp, vq = val[k], val[(k + 1) % m]
        if vp.sign() >= 0: out.append(p)
        if vp.sign()*vq.sign() < 0:
            t = vp/(vp - vq); out.append((p[0] + t*(q[0] - p[0]), p[1] + t*(q[1] - p[1])))
    # drop duplicates
    res = []
    for p in out:
        if not res or not (res[-1][0] == p[0] and res[-1][1] == p[1]): res.append(p)
    if len(res) > 1 and res[0][0] == res[-1][0] and res[0][1] == res[-1][1]: res.pop()
    return res

def area2(poly):
    s = Q5()
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]; s = s + p[0]*q[1] - q[0]*p[1]
    return s/2 if s.sign() >= 0 else -s/2

def coverage(F, fins, finite=False):
    """fraction of the area of planar polygon F (cyclic 5D points) covered by the union of the fin cones; fins whose plate is not
    F's plate are ignored (they meet F in measure zero). Returns (fraction, number of fins that cover positive area, uncovered pieces)"""
    F0 = F[0]; e1 = vsub(F[1], F0); e2 = vsub(F[2], F0)
    Gm = [[dot(e1, e1), dot(e1, e2)], [dot(e1, e2), dot(e2, e2)]]
    F2 = [tuple(solve(Gm, [dot(e1, vsub(p, F0)), dot(e2, vsub(p, F0))])) for p in F]
    total = area2(F2); unc = [F2]; used = 0
    for f in fins:
        lines = [(dot(sv, F0) + d, dot(sv, e1), dot(sv, e2)) for sv, d in cone_ineqs(f, finite)]
        if any(b.iszero() and c.iszero() and a.sign() < 0 for a, b, c in lines): continue
        lines = [(a, b, c) for a, b, c in lines if not (b.iszero() and c.iszero())]   # constant on F's plane and >= 0: no cut
        Cp = F2
        for L in lines: Cp = _clip(Cp, *L)
        if len(Cp) < 3 or area2(Cp).iszero(): continue
        used += 1; new = []
        for piece in unc:
            rest = piece
            for (a, b, c) in lines:
                outside = _clip(rest, -a, -b, -c)
                if len(outside) >= 3 and not area2(outside).iszero(): new.append(outside)
                rest = _clip(rest, a, b, c)
                if len(rest) < 3: break
        unc = new
    ua = sum((area2(p) for p in unc), Q5())
    return (total - ua)/total, used, unc

def edge_coverage(e0, e1, fins, finite=False):
    """fraction of the length of edge e0e1 covered by the fin cones whose plates contain the edge"""
    d = vsub(e1, e0); iv = []
    for f in fins:
        if not (dot(f['n'], e0).iszero() and dot(f['n'], e1).iszero()): continue
        lo, hi = Q5(0), Q5(1); ok = True
        for sv, c in cone_ineqs(f, finite):
            a = dot(sv, e0) + c; b = dot(sv, d)       # a + b t >= 0
            if b.iszero():
                if a.sign() < 0: ok = False; break
            elif b.sign() > 0: t = -a/b; lo = t if lo < t else lo
            else: t = -a/b; hi = t if t < hi else hi
        if ok and lo < hi: iv.append((lo, hi))
    import functools
    iv.sort(key=functools.cmp_to_key(lambda x, y: (x[0] - y[0]).sign()))
    tot = Q5(); cur = None
    for lo, hi in iv:
        if cur is None: cur = [lo, hi]
        elif not (cur[1] < lo): cur[1] = hi if cur[1] < hi else cur[1]
        else: tot = tot + cur[1] - cur[0]; cur = [lo, hi]
    if cur: tot = tot + cur[1] - cur[0]
    return tot, len(iv)
