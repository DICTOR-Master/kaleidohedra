"""Branch D round 3: straight-skeleton division of the resin, EXACT for C1 (field K = Q(sqrt5, sqrt3)) and at 50 digits for C2.
Same wavefront algorithm as skeleton.py (faces move out along unit normals at unit speed; an edge shrinking to 0 flips; degree-4/5 vertices
carried as zero-length edges; simultaneous events resolved until no edge is negative or shrinking).
C1 exact: hexagon unit normals are v/sqrt3 with v in Q(sqrt5)^3, spike-triangle unit normals lie in Q(sqrt5)^3 (2-fold axes), so planes,
vertices, event heights, slab vertices and volumes all lie in K and every test below is an exact sign in K:
 - volume sum of all slabs = mould - C1 (exact);
 - interior-disjointness of every slab pair of different faces and of every slab with the convex parts of C1 (TI, 12 pyramids): a separating
   axis (facet normal or edge cross product) is found in floats and then VERIFIED exactly (max over one vertex set <= min over the other);
 - together these prove the slabs tile the resin;
 - scutoids: real events (an edge of positive length collapsing) whose point lies strictly inside the mould, and the piece's walls.
C2 at 50 digits (decagon normals need sqrt((5+sqrt5)/2)): volume identity |gap| < 1e-40 and the same separating-axis test in floats.
Usage: python skeleton2.py out.json solid mode lattice factor [lattice factor ...]   solid C1|C2, mode exact|mp"""
import itertools, json, math, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from resin import Q, build_C1, TH, act, polytope, congruent, cross as qcross, vsub as qsub, dot as qdot
mp.mp.dps = 50
def pr(*a): print(*a, flush=True)

class K:
    """a + b sqrt5 + c sqrt3 + d sqrt15, Fractions"""
    __slots__ = ("a", "b", "c", "d")
    def __init__(s, a=0, b=0, c=0, d=0):
        s.a = a if type(a) is Fr else Fr(a); s.b = b if type(b) is Fr else Fr(b)
        s.c = c if type(c) is Fr else Fr(c); s.d = d if type(d) is Fr else Fr(d)
    def __add__(s, o):
        if not isinstance(o, K): o = K(o)
        return K(s.a+o.a, s.b+o.b, s.c+o.c, s.d+o.d)
    __radd__ = __add__
    def __neg__(s): return K(-s.a, -s.b, -s.c, -s.d)
    def __sub__(s, o):
        if not isinstance(o, K): o = K(o)
        return K(s.a-o.a, s.b-o.b, s.c-o.c, s.d-o.d)
    def __rsub__(s, o): return (-s) + o
    def __mul__(s, o):
        if not isinstance(o, K):
            o = Fr(o); return K(s.a*o, s.b*o, s.c*o, s.d*o)
        a1, b1, c1, d1, a2, b2, c2, d2 = s.a, s.b, s.c, s.d, o.a, o.b, o.c, o.d
        return K(a1*a2 + 5*b1*b2 + 3*c1*c2 + 15*d1*d2, a1*b2 + b1*a2 + 3*(c1*d2 + d1*c2),
                 a1*c2 + c1*a2 + 5*(b1*d2 + d1*b2), a1*d2 + d1*a2 + b1*c2 + c1*b2)
    __rmul__ = __mul__
    def __truediv__(s, o):
        if not isinstance(o, K):
            o = Fr(o); return K(s.a/o, s.b/o, s.c/o, s.d/o)
        y3 = K(o.a, o.b, -o.c, -o.d); P = o*y3                     # in Q(sqrt5)
        P5 = K(P.a, -P.b); N_ = P.a*P.a - 5*P.b*P.b               # rational
        return (s*y3*P5)*(Fr(1)/N_)
    def sign(s):
        X = Q(s.a, s.b); Y = Q(s.c, s.d); sx, sy = X.sign(), Y.sign()
        if sy == 0: return sx
        if sx == 0: return sy
        if sx == sy: return sx
        return sx*(X*X - 3*(Y*Y)).sign()
    def __float__(s): return float(s.a) + float(s.b)*math.sqrt(5) + float(s.c)*math.sqrt(3) + float(s.d)*math.sqrt(15)
    def mpf(s): return mp.mpf(s.a.numerator)/s.a.denominator + mp.mpf(s.b.numerator)/s.b.denominator*mp.sqrt(5) + \
        mp.mpf(s.c.numerator)/s.c.denominator*mp.sqrt(3) + mp.mpf(s.d.numerator)/s.d.denominator*mp.sqrt(15)
    def key(s): return (s.a, s.b, s.c, s.d)
    def __eq__(s, o): return (s - o).sign() == 0
    def __hash__(s): return hash(s.key())
    def __lt__(s, o): return (s - o).sign() < 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __abs__(s): return s if s.sign() >= 0 else -s
    def __str__(s):
        t = [(s.a, ""), (s.b, "*sqrt5"), (s.c, "*sqrt3"), (s.d, "*sqrt15")]
        out = " + ".join(f"({x}){n}" for x, n in t if x != 0)
        return out or "0"
    __repr__ = __str__

