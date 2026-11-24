# Independent recheck of Theorem 1 (CIRT-30) of study 2026-11-24-aequi-exact-dice.
# Method (own code): exact vertex enumeration in Q(sqrt5) for rational s = t*sqrt3, exact face cycles,
# then each face's solid angle by Girard's formula (angle sum minus (k-2)pi) in arb ball arithmetic.
import sys, itertools, json
from fractions import Fraction as F
import flint
from flint import arb
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from qr import Q, dot, cross, solve3

flint.ctx.prec = 600
S5 = arb(5).sqrt(); PI = arb.pi()
phi = Q(F(1, 2), F(1, 2)); iphi = phi - 1
z, one = Q(0), Q(1)


def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]


def planes(s):
    P = []
    for v in cyc((one, z, z)):
        for sg in (1, -1): P.append(('C', tuple(sg * x for x in v), Q(1)))
    for v in cyc((z, iphi, phi)):
        nz = [i for i in range(3) if not v[i].iszero()]
        for a in (1, -1):
            for b in (1, -1):
                w = list(v); w[nz[0]] = a * w[nz[0]]; w[nz[1]] = b * w[nz[1]]
                P.append(('I', tuple(w), Q(s)))
    for v in cyc((phi, iphi, one)):            # RT24/12a: even number of minus signs
        for sg in itertools.product((1, -1), repeat=3):
            if sg[0] * sg[1] * sg[2] == 1:
                P.append(('R', tuple(g * x for g, x in zip(sg, v)), Q(2)))
    return P


def toarb(q): return arb(q.a.numerator) / q.a.denominator + arb(q.b.numerator) / q.b.denominator * S5


def solid_angles(s):
    P = planes(s); n = len(P)
    assert [p[0] for p in P].count('C') == 6 and [p[0] for p in P].count('I') == 12 and [p[0] for p in P].count('R') == 12
    verts = {}
    for i, j, k in itertools.combinations(range(n), 3):
        x = solve3([P[i][1], P[j][1], P[k][1]], [P[i][2], P[j][2], P[k][2]])
        if x is None or x in verts: continue
        if all((dot(p[1], x) - p[2]).sign() <= 0 for p in P): verts[x] = None
    V = list(verts)
    faces = []
    for (lab, nrm, h) in P:
        on = [v for v in V if (dot(nrm, v) - h).iszero()]
        if len(on) < 3: faces.append((lab, [])); continue
        # order around the face: sort by angle (floats), then verify exact convex cycle
        import math
        c = [sum(float(v[i]) for v in on) / len(on) for i in range(3)]
        nf = [float(x) for x in nrm]
        e1 = [float(on[0][i]) - c[i] for i in range(3)]
        e2 = [nf[1] * e1[2] - nf[2] * e1[1], nf[2] * e1[0] - nf[0] * e1[2], nf[0] * e1[1] - nf[1] * e1[0]]
        ang = lambda v: math.atan2(sum((float(v[i]) - c[i]) * e2[i] for i in range(3)), sum((float(v[i]) - c[i]) * e1[i] for i in range(3)))
        on.sort(key=ang)
        k = len(on)
        for a in range(k):
            A, B, C = on[a], on[(a + 1) % k], on[(a + 2) % k]
            d1 = tuple(B[i] - A[i] for i in range(3)); d2 = tuple(C[i] - B[i] for i in range(3))
            assert dot(nrm, cross(d1, d2)).sign() > 0, 'face cycle not strictly convex'
        faces.append((lab, on))
    # Euler check on the exact structure
    E = sum(len(f) for _, f in faces if f) // 2; Fc = sum(1 for _, f in faces if f)
    assert len(V) - E + Fc == 2, ('Euler', len(V), E, Fc)
    om = {'C': [], 'I': [], 'R': []}
    for lab, on in faces:
        if not on: om[lab].append(arb(0)); continue
        W = [[toarb(x) for x in v] for v in on]; k = len(W); tot = arb(0)
        for a in range(k):
            A, B, C = W[a - 1], W[a], W[(a + 1) % k]
            bb = sum(x * x for x in B)
            tA = [A[i] - sum(A[j] * B[j] for j in range(3)) / bb * B[i] for i in range(3)]
            tC = [C[i] - sum(C[j] * B[j] for j in range(3)) / bb * B[i] for i in range(3)]
            cr = [tA[1] * tC[2] - tA[2] * tC[1], tA[2] * tC[0] - tA[0] * tC[2], tA[0] * tC[1] - tA[1] * tC[0]]
            tot += arb.atan2(sum(x * x for x in cr).sqrt(), sum(tA[i] * tC[i] for i in range(3)))
        om[lab].append(tot - (k - 2) * PI)
    # all faces of one orbit agree (symmetry T), and total 4pi
    for lab in om:
        for w in om[lab]: assert (w - om[lab][0]).contains(0) if True else None
    total = sum(om['C']) + sum(om['I']) + sum(om['R'])
    assert (total - 4 * PI).contains(0) and abs(float((total - 4 * PI).mid())) < 1e-150
    return om['C'][0], om['R'][0], om['I'][0], len(V), [len(f) for _, f in faces]


