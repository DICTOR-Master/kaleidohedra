"""Page data for any Hollow-straw pair (28 Nov 2026; DICTO: the next Scutoid-Frusta bridging solids, a C60 / Kuo #90 thumbnail).
With Claude (Anthropic). Same construction as hs_exact.py (floating-resin pairing of hs_general.py, core size RHO, SWAP=1 for the
reverse) and as the C116 page (frames of P(lam) at full precision; straws = the loft of each face, straw_loft.py; creases as edges;
colours = the Aequi page's colour of the die face each core face becomes).
Usage: CORE=GPc_1_1 DIE=90 RHO=0.7 [SWAP=1] OUT=... python hs_page_data.py"""
import os, sys, json, collections
import numpy as np
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
src = open(os.path.join(HERE, 'hs_general.py')).read()
g = {'__file__': os.path.join(HERE, 'hs_general.py'), '__name__': 'hsg'}
os.environ.setdefault('DICE', os.environ.get('DIE', '90'))
exec(src[:src.index('res = []')].replace("done_ = set()", "done_ = set()").split('OUTJ =')[0], g)
sys.path.insert(0, os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/scripts'))
from straw_loft import loft
import aequus_solid as AS
A = g['A']; core_planes, poly, float_resin = g['core_planes'], g['poly'], g['float_resin']
CORE = os.environ.get('CORE', 'GPc_1_1'); DIE = int(os.environ.get('DIE', '90')); RHO = float(os.environ.get('RHO', '0.7'))
SWAP = os.environ.get('SWAP') == '1'; os.environ.setdefault('NST', '150')
Ac = core_planes(CORE); Nc = Ac / np.linalg.norm(Ac, axis=1)[:, None]; Pc, Fc, Ec = poly(Ac); rc = np.linalg.norm(Pc, axis=1).max(); NF = len(Ac)
S = A.build(f'aequus-{DIE}')
Md = np.array([[float(x) for x in u] for u, c in S['planes']]) / np.array([float(c) for u, c in S['planes']])[:, None]
Nd = Md / np.linalg.norm(Md, axis=1)[:, None]; Pd, Fd, Ed = poly(Md); rin = (1 / np.linalg.norm(Md, axis=1)).min()
tot, R, sig = float_resin(Nc, Nd, np.random.default_rng(DIE))
if not SWAP:
    a0 = (Ac @ R.T) * (rc / (RHO * rin)); a1 = Md[sig]
else:
    rd = np.linalg.norm(Pd, axis=1).max(); rin_c = (1 / np.linalg.norm(Ac, axis=1)).min()
    a0 = ((Md @ R) * (rd / (RHO * rin_c)))[sig]; a1 = Ac
# colours: the Aequi page's colour of each die face (as app_data.py), carried to the plane it pairs with
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}
def mix(a, b, t): return '#' + ''.join('%02x' % round(int(a[1 + 2 * i:3 + 2 * i], 16) * (1 - t) + int(b[1 + 2 * i:3 + 2 * i], 16) * t) for i in range(3))
def colOf(key): base = COL[key.replace('2', '')]; return mix(base, '#ffffff', 0.45) if key.endswith('2') else base
Dd = json.load(open(os.path.join(ST, '2026-11-24-aequi-vacuus-scutoids/src/dice.json'))); e = Dd['dice'][DIE - 1]; ED = AS.C.exact_dirs(Dd['dirs']); lab = {}
for oi in e['o']:
    gr = Dd['groups'][e['g']][oi]
    for i in gr['dirs']: lab[A.key([AS.Q(c.a, c.b) for c in ED[i][0]])] = gr['col']
mcol = [lab[A.key(u)] for u, c in S['planes']]
col = [colOf(mcol[sig[k]]) for k in range(NF)]
names = {'D': 'dodecahedron planes', 'I': 'icosahedron planes', 'I2': 'icosahedron planes', 'RD': 'rhombic dodecahedron planes', 'RT2': 'rhombic triacontahedron planes',
         'RT': 'rhombic triacontahedron planes', 'C': 'cube planes', 'O': 'octahedron planes', 'T': 'tetrahedron planes', 'D2': 'dodecahedron planes'}
