"""Harmony tests for the spherical DICTO Yantra and the spherical Kulaichev Sri Yantra as plane arrangements, and for the
Vacuus of the stella-octangula yantra frame (plate-harmony study, 25 Nov 2026).

Spherical yantra (study 2026-11-08-tetra-yantra, spherical.py): the flat yantra (circle of diameter 1, depth d from the top)
lies on the plane z = 1 touching the unit sphere; the point (x, d) goes to (s x, s(1/2 - d), 1) with s = 2 tan(rho), rho = 60 deg
(the cap of spherical.py). Each of the 27 lines (9 bases, 18 legs) becomes the plane through the centre and that line.

The figures. Both yantras are rebuilt from their defining systems with the construction of #103 (construct(), copied line for
line from studies 2026-11-08-sri-yantra/scripts/breakers_certify.py, itself from the uniqueness studies' s3_backsolve.py):
 - Kulaichev (Huet's conditions, Kulaichev's (a)-(d); v = u): polynomials G, H1, D of study 2026-11-15-yantra-uniqueness;
 - DICTO Yantra (Cleo-Antonius uv = 2/phi^3, with (b)-(d)): polynomials of study 2026-11-15-dicto-yantra-uniqueness.
Each true solution (u, t, S) is certified by the Krawczyk test (exactly one solution in a box of radius 1e-100). Everything
below is Arb ball arithmetic in that box: an inequality is decided when its ball excludes the value; an equality can only be
seen as "inside the box", and is then exact only when it is one of the figure's defining incidences.

Rational angles are decided exactly for one pair by a degree bound. The two legs of the great triangle t7 (apex at the top of
the circle, corners at depth R = 1/(1 + u^2), half-width u/(1 + u^2)) give planes with cos(theta) = (1 - 4u^2)/(1 + 4u^2)
(rho = 60 deg, s^2 = 12), so c = 2cos(2 theta) lies in Q(u^2). u is a root of an even integer polynomial of degree 160 (DICTO)
or 348 (Kulaichev, f348), so [Q(c):Q] <= 80 or 174. If theta = (k/n) pi then [Q(c):Q] = phi(n)/2 (Niven; Conway-Jones), so
n is one of finitely many; for each such n the ball of n theta/pi is checked to hold no integer."""
import os, sys, json, itertools, time
from math import gcd
from fractions import Fraction as Fr
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import flint
from flint import arb, arb_mat
flint.ctx.prec = 1000
ST = os.path.normpath(os.path.join(HERE, "../.."))
KDIR = os.path.join(ST, "2026-11-15-yantra-uniqueness"); DDIR = os.path.join(ST, "2026-11-15-dicto-yantra-uniqueness")
S5 = lambda: arb(5).sqrt()
T0 = time.time()
def say(*a): print(f"[{time.time() - T0:6.1f} s]", *a, flush=True)


# ---------------------------------------------------------------- copied line for line from breakers_certify.py (sri-yantra study)
def load_polys(path, field):
    p = json.load(open(path))
    if field == 'Q': return {k: [(tuple(e), (int(c), 0)) for e, c in p[k]] for k in ('G', 'H1', 'D')}
    return {k: [(tuple(e), (int(c[0]), int(c[1]))) for e, c in p[k]] for k in ('G', 'H1', 'D')}


def kv(c): return c[0] + c[1] * S5() if c[1] else arb(c[0])
def deriv(p, var): return [(tuple(e[i] - (i == var) for i in range(3)), (c[0] * e[var], c[1] * e[var])) for e, c in p if e[var] > 0]


def ev(p, x):
    pw = [{}, {}, {}]
    def pk(i, k):
        if k not in pw[i]: pw[i][k] = x[i] ** k
        return pw[i][k]
    tot = arb(0)
    for e, c in p: tot += kv(c) * pk(0, e[0]) * pk(1, e[1]) * pk(2, e[2])
    return tot


