"""Aim 2, chunk 5c lead (b) (12 Nov 2026): the zero curve N = 0 of the whole-yantra form of the DICTO Yantra (degree 24).
Genus, singular points, real components, and how it meets the marmas, the bindu centre and the circle.
R1 (exact, the same crossing pattern) is done EXACTLY where possible (PARI resultants and gcd over Q); the DICTO Yantra (GF1, degree 160)
at 300 and 600 digits. Usage: python -u zero_curve.py [pilot]"""
import sys, os, json, math, time
from fractions import Fraction as Fr
from multiprocessing import get_context

PILOT = sys.argv[1:] == ['pilot']
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-12-yantra-regions-canonical', 'scripts'))
sys.path.insert(0, BASE)
import yantra_regions as B
from yantra_regions import Ctx, vertex_form, arrangement, grid, interpolate, Lval, GRID


def numerator(K, Y):
    """coefficients C[a][b] of N = Omega_Y * prod(27 side lines), x^a y^b; and the 18 marmas."""
    A = arrangement(K, Y)
    odd = [f for f in A['faces'] if f['c'] % 2]
    xs, ys = grid(K, A['lines'])
    vals = [[sum(vertex_form(f['V'], (x, y)) for f in odd) * math.prod(Lval(l, (x, y)) for l in A['lines']) for y in ys] for x in xs]
    return interpolate(K, xs, ys, vals), A


def pstr(v, K):
    if K.exact: return f'({Fr(v).numerator}/{Fr(v).denominator})'
    return '(' + K.mp.nstr(v, K.dps + 5, strip_zeros=False, min_fixed=-1, max_fixed=-1).replace('e', 'E') + ')'


def task(arg):
    try:
        return task_(arg)
    except Exception as e:                     # PARI errors are not picklable: hand back text
        import traceback
        return f'{arg[0]}@{arg[1]}', False, ['FAIL exception: ' + type(e).__name__ + ': ' + str(e)[:2000], traceback.format_exc()[-3000:]], {}


