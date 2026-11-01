# Star Cores book (2026-11-01): Kuwagata's star (Kagemusha D86 with DICTO's sloping-base notch pieces, t = 2, three steps of the valley
# rule), with every cut-back height made EXACT. The float run of kagemusha_variants.py (study 2026-11-01-star-cores-d, unchanged except for
# recording) finds each height by bisection. Every piece is a tetrahedron, and a moving spike first touches another piece when four of
# their corners become coplanar: det = 0, linear in the height s for one moving spike, quadratic when two spikes are shortened together.
# For each cut spike the event root nearest the bisection value is taken, checked to lie within 1e-6 of it and to be the contact (free
# just below, clashing just above), and solved exactly with sympy over Q(sqrt5) (with a square root where the equation is quadratic).
# Then: are the step-three heights exactly 1 (the star stops exactly)? The final surface exactly: distinct corners, faces after exact
# coplanar merging, Euler; and the counts against every solid of DICTO Solids v7 (similar solids have equal corner and face counts).
# Usage: kuwagata_exact.py <dataset-v7 dir> <star-cores.json> <star-cores-d scripts dir> <out json>
import sys, os, json, itertools, math, types, numpy as np, sympy as sp
DS, SCJ, DSCR, OUT = sys.argv[1:5]
sys.argv = [sys.argv[0], DS, SCJ, '/tmp']; sys.path.insert(0, DSCR); sys.path.append(os.path.expanduser('~/kres-tmp/star-cores/scripts'))
src = open(os.path.join(DSCR, 'kagemusha_variants.py')).read()
p1 = "        for _ in range(12):\n            Qs = [spike(i, s) for i, s in enumerate(S2)]"
p2 = "        V2 = list(V); F2 = []; B2 = []; added = 0.0"
assert src.count(p1) == 1 and src.count(p2) == 1
src = src.replace(p1, "        S_old = list(S2)\n" + p1).replace(p2, "        REC.append(dict(k=k, V=V.copy(), F=[list(f) for f in F], base=base, S=list(S2), S_old=S_old, old=list(old), below=list(below)))\n" + p2)
src = src.replace("if __name__ == '__main__':", "if False:")
KV = types.ModuleType('kv'); KV.__dict__['REC'] = []; KV.__dict__['__file__'] = os.path.join(DSCR, 'kagemusha_variants.py')
exec(compile(src, 'kagemusha_variants_rec', 'exec'), KV.__dict__)
os.chdir(DS)
res = KV.run('sloping', 2.0); REC = KV.REC; t = 2
print('float run: step volumes', [round(s['volume_over_last'], 12) for s in res['steps']], flush=True)
# ---------------- exact points ----------------
r5 = sp.sqrt(5)
d = json.load(open(os.path.join(DS, 'solids', 'dicto-shadow-17.json')))
X0 = [sp.Matrix([sp.nsimplify(sp.sympify(x, locals={'sqrt': sp.sqrt})) for x in v['exact']]) for v in d['vertices']]
cen = sum(X0, sp.zeros(3, 1)) / len(X0); X0 = [sp.Matrix([sp.expand(c) for c in (x - cen)]) for x in X0]
F0 = d['faces']
EX = []   # (float point, exact point)
def addp(P):
    P = sp.Matrix([sp.radsimp(sp.expand(c)) for c in P]); fp = np.array([float(c) for c in P])
    for q, Q_ in EX:
        if np.linalg.norm(q - fp) < 1e-12: return Q_      # the same point reached twice (X from both notch faces)
    EX.append((fp, P)); return P
for x in X0: addp(x)
addp(sp.zeros(3, 1))
def normal(f): a, b, c = (X0[i] for i in f); return (b - a).cross(c - a)
for f in F0:      # full step-one tips t x the foot of O on each face plane (cap spikes, and the notch faces' tips used for X)
    N = normal(f); addp(t * (X0[f[0]].dot(N) / N.dot(N)) * N)
# X of every notch (sloping bases): on the line c -> T, in the plane through the notch edge and O
E = {}
for i, f in enumerate(F0):
    for k in range(3): E.setdefault(tuple(sorted((f[k], f[(k + 1) % 3]))), []).append(i)