def construct(u, t, S, v):
    one = arb(1)
    P = v**2 / (1 + v**2); R = one / (1 + u**2); w3 = v / (1 + v**2); w7 = u / (1 + u**2)
    b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)
    xW = w7 * P / R; xX = xW * (S - R) / (S - P); k9 = xX / (R - P); w9 = k9 * (S - P)
    k3 = w3 / (1 - P); xZ = k3 * (1 - R)
    c138 = w1 * (R - b1) - xZ * (P - b1); Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
    m1 = w1 / (Q - b1); b8 = (k3 + k9 * P) / (k3 + k9); xF = k9 * (Q - P); w6 = xW * (S - Q) / (S - P); k7 = w7 / R
    b2 = m1 * Q / (m1 + k7); c4 = xF / (b8 - Q); c8 = xZ / (R - b1); b4 = (c4 * b8 + c8 * b1) / (c4 + c8)
    b5 = (m1 * Q + k9 * P) / (m1 + k9); w5 = w6 * (b5 - b2) / (Q - b2)
    b = {1: b1, 2: b2, 3: P, 4: b4, 5: b5, 6: Q, 7: R, 8: b8, 9: S}
    a = {8: b1, 6: b2, 9: P, 1: Q, 5: R, 4: b8, 2: S, 3: one, 7: arb(0)}
    w = {3: w3, 7: w7, 6: w6, 5: w5, 1: m1 * (Q - b1), 2: xW * (S - b2) / (S - P), 4: xF * (b8 - b4) / (b8 - Q),
         8: xZ * (b8 - b1) / (R - b1), 9: w9}
    return b, w, a


def newton_krawczyk(F, x, fixed, rad=arb(10) ** -100):
    vars_ = sorted(x); n = len(vars_)
    J = [[deriv(f, j) for j in vars_] for f in F]
    def full(vals):
        z = [None] * 3
        for k, v in fixed.items(): z[k] = v
        for k, v in zip(vars_, vals): z[k] = v
        return z
    y = [arb(x[k]) for k in vars_]
    for _ in range(40):
        z = full(y); Fy = arb_mat([[ev(f, z)] for f in F]); Jy = arb_mat([[ev(J[i][j], z) for j in range(n)] for i in range(n)])
        d = Jy.mid().inv() * Fy.mid(); y = [arb((y[i] - d[i, 0]).mid()) for i in range(n)]
        if all(abs(d[i, 0].mid()) < arb(10) ** -250 for i in range(n)): break
    X = [arb(v.mid(), rad) for v in y]; z = full(y)
    Fy = arb_mat([[ev(f, z)] for f in F]); Y = arb_mat([[ev(J[i][j], z) for j in range(n)] for i in range(n)]).mid().inv().mid()
    JX = arb_mat([[ev(J[i][j], full(X)) for j in range(n)] for i in range(n)])
    M = arb_mat([[1 if i == j else 0 for j in range(n)] for i in range(n)]) - Y * JX
    K = arb_mat([[y[i]] for i in range(n)]) - Y * Fy + M * arb_mat([[X[i] - y[i]] for i in range(n)])
    ok = all(X[i].contains_interior(K[i, 0]) for i in range(n))
    return ok, full([K[i, 0] for i in range(n)])
# ---------------------------------------------------------------- end of the copied part


def bdot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def bcross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def has0(x): return x.contains(0)
def par(a, b): return all(has0(c) for c in bcross(a, b))


def totients(N):
    ph = list(range(N + 1))
    for p in range(2, N + 1):
        if ph[p] == p:
            for q in range(p, N + 1, p): ph[q] -= ph[q] // p
    return ph


