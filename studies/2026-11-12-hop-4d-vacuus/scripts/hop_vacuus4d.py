"""hop_vacuus4d.py - DICTO 11 Nov 2026: "most likely a 4D vacuus that is very sophisticated but that should narrow it down" +
"c the permutahedron 4D vacuus". The Vacuus of the OG hop's 4D sweep built the way the 4D permutohedron's was (#105), with ONE engine
(vac4.py) for the controls and the sweep. Study 2026-11-12-hop-4d-vacuus (question and plan in its README, written first).
  Part 1 POSITIVE control: 4D permutohedron (centred 1..5, 30 facets, integers): f-vector (120, 240, 150, 30); N = 65 central slices at
         its centre; classes 30/20/10/5 with corner/face counts as #105; a scan along a generic line through the centre finds the centre
         as the deepest drop.
  Part 2 NEGATIVE controls: the permutohedron with random rational facet offsets (no lining up at the centre: N = 150, no non-trivial
         special height inside); the sweep at the first level with every b_j moved by a random rational factor (no coincident walls
         at any height: no mirror sheets, no non-trivial special height).
  Part 3 the hop k -> k+1, k = KMIN..KMAX: exact candidates (Q(sqrt5)), the sweep P = {X_j.y - lam <= b_j, 0 <= lam <= LAM}, walls =
         cell-cell 2-faces (checked against og-margin §31a), cut = cells missing from the floor; N(t) for the centre (O, t): exact at
         generic heights; every special height exact (gcd over Q(sqrt5)); INSIDE (t > 0) vs outside; slice classes (I_h) at two
         generic inside heights and the inside special heights with the largest drops: 3D shapes and wall types (aa / ac / cc);
         test T1: do slice types carrying a cut cell's wall differ from those carrying only survivor walls? random orbit labels as a
         negative control for T1 (20 draws).
usage: python -u hop_vacuus4d.py <five-fold-octet dir> <og-margin scripts dir> <kmin> <kmax> <out.json>"""
import sys, os, json, time, itertools, random
from collections import Counter
from fractions import Fraction
import numpy as np
from gmpy2 import mpq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from vac4 import R5, ZERO, ONE, dot, Poly4, special_heights, uf_count, slice_shape, slice_shape_exact, class_key, rank_r5
OCTET, OGM, KMIN, KMAX, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), os.path.abspath(sys.argv[5])
t0 = time.time(); fails = []; res = {'mark': 'DICTO · hop 4D Vacuus scan · dictospheres.com', 'controls': {}, 'levels': []}
STAGES = 3 + (KMAX - KMIN + 1)
SHAPE_KMAX = 5   # exact slice shapes only where they pass Euler: k = 6 pilots failed (float corners of near-degenerate slices; LEAD)
def prog(stage, frac, what): print(f'PROGRESS {(stage + frac) / STAGES:.4f} {what} ({time.time() - t0:.0f}s)', flush=True)
def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what, flush=True)
    if not ok: fails.append(what)
    return ok
def save(): json.dump(res, open(OUT, 'w'), indent=1, default=str)
def hkey_str(h): return repr(h) if isinstance(h, R5) else f'root of t^2 + ({h[2].f():.6g}) t + ({h[1].f():.6g}), sign {h[3]}'

def scan(poly, ridges, c0, u, inside, trivial, stage, label, gen_t):
    """N at the special heights along c0 + t u. The walls that share a slice at EVERY height ('always', e.g. the mirror sheets) are
    taken EXACTLY from the slice partition at the generic heights gen_t (exact R5), which must agree (else FAIL)."""
    A, B = poly.nu_line(ridges, c0, u)
    always_f, heights, st = special_heights(A, B, progress=lambda f: prog(stage, 0.8 * f, f'{label}: special-height search'))
    parts = []
    for t in gen_t:
        gr, thr = poly.count_exact(A, B, t); parts.append(sorted(sorted(g) for g in gr.values()))
    check(all(p == parts[0] for p in parts) and not thr, f'{label}: exact slice partitions agree at {len(gen_t)} generic heights ({len(parts[0])} slices)')
    always = [(g[i], g[i + 1]) for g in parts[0] for i in range(len(g) - 1)]
    st['always_float_prefilter'] = len(always_f)
    Ng, _ = uf_count(len(ridges), always)
    rows = []
    for key, (tf, prs) in heights.items():
        N, lab = uf_count(len(ridges), always + prs)
        triv = trivial(key) if isinstance(key, R5) else False
        par = sum(1 for i, j in prs if rank_r5([poly.N[x] for x in ridges[i] + ridges[j]]) == 2)   # the two 2-faces are parallel (exact)
        rows.append(dict(key=key, t=tf, N=N, drop=Ng - N, pairs=len(prs), parallel_pairs=par, inside=bool(inside(tf, key)), trivial=triv, lab=lab))
    rows.sort(key=lambda r: (-r['drop'], r['t']))
    return A, B, always, Ng, rows, st

