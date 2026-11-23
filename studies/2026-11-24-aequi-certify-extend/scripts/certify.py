# Rigorous certification of the Aequi (study 2026-11-24-aequi-certify-extend).
# For each die: (1) exact face normals in Q(sqrt5) (arb balls); (2) the combinatorial type at the 60-digit depths;
# (3) the type is constant over a box X (every corner, the meet of three planes, lies strictly inside every other
# half-space over X; corner coordinates are linear in the depths, so this test is sharp); (4) Krawczyk's test
# K(X) = x~ - C F(x~) + (I - C J(X)) (X - x~) inside the interior of X, with F the fairness equations
# "solid angle of one face of orbit k = 4 pi / N" (k = 2..m, first orbit at depth 1) and J(X) an arb enclosure of
# the Jacobian over X by forward differentiation. Success proves: exactly one fair depth vector in X.
# Solid angles: Van Oosterom and Strackee's triangle formula (1983), on a fan from one corner of the face.
# Ball arithmetic: python-flint (arb, Johansson).
# usage: certify.py OUT.jsonl NPROC [only_sid_list]
import json, sys, os, glob, itertools, time, numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from groups import DIRS, DFAM, OH, IH
from scipy.spatial import HalfspaceIntersection
from flint import arb, arb_mat, fmpq, ctx
ST = os.path.normpath(os.path.join(HERE, '..', '..'))
PREC = 320

# ---------- exact directions: each coordinate a + b*phi with a, b rational ----------
PH = None
def pats():
    one, ph, iph, z = (1, 0), (0, 1), (-1, 1), (0, 0)     # 1, phi, 1/phi = phi - 1, 0
    P = [(one, z, z), (one, one, one), (one, one, z), (z, ph, one), (z, iph, ph), (one, ph, iph),
         (z, one, ph), (z, ph, iph), (ph, one, iph)]
    out = []
    for t in P:
        for s in itertools.product((1, -1), repeat=3):
            q = [(s[i] * t[i][0], s[i] * t[i][1]) for i in range(3)]
            for k in range(3): out.append(q[-k:] + q[:-k] if k else q)
    return out
def fval(c): return c[0] + c[1] * (1 + 5 ** .5) / 2
EXACT = []
for v in DIRS:
    for q in pats():
        w = np.array([fval(c) for c in q]); w = w / np.linalg.norm(w)
        if np.abs(w - v).max() < 1e-9: EXACT.append(q); break
assert len(EXACT) == len(DIRS)
def arbdir(i):
    ph = (1 + arb(5).sqrt()) / 2
    q = [arb(c[0]) + arb(c[1]) * ph for c in EXACT[i]]
    n = (q[0] * q[0] + q[1] * q[1] + q[2] * q[2]).sqrt()
    return [c / n for c in q]

# ---------- forward differentiation over arb ----------
class D:
    __slots__ = ('v', 'g')
    def __init__(s, v, g): s.v = v; s.g = g
    def __add__(s, o):
        if isinstance(o, D): return D(s.v + o.v, [a + b for a, b in zip(s.g, o.g)])
        return D(s.v + o, s.g)
    __radd__ = __add__
    def __sub__(s, o):
        if isinstance(o, D): return D(s.v - o.v, [a - b for a, b in zip(s.g, o.g)])
        return D(s.v - o, s.g)
    def __neg__(s): return D(-s.v, [-a for a in s.g])
    def __mul__(s, o):
        if isinstance(o, D): return D(s.v * o.v, [s.v * b + o.v * a for a, b in zip(s.g, o.g)])
        return D(s.v * o, [a * o for a in s.g])
    __rmul__ = __mul__
def dsqrt(a): v = a.v.sqrt(); h = 1 / (2 * v); return D(v, [x * h for x in a.g])
def datan2(y, x):
    v = arb.atan2(y.v, x.v); den = x.v * x.v + y.v * y.v
    return D(v, [(x.v * gy - y.v * gx) / den for gy, gx in zip(y.g, x.g)])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def tri(a, b, c, sg):
    """2 atan2(|a.(b x c)|, |a||b||c| + (a.b)|c| + (a.c)|b| + (b.c)|a|): Van Oosterom-Strackee"""
    num = dot(a, cross(b, c)) * sg
    la, lb, lc = dsqrt(dot(a, a)), dsqrt(dot(b, b)), dsqrt(dot(c, c))
    den = la * lb * lc + dot(a, b) * lc + dot(a, c) * lb + dot(b, c) * la
    return datan2(num, den) * 2, num, den

