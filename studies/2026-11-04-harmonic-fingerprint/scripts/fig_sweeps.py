#!/usr/bin/env python3
"""Figure for #94: Q4, Q6, Q8 along the cube–octahedron sweep and the CO–RD sweep, stations marked. dicto-big-brother."""
import itertools, math, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.special import sph_harm_y
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'figures'); os.makedirs(OUT, exist_ok=True)
phi = (1 + 5**.5)/2
def Q(P, l):
    u = P/np.linalg.norm(P, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l+1)]); return math.sqrt(4*math.pi/(2*l+1)*np.sum(np.abs(q)**2))
def perms(v):
    return np.array(sorted({tuple(a*b for a, b in zip(p, s)) for p in itertools.permutations(v) for s in itertools.product((1, -1), repeat=3)}))
def co(mu): return perms((1, mu-1, 0)) if mu <= 2 else perms((1, 1, mu-2))
hs = [[*e, -1.0] for i in range(3) for s in (1, -1) for e in [[s if k == i else 0 for k in range(3)]]] + [[*s, -2.0] for s in itertools.product((1, -1), repeat=3)]
rdh = [[a if k == i else (b if k == j else 0) for k in range(3)] for i, j in itertools.combinations(range(3), 2) for a, b in itertools.product((1, -1), repeat=2)]
def cord(mu):
    return np.unique(np.round(HalfspaceIntersection(np.array(hs + [[*e, -mu] for e in rdh], float), np.zeros(3)).intersections, 9), axis=0)
fig, ax = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={'width_ratios': [2, 1]})
cols = {4: '#b8862e', 6: '#2e7d7a', 8: '#7a4fa0'}
g1 = np.linspace(1.002, 2.998, 500); g2 = np.linspace(1.002, 1.998, 250)
for l in (4, 6, 8):
    ax[0].plot(g1, [Q(co(m), l) for m in g1], color=cols[l], lw=1.8, label=f'Q{l}')
    ax[1].plot(g2, [Q(cord(m), l) for m in g2], color=cols[l], lw=1.8, label=f'Q{l}')
st = {'Unborn Axes\n3 − φ': 3-phi, 'Kelvin\n3/2': 1.5, 'Icosaxes\nφ': phi, 'cubocta-\nhedron 2': 2.0,
      'Greater\nGolden\nCut Cube': 4+1.5*2**.5-5**.5-.5*10**.5, 'Lesser\nGolden\nCut Cube': 4-1.5*2**.5+5**.5-.5*10**.5}
for k, (n, m) in enumerate(st.items()):
    ax[0].axvline(m, color='#bbb', lw=.8, zorder=0); ax[0].text(m + 0.01, 0.84 - 0.13*(k % 2), n.replace(chr(10), ' '), ha='left', va='top', fontsize=7, color='#444', rotation=0)
ax[0].plot([phi], [0], 'o', color='#b8862e', ms=7, zorder=5)
m0 = 1 + math.sqrt((6*math.sqrt(30)-31)/17); ax[1].plot([m0], [0], 'o', color='#b8862e', ms=7)
ax[1].text(m0, 0.04, 'Q4 = 0 at\n1 + √((6√30 − 31)/17)', fontsize=7.5, ha='left')
ax[0].set_title('Cube–octahedron sweep C ∩ μC*: octahedron (μ = 1) to cube (μ = 3)', fontsize=10)
ax[1].set_title('CO ∩ μRD: RD (μ = 1) to cuboctahedron (μ = 2)', fontsize=10)
for a in ax: a.set_xlabel('μ'); a.set_ylim(-0.02, 0.86); a.legend(fontsize=8, loc='upper left' if a is ax[1] else 'lower left', frameon=False)
ax[0].set_ylabel('harmonic strength Q_l of the corner directions')
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#888')
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig1-sweeps.png'), dpi=180)
# Q8 zeros on the first sweep
q8 = np.array([Q(co(m), 8) for m in g1]); print('Q8 minima', [(round(g1[i], 3), round(q8[i], 4)) for i in range(1, len(g1)-1) if q8[i] < q8[i-1] and q8[i] <= q8[i+1]])