# ---------------- Part 1: the 4D permutohedron, positive control ----------------
vals = [2, 1, 0, -1, -2]
def perm_facets(offsets=None):
    N, H = [], []
    for m in range(1, 5):
        for S in itertools.combinations(range(5), m):
            n5 = [1 if i in S else 0 for i in range(5)]
            N.append(tuple(R5(n5[i] - n5[4]) for i in range(4))); H.append(R5(sum(vals[:m])))
    if offsets is not None: H = [h + R5(d) for h, d in zip(H, offsets)]
    return N, H
L = np.vstack([np.eye(4), -np.ones((1, 4))])
Gperm = []
for sg in itertools.permutations(range(5)):
    Pm = np.eye(5)[list(sg)]
    for s in (1, -1):
        Mpt = s * (Pm @ L)[:4]; Gperm.append(np.linalg.inv(Mpt).T)
C0 = (ZERO,) * 4; U = tuple(R5(x) for x in (1, 3, -2, 5))
def perm_run(N, H, stage, label):
    poly = Poly4(N, H).enumerate(np.zeros(4))
    inside = lambda tf, key: bool((poly.Hf - poly.Nf @ (tf * np.array([1, 3, -2, 5.]))).min() > 0)
    def trivial(t):
        c = tuple(t * x for x in U); return any((h - dot(n, c)).iszero() for n, h in zip(N, H))
    A, B, always, Ng, rows, st = scan(poly, poly.ridges, C0, U, inside, trivial, stage, label, [R5(mpq(37, 1013)), R5(mpq(-53, 997)), R5(mpq(101, 1009))])
    groups, through = poly.count_exact(A, B, ZERO)
    return poly, A, B, always, Ng, rows, st, groups, through

prog(0, 0, 'permutohedron (positive control)')
poly, A, B, always, Ng, rows, st, groups, through = perm_run(*perm_facets(), 0, 'permutohedron')
check(poly.fvec == (120, 240, 150, 30) and poly.euler == 0, f'permutohedron f-vector {poly.fvec}, Euler {poly.euler}, incidence gap {poly.gap:.2e}')
check(len(groups) == 65 and not through, f'permutohedron: {len(groups)} central slices at the centre carry the {len(poly.ridges)} 2-faces (#105: 65)')
cls = {}
for k_, ws in groups.items():
    f, g = poly.ridges[ws[0]]; nu = [x.f() for x in k_]
    cls.setdefault(class_key(nu, Gperm), []).append(ws)
shapes = []
for ck, mem in cls.items():
    sh = slice_shape(poly, np.zeros(4), [x.f() for x in next(k_ for k_, ws in groups.items() if ws is mem[0])])
    shapes.append((len(mem), sh['V'], sh['E'], sh['F'], sh['sizes'], sum(len(w) for w in mem), sh['euler']))
shapes.sort(key=lambda s: (-s[0], -s[1]))
print('  classes (count, corners, edges, faces, face sizes, 2-faces carried, Euler): ' + '; '.join(str(s) for s in shapes))
want = sorted([(30, 32, 52, 22), (20, 24, 36, 14), (10, 24, 42, 20), (5, 24, 36, 14)])
check(sorted(s[:4] for s in shapes) == want and all(s[6] == 2 for s in shapes), 'permutohedron slice classes = #105 (30 x 32/52/22, 20 x 24/36/14, 10 x 24/42/20, 5 x 24/36/14)')
inside_rows = [r for r in rows if r['inside'] and not r['trivial']]
deep = min(inside_rows, key=lambda r: r['N']) if inside_rows else None
check(Ng == 150 and deep is not None and isinstance(deep['key'], R5) and deep['key'] == ZERO and deep['N'] == 65,
      f'scan along a generic line: generic N {Ng}; deepest inside drop at t = {deep and deep["t"]} with N = {deep and deep["N"]} (want t = 0, N = 65)')
