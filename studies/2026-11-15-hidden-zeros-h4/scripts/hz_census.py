#!/usr/bin/env python3
"""Hidden-zeros census.  Usage:
  hz_census.py catalogue [--no-p2] [--procs N]      H4 subgroup catalogue -> data/catalogue-h4.json
  hz_census.py analyse U600|U120|E8|U24|SNUB [--no-p2] [--procs N]   -> data/census-<U>.json
For every subgroup G in the catalogue and every universe P: G-orbits on P (and unions of two orbits when G has <= 8 orbits), exact tones
T_1..T_20, and the classification of every zero:
  G   forced by the set's stabiliser in Sym(P) (no invariant harmonic of that degree: Molien),
  X   forced by the set's own full symmetry group in O(n) (Gram automorphisms; Molien on the span),
  SPAN  the indicator lies in the rational span of explained-silent sets, closed under Sym(P)  (design bookkeeping),
  GAL   ... closed under Sym(P) and Double Vision (Galois sigma), but not without sigma,
  OPEN  none of these.
Exact arithmetic: tones and kernels in Q(sqrt5) (integer pairs / python-flint fmpz); Molien dimensions are floats rounded with a 1e-5 check."""
import sys, os, json, time, argparse
import numpy as np
from flint import fmpz_mat
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hz_core import *
from hz_universes import *
from hz_groups import *

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
KMAX = 20
def log(*a): print(*a, flush=True)

# ---------------------------------------------------------------- catalogue
def build_h4(no_p2=False, procs=20):
    X, A, lab, Lp, Rp, St, sig = h4_ambient()
    U = u600(X)
    mats = float_mats(U.Xf, A.P, A.basis)
    cat = Catalogue(A, mats)
    cat.reflection_subgroups(); log(f'PROGRESS 0.02 reflection subgroups: {len(cat.groups)} classes')
    cat.cyclic(); log(f'PROGRESS 0.03 + cyclic: {len(cat.groups)}')
    quaternion_families(cat, lab, X); log(f'PROGRESS 0.04 + quaternion families: {len(cat.groups)}')
    if not no_p2:
        two_generated(cat, procs, log); log(f'PROGRESS 0.30 + two-generated: {len(cat.groups)}')
    cat.derived(); log(f'PROGRESS 0.32 + rotation parts and -I: {len(cat.groups)}')
    return X, A, lab, sig, U, mats, cat

def generic_catalogue(A, mats, no_p2, procs):
    cat = Catalogue(A, mats)
    cat.reflection_subgroups(); cat.cyclic()
    if not no_p2: two_generated(cat, procs, log)
    cat.derived()
    return cat

def canon(Pa, S):
    """lexicographically least sorted image of the set S under the ambient permutations Pa"""
    im = np.sort(Pa[:, S], axis=1)
    o = np.lexsort(im.T[::-1])
    return tuple(int(x) for x in im[o[0]])

