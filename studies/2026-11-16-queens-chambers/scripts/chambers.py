#!/usr/bin/env python3
"""STUDY 2 (DICTO 16 Nov 2026: "if these are the structure where are the shapes"): the Queens' wall system (60 mirrors +
300 cross walls) taken as the structure; the chambers it cuts the 600-cell and the 120-cell into.

Method (symmetry): every chamber of the 360-wall arrangement lies inside one chamber C of W(H4) (the 60 mirrors are among
the walls) and W(H4) moves C onto each of its 14400 images, so  #chambers = 14400 x #(regions of C cut by the cross walls
that pass through its interior).  Inside C the 600-cell is the pyramid from the centre over one 1/24 of a tetrahedral cell
(the cell's own orthoscheme), and the 120-cell the pyramid over 1/120 of a dodecahedral cell; so every chamber is the
pyramid from the centre over one piece of a cell cut by the walls.
Counts: (1) exact in Q(sqrt5): Zaslavsky's count of the regions of the open simplex section of C (sum of |Moebius| over the
flats that meet it; lines and points found exactly, incidences decided exactly); (2) float: direct splitting of the cell
piece by each wall plane; (3) float: the whole 360-hyperplane intersection lattice of R^4 (sum of |Moebius| over all flats),
which must equal 14400 x (1).  Control: mirrors alone, exact lattice of the 60 mirrors = 14400 = |W(H4)| = 2*12*20*30.
Then A and B: their plate subsystems, the group those walls generate, and the chambers they cut A and B into.
usage: python3 chambers.py [part ...]  parts: control cross ab ; FINAL ok only if every check passes.
"""
import os, sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-16-queens-vicinity-vacuus', 'scripts'))
from qv_lib import *   # noqa: F401,F403
import qv_lib as L

CHECKS, OUT, T0 = [], {}, time.time()


def check(name, ok):
    CHECKS.append((name, bool(ok))); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def say(*a):
    print(*a, f'({time.time() - T0:.0f}s)', flush=True)


def dirs(vs):
    d = {}
    for v in vs:
        c = canon(v); d.setdefault(key(c), c)
    return list(d.values())


MIR = dirs(V600)
CRS = dirs(C600)


def dep3(a, b, c):
    return all(x.iszero() for x in cross4(a, b, c))


# ------------------------------------------------------------------ exact lattice count for a central arrangement in R^4
def regions_exact(N):
    """number of regions of the central arrangement {n-perp : n in N} in R^4 (exact; sum of |Moebius| over the lattice)."""
    n = len(N)
    flats2 = {}   # frozenset of hyperplanes containing the 2-flat
    for i, j in itertools.combinations(range(n), 2):
        S = frozenset(k for k in range(n) if dep3(N[i], N[j], N[k]))
        flats2[S] = 1
    lines = {}
    for S in flats2:
        i, j = sorted(S)[:2]
        for k in range(n):
            if k in S:
                continue
            d = canon(cross4(N[i], N[j], N[k]))
            kd = key(d)
            if kd not in lines:
                lines[kd] = frozenset(m for m in range(n) if dot(N[m], d).iszero())
    mu2 = {S: len(S) - 1 for S in flats2}
    total_mu_lines = 0
    for kd, H in lines.items():
        f2 = [S for S in flats2 if S <= H]
        mu = -(1 - len(H) + sum(mu2[S] for S in f2))
        total_mu_lines += mu
    mu0 = -(1 - n + sum(mu2.values()) + total_mu_lines)
    r = 1 + n + sum(mu2.values()) + (-total_mu_lines) + mu0
    return r, {'hyperplanes': n, 'flats2': len(flats2), 'lines': len(lines), 'chi': [1, -n, sum(mu2.values()), total_mu_lines, mu0]}


# ------------------------------------------------------------------ exact Zaslavsky count inside the open chamber C
def cutting(walls, rays):
    """walls whose hyperplane meets the open cone spanned by rays (mixed strict signs)."""
    out = []
    for w in walls:
        s = {dot(w, r).sign() for r in rays}
        if 1 in s and -1 in s:
            out.append(w)
    return out