for e, faces in E.items():
    i, j = faces; a, b = X0[e[0]], X0[e[1]]
    Ni, Nj = normal(F0[i]), normal(F0[j])
    k = F0[i].index(e[0]); runs = F0[i][(k + 1) % 3] == e[1]
    if Ni.cross(Nj).dot((b - a) if runs else (a - b)) >= 0: continue     # convex edge
    m = (b - a).cross(-a)
    for ff, N in ((F0[i], Ni), (F0[j], Nj)):
        cc = X0[[v for v in ff if v not in e][0]]; T = t * (X0[ff[0]].dot(N) / N.dot(N)) * N
        s_ = cc.dot(m) / (cc - T).dot(m); addp(cc + s_ * (T - cc))
def ex(p, tol=1e-5):
    # float corners built on bisection heights sit up to ~1e-7 from their exact values; the nearest exact point must be unique
    dd = np.array([np.linalg.norm(q - p) for q, _ in EX]); o = np.argsort(dd); i = int(o[0])
    if dd[i] > tol or (len(dd) > 1 and dd[o[1]] < 1e-3): raise ValueError(f'no unique exact point for {p} (nearest {dd[i]:.2e}, next {dd[o[1]]:.2e})')
    return EX[i][1]
def det4(P): return (P[1] - P[0]).dot((P[2] - P[0]).cross(P[3] - P[0]))
def fdet(P): P = [np.asarray(x, float) for x in P]; return float(np.dot(P[1] - P[0], np.cross(P[2] - P[0], P[3] - P[0])))
from star_valley import clash, geo
from star_core import axes
def sov(Q, P, eps=1e-12):
    """interiors of two convex pieces meet (no separating axis, touching counts as apart)"""
    try: A1, A2 = axes(Q), axes(P)
    except Exception: return False
    for ax in A1[0] + A2[0] + [np.cross(u, v) for u in A1[1] for v in A2[1]]:
        nn = np.linalg.norm(ax)
        if nn < 1e-12: continue
        pa, pb = Q @ (ax / nn), P @ (ax / nn)
        if pa.max() <= pb.min() + eps or pb.max() <= pa.min() + eps: return False
    return True
