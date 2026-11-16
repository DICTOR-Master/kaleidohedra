"""Off-lattice dry 2D froth built only from the established laws (foam ladder rung 4; event-logger study, 16 Nov 2026).

DICTO, 16 Nov 2026: "otherwise we build a model that matches the laws". The laws go in, the T1/T2 rate comes out; nothing is tuned
towards any published count.
  Plateau and Laplace: every film is a circular arc of curvature (p_left - p_right) / sigma, and three films meet at every vertex with
    their unit tangents summing to zero (angles of exactly 120 degrees). The froth is held in this equilibrium at every instant (the
    quasi-static limit gamma, Gamma -> infinity of Rutenberg & McCurdy's force-based model; the limit Herdtle & Aref 1992 implement).
  von Neumann 1952: every bubble's area changes exactly by dA/dt = (pi/3) sigma D (n - 6); units sigma = D = 1, initial mean area 1.
  Topology (the only moves): T1 when a film is shorter than rc (Rutenberg & McCurdy's microscopic scale); T2_n when a bubble's area
    falls below 10 rc^2 (their rule), the n-fold vertex resolved by their highest-force rule (the two adjacent films with the largest
    combined pull are drawn out on a film of length rc, repeated). A three-sided bubble whose film falls below rc is removed (T2,
    logged 'T2side'), so no two-sided bubbles arise. After every topological move the films relax to the new equilibrium under their
    own tension at fixed areas (a T1 at 120-degree vertices is a finite jump, never a small step); further T1s during that relaxation
    are logged as events of the same instant (avalanches).
Equilibrium: Newton's method on (vertex positions, bubble pressures) with the equations (force balance at every vertex, area of every
bubble = its target); one vertex and one pressure fixed (the dropped equations are identities). Arc derivatives by complex step.
Relaxation after a move: pseudo-transient continuation (implicit gradient flow of the total film length at fixed areas, ending as
Newton's method), with T1s on films that fall below rc on the way.
Start: periodic Voronoi of N0 random points (construction of the grains study's vertex2d.py), relaxed to equilibrium at its own
areas (T1s allowed), as Rutenberg & McCurdy start from a random periodic Voronoi construction.
Output (OUT): events.jsonl (exact T1 / T2 list with the areas of all bubbles involved and <A>), stats.jsonl (law checks at every
record), snap_*.npz (sides, areas, neighbour pairs), cross.jsonl (sides of each bubble as its area falls past l^2 = c rc L,
c = 0.5, 1, 2, L = sqrt(<A>)), final.json.
Usage: vfroth.py OUT N0=10000 Nend=100 rc=3.162e-4 seed=1 rec=0.01 maxwall=SECONDS law=vn|wrong test=hex
law=wrong is the deliberate negative control: dA/dt = (pi/3)(n - 6) + (2 pi/3)(A/<A> - 1) (area-conserving, not von Neumann); its
check 'geometric gas flux = imposed dA/dt' must fail."""
import sys, os, json, time, math
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from scipy.spatial import Voronoi

args = dict(a.split('=') for a in sys.argv[2:])
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
N0 = int(args.get('N0', 10000)); NEND = int(args.get('Nend', 100)); RC = float(args.get('rc', 3.162e-4))
SEED = int(args.get('seed', 1)); REC = float(args.get('rec', 0.01)); MAXWALL = float(args.get('maxwall', 1e9))
LAW = args.get('law', 'vn'); TEST = args.get('test', ''); DEBUG = int(args.get('debug', 0))
TAU0 = float(args.get('tau0', 0.5)); TAUG = float(args.get('taug', 10.0))
AT2 = 10 * RC * RC
CS = (0.5, 1.0, 2.0)
T0 = time.time()
rng = np.random.default_rng(SEED)
L = np.array([math.sqrt(N0)] * 2)
PI3 = math.pi / 3

def mi(d):
    return d - L * np.round(d / L)

# ------------------------------------------------------------------ state
class S: pass
st = S()

def alloc(nv, nf, nb):
    st.X = np.zeros((nv, 2)); st.valive = np.zeros(nv, bool); st.V = np.zeros((nv, 2))
    st.fa = np.zeros(nf, np.int64); st.fb = np.zeros(nf, np.int64); st.fl = np.zeros(nf, np.int64); st.fr = np.zeros(nf, np.int64)
    st.falive = np.zeros(nf, bool)
    st.At = np.zeros(nb); st.p = np.zeros(nb); st.balive = np.zeros(nb, bool); st.Vp = np.zeros(nb)

def snapshot():
    return {k: v.copy() for k, v in st.__dict__.items()}

def restore(s):
    for k, v in s.items(): setattr(st, k, v.copy())

def new_vertex(pos):
    free = np.nonzero(~st.valive)[0]
    if not len(free):
        n = len(st.valive); st.X = np.vstack([st.X, np.zeros((n, 2))]); st.V = np.vstack([st.V, np.zeros((n, 2))])
        st.valive = np.concatenate([st.valive, np.zeros(n, bool)]); free = np.nonzero(~st.valive)[0]
    v = int(free[0]); st.valive[v] = True; st.X[v] = np.mod(pos, L); st.V[v] = 0; return v

def new_film(a, b, l, r):
    free = np.nonzero(~st.falive)[0]
    if not len(free):
        n = len(st.falive)
        for k in ('fa', 'fb', 'fl', 'fr'): setattr(st, k, np.concatenate([getattr(st, k), np.zeros(n, np.int64)]))
        st.falive = np.concatenate([st.falive, np.zeros(n, bool)]); free = np.nonzero(~st.falive)[0]
    e = int(free[0]); st.falive[e] = True; st.fa[e], st.fb[e], st.fl[e], st.fr[e] = a, b, l, r; return e