print(f'  inside special heights on the line: {len(inside_rows)}: ' + ', '.join(f't {r["t"]:+.4f} N {r["N"]}' for r in sorted(inside_rows, key=lambda r: r["t"])) + f' | prefilter {st}')
res['controls']['permutohedron'] = dict(fvec=poly.fvec, N_centre=len(groups), classes=shapes, generic_N=Ng,
                                        inside_special=[(r['t'], r['N']) for r in inside_rows], prefilter=st)
save()

# ---------------- Part 2: negative controls ----------------
prog(1, 0, 'perturbed permutohedron (negative control)')
rng = random.Random(20261112)
offs = [mpq(rng.randint(-25, 25), 1000) for _ in range(30)]
poly2, A2, B2, al2, Ng2, rows2, st2, groups2, through2 = perm_run(*perm_facets(offs), 1, 'perturbed permutohedron')
ins2 = [r for r in rows2 if r['inside'] and not r['trivial']]
check(poly2.fvec == (120, 240, 150, 30), f'perturbed permutohedron f-vector {poly2.fvec} (same as the permutohedron)')
other = max([r['drop'] for r in inside_rows if r['key'] != ZERO], default=0); md2 = max([r['drop'] for r in ins2], default=0)
check(len(groups2) == 150 and md2 <= other and not al2,
      f'perturbed permutohedron: {len(groups2)} slices at the old centre (want 150: nothing lines up there); largest inside drop {md2} '
      f'(want <= {other}, the largest non-centre drop of the permutohedron: parallel 2-faces keep their heights); always-coincident pairs {len(al2)}')
print('  perturbed permutohedron inside drops: ' + str(sorted(Counter(r['drop'] for r in ins2).items())), flush=True)
res['controls']['perturbed_permutohedron'] = dict(fvec=poly2.fvec, N_centre=len(groups2), inside_special=len(ins2), all_special=len(rows2))
save()

# ---------------- the OG family, exact (exact_family.py of og-margin) ----------------
ns = {'__file__': os.path.join(OCTET, 'exact_upward.py')}; argv0 = list(sys.argv); sys.argv = [argv0[0], OCTET, '0', '/dev/null']; cwd = os.getcwd()
exec(open(os.path.join(OGM, 'exact_family.py')).read().split('t0 = time.time()')[0], ns)
sys.argv = argv0; os.chdir(cwd)
OGX, cvx, exact_faces, xdot, GX = ns['OG'], ns['cv'], ns['exact_faces'], ns['dot'], ns['GX']
ns2 = {'__file__': os.path.join(OCTET, 'exact_upward.py')}; sys.argv = [argv0[0], OCTET, '0', '0', '/dev/null']
exec(open(os.path.join(OGM, 'og_exchanges.py')).read().split('rows = []; ok_all = True')[0], ns2)
sys.argv = argv0; os.chdir(cwd)
OGX_choose, OGX_events, OGX_adj = ns2['choose_LAM'], ns2['events'], ns2['adjacency']
Gi = [np.array([[x.f() for x in row] for row in M]) for M in GX]
G4 = []
for g in Gi:
    for s in (1, -1):
        M = np.eye(4); M[:3, :3] = s * g; G4.append(M)                    # I_h acting on (y, lam); orthogonal so normals map alike
EXP = {5: (252, 60, 750, 465), 6: (320, 60, 930, 615), 7: (402, 90, 1170, 1035), 8: (500, 0, 1410, 1095), 9: (732, 252, 2310, 1875),
       10: (662, 192, 2040, 1635), 11: (672, 132, 2040, 1695)}           # og-margin §31a: cells, cut, walls, generic slices