def fmt(x, d=60): return x.str(d, radius=True)


if __name__ == '__main__':
    out = {}
    target = 4 * PI / 30
    print('identity 2*Om_R - Om_C - 4pi/30 at s = t*sqrt3:')
    for s in [F(17, 10), F(172, 100), F(174, 100), F(7, 4), F(1751, 1000), F(1758, 1000), F(176, 100), F(18, 10), F(2), F(5, 2), F(3)]:
        oc, orr, oi, nv, fs = solid_angles(s)
        idv = 2 * orr - oc - target
        rad = float(idv.rad()); mid = float(idv.mid())
        holds = idv.contains(0)
        print(f's={s} ({float(s):.4f})  corners={nv}  value={fmt(idv, 20)}  |value|<={abs(mid)+rad:.2e}  contains0={holds}  Om_I-4pi/30={fmt(oi - target, 15)}')
        out[str(s)] = dict(corners=nv, identity=fmt(idv, 30), bound=abs(mid) + rad, contains0=bool(holds), OmI_minus=fmt(oi - target, 20))
    # fair point: root of 16x^4-40x^3-100x^2+130x+145 near 1.7579
    import mpmath
    mpmath.mp.dps = 80
    x = mpmath.findroot(lambda x: 16 * x**4 - 40 * x**3 - 100 * x**2 + 130 * x + 145, 1.7579)
    print('quartic root x =', mpmath.nstr(x, 50), ' x/sqrt3 =', mpmath.nstr(x / mpmath.sqrt(3), 40))
    xs = F(mpmath.nstr(x, 70))
    eps = F(1, 10**40)
    lo, hi = xs - eps, xs + eps
    oc1, or1, oi1, _, _ = solid_angles(lo); oc2, or2, oi2, _, _ = solid_angles(hi)
    d1, d2 = oi1 - target, oi2 - target
    print('Om_I - 4pi/30 at x-1e-40:', fmt(d1, 15), ' at x+1e-40:', fmt(d2, 15))
    sign_change = (d1 > 0) and (d2 < 0)
    print('sign change across [x-1e-40, x+1e-40]:', sign_change)
    print('at x-1e-40: Om_C-4pi/30 =', fmt(oc1 - target, 10), ' Om_R-4pi/30 =', fmt(or1 - target, 10))
    out['tstar'] = dict(x=mpmath.nstr(x, 50), t=mpmath.nstr(x / mpmath.sqrt(3), 40), sign_change=bool(sign_change),
                        OmC_minus=fmt(oc1 - target, 10), OmR_minus=fmt(or1 - target, 10))
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    ok = all(out[k]['contains0'] and out[k]['bound'] < 1e-50 for k in out if k not in ('tstar',) and F(k) >= F(7, 4)) and sign_change
    if ok: print('FINAL ok')
    else: print('FINAL disagree')
