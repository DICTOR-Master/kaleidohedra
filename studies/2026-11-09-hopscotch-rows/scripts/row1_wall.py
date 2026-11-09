"""Row 1 (hyperboloid / projective row), part (c): Kulaichev's (d) (the bindu's incircle centred) as ONE wall on the beta-line.
Claim: T_beta sends the point p_beta = (0, -beta) to the centre. A Euclidean circle about the centre is a hyperbolic circle about the
centre (Klein model), so the image's incircle is centred exactly when the bindu's HYPERBOLIC incentre (Klein model of the yantra's own
circle) is p_beta. With unit lines l^ = l / sqrt(l^T J l), the incentre lies on the bisector m = l^_base - l^_leg (both oriented
positive inside), so the wall is the single equation m . (0, -beta, 1) = 0, LINEAR in beta:  beta* = m_w / m_y.
Closed form for a symmetric bindu (apex (0,a), base y = b, base half-width c, leg L = sqrt((a-b)^2 + c^2)):
   y_H = (c a sqrt(1-b^2) + b sqrt(L^2 - c^2 a^2)) / (c sqrt(1-b^2) + sqrt(L^2 - c^2 a^2)),   beta* = -y_H,
the Euclidean incentre y_E = (c a + L b)/(c + L) with c -> c sqrt(1-b^2), L -> sqrt(L^2 - c^2 a^2).
Checks: symbolic identity of the closed form with the bisector; K1 -> beta* equals viewpoint.py's root (V1); V1 and GF1 (bindu
already centred) -> beta* = 0; GF1's preimage (Cleo-Icos 2/phi^2 above, Antonius side 1/phi below) -> beta* = (lam^2-1)/(lam^2+1);
200 random symmetric triangles: the image under T_beta* has its Euclidean incentre at the centre, and the Euclidean-incentre height
has exactly one zero on (-1, 1)."""
import json, random, mpmath as mp, sympy as sp
mp.mp.dps = 50
J = mp.diag([1, 1, -1])
checks = {}

# --- symbolic: closed form = bisector solution
a, b, c, be = sp.symbols('a b c beta', real=True)
lb = sp.Matrix([0, 1, -b])                          # base y = b, positive above (inside, apex up)
ll = -sp.Matrix([a - b, c, -c * a])                 # leg through (0,a), (c,b), oriented positive toward the axis
Js = sp.diag(1, 1, -1)
nb, nl = sp.sqrt((lb.T * Js * lb)[0]), sp.sqrt((ll.T * Js * ll)[0])
m = lb / nb - ll / nl
beta_star = sp.solve((m.T * sp.Matrix([0, -be, 1]))[0], be)
L2 = (a - b)**2 + c**2
yH = (c * a * sp.sqrt(1 - b**2) + b * sp.sqrt(L2 - c**2 * a**2)) / (c * sp.sqrt(1 - b**2) + sp.sqrt(L2 - c**2 * a**2))
checks['wall is linear in beta (one root)'] = len(beta_star) == 1 and sp.degree(sp.numer(sp.together((m.T * sp.Matrix([0, -be, 1]))[0])), be) == 1
checks['closed form: beta* = -y_H'] = sp.simplify(beta_star[0] + yH) == 0
print('beta* =', sp.simplify(beta_star[0]))

# --- numeric on the yantras (40-digit data)
def load(f, key):
    K = json.load(open(f))[key]; g = lambda d: {int(k): mp.mpf(v['a']) for k, v in d.items()}
    bb, ww, aa = g(K['b']), g(K['w']), g(K['apex'])
    return {i: ((-2 * ww[i], 1 - 2 * bb[i]), (2 * ww[i], 1 - 2 * bb[i]), (0, 1 - 2 * aa[i])) for i in bb}
def T(p, be_): x, y = p; return (x * mp.sqrt(1 - be_**2) / (1 + be_ * y), (y + be_) / (1 + be_ * y))
def mapped(tr, be_): return {i: tuple(T(p, be_) for p in t) for i, t in tr.items()}
def line(p, q): return mp.matrix([p[1] - q[1], q[0] - p[0], p[0] * q[1] - p[1] * q[0]])
def meet(l1, l2):
    X = [l1[1] * l2[2] - l1[2] * l2[1], l1[2] * l2[0] - l1[0] * l2[2], l1[0] * l2[1] - l1[1] * l2[0]]; return (X[0] / X[2], X[1] / X[2])
def bindu(tr):     # t1's legs and t5's base, as in viewpoint.py (Kulaichev's (d))
    L1, R1, A1 = tr[1]; L5, R5, _ = tr[5]
    base, legL, legR = line(L5, R5), line(L1, A1), line(R1, A1)
    return meet(legL, base), meet(legR, base), A1, base, legL
def orient(l, inside):
    s = l[0] * inside[0] + l[1] * inside[1] + l[2]; return l if s > 0 else -l
def wall(tr):
    P1, P2, A1, base, leg = bindu(tr)
    cen = ((P1[0] + P2[0] + A1[0]) / 3, (P1[1] + P2[1] + A1[1]) / 3)
    lb_, ll_ = orient(base, cen), orient(leg, cen)
    q = lambda l: mp.sqrt(l[0]**2 + l[1]**2 - l[2]**2)
    mm = lb_ / q(lb_) - ll_ / q(ll_)
    return mm[2] / mm[1]                                          # m.(0,-beta,1) = 0
