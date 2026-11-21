"""Tree search round 1, branch B: the SPIKE TRIANGLE is an end face of the scutoid K, the regular hexagon a lateral face on its
base edge at the forced dihedral t' = beta - pi/4, the hexagon's two middle corners Q0, Q1 Y-junctions.
Frame (exact): end face z = 0, P0 = (-1/2,0,0), P1 = (1/2,0,0), Pa = (0,h,0), h^2 = (3phi^2-1)/4 (legs sqrt3 phi/2, base 1).
Hexagon on P0P1 tilted by t': Q0 = (-1, phi/2, 1/(2phi)), R0 = (-1/2, phi, 1/phi) (+ mirrors). Other end plane z = 1/phi.
Standard scutoid rule (every end vertex has degree 3: two end edges, one lateral edge): at P0 the faces are end, hexagon, F0, so
F0 = plane(P0, Pa, Q0) is FORCED; at Q0 (Y) the faces are hexagon, F0, G0 with G0 through the line Q0R0: one free angle g
= dihedral(hexagon, G0). Scan g over the alphabet; K = intersection of the half-spaces (convex, faces planar by construction).
Scores: (1) planar faces + scutoid combinatorics; (2) every K edge ring closable with C1 + K dihedrals; (3) Dehn invariant of K
zero (packet of C1 + nK zero, C1's is zero); (4) 60 copies on the 60 spike triangles of one C1 interior-disjoint from C1 and each
other.  Numerics mpmath 60 digits; identifications by PSLQ with residual printed; geometric margins printed (>> error)."""
import itertools, json, math, sys
from fractions import Fraction as Fr
import mpmath as mp
import sympy as sp
mp.mp.dps = 60
out = {}
def pr(s=""): print(s, flush=True)
phi = (1 + mp.sqrt(5)) / 2
PI = mp.pi; AL = mp.atan(phi); BE = mp.acos(1 / mp.sqrt(6)); GA = mp.acos(mp.sqrt(mp.mpf(2) / 3))
BASIS0 = [("pi", PI), ("alpha", AL), ("beta", BE), ("gamma", GA)]
deg = lambda x: float(x * 180 / PI)
V = lambda *a: mp.matrix([mp.mpf(x) if not isinstance(x, mp.mpf) else x for x in a])
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
cross = lambda u, v: mp.matrix([u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]])
nrm = lambda u: mp.sqrt(dot(u, u))
unit = lambda u: u / nrm(u)
EPS = mp.mpf(10) ** -40
tq = BE - PI / 4

# ---------- alphabet (ring-closing set): p*pi + b*beta, b = +-1: p in Z/4; b = 0: p rational, denominator <= 12 (covers rings.json)
ALPH = []
for b in (1, -1):
    for k in range(-8, 12):
        v = Fr(k, 4) * 1
        a = mp.mpf(k) / 4 * PI + b * BE
        if 0 < a < 2 * PI and abs(a - PI) > EPS: ALPH.append(((Fr(k, 4), b), a))
seen = set()
for q in range(1, 13):
    for k in range(1, 2 * q):
        f = Fr(k, q)
        if f in seen or f == 1: continue
        seen.add(f); ALPH.append(((f, 0), mp.mpf(f.numerator) / f.denominator * PI))
def in_alph(a):
    best = min(ALPH, key=lambda t: abs(t[1] - a))
    return best, abs(best[1] - a)

# ---------- frame
h = mp.sqrt((3 * phi ** 2 - 1) / 4)
P0, P1, Pa = V(-0.5, 0, 0), V(0.5, 0, 0), V(0, h, 0)
Q0, Q1 = V(-1, phi / 2, 1 / (2 * phi)), V(1, phi / 2, 1 / (2 * phi))
R0, R1 = V(-0.5, phi, 1 / phi), V(0.5, phi, 1 / phi)
H = 1 / phi
hexv = [P0, P1, Q1, R1, R0, Q0]
chk = []
def check(name, cond, extra=""):
    chk.append([name, bool(cond)]); pr(f"  [{'pass' if cond else 'FAIL'}] {name} {extra}")