def yantra_arrangement(name, u, t, S, v, D):
    b, w, a = construct(u, t, S, v)
    s = 2 * arb(3).sqrt()            # 2 tan 60 deg
    P = lambda x, d: [s * x, s * (arb(1) / 2 - d), arb(1)]
    lines = []
    for i in range(1, 10):
        L, Rr, A = P(-w[i], b[i]), P(w[i], b[i]), P(arb(0), a[i])
        lines += [(f"base t{i}", bcross(L, Rr)), (f"left leg t{i}", bcross(L, A)), (f"right leg t{i}", bcross(Rr, A))]
    N = [n for _, n in lines]; names = [nm for nm, _ in lines]
    n = len(N)
    for i, j in itertools.combinations(range(n), 2): assert not par(N[i], N[j]), "two equal planes"
    out = {"name": name, "planes": n, "u": u.str(30, radius=False)}
    # intersection points, clustered inside the box
    pts = []
    for i, j in itertools.combinations(range(n), 2):
        c = bcross(N[i], N[j])
        for p in pts:
            if par(p[0], c): p[1].update((i, j)); break
        else:
            pts.append([c, {i, j}])
    mult = Counter(len(S_) for _, S_ in pts)
    f0 = len(pts); f1 = sum(len(S_) for _, S_ in pts)
    b2 = sum(len(S_) - 1 for _, S_ in pts); b3 = b2 - n + 1; R = 2 * (n + b3)
    assert R == 2 * (1 - f0 + f1)
    out.update(lines=f0, line_multiplicities={str(k): v_ for k, v_ in sorted(mult.items())}, regions=R,
               chi=f"(t - 1)(t^2 - {n - 1}t + {b3})", simplicial=2 * f1 == 3 * (1 - f0 + f1))
    out["multiple_points"] = sorted(sorted(names[k] for k in S_) for _, S_ in pts if len(S_) >= 3)
    disc = (n - 1) ** 2 - 4 * b3; sq = int(round(disc ** 0.5)) if disc >= 0 else -1
    out["p7_factors"] = disc >= 0 and sq * sq == disc
    out["p7_free"] = False if not out["p7_factors"] else None
    out["p7_how"] = "chi does not factor over Z (Terao)" if not out["p7_factors"] else "chi factors; freeness not decided (box data)"
    # angles
    nn = [bdot(x, x) for x in N]
    cos2 = {(i, j): bdot(N[i], N[j]) ** 2 / (nn[i] * nn[j]) for i, j in itertools.combinations(range(n), 2)}
    vals = list(cos2.values())
    out["p3_equiangular"] = False if any(not has0(x - vals[0]) for x in vals) else "inside the box only"
    perp = [k for k, x in cos2.items() if has0(x)]
    out["perpendicular_pairs_in_box"] = len(perp)
    out["p4_perp_triples"] = False if len(perp) < n else "undecided"
    # reflection
    refl_no = False
    for i in range(n):
        for j in range(n):
            if i == j: continue
            g = bdot(N[i], N[j]); r = [y - 2 * g / nn[i] * x for x, y in zip(N[i], N[j])]
            if not any(par(r, N[k]) for k in range(n)): refl_no = True; break
        if refl_no: break
    out["reflection"] = False if refl_no else "inside the box only"
    # pencils: order and gaps; regular iff every gap is pi/k
    pi = arb.pi(); pt = {}; allreg = True; lune_fail = None
    for c, S_ in pts:
        idx = sorted(S_); k = len(idx)
        e1 = N[idx[0]]; e2 = bcross(c, e1); n1 = bdot(e1, e1).sqrt(); n2 = bdot(e2, e2).sqrt()
        angs = []
        for i in idx:
            if i == idx[0]: angs.append((arb(0), i)); continue
            a_ = arb.atan2(bdot(N[i], e2) / n2, bdot(N[i], e1) / n1)
            if a_ < 0: a_ += pi
            if a_ >= pi: a_ -= pi
            angs.append((a_, i))
        angs.sort(key=lambda x: float(x[0].mid()))
        gaps = [angs[q + 1][0] - angs[q][0] for q in range(k - 1)] + [pi - angs[-1][0]]
        reg = all(has0(gp - pi / k) for gp in gaps)
        if not reg: allreg = False
        tt = pt.setdefault(k, [0, 0]); tt[0] += 1; tt[1] += reg
        if lune_fail is None:
            for gp in gaps:
                z = gp * R / (2 * pi)
                if not has0(z - z.mid().floor()) and not has0(z - z.mid().floor() - 1):
                    lune_fail = f"a lune of angle {(gp / pi).str(8, radius=False)} pi holds {z.str(8, radius=False)} regions' worth"; break
    out["pencils"] = {str(k): {"count": v_[0], "regular_in_box": v_[1]} for k, v_ in sorted(pt.items())}
    out["p9_all_pencils_regular"] = False if not allreg else "inside the box only"
    out["p5_equal_area"] = False if lune_fail else "undecided"
    out["p5_how"] = "lune test fails (certified): " + lune_fail if lune_fail else "lune test inconclusive"
    # rational angles: the great triangle t7's two leg planes, exactly by a degree bound
    i7l, i7r = names.index("left leg t7"), names.index("right leg t7")
    ct = bdot(N[i7l], N[i7r]) / (nn[i7l] * nn[i7r]).sqrt()
    ct2 = (1 - 4 * u ** 2) / (1 + 4 * u ** 2)
    assert has0(ct - ct2) or has0(ct + ct2), "leg-angle formula"
    th = ct2.acos(); th = th if th <= pi / 2 else pi - th            # acute angle between the planes
    tp = th / pi
    deg = D // 2
    N_ = 8 * (2 * deg) ** 2 + 13
    ph = totients(N_)
    bad = [m_ for m_ in range(1, N_ + 1) if (ph[m_] <= 2 * deg) and (has0(tp * m_ - (tp * m_).mid().floor()) or has0(tp * m_ - (tp * m_).mid().floor() - 1))]
    out["t7_leg_angle_over_pi"] = tp.str(25, radius=False)
    out["t7_leg_angle_rational"] = False if not bad else f"not excluded for n in {bad[:5]}"
    out["p6_rational"] = False if not bad else "undecided"
    out["p6_how"] = (f"t7's leg planes meet at 2 arctan(2u); 2cos(2 theta) lies in Q(u^2) of degree <= {deg}; every n with phi(n) <= {2 * deg} "
                     f"(n <= {N_}) checked: n theta/pi holds no integer (certified)") if not bad else "degree-bound check left n open"
    out["sphericus"] = sphericus_box(N, pts, s, R, pi)
    out["tacitus_crossings"] = tacitus_box(pts)
    return out