out = dict(steps=[])
for rec in REC:
    k, V, F, base, S, S_old, old = rec['k'], rec['V'], rec['F'], rec['base'], rec['S'], rec['S_old'], rec['old']
    cut = [i for i, s in enumerate(S) if 1 + 1e-9 < s < t - 1e-9]
    info = dict(step=k, spikes=len(S), full=sum(s >= t - 1e-9 for s in S), flat=sum(s <= 1 + 1e-9 for s in S), cut=len(cut), heights=[])
    exA, exD = {}, {}
    def exact_base(i):
        if i not in exA:
            f, A, foot = base[i]
            # A = mean of the far points of the piece beneath (as in the float code), mapped to exact points; foot = A projected on the face
            P = rec_below[i]; h = (P - V[f[0]]) @ (np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]) / np.linalg.norm(np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]])))
            far = [ex(q) for q in P[np.abs(h - h.min()) < 1e-9]]; Ae = sum(far, sp.zeros(3, 1)) / len(far)
            a, b, c = (ex(V[v]) for v in f); N = (b - a).cross(c - a); fe = Ae - ((Ae - a).dot(N) / N.dot(N)) * N
            assert np.allclose([float(x) for x in Ae], A, atol=1e-5) and np.allclose([float(x) for x in fe], foot, atol=1e-5)
            exA[i], exD[i] = Ae, fe - Ae
        return exA[i], exD[i]
    rec_below = rec['below']
    for i in cut:
        f, A, foot = base[i]; s0 = S[i]; Dv = foot - A
        tri = [V[v] for v in f]
        def apex(s, A=A, Dv=Dv): return A + s * Dv
        cands = []
        # obstacles: old pieces (fixed tetrahedra) near the spike; partner spikes of the same step (moving, same s)
        def Q(s): return tri + [apex(s)]
        sH = s0 + 1e-6; QH = np.vstack(tri + [apex(sH)])
        for P in old:
            if np.linalg.norm(P.mean(0) - apex(s0)) > 3: continue
            if not sov(QH, P): continue          # only pieces that the spike enters just above its height can stop it
            for m in range(1, 4):        # m corners of the spike (always incl. the apex), 4 - m of the obstacle
                for qi in itertools.combinations(range(3), m - 1):
                    for pj in itertools.combinations(range(len(P)), 4 - m):
                        g = lambda s: fdet([tri[a] for a in qi] + [apex(s)] + [P[b] for b in pj])
                        g0, g1 = g(0.0), g(1.0); c1 = g1 - g0
                        if abs(c1) < 1e-14: continue
                        r = -g0 / c1
                        if 1 - 1e-9 <= r <= t + 1e-9: cands.append((abs(r - s0), r, 'old', qi, pj, P))
        partners = [j for j in range(len(S)) if j != i and abs(S[j] - s0) < 1e-9 and np.linalg.norm(apex(s0) - (base[j][1] + s0 * (base[j][2] - base[j][1]))) < 3]
        for j in partners:
            fj, Aj, footj = base[j]; trj = [V[v] for v in fj]; apj = lambda s, Aj=Aj, Dj=footj - Aj: Aj + s * Dj
            if not sov(QH, np.vstack(trj + [apj(sH)])): continue
            for m in range(1, 4):
                for qi in itertools.combinations(range(3), m - 1):
                    for n_ in range(1, 5 - m):
                        if m + n_ != 4: continue
                        for pj in itertools.combinations(range(3), n_ - 1):
                            g = lambda s: fdet([tri[a] for a in qi] + [apex(s)] + [trj[b] for b in pj] + [apj(s)])
                            c0, cA, cB = g(0.0), g(1.0), g(-1.0); a2 = (cA + cB) / 2 - c0; a1 = (cA - cB) / 2
                            for r in (np.roots([a2, a1, c0]) if abs(a2) > 1e-14 else ([-c0 / a1] if abs(a1) > 1e-14 else [])):
                                if abs(np.imag(r)) < 1e-12 and 1 - 1e-9 <= np.real(r) <= t + 1e-9:
                                    cands.append((abs(np.real(r) - s0), float(np.real(r)), 'pair', qi, pj, j))
        cands.sort(key=lambda c: c[0])
        best = cands[0] if cands else None
        row = dict(spike=i, float_s=s0, float_s_old=S_old[i], kind=None)
        if best is None or best[0] > 1e-5:
            row['status'] = 'no event within 1e-5' + ('' if best is None else f' (nearest {best[0]:.2e})'); info['heights'].append(row); continue
        _, r, kind, qi, pj, other = best
        Ae, De = exact_base(i); s = sp.Symbol('s'); ap = Ae + s * De; trx = [ex(V[v]) for v in f]
        if kind == 'old':
            pts = [trx[a] for a in qi] + [ap] + [ex(other[b]) for b in pj]
        else:
            Aj, Dj = exact_base(other); trjx = [ex(V[v]) for v in base[other][0]]
            pts = [trx[a] for a in qi] + [ap] + [trjx[b] for b in pj] + [Aj + s * Dj]
        poly = sp.Poly(sp.expand(det4(pts)), s)
        roots = [sp.radsimp(x) for x in sp.solve(poly.as_expr(), s)]
        rx = min(roots, key=lambda x: abs(complex(sp.N(x, 30)) - r))
        val = float(sp.N(rx, 30))
        row.update(kind=kind, degree=poly.degree(), exact=str(rx), exact_decimal=val, diff_from_float=val - s0)
        # contact check: free just below the exact root, clash just above (float clash, its tolerance 1e-7)
        def piece(sv): return np.vstack(tri + [apex(sv)])
        if kind == 'old':
            lo_ok = val - 1e-6 < 1 or not sov(piece(val - 1e-6), other); hi_ok = sov(piece(val + 1e-6), other)
        else:
            fj, Aj_, footj = base[other]; pj_ = lambda sv: np.vstack([V[v] for v in fj] + [Aj_ + sv * (footj - Aj_)])
            lo_ok = val - 1e-6 < 1 or not sov(piece(val - 1e-6), pj_(val - 1e-6)); hi_ok = sov(piece(val + 1e-6), pj_(val + 1e-6))
        row.update(free_below=bool(lo_ok), clash_above=bool(hi_ok), is_one=bool(sp.simplify(rx - 1) == 0))
        info['heights'].append(row)
        if not row['is_one']: addp(Ae + rx * De)
        print(k, i, kind, row['degree'], row['exact'][:80], f"{row['diff_from_float']:.2e}", lo_ok, hi_ok, row['is_one'], flush=True)
    kinds = {}
    for h in info['heights']: kinds.setdefault(h.get('exact', h.get('status')), []).append(h['spike'])
    info['distinct_heights'] = {k_: len(v) for k_, v in kinds.items()}
    out['steps'].append(info); json.dump(out, open(OUT, 'w'), indent=1, default=str)