# ------------------------------------------------------------------ film geometry
def film_local(cx, cy, kap):
    """Arc through chord c with curvature kap = p_left - p_right (> 0: bulges to the right of a->b, into the lower-pressure right
    bubble). Returns the outward unit tangents at a and at b, the segment area (added to the left bubble, taken from the right) and
    the arc length."""
    d = np.sqrt(cx * cx + cy * cy); ux, uy = cx / d, cy / d; nx, ny = -uy, ux
    s = kap * d / 2; th = np.arcsin(s); co = np.sqrt(1 - s * s)
    tax, tay = co * ux - s * nx, co * uy - s * ny
    tbx, tby = -(co * ux + s * nx), -(co * uy + s * ny)
    small = np.abs(np.real(th)) < 1e-3
    ssafe = np.where(small, 1.0, s)
    seg = np.where(small, d * d * (th / 6 + th ** 3 / 45), d * d * (2 * th - np.sin(2 * th)) / (8 * ssafe * ssafe))
    arc = np.where(small, d * (1 + s * s / 6 + 3 * s ** 4 / 40), d * th / ssafe)
    return tax, tay, tbx, tby, seg, arc

def residual(X, p, ef=None, jac=False):
    """Forces (sum of outward unit tangents) at vertices and areas of bubbles, from films ef (default: all alive films; forces and
    areas are exact for vertices and bubbles all of whose films are in ef)."""
    if ef is None: ef = np.nonzero(st.falive)[0]
    a, b, l, r = st.fa[ef], st.fb[ef], st.fl[ef], st.fr[ef]
    c = mi(X[b] - X[a]); kap = p[l] - p[r]
    if np.any(np.abs(kap * np.hypot(c[:, 0], c[:, 1]) / 2) >= 0.999): return None
    tax, tay, tbx, tby, seg, arc = film_local(c[:, 0], c[:, 1], kap)
    nv, nb = len(st.valive), len(st.balive)
    F = np.zeros((nv, 2)); A = np.zeros(nb)
    np.add.at(F[:, 0], a, tax); np.add.at(F[:, 1], a, tay); np.add.at(F[:, 0], b, tbx); np.add.at(F[:, 1], b, tby)
    ref = np.zeros((nb, 2)); ref[l] = X[a]; ref[r] = X[a]
    ra = mi(X[a] - ref[l]); rb = mi(X[b] - ref[r])
    polyl = (ra[:, 0] * c[:, 1] - ra[:, 1] * c[:, 0]) / 2
    polyr = -(rb[:, 0] * c[:, 1] - rb[:, 1] * c[:, 0]) / 2
    np.add.at(A, l, polyl + seg); np.add.at(A, r, polyr - seg)   # a film bulging into the right bubble enlarges the left one
    out = dict(F=F, A=A, ef=ef, arc=arc, kap=kap, c=c)
    if not jac: return out
    h = 1e-30; D = []
    for k in range(3):
        cx = c[:, 0] + (1j * h if k == 0 else 0); cy = c[:, 1] + (1j * h if k == 1 else 0); kk = kap + (1j * h if k == 2 else 0)
        o = film_local(cx, cy, kk)
        D.append(np.stack([np.imag(o[i]) / h for i in range(6)], 1))     # d(tax, tay, tbx, tby, seg, arc)/d(cx, cy, kappa)
    out['Dcx'], out['Dcy'], out['Dk'] = D
    return out

def build_index():
    va = np.nonzero(st.valive)[0]; ba = np.nonzero(st.balive)[0]
    vx = -np.ones(len(st.valive), np.int64); vx[va[1:]] = 2 * np.arange(len(va) - 1)
    bx = -np.ones(len(st.balive), np.int64); bx[ba[1:]] = 2 * (len(va) - 1) + np.arange(len(ba) - 1)
    return va, ba, vx, bx, 2 * (len(va) - 1) + len(ba) - 1

def assemble(res, vx, bx, n):
    ef = res['ef']; a, b, l, r = st.fa[ef], st.fb[ef], st.fl[ef], st.fr[ef]; c = res['c']
    Dcx, Dcy, Dk = res['Dcx'], res['Dcy'], res['Dk']
    rows, cols, vals = [], [], []
    def put(R, C, V):
        m = (R >= 0) & (C >= 0); rows.append(R[m]); cols.append(C[m]); vals.append(V[m])
    for (vert, o0) in ((a, 0), (b, 2)):
        for comp in range(2):
            R = np.where(vx[vert] >= 0, vx[vert] + comp, -1); o = o0 + comp
            put(R, np.where(vx[a] >= 0, vx[a], -1), -Dcx[:, o]); put(R, np.where(vx[a] >= 0, vx[a] + 1, -1), -Dcy[:, o])
            put(R, np.where(vx[b] >= 0, vx[b], -1), Dcx[:, o]); put(R, np.where(vx[b] >= 0, vx[b] + 1, -1), Dcy[:, o])
            put(R, bx[l], Dk[:, o]); put(R, bx[r], -Dk[:, o])
    for (bub, sg) in ((l, 1.0), (r, -1.0)):
        R = bx[bub]
        for vert, s_end in ((a, -1.0), (b, 1.0)):
            cx_ = np.where(vx[vert] >= 0, vx[vert], -1); cy_ = np.where(vx[vert] >= 0, vx[vert] + 1, -1)
            put(R, cx_, sg * c[:, 1] / 2 + sg * s_end * Dcx[:, 4]); put(R, cy_, -sg * c[:, 0] / 2 + sg * s_end * Dcy[:, 4])
        put(R, bx[l], sg * Dk[:, 4]); put(R, bx[r], -sg * Dk[:, 4])
    return sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))

LU_CACHE = {'key': None, 'lu': None}

def topo_key():
    ef = st.falive
    return hash(st.fa[ef].tobytes() + st.fb[ef].tobytes() + st.fl[ef].tobytes() + st.fr[ef].tobytes() + np.nonzero(ef)[0].tobytes())

