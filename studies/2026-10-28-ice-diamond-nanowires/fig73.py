# #73 figure: (a) III-V band offsets (dEc) and crystal-field splitting against h, each scaled by its 2H value (Belabbes et al.);
# (b) group-IV and SiC polytype energies from the ANNNI parameters of Ziembicki et al., scaled by the 2H value. Law: the diagonal.
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np, os
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=200)
H = [0, 1/3, 1/2, 1]
EC = {'GaAs': [0, 56, 77, 149], 'GaSb': [0, 50, 70, 146], 'InP': [0, 50, 77, 183], 'InAs': [0, 34, 58, 126], 'InSb': [0, 39, 59, 113]}
CF = {'GaAs': [0, .052, .071, .129], 'GaSb': [0, .057, .076, .148], 'InP': [0, .029, .039, .062], 'InAs': [0, .034, .055, .095],
      'InSb': [0, .036, .061, .113], 'GaP': [0, .021, .027, .045]}
a.plot([0, 1], [0, 1], color='#b8962e', lw=1.6, label='law')
for i, (k, v) in enumerate(EC.items()):
    a.plot(H, np.array(v)/v[-1], 'o', color='#3a6ea5', ms=4.5, mec='white', mew=0.6, label='conduction-band offset' if i == 0 else None)
for i, (k, v) in enumerate(CF.items()):
    a.plot(np.array(H)+0.012, np.array(v)/v[-1], 's', color='#7a7a7a', ms=4, mec='white', mew=0.6, label='crystal-field splitting' if i == 0 else None)
for h, n in zip(H, ['3C', '6H', '4H', '2H']): a.annotate(n, (h, 1.0 if h < 1 else 0.9), ha='center', fontsize=7, color='#555')
a.set_xlabel('hexagonality h'); a.set_ylabel('scaled by the 2H value'); a.set_ylim(-0.05, 1.08)
a.set_title('(a) Nanowire semiconductors: six III-V', fontsize=9, loc='left'); a.legend(fontsize=6.8, frameon=False, loc='lower right')
def spins(seq):
    P = {'A': 0, 'B': 1, 'C': 2}; n = len(seq)
    return [1 if (P[seq[(i+1) % n]] - P[seq[i]]) % 3 == 1 else -1 for i in range(n)]
def E(seq, J):
    s = spins(seq); n = len(s)
    return -sum(J[m-1]*s[i]*s[(i+m) % n] for i in range(n) for m in (1, 2, 3))/n
POLY = {'3C': 'ABC', '6H': 'ABCACB', '15R': 'ABCACBCABACABCB', '4H': 'ABAC', '9R': 'ABABCBCAC', '2H': 'AB'}
hh = {k: sum(v[i-1] == v[(i+1) % len(v)] for i in range(len(v)))/len(v) for k, v in POLY.items()}
J = {'Sn': (15.178, -.222, -.045), 'Ge': (16.816, -1.054, -.344), 'C (diamond)': (25.448, -3.435, -.337),
     'Si': (10.587, -2.593, -.766), 'SiC': (2.735, -2.424, -.396)}
cols = ['#b8962e', '#3a6ea5', '#2e7d5b', '#9a5ba5', '#c0392b']
b.plot([0, 1], [0, 1], color='#222', lw=1, ls='--', label='law', zorder=5)
for (k, j), c in zip(J.items(), cols):
    e0 = E(POLY['3C'], j); e2 = E(POLY['2H'], j); xs = sorted(hh, key=hh.get)
    b.plot([hh[p] for p in xs], [(E(POLY[p], j)-e0)/(e2-e0) for p in xs], 'o-', color=c, lw=1, ms=4, mec='white', mew=0.6, label=k)
b.set_xlabel('hexagonality h'); b.set_ylabel('energy above 3C, scaled by 2H')
b.set_title('(b) Tetrahedral elements: distance from the law', fontsize=9, loc='left'); b.legend(fontsize=6.8, frameon=False, loc='upper left')
for ax in (a, b): ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(); fig.savefig(os.path.expanduser('~/kres-tmp/tetra.png'))
for k, j in J.items():
    e0 = E(POLY['3C'], j); print(k, {p: round(E(POLY[p], j)-e0, 3) for p in POLY}, 'meV/bilayer')
