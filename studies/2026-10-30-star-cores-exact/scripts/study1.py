# Star Cores study 1 (DICTO 2026-10-30 "go ahead with study 1"): exact work in the solids' own fields (Q(sqrt5), Q, Q(cbrt2)).
# Part 1, DICTO's growth rule T of #38, T(S) = {x : v.x <= v.v for every corner v}, run exactly on the ten solids whose chains closed in
# the float survey (survey2): each step's corners, faces and volume; the return after the period checked exactly (the corners of step p
# are k times the corners of step 0, k the radius gain), and the gain given exactly.
# Part 2, the polar-spike fill (results report, conclusion 1), checked exactly on the same solids: tips at the poles of the face planes in
# the sphere rho^2 = t R^2; every piece (solid, spike, corner pyramid, edge tetrahedron) has positive volume, and the pieces add up to the
# halo exactly.  Usage: ~/geom/bin/python study1.py <dataset solids dir> <exactlib dir> <out json>
import sys, os, json
SOL, LIB, OUT = sys.argv[1:4]; sys.path.insert(0, LIB)
from exactlib import *
from fractions import Fraction as Fr
import sympy
SOLIDS = ['dicto-gti', 'dicto-fpd', 'dicto-palintriacontahedron', 'dicto-icosaxes', 'dicto-unborn-axes', 'dicto-metaxyhexecontahedron',
          'dicto-tweedledum', 'dicto-samson', 'dicto-david', 'dicto-delilah']
def fkey(s): return 1 if s == 'Q' else (('cbrt', 2) if s == 'Q(2**(1/3))' else int(s[7:-2]))
def parse(s, d):
    if d == 1:
        e = sympy.Rational(sympy.sympify(s)); return QF(Fr(int(e.p), int(e.q)), 0, 5)
    e = sympy.expand(sympy.sympify(s))
    if isinstance(d, tuple):
        cs = [Fr(0)] * 3; basis = {sympy.Integer(1): 0, sympy.Integer(2) ** sympy.Rational(1, 3): 1, sympy.Integer(2) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items(): cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=2)
    a = b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        if t == 1: a += Fr(int(c.p), int(c.q))
        else: assert t == sympy.sqrt(d), s; b += Fr(int(c.p), int(c.q))
    return QF(a, b, d)
def kinds(F):
    k = {}
    for f in F: k[len(f)] = k.get(len(f), 0) + 1
    return {str(a): b for a, b in sorted(k.items())}
def rad2(V): return max((dot(v, v) for v in V), key=lambda x: x.f())
def similar(A, B, g2):
    """exact: the corners of B are k x the corners of A, k^2 = g2 (|B|^2/|A|^2), by matching each corner of B to a parallel corner of A
    with the right squared ratio; no square root needed."""
    if len(A) != len(B): return False
    for v in B:
        if not any(all(x.sign() == 0 for x in cross(u, v)) and dot(u, v).sign() > 0 and (dot(v, v) - g2 * dot(u, u)).sign() == 0 for u in A):
            return False
    return True
def gstr(x): return fmt(x)
res = []
for slug in SOLIDS:
    m = json.load(open(os.path.join(SOL, slug + '.json'))); d = fkey(m['field'])
    V = [tuple(parse(x, d) for x in v['exact']) for v in m['vertices']]; V, F = hull(V)
    row = dict(solid=m['name'], field=m['field'], symmetry=m.get('symmetry', {}).get('schoenflies'), steps=[])
    V0, F0, R0 = V, F, rad2(V); vol0 = volume(V, F)
    hist = [(V, F, R0, volume(V, F))]; S, SF = V, F
    for k in range(1, 9):
        S, SF = ustep(S); r2 = rad2(S); vs = volume(S, SF)
        st = dict(step=k, corners=len(S), faces=kinds(SF), volume_over_start=gstr(vs / vol0), radius2_over_start=gstr(r2 / R0),
                  radius_over_start_decimal=(r2 / R0).f() ** .5)
        for j, (A, AF, ra, va) in enumerate(hist):
            if kinds(AF) == kinds(SF) and similar(A, S, r2 / ra):
                g2 = r2 / ra; st['returns_to_step'] = j
                row.update(enters_cycle_at_step=j, period=k - j, gain_radius_squared=gstr(g2), gain_volume=gstr(vs / va), gain_radius_decimal=g2.f() ** .5)
                try:
                    g = qsqrt(g2) if isinstance(g2, QF) else None
                    if g is not None: row['gain_radius'] = gstr(g)
                except Exception: pass
                break
        row['steps'].append(st); print(m['name'][:30], st, flush=True); hist.append((S, SF, r2, vs))
        if 'period' in row: break
        if len(S) > 400: row['note'] = 'stopped: over 400 corners'; break
    # Part 2: polar spikes, exact
    row['polar'] = {}
    ts = [('2', 2)] + ([('phi', PHI)] if d == 5 else [])
    for tn, t in ts:
        rho2 = R0 * t
        FP = face_planes(V0, F0); tips = [mul(rho2 / c, n) for n, c in FP]
        HV, HF = hull(tips); vh = volume(HV, HF)
        pieces = [volume(V0, F0)]; typ = ['solid']
        for f, p in zip(F0, tips):
            pieces += [det3(sub(V0[f[0]], p), sub(V0[f[j]], p), sub(V0[f[j + 1]], p)) / 6 for j in range(1, len(f) - 1)]
        typ += ['spike'] * (len(pieces) - len(typ))
        fa = {v: [i for i, f in enumerate(F0) if v in f] for v in range(len(V0))}
        for v in range(len(V0)):   # corner pyramid: apex v, base the polygon of the tips round v (ordered by the faces round v)
            ring = fa[v]; order = [ring[0]]
            while len(order) < len(ring):
                f = F0[order[-1]]; i = f.index(v); w = f[(i - 1) % len(f)]   # the edge (w, v) of face f leads to the next face
                order.append(next(g for g in ring if g not in order and w in F0[g]))
            P = [tips[i] for i in order]
            pieces += [det3(sub(P[0], V0[v]), sub(P[j + 1], V0[v]), sub(P[j], V0[v])) / 6 for j in range(1, len(P) - 1)]
        typ += ['corner'] * (len(pieces) - len(typ))
        for a, b in edges_of(F0):
            f, g = [i for i in fa[a] if i in fa[b]]
            if F0[f][(F0[f].index(a) + 1) % len(F0[f])] != b: f, g = g, f   # f runs a -> b
            pieces.append(det3(sub(V0[b], V0[a]), sub(tips[f], V0[a]), sub(tips[g], V0[a])) / 6)
        typ += ['edge'] * (len(pieces) - len(typ))
        signs = {}
        for x, ty in zip(pieces, typ): signs.setdefault(ty, set()).add(x.sign())
        zer = sum(1 for x in pieces if x.sign() == 0); neg = {ty: sorted(v) for ty, v in signs.items()}
        tot = sum((x if x.sign() >= 0 else -x for x in pieces), zero(d if d != 1 else 5))
        row['polar'][tn] = dict(pieces=len(pieces), signs_by_kind=neg, zero=zer, consistent=all(len(v) == 1 and 0 not in v for v in signs.values()), sum_equals_halo=(tot - vh).sign() == 0,
                                halo_over_solid=gstr(vh / pieces[0]))
        print(' polar', tn, row['polar'][tn], flush=True)
    res.append(row)
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('done', len(res))