def newton(X, p, At, maxit=25):
    """Newton's method on force balance + areas. The LU factorisation of the Jacobian is kept while the topology is unchanged
    (chord iterations); it is refreshed whenever a chord step does not halve the residual."""
    va, ba, vx, bx, n = build_index()
    X = X.copy(); p = p.copy(); nf = 2 * (len(va) - 1)
    scale = np.maximum(At[ba[1:]], 0.01 * At[ba].mean())   # relative 1e-11, absolute floor 1e-13 <A> (rounding)
    key = topo_key(); lu = LU_CACHE['lu'] if LU_CACHE['key'] == key else None; fresh = False; chord = 0
    def rv(Xa, pa):
        r = residual(Xa, pa)
        if r is None: return None, None
        R = np.concatenate([r['F'][va[1:]].ravel(), (r['A'] - At)[ba[1:]]])
        return R, math.sqrt((R[:nf] ** 2).sum() + ((R[nf:] / scale) ** 2).sum())
    R, r0 = rv(X, p)
    if R is None: return None, None, 0, 'arc'
    for it in range(maxit + 1):
        ferr = np.abs(R[:nf]).max(); aerr = (np.abs(R[nf:]) / scale).max()
        if not (np.isfinite(ferr) and np.isfinite(aerr)): return None, None, it, 'nan'
        if ferr < 1e-11 and aerr < 1e-11: return X, p, it, "ok"
        if it == maxit: break
        if lu is not None and not fresh and chord >= 4: lu = None          # stale: four chord steps without converging
        if lu is None:
            chord = 0
            try:
                lu = splu(assemble(residual(X, p, jac=True), vx, bx, n), permc_spec='COLAMD')
            except Exception: return None, None, it, 'singular'
            LU_CACHE['key'] = key; LU_CACHE['lu'] = lu; fresh = True; counts['lu'] = counts.get('lu', 0) + 1
        dz = lu.solve(-R); lam = 1.0; done = False
        for _ in range(6 if fresh else 1):
            X2 = X.copy(); p2 = p.copy()
            X2[va[1:]] = np.mod(X[va[1:]] + lam * dz[:nf].reshape(-1, 2), L); p2[ba[1:]] += lam * dz[nf:]
            R2, r2 = rv(X2, p2)
            if R2 is not None and np.isfinite(r2) and (r2 < r0 if fresh else r2 < 0.5 * r0): done = True; break
            lam /= 2
        if not done:
            if fresh: return None, None, it, 'linesearch'
            lu = None; continue
        X, p, R, r0 = X2, p2, R2, r2
        fresh = False; chord += 1
    return None, None, maxit, 'maxit'

# ------------------------------------------------------------------ topology helpers
def films_of_bubble(g):
    return np.nonzero(st.falive & ((st.fl == g) | (st.fr == g)))[0]

def films_at(v):
    return np.nonzero(st.falive & ((st.fa == v) | (st.fb == v)))[0]

def nsides():
    ef = st.falive
    return np.bincount(np.concatenate([st.fl[ef], st.fr[ef]]), minlength=len(st.balive))

def other_end(e, v):
    return int(st.fb[e] if st.fa[e] == v else st.fa[e])

def set_end(e, old, new):
    if st.fa[e] == old: st.fa[e] = new
    else: st.fb[e] = new

anomalies = {'T1 R==S': 0, 'T2 shared outer': 0, 'T2 n>5': 0, 'relax fail': 0}
counts = {'T1': 0, 'T2': 0, 'T2side': 0, 'T1init': 0, 'T2init': 0}
t = 0.0
RECORDING = False

def T1(e):
    """Swap across film e (a->c, left P, right Q): P and Q lose contact, R and S gain it. New film of length 2 rc along the old
    film's normal. Returns (P, Q, R, S) or None."""
    a, c = int(st.fa[e]), int(st.fb[e]); Pg, Qg = int(st.fl[e]), int(st.fr[e])
    ia = [x for x in films_at(a) if x != e]; ic = [x for x in films_at(c) if x != e]
    if len(ia) != 2 or len(ic) != 2: return None
    def pick(lst, g): return [x for x in lst if st.fl[x] == g or st.fr[x] == g]
    baP, baQ, bcP, bcQ = pick(ia, Pg), pick(ia, Qg), pick(ic, Pg), pick(ic, Qg)
    if not (len(baP) == len(baQ) == len(bcP) == len(bcQ) == 1): return None
    baP, baQ, bcP, bcQ = baP[0], baQ[0], bcP[0], bcQ[0]
    R = int(st.fl[baP] if st.fr[baP] == Pg else st.fr[baP]); Sg = int(st.fl[bcP] if st.fr[bcP] == Pg else st.fr[bcP])
    if R == Sg or R in (Pg, Qg) or Sg in (Pg, Qg): anomalies['T1 R==S'] += 1; return None
    pa = st.X[a]; d = mi(st.X[c] - pa); m = pa + d / 2; nd = np.hypot(*d)
    u = d / nd if nd > 0 else np.array([1.0, 0.0]); n = np.array([-u[1], u[0]])
    st.X[a] = np.mod(m + n * RC, L); st.X[c] = np.mod(m - n * RC, L); st.V[a] = 0; st.V[c] = 0
    set_end(bcP, c, a); set_end(baQ, a, c)
    st.fa[e], st.fb[e], st.fl[e], st.fr[e] = a, c, Sg, R
    return (Pg, Qg, R, Sg)