def open_halfplane(a):
    """exists s in R^2 with a_i . s > 0 for every a_i (exact)."""
    if any(x[0].iszero() and x[1].iszero() for x in a):
        return False
    cands = list(a) + [(-x[1], x[0]) for x in a] + [(x[1], -x[0]) for x in a]
    cands2 = cands + [(p[0] + q[0], p[1] + q[1]) for p, q in itertools.combinations(cands, 2)]
    for s in cands2:
        if all((x[0] * s[0] + x[1] * s[1]).sign() > 0 for x in a):
            return True
    return False


def nullspace(rows, n=4):
    """exact nullspace basis of rows (list of n-vectors)."""
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]; iv = M[r][c].inv(); M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    B = []
    for f in free:
        v = [ZERO] * n; v[f] = ONE
        for i, c in enumerate(piv):
            v[c] = -M[i][f]
        B.append(tuple(v))
    return B


def regions_in_chamber(P):
    """P: list of linear forms on barycentric t (t_i > 0, sum 1): regions of the open simplex (exact Zaslavsky)."""
    n = len(P)
    # lines: 2D subspaces U = {t: p_k.t = p_l.t = 0}; meets the open orthant iff its basis rows admit a positive combination
    lines = {}
    for k, l in itertools.combinations(range(n), 2):
        U = nullspace([P[k], P[l]])
        if len(U) != 2:
            continue
        H = frozenset(m for m in range(n) if dot(P[m], U[0]).iszero() and dot(P[m], U[1]).iszero())
        if H in lines:
            continue
        a = [(U[0][i], U[1][i]) for i in range(4)]
        lines[H] = open_halfplane(a)
    inside_lines = [H for H, ok in lines.items() if ok]
    # points: rays {t: three forms vanish}, inside iff all t_i of one strict sign
    pts = {}
    for k, l, m in itertools.combinations(range(n), 3):
        U = nullspace([P[k], P[l], P[m]])
        if len(U) != 1:
            continue
        u = U[0]; sg = {x.sign() for x in u}
        if sg not in ({1}, {-1}):
            continue
        H = frozenset(q for q in range(n) if dot(P[q], u).iszero())
        pts[H] = 1
    mu_pts = 0
    for H in pts:
        # lines through the point: distinct line flats among pairs of its planes
        Ls = set()
        for k, l in itertools.combinations(sorted(H), 2):
            LH = next(F for F in lines if k in F and l in F and F <= H)
            Ls.add(LH)
        mu_pts += sum(len(F) - 1 for F in Ls) - len(H) + 1
    r = 1 + n + sum(len(F) - 1 for F in inside_lines) + mu_pts
    return r, {'planes': n, 'lines_inside': len(inside_lines), 'points_inside': len(pts), 'points_multiple': sum(len(H) > 3 for H in pts),
               'lines_multiple': sum(len(F) > 2 for F in inside_lines)}


# ------------------------------------------------------------------ float pieces of a cell
def split(regions, a, b, eps=1e-9):
    out = []
    for R in regions:
        s = R @ a + b
        if s.max() <= eps or s.min() >= -eps:
            out.append(R); continue
        pos, neg_ = R[s > eps], R[s < -eps]; on = R[np.abs(s) <= eps]
        sp, sn = s[s > eps], s[s < -eps]
        X = [(p * (-q) + n_ * pp) / (pp - q) for p, pp in zip(pos, sp) for n_, q in zip(neg_, sn)]
        X = np.array(X)
        for side in (pos, neg_):
            Q = np.vstack([side, on, X]) if len(on) else np.vstack([side, X])
            h = ConvexHull(Q)
            out.append(Q[h.vertices])
    return out


def poly3(R):
    h = ConvexHull(R)
    eq = {}; fid = []
    sc = np.max(np.linalg.norm(R - R.mean(0), axis=1))
    for e in h.equations:
        k = tuple(np.round(e / [1, 1, 1, sc], 6) + 0.0); fid.append(eq.setdefault(k, len(eq)))
    fv = [set() for _ in eq]
    for j, s in enumerate(h.simplices):
        fv[fid[j]].update(s.tolist())
    edges = set()
    for j, nb in enumerate(h.neighbors):
        for k in nb:
            if fid[j] != fid[k]:
                edges.add(frozenset(fv[fid[j]] & fv[fid[k]]))
    V = len(h.vertices)
    sizes = sorted(len(f) for f in fv)
    return {'V': V, 'E': len(edges), 'F': len(fv), 'faces': {str(k): sizes.count(k) for k in sorted(set(sizes))}, 'vol': h.volume}


