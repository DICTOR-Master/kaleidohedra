#!/usr/bin/env python3
"""4D groups (A4, B4, D4, F4, H4): silent coincidences in the 3-parameter seed space.

Orbit space (exact, sympy): on the unit sphere the invariant harmonics are polynomials in u_2, u_3, u_4 (power-sum invariants,
u_1 = 1). (a) The design hierarchy: Groebner bases of {h_k : k <= t}. (b) Every minimal interior system of exactly three conditions
from degrees <= K4: all its complex solutions in u-space (Groebner, zero-dimensional), the real ones mapped to seeds by Newton from many
starts and CERTIFIED in seed space by a Krawczyk test on the three tone conditions (unique zero in a box); real u-solutions with no
seed found are listed as 'no real seed found'. (c) Design curves (one-dimensional loci of the hierarchy): restriction of every later
degree to the curve (exact univariate polynomials), realizable range from the certified facet points and from seeds found along it.
Facets (2-dimensional strata, one c_j = 0): the exact resultant enumeration of three_d.py for all pairs of degrees <= KF.
Edges (1-dimensional strata): exact univariate roots for all degrees <= KEVAL. Vertices: exact values.
Usage: four_d.py GROUP KF K4 KEVAL -> data/four-GROUP.json
"""
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import sympy as sp
from flint import fmpq, fmpq_poly, arb
import sil, symm, ustruct, three_d as T
import exact as X
from exact import K, E

HIER = {'B4': [4, 6, 8, 10], 'F4': [6, 8, 12, 14], 'H4': [12, 20, 24, 30], 'D4': [4, 6, 8], 'A4': [3, 4, 5, 6, 7]}

def say(*a): print(*a, flush=True)

def minus_I_symmetric(H, c, tol=1e-12):
    if not H.aut or H.name not in ('A4',): return False
    s = H.aut[0]; return all(abs(c[i] - c[s[i]]) < tol*max(1, abs(c[i])) for i in range(H.r))

def assess(H, rec, zero, nonzero, symmetric):
    sdim = len(nonzero) - 1
    rec['conditions'] = sum(H.dims[k] for k in zero); rec['stratum_dim'] = sdim
    rec['overdetermined_raw'] = rec['conditions'] > sdim
    if symmetric:
        s = H.aut[0]; ld = len({frozenset((j, s[j])) for j in nonzero}) - 1
        ev = [k for k in zero if k % 2 == 0]
        rec['minus_I_symmetric'] = True; rec['even_conditions'] = sum(H.dims[k] for k in ev); rec['locus_dim'] = ld
        rec['overdetermined'] = rec['even_conditions'] > ld
    else: rec['overdetermined'] = rec['overdetermined_raw']
    return rec

# ---------------- seed-space numerics ----------------
def fold(H, c):
    """map the seed v = sum c_j w_j into the closed chamber (reflect in simple roots while some c_j < 0)"""
    v = np.asarray(c, float) @ H.Wf
    for _ in range(2000):
        cc = H.Rf @ v
        j = int(np.argmin(cc))
        if cc[j] >= -1e-15: return cc
        v = v - 2*cc[j]*H.Rf[j]
    return H.Rf @ v

def newton(F, c0, iters=60):
    c = np.array(c0, float)
    for _ in range(iters):
        f, J = F(c)
        try: dc = np.linalg.lstsq(J, -f, rcond=None)[0]
        except np.linalg.LinAlgError: return None
        lam = 1.0
        while lam > 1e-4:
            c2 = c + lam*dc; f2, _ = F(c2)
            if np.linalg.norm(f2) < np.linalg.norm(f) or lam < 2e-4: break
            lam /= 2
        c = c2
        if np.linalg.norm(dc) < 1e-15*max(1, np.linalg.norm(c)): break
    f, _ = F(c)
    return c if np.linalg.norm(f) < 1e-11 else None