def T2(G):
    """Remove bubble G (n = 3, 4 or 5 sides): its vertices merge at their centroid and the n-fold vertex is resolved by the
    highest-force rule. Its remaining target area goes to its neighbours. Returns (n, neighbours, new vertices) or None."""
    fs = films_of_bubble(G); n = len(fs)
    if n > 5: anomalies['T2 n>5'] += 1; return None
    verts = sorted({int(x) for x in np.concatenate([st.fa[fs], st.fb[fs]])})
    if len(verts) != n: anomalies['T2 shared outer'] += 1; return None
    outer = {}
    for v in verts:
        o = [x for x in films_at(v) if x not in fs]
        if len(o) != 1: anomalies['T2 shared outer'] += 1; return None
        outer[v] = int(o[0])
    if len(set(outer.values())) != n or any(other_end(outer[v], v) in verts for v in verts):
        anomalies['T2 shared outer'] += 1; return None
    nbrs = [int(st.fl[x] if st.fr[x] == G else st.fr[x]) for x in fs]
    ref = st.X[verts[0]]; cen = ref + np.mean([mi(st.X[v] - ref) for v in verts], axis=0)
    ang = []
    for v in verts:
        dv = mi(st.X[other_end(outer[v], v)] - cen); ang.append(math.atan2(dv[1], dv[0]))
    order = [verts[i] for i in np.argsort(ang)]
    O = [outer[v] for v in order]
    tdir = []
    for k in range(n):
        dv = mi(st.X[other_end(O[k], order[k])] - cen); tdir.append(dv / np.hypot(*dv))
    def wedge(e1, e2):
        s = {int(st.fl[e1]), int(st.fr[e1])} & {int(st.fl[e2]), int(st.fr[e2])}; s.discard(G)
        return s.pop() if len(s) == 1 else None
    B = [wedge(O[k], O[(k + 1) % n]) for k in range(n)]
    if None in B: anomalies['T2 shared outer'] += 1; return None
    share = st.At[G] / n
    st.falive[fs] = False; st.valive[verts] = False; st.balive[G] = False
    for nb in nbrs: st.At[nb] += share
    st.At[G] = 0; st.p[G] = 0
    c0 = new_vertex(cen); newv = [c0]
    for k in range(n): set_end(O[k], order[k], c0)
    # resolve: ring of (film, its unit direction) around c0 with wedges B between consecutive entries
    ring = list(range(n)); dirs = list(tdir); films = list(O); wed = list(B)
    while len(ring) > 3:
        m = len(ring)
        k = max(range(m), key=lambda j: np.hypot(*(dirs[j] + dirs[(j + 1) % m])))
        k2 = (k + 1) % m
        f = dirs[k] + dirs[k2]; f = f / max(np.hypot(*f), 1e-300)
        w = new_vertex(cen + RC * f); newv.append(w)
        set_end(films[k], c0, w); set_end(films[k2], c0, w)
        nf_ = new_film(c0, w, wed[k2], wed[(k - 1) % m])          # left of c0->w: wedge after the pair; right: wedge before it
        # the pair is replaced in the ring by the new film (direction f), wedge between them disappears
        newring_d, newring_f, newring_w = [], [], []
        for j in range(m):
            if j == k:
                newring_d.append(f); newring_f.append(nf_); newring_w.append(wed[k2])
            elif j == k2: continue
            else:
                newring_d.append(dirs[j]); newring_f.append(films[j]); newring_w.append(wed[j])
        dirs, films, wed = newring_d, newring_f, newring_w; ring = list(range(len(dirs)))
    return n, nbrs, newv

# ------------------------------------------------------------------ relaxation after a topological move
def fail(msg):
    anomalies['relax fail'] += 1
    if DEBUG: print('FAIL', msg, flush=True)
    return None

def topo_moves(At, Ef=None):
    """T1 on every film shorter than rc (a three-sided bubble on it is removed instead: T2side). Returns events (None on failure)."""
    evs = []
    ef = np.nonzero(st.falive)[0] if Ef is None else Ef[st.falive[Ef]]
    cc = mi(st.X[st.fb[ef]] - st.X[st.fa[ef]]); dl = np.hypot(cc[:, 0], cc[:, 1])
    for e in ef[np.argsort(dl)][: int((dl < RC).sum())]:
        if not st.falive[e] or np.hypot(*mi(st.X[st.fb[e]] - st.X[st.fa[e]])) >= RC: continue
        ns = nsides(); P, Q = int(st.fl[e]), int(st.fr[e])
        if ns[P] <= 3 or ns[Q] <= 3:
            G2 = P if ns[P] <= 3 else Q; Ag = float(At[G2]); st.At[:] = At
            o2 = T2(G2)
            if o2 is None: return fail('T2side')
            At[:] = st.At; evs.append(('T2side', G2, o2[0], Ag))
        else:
            q = T1(e)
            if q is None: return fail('T1')
            evs.append(('T1', q, [float(At[x]) for x in q]))
    return evs