pr("== frame")
check("hexagon regular, side 1", all(abs(nrm(hexv[i] - hexv[(i + 1) % 6]) - 1) < EPS for i in range(6)) and abs(nrm(R0 - P0) - mp.sqrt(3)) < EPS)
check("legs of the end triangle = sqrt3 phi/2", abs(nrm(Pa - P0) - mp.sqrt(3) * phi / 2) < EPS)
nh_out = V(0, -mp.sin(tq), mp.cos(tq))
check("hexagon planar and at dihedral t' = beta - pi/4 to the end face", all(abs(dot(nh_out, p)) < EPS for p in hexv))
check("height of the other end = sqrt3 sin t' = 1/phi exactly (R0, R1 at z = 1/phi)", abs(mp.sqrt(3) * mp.sin(tq) - 1 / phi) < EPS)
# sympy exact: sqrt3*sin(beta - pi/4) == 1/phi
bs = sp.acos(1 / sp.sqrt(6)); phs = (1 + sp.sqrt(5)) / 2
check("(sympy) sqrt3 sin(beta-pi/4) - 1/phi == 0", sp.simplify(sp.expand(sp.sqrt(3) * (sp.sin(bs) - sp.cos(bs)) / sp.sqrt(2) - 1 / phs)) == 0)

def plane_through(a, b, c, inside):
    n = unit(cross(b - a, c - a)); d = dot(n, a)
    if dot(n, inside) - d > 0: n, d = -n, -d
    return n, d
INSIDE = V(0, 0.6, 0.1)
F0 = plane_through(P0, Pa, Q0, INSIDE); F1 = plane_through(P1, Pa, Q1, INSIDE)
BOT = (V(0, 0, -1), mp.mpf(0)); TOP = (V(0, 0, 1), H); HEX = (nh_out, mp.mpf(0))
def G_plane(Qp, Rp, g):
    w = unit(Rp - Qp); hc = sum(hexv, V(0, 0, 0)) / 6
    e2 = hc - Qp; e2 = unit(e2 - dot(e2, w) * w)
    n = mp.cos(PI - g) * nh_out - mp.sin(PI - g) * e2
    return n, dot(n, Qp)

def polytope(planes):
    verts = []
    for i, j, k in itertools.combinations(range(len(planes)), 3):
        (ni, di), (nj, dj), (nk, dk) = planes[i], planes[j], planes[k]
        dt = dot(ni, cross(nj, nk))
        if abs(dt) < EPS: continue
        x = (di * cross(nj, nk) + dj * cross(nk, ni) + dk * cross(ni, nj)) / dt
        if all(dot(p[0], x) - p[1] < EPS for p in planes) and not any(nrm(x - y) < EPS for y in verts): verts.append(x)
    faces = {}
    for fi, p in enumerate(planes):
        on = [vi for vi, x in enumerate(verts) if abs(dot(p[0], x) - p[1]) < EPS]
        if len(on) >= 3: faces[fi] = on
    edges = []
    for a, b in itertools.combinations(faces, 2):
        com = sorted(set(faces[a]) & set(faces[b]))
        if len(com) == 2: edges.append((a, b, com))
    return verts, faces, edges

def dihedral(planes, a, b): return PI - mp.acos(max(-1, min(1, dot(planes[a][0], planes[b][0]))))

# ---------- basis extension by PSLQ
def express(theta, basis):
    vec = [theta] + [x for _, x in basis]
    rel = mp.pslq(vec, maxcoeff=2000, maxsteps=20000, tol=mp.mpf(10) ** -50)
    if rel is None or rel[0] == 0: return None
    c = [Fr(-r, rel[0]) for r in rel[1:]]
    res = theta - sum(mp.mpf(ci.numerator) / ci.denominator * x for ci, (_, x) in zip(c, basis))
    return c, res

NAMES = {0: "bottom(end triangle)", 1: "top", 2: "hexagon", 3: "F0", 4: "F1", 5: "G0", 6: "G1"}
def build(g):
    planes = [BOT, TOP, HEX, F0, F1, G_plane(Q0, R0, g), G_plane(Q1, R1, g)]
    for p in planes: assert dot(p[0], INSIDE) - p[1] < 0
    return planes, polytope(planes)

