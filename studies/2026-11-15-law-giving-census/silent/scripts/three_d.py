#!/usr/bin/env python3
"""3D groups (A3, B3, H3): EXACT enumeration of every seed (closed positive orthant, projective) where the corner set is silent in
at least two independent harmonic conditions, for all degrees <= KMAX; then the tones up to KEVAL at each point.

Interior (all c_j > 0, chart c3 = 1): for each minimal system (two 1-dim degrees k1 < k2, or one degree with >= 2 invariant harmonics)
the two polynomials P, Q in (x, y) = (c1/c3, c2/c3), coefficients in Q(sqrt D), are eliminated by resultants Res_y and Res_x
(then the norm to Q by Res_s with s^2 - D); every pair (x root, y root) of positive real roots is either EXCLUDED (P or Q bounded away
from 0 on the root box, arb) or CERTIFIED (Krawczyk: unique zero in the box). Common factors (curves of joint zeros) are found by gcd.
Edges (one c_j = 0): univariate polynomials over Q(sqrt D), certified roots (exact.positive_roots), common roots by equal minimal
polynomial + overlapping balls (exact). Vertices: exact evaluation in Q(sqrt D).
Usage: three_d.py GROUP KMAX KEVAL -> data/three-GROUP.json
"""
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from flint import fmpq, fmpq_poly, fmpq_mpoly_ctx, arb
import sil
import exact as X
from exact import K, E, positive_roots, same_algebraic
import symm

# ---------- K-coefficient polynomials as pairs (A, B): A + sqrt(D) B ----------
class KP:
    __slots__ = ('A', 'B')
    D = 2
    def __init__(s, A, B): s.A, s.B = A, B
    def __add__(s, o): return KP(s.A + o.A, s.B + o.B)
    def __mul__(s, o):
        if isinstance(o, K): return KP(s.A*o.a + s.B*(o.b*KP.D), s.A*o.b + s.B*o.a)
        return KP(s.A*o.A + KP.D*(s.B*o.B), s.A*o.B + s.B*o.A)
    def pow(s, n):
        r = None; b = s
        while n:
            if n & 1: r = b if r is None else r*b
            n >>= 1
            if n: b = b*b
        return r

def chart_polys(H, k, ctx2, cvec):
    """h_{k,i}(c) with c = cvec (list of KP linear polys in ctx2): returns list of KP"""
    zero = ctx2.from_dict({}); one = ctx2.from_dict({(0,)*ctx2.nvars(): fmpq(1)})
    def kconst(q): return KP(one*q.a, one*q.b)
    r = H.r
    u = [None]*H.n
    acc = KP(zero, zero)
    for i in range(r):
        for j in range(r):
            if not H.Gw[i][j].iszero(): acc = acc + (cvec[i]*cvec[j])*H.Gw[i][j]
    u[0] = acc
    for i, d in enumerate(H.degs[1:]):
        acc = KP(zero, zero)
        for h in H.hat[H.choice[i]]:
            L = KP(zero, zero)
            for j in range(r):
                if not h[j].iszero(): L = L + cvec[j]*h[j]
            acc = acc + L.pow(d)
        u[i + 1] = acc
    out = []
    for h in H.harm[k]:
        tot = KP(zero, zero)
        for e, co in h.items():
            t = kconst(co)
            for ui, ei in zip(u, e):
                if ei: t = t*ui.pow(ei)
            tot = tot + t
        out.append(tot)
    return out

def to3(P, ctx3):
    d = {}
    for m, c in P.A.to_dict().items(): d[tuple(m) + (0,)] = c
    for m, c in P.B.to_dict().items(): d[tuple(m) + (1,)] = d.get(tuple(m) + (1,), fmpq(0)) + c
    return ctx3.from_dict(d)

def univ(P3, var_index, ctx3, D):
    """P3 in Q[x, y, s] depending only on var var_index and s -> norm to Q: fmpq_poly"""
    s = ctx3.gens()[2]
    N = P3.resultant(s**2 - D, 's') if P3.degrees()[2] > 0 else P3
    dct = N.to_dict(); deg = max(m[var_index] for m in dct) if dct else 0
    co = [fmpq(0)]*(deg + 1)
    for m, c in dct.items(): co[m[var_index]] += c
    return fmpq_poly(co)