def ptc(seed=None, maxit=400):
    """After a topological move: pseudo-transient continuation, i.e. implicit gradient flow X' - X = tau F(X') at fixed areas
    (each iteration solves (J - diag(1/tau) on positions) dz = -R with the global Jacobian), tau growing as the residual falls
    (at least doubled after every accepted step, up to tenfold as the residual falls) so that it ends as Newton's method. The tension force is minus the gradient of the total film
    length at fixed areas, so the flow descends the energy. A step that would flip a film or make an arc invalid is retried with
    tau / 4. Films falling below rc on the way take T1s (avalanches), logged with the move. Returns the events or None."""
    At = st.At.copy(); evs = []; seed = None if seed is None else set(int(v) for v in seed)
    def index():
        if seed is None: return build_index()
        # local problem: vertices within 4 rings of the seed move, bubbles touching them have free pressures and exact areas;
        # everything else is held (the global Newton then removes the small mismatch pushed outside)
        V = set(seed)
        for _ in range(4):
            e_ = np.nonzero(st.falive & (np.isin(st.fa, list(V)) | np.isin(st.fb, list(V))))[0]
            V |= set(st.fa[e_].tolist()) | set(st.fb[e_].tolist())
        Vf = np.array(sorted(V)); e_ = np.nonzero(st.falive & (np.isin(st.fa, Vf) | np.isin(st.fb, Vf)))[0]
        Bf = np.unique(np.concatenate([st.fl[e_], st.fr[e_]]))
        vx = -np.ones(len(st.valive), np.int64); bx = -np.ones(len(st.balive), np.int64)
        vx[Vf] = 2 * np.arange(len(Vf)); bx[Bf] = 2 * len(Vf) + np.arange(len(Bf))
        va_ = np.concatenate([[-1], Vf]); ba_ = np.concatenate([[-1], Bf])     # index 0 is the (absent) gauge slot
        return va_, ba_, vx, bx, 2 * len(Vf) + len(Bf)
    va, ba, vx, bx, n = index()
    tau = None; rold = None
    for k in range(maxit):
        res = residual(st.X, st.p, jac=True)
        if res is None: return fail('ptc-arc')
        nf = 2 * (len(va) - 1)
        R = np.concatenate([res['F'][va[1:]].ravel(), (res['A'] - At)[ba[1:]]])
        scale = np.maximum(At[ba[1:]], 0.01 * At[st.balive].mean())   # relative 1e-11, absolute floor 1e-13 <A> (rounding)
        ferr = np.abs(R[:nf]).max(); aerr = (np.abs(R[nf:]) / scale).max()
        if ferr < (1e-11 if seed is None else 1e-9) and aerr < (1e-11 if seed is None else 1e-9):
            st.At[:] = At; st.V[:] = 0; st.Vp[:] = 0
            if DEBUG: print('PTC converged', k, 'events', len(evs), flush=True)
            return evs
        rn = math.sqrt((R[:nf] ** 2).sum() + ((R[nf:] / scale) ** 2).sum())
        if tau is None:
            dl = np.hypot(res["c"][:, 0], res["c"][:, 1]); tau = TAU0 * float(np.median(dl))
        elif rold is not None: tau = min(tau * max(2.0, min(rold / max(rn, 1e-300), TAUG)), 1e14)
        rold = rn
        J0 = assemble(res, vx, bx, n)
        X0, p0 = st.X.copy(), st.p.copy(); ok = False
        for _ in range(20):
            J = J0 - sp.diags(np.concatenate([np.full(nf, 1.0 / tau), np.zeros(n - nf)]), format='csc')
            try: dz = splu(J.tocsc(), permc_spec='COLAMD').solve(-R)
            except Exception: tau /= 4; continue
            lam = 1.0
            for _ in range(8):
                st.X = X0.copy(); st.p = p0.copy()
                st.X[va[1:]] = np.mod(X0[va[1:]] + lam * dz[:nf].reshape(-1, 2), L); st.p[ba[1:]] = p0[ba[1:]] + lam * dz[nf:]
                if residual(st.X, st.p) is not None and not flipped(X0, st.X): ok = True; break
                lam /= 2
            if ok: break
            tau /= 4; rold = None
        if not ok:
            if DEBUG:
                rr = residual(st.X, st.p, jac=False); fl_ = flipped(X0, st.X)
                ef = np.nonzero(st.falive)[0]; c0_ = mi(X0[st.fb[ef]] - X0[st.fa[ef]]); d0 = np.hypot(c0_[:, 0], c0_[:, 1])
                k0 = res['kap']; s0 = np.abs(k0 * d0 / 2)
                print('PTC-STEP fail: arc invalid', rr is None, 'flipped', fl_[:5], 'lengths', [float(d0[list(ef).index(e)]) for e in fl_[:5]],
                      'max |s| now', float(s0.max()), 'tau', tau, 'min film', float(d0.min()), flush=True)
            st.X, st.p = X0, p0; return fail('ptc-step')
        if DEBUG > 1: print('  PTC', k, 'ferr', ferr, 'aerr', aerr, 'tau', tau, flush=True)
        more = topo_moves(At)
        if more is None: return None
        if more:
            evs += more; tau = None; rold = None
            if seed is not None:
                ef_ = np.nonzero(st.falive)[0]
                for ev in more:
                    bub = set(ev[1]) if ev[0] == 'T1' else set()
                    seed |= set(int(x) for e in ef_ if st.fl[e] in bub and st.fr[e] in bub for x in (st.fa[e], st.fb[e]))
            va, ba, vx, bx, n = index()
            if len(evs) > 500: return fail('ptc-avalanche')
    return fail('ptc-maxit')

def settle(seed=None):
    """After a topological move: implicit gradient flow on the neighbourhood of the move (4 rings), then the global Newton polish;
    if that does not converge, the same flow on the whole froth. Returns the events of the relaxation or None."""
    base = snapshot()
    if seed is not None and len(seed):
        evs = ptc(seed)
        if evs is not None:
            Xn, pn, it, why = newton(st.X, st.p, st.At)
            if Xn is not None and not flipped(st.X, Xn):
                st.X, st.p = Xn, pn; st.V[:] = 0; st.Vp[:] = 0
                return evs
        restore(base); counts['settle_global'] = counts.get('settle_global', 0) + 1
    return ptc(None)

def log_events(evs, tag=''):
    for ev in evs:
        if ev[0] == 'T1':
            q, Aq = ev[1], ev[2]
            fev.write(json.dumps([t, 'T1' + tag, *q] + Aq + [float(st.At[st.balive].mean())]) + '\n')
            counts['T1' + tag] += 1
        else:
            fev.write(json.dumps([t, ev[0] + tag, ev[1], ev[2], ev[3], float(st.At[st.balive].mean())]) + '\n')
            counts[ev[0] if not tag else 'T2' + tag] += 1
    fev.flush()