def task_(arg):
    name, dps = arg
    out = []; log = out.append; ok = True; res = {}
    def check(c, m):
        nonlocal ok
        ok = ok and bool(c); log(('ok   ' if c else 'FAIL ') + m)
    def find(m): log('FIND ' + m)
    t0 = time.time()
    import cypari2
    pari = cypari2.Pari(); pari.allocatemem(2 * 10 ** 9)
    if name == 'R1':
        K = Ctx(None); Y = B.load_r1(K); prec = dps
    elif name == 'R1num':                      # positive control of the numerical route: R1 through it must give the exact answer
        K = Ctx(dps); Y = B.load_r1(K); prec = dps
    else:
        K = Ctx(dps); Y, ok0 = B.load_gf1(K, log); check(ok0, f'{name}@{dps}: DICTO Yantra rebuilt from its degree-160 polynomial'); prec = dps
    nm = f'{name}' + ('' if K.exact else f'@{dps}')
    pari(f'default(realprecision, {prec})')
    C, A = numerator(K, Y)
    n = len(C)
    cscale = max(abs(C[a][b]) for a in range(n) for b in range(n))
    tol = (lambda v: v == 0) if K.exact else (lambda v: abs(v) <= K.mp.mpf(10) ** (-(dps // 2)) * cscale)
    deg = max(a + b for a in range(n) for b in range(n) if not tol(C[a][b]))
    even = all(tol(C[a][b]) for a in range(1, n, 2) for b in range(n))
    check(deg == 24 and even, f'{nm}: N has degree {deg} and is even in x (N(x, y) = M(x^2, y); mirror symmetry)')
    # M(s, y) = N(sqrt s, y) as a PARI polynomial in x (= s) and y; tiny numerical coefficients cleaned to exact 0
    terms = [f'{pstr(C[a][b] / cscale, K)}*x^{a // 2}*y^{b}' for a in range(0, n, 2) for b in range(n) if not tol(C[a][b])]
    pari('M = ' + '+'.join(terms))
    lcy = pari('pollead(M, y)')
    find(f'{nm}: leading coefficient of N in y: {str(lcy)[:40]} (a constant: no vertical asymptotes)')
    res['lc_y_const'] = pari('poldegree(pollead(M, y), x)') == 0
    # top form: points at infinity
    pari(f'N24 = sum(a = 0, 12, polcoef(polcoef(M, a, x), 24 - 2 * a, y) * t^(2 * a))')
    r24 = pari('polroots(N24)')
    nre = sum(1 for r in r24 if abs(float(pari.imag(r))) < 1e-20)
    dmin = min(float(pari.abs(r24[i] - r24[j])) for i in range(len(r24)) for j in range(i))
    d24 = int(pari('poldegree(N24)'))
    find(f'{nm}: points at infinity: top form N24 = y^{24 - d24} * (degree {d24} in t = x/y; y^24 coefficient nonzero: {pari("polcoef(N24, 0) != 0")}); '
         f'its {d24} finite roots are distinct (min distance {dmin:.3g}) and nonzero: {d24} simple points at infinity, {nre} of them real; '
         f'the factor y^{24 - d24} is the horizontal point (1:0:0), where the 9 parallel bases meet')
    res['inf_real'] = nre; res['inf_squarefree'] = dmin > 1e-30
    # the horizontal point (1:0:0): chart x = 1, coordinates (y, z): multiplicity 24 - deg_x N; tangent cone = coefficient of x^(deg_x N), a form in y
    dx = max(a for a in range(0, n, 2) for b in range(n) if not tol(C[a][b]))
    mult = 24 - dx
    pari(f'Lx = polcoef(M, {dx // 2}, x)')
    dL = int(pari('poldegree(Lx, y)'))
    if K.exact: sqf8 = int(pari('poldegree(gcd(Lx, deriv(Lx, y)))')) == 0; rL = pari('polroots(Lx * 1.)')
    else: rL = pari('polroots(Lx)'); sqf8 = min(float(pari.abs(rL[i] - rL[j])) for i in range(len(rL)) for j in range(i)) > 1e-30
    nrL = sum(1 for r in rL if abs(float(pari.imag(r))) < 1e-20)
    res['inf8'] = {'mult': mult, 'tangents': dL, 'squarefree': bool(sqf8), 'real_tangents': nrL}
    res['inf8_ok'] = mult == 24 - d24 and dL == mult and sqf8
    find(f'{nm}: at (1:0:0) N = 0 has a point of multiplicity {mult} (deg_x N = {dx}); its {dL} tangent lines are the horizontal lines y = r with '
         f'Lx(r) = 0 (Lx = coefficient of x^{dx}), {"distinct" if sqf8 else "NOT distinct"}{" (exact gcd)" if K.exact else ""}, {nrL} real: an ordinary '
         f'{mult}-fold point (delta = {mult * (mult - 1) // 2}), the lemma of 5c at infinity (9 lines through one point, alternate sectors cancel: '
         f'order 9 - 1 = 8); the real tangents are horizontal asymptotes')
    # singular points. Off the axis x = 0: singular points of M (M = M_s = M_y = 0); on the axis: double roots of N(0, y).
    if K.exact:
        t1 = time.time()
        pari('Ar = polresultant(M, deriv(M, y), y); Br = polresultant(deriv(M, x), deriv(M, y), y); G = gcd(Ar, Br); FG = factor(G)')
        degA, degB, degG = int(pari('poldegree(Ar)')), int(pari('poldegree(Br)')), int(pari('poldegree(G)'))
        fac = [(int(pari(f'poldegree(FG[{i},1])')), int(pari(f'FG[{i},2]'))) for i in range(1, int(pari('#FG[,1]')) + 1)]
        find(f'{nm}: EXACT: Res_y(M, M_y) degree {degA}, Res_y(M_s, M_y) degree {degB}, their gcd G degree {degG}, factors (degree, power) {fac} '
             f'({time.time() - t1:.0f} s)')
        sing = []
        for i in range(1, int(pari('#FG[,1]')) + 1):
            if int(pari(f'poldegree(FG[{i},1])')) != 1:
                find(f'{nm}: EXACT: factor of G of degree > 1: not settled'); sing.append(('?', i)); continue
            pari(f's0 = -polcoef(FG[{i},1], 0) / polcoef(FG[{i},1], 1); P0 = subst(M, x, s0); gg = gcd(gcd(P0, deriv(P0, y)), subst(deriv(M, x), x, s0))')
            dg = int(pari('poldegree(gg, y)'))
            if dg == 1: sing.append((Fr(str(pari('s0'))), Fr(str(pari('-polcoef(gg, 0) / polcoef(gg, 1)')))))
            elif dg > 1: sing.append(('?', i)); find(f'{nm}: EXACT: {dg} singular points over one s value')
        corners = [(Y[i][1], Y[i][0]) for i in range(1, 10)] + [(0 * Y[i][1], Y[i][2]) for i in range(1, 10)]
        mar = {(p[0] ** 2, p[1]) for p in A['pts'] if p[0] > 0 and p not in corners and sum(1 for l in A['lines'] if Lval(l, p) == 0) == 3}
        find(f'{nm}: EXACT: singular points of M off the axis: {len(sing)}; marmas (x^2, y) on the right half: {len(mar)}; '
             f'the two sets are equal: {set(sing) == mar}')
        res['exact_sing'] = len(sing)
        res['exact_sing_are_marmas'] = set(sing) == mar
        pari('A0 = subst(M, x, 0)')
        sqf = int(pari('poldegree(gcd(A0, deriv(A0, y)))')) == 0
        find(f'{nm}: EXACT: on the axis x = 0, N(0, y) is squarefree: {sqf} (no singular point on the axis)')
        res['axis_ok'] = sqf
        pari('Ap = Ar')
    else:
        # A(s) = Res_y(M, M_y), B(s) = Res_y(M_s, M_y): exact resultants of the integer polynomial Mi = round(M * 10^60), which is
        # within 10^-60 of M (coefficients scaled to at most 1); their roots then serve as starting points, refined on M itself
        t1 = time.time()
        pari(f'My = deriv(M, y); Ms = deriv(M, x); Mi = round(M * 10^60); '
             f'Ap = polresultant(Mi, deriv(Mi, y), y); Bp = polresultant(deriv(Mi, x), deriv(Mi, y), y)')
        degA, degB = int(pari('poldegree(Ap)')), int(pari('poldegree(Bp)'))
        find(f'{nm}: Res_y(M, M_y) degree {degA}, Res_y(M_s, M_y) degree {degB} (exact resultants of M rounded to 60 digits, used only for starting points, '
             f'{time.time() - t1:.0f} s)')
        res['degA'], res['degB'] = degA, degB
        mar = [(p[0] ** 2, p[1]) for p in A['pts'] if sum(1 for l in A['lines'] if K.zero(Lval(l, p), 1)) == 3 and p[0] > 0]
        mar = [m for m in mar if not any(K.zero(m[0] - c[0] ** 2) and K.zero(m[1] - c[1]) for c in
                                         [(Y[i][1], Y[i][0]) for i in range(1, 10)] + [(0 * Y[i][1], Y[i][2]) for i in range(1, 10)])]
        pari('MAR = [' + ','.join(f'[{pstr(a, K)}, {pstr(b, K)}]' for a, b in mar) + ']')
        pari('Mabs = sum(a = 0, 12, sum(b = 0, 24, abs(polcoef(polcoef(M, a, x), b, y)) * x^a * y^b))')
        # candidates from the roots of B, then Newton on (M_s, M_y) = 0 at full precision, then the test M = 0
        pari('Mss = deriv(Ms, x); Msy = deriv(Ms, y); Myy = deriv(My, y)')
        pari(f'thr = 10^(-{dps // 3}); rB = polroots(Bp); S = List(); ncand = 0; '
             f'for(i = 1, #rB, my(s0 = rB[i]); if(abs(s0) < 1E-30, next); my(yr = polroots(subst(My, x, s0))); '
             f'for(j = 1, #yr, my(y0 = yr[j], sc = substvec(Mabs, [x, y], [abs(s0), abs(y0)]), s1 = s0, y1 = y0); '
             f'if(abs(substvec(Ms, [x, y], [s0, y0])) <= sc * 1E-6 && abs(substvec(M, [x, y], [s0, y0])) <= sc * 1E-6, ncand++; '
             f'for(it = 1, 80, my(v = [substvec(Ms, [x, y], [s1, y1]), substvec(My, [x, y], [s1, y1])]~, '
             f'J = [substvec(Mss, [x, y], [s1, y1]), substvec(Msy, [x, y], [s1, y1]); substvec(Msy, [x, y], [s1, y1]), substvec(Myy, [x, y], [s1, y1])], '
             f'd = iferr(matsolve(J, v), E, 0)); conv = 0; if(d == 0, break); s1 -= d[1]; y1 -= d[2]; if(abs(d[1]) + abs(d[2]) < 10^(-{dps // 2}) * (1 + abs(s1) + abs(y1)), conv = 1); if(conv || abs(s1) + abs(y1) > 1E4, break)); '
             f'my(sc1 = substvec(Mabs, [x, y], [abs(s1), abs(y1)])); '
             f'if(conv && abs(s1) > 1E-30 && abs(s1) + abs(y1) < 1E4 && abs(substvec(M, [x, y], [s1, y1])) <= sc1 * thr && abs(substvec(Ms, [x, y], [s1, y1])) <= sc1 * thr '
             f'&& abs(substvec(My, [x, y], [s1, y1])) <= sc1 * thr, '
             f'if(!sum(k = 1, #S, abs(S[k][1] - s1) < 1E-40 && abs(S[k][2] - y1) < 1E-40), listput(S, [s1, y1]))))))')
        nsing = int(pari('#S'))
        nmar = int(pari('sum(k = 1, #S, sum(m = 1, #MAR, abs(S[k][1] - MAR[m][1]) < 1E-40 && abs(S[k][2] - MAR[m][2]) < 1E-40) > 0)'))
        res['sing'] = nsing
        find(f'{nm}: singular points of M off the axis (M = M_s = M_y = 0, s != 0; {int(pari("ncand"))} candidates from the roots of '
             f'Res_y(M_s, M_y), refined by Newton): {nsing}, of which {nmar} are (x^2, y) of the {len(mar)} right-hand marmas (each gives the two mirror marmas)')
        res['sing_marma'] = nmar
        pari('A0 = subst(M, x, 0); r0 = polroots(A0)')
        d0 = min(float(pari(f'abs(r0[{i}] - r0[{j}])')) for i in range(1, 25) for j in range(1, i))
        find(f'{nm}: on the axis x = 0: the 24 roots of N(0, y) are distinct (min distance {d0:.3g}): no singular point on the axis')
        res['axis_ok'] = d0 > 1e-30
        res['sing_ok'] = nsing == nmar == 9 and res['axis_ok'] and res['inf_squarefree']
    # node type at the marmas (Hessian of N), genus and irreducibility (Bezout: two components of degrees d1 + d2 = 24 meet in d1 d2 >= 23 points)
    nodes = 18
    allnode = ((res.get('exact_sing') == 9 and res.get('exact_sing_are_marmas') and res['axis_ok']) if K.exact else res['sing_ok']) \
        and res['inf_squarefree'] and res['inf8_ok']
    if allnode:
        g = 253 - 18 - mult * (mult - 1) // 2
        find(f'{nm}: the singular points of N = 0 (affine and at infinity, real and complex) are the 18 marmas, each an ordinary double point '
             f'(order 2, Hessian definite: 5c point table), and the ordinary {mult}-fold point (1:0:0). Irreducible over C: components of degrees '
             f'a + b = 24 meet in ab points counted with multiplicity, all at singular points; the nodes give at most 18 and (1:0:0) at most '
             f'm_A m_B <= 16, so ab <= 34, which leaves only a = 1, a line; a non-horizontal line misses (1:0:0) and would need 23 nodes, a '
             f'horizontal line holds at most 2 marmas (mirror pairs) and gets 7 from (1:0:0): 9 < 23. Genus = 253 - 18 - {mult * (mult - 1) // 2} = {g}')
        res['genus'] = g
    else:
        find(f'{nm}: singular points beyond the marmas present or not settled: genus not stated')
        res['genus'] = None
    # real topology (numerical, at 120 digits): branches over the critical x values, joined through critical points and through infinity
    pari('default(realprecision, 120)')
    pari('Mr = M * 1.')
    pari('Adet(s) = my(P = subst(M, x, s)); matdet(polsylvestermatrix(P, deriv(P, y)))')
    pari('RR(x0) = my(r = polroots(subst(Mr, x, x0^2))); vecsort([real(v) | v <- r, abs(imag(v)) < 1E-30])')
    pari('rA = polroots(Ap); CS = List(); '
         'for(i = 1, #rA, if(abs(imag(rA[i])) < 1E-25 && real(rA[i]) >= 0, my(s1 = real(rA[i]), h = 1E-40); '
         'for(it = 1, 40, my(f0 = Adet(s1), f1 = Adet(s1 + h)); if(f1 == f0, break); my(d = f0 * h / (f1 - f0)); s1 -= d; if(abs(d) < 1E-100, break)); '
         'if(!sum(k = 1, #CS, abs(CS[k] - s1) < 1E-30), listput(CS, s1)))); '
         'CX = vecsort(concat([sqrt(c) | c <- Vec(CS)], [-sqrt(c) | c <- Vec(CS)])); '
         'CX = vecsort(CX, , 8)')
    ncx = int(pari('#CX'))
    xs = list(range(1, ncx + 1))
    def realroots(expr):
        return [float(v) for v in pari(f'RR({expr})')]
    par = list(range(100000)); cnt = [0]
    def fnd(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    def uni(a, b): par[fnd(a)] = fnd(b)
    def ids(k): s = cnt[0]; cnt[0] += k; return list(range(s, s + k))
    Xbig = 1000 * (float(pari('vecmax(abs(CX))')) + 10)
    left = realroots(f'{-Xbig:.6E}'); L_ids = ids(len(left)); inf_minus = list(zip(L_ids, [y / -Xbig for y in left]))
    prev = (left, L_ids); bad = 0
    for xc in xs:
        a, b = realroots(f'CX[{xc}] - 1E-20'), realroots(f'CX[{xc}] + 1E-20')
        if len(a) != len(prev[0]): bad += 1
        ia = ids(len(a)); ib = ids(len(b))
        for i in range(min(len(a), len(prev[0]))): uni(prev[1][i], ia[i])
        used_a, used_b = set(), set()
        for i, ya in enumerate(a):
            j = min(range(len(b)), key=lambda j: abs(b[j] - ya), default=None)
            if j is not None and abs(b[j] - ya) < 1e-14 * (1 + abs(ya)) and j not in used_b: uni(ia[i], ib[j]); used_a.add(i); used_b.add(j)
        un = [(ya, ia[i]) for i, ya in enumerate(a) if i not in used_a] + [(yb, ib[j]) for j, yb in enumerate(b) if j not in used_b]
        un.sort()
        for k in range(1, len(un)):
            if abs(un[k][0] - un[k - 1][0]) < 1e-6: uni(un[k][1], un[k - 1][1])
        prev = (b, ib)
    right = realroots(f'{Xbig:.6E}'); R_ids = ids(len(right))
    if len(right) != len(prev[0]): bad += 1
    for i in range(min(len(right), len(prev[0]))): uni(prev[1][i], R_ids[i])
    allids = list(range(cnt[0]))
    comps = {fnd(i) for i in allids}
    unb = {fnd(i) for i in L_ids + R_ids}
    affine = len(comps); bounded = len(comps - unb)
    rre = [float(pari.real(r)) for r in rL if abs(float(pari.imag(r))) < 1e-20]      # the real horizontal asymptotes y = r
    ish = lambda y: any(abs(y - r) < 1e-2 * (1 + abs(r)) for r in rre)
    hor = [ia_ for ia_, y in zip(L_ids, left) if ish(y)] + [ib_ for ib_, y in zip(R_ids, right) if ish(y)]
    for h in hor[1:]: uni(h, hor[0])                 # horizontal asymptotes all end in the one point (1:0:0)
    for i, (ia_, sl) in enumerate(inf_minus):        # other ends: slope y/x at -inf meets the same slope at +inf (a simple point at infinity)
        if ia_ in hor: continue
        j = min((j for j in range(len(right)) if R_ids[j] not in hor), key=lambda j: abs(right[j] / Xbig - sl), default=None)
        if j is not None and abs(right[j] / Xbig - sl) < 1e-3: uni(ia_, R_ids[j])
    res['horizontal_ends'] = len(hor)
    proj = len({fnd(i) for i in allids})
    find(f'{nm}: real picture (numerical, 120 digits, {len(xs)} critical x values, {bad} count mismatches): {affine} connected pieces in the plane, '
         f'{bounded} of them closed ovals, {affine - bounded} running to infinity ({len(left)} + {len(right)} ends); in the projective plane '
         f'{proj} real components of one dimension ({len(hor)} ends on horizontal asymptotes, all joined at (1:0:0)), plus the 18 marmas as isolated real points')
    res['real'] = {'affine': affine, 'ovals': bounded, 'unbounded': affine - bounded, 'projective': proj, 'mismatch': bad, 'ends': (len(left), len(right))}
    # the bindu centre and the circle x^2 + y^2 = y (diameter 1, y = depth): N on the circle via x = t/(1+t^2), y = t^2/(1+t^2)
    Nc = pari('subst(subst(Mr, x, 0), y, 1/2)')
    pari('Ev(t) = substvec(Mr, [x, y], [(t / (1 + t^2))^2, t^2 / (1 + t^2)]) * (1 + t^2)^24')
    pari('nc = 64; z = exp(2 * Pi * I / nc); '
         'vC = vector(nc, k, Ev(z^(k-1) / 2)); cC = vector(nc, j, real(sum(k = 1, nc, vC[k] * z^(-(j-1)*(k-1))) / nc) * 2^(j-1));'
         'mC = vecmax(abs(cC)); dC = 0; for(j = 1, nc, if(abs(cC[j]) > mC * 1E-60, dC = j)); PC = Polrev(cC[1..dC]); rC = polroots(PC)')
    rc = [r for r in pari('rC') if abs(float(pari.imag(r))) < 1e-30]
    find(f'{nm}: N at the circle centre (0, 1/2) = {float(Nc):.6g} (not zero: the curve misses the bindu centre); on the circle N has '
         f'{len(rc)} real zeros (degree {int(pari("poldegree(PC)"))} in the circle parameter), all simple: '
         f'{min((float(pari.abs(rc[i] - rc[j])) for i in range(len(rc)) for j in range(i)), default=1) > 1e-20}')
    res['circle_real'] = len(rc)
    log(f'{nm}: {time.time() - t0:.0f} s')
    return nm, ok, out, res


def main():
    t0 = time.time()
    tasks = [('R1', 200), ('R1num', 150), ('GF1', 150)] if PILOT else [('R1', 300), ('R1num', 300), ('GF1', 300), ('GF1', 600)]
    print(f'chunk 5c lead (b): {len(tasks)} tasks', flush=True)
    results = {}; ok = True
    with get_context('fork').Pool(4) as pool:
        its = [pool.apply_async(task, (t,)) for t in tasks]
        for d, it in enumerate(its):
            name, good, out, res = it.get()
            for line in out: print(line, flush=True)
            print(f'PROGRESS {(d + 1) / len(tasks):.2f} {name}', flush=True)
            results[name] = res; ok = ok and good
    def say(c, m):
        nonlocal ok
        ok = ok and bool(c); print(('ok   ' if c else 'FAIL ') + m, flush=True)
    g = [v for k, v in results.items() if k.startswith('GF1')]
    rn = [v for k, v in results.items() if k.startswith('R1num')][0]
    if not all(results.values()): print('FAIL a task crashed (see its lines)', flush=True); print('FINAL FAIL', flush=True); return
    say(rn['sing_ok'] and rn['genus'] == results['R1']['genus'] and rn['real'] == results['R1']['real'],
        'positive control: R1 through the numerical route gives the exact R1 answer (the 18 marmas only, genus, same real picture)')
    r1 = results.get('R1') or results.get('R1@200') or results.get('R1@300')
    say(all(x['sing_ok'] for x in g), 'DICTO Yantra: the only singular points found are the 18 marmas (each precision)')
    if len(g) == 2:
        say(g[0]['real'] == g[1]['real'] and g[0]['degA'] == g[1]['degA'] and g[0]['circle_real'] == g[1]['circle_real'],
            'DICTO Yantra at 300 and 600 digits: same resultant degrees, singular points, real picture, circle zeros')
    print(f'R1 (exact singular points) genus {r1.get("genus")}, real {r1.get("real")}; DICTO Yantra genus {g[0].get("genus")}, real {g[0].get("real")}', flush=True)
    json.dump(results, open(os.path.join(HERE, '..', 'data', 'zero-curve-pilot.json' if PILOT else 'zero-curve.json'), 'w'), indent=1, default=str)
    print(f'total {time.time() - t0:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL: see the FAIL lines above', flush=True)


if __name__ == '__main__':
    main()
