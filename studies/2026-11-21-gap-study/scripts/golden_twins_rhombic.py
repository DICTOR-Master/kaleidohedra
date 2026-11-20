# Galois twins (Double Vision) of the golden cuts of the rhombic dodecahedron (RD) and rhombic triacontahedron (RT).
# Gap study 2026-11-21, grid cells "RD x TWIN" (empty) and "RT x TWIN" ("33 (?)").
# Cuts from #89 Theorem 3: rhombus of side 1, acute angle alpha, K = (1/sin(alpha/2) + 1/cos(alpha/2))/2;
#   greater: b = 1/(1 + phi K), a = phi b;  lesser: b = 1/(1 + K/phi), a = b/phi;
#   cut depths along the edges: y_sharp = a/(2 sin(alpha/2)), y_blunt = a/(2 cos(alpha/2)); remaining side b = 1 - y_sharp - y_blunt.
# The solid is rational-free of the cut (RD corners in Q; RT corners in Q(sqrt5)), so a twin cut is the cut at the conjugate depths
# sigma(y_sharp), sigma(y_blunt) on the twin solid; it is a real solid iff 0 < sigma(y_sharp), 0 < sigma(y_blunt) and
# sigma(y_sharp) + sigma(y_blunt) < 1 (no two corner cuts cross on an edge; GL Theorem 1A's "over-cut" test).
# We run EVERY field embedding (every Galois conjugate), not only sqrt5 -> -sqrt5.
# Run 1 (21 Nov) found that one embedding pairs the RD's two cuts; the checks below state that exactly.
# Controls: #88 / Golden Ladder Theorem 1A: cube's two cuts are twins of each other (real); triangle-faced cuts over-cut;
#           the identity embedding must reproduce #89 Table 2 (RD: a = 0.477001, b = 0.294803; RT greater a = 0.463634, b = 0.286541).
import itertools, sys
import sympy as sp
from sympy import sqrt, Rational as Q

FAIL = []
def check(label, ok):
    print(('ok   ' if ok else 'FAIL ') + label); sys.stdout.flush()
    if not ok: FAIL.append(label)

r2, r3, r5 = sp.symbols('r2 r3 r5', positive=True)

def cut(K, sh, bl, ph):
    out = {}
    for name, b in [('greater', 1 / (1 + ph * K)), ('lesser', 1 / (1 + K / ph))]:
        a = ph * b if name == 'greater' else b / ph
        out[name] = dict(a=a, b=b, ys=a / (2 * sh), yb=a / (2 * bl))
    return out

def valid(ys, yb): return ys > 0 and yb > 0 and ys + yb < 1

# ---------- controls on #88 (Platonic): x1 = phi/(k + 2 phi), x2 = 1/(phi k + 2); a cut at depth x on every edge is a real solid iff 0 < x < 1/2
phs = (1 + r5) / 2
for solid, k in [('cube', r2), ('tetrahedron/octahedron/icosahedron', 1)]:
    x1 = phs / (k + 2 * phs); x2 = 1 / (phs * k + 2)
    sig = {r5: -sqrt(5), r2: -sqrt(2)}; idm = {r5: sqrt(5), r2: sqrt(2)}
    s1, s2 = sp.nsimplify(sp.radsimp(x1.subs(sig))), sp.radsimp(x2.subs(sig))
    v1, v2 = x1.subs(idm), x2.subs(idm)
    if solid == 'cube':
        check('control #88 cube: sigma(x1) = x2 (the Golden Cut Cubes are twins)', sp.simplify(s1 - v2) == 0)
        check('control #88 cube: twin depths real (0 < x < 1/2)', 0 < s1 < Q(1, 2) and 0 < s2 < Q(1, 2))
    else:
        check('control #88 triangle-faced: sigma(x1) = phi^2 and sigma(x2) = 1/2 + sqrt5/10, both over-cut (> 1/2)',
              sp.simplify(s1 - ((3 + sqrt(5)) / 2)) == 0 and sp.simplify(s2 - (Q(1, 2) + sqrt(5) / 10)) == 0 and s1 > Q(1, 2) and s2 > Q(1, 2))