# ---------- one die ----------
def load_all():
    recs = []
    for study, keep in [('2026-11-19-aequi-complete', {'Ih', 'Oh', 'Td', 'Th', 'T', 'O', 'I'}), ('2026-11-20-aequi-two-placements', None)]:
        for f in sorted(glob.glob(os.path.join(ST, study, 'data', 'dice', '*.json'))):
            d = json.load(open(f))
            if keep is not None and d['group'] not in keep: continue
            recs.append(dict(study=study, sid=d['sid'], file=os.path.basename(f), label=d['label'], group=d['group'], m=d['m'], N=d['N'],
                             sizes=d['orbit_sizes'], idx=d['face_directions'], depths=d['depths_60_digits'], corners=d['corners']))
    return recs

def combinatorics(idx, sizes, depths):
    Nrm = DIRS[idx]; Dd = np.repeat([float(x) for x in depths], sizes)
    hs = HalfspaceIntersection(np.hstack([Nrm, -Dd[:, None]]), np.zeros(3)); V = hs.intersections
    U = []
    for v in V:
        if not any(np.abs(v - w).max() < 1e-8 for w in U): U.append(v)
    V = np.array(U)
    inc = [tuple(int(i) for i in np.where(np.abs(Nrm @ v - Dd) < 1e-8)[0]) for v in V]
    return V, inc

def symmetry_check(idx, sizes):
    """frame maps (Oh and Ih of placement A: exact matrices over Q(sqrt5)) that carry every orbit onto itself;
    check each labelled orbit is ONE orbit of that group (so equal depths per orbit make all its faces congruent)"""
    lab = np.repeat(np.arange(len(sizes)), sizes); P = DIRS[idx]
    G = []
    for g in list(OH) + list(IH):
        img = P @ g.T; dd = np.linalg.norm(img[:, None, :] - P[None, :, :], axis=2)
        j = dd.argmin(1)
        if dd.min(1).max() < 1e-9 and all(lab[j] == lab) and len(set(j)) == len(j): G.append(j)
    ok = True; cut = np.cumsum([0] + sizes)
    for k in range(len(sizes)):
        orb = {int(p[cut[k]]) for p in G}
        ok &= orb == set(range(cut[k], cut[k + 1]))
    return ok, len({tuple(p) for p in G})