def hsys_float(H, conds):
    """conds: list of (k, i). F(c) = [h_{k,i}(c)/|v|^k ..., sum c - 1]"""
    def F(c):
        vals = []; jac = []
        u, Ju = H.u_float(c); n2 = u[0]
        for (k, i) in conds:
            v, J = H.h_float(k, c, jac=True)
            vals.append(v[i]/n2**(k/2)); jac.append(J[i]/n2**(k/2) - (k/2)*v[i]/n2**(k/2 + 1)*Ju[0])
        vals.append(np.sum(c) - 1); jac.append(np.ones(H.r))
        return np.array(vals), np.array(jac)
    return F

def utarget_float(H, conds, extra):
    """conditions plus u_i/|v|^d_i = value for (i, value) in extra"""
    base = hsys_float(H, conds)
    def F(c):
        f, J = base(c); u, Ju = H.u_float(c); n2 = u[0]
        f2 = list(f[:-1]); J2 = list(J[:-1])
        for (i, val) in extra:
            d = H.degs[i]; f2.append(u[i]/n2**(d/2) - val); J2.append(Ju[i]/n2**(d/2) - (d/2)*u[i]/n2**(d/2 + 1)*Ju[0])
        f2.append(f[-1]); J2.append(J[-1])
        return np.array(f2), np.array(J2)
    return F

def certify_seed(H, conds, c):
    """Krawczyk on [h_{k,i} for conds] + [sum c - 1] in R^r (needs len(conds) = r - 1)"""
    def F(z):
        out = [H.h_arb(k, z)[i] for (k, i) in conds]; out.append(sum(z, arb(0)) - 1); return out
    def J(z):
        rows = []
        ub = H.u_arb(z)
        for (k, i) in conds:
            v, jac = H.h_arb(k, z, jac=True, ub=ub); rows.append(jac[i])
        rows.append([arb(1)]*H.r); return rows
    c = np.asarray(c, float)/np.sum(c)
    # polish in arb by a few Newton steps (float midpoint is enough for radius 1e-12)
    for rad in (1e-12, 1e-10, 1e-9):
        st, bx = sil.krawczyk(F, J, list(c), rad)
        if st == 'unique': return bx
    return None

def tone_status(H, box, KEVAL):
    ub = H.u_arb(box); st = {}
    for k in H.degrees(KEVAL):
        vals = H.h_arb(k, box, ub=ub)
        st[k] = 'nonzero' if any(not v.contains(0) for v in vals) else 'zero?'
    return st

def seeds_for(H, F, starts, rng):
    found = []
    for _ in range(starts):
        c0 = rng.dirichlet(np.ones(H.r))
        c = newton(F, c0)
        if c is None: continue
        cc = fold(H, c); cc = np.where(np.abs(cc) < 1e-13, 0.0, cc); cc = cc/np.sum(cc)
        if not any(np.allclose(cc, q, atol=1e-7) for q in found): found.append(cc)
    return found

# ---------------- u-space (sympy) ----------------
def dom(H): return sp.QQ.algebraic_field(sp.sqrt(5)) if H.D == 5 else sp.QQ

def norm_univ(p, z, D):
    """p(z) with coefficients in Q(sqrt D) -> rational polynomial p * conj(p) as fmpq_poly"""
    e = sp.expand(p); s = sp.sqrt(D)
    if e.has(s):
        e = sp.expand(e*e.subs(s, -s))
    P = sp.Poly(e, z)
    co = [sp.Rational(c) for c in reversed(P.all_coeffs())]
    return fmpq_poly([fmpq(int(c.p), int(c.q)) for c in co])

def real_roots_q(f):
    out = []
    if f.degree() < 1: return out
    c, facs = f.factor()
    for g, m in facs:
        if g.degree() < 1: continue
        for zr, _ in g.complex_roots():
            if zr.imag.is_zero(): out.append((T.refine(g, zr.real), [str(q) for q in g.coeffs()]))
    return out