def sweep(Xe, be):
    """Poly4 of the capped sweep; LAM above every event (as og_exchanges.choose_LAM)."""
    n = len(Xe); N = [tuple(x) + (R5(-1),) for x in Xe] + [(ZERO, ZERO, ZERO, R5(-1))]; H = list(be) + [ZERO]
    fr = Fraction(max(b.f() for b in be)).limit_denominator(1000); lam = mpq(4) * mpq(fr.numerator, fr.denominator) + 1
    for _ in range(12):
        p = Poly4(N + [(ZERO, ZERO, ZERO, ONE)], H + [R5(lam)], labels=['c'] * n + ['floor', 'top']).enumerate(np.array([0, 0, 0, float(lam) / 2]))
        ev = p.P[(p.P[:, 3] < float(lam) * (1 - 1e-9))][:, 3]
        if ev.max() < float(lam) / 4: return p, lam
        lam *= 4
    raise RuntimeError('LAM search failed')

def cell_orbits(Xf):
    from scipy.spatial import cKDTree
    tr = cKDTree(Xf); lab = -np.ones(len(Xf), int); o = 0
    for i in range(len(Xf)):
        if lab[i] >= 0: continue
        for g in Gi:
            for s in (1, -1):
                d, j = tr.query(s * g @ Xf[i])
                if d < 1e-8: lab[j] = o
        o += 1
    return lab