# ------------------------------------------------------------------ initial froth: periodic Voronoi (construction of vertex2d.py)
def init_voronoi(pts=None):
    if pts is None: pts = rng.random((N0, 2)) * L
    n0 = len(pts)
    shifts = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
    imgs = np.concatenate([pts + L * np.array(s) for s in shifts])
    vor = Voronoi(imgs); own = np.arange(len(imgs)) % n0
    vpts = {}
    for (i, j), rv in zip(vor.ridge_points, vor.ridge_vertices):
        for v in rv:
            if v >= 0: vpts.setdefault(v, set()).update((own[i], own[j]))
    key, pos = {}, []
    def vid(v):
        k = tuple(sorted(vpts[v]))
        if k not in key: key[k] = len(pos); pos.append(np.mod(vor.vertices[v], L))
        return key[k]
    E = []
    for (i, j), rv in zip(vor.ridge_points, vor.ridge_vertices):
        if -1 in rv: continue
        v0, v1 = vor.vertices[rv[0]], vor.vertices[rv[1]]; m = (v0 + v1) / 2
        if not (0 <= m[0] < L[0] and 0 <= m[1] < L[1]): continue
        d = v1 - v0
        left = i if d[0] * (imgs[i][1] - v0[1]) - d[1] * (imgs[i][0] - v0[0]) > 0 else j
        right = j if left == i else i
        E.append((vid(rv[0]), vid(rv[1]), own[left], own[right]))
    nv, nf = len(pos), len(E)
    assert nv == 2 * n0 and nf == 3 * n0, (nv, nf)
    alloc(nv + 64, nf + 64, n0)
    st.X[:nv] = np.array(pos); st.valive[:nv] = True
    E = np.array(E); st.fa[:nf], st.fb[:nf], st.fl[:nf], st.fr[:nf] = E.T; st.falive[:nf] = True
    st.balive[:] = True
    res = residual(st.X, st.p); st.At[:] = res['A']

def init_honeycomb(m):
    global L, N0
    L = np.array([float(m), m * math.sqrt(3) / 2]); N0 = m * m
    pts = np.array([[(i + 0.5 * (j % 2)) % m, j * math.sqrt(3) / 2] for j in range(m) for i in range(m)]) + 1e-9
    init_voronoi(pts)

# ------------------------------------------------------------------ recording and checks
fev = open(os.path.join(OUT, 'events.jsonl'), 'w'); fst = open(os.path.join(OUT, 'stats.jsonl'), 'w')
fcr = open(os.path.join(OUT, 'cross.jsonl'), 'w')
nsnap = 0

RATE_OVERRIDE = None    # target-area velocities used instead of von Neumann's law (mixing phase and tests only)

def rates():
    if RATE_OVERRIDE is not None:
        r = RATE_OVERRIDE.copy(); r[~st.balive] = 0; return r
    ns = nsides(); r = PI3 * (ns - 6.0)
    if LAW == 'wrong':
        Ab = st.At[st.balive].mean(); r = r + 2 * PI3 * (st.At / Ab - 1)
    r[~st.balive] = 0
    return r

def record(save=True):
    global nsnap
    res = residual(st.X, st.p)
    ef = res['ef']; ba = np.nonzero(st.balive)[0]
    ns = nsides(); n = ns[ba]; A = res['A'][ba]; Ab = A.mean()
    a, b = st.fa[ef], st.fb[ef]; c, kap = res['c'], res['kap']
    tax, tay, tbx, tby, seg, arc = film_local(c[:, 0], c[:, 1], kap)
    vv = np.concatenate([a, b]); an = np.arctan2(np.concatenate([tay, tby]), np.concatenate([tax, tbx]))
    o = np.lexsort((an, vv)); vv, an = vv[o], an[o]
    an3 = an.reshape(-1, 3); gaps = np.diff(np.concatenate([an3, an3[:, :1] + 2 * math.pi], 1), axis=1)
    maxdev = float(np.abs(gaps - 2 * math.pi / 3).max())
    flux = np.zeros(len(st.balive)); l, r = st.fl[ef], st.fr[ef]
    np.add.at(flux, l, -kap * arc); np.add.at(flux, r, kap * arc)       # geometric gas flux -sum_j (p_i - p_j) l_ij
    imposed = rates()
    co = np.polyfit(n, flux[ba], 1) if n.std() > 0 else np.array([np.nan, np.nan])
    E = float(arc.sum()); Ehex = len(ba) * math.sqrt(2 * math.sqrt(3) * Ab)
    rec = dict(t=t, N=int(len(ba)), Abar=float(Ab), mean_n=float(n.mean()), mu2=float(((n - 6.0) ** 2).mean()),
               p=[float((n == k).mean()) for k in range(2, 13)], E_over_Ehex=E / Ehex, max_angle_dev_deg=math.degrees(maxdev),
               flux_vs_imposed_max=float(np.abs(flux[ba] - imposed[ba]).max()),
               flux_vs_vN_max=float(np.abs(flux[ba] - PI3 * (n - 6)).max()), flux_slope=float(co[0]),
               flux_n0=float(-co[1] / co[0]) if co[0] == co[0] else None,
               area_err=float(np.abs(A - st.At[ba]).max()), counts=dict(counts), anomalies=dict(anomalies), wall=time.time() - T0)
    fst.write(json.dumps(rec) + '\n'); fst.flush()
    if save:
        np.savez_compressed(os.path.join(OUT, f'snap_{nsnap:04d}.npz'), t=t, ids=ba, n=n, A=A, pairs=np.stack([l, r], 1))
        nsnap += 1
    return rec

def flipped(Xo, Xn):
    ef = np.nonzero(st.falive)[0]
    co = mi(Xo[st.fb[ef]] - Xo[st.fa[ef]]); cn = mi(Xn[st.fb[ef]] - Xn[st.fa[ef]])
    return [int(e) for e in ef[(co * cn).sum(1) <= 0]]

def accept(Xn, pn, Atn, dt):
    global t
    Ab_o = st.At[st.balive].mean(); Ab_n = Atn[st.balive].mean(); ns = nsides()
    if RECORDING:
        for cc in CS:
            l2o = cc * RC * math.sqrt(Ab_o); l2n = cc * RC * math.sqrt(Ab_n)
            for g in np.nonzero(st.balive & (st.At >= l2o) & (Atn < l2n))[0]:
                fcr.write(json.dumps([t + dt, cc, int(g), int(ns[g])]) + '\n')
    st.V = mi(Xn - st.X) / dt; st.Vp = (pn - st.p) / dt
    st.X, st.p, st.At = Xn, pn, Atn
    t += dt

