# og_window.py, DICTO OG Galois-twin window test (offered 11 Nov, queued 12 Nov 2026): "swap sqrt5 -> -sqrt5 in the OG family; if the twin
# family stays bounded, it behaves like a quasicrystal window."
# The OG downward family D_0 = OG, D_{k+1} = P(D_k) (#43; the hop = antipol then polar = hull of the face foot points). Every coordinate is
# in Q(sqrt5). Here: the Galois twin sigma (sqrt5 -> -sqrt5, the perpendicular space of the 6D icosahedral picture) of every corner, level
# by level, as far as the certified machinery of og-margin (certified_orbit.py, k <= 40 on the large machine) allows on a 6 GB cage.
# WHY THE TWIN IS COMPUTABLE WITHOUT THE HUGE DENOMINATORS: the foot point of a face through members a, b, c is
#   foot = (d / n.n) n,  n = (b - a) x (c - a),  d = n.a,
# a rational expression in the coordinates; sigma is a field automorphism, so sigma(foot) is the SAME expression in sigma(a), sigma(b),
# sigma(c) (and sigma(n).sigma(n) > 0 because n != 0 and sigma is injective). The face combinatorics come from the real side (certified).
# Phases: exact Q(sqrt5) to D_K0 (twins exact: a - b sqrt5 = (a^2 - 5b^2)/(a + b sqrt5), no cancellation), then Arb balls (600 bits) on
# both sides: real balls certify the faces exactly as certified_orbit.py (that file's tools are reused unchanged); twin balls are carried
# with the conjugated group sigma(I_h) (sigma(g) is orthogonal: g g^T = I is an identity over Q(sqrt5)).
# Per level: corners, twin radius max/min (certified for the max), ratio to the previous level, twin hull (corners, faces by size,
# support on the twin 5/3/2-fold axes, R/r), number of sigma(I_h) orbits among twin hull corners, covering ratio (do the twins fill their
# hull?), nesting in the previous twin hull, and the TWIN STEP LEMMA check |sigma foot| <= min over the face's members |sigma a|.
# Validation: ball-phase levels K0+1 .. 10 must match the exact og-twin-10.json (corner counts, twin max/min to 1e-9 relative);
# real t_min must match certified-family-30 for k = 10 .. 30 (as certified_orbit.py).
# usage: python -u og_window.py <five-fold-octet dir> <K0> <KMAX> <out.json> <ck dir>
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
MARGIN = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-09-og-margin', 'scripts'))
_ARGS = list(sys.argv)
K0, KMAX, OUT = int(_ARGS[2]), int(_ARGS[3]), os.path.abspath(_ARGS[4])   # before the tools chdir
co = open(os.path.join(MARGIN, 'certified_orbit.py')).read().split('# ---------------- level K0')[0]
_g = globals(); _g['__file__'] = os.path.join(MARGIN, 'certified_orbit.py')
exec(co)                                                    # perm_maps, hull_faces, polygon_order, balls, FULLX/FULLB/FULLF, VALID, R5 tools
__file__ = os.path.abspath(_ARGS[0])
PREC = int(os.environ.get('OGW_PREC', '600'))           # 12 Nov: at 600 bits the twin balls of D_32 kept only 19 digits (near-collinear twin
flint.ctx.prec = PREC                                    # triples); the main run uses more bits. Balls built by the tools at 600 bits are rebuilt:
r5 = flint.arb(5).sqrt()
FULLB = [[[ball(x) for x in row] for row in M] for M in FULLX]
sys.path.insert(0, HERE)
from window_tools import classify, hull_fingerprint, ico_axes, covering_ratio
K0, KMAX = int(_ARGS[2]), int(_ARGS[3])
REF = {r['k']: r for r in json.load(open(os.path.join(MARGIN, '..', 'data', 'og-twin-10.json')))}
def ballT(x): return flint.arb(int(x.a.numerator)) / int(x.a.denominator) - flint.arb(int(x.b.numerator)) / int(x.b.denominator) * r5
FULLBT = [[[ballT(x) for x in row] for row in M] for M in FULLX]
FULLFT = np.array([[[float(x.a) - float(x.b) * S5 for x in row] for row in M] for M in FULLX])
AX = ico_axes(twin_frame=True)
def twinf(x):                                               # exact-safe float twin of an R5 number
    if x.b == 0: return float(x.a)
    re = float(x.a) + float(x.b) * S5
    if abs(re) < 1e-6: return float(x.a) - float(x.b) * S5
    return float(x.a * x.a - 5 * x.b * x.b) / re