def invariant(P):
    d = np.linalg.norm(P[:, None] - P[None], axis=2)
    return tuple(np.round(np.sort(d[np.triu_indices(len(P), 1)]), 6))


def cell_pieces(name, facet_dir, walls, rays):
    """the cell piece cone(C) & facet plane, cut by every wall; returns pieces (3D) with 4D pyramid data."""
    c = facet_dir
    cf = fl(c); cc = float(dot(c, c))
    B = basis3(c)                                     # orthonormal basis of c-perp
    corners = []
    for r in rays:
        rf = fl(r); x = rf * cc / (rf @ cf)           # ray meets the facet plane c.x = |c|^2
        corners.append((x - cf) @ B)
    R0 = np.array(corners)
    regs = [R0]
    for w in walls:
        wf = fl(w); regs = split(regs, B.T @ wf, wf @ cf)
    pieces = []
    h4 = np.sqrt(cc)
    for R in regs:
        p = poly3(R)
        P4 = np.vstack([np.zeros(4), (R @ B.T) + cf])   # apex 0 and the base in R^4
        p4 = {'V': p['V'] + 1, 'E': p['E'] + p['V'], 'F2': p['F'] + p['E'], 'F3': 1 + p['F'], 'vol4': p['vol'] * h4 / 4}
        pieces.append({'base': p, 'chamber': p4, 'inv': invariant(P4), 'inv3': invariant(R)})
    vol = ConvexHull(R0).volume
    check(f'{name}: pieces fill the cell orthoscheme (volume sum)', abs(sum(q['base']['vol'] for q in pieces) - vol) < 1e-9 * max(1, vol))
    cls = {}
    for q in pieces:
        cls.setdefault(q['inv'], []).append(q)
    classes = []
    for i, (k, qs) in enumerate(sorted(cls.items(), key=lambda kv: (-len(kv[1]), kv[1][0]['base']['V']))):
        q = qs[0]
        classes.append({'class': i + 1, 'in_one_chamber_C': len(qs), 'base': q['base'], 'chamber': q['chamber']})
    # classes up to congruence of the 3D bases as well (two 4D classes may share a base shape)
    return pieces, classes, vol


def lattice_float(N, tol=1e-9):
    """float sum of |Moebius| for a central arrangement in R^4 (the whole lattice)."""
    N = np.array([fl(n) / np.linalg.norm(fl(n)) for n in N]); n = len(N)
    flats2 = {}
    for i in range(n):
        for j in range(i + 1, n):
            Q, _ = np.linalg.qr(N[[i, j]].T)
            res = N - (N @ Q) @ Q.T
            S = frozenset(np.nonzero(np.linalg.norm(res, axis=1) < 1e-7)[0].tolist())
            flats2[S] = 1
    lines = {}
    for S in flats2:
        i, j = sorted(S)[:2]
        for k in range(n):
            if k in S:
                continue
            _, _, vt = np.linalg.svd(N[[i, j, k]]); d = vt[3]
            H = frozenset(np.nonzero(np.abs(N @ d) < 1e-7)[0].tolist())
            lines[H] = 1
    mu2 = {S: len(S) - 1 for S in flats2}
    s2 = sum(mu2.values())
    # rank-2 flats inside each line: index by pair
    pair2 = {}
    for S in flats2:
        for p in itertools.combinations(sorted(S), 2):
            pair2[p] = S
    tl = 0
    for H in lines:
        f2 = {pair2[p] for p in itertools.combinations(sorted(H), 2)}
        tl += -(1 - len(H) + sum(mu2[S] for S in f2))
    mu0 = -(1 - n + s2 + tl)
    return 1 + n + s2 - tl + mu0, {'flats2': len(flats2), 'lines': len(lines), 'chi': [1, -n, s2, tl, mu0]}


# ------------------------------------------------------------------ parts
RAYS = OMEGA   # rays of C: omega_1 (600-cell cell centre / 120-cell corner), ..., omega_4 (600-cell corner)


def parallel(a, b):
    """same direction (equality in Cauchy-Schwarz, exact)."""
    return dot(a, b).sign() > 0 and dot(a, b) * dot(a, b) == dot(a, a) * dot(b, b)