def refine(g, x, target=1e-80):
    """interval Newton refinement of the isolated real root ball x of the squarefree rational polynomial g"""
    dg = g.derivative()
    for _ in range(60):
        if float(x.rad()) < target: break
        m = arb(x.mid()); d = X.pev(dg, x)
        if d.contains(0): break
        nx = m - X.pev(g, m)/d
        y = nx.intersection(x) if nx.overlaps(x) else nx
        if float(y.rad()) >= float(x.rad())*0.99 and float(x.rad()) < 1e-30: x = y; break
        x = y
    return x

def pos_real_roots(f):
    out = []
    if f.degree() < 1: return out
    c, facs = f.factor()
    for g, m in facs:
        if g.degree() < 1: continue
        for z, _ in g.complex_roots():
            if not z.imag.is_zero(): continue
            x = z.real
            if x > 0: out.append((refine(g, x), [str(q) for q in g.coeffs()], int(m)))
    return out

def kstr(c): return [str(c.a), str(c.b)]

def interior(H, sysk, KMAX, chart=('x', 'y', '1')):
    """sysk: list of (k, i) polynomials forming the system (first two eliminated, rest filter). chart: per seed coordinate one of
    'x', 'y' (the two unknowns, > 0), '1', '0' (a 2-parameter stratum: the interior of a 3D chamber or a facet of a 4D one)"""
    ctx2 = fmpq_mpoly_ctx.get(('x', 'y'), 'lex'); ctx3 = fmpq_mpoly_ctx.get(('x', 'y', 's'), 'lex')
    x, y = ctx2.gens(); zero = ctx2.from_dict({}); one = ctx2.from_dict({(0, 0): fmpq(1)})
    cvec = [KP({'x': x, 'y': y, '1': one, '0': zero}[ch], zero) for ch in chart]
    ix, iy = chart.index('x'), chart.index('y')
    def cbox(a, b): return [{'x': a, 'y': b, '1': arb(1), '0': arb(0)}[ch] for ch in chart]
    cache = {}
    def poly(k, i):
        if k not in cache: cache[k] = chart_polys(H, k, ctx2, cvec)
        return to3(cache[k][i], ctx3)
    P = poly(*sysk[0]); Q = poly(*sysk[1])
    curves = []
    Ry = P.resultant(Q, 'y')
    if Ry.is_zero():
        g = P.gcd(Q); curves.append(str(g)); P = P // g; Q = Q // g; Ry = P.resultant(Q, 'y')
    Rx = P.resultant(Q, 'x')
    fx = univ(Ry, 0, ctx3, H.D); fy = univ(Rx, 1, ctx3, H.D)
    xs = pos_real_roots(fx); ys = pos_real_roots(fy)
    pts = []; undecided = []
    for (xr, mx, _) in xs:
        for (yr, my, _) in ys:
            box = cbox(xr, yr)
            vals = []
            for (k, i) in sysk[:2]: vals.append(H.h_arb(k, box)[i])
            if any(not v.contains(0) for v in vals): continue
            def F(z): return [H.h_arb(k, cbox(z[0], z[1]))[i] for (k, i) in sysk[:2]]
            def J(z):
                out = []
                for (k, i) in sysk[:2]:
                    v, jac = H.h_arb(k, cbox(z[0], z[1]), jac=True); out.append([jac[i][ix], jac[i][iy]])
                return out
            rad = max(float(xr.rad()), float(yr.rad()), 1e-60)*4 + 1e-40
            st, bx = sil.krawczyk(F, J, [xr, yr], rad)
            if st != 'unique':
                st, bx = sil.krawczyk(F, J, [xr, yr], 1e-25)
            if st == 'unique': pts.append({'x': bx[0], 'y': bx[1], 'minpoly_x': mx, 'minpoly_y': my})
            else: undecided.append({'x': xr, 'y': yr, 'minpoly_x': mx, 'minpoly_y': my})
    return pts, curves, undecided, (fx.degree(), fy.degree())

def tone_status(H, c_arb, KEVAL):
    st = {}
    ub = H.u_arb(c_arb)
    for k in H.degrees(KEVAL):
        vals = H.h_arb(k, c_arb, ub=ub)
        st[k] = 'nonzero' if any(not v.contains(0) for v in vals) else 'zero?'
    return st

def strength(H, zero_degs):
    for k in range(1, 200):
        if H.dims.get(k, 0) and k not in zero_degs: return k - 1
    return None

def minus_I_locus(H, nonzero, symmetric):
    """for groups without -I (A_n): a seed fixed by the diagram reversal sigma has -I symmetry, so every odd tone vanishes there;
    returns (reduced condition degrees filter, dimension of the symmetric locus inside the stratum) or None"""
    if not H.aut or not symmetric: return None
    s = H.aut[0]; orbs = {frozenset((j, s[j])) for j in nonzero}
    return len(orbs) - 1