def sig(x): return R5(x.a, -x.b)
t0 = time.time(); ok = True; rows = []; levels = []
# the conjugated group is a group of orthogonal matrices (control)
ok_g = all(np.allclose(M @ M.T, np.eye(3), atol=1e-12) for M in FULLFT); ok &= ok_g
print(f'sigma(I_h): 120 matrices orthogonal: {ok_g}; ball precision {PREC} bits', flush=True)

def analyse(k, Ct, corner_ids, pm, listed, extra):
    """float analysis of one level's twin corner set Ct (array), with the real point action pm (or None)."""
    global ok
    R = np.linalg.norm(Ct, axis=1); fp = hull_fingerprint(Ct, AX)
    hv = ConvexHull(Ct / np.abs(Ct).max()).vertices
    if pm is not None:
        oid = pm[:, corner_ids[hv]].min(0); orbits = len(set(oid.tolist()))
    else: orbits = None
    # symmetry control: the twin hull corners are closed under sigma(I_h)
    V = Ct[hv]; tr = cKDTree(V / R.max()); sym = max(float(tr.query((V @ FULLFT[g].T) / R.max())[0].max()) for g in range(0, 120, 7)) < 1e-9
    ok &= sym
    rho = covering_ratio(Ct)
    prevR = rows[-1]['twin_R'] if rows else None
    nested = None
    if levels:
        hp = ConvexHull(levels[-1]); nested = bool(((Ct @ hp.equations[:, :3].T + hp.equations[:, 3]).max(1) <= 1e-12 * np.abs(levels[-1]).max()).all())
    row = dict(k=k, listed=listed, corners=int(len(Ct)), twin_R=float(R.max()), twin_r_min=float(R.min()), spread=float(R.min() / R.max()),
               step_ratio=(float(R.max() / prevR) if prevR else None), twin_hull=fp, twin_hull_orbits=orbits, covering_ratio=rho,
               nested_in_previous=nested, sym_ok=bool(sym))
    row.update(extra); rows.append(row); levels.append(Ct)
    # validation against the exact 11 Nov run where both exist
    if k in REF:
        r0 = REF[k]; v = (r0['corners'] == len(Ct) and abs(r0['twin_max'] / R.max() - 1) < 1e-9 and abs(r0['twin_min'] / R.min() - 1) < 1e-9)
        row['match_og_twin_10'] = bool(v); ok &= v
    print(f"k {k:2d}: listed {listed:7d} corners {len(Ct):7d} | TWIN R {R.max():.6e} (r_min {R.min():.3e}, spread {R.min() / R.max():.3f}) "
          f"step {row['step_ratio'] if prevR is None else round(row['step_ratio'], 6)} | twin hull {fp['corners']} corners, faces {fp['faces']}, "
          f"h5:h3:h2 {fp['h'][5]:.4f}:{fp['h'][3]:.4f}:{fp['h'][2]:.4f}, R/r {fp['R_over_r']:.4f}, {orbits} orbits | cover {rho:.3f} | "
          f"nested {nested} | sym {sym}{' | og-twin-10 ' + ('MATCH' if row.get('match_og_twin_10') else 'MISMATCH') if k in REF else ''} "
          f"| {' '.join(f'{a}={b}' for a, b in extra.items())} | {time.time() - t0:.0f} s", flush=True)
    json.dump(dict(mark='DICTO OG Galois-twin window test, 2026-11-12 · DICTO · dictospheres.com', K0=K0, KMAX=KMAX, rows=rows),
              open(OUT, 'w'), indent=1, default=str)

