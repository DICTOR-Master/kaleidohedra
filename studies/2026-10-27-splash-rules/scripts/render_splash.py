# Splash Rules picture: one panel per layer spacing s; rows = piece (role + layer steps around it, mirror-merged), columns = weight
# windows; colour = the exact rule found: all cubic, all hexagonal, halves, thirds, other mix, no rule, empty.
import json, glob, os, sys
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
D = os.path.expanduser('~/kres-tmp/splash/data')
COL = {'swap': '#d97a3a', 'cubic': '#c9a646', 'hex': '#b8c2cc', 'halves': '#4f7cc9', 'thirds': '#4caf6a', 'other': '#9a5fc0', 'same': '#7d8794', 'none': '#d0453b', 'empty': '#3b4048'}
NAME = {'swap': 'Swap Rule: the 2 mixed = the 2 pure', 'cubic': 'all cubic (pure c)', 'hex': 'all hexagonal (pure h)', 'halves': 'half c + half h', 'thirds': 'thirds (1/3, 2/3)',
        'other': 'other exact mix', 'same': 'c and h pieces equal here', 'none': 'no c/h mix', 'empty': 'absent / nothing to compare'}
def kind(x):
    f = x['fit']
    if x['volume'] in ('0',): return 'empty'
    if not isinstance(f, dict): return 'none' if f == 'none' else 'empty'
    if len(f) < 2 or any(not set(v) <= set('0123456789/-') for v in f.values()): return 'same'   # pure c = pure h here: any mix fits
    a, b = Fr(f.get('a', '0')), Fr(f.get('b', '0'))
    if (a, b) == (1, 0): return 'cubic'
    if (a, b) == (0, 1): return 'hex'
    if (a, b) == (Fr(1, 2), Fr(1, 2)): return 'halves'
    if {a, b} == {Fr(1, 3), Fr(2, 3)}: return 'thirds'
    return 'other'
files = sorted(glob.glob(f'{D}/s_*.json'), key=lambda p: Fr(json.load(open(p))['s']))
fig, axes = plt.subplots(1, len(files), figsize=(4.2 * len(files), 13), facecolor='#2b2f36')
axes = [axes] if len(files) == 1 else axes
for ax, p in zip(axes, files):
    d = json.load(open(p)); wins = sorted(d['mix'], key=Fr)
    rows = sorted({(x['role'], x['ctx']) for w in wins for x in d['mix'][w]})
    cell = {(w, x['role'], x['ctx']): kind(x) for w in wins for x in d['mix'][w]}
    import sympy as sp
    for w in wins:                                   # Swap Rule check, exact: V(c under h) + V(h under c) = V(cc) + V(hh)
        for role in ('tetX', 'tetY'):
            V = {x['ctx']: sp.sympify(x['volume']) for x in d['mix'][w] if x['role'] == role}
            if all(k in V for k in ('--+', '-++', '---', '-+-')) and sp.expand(V['--+'] + V['-++'] - V['---'] - V['-+-']) == 0:
                for k in ('--+', '-++'):
                    if cell[(w, role, k)] == 'none': cell[(w, role, k)] = 'swap'
    for j, w in enumerate(wins):
        for i, r in enumerate(rows):
            ax.add_patch(plt.Rectangle((j, i), 0.94, 0.9, color=COL[cell.get((w, *r), 'empty')]))
    ax.set_xlim(0, len(wins)); ax.set_ylim(len(rows), 0); ax.set_facecolor('#2b2f36')
    ax.set_xticks([j + 0.47 for j in range(len(wins))]); ax.set_xticklabels([f'λ>{w}' for w in wins], rotation=60, color='#ccc', fontsize=7)
    ax.set_yticks([i + 0.45 for i in range(len(rows))]); ax.set_yticklabels([f'{r[0]} {r[1]}' for r in rows], color='#ccc', fontsize=5, family='monospace')
    ax.set_title(f"layer spacing² = {d['s']} × 2/3\nreach: {d['rmin']} gap(s) each side", color='white', fontsize=10)
    for s in ax.spines.values(): s.set_visible(False)
fig.legend(handles=[Patch(color=COL[k], label=NAME[k]) for k in COL], loc='lower center', ncol=5, facecolor='#2b2f36', labelcolor='white', fontsize=9)
fig.suptitle('Splash Rules, run 1: hole pieces of close-packed stackings, every piece against the pure cubic and hexagonal ones (exact)', color='white', fontsize=12)
fig.text(0.99, 0.005, 'DICTO', color='#c9a646', ha='right', fontsize=14, weight='bold')
plt.tight_layout(rect=(0, 0.03, 1, 0.96)); out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/kres-tmp/splash/splash-run1.png')
plt.savefig(out, dpi=130, facecolor=fig.get_facecolor()); print('wrote', out)
