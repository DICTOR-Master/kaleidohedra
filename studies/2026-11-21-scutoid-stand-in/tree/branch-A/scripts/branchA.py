"""Branch A (hexagon = end face).  C1 and C1' share hexagon H (types swapped, B2).  H2 = the C1 hexagon across the C1 hh edge e of H.
K sits on H2 (outside C1), its lateral face over e is the C1' spike triangle Delta_e (20.91 deg to H2, lemma FORCED of the proper round).
Part 1: exact frame + forced data.  Part 2: classic scutoid combinatorics with Delta_e as the Y-triangle (apex P = Y vertex):
the faces at the two top edges next to e must contain P, so their tilt is forced; the other three top-edge tilts are taken from the
ring-closing alphabet; score checks (1)-(4).  Run: python branchA.py   (writes ../data/branchA.json)"""
import itertools, json, sys
from fractions import Fraction as F
import mpmath as mp
sys.path.insert(0, __import__('os').path.dirname(__file__))
from geom import *
out = {'checks': []}; OK = True
def pr(s): print(s, flush=True)
def score(name, c):
    pr(f"  [score {'pass' if c else 'FAIL'}] {name}"); out.setdefault('score', []).append([name, bool(c)])
def chk(name, c):
    global OK
    OK = OK and bool(c); pr(f"  [{'pass' if c else 'FAIL'}] {name}"); out['checks'].append([name, bool(c)])
deg = lambda x: float(x*180/mp.pi)
PI = mp.pi
def ident(th):
    """th = p*pi + b*beta with b in -2..2, p = k/24 ? (match at 1e-35, 50 digits)"""
    for b in (0, 1, -1, 2, -2):
        q = (th - b*BETA)/PI*24
        k = mp.nint(q)
        if abs(q - k) < TOL: return (F(int(k), 24), b)
    return None
val = lambda pb: pb[0]*PI + pb[1]*BETA
ALPH = [(F(k, 4), b) for b in (1, -1) for k in range(-4, 12)] + [(F(k, 12), 0) for k in range(1, 24) if k != 12]
ALPH = [a for a in ALPH if 0 < val(a) < 2*PI and abs(val(a) - PI) > TOL]
CONV = [a for a in ALPH if val(a) < PI]
hh, r, s = (F(3, 2), -2), (F(3, 4), 1), (F(2, 3), 0)
pr("== part 1: frame")
C = build_C1()
H = C['hexes'][0]
H2 = [h for h in C['hexes'][1:] if sum(any(same(u, v) for v in H) for u in h) == 2][0]
Ae, Be = [u for u in H2 if any(same(u, v) for v in H)]
img = iso_swap(H)
C1p_spikes = [tuple(img(x) for x in t) for t in C['spikes']]
De = [t for t in C1p_spikes if (same(t[0], Ae) and same(t[1], Be)) or (same(t[0], Be) and same(t[1], Ae))]
chk("C1' has a spike triangle on the C1 hh edge e (types swapped)", len(De) == 1)
Pg = De[0][2]
c2 = sum(H2, V(0, 0, 0))/6; zh = unit(c2); mid = (Ae + Be)/2
xh = unit(Be - Ae); yh = unit((c2 - mid) - dot(c2 - mid, xh)*xh)
loc = lambda p: V(dot(p - mid, xh), dot(p - mid, yh), dot(p - c2, zh))
glob = lambda q: mid + q[0]*xh + q[1]*yh + (q[2] + dot(c2 - mid, zh))*zh
Pl = loc(Pg)
tq = BETA - PI/4
chk(f"P (spike apex of C1') at depth {mp.nstr(Pl[2],12)} outside H2, over H2 (y={mp.nstr(Pl[1],8)}); angle to H2 = beta - pi/4 exactly",
    Pl[2] > 0 and abs(mp.atan2(Pl[2], Pl[1]) - tq) < TOL and abs(Pl[0]) < TOL)
# hexagon vertices in order A, B, C, D, E, F
Hl = [loc(u) for u in H2]
cen = sum(Hl, V(0, 0, 0))/6
Hl.sort(key=lambda q: float(mp.atan2(q[1] - cen[1], q[0] - cen[0])))
i0 = [i for i, q in enumerate(Hl) if abs(q[0] + mp.mpf(1)/2) < TOL and abs(q[1]) < TOL][0]
Hl = Hl[i0:] + Hl[:i0]
if abs(Hl[1][0] - mp.mpf(1)/2) > TOL: Hl = [Hl[0]] + Hl[1:][::-1]
A, B, Cv, D, E, Fv = Hl
names = "ABCDEF"
# C1 edge types around H2: AB hh (shared hexagon H); alternate
etype = {}
for i in range(6):
    u, w = Hl[i], Hl[(i+1) % 6]
    ug, wg = glob(u), glob(w)
    inpent = any(any(same(ug, a) for a in f) and any(same(wg, a) for a in f) for f in C['pents'])
    etype[names[i]+names[(i+1) % 6]] = 'r' if inpent else 'hh'
