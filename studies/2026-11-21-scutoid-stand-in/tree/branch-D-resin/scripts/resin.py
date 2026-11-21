"""Branch D, DICTO's "resin solution" (21 Nov 2026).
Mould = Voronoi cell of a cubic lattice (sc cube, bcc truncated octahedron, fcc rhombic dodecahedron) with C1 at every lattice point,
C1's T_h axes on the cube axes (standard coordinates: TI vertices = cyclic permutations of (0,1,3phi)/2, (1,2+phi,2phi)/2, (phi,2,2phi+1)/2
with all signs; the cyclic-permutation x sign group of order 24 is T_h).  Resin = cell minus C1, divided face by face.

Division rules (both give convex, flat-faced pieces, one per C1 face, 80 per cell):
 R1 "central": piece(F) = cell  cap  {in front of F's plane}  cap  cone from C1's centre over F.  Exact in Q(sqrt5).
    Valid partition because C1 is star-shaped from its centre with every face plane at positive offset (checked exactly);
    lateral faces are planes through the centre and an edge of F.
 R2 "normal / mitre": piece(F) = cell cap {in front of F} cap, for each edge e = F|G, the side of the dihedral bisector plane of e that
    holds F (the mitred offset of F along its normal, DICTO's "segments along face normals" with bisector walls).  Bisectors between a
    hexagon and a spike triangle carry sqrt3, so R2 runs at 50 digits (mpmath), margins printed; it is a partition only if the
    checks (volume sum, no overlaps) pass.
Usage: python resin.py  (writes ../data/resin.json, prints the log)."""
import itertools, json, math, sys
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
from scipy.optimize import linprog
mp.mp.dps = 50
def pr(*a): print(*a, flush=True)

# ---------------- exact Q(sqrt5) ----------------
class Q:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0):
        s.a = a if isinstance(a, Fr) else Fr(a); s.b = b if isinstance(b, Fr) else Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return (-s) + o
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = o if isinstance(o, Q) else Q(o); n = o.a*o.a - 5*o.b*o.b
        return Q((s.a*o.a - 5*s.b*o.b)/n, (s.b*o.a - s.a*o.b)/n)
    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0: return 0 if (a == 0 and b == 0) else 1
        if a <= 0 and b <= 0: return -1
        d = a*a - 5*b*b
        return (1 if d > 0 else -1 if d < 0 else 0) * (1 if a > 0 else -1)
    def __float__(s): return float(s.a) + float(s.b)*math.sqrt(5)
    def mpf(s): return mp.mpf(s.a.numerator)/s.a.denominator + mp.mpf(s.b.numerator)/s.b.denominator*mp.sqrt(5)
    def key(s): return (s.a, s.b)
    def __repr__(s): return f"{s.a}+{s.b}r5" if s.b else f"{s.a}"