def _clusters(balls):
    cl = []
    for x in sorted(balls, key=lambda y: float(y.mid())):
        if cl and cl[-1].overlaps(x): continue
        cl.append(x)
    return len(cl)


def sphericus_box(N, pts, s, R, pi):
    """Sphericus (DICTO's name, 25 Nov; definition to be fixed with him) for box data: (a) histogram of crossing points;
    (b) crossing angles (gaps between neighbouring circles at each point) and (c) arcs between consecutive crossings along
    each great circle, counted as values certified apart (a lower bound; equal values only within the box); the yantra's ring
    (the circle of diameter 1, a small circle of angular radius 60 deg about the pole) and its crossings with the 27 great
    circles: points, how many great circles through each, crossing angles, arcs along the ring."""
    hist = Counter()
    gaps = []; arcs = []
    for c, S_ in pts:
        hist[str(len(S_))] += 2
        idx = sorted(S_); e1 = N[idx[0]]; e2 = bcross(c, e1); n1 = bdot(e1, e1).sqrt(); n2 = bdot(e2, e2).sqrt()
        an = sorted([arb(0)] + [(lambda a_: a_ + pi if a_ < 0 else a_)(arb.atan2(bdot(N[i], e2) / n2, bdot(N[i], e1) / n1)) for i in idx[1:]], key=lambda x: float(x.mid()))
        an = [x - pi if x >= pi else x for x in an]; an.sort(key=lambda x: float(x.mid()))
        gaps += [an[q + 1] - an[q] for q in range(len(an) - 1)] + [pi - an[-1] + an[0]]
    for i in range(len(N)):
        U = [c for c, S_ in pts if i in S_]
        U = [[x / bdot(c, c).sqrt() for x in c] for c in U]
        nn_ = bdot(N[i], N[i]).sqrt(); e1 = U[0]; e2 = [x / nn_ for x in bcross(N[i], e1)]
        half = [arb(0)] + [(lambda a_: a_ + 2 * pi if a_ < 0 else a_)(arb.atan2(bdot(u, e2), bdot(u, e1))) for u in U[1:]]
        half = [h - pi if h >= pi else h for h in half]            # one of each antipodal pair, in [0, pi); the other is +pi
        thb = sorted(half + [h + pi for h in half], key=lambda x: float(x.mid()))
        arcs += [thb[q + 1] - thb[q] for q in range(len(thb) - 1)] + [2 * pi - thb[-1]]
    # the ring: x = (sin r cos f, sin r sin f, cos r), r = 60 deg
    sr, cr = arb(3).sqrt() / 2, arb(1) / 2
    ring = []
    for i, n_ in enumerate(N):
        A, B, C = n_[0] * sr, n_[1] * sr, n_[2] * cr
        h = (A * A + B * B).sqrt(); q_ = -C / h
        if q_ > 1 or q_ < -1: continue
        assert not has0(q_ - 1) and not has0(q_ + 1), "a great circle tangent to the ring (inside the box)"
        f0 = arb.atan2(B, A); d_ = q_.acos()
        for f in (f0 + d_, f0 - d_):
            while f < 0: f += 2 * pi
            while f >= 2 * pi: f -= 2 * pi
            x = [sr * f.cos(), sr * f.sin(), cr]; ts = [-f.sin(), f.cos(), arb(0)]; tg = bcross(n_, x)
            ca = abs(bdot(ts, tg)) / bdot(tg, tg).sqrt()
            ring.append([f, {i}, ca])
    rp = []
    for f, S_, ca in sorted(ring, key=lambda r_: float(r_[0].mid())):
        if rp and rp[-1][0].overlaps(f): rp[-1][1] |= S_; rp[-1][2].append(ca)
        else: rp.append([f, set(S_), [ca]])
    rarcs = [rp[q + 1][0] - rp[q][0] for q in range(len(rp) - 1)] + [2 * pi - rp[-1][0] + rp[0][0]]
    out = {"crossing_points_histogram": dict(sorted(hist.items())), "crossing_angle_values_certified_apart": _clusters(gaps),
           "arc_length_values_certified_apart": _clusters(arcs),
           "ring": {"crossing_points": len(rp), "great_circles_per_point": dict(sorted(Counter(str(len(r_[1])) for r_ in rp).items())),
                    "crossing_angle_values_certified_apart": _clusters([a for r_ in rp for a in r_[2]]),
                    "arc_values_certified_apart": _clusters(rarcs)}}
    out["harmonious_crossing"] = (len(hist) == 1 and out["crossing_angle_values_certified_apart"] == 1 and out["arc_length_values_certified_apart"] == 1) or False
    return out