# ---------------- exact phase D_0 .. D_K0
W = [tuple(cv(x) for x in v) for v in OG]
for k in range(K0):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wfx)
    cids = np.array(sorted(set(i for mem in F for i in mem)))
    C = [W[i] for i in cids]; Ct = np.array([[twinf(x) for x in v] for v in C])
    # exact largest twin radius^2 and the exact twin step lemma
    s2 = [sig(dot(v, v)) for v in C]; jmax = int(np.argmax([twinf(dot(v, v)) for v in C]))
    exact_max = all((s2[jmax] - s).sign() >= 0 for s in s2)
    lem = True
    for n, d, isrep in F.values():
        if not isrep: continue
        s = d / dot(n, n); foot = tuple(s * x for x in n); fs = sig(dot(foot, foot))
        mem = [w for w in W if (dot(n, w) - d).sign() == 0]          # members of this face: the points on its plane
        lem &= all((sig(dot(a, a)) - fs).sign() >= 0 for a in mem)
    ok &= exact_max and lem
    dg = max(x.digits() for v in C for x in v); R2 = s2[jmax]
    extra = dict(exact_twin_R2=(repr(R2) if R2.digits() < 120 else f'{R2.digits()} digits'), exact_max_ok=exact_max, step_lemma_exact=lem, max_digits=dg)
    pm = None
    analyse(k, Ct, cids, pm, len(W), extra)
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f} level {k}', flush=True)
    feet = {}
    for n, d, _ in F.values():
        s = d / dot(n, n); feet[tuple(s * x for x in n)] = 1
    W = list(feet)
