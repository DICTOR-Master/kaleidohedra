"""Branch B2, stage 1: vertex figure of K at an end corner P0 of degree 4 (faces: end triangle, F0 on the leg P0Pa, E0 on the
hexagon edge P0Q0, hexagon).  Given f = dihedral(end, F0) and e = dihedral(hexagon, E0), the fourth corner rho (F0|E0 along the
edge d = F0 cap E0) is determined.  Screen: rho in the ring-closing alphabet?  (PSLQ in pi, alpha, beta, gamma; margins printed.)
f in {2pi/3 (ring 3 x 120), 11pi/12 = 165, 5pi/12 = 75 (branch A's chiral pair)}; e over the alphabet in (0, 2pi)."""
import json, sys, itertools
from fractions import Fraction as Fr
import mpmath as mp
mp.mp.dps = 60
PI = mp.pi; phi = (1 + mp.sqrt(5)) / 2; AL = mp.atan(phi); BE = mp.acos(1 / mp.sqrt(6)); GA = mp.acos(mp.sqrt(mp.mpf(2) / 3))
tq = BE - PI / 4; EPS = mp.mpf(10) ** -40
V = lambda *a: mp.matrix([mp.mpf(x) for x in a])
dot = lambda u, v: u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
cross = lambda u, v: mp.matrix([u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]])
unit = lambda u: u / mp.sqrt(dot(u, u))
deg = lambda x: float(x * 180 / PI)
h = mp.sqrt((3 * phi ** 2 - 1) / 4)
P0, P1, Pa, Q0 = V(-0.5, 0, 0), V(0.5, 0, 0), V(0, h, 0), V(-1, phi / 2, 1 / (2 * phi))
ux, uL, uQ = unit(P1 - P0), unit(Pa - P0), unit(Q0 - P0)
ALPH = []
for b in (1, -1):
    for k in range(-8, 12):
        a = mp.mpf(k) / 4 * PI + b * BE
        if 0 < a < 2 * PI: ALPH.append((f"{Fr(k,4)}pi{'+' if b>0 else '-'}beta", a))
seen = set()
for q in range(1, 13):
    for k in range(1, 2 * q):
        f = Fr(k, q)
        if f in seen or f == 1: continue
        seen.add(f); ALPH.append((f"{f}pi", PI * f.numerator / f.denominator))
def nearest(a): return min(ALPH, key=lambda t: abs(t[1] - a))
def corner(v, a, b):
    """interior angle at v of a spherical polygon traversed ... a -> v -> b, interior on the left (axis v outward)"""
    ta = unit(a - dot(a, v) * v); tb = unit(b - dot(b, v) * v)
    return mp.atan2(dot(v, cross(tb, ta)), dot(tb, ta)) % (2 * PI)
def rot(u, axis, t):
    axis = unit(axis); return u * mp.cos(t) + cross(axis, u) * mp.sin(t) + axis * dot(axis, u) * (1 - mp.cos(t))
# orientation: polygon order ux -> uL -> d -> uQ -> ux; check corner at ux = t'
s_or = 1 if abs(corner(ux, uQ, uL) - tq) < EPS else -1
if s_or < 0: assert abs(corner(ux, uL, uQ) - tq) < EPS
def poly_corners(seq):
    n = len(seq)
    if s_or > 0: return [corner(seq[i], seq[i - 1], seq[(i + 1) % n]) for i in range(n)]
    return [corner(seq[i], seq[(i + 1) % n], seq[i - 1]) for i in range(n)]
# F0's in-face direction at uL (perpendicular to leg, inside K): rotate the end face's inward direction (toward ux side) about uL by f
w_end = unit(ux - dot(ux, uL) * uL)                 # inside the end face, perpendicular to the leg
w_hex = unit(ux - dot(ux, uQ) * uQ)                 # inside the hexagon, perpendicular to P0Q0
res = []
def solve(f, e):
    best = None
    for sf in (1, -1):
        for se in (1, -1):
            wF = rot(w_end, uL, sf * f); wE = rot(w_hex, uQ, se * e)
            nF = unit(cross(uL, wF)); nE = unit(cross(uQ, wE))
            d0 = cross(nF, nE)
            if mp.sqrt(dot(d0, d0)) < EPS: continue
            for d in (unit(d0), -unit(d0)):
                c = poly_corners([ux, uL, d, uQ])
                if abs(c[0] - tq) < EPS and abs(c[1] - f) < EPS and abs(c[3] - e) < EPS:
                    # d must be reached along F0 from uL on the wF side and along E0 from uQ on the wE side (arc < pi)
                    if dot(d - dot(d, uL) * uL, wF) > EPS and dot(d - dot(d, uQ) * uQ, wE) > EPS:
                        area = sum(c) - 2 * PI
                        if area > EPS and (best is None): best = (c[2], area, d)
    return best
out = []
for fname, f in (("2pi/3", 2 * PI / 3), ("11pi/12", 11 * PI / 12), ("5pi/12", 5 * PI / 12)):
    print(f"== f = {fname} ({deg(f):.4f} deg)", flush=True)
    for en, e in ALPH:
        r = solve(f, e)
        if r is None: continue
        rho, area, d = r
        nm, nv = nearest(rho)
        rel = mp.pslq([rho, PI, AL, BE, GA], maxcoeff=500, maxsteps=20000, tol=mp.mpf(10) ** -50)
        ok = abs(nv - rho) < EPS
        rec = dict(f=fname, e=en, e_deg=deg(e), rho_deg=deg(rho), area=float(area), in_alphabet=ok, nearest=nm, gap_deg=deg(abs(nv - rho)),
                   pslq=None if rel is None else [int(x) for x in rel], d=[float(x) for x in d])
        out.append(rec)
        print(f"  e = {en:14s} {deg(e):9.4f}  rho = {deg(rho):10.5f}  area {float(area):.4f}  {'IN ' + nm if ok else 'not in (nearest ' + nm + f', gap {deg(abs(nv-rho)):.4f})'}"
              f"  pslq {rec['pslq']}", flush=True)
hits = [r for r in out if r['in_alphabet']]
print(f"== {len(out)} valid (f, e), {len(hits)} with rho in the alphabet")
for r in hits: print("  HIT", r['f'], r['e'], round(r['rho_deg'], 6))
json.dump(dict(results=out, hits=hits), open(sys.argv[1], 'w'), indent=1)
sane = len(out) > 0 and all(r['area'] > 0 for r in out) and all(r['pslq'] is not None for r in hits) and \
    all(r['e_deg'] > 159.0948 for r in hits)
print("FINAL ok" if sane else "FINAL FAIL (sanity: empty scan, non-positive area, or an alphabet hit without a PSLQ relation)")
