#!/usr/bin/env python3
"""Heptagonal Queen, part 1: construction and hidden-symmetry test (18 Nov 2026).
Golden controls in sum-zero R^5 (600-cell = A u -A u C3 u B u -B), then the heptagonal S7 orbits in sum-zero R^7.
Symmetry group of a finite set = all linear isometries mapping it to itself, found exactly by base backtracking
(images of a base of points, exact inner-product constraints, each leaf verified on every point).
Usage: s1_symmetry.py out.json"""
import sys, json, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hlib import *
from math import factorial
from collections import defaultdict
import sympy as sp
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}

# ---------- golden controls (R^5) ----------
K = GOLD; z, one, ph, ph2 = K.el(0), K.el(1), K.el(0, 1), K.el(1, 1)
A = centre(canon_orbit([z, ph, ph2, ph2, ph2], K)); B = centre(canon_orbit([z, one, one, ph2, ph2], K))
R = centre(canon_orbit([ph, z, z, z, -ph], K))
P = uniq_pts(np.concatenate([A, -A, B, -B, R]))
C(len(P) == 120 and len({K.ip(p, p).tobytes() for p in P}) == 1, f'control: A,-A,C3,B,-B = 120 points on one sphere ({len(P)})')
o, perms = isometry_group(K, P)
C(o == 14400 and orbits_of(perms, 120) == [120], f'control: the 600-cell set has |G| = {o} (H4 = 14400) and is vertex-transitive {orbits_of(perms, 120)}')
d2 = K.ip(P[:, None] - P[None], P[:, None] - P[None]); df = K.f(d2); mn = df[df > 1e-9].min()
ne = int(np.sum(np.isclose(df, mn)) // 2); C(ne == 720, f'control: 720 shortest edges ({ne})')
oA, _ = isometry_group(K, A); C(oA == 120, f'control: ordinary orbit A alone has |G| = {oA} = |S5| (no hidden symmetry)')
O2 = centre(canon_orbit([z, one, one, K.el(3), K.el(3)], K)); O2 = np.concatenate([O2, -O2])
oO, _ = isometry_group(K, O2); C(oO == 240, f'control: ordinary orbit perms(0,1,1,3,3) and its negative: |G| = {oO} = |S5 x {{+-1}}|')
out['gold'] = dict(n=120, G=14400, edges=720, A_alone=oA, ordinary=oO)

# ---------- heptagonal field ----------
K = HEPT; z = K.el(0); one = K.el(1); rho = K.el(0, 1); sig = K.el(-1, 0, 1)
rho2, sig2, rs = K.mul(rho, rho), K.mul(sig, sig), K.mul(rho, sig)
C(np.array_equal(rho2, one + sig) and np.array_equal(rs, rho + sig) and np.array_equal(sig2, one + rho + sig),
  'heptagon identities rho^2 = 1 + sigma, rho*sigma = rho + sigma, sigma^2 = 1 + rho + sigma (Steinbach 1997)')
x = sp.symbols('x'); cc = sp.cos(2*sp.pi/7)
C(sp.minimal_polynomial(2*sp.cos(sp.pi/7), x) == x**3 - x**2 - 2*x + 1, 'rho = 2cos(pi/7) has minimal polynomial x^3 - x^2 - 2x + 1')
C(sp.minimal_polynomial((2*sp.cos(sp.pi/7))**2 - 2 - 2*cc, x) == x, 'rho^2 = 2 + 2c, c = cos(2pi/7): Q(rho) = Q(c), the field of the fair die')
L = {'0': z, '1': one, 'r': rho, 's': sig}
def vec(g):
    v = [z]
    for ch in g: v.append(v[-1] + L[ch])
    return np.array(v)
def nrm(g): xx = centre(vec(g)[None])[0]; return K.ip(xx, xx)
tt = defaultdict(list)
for slots in itertools.combinations(range(6), 3):
    for pm in itertools.permutations('1rs'):
        g = ['0']*6
        for s_, ch in zip(slots, pm): g[s_] = ch
        tt[nrm(g).tobytes()].append(''.join(g))
szs = sorted(len(v) for v in tt.values())
C(sum(szs) == 120 and szs.count(4) == 1 and all(s in (2, 4) for s in szs),
  f'truncation-type orbits: 120 in {len(tt)} sphere classes; exactly one class has 4 orbits, the rest are +- pairs')
four = [v for v in tt.values() if len(v) == 4][0]
C(sorted(four) == sorted(['rs1000', '10s0r0', '0001sr', '0r0s01']), f'the 4-orbit class = A_h, B_h and their negatives {four}')
out['truncation_type'] = dict(orbits=120, classes=len(tt), four_class=four)
cls = defaultdict(list)
for g in itertools.product('01rs', repeat=6):
    if g != ('0',)*6: cls[nrm(g).tobytes()].append(''.join(g))
mates = cls[nrm('rs1000').tobytes()]
C(sorted(mates) == sorted(four), f'among all 4095 orbits with gaps in {{0,1,rho,sigma}} ({len(cls)} spheres), the sphere of A_h holds only A_h, B_h, -A_h, -B_h ({len(mates)})')
out['family4095'] = dict(orbits=4095, sphere_classes=len(cls), mates_of_Ah=mates)
Ah = centre(canon_orbit(list(vec('rs1000')), K)); Bh = centre(canon_orbit(list(vec('10s0r0')), K))
C(len(Ah) == 210 and len(Bh) == 630, 'A_h = perms(0, rho, rho*sigma, sigma^2 x4): 210 points; B_h = perms(0, 1, 1, rho^2, rho^2, sigma^2, sigma^2): 630 points')
C(np.array_equal(vec('rs1000')[-1], sig2) and np.array_equal(vec('rs1000')[2], rs) and np.array_equal(vec('10s0r0')[3], rho2), 'entries as stated')
nu = K.ip(Ah[0], Ah[0]); C(np.array_equal(nu, K.ip(Bh[0], Bh[0])) and np.array_equal(nu, 98*K.el(-1, 2, 3)),
  'A_h and B_h on one sphere: |x - mean|^2 = 2(-1 + 2rho + 3rho^2)')
t, y = sp.symbols('t y')
res_ = sp.resultant(y**2 - (-1 + 2*t + 3*t**2), t**3 - t**2 - 2*t + 1, t)
fl = sp.factor_list(res_)
C(len(fl[1]) == 1 and fl[1][0][1] == 1 and sp.degree(fl[1][0][0], y) == 6,
  f'no k in Q(rho) with k^2 = -1 + 2rho + 3rho^2 (norm polynomial {sp.expand(res_)} is irreducible of degree 6): no scaled root orbit (C3 analogue) lies on the sphere')
out['C3'] = 'none: -1+2rho+3rho^2 is not a square in Q(rho)'
res = {}
for name, X in [('A_h', Ah), ('B_h', Bh), ('A_h u B_h', np.concatenate([Ah, Bh])), ('A_h u -A_h', np.concatenate([Ah, -Ah])),
                ('B_h u -B_h', np.concatenate([Bh, -Bh])), ('Q_h = A_h u -A_h u B_h u -B_h', np.concatenate([Ah, -Ah, Bh, -Bh]))]:
    t1 = time.time(); o, perms = isometry_group(K, X); orb = orbits_of(perms, len(X)); res[name] = dict(n=len(X), G=o, orbits=orb)
    exp = 10080 if '-' in name else 5040
    C(o == exp, f'{name}: {len(X)} points, |G| = {o} (= |S7|{" x 2" if exp > 5040 else ""}), vertex orbits {orb} ({time.time() - t1:.1f} s)')
out['groups'] = res
Q = np.concatenate([Ah, -Ah, Bh, -Bh]); prof = {}
for i, nm in ((0, 'A'), (420, 'B')):
    ips = K.ip(Q, np.broadcast_to(Q[i], Q.shape)); prof[nm] = len({v.tobytes() for v in ips})
d2 = K.f(K.ip(Q[:, None] - Q[None], Q[:, None] - Q[None])); mn = d2[d2 > 1e-9].min(); deg = np.isclose(d2, mn).sum(1)
out['Q_h'] = dict(n=1680, distinct_ip_from_A=prof['A'], distinct_ip_from_B=prof['B'], min_dist2=mn/49, edges_min=int(deg.sum()//2), degrees=sorted(set(deg.tolist())))
C(True, f"Q_h: distinct inner products from an A_h corner {prof['A']}, from a B_h corner {prof['B']}; shortest distance^2 {mn/49:.6f} (float), {int(deg.sum()//2)} shortest pairs, degrees {sorted(set(deg.tolist()))}")
json.dump(out, open(OUT, 'w'), indent=1, default=str)
C.final(); print(f'time {time.time() - t0:.1f} s')
