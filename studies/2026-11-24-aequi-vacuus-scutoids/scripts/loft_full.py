"""Full-precision straws for the Hollow-straw page and its 3D printing (28 Nov 2026; DICTO: the inner as a core, all parts
printable, fit presets; choice 1: each face shrunk in its own plane at every step). With Claude (Anthropic).
Uses app_data.py's frames at full double precision (not rounded); each straw = the loft of face k's polygon over the frames,
consecutive polygons joined by zipping their edges in angle order. Checks: every straw closed, the straws' volumes add up to
die - core, no straw crosses itself; then the same with every polygon shrunk inward in its plane by h (gap 0.2 and 0.5 mm at 60 mm)."""
import os, sys, json, collections
import numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'app_data.py')).read()
g = {'__file__': os.path.join(HERE, 'app_data.py'), '__name__': 'ad'}
exec(src[:src.index('# straws on a coarser grid')], g)
F, grid = g['F'], g['grid']
from straw_loft import unit, pnormal, clean, shrink, loft as _loft
def loft(k, h): return _loft(F, k, h)
def vol(P, T): return np.einsum('ij,ij->i', P[T[:, 0]], np.cross(P[T[:, 1]], P[T[:, 2]])).sum() / 6
def open_edges(P, T):
    key = {}; I = [[key.setdefault(tuple(np.round(P[i], 9)), len(key)) for i in t] for t in T]; E = collections.Counter()
    for a, b, c in I:
        if len({a, b, c}) < 3: continue
        for x, y in ((a, b), (b, c), (c, a)): E[(min(x, y), max(x, y))] += 1
    return sum(1 for v in E.values() if v != 2)
def self_cross(P, T, tol=1e-9):
    TT = P[T]; a = np.linalg.norm(np.cross(TT[:, 1] - TT[:, 0], TT[:, 2] - TT[:, 0]), axis=1); keep = a > 1e-14; TT = TT[keep]; I = T[keep]
    key = {}; I = np.array([[key.setdefault(tuple(np.round(P[i], 9)), len(key)) for i in t] for t in I])
    cen = TT.mean(1); rad = np.linalg.norm(TT - cen[:, None], axis=2).max(1); tree = cKDTree(cen); R = 2 * rad.max(); n = 0
    for i, t in enumerate(TT):
        near = [j for j in tree.query_ball_point(cen[i], R) if j != i and not set(I[j]) & set(I[i])]
        if not near: continue
        S = TT[near]; a_, b_, c_ = S[:, 0], S[:, 1], S[:, 2]
        for x, y in ((0, 1), (1, 2), (2, 0)):
            p0, p1 = t[x], t[y]; d = p1 - p0; e1, e2 = b_ - a_, c_ - a_; h = np.cross(d, e2); det = np.einsum('ij,ij->i', e1, h)
            ok = np.abs(det) > 1e-18; f = 1 / np.where(ok, det, 1); s = p0 - a_
            u = f * np.einsum('ij,ij->i', s, h); q = np.cross(s, e1); v = f * (q @ d); tt = f * np.einsum('ij,ij->i', e2, q)
            if (ok & (u > tol) & (v > tol) & (u + v < 1 - tol) & (tt > tol) & (tt < 1 - tol)).any(): return True
    return False
Pd, Fd = F[-1][0], F[-1][1]; Pc, Fc = F[0][0], F[0][1]
def vfaces(P, Fs): return sum(np.dot(P[f[0]], np.cross(P[f[t]], P[f[t + 1]])) for f in Fs for t in range(1, len(f) - 1)) / 6
die, core = vfaces(Pd, Fd), vfaces(Pc, Fc); R = np.linalg.norm(Pd, axis=1).max(); scale = 60 / (2 * R)
print('frames', len(F), 'die', die, 'core', core, 'die - core', die - core, flush=True)
ok = True
for gap in (0.0, 0.2, 0.5):
    h = gap / 2 / scale; tot = 0; op = 0; cr = 0
    for k in range(60):
        P, T = loft(k, h); tot += vol(P, T); op += open_edges(P, T) > 0; cr += self_cross(P, T)
    print(f'gap {gap} mm: straws volume {tot:.6f} (die - core {die - core:.6f}), straws with open edges {op}, straws crossing themselves {cr}', flush=True)
    ok &= op == 0 and cr == 0 and (gap > 0 or abs(tot - (die - core)) < 1e-6 * (die - core) * 10)
print('FINAL ok' if ok else 'FINAL FAIL')