def assess(H, rec, zero, nonzero, symmetric):
    sdim = len(nonzero) - 1
    rec['conditions'] = sum(H.dims[k] for k in zero); rec['stratum_dim'] = sdim
    rec['overdetermined_raw'] = rec['conditions'] > sdim
    ld = minus_I_locus(H, nonzero, symmetric)
    if ld is None:
        rec['overdetermined'] = rec['overdetermined_raw']
    else:
        ev = [k for k in zero if k % 2 == 0]
        rec['minus_I_symmetric'] = True; rec['even_conditions'] = sum(H.dims[k] for k in ev); rec['locus_dim'] = ld
        rec['overdetermined'] = rec['even_conditions'] > ld
        rec['note'] = 'seed fixed by the diagram reversal: -I symmetry kills every odd tone; counted on the symmetric locus'
    return rec

def line_polys(H, c0, c1, KEVAL):
    """c = c0 + t c1 (K vectors): exact E-polynomials h_{k,i}(t) for every degree <= KEVAL"""
    r = H.r; t = E.t()
    cv = [E.const(c0[i]) + E.const(c1[i])*t for i in range(r)]
    acc = E.const(0)
    for i in range(r):
        for j in range(r):
            if not H.Gw[i][j].iszero(): acc = acc + cv[i]*cv[j]*E.const(H.Gw[i][j])
    u = [acc]
    for i, d in enumerate(H.degs[1:]):
        acc = E.const(0)
        for h in H.hat[H.choice[i]]:
            L = E.const(0)
            for j in range(r): L = L + E.const(h[j])*cv[j]
            acc = acc + L**d
        u.append(acc)
    out = {}
    for k in H.degrees(KEVAL):
        polys = []
        for h in H.harm[k]:
            tot = E.const(0)
            for e, co in h.items():
                term = E.const(co)
                for ui, ei in zip(u, e):
                    if ei: term = term*(ui**ei)
                tot = tot + term
            polys.append(tot)
        out[k] = polys
    return out

def line_roots(H, c0, c1, KEVAL):
    """positive t where whole degrees vanish on the line c0 + t c1, grouped across degrees (exact: certified roots, equal minimal
    polynomials + overlapping balls); also the degrees vanishing identically on the line"""
    P = line_polys(H, c0, c1, KEVAL); roots = {}; ident = []
    for k, polys in P.items():
        nz = [p for p in polys if not p.iszero()]
        if not nz: ident.append(k); continue
        common = []
        for rt in positive_roots(nz[0]):
            if all(any(same_algebraic(rt, q) for q in positive_roots(p)) for p in nz[1:]): common.append(rt)
        roots[k] = common
    groups = []
    for k, rts in roots.items():
        for rt in rts:
            g = next((g for g in groups if same_algebraic(g['root'], rt)), None)
            if g is None: groups.append({'root': rt, 'degrees': [k]})
            else: g['degrees'].append(k)
    return groups, ident

def edges(H, KEVAL):
    """every edge (exactly one c_j = 0 ... in 3D: two nonzero nodes a < b), seed c_a = 1, c_b = t > 0"""
    r = H.r; out = []
    for a, b in itertools.combinations(range(r), 2):
        t = E.t()
        cv = [E.const(0)]*r; cv[a] = E.const(1); cv[b] = t
        u = [E.const(0)]
        acc = E.const(0)
        for i in range(r):
            for j in range(r):
                if not H.Gw[i][j].iszero(): acc = acc + cv[i]*cv[j]*E.const(H.Gw[i][j])
        u = [acc]
        for i, d in enumerate(H.degs[1:]):
            acc = E.const(0)
            for h in H.hat[H.choice[i]]:
                L = E.const(h[a]) + E.const(h[b])*t; acc = acc + L**d
            u.append(acc)
        roots = {}; ident = []
        for k in H.degrees(KEVAL):
            polys = []
            for h in H.harm[k]:
                tot = E.const(0)
                for e, co in h.items():
                    term = E.const(co)
                    for ui, ei in zip(u, e):
                        if ei: term = term*(ui**ei)
                    tot = tot + term
                polys.append(tot)
            nz = [p for p in polys if not p.iszero()]
            if not nz: ident.append(k); continue
            cand = positive_roots(nz[0])
            common = []
            for rt in cand:
                ok = True
                for p in nz[1:]:
                    rs = positive_roots(p)
                    if not any(same_algebraic(rt, q) for q in rs): ok = False; break
                if ok: common.append(rt)
            roots[k] = common
        # group roots across degrees
        groups = []
        for k, rts in roots.items():
            for rt in rts:
                g = next((g for g in groups if same_algebraic(g['root'], rt)), None)
                if g is None: groups.append({'root': rt, 'degrees': [k]})
                else: g['degrees'].append(k)
        out.append({'nodes': (a, b), 'identically_zero_degrees': ident,
                    'points': [{'t': g['root']['value'], 'minpoly_t': g['root']['minpoly'], 'genuine': g['root']['genuine'],
                                'degrees': sorted(g['degrees']), '_x': g['root']['x']} for g in groups]})
    return out