def ratsqrt(x):
    if x < 0: return None
    n, d = x.numerator, x.denominator; rn, rd = math.isqrt(n), math.isqrt(d)
    return Fr(rn, rd) if rn*rn == n and rd*rd == d else None
def sqrtQ5(r0, r1):
    """sqrt of r0 + r1 sqrt5 (rationals) as a + b sqrt5, or None"""
    if r1 == 0:
        a = ratsqrt(r0)
        if a is not None: return (a, Fr(0))
        b = ratsqrt(r0/5)
        return (Fr(0), b) if b is not None else None
    disc = ratsqrt(r0*r0 - 5*r1*r1)
    if disc is None: return None
    for z in ((r0 + disc)/2, (r0 - disc)/2):
        a = ratsqrt(z)
        if a:
            b = r1/(2*a)
            if (Q(a, b)).sign() < 0: a, b = -a, -b
            return (a, b)
    return None
def sqrtK_of_Q5(q):
    """sqrt of a positive element of Q(sqrt5), inside K"""
    r = sqrtQ5(q.a, q.b)
    if r: return K(r[0], r[1])
    r = sqrtQ5(q.a/3, q.b/3)        # q = 3 x^2 -> sqrt = x sqrt3
    if r: return K(0, 0, r[0], r[1])
    raise ValueError(f"sqrt of {q} not in K")

# ---------- solids ----------
def solid(name):
    if name == "C1":
        C = build_C1()
        pyr = [(C["pents"][p], 60 + p, list(range(20 + 5*p, 25 + 5*p))) for p in range(12)]
        core = C["hexes"] + C["pents"]
        volS = Q(35, Fr(25, 2))
    else:
        from c2 import build_C2
        C = build_C2()
        pyr = [(C["tris"][p], 60 + p, list(range(12 + 3*p, 15 + 3*p))) for p in range(20)]
        core = C["decs"] + C["tris"]
        volS = None
    return C, pyr, core, volS

def setup(name, mode):
    C, pyr, core, volS = solid(name)
    V, faces, planes = C["V"], C["faces"], C["planes"]
    if mode == "exact":
        num = lambda q: K(q.a, q.b)
        N = []
        for n, c in planes:
            r = qdot(n, n); L = sqrtK_of_Q5(r)
            N.append([num(x)/L for x in n])
        Vn = [[num(x) for x in v] for v in V]
    else:
        num = lambda q: q.mpf()
        N = []
        for n, c in planes:
            m = [x.mpf() for x in n]; L = mp.sqrt(sum(x*x for x in m)); N.append([x/L for x in m])
        Vn = [[x.mpf() for x in v] for v in V]
    return dict(C=C, pyr=pyr, core=core, volS=volS, V=V, Vn=Vn, faces=faces, planes=planes, N=N, num=num, mode=mode)