# the true facet centres inside C: the 600-cell's cell centre on the omega_1 ray; the 120-cell's dodecahedral cell centre
# (centroid of the 20 tetrahedron centres round one 600-cell corner) on the omega_4 ray
FC600 = next(c for c in C600 if parallel(c, OMEGA[0]))
_v = next(i for i, v in enumerate(V600) if parallel(v, OMEGA[3]))
_ring = [C600[j] for j, c in enumerate(CELLS600) if _v in c]
FC120 = tuple(sum((p[k] for p in _ring), ZERO) * Q5(Fr(1, len(_ring))) for k in range(4))
FACET = {'600-cell': FC600, '120-cell': FC120}


def part_control():
    r, info = regions_exact(MIR)
    say('mirrors alone, exact lattice:', r, info)
    check('control: the 60 mirrors cut R^4 into 14400 chambers = |W(H4)| (exact)', r == 14400)
    check('control: characteristic polynomial (t-1)(t-11)(t-19)(t-29) (exact)', info['chi'] == [1, -60, 1 * 11 + 1 * 19 + 1 * 29 + 11 * 19 + 11 * 29 + 19 * 29, -(1 * 11 * 19 + 1 * 11 * 29 + 1 * 19 * 29 + 11 * 19 * 29), 1 * 11 * 19 * 29])
    check('control: no mirror meets the open chamber C', cutting(MIR, RAYS) == [])
    for nm, fdir in FACET.items():
        pieces, classes, vol = cell_pieces(f'{nm}, mirrors only', fdir, [], RAYS)
        check(f'control {nm}: one chamber per W(H4) chamber (one class, 14400 chambers)', len(pieces) == 1)
        full = ConvexHull(np.array([fl(v) for v in (V600 if nm == '600-cell' else C600)])).volume
        check(f'control {nm}: 14400 x chamber volume = volume of the {nm}', abs(14400 * classes[0]['chamber']['vol4'] - full) < 1e-8 * full)
        OUT[f'control_{nm}'] = {'chambers': 14400 * len(pieces), 'classes': classes}
        say(nm, 'mirrors only:', classes)


def part_cross():
    cut = cutting(CRS, RAYS)
    touch = [w for w in CRS if w not in cut and any(dot(w, r).iszero() for r in RAYS)]
    say('cross walls through the open chamber C:', len(cut), '; touching its boundary only:', len(touch))
    P = [tuple(dot(w, r) for r in RAYS) for w in cut]          # barycentric linear forms
    r, info = regions_in_chamber(P)
    say('exact regions of C:', r, info)
    OUT['cross'] = {'walls_cutting_C': len(cut), 'regions_in_C_exact': r, 'zaslavsky': info, 'chambers_total': 14400 * r}
    for nm, fdir in FACET.items():
        pieces, classes, vol = cell_pieces(f'{nm}, 60 mirrors + 300 cross walls', fdir, cut, RAYS)
        check(f'{nm}: float splitting gives the exact count {r}', len(pieces) == r)
        OUT['cross'][nm] = {'chambers': 14400 * len(pieces), 'classes_in_C': len(classes), 'classes': classes,
                            'cell_pieces_per_cell': len(pieces) * (24 if nm == '600-cell' else 120)}
        say(nm, 'pieces in C', len(pieces), 'congruence classes (4D invariants)', len(classes))
        full = ConvexHull(np.array([fl(v) for v in (V600 if nm == '600-cell' else C600)])).volume
        check(f'{nm}: 14400 x (sum of chamber volumes in C) = volume of the {nm}', abs(14400 * sum(q['chamber']['vol4'] for q in pieces) - full) < 1e-8 * full)
        comb = {}
        for c in classes:
            k = (c['chamber']['V'], c['chamber']['E'], c['chamber']['F2'], c['chamber']['F3'], json.dumps(c['base']['faces']))
            comb[k] = comb.get(k, 0) + c['in_one_chamber_C']
        OUT['cross'][nm]['combinatorial_types'] = [{'chamber_f': list(k[:4]), 'base_faces': json.loads(k[4]), 'pieces_in_C': v} for k, v in sorted(comb.items())]
        vols = sorted(q['chamber']['vol4'] for q in pieces)
        OUT['cross'][nm]['vol_ratio_max_min'] = vols[-1] / vols[0]
        say(nm, 'combinatorial types:', len(comb), 'largest/smallest chamber volume', round(vols[-1] / vols[0], 2))
        for k, v in sorted(comb.items()):
            print('   chamber (V,E,F2,F3)', k[:4], 'base faces', k[4], 'x', v, flush=True)
    rf, finfo = lattice_float(MIR + CRS)
    say('float whole lattice of the 360 walls:', rf, finfo)
    check('float whole-lattice count of the 360-wall arrangement = 14400 x exact regions of C', rf == 14400 * r)
    OUT['cross']['lattice_float'] = {'regions': rf, **finfo}
    check('the 120-cell adds no cell-parallel walls of its own (its cell centres point along 600-cell corners = the mirrors)',
          {key(canon(v)) for v in V600} == MIRROR)