def scutoid_ok(verts, faces, edges):
    """end face 0 is exactly the spike triangle; top is a different polygon; Y vertices off both ends have degree 3; >= 1 Y;
    all 7 planes are faces; Q0, Q1 are Y vertices."""
    if len(faces) != 7: return False, f"only {len(faces)} of 7 planes are faces"
    bot = sorted(faces[0]); want = [P0, P1, Pa]
    if len(bot) != 3 or not all(any(nrm(verts[v] - w) < EPS for v in bot) for w in want): return False, "end face is not the spike triangle"
    if len(faces[1]) == 3: return False, "top is a triangle"
    deg_ = {v: sum(v in f for f in faces.values()) for v in range(len(verts))}
    Y = [v for v in range(len(verts)) if abs(verts[v][2]) > EPS and abs(verts[v][2] - H) > EPS]
    if not Y: return False, "no Y vertex"
    if any(deg_[v] != 3 for v in Y): return False, "a Y vertex has degree != 3"
    for q in (Q0, Q1):
        if not any(nrm(verts[v] - q) < EPS for v in Y): return False, "Q0/Q1 not Y vertices"
    if any(d != 3 for d in deg_.values()): return False, "an end vertex has degree != 3"
    return True, f"{len(verts)} vertices, {len(edges)} edges, Y = {len(Y)}, top {len(faces[1])}-gon"

# ---------- C1 (edge 1) for check (4)
def c1_model():
    cyc = lambda t: [(t[0], t[1], t[2]), (t[2], t[0], t[1]), (t[1], t[2], t[0])]
    TV = []
    for b in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]:
        for sg in itertools.product((1, -1), repeat=3):
            t = tuple(sg[i] * b[i] / 2 for i in range(3))
            for c in cyc(t):
                x = V(*c)
                if not any(nrm(x - y) < EPS for y in TV): TV.append(x)
    assert len(TV) == 60
    pdirs = []
    for a_, b_ in itertools.product((1, -1), repeat=2):
        for c in cyc((0, a_, b_ * phi)): pdirs.append(unit(V(*c)))
    Rd = mp.sqrt(3) * phi / 2
    pyrs = []; tris = []
    for pd in pdirs:
        m = max(dot(pd, x) for x in TV); pent = [x for x in TV if abs(dot(pd, x) - m) < EPS]; assert len(pent) == 5
        cen = sum(pent, V(0, 0, 0)) / 5; apex = cen + mp.sqrt(Rd ** 2 - nrm(pent[0] - cen) ** 2) * pd
        pyrs.append(pent + [apex])
        for a, b in itertools.combinations(pent, 2):
            if abs(nrm(a - b) - 1) < EPS: tris.append((a, b, apex, cen))
    assert len(tris) == 60
    return TV, pyrs, tris
def place(tri, pts):
    a, b, apex, cen = tri
    M = (a + b) / 2; ex = b - a; ey = unit(apex - M); ez = cross(ex, ey)
    inner = cen * mp.mpf(0.7) + apex * mp.mpf(0.3)
    if dot(ez, M - inner) < 0: ez = -ez
    return [M + p[0] * ex + p[1] * ey + p[2] * ez for p in pts]

import numpy as np
def hull_parts(pts):
    """face normals and true edge directions of a convex point set (numpy float64)"""
    P = np.array([[float(c) for c in p] for p in pts])
    N = []; On = []
    for i, j, k in itertools.combinations(range(len(P)), 3):
        n = np.cross(P[j] - P[i], P[k] - P[i]); ln = np.linalg.norm(n)
        if ln < 1e-12: continue
        n = n / ln; s = (P - P[i]) @ n
        if (s <= 1e-9).all() or (s >= -1e-9).all():
            if not any(abs(abs(n @ m) - 1) < 1e-9 and abs((P[i] - P[min(On[t])]) @ m) < 1e-9 for t, m in enumerate(N)):
                N.append(n); On.append(set(np.nonzero(abs(s) < 1e-9)[0]))
    E = []
    for i, j in itertools.combinations(range(len(P)), 2):
        if sum(i in o and j in o for o in On) >= 2:
            d = P[j] - P[i]; d = d / np.linalg.norm(d)
            if not any(abs(abs(d @ m) - 1) < 1e-9 for m in E): E.append(d)
    NN = []
    for n in N:
        if not any(abs(abs(n @ m) - 1) < 1e-9 for m in NN): NN.append(n)
    return P, NN, E
def sat(A, B):
    """min over separating-axis candidates of (overlap length); <= 0 means separated (touching = 0)."""
    PA, NA, EA = A; PB, NB, EB = B
    axes = NA + NB
    for u in EA:
        for v in EB:
            c = np.cross(u, v); l = np.linalg.norm(c)
            if l > 1e-9: axes.append(c / l)
    worst = 1e9
    for ax in axes:
        a = PA @ ax; b = PB @ ax
        ov = min(a.max(), b.max()) - max(a.min(), b.min())
        worst = min(worst, ov)
        if worst < -1e-9: return worst
    return worst