pr(f"  C1 edge types round H2: {etype}")
chk("H2 edges alternate hh, r with AB = hh", [etype[k] for k in ('AB','BC','CD','DE','EF','FA')] == ['hh','r','hh','r','hh','r'])
pr("== part 2: classic scutoid, Y vertex at P")
def plane3(p, q, w, inside):
    n = unit(cross(q - p, w - p)); d = dot(n, p)
    if dot(n, inside) > d: n, d = -n, -d
    return (n, d)                                # K side: n.x <= d
def tilt(U, W, th):
    t = unit(W - U); uin = unit(cen - U - dot(cen - U, t)*t); uin[2] = 0; uin = unit(uin)
    w = mp.cos(th)*uin + mp.sin(th)*V(0, 0, 1)
    m = (U + W)/2; inside = m + mp.mpf('0.1')*uin + V(0, 0, mp.mpf('1e-4'))
    return plane3(U, W, U + w, inside)
def angle_with_top(pl):
    n = pl[0]; return PI - mp.acos(dot(n, V(0, 0, -1)))
ins0 = lambda U, W: (U + W)/2 + mp.mpf('0.1')*unit(cen - (U + W)/2) + V(0, 0, mp.mpf('1e-4'))
pD = plane3(A, B, Pl, ins0(A, B))
pFA = plane3(Fv, A, Pl, ins0(Fv, A)); pBC = plane3(B, Cv, Pl, ins0(B, Cv))
thFA, thBC = angle_with_top(pFA), angle_with_top(pBC)
idFA = ident(thFA)
chk(f"forced tilt of the faces through P at FA and BC: {deg(thFA):.6f} deg = {idFA} = pi/2 - beta (in the alphabet)",
    idFA == (F(1, 2), -1) and abs(thFA - thBC) < TOL)
def dihedral(p, q): return PI - mp.acos(dot(p[0], q[0]))
dAP, dBP, dPP = dihedral(pD, pFA), dihedral(pD, pBC), dihedral(pFA, pBC)
pr(f"  forced dihedrals: leg AP {deg(dAP):.6f} ({ident(dAP)}), leg BP {deg(dBP):.6f} ({ident(dBP)}), down edge PP' {deg(dPP):.6f} ({ident(dPP)})")
out['forced'] = dict(tilt_FA_BC=[str(idFA[0]), idFA[1], deg(thFA)], leg=[deg(dAP), str(ident(dAP))], down_edge=[deg(dPP), str(ident(dPP))])
# down edge direction from P must stay on K's side of Delta (convex trihedral at P)
dd = unit(cross(pFA[0], pBC[0]));  dd = dd if dd[2] > 0 else -dd
chk(f"down edge PP' leaves P downward on K's side of Delta_e (dip {deg(mp.atan2(dd[2], mp.sqrt(dd[0]**2+dd[1]**2))):.4f} < 20.9052 deg)",
    dot(pD[0], dd) < 0)

pr("== lemma A1: leg dihedral of ANY branch-A K that is locally convex at A (or B)")
# convex vertex figure at A with consecutive sides H2 (AF->AB) and Delta_e (AB->AP): the next side from AP must keep AF inside,
# so the corner at AP (K's dihedral at leg AP) is >= the dihedral between planes (A,P,B) and (A,P,F) = dAP.
lam = dAP
cpoly = mp.findpoly(mp.cos(lam), 8, maxcoeff=10**6)
pr(f"  lambda* = angle(B, AP, F) = {mp.nstr(lam*180/PI, 20)} deg; cos lambda* = {mp.nstr(mp.cos(lam), 20)}, integer polynomial {cpoly}")
rel = mp.pslq([lam, PI, BETA], maxcoeff=10**4, maxsteps=10**6)
chk(f"lambda* is not p*pi + b*beta (no integer relation lambda*, pi, beta with coefficients <= 1e4 at 50 digits: {rel})", rel is None)
# every C1 spike triangle is a face of a K (B1); K has its spike-triangle face Delta with legs; at each pyramid side-side edge of a C1
# the two spike triangles meeting there are faces of two K, so the ring is 2pi/3 + lambda_1 + lambda_2 + (rest >= 0)
marg = 2*PI/3 + 2*lam - 2*PI
chk(f"ss ring with both K convex at their leg ends: 120 + 2 lambda* = {mp.nstr((2*PI/3+2*lam)*180/PI, 15)} deg > 360 (excess {mp.nstr(marg*180/PI, 12)} deg)",
    marg > mp.mpf('0.1'))