# ------------------------------------------------------------------ time stepping
def run(t_stop=np.inf, tag='', stop_after_T1=False):
    """von Neumann's law in time, exact equilibrium at every accepted step. Step size: at most the time for the fastest-shrinking
    film to lose half of its excess over rc, at most the time to the next bubble reaching 10 rc^2 (landed exactly), adapted to the
    Newton iteration count."""
    global t
    nlast = int(st.balive.sum()); dt_try = 1e-3; nextp = time.time()
    while True:
        Nn = int(st.balive.sum())
        if Nn <= NEND: return 'done'
        if t >= t_stop - 1e-12: return 'tstop'
        if stop_after_T1 and counts['T1' + tag] > 0: return 'T1seen'
        if time.time() - T0 > MAXWALL: return 'maxwall'
        # topological moves due now
        ef = np.nonzero(st.falive)[0]; c = mi(st.X[st.fb[ef]] - st.X[st.fa[ef]]); dl = np.hypot(c[:, 0], c[:, 1])
        if (dl < RC).any():
            e = int(ef[np.argmin(dl)]); ns = nsides(); P, Q = int(st.fl[e]), int(st.fr[e]); base = snapshot()
            if ns[P] <= 3 or ns[Q] <= 3:
                G = P if ns[P] <= 3 else Q; Ag = float(st.At[G]); out = T2(G)
                evs = None if out is None else [('T2side', G, out[0], Ag)]
                seed = [] if out is None else out[2]
            else:
                q = T1(e); evs = None if q is None else [('T1', q, [float(st.At[x]) for x in q])]
                seed = [int(st.fa[e]), int(st.fb[e])]
            more = settle(seed) if evs is not None else None
            if more is None: restore(base); return 'stuck-T1'
            log_events(evs + more, tag); dt_try = max(dt_try / 4, 1e-6)
            continue
        land = np.nonzero(st.balive & (st.At <= AT2 * (1 + 1e-9)))[0]
        if len(land):
            G = int(land[0]); Ag = float(st.At[G]); base = snapshot(); out = T2(G)
            more = settle(out[2]) if out is not None else None
            if more is None: restore(base); return 'stuck-T2'
            log_events([('T2', G, out[0], Ag)] + more, tag); dt_try = max(dt_try / 4, 1e-6)
            continue
        r = rates()
        shrink = st.balive & (r < 0)
        dt_land = ((st.At[shrink] - AT2) / -r[shrink]).min() if shrink.any() else np.inf
        # small bubbles on their way out (area below 5% of <A>, shrinking) shrink nearly self-similarly: their films are left out of
        # the film-shrink limit (their vanishing is landed exactly) and their vertices are predicted by scaling about the centroid
        Ab = st.At[st.balive].mean(); small = shrink & (st.At < 0.05 * Ab)
        dV = st.V[st.fb[ef]] - st.V[st.fa[ef]]; rate = -(dV * c).sum(1) / dl
        own = small[st.fl[ef]] | small[st.fr[ef]]
        lim = np.where((rate > 0) & ~own, 0.5 * (dl - 0.5 * RC) / np.maximum(rate, 1e-300), np.inf).min()
        dt = min(dt_try, dt_land, max(lim, 1e-12), t_stop - t); landing = dt == dt_land
        Atn = st.At + dt * r
        if landing: Atn[np.nonzero(shrink)[0][np.argmin((st.At[shrink] - AT2) / -r[shrink])]] = AT2
        Xg = np.mod(st.X + dt * st.V, L); pg = st.p + dt * st.Vp
        for g in np.nonzero(small)[0][np.argsort(-st.At[small])]:          # smallest last, so it wins at shared vertices
            fs = films_of_bubble(g); vs = np.unique(np.concatenate([st.fa[fs], st.fb[fs]]))
            ref = st.X[vs[0]]; rel = mi(st.X[vs] - ref); cen = ref + rel.mean(0); k = math.sqrt(max(Atn[g], 0) / st.At[g])
            Xg[vs] = np.mod(cen + (rel - rel.mean(0)) * k, L)
            nb = np.unique(np.concatenate([st.fl[fs], st.fr[fs]])); nb = nb[nb != g]
            pg[g] = st.p[nb].mean() + (st.p[g] - st.p[nb].mean()) / k
        Xn, pn, it, why = newton(Xg, pg, Atn)
        if Xn is None or flipped(st.X, Xn):
            dt_try = dt / 4
            if dt_try < 1e-13: return f'stuck-{why}'
            continue
        accept(Xn, pn, Atn, dt)
        dt_try = dt * (1.5 if it <= 6 else (0.5 if it >= 12 else 1.0))   # chord iterations are cheap
        if RECORDING and Nn <= nlast * (1 - REC):
            nlast = record()['N']
        if time.time() > nextp:
            print(f'PROGRESS {math.log(N0 / Nn) / math.log(N0 / NEND) if RECORDING else 0:.3f} {"coarsen" if RECORDING else "mix"} N={Nn} t={t:.4f} dt={dt:.2e} T1={counts["T1"]} '
                  f'T2={counts["T2"]} T2side={counts["T2side"]} mix={counts["T1init"]}/{counts["T2init"]} anomalies={sum(anomalies.values())} wall={time.time() - T0:.0f}', flush=True)
            nextp = time.time() + 60

def main():
    """Start: periodic Voronoi of N0 random points, as Rutenberg & McCurdy, relaxed to exact equilibrium at its own areas (implicit
    gradient flow, T1s logged as T1init and three-sided collapses as T2init, not counted). Then t = 0 and von Neumann's law alone."""
    global t, RECORDING
    init_voronoi()
    evs = ptc(None, maxit=5000)
    if evs is None: return 'init-fail'
    log_events(evs, tag='init')
    print('INIT', dict(N=int(st.balive.sum()), T1=counts['T1init'], T2=counts['T2init'],
                       mu2=float(((nsides()[st.balive] - 6.0) ** 2).mean()), wall=round(time.time() - T0)), flush=True)
    t = 0.0; RECORDING = True; st.V[:] = 0; st.Vp[:] = 0
    record()
    return run()

