"""Kulaichev's Sri Yantra (#103 Theorem 10): the leg slope u (half-width per depth) of the great triangles is a root of the
irreducible degree-348 polynomial f348 (paper data file kulaichev-minpoly-u.txt, read from stdin path argv[1]).

Method A (this script): Newton's method on f348 in mpmath at 160 digits from the paper's 40-digit isolating interval,
          then a strict sign change of f348 at u -/+ 1e-125 (so a root lies within 1e-125).
Method B (independent, earlier): the yantra audit's exact rational sign-change refinement to width 3e-1000
          (studies/2026-11-09-yantra-audit, stage1-K.json, 1000 digits; file argv[2]); and the 260-digit Newton solve of the
          geometric conditions (no polynomial) stored in studies/2026-11-08-sri-yantra/data/kulaichev-numeric-data.txt (60 digits).
Run: python kulaichev_slope.py minpoly.txt audit1000.txt"""
import sys, re
import mpmath as mp
mp.mp.dps = 160
txt = open(sys.argv[1]).read().replace('\n', '').replace(' ', '')
coef = {}
terms = re.findall(r'[+-]?[^+-]+', txt)
for t in terms:
    m = re.fullmatch(r'([+-]?)(\d*)\*?x(?:\^(\d+))?', t)
    if m:
        c = int(m.group(2) or 1) * (-1 if m.group(1) == '-' else 1); e = int(m.group(3) or 1)
    else:
        c = int(t); e = 0
    coef[e] = coef.get(e, 0) + c
deg = max(coef); assert deg == 348, deg
P = [coef.get(e, 0) for e in range(deg, -1, -1)]
f = lambda x: mp.polyval(P, x)
lo = mp.mpf('0.7504385160222140244060846570512345103408'); hi = mp.mpf('0.7504385160222140244060846570512345103409')
assert mp.sign(f(lo)) != mp.sign(f(hi)), 'no sign change on the paper interval'
u = mp.findroot(f, (lo + hi) / 2, tol=mp.mpf(10) ** -150)
eps = mp.mpf(10) ** -125
assert mp.sign(f(u - eps)) != mp.sign(f(u + eps))
s = mp.nstr(u, 130, strip_zeros=False)
audit = open(sys.argv[2]).read().strip()
geom60 = '0.750438516022214024406084657051234510340891003639790315415314'
print('u (method A, 120 digits):', s[:122])
print('agrees with audit 1000-digit value to 120 digits:', s[:122] == audit[:122])
print('agrees with geometric 260-digit Newton (60 stored digits):', s[:62] == geom60[:62])
digits = s[2:2 + 105]
print('digits for OEIS (offset 0):', ','.join(digits))
print('FINAL ok' if s[:122] == audit[:122] and s[:62] == geom60[:62] else 'FINAL FAIL')
