"""Branch D lead 1: the straight skeleton (offset-surface division) of the resin between C1 and the mould.
Every C1 face plane moves outward along its normal at unit speed; the wavefront is tracked as a polyhedral surface (each face keeps the
cyclic list of its neighbouring faces, counter-clockwise about its outward normal; vertices = intersections of three moving planes, linear
in t).  Events: an edge of the wavefront shrinks to length 0 -> flip (faces A|B part, faces C|D meet; a face left with < 3 neighbours
vanishes).  Degenerate events (several edges at once, forced by the symmetry) are resolved by flipping until every edge has length >= 0
and none is shrinking at t+ (the unique non-negative continuation).  Piece(F) = union over event intervals [t_k, t_k+1] of the slab
{t_k <= d_F <= t_k+1} cut by the walls (bisector planes d_F = d_G) of F's neighbours in that interval, clipped by the mould.
50 digits (mpmath).  Checks: volume sum = mould - C1 (|gap| < 1e-30), no overlap between slabs of different faces and between slabs and
C1 (LP Chebyshev depth <= 1e-9, float64), wavefront consistency after every event batch.
Usage: python skeleton.py out.json lattice factor [lattice factor ...]   (factor as p/q of s0)"""
import itertools, json, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
from scipy.optimize import linprog
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from resin import build_C1, Q, dot, vsub, cross, tofl, TH, act, polytope, congruent, ident, LAMBDA
mp.mp.dps = 50
EPS = mp.mpf(10)**-30
def pr(*a): print(*a, flush=True)
def M(u): return [x.mpf() if isinstance(x, Q) else mp.mpf(x) for x in u]
def mdot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def mcross(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
def unit(u): L = mp.sqrt(mdot(u, u)); return [x/L for x in u]

C = build_C1(); V, faces, planes = C["V"], C["faces"], C["planes"]
NF = len(faces)
N = [unit(M(n)) for n, c in planes]
Cf = [mdot(N[f], M(V[faces[f][0][0]])) for f in range(NF)]
# CCW vertex order about the outward normal
fv = []
for f, (vs, kind) in enumerate(faces):
    P = [M(V[i]) for i in vs]
    if mdot(mcross([P[1][j]-P[0][j] for j in range(3)], [P[2][j]-P[0][j] for j in range(3)]), N[f]) < 0: vs = vs[::-1]
    fv.append(vs)
edge_face = {}
for f, vs in enumerate(fv):
    for i in range(len(vs)): edge_face.setdefault(frozenset((vs[i], vs[(i+1) % len(vs)])), []).append(f)
cyc0 = [[[g for g in edge_face[frozenset((vs[i], vs[(i+1) % len(vs)]))] if g != f][0] for i in range(len(vs))] for f, vs in enumerate(fv)]

def vert(f, g, h):
    """intersection of the three moving planes: x(t) = x0 + t x1"""
    A = mp.matrix([N[f], N[g], N[h]])
    if abs(mp.det(A)) < mp.mpf(10)**-25: return None
    x0 = mp.lu_solve(A, mp.matrix([Cf[f], Cf[g], Cf[h]])); x1 = mp.lu_solve(A, mp.matrix([1, 1, 1]))
    return [x0[i] for i in range(3)], [x1[i] for i in range(3)]

class Front:
    def __init__(s):
        s.cyc = {f: list(cyc0[f]) for f in range(NF)}; s.t = mp.mpf(0)
        s.sg = {}
        for f in range(NF):
            vs = fv[f]
            for i, g in enumerate(s.cyc[f]):
                a, b = M(V[vs[i]]), M(V[vs[(i+1) % len(vs)]])
                s.sg[(f, g)] = 1 if mdot([b[j]-a[j] for j in range(3)], mcross(N[f], N[g])) > 0 else -1
        # vertices of degree > 3 (TI vertices: 4 faces; apices: 5) -> fan of zero-length edges (degree-3 representation)
        for v in range(len(V)):
            ring = [f for f in range(NF) if v in fv[f]]
            if len(ring) <= 3: continue
            f0 = ring[0]; order = [f0]
            while len(order) < len(ring):
                f = order[-1]; i = fv[f].index(v); nxt = cyc0[f][i-1]
                order.append(nxt)
            d = len(order); F0 = order[0]
            c = s.cyc[F0]
            for j in range(len(c)):
                a, b = c[j], c[(j+1) % len(c)]
                if {a, b} == {order[1], order[-1]}:
                    mid = order[2:-1] if a == order[1] else order[-2:1:-1]
                    s.cyc[F0] = c[:j+1] + mid + c[j+1:]; break
            else: raise RuntimeError("fan F0")
            for k in range(2, d-1):
                cc = s.cyc[order[k]]
                for j in range(len(cc)):
                    if {cc[j], cc[(j+1) % len(cc)]} == {order[k-1], order[k+1]}: cc.insert(j+1, F0); break
                else: raise RuntimeError("fan Fk")
        s.check()
    def edge(s, f, i):
        c = s.cyc[f]; n = len(c); g = c[i]
        a = vert(f, c[i-1], g); b = vert(f, g, c[(i+1) % n])
        if a is None or b is None: return None
        u = unit(mcross(N[f], N[g])); t = s.t
        poly = [vert(f, c[k], c[(k+1) % n]) for k in range(n)]
        poly = [[p[0][j] + t*p[1][j] for j in range(3)] for p in poly if p is not None]
        cen = [sum(p[j] for p in poly)/len(poly) for j in range(3)]
        sg = 1 if mdot([cen[j] - a[0][j] - t*a[1][j] for j in range(3)], mcross(N[f], u)) > 0 else -1
        L0 = sg*mdot([b[0][j]-a[0][j] for j in range(3)], u); L1 = sg*mdot([b[1][j]-a[1][j] for j in range(3)], u)
        return L0, L1, a
    def edges(s):
        for f in s.cyc:
            for i, g in enumerate(s.cyc[f]):
                if f < g: yield f, i, g
    def flip(s, A, B, t):
        cA = s.cyc[A]; i = cA.index(B); Cc = cA[i-1]; D = cA[(i+1) % len(cA)]
        def insert(X, P1, P2, new):
            c = s.cyc[X]
            for j in range(len(c)):
                if {c[j], c[(j+1) % len(c)]} == {P1, P2}: c.insert(j+1, new); return
            raise RuntimeError(f"flip: {P1},{P2} not consecutive in face {X}")
        insert(Cc, A, B, D); insert(D, A, B, Cc)
        cA.remove(B); s.cyc[B].remove(A)
        for X in (A, B):
            if len(s.cyc[X]) < 3: s.kill(X)
        return (A, B, Cc, D)
    def kill(s, X):
        for P in set(s.cyc[X]):
            c = s.cyc[P]
            while X in c: c.remove(X)
            k = 0
            while k < len(c) and len(c) > 1:
                if c[k] == c[(k+1) % len(c)]: c.pop(k)
                else: k += 1
        del s.cyc[X]
    def check(s):
        for f, c in s.cyc.items():
            for i, g in enumerate(c):
                h = c[(i+1) % len(c)]
                cg = s.cyc[g]; j = cg.index(f)
                assert cg[j-1] == h, f"inconsistent vertex ({f},{g},{h})"

def simulate(t_end):
    F = Front(); t = mp.mpf(0); intervals = []; events = []
    while True:
        best = None
        for f, i, g in F.edges():
            e = F.edge(f, i)
            if e is None: continue
            L0, L1, a = e
            if L1 < -EPS:
                te = -L0/L1
                if te > t + EPS and (best is None or te < best): best = te
        tn = t_end if best is None or best > t_end else best
        intervals.append((t, tn, {f: list(c) for f, c in F.cyc.items()}, dict(F.sg)))
        if tn >= t_end: return intervals, events
        t = tn; F.t = t
        for rnd in range(1000):
            todo = []
            for f, i, g in F.edges():
                e = F.edge(f, i)
                if e is None: continue
                L0, L1, a = e; L = L0 + L1*t
                if abs(L) < mp.mpf(10)**-25 and L1 < -EPS: todo.append((f, g, [a[0][j]+t*a[1][j] for j in range(3)]))
                elif L < -mp.mpf(10)**-25: raise RuntimeError(f"negative edge {f}|{g} at t={t}")
            if not todo: break
            f, g, p = todo[0]
            if g in F.cyc.get(f, []):
                ev = F.flip(f, g, t); events.append(dict(t=t, faces=ev, point=p))
        else: raise RuntimeError("event resolution did not settle")
        F.check()

def run(lat, fac):
    from resin import vsc
    s0 = {"sc": Q(Fr(5, 2), Fr(3, 2)), "bcc": Q(Fr(10, 3), Fr(4, 3)), "fcc": Q(5, 2)}[lat]
    s = s0*fac
    Hs = []
    if lat in ("sc", "bcc"):
        for i in range(3):
            for sg in (1, -1):
                n = [0, 0, 0]; n[i] = sg; Hs.append((n, s*Fr(1, 2)))
    if lat == "bcc":
        for sg in itertools.product((1, -1), repeat=3): Hs.append((list(sg), s*Fr(3, 4)))
    if lat == "fcc":
        for i, j in ((0, 1), (1, 2), (0, 2)):
            for a, b in itertools.product((1, -1), repeat=2):
                n = [0, 0, 0]; n[i] = a; n[j] = b; Hs.append((n, s*Fr(1, 2)))
    Hm = [([mp.mpf(x) for x in n], c.mpf(), ("shell", k)) for k, (n, c) in enumerate(Hs)]
    cell = {"sc": 1, "bcc": mp.mpf(1)/2, "fcc": mp.mpf(1)/4}[lat]*s.mpf()**3
    volC1 = Q(35, Fr(25, 2)).mpf()
    # mould vertices -> t_end (arrival time <= distance to C1 <= |x|)
    mv = polytope([(n, c, l) for n, c, l in Hm], tol=mp.mpf(10)**-35, mpmode=True)["verts"]
    t_end = max(mp.sqrt(mdot(v, v)) for v in mv)
    intervals, events = simulate(t_end)
    pr(f"\n=== {lat} s = {fac} s0 = {float(s):.6f}: wavefront events up to t_end = {float(t_end):.4f}: {len(events)} flips in "
       f"{len(intervals)-1} event times: " + ", ".join(sorted({mp.nstr(e['t'], 10) for e in events})))
    def inside_mould(p, strict=True):
        return all(mdot(n, p) - c < (-EPS if strict else EPS) for n, c, l in Hm)
    for tt in sorted({mp.nstr(e["t"], 12) for e in events}):
        evs = [e for e in events if mp.nstr(e["t"], 12) == tt]
        kinds_ = sorted({tuple(faces[x][1] for x in e["faces"]) for e in evs})
        nin = sum(1 for e in evs if inside_mould(e["point"]))
        pr(f"   t = {tt}: {len(evs)} flips (A|B part, C|D meet) types {kinds_}; event points inside the mould: {nin}")
    slabs = []   # (face, k, H, P)
    nfail = [0]
    for k, (t0, t1, cyc, sg) in enumerate(intervals):
        for f, c in cyc.items():
            H = [([-x for x in N[f]], -(Cf[f] + t0), ("bottom" if k == 0 else "tk", f)),
                 (list(N[f]), Cf[f] + t1, ("tk", f))]
            tm = (t0 + t1)/2; poly = []
            for i in range(len(c)):
                X = vert(f, c[i], c[(i+1) % len(c)])
                if X is not None: poly.append([X[0][j] + tm*X[1][j] for j in range(3)])
            cen = [sum(p[j] for p in poly)/len(poly) for j in range(3)]
            for ig, g in enumerate(c):
                A_ = vert(f, c[ig-1], g); B_ = vert(f, g, c[(ig+1) % len(c)])
                if A_ is not None and B_ is not None:
                    dd = [(B_[0][j] - A_[0][j]) + tm*(B_[1][j] - A_[1][j]) for j in range(3)]
                    if mp.sqrt(mdot(dd, dd)) < mp.mpf(10)**-25: continue      # zero-length edge in this interval: no wall
                val = mdot([N[f][j]-N[g][j] for j in range(3)], cen) - (Cf[f]-Cf[g])
                if abs(val) < mp.mpf(10)**-25: continue
                sig = 1 if val > 0 else -1
                # inside: sig*(d_f - d_g) >= 0  <=>  -sig*(N_f - N_g).x <= -sig*(C_f - C_g)
                H.append(([-sig*(N[f][j]-N[g][j]) for j in range(3)], -sig*(Cf[f]-Cf[g]), ("lat", g)))
            H += Hm
            try:
                P = polytope(H, tol=mp.mpf(10)**-35, mpmode=True)
            except (AssertionError, ValueError, ZeroDivisionError, IndexError) as ex:
                P = None; nfail[0] += 1
            if P is None or len(P["verts"]) < 4 or P["vol"] < mp.mpf(10)**-35: continue
            slabs.append((f, k, H, P))
    total = sum(P["vol"] for f, k, H, P in slabs)
    gap = total - (cell - volC1)
    # overlaps
    def hrep(H):
        A_ = np.array([[float(x) for x in h[0]] for h in H]); b_ = np.array([float(h[1]) for h in H])
        L = np.linalg.norm(A_, axis=1); return A_/L[:, None], b_/L
    def depth(P1, P2):
        A_ = np.vstack([P1[0], P2[0]]); b_ = np.concatenate([P1[1], P2[1]])
        r = linprog([0, 0, 0, -1], A_ub=np.hstack([A_, np.ones((len(A_), 1))]), b_ub=b_, bounds=[(None, None)]*3 + [(None, 10)], method="highs")
        return -r.fun if r.status == 0 else -1.0
    HR = [hrep(H) for f, k, H, P in slabs]
    BB = [(np.array([[float(x) for x in v] for v in P["verts"]]).min(0), np.array([[float(x) for x in v] for v in P["verts"]]).max(0)) for f, k, H, P in slabs]
    worst = -1.0; npairs = 0
    for i, j in itertools.combinations(range(len(slabs)), 2):
        if slabs[i][0] == slabs[j][0]: continue
        if np.any(BB[i][1] < BB[j][0] - 1e-9) or np.any(BB[j][1] < BB[i][0] - 1e-9): continue
        npairs += 1; worst = max(worst, depth(HR[i], HR[j]))
    # C1 parts: TI and 12 pyramids
    parts = []
    dirs = np.array([tofl(d) for d in C["hd"] + C["pd"]]); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    TVf = np.array([tofl(v) for v in C["TV"]]); bti = np.array([max(d @ v for v in TVf) for d in dirs]); parts.append((dirs, bti))
    for p in range(12):
        rows = [(-dirs[20+p], -bti[20+p])] + [(tofl(planes[fi][0])/np.linalg.norm(tofl(planes[fi][0])), float(planes[fi][1])/np.linalg.norm(tofl(planes[fi][0]))) for fi in range(20+5*p, 25+5*p)]
        parts.append((np.array([r[0] for r in rows]), np.array([r[1] for r in rows])))
    worstC = max(depth(h, q) for h in HR for q in parts)
    valid = abs(gap) < mp.mpf(10)**-30 and worst < 1e-9 and worstC < 1e-9
    pr(f"   slabs {len(slabs)} (empty or degenerate slabs dropped: {nfail[0]}); volume sum - (mould - C1) = {mp.nstr(gap, 5)}; overlap depth slab/slab max {worst:.3g} over {npairs} pairs; "
       f"slab/C1 max {worstC:.3g}  => {'VALID division' if valid else 'NOT valid'}")
    # pieces per face, kinds by T_h orbit + congruence
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
        pts = []
        for k, H, P in mine:
            for v in P["verts"]:
                fl = np.array([float(x) for x in v])
                if not any(np.linalg.norm(fl - q) < 1e-9 for q in pts): pts.append(fl)
        vol = sum(P["vol"] for k, H, P in mine)
        # faces of the union: distinct bounding planes (bottom, walls by neighbour, mould facets) carrying a slab face
        planes_ = set()
        angs = {}
        for k, H, P in mine:
            for t_ in P["faces"]:
                lab = H[t_][2]
                if lab[0] == "tk": continue
                planes_.add((lab[0], lab[1]))
            for a, b in itertools.combinations(P["faces"], 2):
                if len(set(P["faces"][a]) & set(P["faces"][b])) < 2: continue
                la, lb = H[a][2][0], H[b][2][0]
                if "tk" in (la, lb): continue
                n1, n2 = H[a][0], H[b][0]
                th = mp.acos(-mdot(n1, n2)/mp.sqrt(mdot(n1, n1)*mdot(n2, n2)))
                key = mp.nstr(th*180/mp.pi, 12)
                angs.setdefault(key, dict(deg=float(th*180/mp.pi), pair=f"{la}|{lb}", basis=None, th=th))
        for a in angs.values(): a["basis"] = ident(a.pop("th"))
        nb0 = sorted(cyc0[f])
        ev_in = [e for e in events if f in e["faces"] and inside_mould(e["point"])]
        wallset = {x[1] for x in planes_ if x[0] == "lat"}
        realev = [e for e in ev_in if (f in e["faces"][:2] and e["faces"][1-e["faces"].index(f)] in wallset)
                  or (f in e["faces"][2:] and e["faces"][5-e["faces"].index(f)] in wallset)]
        lost = sorted({e["faces"][1-e["faces"].index(f)] for e in realev if f in e["faces"][:2]})
        gained = sorted({e["faces"][5-e["faces"].index(f)] for e in realev if f in e["faces"][2:]})
        ev_in = realev   # flips of zero-length (virtual) edges at the degree-4/5 vertices are not counted
        rec = dict(face=f, kind=faces[f][1], orbit=len(o), vol=float(vol), nV_points=len(pts), n_planes=len(planes_),
                   walls=sorted(x[1] for x in planes_ if x[0] == "lat"), mould_facets=sum(1 for x in planes_ if x[0] == "shell"),
                   nb_C1_side=nb0, lost_inside=lost, gained_inside=gained, Y=len(ev_in), scutoid=len(ev_in) > 0,
                   angles=sorted(angs.values(), key=lambda a: a["deg"]), pts=[list(p) for p in pts])
        for kd in kinds:
            if abs(kd["vol"] - rec["vol"]) < 1e-9 and congruent(np.array(kd["pts"]), np.array(rec["pts"])):
                kd["members"].append(f); break
        else:
            rec["members"] = [f]; kinds.append(rec)
    for kd in kinds:
        pr(f"   kind {kd['kind']} face {kd['face']} ({kd['orbit']} per cell; merged {kd['members']}): planes {kd['n_planes']} "
           f"(walls to {kd['walls']}, mould facets {kd['mould_facets']}), points {kd['nV_points']}, vol {kd['vol']:.6f}; C1-side neighbours "
           f"{kd['nb_C1_side']}; inside the mould loses {kd['lost_inside']} gains {kd['gained_inside']}; Y events {kd['Y']} scutoid {kd['scutoid']}")
        pr("      dihedrals: " + "; ".join(f"{a['deg']:.4f} {a['pair']} [{a['basis'] or 'not in basis'}]" for a in kd["angles"]))
    pr(f"   SUMMARY {lat} x{fac}: valid {valid}; kinds {len(kinds)}; scutoid kinds {sum(1 for k in kinds if k['scutoid'])}")
    return dict(lattice=lat, factor=str(fac), s=float(s), events=[dict(t=float(e["t"]), faces=e["faces"], point=[float(x) for x in e["point"]],
                inside=inside_mould(e["point"])) for e in events], volume_gap=mp.nstr(gap, 8), overlap=worst, overlapC1=worstC, valid=valid,
                kinds=[{k: v for k, v in kd.items()} for kd in kinds])

if __name__ == "__main__":
    out = []; args = sys.argv[2:]
    for lat, fac in zip(args[::2], args[1::2]): out.append(run(lat, Fr(fac)))
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
    ok = all(r["valid"] for r in out)
    pr("FINAL ok" if ok else "FINAL FAIL: " + ", ".join(f"{r['lattice']} x{r['factor']} valid={r['valid']}" for r in out))