pr("  => a branch-A K with Delta's two leg ends convex cannot exist; at every ss edge one of the two K has a leg dihedral <= "
   f"{mp.nstr((4*PI/3 - lam)*180/PI, 10)} deg (reflex vertex figure at that end).")
# which alphabet pairs (lambda, lambda') could close the ss ring with lambda >= lambda* (one convex end): 2pi/3 + l + l' (+ more K) = 2pi
pairs = [(a, b) for a in CONV for b in ALPH if val(a) >= lam - TOL and abs(val(a) + val(b) - 4*PI/3) < TOL]
pairs += [(a, b, c) for a in CONV for b in ALPH for c in ALPH if val(a) >= lam - TOL and abs(val(a) + val(b) + val(c) - 4*PI/3) < TOL]
pr(f"  alphabet completions of the ss ring with one convex leg end: {[[round(deg(val(x)),4) for x in p] for p in pairs]}")
out['lemmaA1'] = dict(lambda_star_deg=deg(lam), cos_poly=str(cpoly), excess_deg=deg(marg), ss_completions=[[deg(val(x)) for x in p] for p in pairs])
pr("== score of the classic candidate K0 (Y at P)")
def polytope(planes):
    vs = []
    for i, j, k in itertools.combinations(range(len(planes)), 3):
        M = mp.matrix([[planes[t][0][c] for c in range(3)] for t in (i, j, k)])
        n1, n2, n3 = (planes[t][0] for t in (i, j, k))
        if abs(dot(n1, cross(n2, n3))) < mp.mpf(10)**-20: continue
        x = mp.lu_solve(M, mp.matrix([planes[t][1] for t in (i, j, k)]))
        if all(dot(p[0], x) <= p[1] + TOL for p in planes) and all(nrm(x - y) > TOL for y in vs): vs.append(x)
    act = [[t for t, p in enumerate(planes) if abs(dot(p[0], x) - p[1]) < TOL] for x in vs]
    return vs, act
top = (V(0, 0, -1), mp.mpf(0))
pn = ['top', 'bottom', 'Delta', 'FA', 'BC', 'CD', 'DE', 'EF']
def classic(tCD, tDE, tEF, h):
    pl = [top, (V(0, 0, 1), h), pD, pFA, pBC, tilt(Cv, D, tCD), tilt(D, E, tDE), tilt(E, Fv, tEF)]
    vs, act = polytope(pl)
    fs = {pn[t]: sum(t in a for a in act) for t in range(len(pl))}
    mids = [x for x in vs if TOL < x[2] < h - TOL]
    good = fs['Delta'] == 3 and fs['top'] == 6 and fs['bottom'] == 5 and len(mids) == 1 and all(fs[k] >= 4 for k in ('FA','BC','CD','DE','EF'))
    return good, pl, vs, act, fs, mids
found = []
for tCD in CONV:
    for tDE in CONV:
        for h in (mp.mpf('0.5'), mp.mpf('0.6'), mp.mpf('0.8')):
            g = classic(val(tCD), val(tDE), val(tCD), h)
            if g[0]: found.append((tCD, tDE, h)); break
pr(f"  symmetric tilt choices (CD = EF, DE) from the convex alphabet giving the classic scutoid (6 top, 5 bottom, Y at P) for some h in 0.5, 0.6, 0.8: "
   f"{len(found)}: {[(round(deg(val(a)),4), round(deg(val(b)),4), float(h)) for a, b, h in found]}")
out['classic_tilts'] = [[deg(val(a)), deg(val(b)), float(h)] for a, b, h in found]
tCD, tDE, h0 = found[0] if found else (CONV[0], CONV[0], mp.mpf('0.6'))
pr(f"  representative K0: CD = EF = {deg(val(tCD)):.4f}, DE = {deg(val(tDE)):.4f}, h = {float(h0)}")
_, planes, vs, act, _, _ = classic(val(tCD), val(tDE), val(tCD), h0)
faces = {pn[t]: sum(t in a for a in act) for t in range(len(planes))}
mids = [x for x in vs if TOL < x[2] < h0 - TOL]
pr(f"  K0: {len(vs)} vertices; face sizes {faces}; vertices strictly between the end planes: {[mp.nstr(x[2],8) for x in mids]}")
score("(1) K0 faces planar (each face is a plane section of a convex polytope); Delta face = whole spike triangle A,B,P; top = whole H2; "
    "bottom 5 sides; one Y vertex (P)", faces['Delta'] == 3 and faces['top'] == 6 and faces['bottom'] == 5 and len(mids) == 1)
