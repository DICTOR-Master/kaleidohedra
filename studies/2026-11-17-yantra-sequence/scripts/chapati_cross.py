"""Chapati and Chapati's own star-point enumerator (MIT licence, their src/ from Zenodo 10.5281/zenodo.23188650,
imported unchanged and not copied here) on the nine-triangle samples of family.py, beside the parity rule
and the outline-from-the-arrangement version of their rule (yarr.py).  Their rule needs Huet's transcribed
outlines and so exists only for nine triangles.
usage: python3 -I chapati_cross.py <chapati src dir> <study dir> <family json>"""
import sys, os, json, math
from fractions import Fraction as Fr
src, ST, FJ = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(ST, 'scripts'))
sys.argv = [sys.argv[0], ST, '1']          # family.py reads argv at import
import family as F
from yarr import QF
sys.path.insert(0, src)
import gate1_complete as G1
import huet_build as H


def fl(z):
    if isinstance(z, QF):
        return float(z.a) + float(z.b) * math.sqrt(float(QF.D))
    return float(z)


def huet_params(y):
    b = {i: fl(y['b'][i]) for i in range(1, 10)}; w = {i: fl(y['w'][i]) for i in range(1, 10)}
    a = {i: fl(y['a'][i]) for i in range(1, 10)}
    YQ = 1 - b[3]; YJ = 1 - b[7]; YP = 1 - b[6]
    XF = w[1] * (b[3] - a[1]) / (b[1] - a[1])
    XA = w[3] * (1 - b[8]) / (1 - b[3])
    return (YQ, XF, YP, XA, YJ), b


def frac(s):
    return Fr(s)


d = json.load(open(FJ))
rows, bad = [], []
for r in d['raw']['9']:
    p = r['params']
    par = (frac(p[0]), frac(p[1]), frac(p[2]), frac(p[3]), int(p[4]))
    y = F.build(9, par)
    hp, b = huet_params(y)
    P, L, D = H.build(*hp)
    mapchk = abs(D['YL'] - (1 - b[9]))
    try:
        res, _, _, _ = G1.enumerate_chambers(*hp, verbose=False)
    except Exception as ex:
        rows.append(dict(params=p, odd=r['odd'], error=repr(ex)[:200])); continue
    star_c = sum(x[2] for x in res)
    tips = [x[1] for x in res]
    rows.append(dict(params=p, odd=r['odd'], odd_rings=[r['rings'].get(str(c), r['rings'].get(c, 0)) for c in (1, 3, 5, 7, 9)],
                     star_outline=r['star'], star_chapati=star_c, chapati_by=[x[2] for x in res], chapati_tips=tips,
                     map_check=mapchk))
    if mapchk > 1e-9:
        bad.append(('mapping', p, mapchk))
# calibration of their code here: the DICTO Yantra and Kulaichev's yantra must give 43 star points each
import calibrate_loaders as CL
calib = {}
for nm, T in (('DICTO Yantra', CL.gf1(ST)), ('Kulaichev', CL.kulaichev(ST))):
    y = {'b': {i: T[i - 1][0] for i in range(1, 10)}, 'w': {i: T[i - 1][1] for i in range(1, 10)},
         'a': {i: T[i - 1][2] for i in range(1, 10)}}
    hp, _ = huet_params(y)
    res, _, _, _ = G1.enumerate_chambers(*hp, verbose=False)
    calib[nm] = sum(x[2] for x in res)
    print(f"calibration, Chapati's code: {nm} {calib[nm]} star points {[x[2] for x in res]}")
if calib != {'DICTO Yantra': 43, 'Kulaichev': 43}:
    bad.append(('calibration', calib))
errs = [row for row in rows if 'error' in row]
print(f"samples where their code raised: {len(errs)}")
rows = [row for row in rows if 'error' not in row]
dist = {}
for row in rows:
    k = (row['odd'], tuple(row['odd_rings']), row['star_outline'], row['star_chapati'], tuple(row['chapati_by']))
    dist[k] = dist.get(k, 0) + 1
for k, c in sorted(dist.items(), key=lambda kv: -kv[1]):
    print(f"{c:5d} x  parity {k[0]} {k[1]}  star (outline) {k[2]}  star (Chapati's code) {k[3]} {k[4]}")
json.dump({'rows': rows, 'distribution': [dict(parity=k[0], rings=k[1], star_outline=k[2], star_chapati=k[3],
                                                chapati_by=k[4], samples=c) for k, c in dist.items()]},
          open(os.path.join(ST, 'data', 'chapati-cross-n9.json'), 'w'), indent=0)
ok = not bad and len(rows) + len(errs) == len(d['raw']['9']) and len(rows) > 0
print("FINAL ok" if ok else f"FINAL FAIL {bad[:5]}")