def main():
    pr("== forced faces at P0, P1 (standard scutoid: end vertices of degree 3)")
    planes, _ = build(PI / 2)
    a_bot_F0 = dihedral(planes, 0, 3); a_hex_F0 = dihedral(planes, 2, 3)
    for nm, a in (("end triangle | F0 at P0Pa", a_bot_F0), ("hexagon | F0 at P0Q0", a_hex_F0)):
        (key, val), dist = in_alph(a)
        pr(f"  {nm}: {deg(a):.6f} deg; nearest alphabet item {key[0]}pi{'+' if key[1]>=0 else '-'}{abs(key[1])}beta = {deg(val):.6f} deg, gap {deg(dist):.6f} deg")
        ex = express(a, BASIS0)
        pr(f"    PSLQ in (pi, alpha, beta, gamma), coeffs <= 2000: {'none' if ex is None else [str(x) for x in ex[0]]}")
    # exact cosines (sympy)
    hs = sp.sqrt((3 * phs ** 2 - 1) / 4)
    p0, pa, q0 = sp.Matrix([-sp.Rational(1, 2), 0, 0]), sp.Matrix([0, hs, 0]), sp.Matrix([-1, phs / 2, 1 / (2 * phs)])
    nF = (pa - p0).cross(q0 - p0); nF = nF / sp.sqrt(nF.dot(nF))
    cosF = sp.radsimp(sp.nsimplify(sp.simplify(abs(nF[2]))))
    pr(f"  exact |cos| of the F0 plane against the end plane: {cosF}  (= {float(cosF):.12f})")
    th0 = sp.pi - sp.acos(cosF)
    check("exact: interior dihedral end|F0 is obtuse with cos = -sqrt(7+3sqrt5)/4 < -1/2, so on a C1 pyramid side-side edge "
          "2pi/3 + 2 x (end|F0) > 2pi (two K on adjacent spike triangles overlap, for every g)",
          sp.simplify(cosF**2 - sp.Rational(1, 4)) > 0 and abs(float(sp.N(th0)) - float(a_bot_F0)) < 1e-12)
    out['forced'] = dict(end_F0_deg=deg(a_bot_F0), hex_F0_deg=deg(a_hex_F0), cos_F0_vs_end=str(cosF),
                         end_F0_in_alphabet=bool(in_alph(a_bot_F0)[1] < EPS), hex_F0_in_alphabet=bool(in_alph(a_hex_F0)[1] < EPS),
                         gap_end_F0_deg=deg(in_alph(a_bot_F0)[1]), gap_hex_F0_deg=deg(in_alph(a_hex_F0)[1]))
    pr("== scan g = dihedral(hexagon, G0) over the alphabet (0 < g < pi)")
    TV, pyrs, tris = c1_model()
    C1parts = [hull_parts(TV)] + [hull_parts(p) for p in pyrs]
    results = []
    for key, g in ALPH:
        if not (0 < g < PI): continue
        planes, (verts, faces, edges) = build(g)
        ok, why = scutoid_ok(verts, faces, edges)
        if not ok:
            pr(f"  g = {deg(g):9.4f} rejected: {why}"); continue
        # edge dihedrals and lengths
        E = []
        for a, b, com in edges:
            E.append(dict(faces=(NAMES[a], NAMES[b]), length=nrm(verts[com[0]] - verts[com[1]]), angle=dihedral(planes, a, b)))
        # (1) planar: every face's vertices on its plane (by construction), polygon convex: report max deviation
        dev = max(abs(dot(planes[f][0], verts[v]) - planes[f][1]) for f in faces for v in faces[f])
        s1 = dev < EPS and ok
        # basis for K + C1 angles
        basis = list(BASIS0); vecs = []
        for e in E:
            ex = express(e['angle'], basis)
            if ex is None:
                basis.append((f"theta{len(basis)-3}", e['angle'])); ex = express(e['angle'], basis)
            c, res = ex; e['vec'] = c + [Fr(0)] * (len(basis) - len(c)); e['res'] = res
        nb = len(basis)
        for e in E: e['vec'] = (e['vec'] + [Fr(0)] * nb)[:nb]
        c1ang = [[Fr(3, 2), 0, -2, 0], [Fr(3, 4), 0, 1, 0], [Fr(2, 3), 0, 0, 0]]
        c1ang = [[Fr(x) for x in v] + [Fr(0)] * (nb - 4) for v in c1ang]
        pool = c1ang + [e['vec'] for e in E]
        val = lambda v: sum(float(x) * float(bx) for x, (_, bx) in zip(v, basis))
        def closable(vfix, maxn=6):
            for target in ([Fr(2)] + [Fr(0)] * (nb - 1), [Fr(1)] + [Fr(0)] * (nb - 1)):
                tv = val(target)
                def rec(start, left, n):
                    if all(x == 0 for x in left): return True
                    if n == maxn or val(left) < 1e-9: return False
                    for i in range(start, len(pool)):
                        if val(pool[i]) <= val(left) + 1e-9 and rec(i, [x - y for x, y in zip(left, pool[i])], n + 1): return True
                    return False
                if rec(0, [x - y for x, y in zip(target, vfix)], 1): return True
            return False
        ring_fail = [e for e in E if not closable(e['vec'])]
        s2 = not ring_fail
        # (3) Dehn invariant of K: coefficient of each non-pi basis element
        dehn = [sum(e['length'] * mp.mpf(e['vec'][k].numerator) / e['vec'][k].denominator for e in E) for k in range(1, nb)]
        s3 = all(abs(x) < mp.mpf(10) ** -35 for x in dehn)
        # (4) copies on all 60 spike triangles of one C1
        Kloc = verts
        copies = [hull_parts(place(t, Kloc)) for t in tris]
        worstC1 = max(sat(c, p) for c in copies[:5] for p in C1parts)   # symmetry: all triangles equivalent; 5 suffice
        worstKK = -1e9; pairKK = None
        for i in range(60):
            for j in range(i + 1, 60):
                if np.linalg.norm(copies[i][0].mean(0) - copies[j][0].mean(0)) > 8: continue
                s = sat(copies[i], copies[j])
                if s > worstKK: worstKK, pairKK = s, (i, j)
        s4 = worstC1 <= 1e-9 and worstKK <= 1e-9
        score = sum([s1, s2, s3, s4])
        results.append(dict(g_key=f"{key[0]}pi{'+' if key[1]>=0 else '-'}{abs(key[1])}beta", g_deg=deg(g), combinatorics=why, score=score,
                            s1=s1, s2=s2, s3=s3, s4=s4, n_new_basis=nb - 4,
                            ring_fail=[(e['faces'], round(deg(e['angle']), 6)) for e in ring_fail],
                            dehn_coeffs=[mp.nstr(x, 12) for x in dehn], basis=[b for b, _ in basis],
                            overlap_with_C1=worstC1, overlap_KK=worstKK, KK_pair=pairKK,
                            edges=[dict(faces=e['faces'], length=mp.nstr(e['length'], 15), deg=round(deg(e['angle']), 8),
                                        vec=[str(x) for x in e['vec']], pslq_res=mp.nstr(abs(e['res']), 3)) for e in E],
                            vertices=[[mp.nstr(c, 15) for c in v] for v in verts],
                            faces={NAMES[f]: v for f, v in faces.items()}))
        pr(f"  g = {results[-1]['g_key']:16s} {deg(g):9.4f}  {why:44s} score {score}  (1){int(s1)} (2){int(s2)} (3){int(s3)} (4){int(s4)}"
           f"  ring-fails {len(ring_fail)}  overlap C1 {worstC1:.4f} K-K {worstKK:.4f}")
    out['scan'] = results
    if results:
        best = max(results, key=lambda r: (r['score'], -len(r['ring_fail']), -r['overlap_KK']))
        out['best'] = best
        pr("== best K"); pr(json.dumps({k: best[k] for k in ('g_key', 'g_deg', 'combinatorics', 'score', 's1', 's2', 's3', 's4', 'ring_fail',
                                                               'dehn_coeffs', 'basis', 'overlap_with_C1', 'overlap_KK', 'KK_pair')}, indent=1, default=str))
        for e in best['edges']: pr(f"   {e['faces'][0]:22s}|{e['faces'][1]:22s} len {e['length']:>18s}  {e['deg']:12.6f} deg  vec {e['vec']}  res {e['pslq_res']}")
        for v in best['vertices']: pr(f"   v {v}")
    out['checks'] = chk
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'branchB.json', 'w'), indent=1, default=str)
    pr("FINAL ok" if all(c[1] for c in chk) else "FINAL frame checks failed")
main()