def test_hex():
    global RATE_OVERRIDE, NEND
    """Known answers. (1) A regular honeycomb is an equilibrium: forces 0, all angles 120 degrees, every flux 0. (2) One bubble's
    target halved (the rest shared out): the solver must restore exact 120-degree vertices, and the geometric gas flux of every bubble
    must equal von Neumann's (pi/3)(n - 6) = 0 to rounding. (3) Negative: a vertex moved off equilibrium must show a large angle
    error. (4) A T1 forced on one film of the perturbed honeycomb must relax to a new exact equilibrium (two 5- and two 7-sided
    bubbles) whose flux obeys von Neumann exactly (slope pi/3, zero at 6)."""
    ok = True
    init_honeycomb(8)
    res = residual(st.X, st.p)
    f0 = float(np.abs(res['F'][st.valive]).max()); a0 = float(np.abs(res['A'][st.balive] - math.sqrt(3) / 2).max())
    print('HEX regular: max force', f0, 'max area error', a0, flush=True); ok &= f0 < 1e-9 and a0 < 1e-9
    r1 = record(False); print('HEX regular', {k: r1[k] for k in ('max_angle_dev_deg', 'flux_vs_vN_max')}, flush=True)
    ok &= r1['max_angle_dev_deg'] < 1e-6 and r1['flux_vs_vN_max'] < 1e-9
    d = st.At[0] * 0.5; st.At[0] -= d; st.At[1:N0] += d / (N0 - 1)
    Xn, pn, it, why = newton(st.X, st.p, st.At, maxit=40)
    print('HEX perturbed: newton', why, it, flush=True); ok &= Xn is not None
    Xg = st.X.copy(); st.X, st.p = Xn, pn
    r2 = record(False); print('HEX perturbed', {k: r2[k] for k in ('max_angle_dev_deg', 'flux_vs_vN_max', 'area_err')}, flush=True)
    ok &= r2['max_angle_dev_deg'] < 1e-6 and r2['flux_vs_vN_max'] < 1e-8 and r2['area_err'] < 1e-9 and not flipped(Xg, Xn)
    base = snapshot()
    st.X[5] += 0.05; r3 = record(False); print('HEX negative (vertex moved): angle error', r3['max_angle_dev_deg'], flush=True)
    ok &= r3['max_angle_dev_deg'] > 0.1
    restore(base)
    # driven T1: the two bubbles P, Q on one film shrink to 0.45 of their area and the two bubbles R, S at its ends grow to keep
    # the total; relaxing at these areas must swap the film (R and S gain contact), ending in exact equilibrium with 5- and 7-sided
    # bubbles whose gas flux obeys von Neumann exactly.
    e = int(films_of_bubble(20)[0]); a_, b_ = int(st.fa[e]), int(st.fb[e]); P_, Q_ = int(st.fl[e]), int(st.fr[e])
    R_ = [int(st.fl[x] if st.fr[x] == P_ else st.fr[x]) for x in films_at(a_) if x != e and P_ in (st.fl[x], st.fr[x])][0]
    S_ = [int(st.fl[x] if st.fr[x] == P_ else st.fr[x]) for x in films_at(b_) if x != e and P_ in (st.fl[x], st.fr[x])][0]
    RATE_OVERRIDE = np.zeros(len(st.balive)); RATE_OVERRIDE[[P_, Q_]] = -0.5; RATE_OVERRIDE[[R_, S_]] = 0.5
    NEND = 0; stt = run(1.5, tag='', stop_after_T1=True); RATE_OVERRIDE = None
    evs = [] if stt in ('T1seen', 'tstop') else None
    q = [tuple(json.loads(l)[2:6]) for l in open(os.path.join(OUT, 'events.jsonl')) if json.loads(l)[1] == 'T1']
    print('HEX driven T1:', stt, 'events', q, 'expected the swap of', (P_, Q_, R_, S_), flush=True)
    ok &= any(set(x) == {P_, Q_, R_, S_} for x in q)
    ok &= evs is not None
    if evs is not None:
        r4 = record(False)
        print('HEX driven T1 final:', dict( p=r4['p'][1:7], angle=r4['max_angle_dev_deg'], slope=r4['flux_slope'],
                                     n0=r4['flux_n0'], flux_vs_vN=r4['flux_vs_vN_max']), flush=True)
        ok &= r4['max_angle_dev_deg'] < 1e-6 and abs(r4['flux_slope'] - PI3) < 1e-8 and abs(r4['flux_n0'] - 6) < 1e-8
    return ok

if __name__ == '__main__' and TEST == 'hex':
    ok = test_hex(); fev.close(); fst.close(); fcr.close()
    print('FINAL ok' if ok else 'FINAL FAIL', flush=True); sys.exit(0)

if __name__ == '__main__':
    status = main()
    rec = record()
    fev.close(); fst.close(); fcr.close()
    fin = dict(params=dict(N0=N0, Nend=NEND, rc=RC, AT2=AT2, seed=SEED, law=LAW), status=status, t=t, N=int(st.balive.sum()),
               counts=counts, anomalies=anomalies, last=rec, wall=time.time() - T0)
    json.dump(fin, open(os.path.join(OUT, 'final.json'), 'w'), indent=1)
    good = status == 'done' and rec['max_angle_dev_deg'] < 1e-4 and anomalies['T1 R==S'] + anomalies['T2 shared outer'] == 0
    if LAW == 'wrong': good = status == 'done' and rec['flux_vs_imposed_max'] > 1e-3      # the negative control must FAIL the check
    print('VFROTH', json.dumps(dict(status=status, N=fin['N'], counts=counts, anomalies=anomalies)), flush=True)
    print('FINAL ok' if good else f'FINAL FAIL status={status}', flush=True)