# switch: balls for D_{K0} (both sides) and the first ball-phase step
WB0 = [tuple(ball(x) for x in v) for v in W]; WT0 = [tuple(ballT(x) for x in v) for v in W]
pointB = lambda p: WB0[p]; pointT = lambda p: WT0[p]
Wf = np.array([[float(x.mid()) for x in v] for v in WB0]); prevWf = None
for k in range(K0, KMAX + 1):
    t = time.time(); N = len(Wf)
    if np.linalg.norm(Wf, axis=1).max() > 2: fail(f'D_{k}: a point with |w| > 2')
    pm = perm_maps(Wf, f'D_{k} points')
    mems, Nf = hull_faces(Wf); F = len(mems)
    memb = np.concatenate(mems); offs = np.concatenate([[0], np.cumsum([len(m) for m in mems])[:-1]])
    wt = np.random.default_rng(k).integers(1, 2 ** 62, N, dtype=np.uint64)
    fkey = np.add.reduceat(wt[memb], offs); order_ = np.argsort(fkey); sk = fkey[order_]
    if (np.diff(sk) == 0).any(): fail(f'D_{k}: two faces with the same member key')
    fm = np.empty((120, F), np.int32)
    for g in range(120):
        kg = np.add.reduceat(wt[pm[g][memb]], offs); pos = np.searchsorted(sk, kg); pos[pos >= F] = 0
        if not (sk[pos] == kg).all(): fail(f'D_{k}: face set not closed under I_h (g {g})')
        fm[g] = order_[pos]
        if np.bincount(fm[g], minlength=F).max() != 1: fail(f'D_{k}: g {g} does not permute the faces')
    orbit_min = fm.min(0); reps = np.unique(orbit_min); R = len(reps); ridx = {int(r): i for i, r in enumerate(reps)}
    rep_of = np.array([ridx[int(x)] for x in orbit_min]); gof = -np.ones(F, np.int64)
    for g in range(120):
        img = fm[g][reps[rep_of]]; hit = (img == np.arange(F)) & (gof < 0); gof[hit] = g
    if (gof < 0).any(): fail(f'D_{k}: a face not reached from its orbit representative')
    NF = np.zeros((R, 3)); DF = np.zeros(R); planes = []; unforced = 0; polys = []; triples = []
    for i, r in enumerate(reps):
        mm = np.array(sorted(mems[r])); P = Wf[mm]
        if len(mm) == 3: best = (0, 1, 2)
        else:
            cand = itertools.combinations(range(len(mm)), 3) if len(mm) <= 24 else [(0, len(mm) // 3, 2 * len(mm) // 3)]
            best = max(cand, key=lambda c: np.linalg.norm(np.cross(P[c[1]] - P[c[0]], P[c[2]] - P[c[0]])))
        a, b, c = (pointB(int(mm[q])) for q in best)
        n = bcross(bsub(b, a), bsub(c, a)); d = bdot(n, a)
        if float(d.mid()) < 0: n = tuple(-x for x in n); d = -d
        nn = bdot(n, n)
        if not nn > 0 or not d > 0: fail(f'D_{k}: degenerate face or origin not inside (rep {r})')
        nl = nn.sqrt(); NF[i] = [float((x / nl).mid()) for x in n]; DF[i] = float((d / nl).mid()); planes.append((n, d))
        triples.append([int(mm[q]) for q in best])
        if len(mm) > 3:
            stab = [g for g in range(120) if fm[g][r] == r]
            orb = set(int(pm[g][mm[0]]) for g in stab)
            forced = orb == set(mm.tolist()) or any(len(set(frozenset((int(j), int(pm[g][j]))) for j in mm)) <= 2 for g in stab if g in REFL)
            if not forced: unforced += 1
        polys.append(mm[polygon_order(P)])
    if unforced: fail(f'D_{k}: {unforced} coplanar face orbits not forced by symmetry')
    near = [[] for _ in range(R)]; CH = max(1, int(2e7 // max(R, 1)))       # 6 GB cage: chunks of 2e7 floats
    for s0 in range(0, N, CH):
        V = Wf[s0:s0 + CH] @ NF.T - DF[None, :]
        pi, ri = np.nonzero(V > -EPS)
        for p, q in zip(pi + s0, ri): near[q].append(int(p))
    close_calls = 0
    for i, r in enumerate(reps):
        ms = set(mems[r].tolist()); extra_ = [p for p in near[i] if p not in ms]
        if not ms.issubset(set(near[i])): fail(f'D_{k}: a member of face {r} is not on its plane in float')
        n, d = planes[i]
        for p in extra_:
            close_calls += 1
            if not (bdot(n, pointB(p)) - d < 0): fail(f'D_{k}: point {p} not certified strictly inside face {r}')
    E = []
    for i, r in enumerate(reps):
        J = np.where(rep_of == i)[0]; poly = polys[i]; e = np.stack([poly, np.roll(poly, -1)], 1)
        E.append(np.sort(pm[gof[J]][:, e].reshape(-1, 2), axis=1))
    E = np.concatenate(E); _, cnt = np.unique(E, axis=0, return_counts=True)
    if not (cnt == 2).all(): fail(f'D_{k}: faces do not close up ({int((cnt != 2).sum())} bad edges)')
    tchk = ''
    if prevWf is not None and (k - 1) in VALID:
        tmax = -1.0
        for s0 in range(0, len(prevWf), CH): tmax = max(tmax, float(((prevWf[s0:s0 + CH] @ NF.T) / DF[None, :]).max()))
        okx = abs(tmax - VALID[k - 1]) < 1e-9; ok &= okx; tchk = f'real t_min(D_{k - 1}) {"MATCH" if okx else "MISMATCH"} certified-30'
    # ---- twin side of THIS level: corners = points on some certified face
    cids = np.unique(memb)
    if k == K0:
        Ct = np.array([[float(x.mid()) for x in pointT(int(p))] for p in cids])
        # certified twin radius over corner points (balls)
        Rb = max((bdot(pointT(int(p)), pointT(int(p))) for p in cids), key=lambda b: float(b.mid()))
    else:
        Ct = WTf[cids]
        corner_rep = np.unique(prep[cids])
        Rb = max((bdot(footT[j], footT[j]) for j in corner_rep), key=lambda b: float(b.mid()))
    extra = dict(twin_R_certified=Rb.sqrt().str(12, radius=True), faces=F, orbits=R, close_calls=close_calls)
    if tchk: extra['real_check'] = tchk
    # ---- twin step lemma, certified per representative face: |sigma foot|^2 <= min over its members |sigma a|^2 (no ball violation)
    footB, footT, lem_bad, relrad = [], [], 0, 0.0
    for i, r in enumerate(reps):
        n, d = planes[i]; s = d / bdot(n, n); footB.append(tuple(s * x for x in n))
        a, b, c = (pointT(j) for j in triples[i])
        nT = bcross(bsub(b, a), bsub(c, a)); nnT = bdot(nT, nT)
        if not nnT > 0: fail(f'D_{k}: twin normal not certified non-zero (rep {r})')
        dT = bdot(nT, a); fT = tuple((dT / nnT) * x for x in nT); footT.append(fT)
        f2 = bdot(fT, fT)
        for j in mems[r]:
            a2 = bdot(pointT(int(j)), pointT(int(j)))
            if f2 > a2: lem_bad += 1                         # certified violation (would refute the lemma)
        nf_ = float(f2.mid()) ** .5                           # ball radius relative to the twin foot's length (coordinates may be exactly 0)
        if nf_ > 0: relrad = max(relrad, max(float(x.rad()) for x in fT) / nf_)
    extra.update(step_lemma_violations=lem_bad, twin_rel_ball_radius=f'{relrad:.1e}')
    ok &= lem_bad == 0
    if relrad > 1e-12: fail(f'D_{k}: twin balls lost precision (relative radius {relrad:.1e})')
    analyse(k, Ct, cids, pm, N, extra)
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f} level {k} ({time.time() - t:.0f} s)', flush=True)
    if k == KMAX: break
    rads = max(float(x.rad()) for v in footB for x in v)
    if rads > 1e-60: fail(f'D_{k}: ball radii grew to {rads:.1e}')
    footf = np.array([[float(x.mid()) for x in v] for v in footB]); footTf = np.array([[float(x.mid()) for x in v] for v in footT])
    prep, pg = rep_of.astype(np.int64), gof.astype(np.int64)
    prevWf = Wf
    Wf = np.einsum('pij,pj->pi', FULLF[pg], footf[prep]); WTf = np.einsum('pij,pj->pi', FULLFT[pg], footTf[prep])
    pointB = (lambda fb, pr, gg: (lambda p: bapp(FULLB[gg[p]], fb[pr[p]])))(footB, prep, pg)
    pointT = (lambda fb, pr, gg: (lambda p: bapp(FULLBT[gg[p]], fb[pr[p]])))(footT, prep, pg)
    del pm, fm
# ---------------- summary
c = classify(levels)
st = [r['step_ratio'] for r in rows if r['step_ratio']]
tail = st[-10:]; gm = float(np.exp(np.mean(np.log(tail))))
print(f"CLASS {c['class']} | twin R first {c['R'][0]:.4e} last {c['R'][-1]:.4e} (x{c['growth_last_over_first']:.3e}) | "
      f"geometric mean step over the last {len(tail)} levels {gm:.4f} (1/phi = 0.6180, 1/phi^2 = 0.3820) | max step {max(st):.4f}", flush=True)
mono = all(r['step_ratio'] is None or r['step_ratio'] <= 1 + 1e-12 for r in rows)
print(f'twin radius non-increasing at every level: {mono}', flush=True); ok &= mono
json.dump(dict(mark='DICTO OG Galois-twin window test, 2026-11-12 · DICTO · dictospheres.com', K0=K0, KMAX=KMAX, rows=rows,
               summary=dict(cls=c['class'], R=c['R'], rho=c['rho'], gm_step_last10=gm, monotone=mono)), open(OUT, 'w'), indent=1, default=str)
print(f'done in {time.time() - t0:.0f} s')
print('FINAL ok' if ok else 'FINAL FAIL: a validation, symmetry or lemma check failed')