# ---------------- the final surface ----------------
# Coplanarity of neighbouring triangles: the determinant evaluated from the exact corners at 60 digits (a nonzero value is certain once it
# exceeds the evaluation error; a value below 1e-40 is then tried for an exact zero with sympy). Similarity with the solids of v7: similar
# solids have equal corner counts and, after scaling to the same largest corner distance from the corner centroid, equal sorted lists
# of corner distances; a difference far above the 60-digit error proves the shapes are not similar.
import mpmath
mpmath.mp.dps = 60
last = REC[-1]; flat_exact = {h['spike'] for h in out['steps'][-1]['heights'] if h.get('is_one')}
V = list(last['V']); F = []
for i, (f, A, foot) in enumerate(last['base']):
    s_ = last['S'][i]
    if s_ <= 1 + 1e-9 or i in flat_exact: F.append(list(f)); continue
    ti = len(V); V.append(A + s_ * (foot - A))
    for a_ in range(len(f)): F.append([f[a_], f[(a_ + 1) % len(f)], ti])
V = np.array(V); out['flat_exact_step3'] = len(flat_exact)
used = sorted({v for f in F for v in f}); out['final_float'] = dict(corners=len(used), triangles=len(F))
try:
    VX = {v: ex(V[v]) for v in used}
    VM = {v: [mpmath.mpf(str(sp.N(c, 70))) for c in VX[v]] for v in used}
    def mdet(a, b, c, d_):
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]; w = [d_[i] - a[i] for i in range(3)]
        return u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0])
    Ed = {}
    for fi, f in enumerate(F):
        for a_ in range(len(f)): Ed.setdefault(tuple(sorted((f[a_], f[(a_ + 1) % len(f)]))), []).append(fi)
    parent = list(range(len(F)))
    def root(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    small, proved = [], 0
    for e, (fa, fb) in Ed.items():
        o = [v for v in F[fb] if v not in e][0]
        dv = abs(mdet(*(VM[v] for v in F[fa]), VM[o]))
        if dv < mpmath.mpf('1e-40'):
            small.append(float(dv)); parent[root(fa)] = root(fb)
            try:
                if sp.simplify(sp.expand(det4([VX[F[fa][0]], VX[F[fa][1]], VX[F[fa][2]], VX[o]]))) == 0: proved += 1
            except Exception: pass
    groups = {}
    for fi in range(len(F)): groups.setdefault(root(fi), []).append(fi)
    sides = {}
    for g in groups.values():
        ee = {}
        for fi in g:
            for a_ in range(3): k_ = tuple(sorted((F[fi][a_], F[fi][(a_ + 1) % 3]))); ee[k_] = ee.get(k_, 0) + 1
        nb = sum(1 for c in ee.values() if c == 1); sides[nb] = sides.get(nb, 0) + 1
    nE = len(Ed) - sum(len(g) - 1 for g in groups.values())
    out['final'] = dict(corners=len(used), edges=nE, faces=len(groups), faces_by_sides=sides, euler=len(used) - nE + len(groups),
                        coplanar_pairs=len(small), coplanar_proved_exactly=proved)
    # corner distances from the corner centroid, scaled to the largest
    cm = [sum(VM[v][i] for v in used) / len(used) for i in range(3)]
    rr = sorted(mpmath.sqrt(sum((VM[v][i] - cm[i]) ** 2 for i in range(3))) for v in used); rr = [x / rr[-1] for x in rr]
    out['final']['distance_kinds'] = len({mpmath.nstr(x, 30) for x in rr})
    cmp_ = []
    for fn in sorted(os.listdir(os.path.join(DS, 'solids'))):
        if not fn.endswith('.json'): continue
        m = json.load(open(os.path.join(DS, 'solids', fn)))
        if len(m['vertices']) != len(used): continue
        W = [[mpmath.mpf(x) for x in v['decimal']] for v in m['vertices']]
        c2 = [sum(w[i] for w in W) / len(W) for i in range(3)]
        q = sorted(mpmath.sqrt(sum((w[i] - c2[i]) ** 2 for i in range(3))) for w in W); q = [x / q[-1] for x in q]
        cmp_.append(dict(file=fn, faces=len(m['faces']), max_distance_difference=float(max(abs(a_ - b_) for a_, b_ in zip(rr, q)))))
    out['v7_same_corner_count'] = cmp_
except Exception as e:
    import traceback; out['final_error'] = traceback.format_exc()[-800:]
json.dump(out, open(OUT, 'w'), indent=1, default=str); print(json.dumps({k_: v for k_, v in out.items() if k_ != 'steps'}, default=str)); print('done')