class Die:
    def __init__(s, rec):
        ctx.prec = PREC
        s.rec = rec; idx = rec['idx']; sizes = rec['sizes']; s.m = m = len(sizes); s.N = N = len(idx)
        s.orb = list(np.repeat(np.arange(m), sizes)); s.cut = np.cumsum([0] + sizes)
        s.n = [arbdir(i) for i in idx]
        V, inc = combinatorics(idx, sizes, rec['depths'])
        s.Vf = V; s.inc = inc; s.degenerate = [I for I in inc if len(I) > 3]
        s.allow_flat = False
        s.xt = [arb(x).mid() for x in rec['depths'][1:]]         # exact binary midpoints of the 60-digit depths
    def setup(s):
        """corner = meet of the planes tight there (s.full); its coordinates from one triple of them (s.trip) are
        linear in the depths, v = sum_o d_o A[o]. A corner with more than three planes is STRUCTURAL when the extra
        planes pass through it for every depth vector (coefficients exactly zero; proved separately in exact
        arithmetic by structural.py) and ACCIDENTAL otherwise (the planes meet in one point only on a hyperplane of
        depth space: the type changes across every box around such a point)."""
        s.full = [I for I in s.inc]; s.trip = []; s.A = []; s.extra = []
        for I in s.full:
            for t in itertools.combinations(I, 3):
                a, b, c = s.n[t[0]], s.n[t[1]], s.n[t[2]]; dt = dot(a, cross(b, c))
                if abs(dt).lower() > 1e-3: break
            else: raise RuntimeError('no independent triple')
            i, j, k = t; bc, ca, ab = cross(b, c), cross(c, a), cross(a, b)
            A = [[arb(0)] * 3 for _ in range(s.m)]
            for f, w in ((i, bc), (j, ca), (k, ab)):
                o = s.orb[f]; A[o] = [A[o][q] + w[q] / dt for q in range(3)]
            s.trip.append(t); s.A.append(A)
            for f in I:
                if f in t: continue
                c_ = [dot(s.n[f], A[o]) for o in range(s.m)]; c_[s.orb[f]] -= 1
                s.extra.append(dict(corner=len(s.trip) - 1, plane=f, triple=t,
                                    zero=all(x.contains(0) for x in c_), coef=[x.str(12, radius=False) for x in c_]))
        s.accidental = [e for e in s.extra if not e['zero']]
        # graph: two corners sharing two planes are joined by an edge; at most two corners per pair
        s.graph_ok = True
        pair = {}
        for vi, I in enumerate(s.full):
            for p in itertools.combinations(I, 2): pair.setdefault(p, []).append(vi)
        if any(len(L) > 2 for L in pair.values()): s.graph_ok = False
        # each corner: its edges (pairs shared with one other corner) close up into one cycle through all its planes
        for vi, I in enumerate(s.full):
            ed = [p for p in itertools.combinations(I, 2) if len(pair[p]) == 2]
            if len(ed) != len(I): s.graph_ok = False; continue
            adj = {f: [] for f in I}
            for a, b in ed: adj[a].append(b); adj[b].append(a)
            if any(len(x) != 2 for x in adj.values()): s.graph_ok = False; continue
            c = [I[0], adj[I[0]][0]]
            while len(c) < len(I): c.append([w for w in adj[c[-1]] if w != c[-2]][0])
            if c[0] not in adj[c[-1]] or len(set(c)) != len(I): s.graph_ok = False
        # face cycles from the graph (not from angles)
        s.cyc = []
        for f in range(s.N):
            vs = [vi for vi, I in enumerate(s.full) if f in I]
            if len(vs) < 3: s.graph_ok = False; s.cyc.append(vs); continue
            adj = {v: [] for v in vs}
            for p, L in pair.items():
                if f in p and len(L) == 2: adj[L[0]].append(L[1]); adj[L[1]].append(L[0])
            adj = {v: sorted(set(a)) for v, a in adj.items()}
            if any(len(a) != 2 for a in adj.values()): s.graph_ok = False; s.cyc.append(vs); continue
            c = [vs[0], adj[vs[0]][0]]
            while len(c) < len(vs):
                nx = [w for w in adj[c[-1]] if w != c[-2]][0]; c.append(nx)
            if c[0] not in adj[c[-1]] or len(set(c)) != len(vs): s.graph_ok = False
            s.cyc.append(c)
        # orientation sign of each fan triangle at the midpoint (floats), checked again in arb over the box
        s.sg = []
        for f in range(s.N):
            c = s.cyc[f]; P = s.Vf_from_trip(c)
            s.sg.append([1 if np.dot(P[0], np.cross(P[i], P[i + 1])) > 0 else -1 for i in range(1, len(c) - 1)])
        s.rep = [int(s.cut[k]) for k in range(s.m)]
    def Vf_from_trip(s, c):
        out = []
        for vi in c:
            I = s.trip[vi]; Nm = DIRS[[s.rec['idx'][i] for i in I]]  # one independent triple
            dd = np.array([float(s.rec['depths'][s.orb[i]]) for i in I]); out.append(np.linalg.solve(Nm, dd))
        return out
    def depthvec(s, x):
        return [D(arb(1), [arb(0)] * (s.m - 1))] + x
    def corner(s, vi, d):
        A = s.A[vi]
        return [sum((d[o] * A[o][t] for o in range(s.m)), D(arb(0), [arb(0)] * (s.m - 1))) for t in range(3)]
    def F(s, x):
        """fairness residuals (m-1) and Jacobian rows, for depth balls x (orbits 2..m); sign check of every fan triangle"""
        d = s.depthvec(x); T = 4 * arb.pi() / s.N; res = []; signs_ok = True
        cache = {}
        for k in range(1, s.m):
            f = s.rep[k]; c = s.cyc[f]
            P = [cache.setdefault(vi, s.corner(vi, d)) for vi in c]
            om = D(arb(0), [arb(0)] * (s.m - 1))
            for i in range(1, len(c) - 1):
                t, num, den = tri(P[0], P[i], P[i + 1], s.sg[f][i - 1]); om = om + t
                # a fan triangle must be positively oriented; one that shrinks to a segment on a hyperplane where
                # the type changes may touch 0 there, which is harmless while den > 0 (atan2 analytic near (0, +))
                signs_ok &= bool(num.v > 0) or (s.allow_flat and bool(den.v > 0))
            res.append(om - T)
        return res, signs_ok
    def all_faces_mid(s):
        """every face's solid angle at the midpoint (check of the symmetry reduction)"""
        d = s.depthvec([D(v, [arb(0)] * (s.m - 1)) for v in s.xt]); T = 4 * arb.pi() / s.N; worst = 0.0
        for f in range(s.N):
            c = s.cyc[f]; P = [s.corner(vi, d) for vi in c]; om = arb(0)
            for i in range(1, len(c) - 1): om += tri(P[0], P[i], P[i + 1], s.sg[f][i - 1])[0].v
            worst = max(worst, float(abs(om - T).upper()))
        return worst
    def type_radius(s):
        """largest r with every corner strictly inside every other half-space on the box |x - x~| <= r:
        slack(x) = d_f - n_f.v(x) is linear in x, so min over the box = slack(x~) - r * sum_k |c_k|"""
        rmin = None; worst_slack = None
        for vi, I in enumerate(s.full):
            A = s.A[vi]
            for f in range(s.N):
                if f in I: continue
                nf = s.n[f]; o_f = s.orb[f]
                c = [dot(nf, A[o]) for o in range(s.m)]      # n_f . v = sum_o d_o c_o
                c[o_f] -= 1                                   # minus d_f
                sl0 = -(c[0] + sum((c[k] * s.xt[k - 1] for k in range(1, s.m)), arb(0)))
                L = sum((abs(c[k]) for k in range(1, s.m)), arb(0))
                if not sl0 > 0: return arb(0), sl0
                r = (sl0 / L) if L > 0 else arb(10) ** 9
                if rmin is None or r.lower() < rmin.lower(): rmin = r
                if worst_slack is None or sl0.lower() < worst_slack.lower(): worst_slack = sl0
        return rmin.lower(), worst_slack
    def newton(s, steps=9):
        """refine double-precision depths to working precision (Newton with the arb Jacobian at the point)"""
        ctx.prec = PREC; n = s.m - 1
        for _ in range(steps):
            X = [D(v, [arb(1) if j == i else arb(0) for j in range(n)]) for i, v in enumerate(s.xt)]
            Fx, _ = s.F(X)
            J = arb_mat([[arb(Fx[i].g[j].mid()) for j in range(n)] for i in range(n)])
            f = arb_mat([[arb(Fx[i].v.mid())] for i in range(n)])
            dx = J.solve(f)
            s.xt = [arb((s.xt[i] - dx[i, 0]).mid()) for i in range(n)]
        return max(float(Fx[i].v.abs_upper()) for i in range(n))
    def krawczyk(s, r):
        ctx.prec = PREC; ra = arb(r); n = s.m - 1
        X = [D(arb(v, ra), [arb(1) if j == i else arb(0) for j in range(n)]) for i, v in enumerate(s.xt)]
        Fx, sok = s.F(X)
        if not sok: return dict(ok=False, why='fan triangle orientation not certain on the box')
        J = arb_mat([[Fx[i].g[j] for j in range(n)] for i in range(n)])
        Xm = [D(v, [arb(0)] * n) for v in s.xt]
        F0, sok0 = s.F(Xm)
        f0 = arb_mat([[F0[i].v] for i in range(n)])
        Jm = arb_mat([[arb(J[i, j].mid()) for j in range(n)] for i in range(n)])
        try:
            Cm = Jm.inv()
        except Exception as e:
            return dict(ok=False, why='midpoint Jacobian not invertible')
        C = arb_mat([[arb(Cm[i, j].mid()) for j in range(n)] for i in range(n)])
        I = arb_mat([[arb(1) if i == j else arb(0) for j in range(n)] for i in range(n)])
        dX = arb_mat([[arb(0, ra)] for i in range(n)])
        K = -(C * f0) + (I - C * J) * dX               # K - x~
        dev = max(float(K[i, 0].abs_upper()) for i in range(n))
        ok = all(K[i, 0].abs_upper() < ra for i in range(n))
        # enclosure of the zero: x~ + K (K subset of X)
        return dict(ok=bool(ok), dev=dev, r=r, fres=max(float(f0[i, 0].abs_upper()) for i in range(n)),
                    enclosure=[(s.xt[i] + K[i, 0]).str(40, radius=True) for i in range(n)] if ok else None,
                    smin_ratio=None)