def wall_closed(tr):
    P1, P2, A1, _, _ = bindu(tr); aa, bb, cc = A1[1], P1[1], abs(P1[0])
    L2_ = (aa - bb)**2 + cc**2; s = mp.sqrt(L2_ - cc**2 * aa**2); t = cc * mp.sqrt(1 - bb**2)
    return -(t * aa + s * bb) / (t + s)
def euclid_incentre_y(tr):
    P1, P2, P3, _, _ = bindu(tr)
    la, lb2, lc = [mp.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2) for p, q in ((P2, P3), (P3, P1), (P1, P2))]
    return (la * P1[1] + lb2 * P2[1] + lc * P3[1]) / (la + lb2 + lc)

tol = mp.mpf(10)**-35                                             # the data carry 40 digits
K1 = load('../data/kites.json', 'K1')
bK = wall(K1); bV = mp.mpf(json.load(open('../data/viewpoint.json'))['V1']['beta'])
print('K1: beta* (one linear wall) =', mp.nstr(bK, 30), '| viewpoint.py root =', mp.nstr(bV, 30), '| closed form', mp.nstr(wall_closed(K1), 30))
checks['K1: beta* = viewpoint.py root (V1)'] = abs(bK - bV) < mp.mpf(10)**-28
checks['K1: closed form = bisector'] = abs(wall_closed(K1) - bK) < tol
checks['K1: image at beta* has Euclidean incentre at the centre'] = abs(euclid_incentre_y(mapped(K1, bK))) < tol
V1 = load('../data/viewpoint.json', 'V1')
checks['V1 (centred): beta* = 0'] = abs(wall(V1)) < tol
G = load('../data/golden_family.json', 'GF1')
checks['GF1 DICTO Yantra (centred): beta* = 0'] = abs(wall(G)) < tol
print('V1 beta* =', mp.nstr(wall(V1), 5), '  GF1 beta* =', mp.nstr(wall(G), 5))
phi = (1 + mp.sqrt(5)) / 2
uG = mp.mpf(json.load(open('../data/golden_family.json'))['GF1']['u'])
lamG = uG / (2 / phi**2); bG = (lamG**2 - 1) / (lamG**2 + 1)
pre = mapped(G, -bG)                                              # undo the viewpoint
slope = lambda Lp, Ap: abs(Lp[0] / (Lp[1] - Ap[1]))
# upper great slope: legs through O (apex at top); lower: through T. Identify by the apex position
up = [i for i in pre if pre[i][2][1] > pre[i][0][1]]; lo = [i for i in pre if pre[i][2][1] < pre[i][0][1]]
sl_up = max((slope(pre[i][0], pre[i][2]), i) for i in up); sl_lo = max((slope(pre[i][0], pre[i][2]), i) for i in lo)
print('GF1 preimage: beta_GF =', mp.nstr(bG, 20), ' wall of preimage =', mp.nstr(wall(pre), 20))
print('  slopes of the great triangles of the preimage:', [mp.nstr(s, 15) for s in (slope(pre[i][0], pre[i][2]) for i in sorted(pre))])
checks['GF1 preimage: wall = beta_GF'] = abs(wall(pre) - bG) < mp.mpf(10)**-30
gs = [slope(pre[i][0], pre[i][2]) for i in sorted(pre)]
checks['GF1 preimage has slopes 2/phi^2 and 1/phi (Cleo-Icos, Antonius side)'] = min(abs(s - 2 / phi**2) for s in gs) < mp.mpf(10)**-30 and min(abs(s - 1 / phi) for s in gs) < mp.mpf(10)**-30

# random symmetric yantra-like bindus: the wall centres the image; the Euclidean height has one zero on (-1,1)
random.seed(11); ok_r, ok_u = True, True
for _ in range(200):
    aa = mp.mpf(random.uniform(-0.9, 0.9)); bb = aa - mp.mpf(random.uniform(0.02, 0.9))
    if bb < -0.98: continue
    cmax = mp.sqrt(1 - bb**2) * 0.99; cc = mp.mpf(random.uniform(0.01, 1)) * cmax
    tr = {1: ((-cc, bb), (cc, bb), (0, aa)), 5: ((-cc, bb), (cc, bb), (0, aa))}
    bs = wall(tr); ok_r &= abs(euclid_incentre_y(mapped(tr, bs))) < mp.mpf(10)**-40 and -1 < bs < 1
    grid = [mp.mpf(k) / 200 for k in range(-199, 200)]
    vals = [euclid_incentre_y(mapped(tr, g_)) for g_ in grid]
    ok_u &= sum(1 for p_, q_ in zip(vals, vals[1:]) if p_ * q_ < 0) == 1
checks['200 random bindus: T_beta* centres the Euclidean incircle'] = ok_r
checks['200 random bindus: exactly one centring beta on (-1,1)'] = ok_u

for k, ok in checks.items(): print(('ok   ' if ok else 'FAIL ') + k)
bad = [k for k, ok in checks.items() if not ok]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