legend = {colOf(k): names.get(k, k) for k in set(mcol)}
def solid(lam):
    A_ = (1 - lam) * a0 + lam * a1
    P = HalfspaceIntersection(np.hstack([A_, -np.ones((NF, 1))]), np.zeros(3)).intersections
    sc = np.abs(P).max(); pts = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 * sc for q in pts): pts.append(p)
    P = np.array(pts); tight = np.abs(A_ @ P.T - 1) < 1e-8; faces = []
    for k in range(NF):
        idx = list(np.where(tight[k])[0]); X = P[idx]; c0 = X.mean(0); n = A_[k] / np.linalg.norm(A_[k]); e1 = X[0] - c0; e2 = np.cross(n, e1)
        order = np.argsort(np.arctan2((X - c0) @ e2, (X - c0) @ e1)); faces.append([idx[i] for i in order])
    return P, faces, None, A_
# swap times from the exact certificate (its json), else a fine uniform grid
tag = ('rev_' if SWAP else '') + f'{CORE}_{DIE}_rho{RHO}'
try: ev = sorted({round(x['lam'], 4) for x in json.load(open(os.path.join(HERE, f'../data/exact_{tag}.json')))['events']})
except Exception: ev = []
grid = sorted(set(np.round(np.concatenate([np.linspace(0, 1, 61)] + [np.linspace(t - 0.003, t + 0.003, 9) for t in ev]), 6)))
grid = [x for x in grid if 0 <= x <= 1]
F = [solid(l) for l in grid]
frames = [dict(lam=float(l), v=np.round(P, 6).tolist(), f=[[int(i) for i in fc] for fc in faces]) for l, (P, faces, _, _) in zip(grid, F)]
straws = []; vtot = 0
for k in range(NF):
    V, T = loft(F, k, 0.0)
    vtot += np.einsum('ij,ij->i', V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum() / 6
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]); fl = np.linalg.norm(fn, axis=1); good = fl > 1e-14; fn[good] /= fl[good][:, None]
    adj = collections.defaultdict(list)
    for i, t in enumerate(T):
        if good[i]:
            for a_, b_ in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): adj[(min(a_, b_), max(a_, b_))].append(i)
    E = [[int(x[0]), int(x[1])] for x, fs in adj.items() if len(fs) == 2 and fn[fs[0]] @ fn[fs[1]] < np.cos(np.radians(20))]
    straws.append(dict(k=k, v=np.round(V, 6).tolist(), t=T.tolist(), e=E))
def vf(P, Fs): return sum(np.dot(P[f[0]], np.cross(P[f[t]], P[f[t + 1]])) for f in Fs for t in range(1, len(f) - 1)) / 6
shell = vf(F[-1][0], F[-1][1]) - vf(F[0][0], F[0][1]); vol_ok = abs(vtot - shell) < 0.005 * shell
nested = all((((1 - grid[i + 1]) * a0 + grid[i + 1] * a1) @ F[i][0].T <= 1 + 1e-9).all() for i in range(len(grid) - 1))
names_ = json.load(open(os.path.join(os.path.expanduser('~'), 'k-mix/aequi/names.json'))) if os.path.exists(os.path.expanduser('~/k-mix/aequi/names.json')) else None
dname = names_[DIE - 1] if names_ else f'die {DIE}'; cname = {'GPc_1_1': 'C60', 'GPc_2_0': 'C80', 'GP_2_1': 'C140'}.get(CORE, CORE)
title = f'{dname} into {cname}' if SWAP else f'{cname} into {dname}'
out = dict(title=title, colour=col, legend=legend, swaps=[dict(lam=t) for t in ev], frames=frames, straws=straws,
           checks=dict(nested_frames=bool(nested), straws_volume_ok=bool(vol_ok)))
json.dump(out, open(os.environ['OUT'], 'w'), separators=(',', ':'))
print(title, 'frames', len(frames), 'straws', len(straws), 'volume', vtot, 'shell', shell, 'nested', nested, 'volume ok', vol_ok, flush=True)
print('FINAL ok' if nested and vol_ok else 'FINAL FAIL')