def work(rec):
    t0 = time.time(); out = dict(study=rec['study'], sid=rec['sid'], file=rec['file'], label=rec['label'], group=rec['group'], m=rec['m'], N=rec['N'])
    try:
        s = Die(rec)
        out['corners_float'] = len(s.inc); out['corners_recorded'] = rec['corners']
        sym_ok, gorder = symmetry_check(rec['idx'], rec['sizes']); out['symmetry_ok'] = bool(sym_ok); out['frame_group_order'] = gorder
        s.setup()
        out['graph_ok'] = s.graph_ok; out['simple'] = not s.degenerate
        out['n_multi_corners'] = len(s.degenerate); out['n_structural_extra'] = sum(e['zero'] for e in s.extra)
        out['structural_extra'] = [dict(planes=[int(rec['idx'][i]) for i in e['triple']] + [int(rec['idx'][e['plane']])],
                                        orbits=[int(s.orb[i]) for i in e['triple']] + [int(s.orb[e['plane']])]) for e in s.extra if e['zero']]
        if s.accidental:
            out.update(status='accidental', accidental=[dict(corner=e['corner'], planes=[int(rec['idx'][i]) for i in e['triple']] + [int(rec['idx'][e['plane']])],
                                                            coef=e['coef']) for e in s.accidental][:12], n_accidental=len(s.accidental))
            return out
        if not s.graph_ok: out['status'] = 'graph_fail'; return out
        if rec.get('refine'): out['newton_last_residual'] = s.newton()
        rt, slack = s.type_radius(); out['type_radius'] = float(rt); out['min_slack'] = float(slack.lower())
        out['all_faces_mid_residual'] = float(s.all_faces_mid())
        tight = s.krawczyk(1e-40); out['tight'] = tight
        # widest uniqueness box: radii 1e-2 .. 1e-12 below the type radius
        wide = None
        for e in range(4, 25):
            r = 10.0 ** (-e / 2)
            if r >= float(rt): continue
            kk = s.krawczyk(r)
            if kk['ok']: wide = dict(r=r, dev=kk['dev']); break
        out['wide'] = wide
        out['status'] = 'certified' if tight['ok'] and sym_ok and float(rt) > 1e-40 else 'fail'
    except Exception as e:
        import traceback; out['status'] = 'error'; out['error'] = traceback.format_exc()[-800:]
    out['sec'] = round(time.time() - t0, 2)
    return out

if __name__ == '__main__':
    outp, npr = sys.argv[1], int(sys.argv[2])
    recs = load_all() if not os.environ.get('DICE') else json.load(open(os.environ['DICE']))
    if len(sys.argv) > 3: want = set(sys.argv[3].split(',')); recs = [r for r in recs if '%s:%s' % (r['study'][:10], r['sid']) in want or str(r['sid']) in want]
    print('dice', len(recs), flush=True)
    done = set()
    if os.path.exists(outp):
        for L in open(outp):
            try: j = json.loads(L); done.add((j['study'], j['sid']))
            except Exception: pass
    recs = [r for r in recs if (r['study'], r['sid']) not in done]
    t0 = time.time(); k = 0
    with Pool(npr) as pool, open(outp, 'a') as fo:
        for r in pool.imap_unordered(work, recs):
            fo.write(json.dumps(r) + '\n'); fo.flush(); k += 1
            if k % 50 == 0: print('PROGRESS %.3f %d dice' % (k / len(recs), k), flush=True)
    print('done in', round(time.time() - t0, 1), 's', flush=True)