def tacitus_box(pts):
    """Tacitus of the crossing points (float screen of study 2026-11-25-tacitus; box data, so a silence would be box-level)"""
    sys.path.insert(0, HERE)
    from harmony import _tac
    import numpy as np
    T = _tac()
    X = np.array([[float(x.mid()) for x in c] for c, _ in pts]); X /= np.linalg.norm(X, axis=1)[:, None]
    PP = np.vstack([X, -X]); out = {}
    for var, w in (("unweighted", np.ones(len(PP))), ("weighted", np.array([len(S_) for _, S_ in pts] * 2, float))):
        Rs = T.sym_group(PP, T.labels(w)); dims = T.char_dims(Rs); e = T.energies(PP, w, 3)
        out[var] = {"G": len(Rs), "silent_even": [k for k in range(2, 21, 2) if e[k] < T.ZERO],
                    "beyond_box_level": [k for k in range(2, 21, 2) if e[k] < T.NONZERO and dims[k] > 0],
                    "min_even_energy": min(e[k] for k in range(2, 21, 2))}
    return out


def stella_frame():
    from nf import NF
    from harmony import analyse
    Fq = NF([0, 1], "0")
    T = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; Ts = [tuple(-c for c in p) for p in T]
    N = []
    for P_ in (T, Ts):
        for p, q in itertools.combinations(P_, 2):
            a = tuple(Fq.c(x) for x in p); b = tuple(Fq.c(x) for x in q)
            N.append((a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]))
    return analyse(Fq, N, "Vacuus of the stella-octangula yantra frame (12 edges, about the centre)")


if __name__ == "__main__":
    res = {}
    PK = load_polys(os.path.join(KDIR, "data", "polys-K.json"), "Q"); PD = load_polys(os.path.join(DDIR, "data", "polys-D.json"), "K")
    c = 2 * S5() - 4
    for key, nm, Pp, seed, vr, D in (("kulaichev", "spherical Kulaichev Sri Yantra", PK, ("0.7504385160222140244060846", "0.33935669020884128740", "0.92006014590959597529"), "u", 348),
                                     ("dicto", "spherical DICTO Yantra", PD, ("0.679318588706774657388650310391", "0.21447781650967411124", "0.96826860745869437414"), "c/u", 160)):
        ok, z = newton_krawczyk([Pp["G"], Pp["H1"], Pp["D"]], {0: seed[0], 1: seed[1], 2: seed[2]}, {})
        assert ok, f"Krawczyk failed for {key}"
        u, t, S = z; v = u if vr == "u" else c / u
        say(key, "Krawczyk ok, u =", u.str(25, radius=False))
        r = yantra_arrangement(nm, u, t, S, v, D)
        res[key] = r
        say(json.dumps(r))
    res["stella_frame_vacuus"] = stella_frame()
    say(json.dumps(res["stella_frame_vacuus"], default=str))
    json.dump(res, open(os.path.join(STUDY, "data/yantra.json"), "w"), indent=1, default=str)
    print("FINAL ok yantra", flush=True)