PHI = Q(Fr(1, 2), Fr(1, 2))
def vadd(u, v): return [u[i] + v[i] for i in range(3)]
def vsub(u, v): return [u[i] - v[i] for i in range(3)]
def vsc(k, u): return [k*u[i] for i in range(3)]
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def cross(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
def det3(a, b, c): return dot(a, cross(b, c))
def sgn(x, tol=None):
    if hasattr(x, "sign"): return x.sign()
    return 0 if abs(x) < tol else (1 if x > 0 else -1)
def tofl(u): return np.array([float(x) for x in u])

# ---------------- C1 exact ----------------
def build_C1():
    TV = []
    seen = set()
    for b in [(Q(0), Q(1), 3*PHI), (Q(1), 2+PHI, 2*PHI), (PHI, Q(2), 2*PHI+1)]:
        for sg in itertools.product((1, -1), repeat=3):
            t = [b[i]*Fr(sg[i], 2) for i in range(3)]
            for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
                k = tuple(x.key() for x in c)
                if k not in seen: seen.add(k); TV.append(c)
    assert len(TV) == 60
    one = Q(1)
    d2 = lambda i, j: dot(vsub(TV[i], TV[j]), vsub(TV[i], TV[j]))
    nb = {i: [j for j in range(60) if j != i and (d2(i, j) - one).sign() == 0] for i in range(60)}
    assert all(len(v) == 3 for v in nb.values())
    # faces of the TI: directions
    pd = []
    for a, b in itertools.product((1, -1), repeat=2):
        t = [Q(0), Q(a), PHI*b]
        pd += [[t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]]
    hd = [[Q(a), Q(b), Q(c)] for a, b, c in itertools.product((1, -1), repeat=3)]
    for a, b in itertools.product((1, -1), repeat=2):
        t = [Q(0), PHI*a, (PHI-1)*b]
        hd += [[t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]]
    def face(d):
        vals = [dot(d, v) for v in TV]; m = vals[0]
        for x in vals:
            if (x - m).sign() > 0: m = x
        idx = [i for i in range(60) if (vals[i] - m).sign() == 0]
        # order cyclically along edges
        cyc = [idx[0]]
        while len(cyc) < len(idx):
            nxt = [j for j in nb[cyc[-1]] if j in idx and j not in cyc]
            cyc.append(nxt[0])
        return cyc
    pents = [face(d) for d in pd]; hexes = [face(d) for d in hd]
    assert all(len(f) == 5 for f in pents) and all(len(f) == 6 for f in hexes)
    # apex: on the 5-fold axis d at k*d with k = (5+sqrt5)/4; check every lateral edge = dodecahedron circumradius sqrt3 phi/2
    k = Q(Fr(5, 4), Fr(1, 4)); R2 = 3*PHI*PHI/4
    apex = []
    for d, f in zip(pd, pents):
        A = vsc(k, d)
        for i in f: assert (dot(vsub(A, TV[i]), vsub(A, TV[i])) - R2).sign() == 0
        apex.append(A)
    V = TV + apex                         # indices 60..71 = apices
    faces = []                            # (vertex index list, kind)
    for f in hexes: faces.append((f, "hex"))
    for p, f in enumerate(pents):
        for i in range(5): faces.append(([f[i], f[(i+1) % 5], 60+p], "tri"))
    # outward planes n.x = c with n exact; inner test point
    planes = []
    for f, kind in faces:
        P = [V[i] for i in f]
        n = cross(vsub(P[1], P[0]), vsub(P[2], P[0]))
        if kind == "hex": inner = [Q(0)]*3
        else:
            p = f[2] - 60; cp = [sum((TV[i][j] for i in pents[p]), Q(0))*Fr(1, 5) for j in range(3)]
            inner = vsc(Fr(1, 2), vadd(cp, apex[p]))
        if dot(n, vsub(inner, P[0])).sign() > 0: n = vsc(-1, n)
        planes.append((n, dot(n, P[0])))
    return dict(V=V, TV=TV, apex=apex, faces=faces, planes=planes, pents=pents, hexes=hexes, pd=pd, hd=hd)

# T_h: x -> cyclic permutation then signs (24 elements)
TH = [(c, s) for c in range(3) for s in itertools.product((1, -1), repeat=3)]
def act(g, x):
    c, s = g; y = [x[(i - c) % 3] for i in range(3)]
    return [y[i]*s[i] for i in range(3)]

# ---------------- polytope from halfspaces n.x <= c ----------------
def polytope(H, tol=None, mpmode=False):
    """H: list of (n, c, label). Returns dict with vertices (field), incidences, faces, volume (field)."""
    m = len(H)
    Nf = np.array([tofl(h[0]) if not mpmode else np.array([float(x) for x in h[0]]) for h in H])
    cf = np.array([float(h[1]) for h in H])
    scale = np.linalg.norm(Nf, axis=1)
    pts = []
    for i, j, k in itertools.combinations(range(m), 3):
        M = Nf[[i, j, k]]
        if abs(np.linalg.det(M)) < 1e-10*scale[i]*scale[j]*scale[k]: continue
        x = np.linalg.solve(M, cf[[i, j, k]])
        if np.all(Nf @ x <= cf + 1e-7*scale):
            if not any(np.linalg.norm(x - p[0]) < 1e-6 for p in pts): pts.append((x, (i, j, k)))
    verts, inc = [], []
    for x, (i, j, k) in pts:
        a, b, c = H[i][0], H[j][0], H[k][0]
        D = det3(a, b, c)
        cx = cross(b, c); cy = cross(c, a); cz = cross(a, b)
        X = [(H[i][1]*cx[t] + H[j][1]*cy[t] + H[k][1]*cz[t])/D for t in range(3)]
        s_ = [sgn(dot(h[0], X) - h[1], tol) for h in H]
        assert max(s_) <= 0, "float vertex not feasible in exact check"
        verts.append(X); inc.append(frozenset(t for t in range(m) if s_[t] == 0))
    faces = {}
    for t in range(m):
        vs = [v for v in range(len(verts)) if t in inc[v]]
        if len(vs) >= 3: faces[t] = vs
    # merge duplicate planes (same vertex set)
    seenv = {}
    for t in sorted(faces):
        key = frozenset(faces[t])
        if key in seenv: del faces[t]
        else: seenv[key] = t
    # order face vertices, exact volume
    c0 = [sum((v[i] for v in verts), verts[0][i]*0)/len(verts) for i in range(3)]
    vol = 0
    fl = [tofl(v) if not mpmode else np.array([float(x) for x in v]) for v in verts]
    for t, vs in faces.items():
        n = Nf[t]; cen = sum(fl[v] for v in vs)/len(vs)
        u = fl[vs[0]] - cen; u /= np.linalg.norm(u); w = np.cross(n/np.linalg.norm(n), u)
        vs.sort(key=lambda v: math.atan2(np.dot(fl[v]-cen, w), np.dot(fl[v]-cen, u)))
        for q in range(1, len(vs) - 1):
            d = det3(vsub(verts[vs[0]], c0), vsub(verts[vs[q]], c0), vsub(verts[vs[q+1]], c0))
            vol = vol + (d if sgn(d, tol) >= 0 else -d)
    vol = vol/6
    nE = sum(1 for a, b in itertools.combinations(faces, 2) if len(set(faces[a]) & set(faces[b])) >= 2)
    assert len(verts) - nE + len(faces) == 2, "Euler fails"
    return dict(verts=verts, inc=inc, faces=faces, vol=vol, nE=nE)

PIm = mp.pi; ALm = mp.atan((1+mp.sqrt(5))/2); BEm = mp.acos(1/mp.sqrt(6)); GAm = mp.acos(mp.sqrt(mp.mpf(2)/3))
LAMBDA = mp.pi - mp.acos(mp.sqrt(7 + 3*mp.sqrt(5))/4)
def ident(theta):
    """basis pi, alpha, beta, gamma; if that fails, the same plus lambda* = 157.7612 deg (marked)"""
    for B, names in (([PIm, ALm, BEm, GAm], ["pi", "alpha", "beta", "gamma"]), ([PIm, ALm, BEm, GAm, LAMBDA], ["pi", "alpha", "beta", "gamma", "LAMBDA"])):
        r = mp.pslq([theta] + B, maxcoeff=48, maxsteps=20000)
        if r is not None and r[0] != 0: break
    else: return None
    terms = [f"{Fr(-r[i+1], r[0])}{names[i]}" for i in range(len(names)) if r[i+1] != 0]
    return " + ".join(terms) if terms else "0"

def analyse(P, H, mpmode):
    """faces labelled bottom / top(shell) / lat(edge); dihedrals; scutoid data"""
    tol = mp.mpf(10)**-35 if mpmode else None
    lab = {t: H[t][2] for t in P["faces"]}
    bottom = [t for t in lab if lab[t][0] == "bottom"]
    top = [t for t in lab if lab[t][0] == "shell"]
    lat = [t for t in lab if lab[t][0] == "lat"]
    fs = {t: set(P["faces"][t]) for t in P["faces"]}
    def adj(a, b): return len(fs[a] & fs[b]) >= 2
    nb_bottom = sorted(lab[t][1] for t in lat if any(adj(t, b) for b in bottom))
    nb_top = sorted(lab[t][1] for t in lat if any(adj(t, b) for b in top))
    onplanes = set().union(*[fs[t] for t in bottom + top]) if bottom + top else set()
    yv = [v for v in range(len(P["verts"])) if v not in onplanes and sum(1 for t in lat if v in fs[t]) >= 3]
    dih = []
    for a, b in itertools.combinations(P["faces"], 2):
        if not adj(a, b): continue
        n1, n2 = H[a][0], H[b][0]
        if mpmode:
            c = -mp.fdot(n1, n2)/mp.sqrt(mp.fdot(n1, n1)*mp.fdot(n2, n2))
        else:
            c = -(dot(n1, n2)).mpf()/mp.sqrt((dot(n1, n1)*dot(n2, n2)).mpf())
        th = mp.acos(c)
        dih.append((lab[a][0], lab[b][0], th))
    angs = {}
    for la, lb, th in dih:
        key = mp.nstr(th*180/mp.pi, 12)
        if key not in angs: angs[key] = dict(deg=float(th*180/mp.pi), pair=f"{la}|{lb}", basis=ident(th), lam=bool(abs(th-LAMBDA) < mp.mpf(10)**-30))
    return dict(nV=len(P["verts"]), nF=len(P["faces"]), nE=P["nE"], face_sizes=sorted(len(v) for v in P["faces"].values()),
                n_bottom=len(bottom), n_top=len(top), n_lat=len(lat), nb_bottom=nb_bottom, nb_top=nb_top, Y=len(yv),
                scutoid=bool(yv) and bool(top) and nb_bottom != nb_top, reaches_shell=bool(top),
                angles=sorted(angs.values(), key=lambda a: a["deg"]))

def main():
    C = build_C1(); V, faces, planes = C["V"], C["faces"], C["planes"]
    pr("C1: 60 TI vertices + 12 apices at ((5+sqrt5)/4)(0,1,phi) etc. (exact; lateral edges = sqrt3 phi/2 checked)")
    assert all(c.sign() > 0 for n, c in planes)
    pr("star check: all 80 face planes at positive offset from the centre (exact) -> R1 cones partition space outside C1")
    # C1 volume exact: cones from centre
    volC1 = Q(0)
    for (f, kind), (n, c) in zip(faces, planes):
        P = [V[i] for i in f]
        for q in range(1, len(P) - 1):
            d = det3(P[0], P[q], P[q+1]); volC1 = volC1 + (d if d.sign() > 0 else -d)
    volC1 = volC1/6
    pr(f"vol C1 = {volC1} = {float(volC1):.10f}")
    # face neighbours across each edge
    edge_face = {}
    for fi, (f, kind) in enumerate(faces):
        for i in range(len(f)): edge_face.setdefault(frozenset((f[i], f[(i+1) % len(f)])), []).append(fi)
    assert all(len(v) == 2 for v in edge_face.values()) and len(edge_face) == 150
    # T_h orbits of faces
    keyv = {tuple(x.key() for x in v): i for i, v in enumerate(V)}
    def gface(g, fi): return frozenset(keyv[tuple(x.key() for x in act(g, V[i]))] for i in faces[fi][0])
    fid = {frozenset(f): i for i, (f, k) in enumerate(faces)}
    orbits, done = [], set()
    for fi in range(80):
        if fi in done: continue
        orb = sorted({fid[gface(g, fi)] for g in TH}); done |= set(orb); orbits.append(orb)
    pr("T_h face orbits:", [(faces[o[0]][1], len(o)) for o in orbits])
    # lattices
    def shell(lat, s):
        H = []
        if lat in ("sc", "bcc"):
            for i in range(3):
                for sg in (1, -1):
                    n = [Q(0)]*3; n[i] = Q(sg); H.append((n, s*Fr(1, 2), ("shell", f"e{i}{'+' if sg > 0 else '-'}")))
        if lat == "bcc":
            for sg in itertools.product((1, -1), repeat=3): H.append(([Q(x) for x in sg], s*Fr(3, 4), ("shell", f"111{sg}")))
        if lat == "fcc":
            for i, j in ((0, 1), (1, 2), (0, 2)):
                for a, b in itertools.product((1, -1), repeat=2):
                    n = [Q(0)]*3; n[i] = Q(a); n[j] = Q(b); H.append((n, s*Fr(1, 2), ("shell", f"{i}{j}{a}{b}")))
        return H
    cellvol = {"sc": Fr(1), "bcc": Fr(1, 2), "fcc": Fr(1, 4)}
    out = dict(volC1=str(volC1), arrangements=[])
    for lat in ("sc", "bcc", "fcc"):
        H0 = shell(lat, Q(1))
        smin = None
        for n, c, _ in H0:
            for v in V:
                r = dot(n, v)/c
                if smin is None or (r - smin).sign() > 0: smin = r
        pr(f"\n=== {lat}: smallest scale with C1 inside the Voronoi cell s0 = {smin} = {float(smin):.6f} (cube edge of the lattice)")
        for fac in (Fr(1), Fr(6, 5), Fr(3, 2)):
            s = smin*fac
            Hs = shell(lat, s)
            volres = s*s*s*cellvol[lat] - volC1
            for rule in ("R1", "R2"):
                mpmode = rule == "R2"
                tol = mp.mpf(10)**-35 if mpmode else None
                def piece_H(fi, floats=False):
                    f, kind = faces[fi]; n, c = planes[fi]
                    if not mpmode:
                        H = [(vsc(-1, n), -c, ("bottom", fi))]
                        cen = [sum((V[i][j] for i in f), Q(0))/len(f) for j in range(3)]
                        for i in range(len(f)):
                            a, b = V[f[i]], V[f[(i+1) % len(f)]]
                            m = cross(a, b)
                            if dot(m, cen).sign() < 0: m = vsc(-1, m)
                            G = [g for g in edge_face[frozenset((f[i], f[(i+1) % len(f)]))] if g != fi][0]
                            H.append((vsc(-1, m), Q(0), ("lat", G)))
                        return H + Hs
                    # R2 at 50 digits
                    def um(u): u = [x.mpf() for x in u]; L = mp.sqrt(mp.fdot(u, u)); return [x/L for x in u]
                    nf = um(n); cF = mp.fdot(nf, [x.mpf() for x in V[f[0]]])
                    H = [([-x for x in nf], -cF, ("bottom", fi))]
                    cen = [sum((V[i][j] for i in f), Q(0)).mpf()/len(f) for j in range(3)]
                    for i in range(len(f)):
                        e = frozenset((f[i], f[(i+1) % len(f)]))
                        G = [g for g in edge_face[e] if g != fi][0]
                        ng = um(planes[G][0]); m = [nf[t] - ng[t] for t in range(3)]
                        p0 = [x.mpf() for x in V[f[i]]]; cm = mp.fdot(m, p0)
                        if mp.fdot(m, cen) - cm < 0: m = [-x for x in m]; cm = -cm
                        H.append(([-x for x in m], -cm, ("lat", G)))
                    return H + [([x.mpf() for x in hn], hc.mpf(), hl) for hn, hc, hl in Hs]
                reps = []
                total = 0
                for orb in orbits:
                    H = piece_H(orb[0])
                    P = polytope(H, tol=tol, mpmode=mpmode)
                    A = analyse(P, H, mpmode)
                    vol = P["vol"]
                    total = total + vol*len(orb)
                    fl = np.array([[float(x) for x in v] for v in P["verts"]])
                    d2 = sorted(round(float(np.dot(a-b, a-b)), 9) for a, b in itertools.combinations(fl, 2))
                    reps.append(dict(face=orb[0], kind=faces[orb[0]][1], orbit=len(orb), vol=float(vol), volx=str(vol) if not mpmode else mp.nstr(vol, 30),
                                     verts=[[float(x) for x in v] for v in P["verts"]], d2=d2, **A))
                gap = (total - volres) if not mpmode else total - volres.mpf()
                ok_vol = (gap.sign() == 0) if not mpmode else abs(gap) < mp.mpf(10)**-30
                # overlap checks (float LP): all 80 pieces pairwise, and against C1 parts
                Hall = []
                for fi in range(80):
                    H = piece_H(fi)
                    A_ = np.array([[float(x) for x in h[0]] for h in H]); b_ = np.array([float(h[1]) for h in H])
                    L = np.linalg.norm(A_, axis=1); Hall.append((A_/L[:, None], b_/L))
                parts = []
                TIn = [planes[i] for i in range(20)]
                Ati = [];
                for d in C["hd"] + C["pd"]:
                    df = tofl(d); df /= np.linalg.norm(df); Ati.append(df)
                Ati = np.array(Ati); bti = np.array([max(np.dot(a, tofl(v)) for v in C["TV"]) for a in Ati]); parts.append((Ati, bti))
                for p in range(12):
                    rows = [(-np.array(Ati[20+p]), -bti[20+p])]
                    for fi in range(20 + 5*p, 25 + 5*p):
                        nn = tofl(planes[fi][0]); L = np.linalg.norm(nn); rows.append((nn/L, float(planes[fi][1])/L))
                    parts.append((np.array([r[0] for r in rows]), np.array([r[1] for r in rows])))
                def depth(P1, P2):
                    A_ = np.vstack([P1[0], P2[0]]); b_ = np.concatenate([P1[1], P2[1]])
                    A2 = np.hstack([A_, np.ones((len(A_), 1))])
                    r = linprog([0, 0, 0, -1], A_ub=A2, b_ub=b_, bounds=[(None, None)]*3 + [(None, 10)], method="highs")
                    return -r.fun if r.status == 0 else -1.0
                worst_pp = max(depth(Hall[i], Hall[j]) for i, j in itertools.combinations(range(80), 2))
                worst_pc = max(depth(Hall[i], q) for i in range(80) for q in parts)
                ok_part = ok_vol and worst_pp < 1e-7 and worst_pc < 1e-7
                pr(f"-- {lat} s = {fac} s0 = {float(s):.6f}  rule {rule}: volume sum - resin = {mp.nstr(gap if mpmode else gap.mpf(), 5)} "
                   f"({'exact 0' if (not mpmode and ok_vol) else ('|gap|<1e-30' if ok_vol else 'NONZERO')}); max overlap depth piece/piece {worst_pp:.3g}, "
                   f"piece/C1 {worst_pc:.3g}  => {'PARTITION' if ok_part else 'NOT a partition'}")
                # kinds up to congruence (orbit reps; congruence by distance multiset + volume, then isometry search)
                kinds = []
                for r in reps:
                    for k in kinds:
                        if k["d2"] == r["d2"] and abs(k["vol"] - r["vol"]) < 1e-9 and congruent(np.array(k["verts"]), np.array(r["verts"])):
                            k["members"].append(r["face"]); break
                    else:
                        kinds.append(dict(r, members=[r["face"]]))
                for k in kinds:
                    pr(f"   kind {k['kind']} face {k['face']} (orbits merged {k['members']}, {sum(len(o) for o in orbits if o[0] in k['members'])} per cell): "
                       f"F={k['nF']} V={k['nV']} E={k['nE']} faces {k['face_sizes']} top facets {k['n_top']} lateral {k['n_lat']} "
                       f"neighbours C1-side {k['nb_bottom']} shell-side {k['nb_top']} Y={k['Y']} scutoid={k['scutoid']} vol={k['vol']:.6f}")
                    pr("      dihedrals: " + "; ".join(f"{a['deg']:.4f} {a['pair']} [{a['basis'] or 'not in basis'}]" + (" LAMBDA*" if a['lam'] else "") for a in k["angles"]))
                rec = dict(lattice=lat, scale_factor=str(fac), s=float(s), sx=str(s), rule=rule, volume_gap=mp.nstr(gap if mpmode else gap.mpf(), 8),
                           overlap_pp=worst_pp, overlap_pc=worst_pc, partition=ok_part, n_kinds=len(kinds),
                           n_scutoid_kinds=sum(1 for k in kinds if k["scutoid"]),
                           all_angles_in_basis=all(a["basis"] and "LAMBDA" not in a["basis"] for k in kinds for a in k["angles"]),
                           angles_in_basis_with_lambda=all(a["basis"] for k in kinds for a in k["angles"]),
                           lambda_shifted_present=any(a["basis"] and "LAMBDA" in a["basis"] for k in kinds for a in k["angles"]),
                           lambda_present=any(a["lam"] for k in kinds for a in k["angles"]),
                           kinds=[{x: k[x] for x in k if x not in ("d2",)} for k in kinds])
                out["arrangements"].append(rec)
                pr(f"   SUMMARY {lat} x{fac} {rule}: kinds {len(kinds)}, scutoid kinds {rec['n_scutoid_kinds']}, all dihedrals in basis {rec['all_angles_in_basis']} (with lambda* added {rec['angles_in_basis_with_lambda']}), "
                   f"157.7612 present {rec['lambda_present']}, partition {ok_part}")
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "resin.json", "w"), indent=1, default=str)
    okR1 = all(a["partition"] and a["volume_gap"].strip() in ("0", "0.0") for a in out["arrangements"] if a["rule"] == "R1")
    pr("FINAL ok" if okR1 else "FINAL FAIL: an R1 division is not an exact partition")

def congruent(A, B):
    """isometry (proper or improper) mapping vertex set A onto B, float search"""
    if len(A) != len(B): return False
    cA, cB = A.mean(0), B.mean(0); A0, B0 = A - cA, B - cB
    # pick 3 independent vertices of A
    idx = [0]
    for i in range(1, len(A)):
        M = A0[idx + [i]]
        if np.linalg.matrix_rank(M, 1e-8) == len(idx) + 1: idx.append(i)
        if len(idx) == 3: break
    dA = lambda i, j: np.dot(A0[i]-A0[j], A0[i]-A0[j])
    for t in itertools.permutations(range(len(B)), 3):
        if any(abs(np.dot(A0[idx[a]], A0[idx[a]]) - np.dot(B0[t[a]], B0[t[a]])) > 1e-7 for a in range(3)): continue
        R = np.linalg.solve(A0[idx], B0[list(t)]).T
        if np.abs(R.T @ R - np.eye(3)).max() > 1e-7: continue
        M = (R @ A0.T).T
        if all(np.min(np.linalg.norm(B0 - m, axis=1)) < 1e-7 for m in M): return True
    return False

if __name__ == "__main__":
    main()