# ---------- RD: cos alpha = 1/3, sin(alpha/2) = 1/sqrt3, cos(alpha/2) = sqrt2/sqrt3; field Q(sqrt2, sqrt3, sqrt5), 8 embeddings
sh, bl = 1 / r3, r2 / r3
K = (1 / sh + 1 / bl) / 2
check('RD: K = (2 sqrt3 + sqrt6)/4 as in #89', sp.simplify(K.subs({r2: sqrt(2), r3: sqrt(3)}) - (2 * sqrt(3) + sqrt(6)) / 4) == 0)
C = cut(K, sh, bl, (1 + r5) / 2)
real_twins = {}
for s2_, s3_, s5_ in itertools.product([1, -1], repeat=3):
    emb = {r2: s2_ * sqrt(2), r3: s3_ * sqrt(3), r5: s5_ * sqrt(5)}
    for name, d in C.items():
        ys, yb, a, b = [sp.radsimp(d[k].subs(emb)) for k in ('ys', 'yb', 'a', 'b')]
        ok = valid(ys, yb)
        tag = f'RD {name} cut under sqrt2->{"+" if s2_>0 else "-"}sqrt2, sqrt3->{"+" if s3_>0 else "-"}sqrt3, sqrt5->{"+" if s5_>0 else "-"}sqrt5'
        print(f'    {tag}: y_sharp = {sp.N(ys, 12)}, y_blunt = {sp.N(yb, 12)}, sum = {sp.N(ys + yb, 12)}  -> {"REAL SOLID" if ok else "no solid"}')
        if (s2_, s3_, s5_) == (1, 1, 1):
            check(f'RD {name}: identity embedding reproduces #89 Table 2 and is a real solid', ok and
                  (abs(sp.N(a) - (0.477001 if name == 'greater' else 0.322952)) < 1e-6) and (abs(sp.N(b) - (0.294803 if name == 'greater' else 0.522548)) < 1e-6))
        elif ok:
            real_twins[tag] = (ys, yb)
# Found on the first run (log of 21 Nov kept as golden_twins_rhombic-run1.log): the embedding fixing sqrt2 and flipping sqrt3, sqrt5
# sends each cut to the OTHER one.  Exact check of that pairing, and that it is the only non-trivial embedding giving a real cut.
emb = {r2: sqrt(2), r3: -sqrt(3), r5: -sqrt(5)}; idm = {r2: sqrt(2), r3: sqrt(3), r5: sqrt(5)}
for n1, n2 in [('greater', 'lesser'), ('lesser', 'greater')]:
    check(f'RD: sigma(sqrt3 -> -sqrt3, sqrt5 -> -sqrt5, sqrt2 fixed) sends the {n1} golden cut exactly to the {n2} one (y_sharp and y_blunt)',
          all(sp.simplify(sp.radsimp(C[n1][k].subs(emb) - C[n2][k].subs(idm))) == 0 for k in ('ys', 'yb')))
check('RD: sigma(K) = -K for that embedding (the reason: b = 1/(1 + phi K) -> 1/(1 + K/phi))', sp.simplify((K.subs(emb) + K.subs(idm))) == 0)
check('RD: every other non-trivial embedding gives no real cut', set(real_twins) == {t for t in real_twins if 'sqrt2->+sqrt2, sqrt3->-sqrt3, sqrt5->-sqrt5' in t} and len(real_twins) == 2)