We = [tuple(cvx(x) for x in v) for v in OGX]
for k in range(KMAX + 1):
    idx = {v: i for i, v in enumerate(We)}; Wfx = np.array([[x.f() for x in v] for v in We])
    Fx, _, _ = exact_faces(We, idx, Wfx); feet = {}
    for n_, d_, _ in Fx.values():
        s_ = d_ / xdot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    feet = list(feet)                                                       # exact corners of D_{k+1} = candidates of hop k
    if k >= KMIN:
        stage = 3 + k - KMIN; tk = time.time()
        Xe = []
        for w in feet:
            wm = [R5(x.a, x.b) for x in w]; w2 = dot(wm, wm); Xe.append([x / w2 for x in wm])
        fr = Fraction(max(np.linalg.norm([x.f() for x in X]) for X in Xe)).limit_denominator(1000); q = R5(mpq(fr.numerator, fr.denominator))
        Xe = [tuple(x / q for x in X) for X in Xe]; be = [dot(X, X) for X in Xe]; n = len(Xe)
        maxb = max(be, key=lambda b: b.f())
        poly, lam = sweep(Xe, be)
        walls_e = [(f, g) for f, g in poly.ridges if f < n and g < n]
        enum_ok = poly.euler == 0 and len(poly.facets) == n + 2
        # walls = cell-cell 2-faces of the float 4D enumeration; used only where it is a 4D polytope (Euler 0) - checked below against §31a
        walls = walls_e
        floor = {f for f, g in poly.ridges if g == n and f < n} | {g for f, g in poly.ridges if f == n and g < n}
        act = np.array([j in floor for j in range(n)]); ncut = int((~act).sum())
        print(f'k {k}: {n} cells, cut {ncut}, walls {len(walls)}, 4D float enumeration f-vector {poly.fvec} Euler {poly.euler}, incidence gap {poly.gap:.2e} '
              f'(max tight residual {poly.maxres:.1e}); LAM/max b {float(lam) / maxb.f():.2f}', flush=True)
        if not enum_ok:                                                     # recorded as SKIPPED (an outcome, not hidden): see README
            print(f'  k {k} SKIPPED: walls not trustworthy at this level (see og-margin §31a for its counts)', flush=True)
            res['levels'].append(dict(k=k, skipped='float 4D enumeration fails Euler')); save(); prog(stage, 1, f'k {k} skipped'); We = feet; continue
        if k in EXP: check((n, ncut, len(walls)) == EXP[k][:3], f'k {k}: cells/cut/walls {(n, ncut, len(walls))} = og-margin §31a {EXP[k][:3]}')
        typ = [int(act[f]) + int(act[g]) for f, g in walls]                    # 2 aa, 1 ac, 0 cc
        U4 = (ZERO, ZERO, ZERO, ONE)
        bset = set(be)
        trivial = lambda t: t.iszero() or (-t) in bset                          # centre on the floor or on a cell's hyperplane
        A, B, always, Ng, rows, st = scan(poly, walls, C0, U4, lambda tf, key: tf > 0, trivial, stage, f'k {k}', [maxb * R5(mpq(1, 3)), maxb, maxb * R5(mpq(-2718, 10000))])
        gen = {}
        for name, t in (('inside maxb/3', maxb * R5(mpq(1, 3))), ('inside maxb', maxb), ('outside -0.2718 maxb', maxb * R5(mpq(-2718, 10000)))):
            gr, thr = poly.count_exact(A, B, t); gen[name] = len(gr) + (1 if thr else 0)
        check(len(set(gen.values())) == 1 and Ng in gen.values(), f'k {k}: exact slice counts at three generic heights {gen} agree with the union count {Ng}')
        if k in EXP: check(Ng == EXP[k][3], f'k {k}: generic N {Ng} = og-margin §31a {EXP[k][3]}')
        nontriv = [r for r in rows if not r['trivial']]; ins = [r for r in nontriv if r['inside']]
        print(f'  special heights: {len(rows)} ({len(rows) - len(nontriv)} trivial), non-trivial {len(nontriv)}, INSIDE the solid {len(ins)}; '
              f'always-coincident wall pairs {len(always)}; prefilter {st}', flush=True)
        print(f'  inside heights by drop: ' + str(sorted(Counter(r['drop'] for r in ins).items())) + f'; pairs at inside heights {sum(r["pairs"] for r in ins)}, of them parallel walls {sum(r["parallel_pairs"] for r in ins)}', flush=True)
        print(f'  largest drops: all ' + ', '.join(f'{r["drop"]}@{r["t"] / maxb.f():+.4f}' for r in nontriv[:6]) +
              ' | inside ' + ', '.join(f'{r["drop"]}@{r["t"] / maxb.f():+.4f}' for r in ins[:8]), flush=True)
        check(all(r['drop'] >= 0 for r in rows), f'k {k}: special heights only merge slices')
        # slice classes and test T1 at two generic inside heights and the inside special heights with the largest drops
        orb = cell_orbits(np.array([[x.f() for x in X] for X in Xe]))
        picks = [('generic maxb/3', maxb.f() / 3, None, maxb * R5(mpq(1, 3))), ('generic maxb', maxb.f(), None, maxb)] + \
                [(f'special drop {r["drop"]}', r['t'], r, r['key'] if isinstance(r['key'], R5) else None) for r in ins[:5]]
        lab_g = uf_count(len(walls), always)[1]
        lvl_slices = []; do_shapes = k <= SHAPE_KMAX and enum_ok
        def t1(typ_):
            sig_c, sig_a = set(), set()
            for cl in classes.values():
                ts = {typ_[w] for w in cl['walls']}; (sig_c if (0 in ts or 1 in ts) else sig_a).add(cl['sig'])
            return sig_c, sig_a
        for name, tf, r, te in picks:
            lab = r['lab'] if r else uf_count(len(walls), always)[1]
            slices = {}
            for w, l_ in enumerate(lab): slices.setdefault(l_, []).append(w)
            Hf_save = poly.Hf.copy(); poly.Hf[-1] = max(poly.Hf[-1], 2 * tf)
            c = np.array([0, 0, 0, tf]); classes = {}
            for l_, ws in slices.items():
                nu = np.array([a.f() for a in A[ws[0]]]) + tf * np.array([b.f() for b in B[ws[0]]])
                classes.setdefault(class_key(nu, G4), {'walls': [], 'n': 0, 'nu': nu, 'w0': ws[0], 'newmerge': len({lab_g[w] for w in ws}) > 1})
                classes[class_key(nu, G4)]['walls'] += ws; classes[class_key(nu, G4)]['n'] += 1
            bad = 0; gaps = []; mres = []
            for cl in classes.values():
                cl['types'] = {tt: sum(1 for w in cl['walls'] if typ[w] == tt) for tt in (2, 1, 0) if any(typ[w] == tt for w in cl['walls'])}
                if not do_shapes:
                    cl.update(sig=None, V=None, E=None, F=None, sizes=None, top=None, floor=None, met_cut=None, met_act=None); gaps.append(np.inf); continue
                if te is not None:
                    w0 = cl['w0']; nue = tuple(a + te * b for a, b in zip(A[w0], B[w0]))
                    Hsave = poly.H[-1]; poly.H[-1] = R5(mpq(max(int(lam), int(2 * tf) + 1)))
                    poly.Hf[-1] = poly.H[-1].f()
                    sh = slice_shape_exact(poly, (ZERO, ZERO, ZERO, te), nue, c, cl['nu']); poly.H[-1] = Hsave
                else:
                    sh = slice_shape(poly, c, cl['nu'])
                bad += sh['euler'] != 2; gaps.append(sh['gap']); mres.append(sh['maxres'])
                if sh['euler'] != 2: print(f'      EULER FAIL class x{cl["n"]}: V {sh["V"]} E {sh["E"]} F {sh["F"]} sizes {sh["sizes"]} deg {sh["deg"]} float corners {sh.get("float_corners")}', flush=True)
                met = [f for f in sh['facets_met'] if f < n]
                cl['sig'] = (sh['V'], sh['E'], sh['F'], tuple(sorted(sh['sizes'].items())))
                sh.pop('_V', None); sh.pop('_verts', None); sh.pop('_faces', None); cl.update(V=sh['V'], E=sh['E'], F=sh['F'], sizes=sh['sizes'], top=(n + 1) in sh['facets_met'], floor=n in sh['facets_met'],
                          met_cut=sum(1 for f in met if not act[f]), met_act=sum(1 for f in met if act[f]))
                cl['types'] = {tt: sum(1 for w in cl['walls'] if typ[w] == tt) for tt in (2, 1, 0) if any(typ[w] == tt for w in cl['walls'])}
            poly.Hf = Hf_save
            if do_shapes: check(bad == 0, f'k {k} {name}: every slice class rep has Euler 2 ({len(classes)} classes, {"EXACT corners and incidences" if te is not None else "float"}, min float margin outside the band {min(gaps):.1e})')
            sig_c, sig_a = t1(typ); sep = not (sig_c & sig_a)
            # negative control: random whole-orbit cut labels with about the same number of cut cells
            nsep = 0; ndraw = 20 if ncut else 0; osz = np.bincount(orb); rmix = []
            for d in range(ndraw):
                rr = random.Random(1000 * k + d); order = list(range(len(osz))); rr.shuffle(order); cutset = set(); tot = 0
                for o in order:
                    if tot >= ncut: break
                    cutset.add(o); tot += osz[o]
                ra = np.array([orb[j] not in cutset for j in range(n)])
                rtyp = [int(ra[f]) + int(ra[g]) for f, g in walls]
                sc_, sa_ = t1(rtyp); nsep += not (sc_ & sa_)
                rmix.append(sum(1 for cl in classes.values() if cl['newmerge'] and len({rtyp[w] for w in cl['walls']}) > 1))
            nmix = sum(1 for cl in classes.values() if cl['newmerge'] and len(cl['types']) > 1)
            nmulti = sum(1 for cl in classes.values() if cl['newmerge'])                          # classes merged at THIS height (not the mirror sheets)
            print(f'  {name} (t/max b {tf / maxb.f():+.4f}): {len(slices)} slices in {len(classes)} classes; slice types carrying a cut wall {len(sig_c)}, '
                  f'only survivor walls {len(sig_a)}, shared {len(sig_c & sig_a)} -> T1 {"n/a (no shapes at this level)" if not do_shapes else "SEPARATES" if sep and ncut else "does not separate" if ncut else "n/a (no cut)"}; '
                  f'random labels separate {nsep}/{ndraw}; T2 classes merged at this height {nmulti}, mixing wall types {nmix} '
                  f'(random labels: mean {np.mean(rmix) if rmix else 0:.2f}, max {max(rmix, default=0)}, draws with none {sum(1 for x in rmix if x == 0)}/{ndraw})', flush=True)
            for cl in (sorted(classes.values(), key=lambda c_: (-c_['n'], c_['V']))[:4] if do_shapes else []):
                print(f'      class x{cl["n"]}: {cl["V"]} corners {cl["E"]} edges {cl["F"]} faces {cl["sizes"]}, walls {cl["types"]}, meets cut {cl["met_cut"]} active {cl["met_act"]} cells, floor {cl["floor"]} top {cl["top"]}', flush=True)
            lvl_slices.append(dict(name=name, t_over_maxb=tf / maxb.f(), slices=len(slices), classes=len(classes), T1_separates=bool(sep) if (ncut and do_shapes) else None,
                                   types_cut=len(sig_c), types_survivor_only=len(sig_a), types_shared=len(sig_c & sig_a), random_separate=f'{nsep}/{ndraw}',
                                   classes_mixing=nmix, multi_wall_classes=nmulti, random_mixing=rmix,
                                   class_table=[{kk: vv for kk, vv in cl.items() if kk not in ('walls', 'nu', 'w0')} for cl in classes.values()]))
        res['levels'].append(dict(k=k, cells=n, cut=ncut, walls=len(walls), fvec=poly.fvec, N_generic=Ng, generic_exact=gen, always_pairs=len(always),
                                  special=len(rows), trivial=len(rows) - len(nontriv), nontrivial=len(nontriv), inside=len(ins),
                                  max_drop=max([r['drop'] for r in nontriv], default=0), max_drop_inside=max([r['drop'] for r in ins], default=0),
                                  inside_heights=[dict(t_over_maxb=r['t'] / maxb.f(), N=r['N'], drop=r['drop'], pairs=r['pairs'], parallel_pairs=r['parallel_pairs'], exact=hkey_str(r['key'])) for r in ins],
                                  prefilter=st, slices=lvl_slices, seconds=round(time.time() - tk)))
        save()
        # NEGATIVE control on the sweep (first level only): every b_j moved by a random rational factor
        if k == KMIN:
            prog(2, 0, f'perturbed sweep k {k} (negative control)')
            rr = random.Random(7); bp = [b * R5(1 + mpq(rr.randint(-500, 500), 500000)) for b in be]
            polyp, lamp = sweep(Xe, bp)
            Xs = np.array([[x.f() for x in X] for X in Xe]); Xsp = Xs; bsp = np.array([b.f() for b in bp]); LAMp, topp = OGX_choose(Xsp, bsp); evp = OGX_events(Xsp, bsp, LAMp, 1e-9)
            lvp = np.array(sorted(set(np.round([e[0] for e in evp], 9)), reverse=True))
            cutp = np.array([0.0] + list((lvp[:-1] + lvp[1:]) / 2) + [lvp[-1] / 2]); cutp[0] = min(LAMp * 0.9, max(topp * 2, topp + 0.1))
            wsp = set()
            for l in list(cutp) + [0.0]:
                for pr in OGX_adj(Xsp, bsp, l)[0]: wsp.add(tuple(sorted(pr)))
            wallsp = sorted(wsp)
            bsetp = set(bp); trivp = lambda t: t.iszero() or (-t) in bsetp
            _, _, alp, Ngp, rowsp, stp = scan(polyp, wallsp, C0, U4, lambda tf, key: tf > 0, trivp, 2, 'perturbed sweep', [maxb * R5(mpq(1, 3)), maxb])
            ntp = [r for r in rowsp if not r['trivial']]
            mdp = max([r['drop'] for r in ntp], default=0)
            check(not alp and mdp <= 3 and Ngp == len(wallsp), f'perturbed sweep k {k}: walls {len(wallsp)}, generic N {Ngp} (want = walls: no mirror sheets), always pairs {len(alp)}, '
                  f'non-trivial special heights {len(ntp)} with largest drop {mdp} (want <= 3: no orbit merges); trivial {len(rowsp) - len(ntp)}')
            res['controls']['perturbed_sweep'] = dict(k=k, walls=len(wallsp), N_generic=Ngp, always=len(alp), nontrivial=len(ntp), max_drop=mdp, trivial=len(rowsp) - len(ntp))
            save()
        prog(stage, 1, f'k {k} done')
    We = feet
res['fails'] = fails; save()
print(f'done in {time.time() - t0:.0f} s')
print('FINAL ok' if not fails else f'FINAL FAIL: {len(fails)} checks failed: ' + ' | '.join(fails[:5]))