def solve_u(H, polys, U):
    """all real solutions of a zero-dimensional system in u_2..u_4 (sympy polys), as float triples (via lex Groebner basis)"""
    G = sp.groebner(polys, *U, order='lex', domain=dom(H))
    if list(G.exprs) == [1]: return 'empty', [], G
    if not G.is_zero_dimensional: return 'positive-dimensional', [], G
    exprs = list(G.exprs); z = U[-1]
    last = [e for e in exprs if e.free_symbols <= {z}]
    f = norm_univ(last[0], z, H.D)
    sols = []
    for zr, mp in real_roots_q(f):
        zv = sp.Float(zr.mid().str(60, radius=False), 60)
        # back substitution: solve the remaining basis for (u2, u3) numerically, then keep common zeros
        rest = [sp.expand(e.subs(z, zv)) for e in exprs if e not in last]
        cand = [{}]
        for var in reversed(U[:-1]):
            new = []
            for cd in cand:
                es = [sp.expand(e.subs(cd)) for e in rest]
                uni = [e for e in es if e.free_symbols == {var}]
                if not uni: continue
                rts = sp.Poly(uni[0], var).nroots(n=40, maxsteps=200)
                for rt in rts:
                    if abs(sp.im(rt)) > 1e-25: continue
                    rt = sp.re(rt); d2 = dict(cd); d2[var] = rt
                    if all(abs(sp.N(e.subs(d2), 30)) < 1e-15 for e in uni): new.append(d2)
            cand = new
        for cd in cand:
            if all(abs(sp.N(e.subs(cd), 30)) < 1e-12*max(1, 1) for e in rest):
                u = [float(cd[v]) for v in U[:-1]] + [float(zv)]
                # genuine (not a conjugate-field root): check every original polynomial
                vals = [abs(complex(sp.N(p.subs(dict(zip(U, u))), 20))) for p in polys]
                if max(vals) < 1e-6: sols.append({'u': u, 'minpoly_u_last': mp})
    return 'ok', sols, G