def vertices(H, KEVAL):
    out = []
    for j in range(H.r):
        c = [K(1) if i == j else K(0) for i in range(H.r)]
        u = H.u_exact(c); zero = []
        for k in H.degrees(KEVAL):
            if all(v.iszero() for v in H.h_exact(k, c, u)): zero.append(k)
        out.append({'node': j, 'zero_degrees_exact': zero})
    return out

def main(name, KMAX, KEVAL):
    t0 = time.time(); H = sil.H(name); KP.D = H.D
    degs = H.degrees(KMAX)
    print(f'{name}: degrees with invariant harmonics up to {KEVAL}: ' + ', '.join(f'{k}' + (f'(dim {H.dims[k]})' if H.dims[k] > 1 else '') for k in H.degrees(KEVAL)), flush=True)
    systems = []
    one = [k for k in degs if H.dims[k] == 1]
    for k1, k2 in itertools.combinations(one, 2): systems.append([(k1, 0), (k2, 0)])
    for k in degs:
        if H.dims[k] >= 2: systems.append([(k, i) for i in range(H.dims[k])])
    res = {'group': name, 'KMAX': KMAX, 'KEVAL': KEVAL, 'dims': {k: H.dims[k] for k in H.degrees(KEVAL)}, 'systems': []}
    allpts = []; allund = []
    for si, sysk in enumerate(systems):
        ts = time.time()
        pts, curves, und, dg = interior(H, sysk, KMAX)
        lab = '+'.join(f'h{k}' + (f'.{i}' if H.dims[k] > 1 else '') for k, i in sysk[:2])
        print(f'PROGRESS {(si+1)/len(systems):.3f} {name} system {lab}: resultant degrees {dg}, {len(pts)} certified interior points, '
              f'{len(curves)} common curves {curves}, {len(und)} undecided ({time.time()-ts:.1f} s)', flush=True)
        res['systems'].append({'system': lab, 'resultant_degrees': dg, 'n_points': len(pts), 'curves': curves, 'undecided': [{'x': u['x'].str(20), 'y': u['y'].str(20), 'minpoly_x': u['minpoly_x'], 'minpoly_y': u['minpoly_y']} for u in und]})
        for u in und: u['system'] = lab; allund.append(u)
        for p in pts:
            p['sys_degrees'] = sorted({k for k, i in sysk})
            if not any(q['x'].overlaps(p['x']) and q['y'].overlaps(p['y']) for q in allpts): allpts.append(p)
    # analyse each distinct point
    out_pts = []
    for p in allpts:
        c = [p['x'], p['y'], arb(1)]
        st = tone_status(H, c, KEVAL)
        zero = [k for k, v in st.items() if v == 'zero?']
        cf = [float(p['x'].mid()), float(p['y'].mid()), 1.0]
        rec = {'seed_c': cf, 'x_box': p['x'].str(25), 'y_box': p['y'].str(25), 'minpoly_c1/c3': p['minpoly_x'], 'minpoly_c2/c3': p['minpoly_y'],
               'zero_degrees': zero, 'design_strength': strength(H, zero), 'orbit_size': symm.orbit_size(H, cf)}
        if H.aut and p['minpoly_x'] == ['-1', '1']:   # c1 = c3 exactly: exact tones on the line c = (1, t, 1)
            groups, ident = line_roots(H, [K(1), K(0), K(1)], [K(0), K(1), K(0)], KEVAL)
            yr = {'minpoly': p['minpoly_y'], 'x': p['y']}
            g = next((g for g in groups if same_algebraic(g['root'], yr)), None)
            exact_zero = sorted(ident + (g['degrees'] if g else []))
            rec['zero_degrees_exact'] = exact_zero; rec['exact_matches_interval'] = exact_zero == zero
            zero = exact_zero; rec['zero_degrees'] = zero; rec['design_strength'] = strength(H, zero)
        else:
            extra = [k for k in zero if k not in p['sys_degrees']]
            rec['zero_beyond_system_unproven'] = extra
        assess(H, rec, zero, [0, 1, 2], p['minpoly_x'] == ['-1', '1'])
        if rec['overdetermined_raw']: rec['symmetry'] = symm.explain(H, cf)
        out_pts.append(rec)
        print(f'POINT {name} c = {np.round(cf, 6).tolist()} zero degrees {zero} conditions {rec["conditions"]} strength {rec["design_strength"]} '
              f'orbit {rec["orbit_size"]}' + (' [-I symmetric]' if rec.get('minus_I_symmetric') else '')
              + (f'  <<< OVER-DETERMINED  symmetry {rec["symmetry"]}' if rec['overdetermined'] else ''), flush=True)
    res['interior_points'] = out_pts
    for u in allund:
        m = next((q for q in allpts if q['x'].overlaps(u['x']) and q['y'].overlaps(u['y'])), None)
        odd = all(int(t[1:].split('.')[0]) % 2 for t in u['system'].split('+'))
        u['resolved'] = ('coincides with a certified point (non-transversal intersection there)' if m else
                         'on the line c1 = c3 (exact x = 1), where every odd tone vanishes identically (-I symmetry)' if (H.aut and odd and u['minpoly_x'] == ['-1', '1'])
                         else 'UNRESOLVED')
        print(f'UNDECIDED {name} {u["system"]} at ({float(u["x"].mid()):.6f}, {float(u["y"].mid()):.6f}): {u["resolved"]}', flush=True)
    res['undecided'] = [{'system': u['system'], 'x': u['x'].str(20), 'y': u['y'].str(20), 'resolved': u['resolved']} for u in allund]
    if H.aut:   # A3: (c1, c2, c3) ~ (c3, c2, c1) congruent
        for rec in out_pts:
            c = rec['seed_c']; rc = [c[2]/c[0], c[1]/c[0], 1.0]
            rec['diagram_partner'] = next((i for i, q in enumerate(out_pts) if np.allclose(q['seed_c'], rc, rtol=1e-9) and q is not rec), None)
    # edges and vertices
    ed = edges(H, KEVAL)
    for e in ed:
        for p in e['points']:
            a, b = e['nodes']; cf = [0.0]*H.r; cf[a] = 1.0; cf[b] = float(p['_x'].mid())
            p['seed_c'] = cf; p['orbit_size'] = symm.orbit_size(H, cf)
            symm_ = bool(H.aut) and tuple(sorted((H.aut[0][a], H.aut[0][b]))) == (a, b) and p['minpoly_t'] == ['-1', '1']
            assess(H, p, p['degrees'], [a, b], symm_)
            p['design_strength'] = strength(H, p['degrees'] + e['identically_zero_degrees'])
            if p['overdetermined_raw']: p['symmetry'] = symm.explain(H, cf)
            del p['_x']
            if p['conditions'] >= 1:
                print(f'EDGE {name} nodes {e["nodes"]} t = {p["t"][:20]} minpoly {p["minpoly_t"]} zero degrees {p["degrees"]}'
                      + (f'  <<< OVER-DETERMINED  symmetry {p["symmetry"]}' if p['overdetermined'] else ''), flush=True)
        if e['identically_zero_degrees']: print(f'EDGE {name} nodes {e["nodes"]}: degrees identically zero {e["identically_zero_degrees"]}')
    res['edges'] = ed
    vt = vertices(H, KEVAL)
    for v in vt:
        cf = [0.0]*H.r; cf[v['node']] = 1.0; v['orbit_size'] = symm.orbit_size(H, cf)
        v['design_strength'] = strength(H, v['zero_degrees_exact'])
        j = v['node']; assess(H, v, v['zero_degrees_exact'], [j], bool(H.aut) and H.aut[0][j] == j)
        if v['zero_degrees_exact']: v['symmetry'] = symm.explain(H, cf)
        print(f'VERTEX {name} node {v["node"]} orbit {v["orbit_size"]} zero degrees (exact) {v["zero_degrees_exact"]} strength {v["design_strength"]}'
              + (' [-I symmetric]' if v.get('minus_I_symmetric') else '')
              + (f'  <<< OVER-DETERMINED  symmetry {v["symmetry"]}' if v['overdetermined'] else ''), flush=True)
    res['vertices'] = vt
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(HERE, '..', 'data', f'three-{name}.json'), 'w'), indent=1, default=str)
    print(f'{name}: done in {res["seconds"]} s', flush=True)
    return res

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