def part_ab():
    """the plate subsystems of A and B (W(A4) orbits of the 600-cell's corners, see study 1 part ab) as structures."""
    import study1 as S1
    gens = [S1.perm_of_reflection(a) for a in ALPHA]
    v0 = V600[0]
    sr = None
    for a2 in range(120):
        if dot(V600[a2], v0) != Q5(-2): continue
        for a3 in range(120):
            if dot(V600[a3], V600[a2]) != Q5(-2) or not dot(V600[a3], v0).iszero(): continue
            for a4 in range(120):
                if dot(V600[a4], V600[a3]) == Q5(-2) and dot(V600[a4], v0).iszero() and dot(V600[a4], V600[a2]).iszero():
                    t = [v0, V600[a2], V600[a3], V600[a4]]
                    rs = set()
                    for g0 in t:
                        rs |= {key(x) for x in orbit(g0, t, cap=200)}
                    if len(rs) == 20:
                        sr = t; break
            if sr: break
        if sr: break
    W = S1.group([S1.perm_of_reflection(a) for a in sr])
    orbs = S1.orbits_on(W, 120, lambda g, i: g[i])
    p = (1 + 5 ** .5) / 2
    def spec(P):
        P = np.array([fl(x) for x in P]); P = P - P.mean(0); g = P @ P.T; g = g / np.max(np.diag(g)); return np.sort(np.round(g.ravel(), 7))
    def spec5(S):
        S = S - S.mean(0); g = S @ S.T; g = g / np.max(np.diag(g)); return np.sort(np.round(g.ravel(), 7))
    sA = spec5(np.array(sorted(set(itertools.permutations((p * p, p * p, p * p, p, 0))))))
    sB = spec5(np.array(sorted(set(itertools.permutations((p * p, p * p, 1, 1, 0))))))
    A = next([V600[i] for i in o] for o in orbs if len(o) == 20 and np.allclose(spec([V600[i] for i in o]), sA))
    B = next([V600[i] for i in o] for o in orbs if len(o) == 30 and np.allclose(spec([V600[i] for i in o]), sB))
    res = {}
    for nm, X in (('A', A), ('B', B)):
        Xf = np.array([fl(v) for v in X])
        fac, rid, _ = L.lattice(Xf)
        plates = {}
        for r_ in rid:
            a, b, c = L.three_independent(Xf, r_)
            n = canon(cross4(X[a], X[b], X[c])); plates.setdefault(key(n), n)
        N = list(plates.values())
        kinds = [wall_kind(n) for n in N]
        mir = [n for n, k in zip(N, kinds) if k == 'mirror']; crs = [n for n, k in zip(N, kinds) if k == 'cross']
        # the group generated by the reflections in the plates: closure of the plate set under its own reflections
        def closure(S, cap=400):
            # stops as soon as more than cap distinct walls appear (cross-wall reflections need not close up)
            D = {key(canon(n)): n for n in S}; grow = True
            while grow and len(D) <= cap:
                grow = False; Lst = list(D.values())
                for a in Lst:
                    for b in Lst:
                        y = canon(reflect(b, a)); k = key(y)
                        if k not in D:
                            D[k] = y; grow = True
                            if len(D) > cap:
                                return D
            return D
        clm = closure(mir)
        ent = {'plates': len(N), 'mirror': len(mir), 'cross': len(crs), 'mirror_closure': len(clm),
               'mirror_subsystem_closed': len(clm) == len(mir)}
        if crs:
            clc = closure(crs); ent['cross_closure'] = len(clc); clall = closure(N); ent['all_closure'] = len(clall)
            ent['cross_closure_stays_in_queen_walls'] = all(k in MIRROR or k in CROSS for k in clc)
            ent['all_closure_stays_in_queen_walls'] = all(k in MIRROR or k in CROSS for k in clall)
        r_all, i_all = regions_exact(N)
        ent['chambers_own_walls'] = r_all; ent['chi'] = i_all['chi']
        if crs:
            ent['chambers_mirror_part'] = regions_exact(mir)[0]; ent['chambers_cross_part'] = regions_exact(crs)[0]
        # do the own walls cut through the cone over any cell (facet) of the solid?  (exact sign test on the facet's corners)
        cuts = []
        for F in fac:
            cuts.append(sum(1 for n in N if len({dot(n, X[i]).sign() for i in F} - {0}) == 2))
        ent['cells'] = len(fac); ent['walls_through_each_cell'] = sorted(cuts)
        # chambers inside the solid: pieces of each facet cut by the walls through it (float), pyramids from the centre
        pieces = []
        for F, ncut in zip(fac, cuts):
            ids = sorted(F); Pf = Xf[ids]
            # 3D frame of the facet hyperplane
            nrm = np.linalg.svd(Pf - Pf.mean(0))[2][3]; Bf = np.linalg.svd(Pf - Pf.mean(0))[2][:3].T; o = Pf.mean(0)
            regs = [ (Pf - o) @ Bf ]
            for n in N:
                if len({dot(n, X[i]).sign() for i in F} - {0}) == 2:
                    nf = fl(n); regs = split(regs, Bf.T @ nf, nf @ o)
            for R in regs:
                P4 = np.vstack([np.zeros(4), R @ Bf.T + o])
                pieces.append({'cell_size': len(F), 'base': poly3(R), 'inv': invariant(P4)})
        cls = {}
        for q in pieces:
            cls.setdefault(q['inv'], []).append(q)
        ent['pieces_in_solid'] = len(pieces)
        # is any piece congruent to the H4 Coxeter chamber of the 600-cell or of the 120-cell (the Queens' own chambers)?
        ref = {q: cell_pieces(f'reference {q} chamber', FACET[q], [], RAYS)[0][0]['inv'] for q in FACET}
        ent['pieces_equal_to_queen_chambers'] = {q: sum(len(v) for k, v in cls.items() if len(k) == len(r_) and np.allclose(k, r_, atol=1e-6)) for q, r_ in ref.items()}
        say(nm, 'pieces congruent to the Queens chambers (distance test):', ent['pieces_equal_to_queen_chambers'])
        ent['piece_classes'] = [{'count': len(v), 'from_cell_with_corners': v[0]['cell_size'], 'base': v[0]['base'],
                                 'chamber_f': [v[0]['base']['V'] + 1, v[0]['base']['E'] + v[0]['base']['V'], v[0]['base']['F'] + v[0]['base']['E'], 1 + v[0]['base']['F']]}
                                for v in sorted(cls.values(), key=lambda v: -len(v))]
        check(f'{nm}: chambers inside the solid = chambers of its own walls (every chamber meets the solid)', len(pieces) == r_all)
        res[nm] = ent
        say(nm, {k: v for k, v in ent.items() if k != 'piece_classes'})
        for c in ent['piece_classes']:
            print('   ', c, flush=True)
    check('A: 30 plates all mirrors; B: 40 mirrors + 40 cross', (res['A']['plates'], res['A']['mirror']) == (30, 30) and (res['B']['mirror'], res['B']['cross']) == (40, 40))
    OUT['ab'] = res


if __name__ == '__main__':
    parts = sys.argv[1:] or ['control', 'cross', 'ab']
    for i, p_ in enumerate(parts):
        print('== part', p_, flush=True)
        globals()['part_' + p_]()
        print(f'PROGRESS {(i + 1) / len(parts):.2f} {p_}', flush=True)
    tag = '-'.join(parts)
    json.dump({'out': OUT, 'checks': CHECKS}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'chambers-{tag}.json'), 'w'), indent=1, default=str)
    bad = [c for c in CHECKS if not c[1]]
    print('checks', len(CHECKS), 'failed', bad)
    print('FINAL ok' if CHECKS and not bad else 'FINAL FAIL')