# ---------------------------------------------------------------- per-universe analysis
def analyse(uname, no_p2=False, procs=20):
    t0 = time.time()
    X, A, lab, sig, U600, mats600, cat = build_h4(no_p2 or uname in ('U24', 'SNUB'), procs)   # 24-cell, snub: own catalogue below
    if uname == 'U600':
        U, Pa, gal = U600, A.P, sig
        amb_mats = mats600; extra_gens = []
    elif uname == 'U120':
        Y, lift = cell120_from(X, A)
        U = Universe('120-cell', Y, 4, to_float(Y)); Pa = lift; gal = galois_perm(Y)
        amb_mats = float_mats(U.Xf, Pa, span_basis(U.Xf)); extra_gens = []
    elif uname == 'E8':
        P8, ipB, Yf = e8_from(X)
        U = Universe('E8 roots', P8, 8, Yf, ipfun=ipB); Pa = np.hstack([A.P, A.P + 120]).astype(np.int32); gal = None
        amb_mats = float_mats(U.Xf, Pa, span_basis(U.Xf)); extra_gens = list(e8_reflections(P8, ipB))
    elif uname in ('U24', 'SNUB'):
        Xf600 = U600.Xf
        rat = np.nonzero((X[..., 1] == 0).all(1))[0]
        idx = rat if uname == 'U24' else np.setdiff1d(np.arange(120), rat)
        Y = X[idx]
        U = Universe('24-cell' if uname == 'U24' else 'snub 24-cell', Y, 4, to_float(Y) / 2)
        perms, basis = sym_perms(U.IM, U.Xf)
        log(f'{U.name}: {U.N} points, symmetry group order {len(perms)}')
        A = Ambient(perms, basis); Pa = A.P
        amb_mats = float_mats(U.Xf, Pa, A.basis)
        cat = generic_catalogue(A, amb_mats, no_p2, procs)
        gal = galois_perm(Y); extra_gens = []
    else:
        raise SystemExit('unknown universe')
    N = U.N
    log(f'PROGRESS 0.35 {U.name}: N={N}, {len(cat.groups)} subgroup classes, ambient order {len(Pa)}, galois={"yes" if gal is not None else "no"} ({time.time()-t0:.0f}s)')
    chi = harm_char_table(amb_mats, KMAX, U.dim)               # per ambient element
    mi = np.nonzero(np.abs(amb_mats + np.eye(amb_mats.shape[1])).max(axis=(1, 2)) < 1e-9)[0]
    minus_perm = Pa[mi[0]] if len(mi) else None
    log(f'-I in the ambient group: {minus_perm is not None}')
    dimG_all = np.rint(chi.mean(0)).astype(int).tolist()
    # ---- sets: orbits and unions of two orbits
    sets = {}
    def add_set(S, gi, kind):
        S = np.asarray(sorted(S), dtype=np.int64)
        key = canon(Pa, S)
        if key not in sets:
            sets[key] = {'key': key, 'size': len(S), 'rep': S.tolist(), 'groups': [], 'kind': kind}
        rec = sets[key]
        if len(rec['groups']) < 6 and gi not in rec['groups']: rec['groups'].append(gi)
    for gi, G in enumerate(cat.groups):
        gp = Pa[G['gens']]
        orbs = orbits_from_gens(gp, N)
        G.setdefault('orbits', {})[uname] = sorted(len(o) for o in orbs)
        for o in orbs: add_set(o, gi, 'orbit')
        if len(orbs) <= 8:
            for i in range(len(orbs)):
                for j in range(i + 1, len(orbs)):
                    add_set(np.concatenate([orbs[i], orbs[j]]), gi, 'union')
        if gi % max(1, len(cat.groups) // 20) == 0:
            log(f'PROGRESS {0.35 + 0.15 * gi / len(cat.groups):.3f} sets from group {gi}/{len(cat.groups)}: {len(sets)} distinct sets')
    # every union of twisted classes (subgroups of 2I, or 2O for the 24-cell) is added as a set of its own
    tw = {}
    if uname in ('U600', 'SNUB', 'U24'):
        from hz_twisted import build_twisted, hom_dim, intertwines, qmul
        if uname == 'U24':
            T2 = U.Xf; c = np.array([1, 1, 0, 0]) / 2 ** 0.5
            base = np.vstack([T2, np.array([qmul(c, t) for t in T2])])
            cinv = np.array([c[0], -c[1], -c[2], -c[3]])
            def translate(pts):
                in2T = lambda p: np.allclose(np.abs(p) * 2 % 1, 0, atol=1e-7)
                if all(in2T(p) for p in pts): return pts
                q = np.array([qmul(cinv, p) for p in pts])
                return q if all(in2T(p) for p in q) else None
        else:
            base = U600.Xf; translate = None
        tw = build_twisted(U.Xf, base, lambda S_: canon(Pa, S_), translate, right_translates=(uname != 'U600'), log=log)
        for key, lst in tw.items():
            if key not in sets:
                sets[key] = {'key': key, 'size': len(lst[0]['idx']), 'rep': lst[0]['idx'], 'groups': [], 'kind': 'twisted'}
    log(f'{len(sets)} distinct sets (up to the ambient group)')
    # ---- per-set exact analysis
    recs = list(sets.values())
    for ri, r in enumerate(recs):
        S = np.array(r['rep'])
        r['zeros'] = U.zeros(S)
        inS = np.zeros(N, bool); inS[S] = True
        stab = np.nonzero(inS[Pa[:, S]].all(1))[0]
        r['stab_order'] = int(len(stab))
        dS = np.rint(chi[stab].mean(0)).astype(int).tolist()
        r['dim_stab'] = dS
        r['G'] = [k for k in r['zeros'] if dS[k] == 0]
        rest = [k for k in r['zeros'] if dS[k] != 0]
        r['X'] = []; r['sym_order'] = None
        if rest:
            sp, sb = sym_perms(U.IM[np.ix_(S, S)], U.Xf[S], cap=(20000 if uname == 'E8' else 300000))
            if sp is not None:
                r['sym_order'] = int(len(sp))
                M = float_mats(U.Xf[S], sp, sb)
                dX = harm_dims(M, KMAX, U.dim)
                r['span_dim'] = int(M.shape[1]); r['dim_sym'] = dX
                r['X'] = [k for k in rest if dX[k] == 0]
            else:
                r['sym_order'] = '>300000'
        r['after_X'] = [k for k in rest if k not in r['X']]
        # ZONAL: the stabiliser fixes exactly one axis e (the centroid direction), its only invariant harmonic of degree k is the zonal
        # one about e, and all points lie on one latitude: then T_k = 0 <=> G_k(cos theta) = 0 (e.g. U_k(cos theta) = 0 at theta = j pi/(k+1)).
        r['ZONAL'] = []
        if r['after_X']:
            Mst = amb_mats[stab]; Pf = Mst.mean(0); fixdim = int(round(np.trace(Pf)))
            c = U.Xf[S].sum(0)
            if fixdim == 1 and np.linalg.norm(c) > 1e-9:
                cs = U.Xf[S] @ c / (np.linalg.norm(U.Xf[S], axis=1) * np.linalg.norm(c))
                if np.ptp(cs) < 1e-9:
                    r['latitude_deg'] = float(np.degrees(np.arccos(np.clip(cs[0], -1, 1))))
                    r['ZONAL'] = [k for k in r['after_X'] if dS[k] == 1]
            # the same test with the set's full symmetry group (it may exceed the stabiliser in Sym(P))
            if r['after_X'] and r.get('dim_sym') and r.get('span_dim') == U.dim:
                Pf2 = M.mean(0); fd2 = int(round(np.trace(Pf2)))
                if fd2 == 1 and np.linalg.norm(c) > 1e-9:
                    cs = U.Xf[S] @ c / (np.linalg.norm(U.Xf[S], axis=1) * np.linalg.norm(c))
                    if np.ptp(cs) < 1e-9:
                        r['latitude_deg'] = float(np.degrees(np.arccos(np.clip(cs[0], -1, 1))))
                        r['ZONAL'] += [k for k in r['after_X'] if r['dim_sym'][k] == 1 and k not in r['ZONAL']]
            r['after_X'] = [k for k in r['after_X'] if k not in r['ZONAL']]
        if gal is not None:
            gS = sorted(int(gal[i]) for i in S)
            r['galois_self'] = canon(Pa, np.array(gS)) == r['key']
        if ri % max(1, len(recs) // 20) == 0:
            log(f'PROGRESS {0.50 + 0.25 * ri / len(recs):.3f} sets analysed {ri}/{len(recs)} ({time.time()-t0:.0f}s)')
    # ---- twisted silence (classes and unions of twisted classes of subgroups of 2I / 2O)
    for r in recs: r['TW'] = []
    if tw:
        ntw = 0
        for r in recs:
            lst = tw.get(r['key'])
            if not lst: continue
            t = min(lst, key=lambda u: u['n_classes_used']); per = {}
            for k in r['after_X']:
                hd = hom_dim(t['Q'], t['S'], t['gens'], t['alpha'], k)
                err, nrm = intertwines(t['Q'], t['sel'], t['gens'], t['alpha'], k)
                per[k] = {'hom_dim': hd, 'intertwine_err': err, 'sum_norm': nrm,
                          'type': 'forced (no alpha-stable constituent)' if hd == 0 else 'twisted character zero'}
                if err > 1e-7 or nrm > 1e-7: CHECKS.append((f'twisted intertwining/zero at k={k} size {r["size"]}', False))
            r['twisted'] = {'G_order': t['G_order'], 'alpha_inner': t['alpha_inner'], 'class_sizes': t['class_sizes'],
                            'n_classes_used': t['n_classes_used'], 'degrees': per,
                            'other_realisations': [(u['G_order'], u['alpha_inner'], u['class_sizes']) for u in lst[1:]]}
            # explained: no alpha-stable constituent (forced), or a single twisted class with twisted character zero.
            # A zero of a union of several classes that no single class has is a cancellation: kept OPEN, flagged TWU.
            r['TW'] = [k for k in r['after_X'] if k in per and (per[k]['hom_dim'] == 0 or t['n_classes_used'] == 1)]
            r['TWU'] = [k for k in r['after_X'] if k in per and k not in r['TW']]
            r['after_X'] = [k for k in r['after_X'] if k not in r['TW']]
            ntw += 1
        CHECKS.append(('twisted intertwining identity and zero sums', all(c_[1] for c_ in CHECKS if c_[0].startswith('twisted'))))
        log(f'twisted-class unions among the census sets: {ntw}')
    # ---- rational kernels N_k and explained spans E_k
    gram_mats = []
    for k in range(KMAX + 1):
        ga = [g[0] for g in U.G[k]]; gb = [g[1] for g in U.G[k]]
        den = 1
        for v in ga + gb: den = np.lcm(den, v.denominator)
        ia = np.array([int(v * den) for v in ga], dtype=object); ib = np.array([int(v * den) for v in gb], dtype=object)
        Ak = ia[U.IM]; Bk = ib[U.IM]
        gram_mats.append(fmpz_mat(np.vstack([Ak, Bk]).tolist()))
    def in_kernel(k, v):
        return (gram_mats[k] * fmpz_mat([[int(x)] for x in v])).is_zero()
    # consistency: T_k(S) = 0  <=>  1_S in N_k
    bad = 0
    for r in recs[:400]:
        v = np.zeros(N, int); v[r['rep']] = 1
        for k in range(1, KMAX + 1):
            if in_kernel(k, v) != (k in r['zeros']): bad += 1
    log(f'CHECK tone/kernel consistency on {min(400, len(recs))} sets: {"ok" if bad == 0 else f"FAIL {bad}"}')
    CHECKS.append(('tone-kernel consistency', bad == 0))
    kern = []
    for k in range(KMAX + 1):
        Xn, nul = gram_mats[k].nullspace()
        kern.append((Xn, nul))
    dims_N = [int(kern[k][1]) for k in range(KMAX + 1)]
    log(f'dim N_k = {dims_N}')
    # linkage: N_j subset N_k  (T_j(S)=0 implies T_k(S)=0 for every rational weighting S)
    link = {}
    for j in range(1, KMAX + 1):
        Xn, nul = kern[j]
        impl = []
        if nul:
            XL = Xn.tolist(); Bj = fmpz_mat([row[:nul] for row in XL])
        for k in range(1, KMAX + 1):
            if k == j: continue
            if nul == 0 or (gram_mats[k] * Bj).is_zero(): impl.append(k)
        link[j] = impl
    log(f'PROGRESS 0.80 linkage done ({time.time()-t0:.0f}s)')
    # generators of the ambient (for closing spans)
    rng = np.random.default_rng(7)
    amb_gens = []
    if uname in ('U24', 'SNUB'):
        amb_idx = np.arange(A.n); cl = np.array([A.e])
        while len(cl) < A.n:
            g = int(rng.integers(A.n)); amb_gens.append(g); cl = A.closure(amb_gens)
        amb_perm_gens = [Pa[g] for g in amb_gens]
    else:
        H = []; cl = np.array([A.e])
        while len(cl) < A.n:
            g = int(rng.integers(A.n)); H.append(g); cl = A.closure(H)
        amb_perm_gens = [Pa[g] for g in H]
    amb_perm_gens += extra_gens
    def close_span(vecs, use_gal, wrong=None):
        if not vecs: return None, 0
        M = fmpz_mat([list(map(int, v)) for v in vecs])
        def rows_of(M):
            rk = M.rank(); R = M.rref()[0]
            return [list(map(int, row)) for row in R.tolist()[:rk]], rk
        rows, rk = rows_of(M)
        maps = list(amb_perm_gens) + ([gal] if use_gal else []) + ([wrong] if wrong is not None else [])
        while True:
            new = list(rows)
            for p in maps:
                inv = np.argsort(p)
                for row in rows: new.append([row[int(inv[j])] for j in range(N)])     # (v o p^-1)
            rows2, rk2 = rows_of(fmpz_mat(new))
            if rk2 == rk: return rows, rk
            rows, rk = rows2, rk2
    def annihilator(rows):
        if rows is None: return None
        Xn, nul = fmpz_mat(rows).nullspace()
        return np.array([[int(x) for x in row[:nul]] for row in Xn.tolist()], dtype=object) if nul else np.zeros((N, 0), dtype=object)
    def member(ann, v):
        if ann is None: return False
        return not np.any(np.asarray(v, dtype=object) @ ann != 0)
    def subset_of_kernel(rows, k):
        if rows is None: return True
        return (gram_mats[k] * fmpz_mat(rows).transpose()).is_zero()
    expl_dim = {}
    for r in recs: r['SPAN'] = []; r['GAL'] = []
    wrong_fail = []
    for k in range(1, KMAX + 1):
        todo = [r for r in recs if k in r['after_X']]
        gens = [np.isin(np.arange(N), r['rep']).astype(int) for r in recs if k in r['G'] or k in r['X'] or k in r['ZONAL'] or k in r['TW']]
        if dimG_all[k] == 0: gens.append(np.ones(N, int))
        if minus_perm is not None:          # parity: S and -S have equal even tones and opposite odd harmonic parts
            for x in range(N):
                v = np.zeros(N, int); v[x] += 1; v[minus_perm[x]] += -1 if k % 2 == 0 else 1
                if v.any(): gens.append(v)
        if not todo:
            expl_dim[k] = None; continue
        rows0, rk0 = close_span(gens, False)
        ok0 = subset_of_kernel(rows0, k); CHECKS.append((f'E_{k} inside N_{k} (no sigma)', ok0))
        rows1, rk1 = (close_span(gens, True) if gal is not None else (rows0, rk0))
        ok1 = subset_of_kernel(rows1, k); CHECKS.append((f'E_{k} inside N_{k} (with sigma)', ok1))
        expl_dim[k] = (rk0, rk1, dims_N[k])
        an0 = annihilator(rows0); an1 = annihilator(rows1) if gal is not None else None
        for r in todo:
            v = np.isin(np.arange(N), r['rep']).astype(int)
            if member(an0, v): r['SPAN'].append(k)
            elif gal is not None and member(an1, v): r['GAL'].append(k)
        # negative control: a wrong 'Double Vision' (random permutation) must break E_k inside N_k for some k
        if gal is not None and k in (3, 5, 7) and gens:
            wp = rng.permutation(N)
            rw, _ = close_span(gens, False, wrong=wp)
            wrong_fail.append(not subset_of_kernel(rw, k))
        log(f'PROGRESS {0.80 + 0.18 * k / KMAX:.3f} degree {k}: E dims (no sigma, sigma, N_k) = {expl_dim[k]}, {len(todo)} sets to explain')
    if wrong_fail:
        CHECKS.append(('wrong Double Vision (random permutation) is caught by the soundness check', all(wrong_fail)))
    # open zeros and their number of independent conditions on stabiliser-invariant weightings
    for r in recs:
        r['OPEN'] = [k for k in r['after_X'] if k not in r['SPAN'] and k not in r['GAL']]
        if r['OPEN']:
            S = np.array(r['rep']); inS = np.zeros(N, bool); inS[S] = True
            stab = np.nonzero(inS[Pa[:, S]].all(1))[0]
            orbs = orbits_from_gens(Pa[stab[:min(len(stab), 64)]], N) if len(stab) else [np.array([i]) for i in range(N)]
            # exact stabiliser orbits need all stabiliser elements: use them all
            orbs = orbits_from_gens(Pa[stab], N)
            Fm = fmpz_mat([[1 if i in set(o.tolist()) else 0 for o in orbs] for i in range(N)])
            per = {}
            stack = []
            for k in r['OPEN']:
                Z = gram_mats[k] * Fm; per[k] = Z.rank(); stack.append(Z)
            r['conditions_per_degree'] = per
            big = fmpz_mat([[stack[s][a, b] for b in range(len(orbs))] for s in range(len(stack)) for a in range(stack[s].nrows())])
            r['conditions'] = big.rank(); r['stab_orbits'] = len(orbs)
    out = {'universe': U.name, 'N': N, 'dim': U.dim, 'ambient_order': int(len(Pa)), 'galois': gal is not None,
           'cosines': [qstr(c) for c in U.cos], 'dim_harm_ambient': dimG_all, 'dim_N': dims_N, 'linkage': link,
           'explained_span_dims': expl_dim, 'n_groups': len(cat.groups),
           'groups': [{'order': g['order'], 'src': g['src'][:4], 'gens': g['gens'], 'orbits': g.get('orbits', {}).get(uname)} for g in cat.groups],
           'sets': [{k: v for k, v in r.items() if k not in ('key',)} for r in recs], 'checks': CHECKS}
    return out

CHECKS = []
def jdump(o, path):
    def cv(x):
        if isinstance(x, (np.integer,)): return int(x)
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, tuple): return list(x)
        raise TypeError(type(x))
    json.dump(o, open(path, 'w'), default=cv)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('uni', nargs='?')
    ap.add_argument('--no-p2', action='store_true'); ap.add_argument('--procs', type=int, default=20); ap.add_argument('--tag', default='')
    a = ap.parse_args()
    if a.cmd == 'analyse':
        out = analyse(a.uni, a.no_p2, a.procs)
        path = os.path.join(DATA, f'census-{a.uni}{a.tag}.json'); jdump(out, path)
        nopen = sum(1 for s in out['sets'] if s['OPEN'])
        log(f'{out["universe"]}: {len(out["sets"])} sets, {nopen} with OPEN zeros; checks {sum(c[1] for c in CHECKS)}/{len(CHECKS)} ok')
        for s in out['sets']:
            if s['OPEN'] or s['GAL'] or s['TW']:
                log(f'  size {s["size"]} {s["kind"]} stab {s["stab_order"]} sym {s["sym_order"]} zeros {s["zeros"]} G {s["G"]} X {s["X"]} ZONAL {s["ZONAL"]} TW {s["TW"]} SPAN {s["SPAN"]} GAL {s["GAL"]} OPEN {s["OPEN"]} cond {s.get("conditions")} gal-self {s.get("galois_self")}')
        print('FINAL ok' if all(c[1] for c in CHECKS) else 'FINAL FAIL (a check failed: ' + '; '.join(c[0] for c in CHECKS if not c[1]) + ')')
