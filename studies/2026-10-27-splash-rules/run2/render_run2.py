# Splash Rules run 2 picture: the pyrochlore walk's two hole pieces (O, Y) against lam, exact volumes from out/pyro_mix.json.
# Curves: pure c (cc), pure h (hh), the two mixed pieces (c under h, h under c) and the half-and-half mean (dashed).
# The Swap Rule holds exactly (ch + hc = cc + hh in every window); the half-and-half mean misses the mixed pieces.
import json, os, sys
import numpy as np, sympy as sp
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); L = sp.Symbol('lam')
d = json.load(open(os.path.join(HERE, 'out', 'pyro_mix.json')))
COL = {'cc': '#c9a646', 'hh': '#b8c2cc', 'ch': '#d97a3a', 'hc': '#4f7cc9'}
NAME = {'cc': 'pure c (3C)', 'hh': 'pure h (2H)', 'ch': 'mixed: c below, h above', 'hc': 'mixed: h below, c above'}
fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), facecolor='#2b2f36')
for ax, role, title in zip(axes, ('O', 'Y'), ('octahedral hole O (cut at mid-gap)', 'hole Y (a quarter of the gap above the lower layer)')):
    for w in d['windows']:
        o = w['roles'][role]
        if isinstance(o, str): continue
        x = np.linspace(float(sp.Rational(w['lo'])), float(sp.Rational(w['hi'])), 60)
        V = {k: sp.lambdify(L, sp.sympify(v)) for k, v in o['volumes'].items()}
        for k in ('cc', 'hh', 'ch', 'hc'): ax.plot(x, V[k](x) * np.ones_like(x), color=COL[k], lw=2, label=NAME[k] if w is d['windows'][1] else None)
        ax.plot(x, (V['cc'](x) + V['hh'](x)) / 2 * np.ones_like(x), color='white', lw=1, ls='--', label='½ c + ½ h' if w is d['windows'][1] else None)
        ax.axvline(float(sp.Rational(w['lo'])), color='#555b66', lw=0.6)
    ax.set_facecolor('#2b2f36'); ax.set_title(title, color='white', fontsize=11)
    ax.set_xlabel('weight λ (atoms − holes)', color='#ccc'); ax.set_ylabel('piece volume (ball spacing 1)', color='#ccc')
    ax.tick_params(colors='#ccc')
    for s in ax.spines.values(): s.set_color('#555b66')
axes[0].legend(facecolor='#2b2f36', labelcolor='white', fontsize=9, edgecolor='#555b66')
fig.suptitle('Splash Rules, run 2: pyrochlore stackings (6 words up to 6 layers, exact). Swap Rule holds in every window\n'
             '(mixed + mixed = pure c + pure h); the halves rule does not (mixed ≠ ½ c + ½ h).', color='white', fontsize=11)
fig.text(0.99, 0.01, 'DICTO', color='#c9a646', ha='right', fontsize=14, weight='bold')
plt.tight_layout(rect=(0, 0.03, 1, 0.93)); out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'splash-run2.png')
plt.savefig(out, dpi=130, facecolor=fig.get_facecolor()); print('wrote', out)