def run(S, lat, fac, t_extra=None):
    mode = S["mode"]; V, Vn, faces, N = S["V"], S["Vn"], S["faces"], S["N"]; NF = len(faces)
    exact = mode == "exact"
    def fr(x): x = Fr(x); return K(x) if exact else mp.mpf(x.numerator)/x.denominator
    def zero(x): return x.sign() == 0 if exact else abs(x) < mp.mpf(10)**-30
    def neg(x): return x.sign() < 0 if exact else x < -mp.mpf(10)**-30
    def pos(x): return x.sign() > 0 if exact else x > mp.mpf(10)**-30
    def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
    def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    def det(a, b, c): return dot(a, cr(b, c))
    Cf = [dot(N[f], Vn[faces[f][0][0]]) for f in range(NF)]
    fv = []
    for f, (vs, kind) in enumerate(faces):
        P = [Vn[i] for i in vs]
        if neg(dot(cr([P[1][j]-P[0][j] for j in range(3)], [P[2][j]-P[0][j] for j in range(3)]), N[f])): vs = vs[::-1]
        fv.append(vs)
    edge_face = {}
    for f, vs in enumerate(fv):
        for i in range(len(vs)): edge_face.setdefault(frozenset((vs[i], vs[(i+1) % len(vs)])), []).append(f)
    cyc0 = [[[g for g in edge_face[frozenset((vs[i], vs[(i+1) % len(vs)]))] if g != f][0] for i in range(len(vs))] for f, vs in enumerate(fv)]
    vcache = {}
    def vert(f, g, h):
        key = tuple(sorted((f, g, h)))
        if key in vcache: return vcache[key]
        a, b, c = N[f], N[g], N[h]; D = det(a, b, c)
        if zero(D): vcache[key] = None; return None
        ca, cb, cc = cr(b, c), cr(c, a), cr(a, b)
        x0 = [(Cf[f]*ca[t] + Cf[g]*cb[t] + Cf[h]*cc[t])/D for t in range(3)]
        x1 = [(ca[t] + cb[t] + cc[t])/D for t in range(3)]
        vcache[key] = (x0, x1); return vcache[key]
    def at(X, t): return [X[0][j] + t*X[1][j] for j in range(3)]
    class Front: pass
    F = Front(); F.cyc = {f: list(cyc0[f]) for f in range(NF)}; F.t = 0*Cf[0]
    def edge(f, i):
        c = F.cyc[f]; n = len(c); g = c[i]
        a = vert(f, c[i-1], g); b = vert(f, g, c[(i+1) % n])
        if a is None or b is None: return None
        u = cr(N[f], N[g]); t = F.t
        poly = [at(p, t) for p in (vert(f, c[k], c[(k+1) % n]) for k in range(n)) if p is not None]
        cen = [sum((p[j] for p in poly), 0*t)/len(poly) for j in range(3)]
        side = dot([cen[j] - a[0][j] - t*a[1][j] for j in range(3)], cr(N[f], u))
        sg = 1 if pos(side) else -1
        L0 = sg*dot([b[0][j]-a[0][j] for j in range(3)], u); L1 = sg*dot([b[1][j]-a[1][j] for j in range(3)], u)
        return L0, L1, a
    def edges():
        for f in F.cyc:
            for i, g in enumerate(F.cyc[f]):
                if f < g: yield f, i, g
    def kill(X):
        for P in set(F.cyc[X]):
            c = F.cyc[P]
            while X in c: c.remove(X)
            k = 0
            while k < len(c) and len(c) > 1:
                if c[k] == c[(k+1) % len(c)]: c.pop(k)
                else: k += 1
        del F.cyc[X]
    def flip(A, B):
        cA = F.cyc[A]; i = cA.index(B); Cc = cA[i-1]; D = cA[(i+1) % len(cA)]
        def insert(X, P1, P2, new):
            c = F.cyc[X]
            for j in range(len(c)):
                if {c[j], c[(j+1) % len(c)]} == {P1, P2}: c.insert(j+1, new); return
            raise RuntimeError(f"flip: {P1},{P2} not consecutive in face {X}")
        insert(Cc, A, B, D); insert(D, A, B, Cc)
        cA.remove(B); F.cyc[B].remove(A)
        for X in (A, B):
            if len(F.cyc[X]) < 3: kill(X)
        return (A, B, Cc, D)
    def check():
        for f, c in F.cyc.items():
            for i, g in enumerate(c):
                h = c[(i+1) % len(c)]; cg = F.cyc[g]; j = cg.index(f)
                assert cg[j-1] == h, f"inconsistent vertex ({f},{g},{h})"
    # fan of zero-length edges at vertices of degree > 3
    for v in range(len(V)):
        ring = [f for f in range(NF) if v in fv[f]]
        if len(ring) <= 3: continue
        order = [ring[0]]
        while len(order) < len(ring):
            f = order[-1]; i = fv[f].index(v); order.append(cyc0[f][i-1])
        d = len(order); F0 = order[0]; c = F.cyc[F0]
        for j in range(len(c)):
            a, b = c[j], c[(j+1) % len(c)]
            if {a, b} == {order[1], order[-1]}:
                mid = order[2:-1] if a == order[1] else order[-2:1:-1]
                F.cyc[F0] = c[:j+1] + mid + c[j+1:]; break
        else: raise RuntimeError("fan F0")
        for k in range(2, d-1):
            cc = F.cyc[order[k]]
            for j in range(len(cc)):
                if {cc[j], cc[(j+1) % len(cc)]} == {order[k-1], order[k+1]}: cc.insert(j+1, F0); break
            else: raise RuntimeError("fan Fk")
    check()
    # mould
    from resin import Q as QQ
    s0 = {"sc": QQ(Fr(5, 2), Fr(3, 2)), "bcc": QQ(Fr(10, 3), Fr(4, 3)), "fcc": QQ(5, 2)}
    if S["volS"] is None: s0 = {"sc": QQ(Fr(7, 2), Fr(3, 2)), "bcc": QQ(4, 2), "fcc": QQ(5, 2)}
    sq = s0[lat]*fac
    unitH = []
    if lat in ("sc", "bcc"):
        for i in range(3):
            for sgn_ in (1, -1):
                n = [0, 0, 0]; n[i] = sgn_; unitH.append((n, Fr(1, 2)))
    if lat == "bcc":
        for sg3 in itertools.product((1, -1), repeat=3): unitH.append((list(sg3), Fr(3, 4)))
    if lat == "fcc":
        for i, j in ((0, 1), (1, 2), (0, 2)):
            for a, b in itertools.product((1, -1), repeat=2):
                n = [0, 0, 0]; n[i] = a; n[j] = b; unitH.append((n, Fr(1, 2)))
    sN = S["num"](sq)
    Hm = [([0*sN + x for x in n], sN*fr(k), ("shell", idx)) for idx, (n, k) in enumerate(unitH)]
    cellf = {"sc": Fr(1), "bcc": Fr(1, 2), "fcc": Fr(1, 4)}[lat]
    cell = sN*sN*sN*fr(cellf)
    # C volume
    volS = 0*sN
    for f in range(NF):
        P = [Vn[i] for i in fv[f]]
        for q in range(1, len(P) - 1):
            d_ = det(P[0], P[q], P[q+1]); volS = volS + (d_ if not neg(d_) else -d_)
    volS = volS/6
    mv = polytope(Hm, tol=None if exact else mp.mpf(10)**-35)["verts"]
    t_end = max(math.sqrt(sum(float(x)**2 for x in v)) for v in mv) + 0.01
    if t_extra: t_end = max(t_end, t_extra)
    t_endN = S["num"](QQ(Fr(t_end).limit_denominator(1000)))
    def real_before(A, B):
        """edge A|B existed with positive length in the interval before this event (not a zero-length fan edge)"""
        t0_, t1_, cyc = intervals[-1]
        if B not in cyc.get(A, []): return False
        c = cyc[A]; i = c.index(B); a = vert(A, c[i-1], B); b = vert(A, B, c[(i+1) % len(c)])
        if a is None or b is None: return False
        tm_ = (t0_ + t1_)/2; dd = [b[0][j]-a[0][j] + tm_*(b[1][j]-a[1][j]) for j in range(3)]
        return not zero(dot(dd, dd))
    # simulate
    t = 0*sN; intervals = []; events = []
    while True:
        best = None
        for f, i, g in edges():
            e = edge(f, i)
            if e is None: continue
            L0, L1, a = e
            if neg(L1):
                te = -L0/L1
                if pos(te - t) and (best is None or neg(te - best)): best = te
        tn = t_endN if best is None or pos(best - t_endN) else best
        intervals.append((t, tn, {f: list(c) for f, c in F.cyc.items()}))
        if not neg(tn - t_endN): break
        tprev = t; t = tn; F.t = t
        for rnd in range(2000):
            todo = None
            for f, i, g in edges():
                e = edge(f, i)
                if e is None: continue
                L0, L1, a = e; L = L0 + L1*t
                if zero(L) and neg(L1): todo = (f, g, at(a, t), real_before(f, g)); break
                if neg(L): raise RuntimeError(f"negative edge {f}|{g}")
            if todo is None: break
            f, g, p, real = todo
            ev = flip(f, g); events.append(dict(t=t, faces=ev, point=p, real=real))
        else: raise RuntimeError("events did not settle")
        check()
    # an event point is real when at least one flip there collapses an edge of positive length; every adjacency change at a real point
    # counts (it is kept only if the new or lost wall has positive area in the slabs)
    for e in events:
        e["realpt"] = any(x["real"] and all(zero(e["point"][j] - x["point"][j]) for j in range(3)) for x in events if zero(x["t"] - e["t"]))
    def inside(p):
        return all(neg(dot(n, p) - c) for n, c, l in Hm)
    # slabs
    slabs = []
    for k, (t0, t1, cyc) in enumerate(intervals):
        tm = (t0 + t1)/2
        for f, c in cyc.items():
            H = [([-x for x in N[f]], -(Cf[f] + t0), ("bottom" if k == 0 else "tk", f)), (list(N[f]), Cf[f] + t1, ("tk", f))]
            poly = [at(X, tm) for X in (vert(f, c[i], c[(i+1) % len(c)]) for i in range(len(c))) if X is not None]
            cen = [sum((p[j] for p in poly), 0*tm)/len(poly) for j in range(3)]
            for ig, g in enumerate(c):
                A_ = vert(f, c[ig-1], g); B_ = vert(f, g, c[(ig+1) % len(c)])
                if A_ is not None and B_ is not None:
                    dd = [(B_[0][j] - A_[0][j]) + tm*(B_[1][j] - A_[1][j]) for j in range(3)]
                    if zero(dot(dd, dd)): continue
                val = dot([N[f][j]-N[g][j] for j in range(3)], cen) - (Cf[f]-Cf[g])
                if zero(val): continue
                sig = 1 if pos(val) else -1
                H.append(([-sig*(N[f][j]-N[g][j]) for j in range(3)], -sig*(Cf[f]-Cf[g]), ("lat", g)))
            H += Hm
            try: P = polytope(H, tol=None if exact else mp.mpf(10)**-35)
            except (AssertionError, ValueError, ZeroDivisionError, IndexError): continue
            if len(P["verts"]) < 4 or not pos(P["vol"]): continue
            slabs.append((f, k, H, P))
    total = sum((P["vol"] for f, k, H, P in slabs), 0*sN)
    gap = total - (cell - volS)
    vol_ok = zero(gap) if exact else abs(gap) < mp.mpf(10)**-40
    # separating-axis test: float search, exact verification
    def axes_of(verts, facesets, normals):
        ax = [n for n in normals]
        eds = set()
        for fs in facesets:
            for i in range(len(fs)): eds.add(tuple(sorted((fs[i], fs[(i+1) % len(fs)]))))
        dirs = [[verts[b][j] - verts[a][j] for j in range(3)] for a, b in eds]
        return ax, dirs
    def slab_geom(H, P):
        verts = P["verts"]; fl = np.array([[float(x) for x in v] for v in verts])
        fs = list(P["faces"].values()); normals = [H[t][0] for t in P["faces"]]
        ax, dirs = axes_of(verts, fs, normals)
        return verts, fl, ax, dirs
    def separated(GA, GB):
        vA, fA, axA, dA = GA; vB, fB, axB, dB = GB
        cands = [(a, None) for a in axA + axB]
        best = None
        for a, _ in cands:
            af = np.array([float(x) for x in a]); pa, pb = fA @ af, fB @ af
            g = max(pb.min() - pa.max(), pa.min() - pb.max()) / (np.linalg.norm(af) or 1)
            if best is None or g > best[0]: best = (g, a)
        if best[0] < -1e-9:
            for da in dA:
                for db in dB:
                    a = cr(da, db); af = np.array([float(x) for x in a]); L = np.linalg.norm(af)
                    if L < 1e-12: continue
                    pa, pb = fA @ af, fB @ af
                    g = max(pb.min() - pa.max(), pa.min() - pb.max()) / L
                    if g > best[0]: best = (g, a)
        if best[0] < -1e-9: return False, best[0]
        a = best[1]
        pa = [dot(a, v) for v in vA]; pb = [dot(a, v) for v in vB]
        if exact:
            ok = (not pos(max(pa) - min(pb))) or (not pos(max(pb) - min(pa)))
        else:
            ok = max(pa) - min(pb) < mp.mpf(10)**-30 or max(pb) - min(pa) < mp.mpf(10)**-30
        return ok, best[0]
    G = [slab_geom(H, P) for f, k, H, P in slabs]
    BB = [(g[1].min(0), g[1].max(0)) for g in G]
    npairs = 0; bad = []
    for i, j in itertools.combinations(range(len(slabs)), 2):
        if slabs[i][0] == slabs[j][0]: continue
        if np.any(BB[i][1] < BB[j][0] - 1e-9) or np.any(BB[j][1] < BB[i][0] - 1e-9): continue
        npairs += 1
        ok, g = separated(G[i], G[j])
        if not ok: bad.append((slabs[i][0], slabs[j][0], g))
    # convex parts of the solid
    parts = []
    for fs in [S["core"]]:
        verts = [Vn[i] for i in range(60)]
        normals = []
        idxfaces = []
        for face_ in fs:
            P = [Vn[i] for i in face_]; normals.append(cr([P[1][j]-P[0][j] for j in range(3)], [P[2][j]-P[0][j] for j in range(3)]))
            idxfaces.append(face_)
        ax, dirs = axes_of(Vn, idxfaces, normals)
        parts.append(([Vn[i] for i in range(60)], np.array([[float(x) for x in Vn[i]] for i in range(60)]), ax, dirs))
    for base, apx, lat_ in S["pyr"]:
        ids = list(base) + [apx]
        fsl = [list(base)] + [list(S["faces"][fi][0]) for fi in lat_]
        normals = [cr([Vn[f_[1]][j]-Vn[f_[0]][j] for j in range(3)], [Vn[f_[2]][j]-Vn[f_[0]][j] for j in range(3)]) for f_ in fsl]
        ax, dirs = axes_of(Vn, fsl, normals)
        parts.append(([Vn[i] for i in ids], np.array([[float(x) for x in Vn[i]] for i in ids]), ax, dirs))
    nC = 0
    for i in range(len(slabs)):
        for q in parts:
            if np.any(BB[i][1] < q[1].min(0) - 1e-9) or np.any(q[1].max(0) < BB[i][0] - 1e-9): continue
            nC += 1
            ok, g = separated(G[i], q)
            if not ok: bad.append((slabs[i][0], "solid", g))
    valid = vol_ok and not bad
    word = "exact" if exact else "50 digits"
    pr(f"\n=== {S['name']} {lat} s = {fac} s0 = {float(sq):.6f} ({word}): events {len(events)} flips ({sum(1 for e in events if e['real'])} real) at heights "
       + ", ".join(sorted({str(e['t']) if exact else mp.nstr(e['t'], 12) for e in events})))
    pr(f"   slabs {len(slabs)}; volume sum - (mould - solid) = {gap if exact else mp.nstr(gap, 5)}; separating axes verified for {npairs} slab pairs and "
       f"{nC} slab/part pairs, failures {len(bad)} {bad[:3]}  => {'VALID division' if valid else 'NOT valid'}")
    # kinds
    keyv = {tuple(x.key() for x in v): i for i, v in enumerate(V)}
    fid = {frozenset(fv[f]): f for f in range(NF)}
    def gface(g, f): return fid[frozenset(keyv[tuple(x.key() for x in act(g, V[i]))] for i in fv[f])]
    orbits, done = [], set()
    for f in range(NF):
        if f in done: continue
        o = sorted({gface(g, f) for g in TH}); done |= set(o); orbits.append(o)
    kinds = []
    for o in orbits:
        f = o[0]; mine = [(k, H, P) for ff, k, H, P in slabs if ff == f]
        if not mine: continue
        pts, ptsx = [], []
        walls, mouldf = set(), set()
        for k, H, P in mine:
            for v in P["verts"]:
                fl = np.array([float(x) for x in v])
                if not any(np.linalg.norm(fl - q) < 1e-9 for q in pts): pts.append(fl); ptsx.append(v)
            for t_ in P["faces"]:
                lab = H[t_][2]
                if lab[0] == "lat": walls.add(lab[1])
                if lab[0] == "shell": mouldf.add(lab[1])
        vol = sum((P["vol"] for k, H, P in mine), 0*sN)
        realin = [e for e in events if e["realpt"] and f in e["faces"] and inside(e["point"])]
        lost = sorted({e["faces"][1-e["faces"].index(f)] for e in realin if f in e["faces"][:2]} & walls)
        gained = sorted({e["faces"][5-e["faces"].index(f)] for e in realin if f in e["faces"][2:]} & walls)
        ypts = []
        for e in realin:
            if not any(np.linalg.norm(np.array([float(x) for x in e["point"]]) - np.array([float(x) for x in q])) < 1e-9 for q in ypts): ypts.append(e["point"])
        nb0 = sorted(cyc0[f]); nbtop = sorted((set(nb0) - set(lost)) | set(gained))
        rec = dict(face=f, kind=faces[f][1], orbit=len(o), vol=float(vol), volx=str(vol) if exact else mp.nstr(vol, 30),
                   n_points=len(pts), walls=sorted(walls), mould_facets=len(mouldf), nb_C1_side=nb0, nb_mould_side=nbtop,
                   n_nb_C1_side=len(nb0), n_nb_mould_side=len(nbtop), Y=len(ypts) if (lost or gained) else 0,
                   Y_points=[[str(x) for x in p] for p in ypts] if (lost or gained) else [],
                   scutoid=bool(lost or gained), pts=[list(p) for p in pts],
                   slabs=[dict(interval=k, vertices=[[str(x) for x in v] for v in P["verts"]],
                               faces=[dict(label=list(map(str, H[t_][2])), vertices=vs) for t_, vs in P["faces"].items()]) for k, H, P in mine])
        for kd in kinds:
            if abs(kd["vol"] - rec["vol"]) < 1e-9 and congruent(np.array(kd["pts"]), np.array(rec["pts"])): kd["members"].append(f); break
        else: rec["members"] = [f]; kinds.append(rec)
    for kd in kinds:
        pr(f"   kind {kd['kind']} face {kd['face']} ({sum(len(o) for o in orbits if o[0] in kd['members'])} per cell): vol {kd['volx'] if exact else kd['vol']}"
           f" (= {kd['vol']:.6f}); neighbours C1 side {kd['n_nb_C1_side']} -> mould side {kd['n_nb_mould_side']}; Y vertices {kd['Y']}; scutoid {kd['scutoid']}; "
           f"walls {kd['walls']}, mould facets {kd['mould_facets']}")
        for p in kd["Y_points"]: pr(f"      Y vertex: ({', '.join(p)})")
    # scale thresholds: smallest scale with a real event point strictly inside the mould
    thr = None
    for e in events:
        if not e["real"]: continue
        sp = None
        for n, k in unitH:
            r = dot([0*sN + x for x in n], e["point"])/fr(k)
            if sp is None or pos(r - sp): sp = r
        if thr is None or neg(sp - thr): thr = sp
    pr(f"   SUMMARY {S['name']} {lat} x{fac}: valid {valid}; kinds {len(kinds)}; scutoid kinds {sum(1 for k in kinds if k['scutoid'])}; "
       f"scutoids appear for mould scale s > {thr if exact else mp.nstr(thr, 15)} (= {float(thr):.6f} = {float(thr)/float(s0[lat]):.6f} s0)")
    return dict(solid=S["name"], lattice=lat, factor=str(fac), s=str(sq), mode=mode, valid=valid, volume_gap=str(gap) if exact else mp.nstr(gap, 8),
                event_heights=sorted({str(e["t"]) if exact else mp.nstr(e["t"], 30) for e in events}),
                scutoid_threshold_s=str(thr) if exact else mp.nstr(thr, 30), scutoid_threshold_ratio=float(thr)/float(s0[lat]),
                n_kinds=len(kinds), n_scutoid_kinds=sum(1 for k in kinds if k["scutoid"]),
                kinds=[{k: v for k, v in kd.items() if k != "pts"} for kd in kinds]), events, intervals

if __name__ == "__main__":
    outp, name, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    S = setup(name, mode); S["name"] = name
    args = sys.argv[4:]; res = []
    for lat, fac in zip(args[::2], args[1::2]):
        r, events, intervals = run(S, lat, Fr(fac)); res.append(r)
        if name == "C1" and mode == "exact":
            t1 = min((e["t"] for e in events), key=lambda x: float(x))
            claim = K(Fr(-1, 2), Fr(1, 2), Fr(-1, 4), Fr(1, 4))
            pr(f"   first event height t1 = {t1}; equals (2+sqrt3)(sqrt5-1)/4 exactly: {(t1 - claim).sign() == 0}")
            r["t1"] = str(t1); r["t1_is_closed_form"] = (t1 - claim).sign() == 0
    json.dump(res, open(outp, "w"), indent=1, default=str)
    ok = all(r["valid"] for r in res) and all(r.get("t1_is_closed_form", True) for r in res)
    pr("FINAL ok" if ok else "FINAL FAIL: " + ", ".join(f"{r['lattice']} x{r['factor']} valid={r['valid']}" for r in res))