score("(2) K0 rings closable: ss ring at leg AP = 120 + 157.7612 (K0) + 157.7612 (the K0 on the neighbouring C1' spike) > 360", False)
# (4) local disjointness K0 vs C1 (truncated icosahedron + 12 pyramids) and vs C1' : separating axis test at 50 digits
def sat(P1, P2):
    """separating-axis test for convex polytopes given as (points, face normals, edge directions); returns the best separation"""
    axes = list(P1[1]) + list(P2[1])
    for a in P1[2]:
        for b in P2[2]:
            c = cross(a, b)
            if nrm(c) > mp.mpf(10)**-20: axes.append(unit(c))
    best = -mp.inf
    for n in axes:
        p1 = [dot(n, x) for x in P1[0]]; p2 = [dot(n, x) for x in P2[0]]
        best = max(best, min(p2) - max(p1), min(p1) - max(p2))
    return best
def poly_from_pts(pts, normals):
    E = [pts[j] - pts[i] for i, j in itertools.combinations(range(len(pts)), 2)
         if sum(1 for n in normals if abs(dot(n, pts[i]) - max(dot(n, q) for q in pts)) < TOL and abs(dot(n, pts[j]) - max(dot(n, q) for q in pts)) < TOL) >= 2]
    return (pts, normals, E)
K0g = [glob(x) for x in vs]
lin = lambda n: glob(n) - glob(V(0, 0, 0))
K0P = poly_from_pts(K0g, [unit(lin(p[0])) for p in planes])
def hull_normals(pts):
    N = []
    for a, b, c in itertools.combinations(pts, 3):
        n = cross(b - a, c - a)
        if nrm(n) < mp.mpf(10)**-20: continue
        n = unit(n); d = [dot(n, q - a) for q in pts]
        if all(x <= TOL for x in d) or all(x >= -TOL for x in d):
            n = n if all(x <= TOL for x in d) else -n
            if all(nrm(n - m) > TOL for m in N): N.append(n)
    return N
TIP = poly_from_pts(C['TV'], C['hd'] + C['pd'])
pyrP = [poly_from_pts(p, hull_normals(p)) for p in C['pyrs']]
C1p = [TIP] + pyrP
mov = lambda P: ([img(x) for x in P[0]], [unit(img(n) - img(V(0, 0, 0))) for n in P[1]], [img(e) - img(V(0, 0, 0)) for e in P[2]])
C1pp = [mov(P) for P in C1p]
kc = sum(K0g, V(0,0,0))/len(K0g)
near = lambda X: nrm(sum(X[0], V(0,0,0))/len(X[0]) - kc) < 6
s1 = min(sat(K0P, X) for X in C1p if near(X)); s2 = min(sat(K0P, X) for X in C1pp if near(X))
s12 = min(sat(X, Y) for X in C1p for Y in C1pp if near(X) and near(Y))
pr(f"  worst separation K0|C1 = {mp.nstr(s1, 8)}, K0|C1' = {mp.nstr(s2, 8)}, C1|C1' = {mp.nstr(s12, 8)} (>= -1e-30 means interiors disjoint)")
out['K0'] = dict(tilts_deg=dict(FA=deg(thFA), BC=deg(thBC), CD=deg(val(tCD)), DE=deg(val(tDE)), EF=deg(val(tCD))), h=float(h0),
                 vertices_local=[[float(c) for c in x] for x in vs], faces=faces, sep_C1=float(s1), sep_C1p=float(s2), sep_C1_C1p=float(s12))
json.dump(out, open(__import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'data', 'branchA.json'), 'w'), indent=1, default=str)
score(f"(4) K0 interior-disjoint from C1 and C1' (local): margins {mp.nstr(s1,6)}, {mp.nstr(s2,6)}", s1 > -mp.mpf(10)**-30 and s2 > -mp.mpf(10)**-30)
chk("control: C1 and C1' interior-disjoint (hexagon shared, types swapped)", s12 > -mp.mpf(10)**-30)
pr("FINAL ok" if OK else "FINAL FAIL")