def main(name, KF, K4, KEVAL):
    t0 = time.time(); H = sil.H(name); T.KP.D = H.D; rng = np.random.default_rng(11)
    res = {'group': name, 'KF': KF, 'K4': K4, 'KEVAL': KEVAL, 'dims': {k: H.dims[k] for k in H.degrees(KEVAL)}}
    say(f'{name}: degrees with invariant harmonics up to {KEVAL}: ' + ', '.join(f'{k}' + (f'(dim {H.dims[k]})' if H.dims[k] > 1 else '') for k in H.degrees(KEVAL)))
    _, U, P = ustruct.polys(name, KEVAL); U = list(U[1:])
    # ---------- (a) design hierarchy ----------
    hier = []
    for t in range(1, len(HIER[name]) + 1):
        degs = HIER[name][:t]; polys = [p for k in degs for p in P[k]]
        G = sp.groebner(polys, *U, order='lex', domain=dom(H))
        if list(G.exprs) == [1]: dim = -1
        elif G.is_zero_dimensional: dim = 0
        else: dim = 3 - len([e for e in G.exprs if True]) if len(G.exprs) < 3 else 1
        hier.append({'degrees': degs, 'conditions': sum(H.dims[k] for k in degs), 'groebner': [str(e) for e in G.exprs], 'dim_hint': dim})
        say(f'HIER {name} degrees {degs} ({sum(H.dims[k] for k in degs)} conditions): Groebner basis {[str(e)[:90] for e in G.exprs]}')
    res['hierarchy'] = hier
    # ---------- (c) design curve: prefix of the hierarchy whose locus is a line u2 = a0, u3 = b0 ----------
    curves = []
    for t in range(1, len(HIER[name]) + 1):
        degs = HIER[name][:t]; polys = [p for k in degs for p in P[k]]
        if sum(H.dims[k] for k in degs) != 2: continue
        G = sp.groebner(polys, *U, order='lex', domain=dom(H)); ex = list(G.exprs)
        lin = {}
        for e in ex:
            for v in U[:-1]:
                pe = sp.Poly(e, *U)
                if pe.degree(v) == 1 and all(pe.degree(w) == 0 for w in U if w not in (v,)):
                    lin[v] = sp.solve(e, v)[0]
        if len(lin) != 2: say(f'CURVE {name} {degs}: not a coordinate line, basis {ex}'); continue
        z = U[-1]; sub = {v: lin[v] for v in U[:-1]}
        cur = {'degrees': degs, 'u_fixed': {str(v): str(sp.nsimplify(lin[v])) for v in U[:-1]}, 'free': str(z), 'later': []}
        conds = [(k, i) for k in degs for i in range(H.dims[k])]
        roots_by_deg = {}
        for k in H.degrees(KEVAL):
            if k in degs: continue
            rs = [sp.expand(p.subs(sub)) for p in P[k]]
            if all(r == 0 for r in rs): cur['later'].append({'degree': k, 'restriction': 'identically zero'}); roots_by_deg[k] = 'all'; continue
            consts = [r for r in rs if r.free_symbols == set() and r != 0]
            if consts:
                cur['later'].append({'degree': k, 'restriction': 'nonzero constant on the curve', 'value': str(sp.N(consts[0], 20))}); roots_by_deg[k] = []; continue
            # common real roots of all restricted polys
            f0 = norm_univ(rs[0], z, H.D); cands = real_roots_q(f0)
            good = []
            for zr, mp in cands:
                zv = sp.Float(zr.mid().str(50, radius=False), 50)
                if all(abs(complex(sp.N(r.subs(z, zv), 40))) < sp.Float(10)**-25*max(1, abs(zv))**k for r in rs): good.append((zr, mp))
            roots_by_deg[k] = good
            cur['later'].append({'degree': k, 'restriction': f'polynomial(s) of degree {[sp.Poly(r, z).degree() for r in rs]} in {z}',
                                 'real_roots': [zr.mid().str(25, radius=False) for zr, _ in good]})
        # realizable range: seeds along the line; sample z between min and max of all candidate values
        allz = sorted({float(zr.mid()) for k, g in roots_by_deg.items() if g != 'all' for zr, _ in g})
        # find seeds of the curve itself (prefix conditions only) at random: their z-range
        Fcurve = None; zs_found = []
        base_conds = conds
        def Fz(zval):
            return utarget_float(H, base_conds, [(len(U), zval)])
        # z of random curve points: solve prefix conditions + random linear slice c . a = 0
        samples = []
        for _ in range(400):
            a = rng.normal(size=H.r)
            def Fs(c, a=a):
                f, J = hsys_float(H, base_conds)(c)
                return np.append(f, np.dot(a, c)), np.vstack([J, a])
            c = newton(Fs, rng.dirichlet(np.ones(H.r)))
            if c is None: continue
            cc = fold(H, c); cc = cc/np.sum(cc)
            u, _ = H.u_float(cc); samples.append((u[-1]/u[0]**(H.degs[-1]/2), cc))
        if samples:
            zmin = min(s[0] for s in samples); zmax = max(s[0] for s in samples)
            cur['sampled_z_range'] = [zmin, zmax]; cur['n_samples'] = len(samples)
            cur['sample_seeds'] = [s[1].tolist() for s in sorted(samples, key=lambda s: s[0])[::max(1, len(samples)//6)]]
            say(f'CURVE {name} {degs}: line {cur["u_fixed"]}, {len(samples)} sampled seeds, z = {z} in [{zmin:.6g}, {zmax:.6g}]')
        else: say(f'CURVE {name} {degs}: line {cur["u_fixed"]}, NO real seed found on it')
        # certify a seed for every later-degree root and check coincidences
        pts = []
        for k, g in roots_by_deg.items():
            if g == 'all': continue
            for zr, mp in g:
                zval = float(zr.mid())
                F = Fz(zval); found = seeds_for(H, F, 300, rng)
                for cc in found:
                    if cc.min() < 1e-5:
                        pts.append({'degree': k, 'z': zr.mid().str(25, radius=False), 'seed_c': cc.tolist(), 'boundary': True})
                        say(f'CURVEPOINT {name} {degs}+{k}: z = {zval:.10g} seed {np.round(cc, 6).tolist()} on the boundary (facet enumeration)')
                        continue
                    bx = certify_seed(H, base_conds + [(k, 0)], cc) if H.dims[k] >= 1 else None
                    rec = {'degree': k, 'z': zr.mid().str(25, radius=False), 'minpoly_z': mp, 'seed_c': cc.tolist(), 'certified': bx is not None}
                    if bx is not None:
                        st = tone_status(H, bx, KEVAL); zero = [kk for kk, v in st.items() if v == 'zero?']
                        rec['zero_degrees'] = zero; rec['orbit_size'] = symm.orbit_size(H, cc)
                        rec['design_strength'] = T.strength(H, zero)
                        nz = [j for j in range(H.r) if cc[j] > 1e-12]
                        assess(H, rec, zero, nz, minus_I_symmetric(H, cc))
                        if rec['overdetermined_raw']: rec['symmetry'] = symm.explain(H, cc)
                    pts.append(rec)
                    say(f'CURVEPOINT {name} {degs}+{k}: z = {zval:.10g} seed {np.round(cc, 6).tolist()} certified {rec["certified"]} '
                        f'zero {rec.get("zero_degrees")} strength {rec.get("design_strength")} orbit {rec.get("orbit_size")}'
                        + (f'  <<< OVER-DETERMINED {rec.get("symmetry")}' if rec.get('overdetermined') else ''))
                if not found: say(f'CURVEPOINT {name} {degs}+{k}: z = {zval:.10g}: no real seed found (outside the realizable part of the curve)')
        # exact coincidences of two later degrees on the curve (same algebraic number)
        coinc = []
        ks = [k for k, g in roots_by_deg.items() if g != 'all']
        for k1, k2 in itertools.combinations(ks, 2):
            for z1, m1 in roots_by_deg[k1]:
                for z2, m2 in roots_by_deg[k2]:
                    if m1 == m2 and z1.overlaps(z2): coinc.append({'degrees': [k1, k2], 'z': z1.mid().str(25, radius=False), 'minpoly': m1})
        cur['coincidences_exact'] = coinc
        for c_ in coinc: say(f'CURVECOINCIDENCE {name} {degs}: degrees {c_["degrees"]} vanish together at z = {c_["z"]}  <<< check realizability above')
        cur['points'] = pts; curves.append(cur)
    res['curves'] = curves
    # ---------- (b) interior: every minimal system of exactly three conditions from degrees <= K4 ----------
    degs4 = H.degrees(K4); systems = []
    for rr in range(1, 4):
        for combo in itertools.combinations(degs4, rr):
            if sum(H.dims[k] for k in combo) == 3: systems.append(list(combo))
    inter = []; allseeds = []
    for si, combo in enumerate(systems):
        polys = [p for k in combo for p in P[k]]; conds = [(k, i) for k in combo for i in range(H.dims[k])]
        ts = time.time()
        st, sols, G = solve_u(H, polys, U)
        rec = {'system': combo, 'status': st, 'n_real_u': len(sols), 'points': []}
        if st == 'positive-dimensional': rec['groebner'] = [str(e) for e in G.exprs]
        for sol in sols:
            u = sol['u']; F = utarget_float(H, conds[:0], [(i + 1, u[i]) for i in range(len(u))])
            found = seeds_for(H, F, 200, rng)
            if not found:
                rec['points'].append({'u': u, 'seed': None}); continue
            for cc in found:
                if cc.min() < 1e-5:
                    rec['points'].append({'u': u, 'seed_c': cc.tolist(), 'boundary': True,
                                          'note': 'seed on a facet (some c_j = 0): treated in the facet enumeration'})
                    say(f'INTERIOR {name} {combo}: u = {np.round(u, 8).tolist()} seed {np.round(cc, 6).tolist()} lies on the boundary (facet enumeration)')
                    continue
                bx = certify_seed(H, conds, cc)
                pr = {'u': u, 'seed_c': cc.tolist(), 'certified': bx is not None}
                if bx is not None:
                    stt = tone_status(H, bx, KEVAL); zero = [kk for kk, v in stt.items() if v == 'zero?']
                    pr['zero_degrees'] = zero; pr['zero_beyond_system_unproven'] = [k for k in zero if k not in combo]
                    pr['orbit_size'] = symm.orbit_size(H, cc); pr['design_strength'] = T.strength(H, zero)
                    nz = [j for j in range(H.r) if cc[j] > 1e-12]
                    assess(H, pr, zero, nz, minus_I_symmetric(H, cc))
                    if pr['overdetermined_raw']: pr['symmetry'] = symm.explain(H, cc)
                rec['points'].append(pr)
                say(f'INTERIOR {name} {combo}: u = {np.round(u, 8).tolist()} seed {np.round(cc, 6).tolist()} certified {pr["certified"]} '
                    f'zero {pr.get("zero_degrees")} strength {pr.get("design_strength")} orbit {pr.get("orbit_size")}'
                    + (f'  <<< OVER-DETERMINED {pr.get("symmetry")}' if pr.get('overdetermined') else ''))
        nseed = sum(1 for p in rec['points'] if p.get('seed_c'))
        say(f'PROGRESS {(si+1)/len(systems):.3f} {name} interior system {combo}: {st}, {len(sols)} real u-solutions, {nseed} seeds ({time.time()-ts:.1f} s)'
            + (f' basis {rec.get("groebner")}' if st == 'positive-dimensional' else ''))
        inter.append(rec)
    res['interior_systems'] = inter
    # ---------- facets ----------
    facets = []
    one = [k for k in H.degrees(KF) if H.dims[k] == 1]
    fsys = [[(a, 0), (b, 0)] for a, b in itertools.combinations(one, 2)] + [[(k, i) for i in range(H.dims[k])] for k in H.degrees(KF) if H.dims[k] >= 2]
    for j in range(H.r):
        oth = [i for i in range(H.r) if i != j]; chart = ['0']*H.r; chart[oth[0]] = 'x'; chart[oth[1]] = 'y'; chart[oth[2]] = '1'
        fpts = []; fund = []
        for sysk in fsys:
            ts = time.time()
            pts, cv, und, dg = T.interior(H, sysk, KF, tuple(chart))
            for p in pts:
                cbx = [{'x': p['x'], 'y': p['y'], '1': arb(1), '0': arb(0)}[ch] for ch in chart]
                if not any(all(a.overlaps(b) for a, b in zip(cbx, q['_box'])) for q in fpts):
                    p['_box'] = cbx; p['sys'] = sysk; fpts.append(p)
            fund += [{'system': sysk, 'x': u['x'].str(20), 'y': u['y'].str(20)} for u in und]
            if cv: say(f'FACET {name} c{j}=0 system {sysk}: COMMON CURVE {cv}')
        recs = []
        for p in fpts:
            stt = tone_status(H, p['_box'], KEVAL); zero = [k for k, v in stt.items() if v == 'zero?']
            cf = [float(b.mid()) for b in p['_box']]; s_ = sum(cf); cf = [x/s_ for x in cf]
            rec = {'seed_c': cf, 'zero_degrees': zero, 'orbit_size': symm.orbit_size(H, cf), 'design_strength': T.strength(H, zero),
                   'minpoly_x': p['minpoly_x'], 'minpoly_y': p['minpoly_y'], 'chart': chart}
            rec['zero_beyond_system_unproven'] = [k for k in zero if k not in {kk for kk, _ in p['sys']}]
            assess(H, rec, zero, oth, False)
            if rec['overdetermined_raw']: rec['symmetry'] = symm.explain(H, cf)
            recs.append(rec)
            if rec['overdetermined'] or (set(HIER[name][:2]) <= set(zero)):
                say(f'FACETPOINT {name} c{j}=0 seed {np.round(cf, 6).tolist()} zero {zero} strength {rec["design_strength"]} orbit {rec["orbit_size"]}'
                    + (f'  <<< OVER-DETERMINED {rec.get("symmetry")}' if rec['overdetermined'] else ''))
        facets.append({'zero_node': j, 'points': recs, 'undecided': fund})
        say(f'PROGRESS {(j+1)/H.r:.3f} {name} facet c{j}=0: {len(recs)} certified points with >= 2 conditions, {len(fund)} undecided pairs')
    res['facets'] = facets
    # ---------- edges and vertices (exact) ----------
    edges = []
    for a, b in itertools.combinations(range(H.r), 2):
        c0 = [K(0)]*H.r; c1 = [K(0)]*H.r; c0[a] = K(1); c1[b] = K(1)
        groups, ident = T.line_roots(H, c0, c1, KEVAL)
        pts = []
        for g in groups:
            cf = [0.0]*H.r; cf[a] = 1.0; cf[b] = float(g['root']['x'].mid())
            rec = {'t': g['root']['value'], 'minpoly_t': g['root']['minpoly'], 'degrees': sorted(g['degrees']), 'seed_c': cf}
            sym_ = bool(H.aut) and H.name == 'A4' and tuple(sorted((H.aut[0][a], H.aut[0][b]))) == (a, b) and rec['minpoly_t'] == ['-1', '1']
            assess(H, rec, rec['degrees'], [a, b], sym_)
            rec['design_strength'] = T.strength(H, rec['degrees'] + ident)
            if rec['overdetermined_raw']:
                rec['orbit_size'] = symm.orbit_size(H, cf); rec['symmetry'] = symm.explain(H, cf)
                say(f'EDGE {name} nodes {(a, b)} t = {rec["t"][:20]} minpoly {rec["minpoly_t"]} zero {rec["degrees"]}'
                    + (f'  <<< OVER-DETERMINED {rec["symmetry"]}' if rec['overdetermined'] else ' (explained by -I)'))
            pts.append(rec)
        edges.append({'nodes': [a, b], 'identically_zero_degrees': ident, 'points': pts})
        if ident: say(f'EDGE {name} nodes {(a, b)}: identically zero degrees {ident}')
    res['edges'] = edges
    verts = []
    for j in range(H.r):
        c = [K(1) if i == j else K(0) for i in range(H.r)]; u = H.u_exact(c)
        zero = [k for k in H.degrees(KEVAL) if all(v.iszero() for v in H.h_exact(k, c, u))]
        cf = [0.0]*H.r; cf[j] = 1.0
        rec = {'node': j, 'zero_degrees_exact': zero, 'orbit_size': symm.orbit_size(H, cf), 'design_strength': T.strength(H, zero)}
        assess(H, rec, zero, [j], False)
        if zero: rec['symmetry'] = symm.explain(H, cf)
        say(f'VERTEX {name} node {j} orbit {rec["orbit_size"]} zero (exact) {zero} strength {rec["design_strength"]}'
            + (f'  <<< OVER-DETERMINED {rec.get("symmetry")}' if zero else ''))
        verts.append(rec)
    res['vertices'] = verts
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(HERE, '..', 'data', f'four-{name}.json'), 'w'), indent=1, default=str)
    say(f'{name}: done in {res["seconds"]} s')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