# ---------- RT: tan(alpha/2) = 1/phi; sin(alpha/2) = 1/s, cos(alpha/2) = phi/s with s = sqrt(2 + phi) = sqrt((5 + sqrt5)/2);
# field Q(s), s^4 - 5 s^2 + 5 = 0, sqrt5 = 2 s^2 - 5; four embeddings s -> the four real roots of s^4 - 5 s^2 + 5.
s = sp.Symbol('s')
p5 = 2 * s ** 2 - 5; phiS = (1 + p5) / 2
sh, bl = 1 / s, phiS / s
K = (1 / sh + 1 / bl) / 2
roots = sorted(sp.Poly(s ** 4 - 5 * s ** 2 + 5, s).all_roots(), key=lambda r: -sp.N(r))
check('RT: s^4 - 5 s^2 + 5 has four real roots +-sqrt((5 +- sqrt5)/2)', len(roots) == 4 and all(r.is_real for r in roots))
s0 = sqrt((5 + sqrt(5)) / 2)
check('RT: K = phi sqrt(2 + phi)/2 as in #89 (at s = sqrt((5 + sqrt5)/2))', sp.simplify(sp.radsimp(K.subs(s, s0)) - ((1 + sqrt(5)) / 2) * s0 / 2) == 0)
C = cut(K, sh, bl, phiS)
real_twins = {}
for r in roots:
    rr = sp.radsimp(sp.sqrtdenest(sp.nsimplify(r))) if False else r
    for name, d in C.items():
        ys, yb, a, b = [sp.N(d[k].subs(s, r), 40) for k in ('ys', 'yb', 'a', 'b')]
        # exact sign decisions: each quantity is an element of Q(s); its value at a root is decided by its minimal polynomial's
        # real roots isolated in intervals (sympy RootOf). We evaluate at 40 digits and confirm the sign exactly below.
        ok = valid(ys, yb)
        is_id = abs(sp.N(r - s0, 30)) < 1e-25
        tag = f'RT {name} cut, s -> {sp.N(r, 12)}'
        print(f'    {tag}: y_sharp = {sp.N(ys, 12)}, y_blunt = {sp.N(yb, 12)}, sum = {sp.N(ys + yb, 12)}  -> {"REAL SOLID" if ok else "no solid"}')
        # exact confirmation of each decisive sign: the quantity q (in Q(s)) has a minimal polynomial; its value at this root is a
        # real root of it, isolated from the others by sympy's exact real-root isolation
        for qn, q in (('y_sharp', d['ys']), ('y_blunt', d['yb']), ('1 - y_sharp - y_blunt', 1 - d['ys'] - d['yb'])):
            val = sp.N(q.subs(s, r), 50)
            mp = sp.minimal_polynomial(sp.radsimp(q.subs(s, r)), sp.Symbol('z'))
            rts = sp.Poly(mp, sp.Symbol('z')).intervals()
            hit = [iv for iv, m in rts if iv[0] <= val <= iv[1]]
            okiso = len(hit) == 1 and (hit[0][0] > 0 or hit[0][1] < 0)
            if not okiso:
                rts = sp.Poly(mp, sp.Symbol('z')).intervals(eps=Q(1, 10 ** 12))
                hit = [iv for iv, m in rts if iv[0] <= val <= iv[1]]
                okiso = len(hit) == 1 and (hit[0][0] > 0 or hit[0][1] < 0)
            check(f'      exact sign of {qn} ({tag}): isolating interval of its minimal polynomial excludes 0', okiso)
        if is_id:
            check(f'RT {name}: identity embedding reproduces #89 Table 2 and is a real solid', ok and
                  abs(a - (0.463634 if name == 'greater' else 0.316769)) < 1e-6 and abs(b - (0.286541 if name == 'greater' else 0.512543)) < 1e-6)
        elif ok:
            real_twins[tag] = (ys, yb)
print('RT real twins:', real_twins if real_twins else 'none')
check('RT: no Galois conjugate of either golden cut (3 non-trivial embeddings x 2 cuts) is a real cut', not real_twins)
print('FINAL ok' if not FAIL else f'FINAL FAIL {FAIL}')
