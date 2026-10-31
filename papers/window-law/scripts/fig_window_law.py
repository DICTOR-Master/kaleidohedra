# The Window Law in one picture (dicto-big-brother): ~/geom/bin/python fig_window_law.py <data dir> <out png>
# <data dir> holds splash2_perovskite.json, splash2_fk.json, sturm.json, abfam.json from the three Splash Rules II studies.
# Every plotted value is exact (Fraction) and every point is asserted to lie on its law before drawing; floats only for drawing.
import sys, os, json, math
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

IN, OUT = sys.argv[1], sys.argv[2]
LOGO = plt.imread(os.path.expanduser('~/kres-tmp/dicto-logo.png'))
GOLD, INK, GREY, BLUE, RED, GREEN, PURPLE = '#b8962e', '#222222', '#9a9a9a', '#2f5d8a', '#a8402e', '#4f7d3a', '#6a4c93'
plt.rcParams.update({'font.size': 8, 'axes.linewidth': 1.0, 'font.family': 'DejaVu Sans', 'axes.edgecolor': '#555555'})
def mark(fig):
    fig.add_artist(AnnotationBbox(OffsetImage(LOGO, zoom=24 / LOGO.shape[0]), (0.995, 0.005), xycoords='figure fraction', box_alignment=(1, 0), frameon=False))
    fig.text(0.962, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=6.5, color='#8a6d1c')
def style(ax):
    ax.grid(True, color='#e6e6e6', linewidth=0.6, zorder=0); ax.tick_params(length=3, width=0.8)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
J = lambda f: json.load(open(os.path.join(IN, f)))

def shares(word, a, b):
    """share of letter b and of neighbouring bb pairs in the cyclic word over {a, b}"""
    n = len(word); assert set(word) <= {a, b}
    return Fr(word.count(b), n), Fr(sum(word[i] == b and word[(i + 1) % n] == b for i in range(n)), n)

def solve3(rows):
    """exact solve of value = al + be*x + ga*p from three independent rows (x, p, value)"""
    import itertools
    for r in itertools.combinations(rows, 3):
        M = [[Fr(1), x, p, v] for x, p, v in r]
        try:
            for c in range(3):
                piv = next(i for i in range(c, 3) if M[i][c] != 0); M[c], M[piv] = M[piv], M[c]
                for i in range(3):
                    if i != c and M[i][c] != 0:
                        f = M[i][c] / M[c][c]; M[i] = [M[i][k] - f * M[c][k] for k in range(4)]
            return [M[i][3] / M[i][i] for i in range(3)]
        except StopIteration:
            continue
    raise ValueError

pts = {}   # family -> list of (second number, departure / coefficient)
plane = {}  # family -> list of (one number, second number)

# 1. perovskite: every plane count (h, p_hh) over all 555 stackings
P = J('splash2_perovskite.json')
pk = [k for k, f in P['fits'].items() if f['kind'] == 'line in (h, p_hh)']
pts['per'] = []; plane['per'] = []
for w in P['words']:
    h, p = Fr(w['stats']['h']), Fr(w['stats']['p_hh']); plane['per'].append((h, p, w['random']))
    for k in pk:
        f = P['fits'][k]; a, b, c = Fr(f['a']), Fr(f['b']), Fr(f['c']); v = Fr(w['Q'][k])
        assert v == a + b * h + c * p
        pts['per'].append((p, (v - a - b * h) / c))
assert len(P['words']) == 555 and len(pk) == 9

# 2. Frank-Kasper layered families: window-2 counts per unit
FK = json.load(open(os.path.join(IN, 'splash2_fk.json')))
for fam, win, A, B in (('st', 'window_st', 'T', 'S'), ('fk59', 'window_fk59', 'L', '0')):
    S = [s for s in FK['structures'] if s['kind'] == fam]
    rows = []
    for s in S:
        wd = s['meta']['word'] if fam == 'st' else ''.join('0' if ch == '0' else 'L' for ch in s['meta']['word'])
        x, p = shares(wd, A, B); rows.append((s, x, p))
    plane[fam] = [(x, p, False) for _, x, p in rows]
    keys = [k for k, v in FK[win].items() if v[0] == 2]
    pts[fam] = []
    for k in keys:
        data = [(x, p, Fr(s['census'].get(k, 0), s['meta']['units'])) for s, x, p in rows]
        al, be, ga = solve3(data)
        assert ga != 0
        for x, p, v in data:
            assert v == al + be * x + ga * p, (fam, k)
            pts[fam].append((p, (v - al - be * x) / ga))
    print(fam, len(S), 'structures', len(keys), 'window-2 counts')

# 3. Frank-Kasper, every structure: Zbar minus the YK line, over -(6/5), against a0
fkz = []
for s in FK['structures']:
    if s['kind'] == 'cif' and s['meta'].get('nonfk'): continue
    if not s.get('ok', True): continue
    x12, a0, Z = Fr(s['x']['12']), Fr(s['a0']), Fr(s['Zbar'])
    fkz.append((a0, (Z - Fr(68, 5) + Fr(2, 5) * x12) / Fr(-6, 5)))
for t in FK['table']:
    n = t['counts']; N = sum(n); x = [Fr(c, N) for c in n]
    Z = Fr(12 * n[0] + 14 * n[1] + 15 * n[2] + 16 * n[3], N); a0 = x[0] - x[1] / 3 - 7 * x[2] / 6 - 2 * x[3]
    assert a0 == Fr(t['a0'])
    fkz.append((a0, (Z - Fr(68, 5) + Fr(2, 5) * x[0]) / Fr(-6, 5)))
assert all(abs(u - v) == 0 for u, v in fkz)
pts['fkz'] = fkz; print('FK Zbar points', len(fkz), 'off the line', sum(u != 0 for u, v in fkz))

# 4. 1D approximants: pair frequencies minus the chamber line of 1/phi^2 (a <= 1/2), over the Swap defect of the pair
St = J('sturm.json')
line = {'LL': lambda a: 1 - 2 * a, 'LS': lambda a: a, 'SL': lambda a: a, 'SS': lambda a: Fr(0)}
dlt = {'LL': 1, 'LS': -1, 'SL': -1, 'SS': 1}
pts['1d'] = []; plane['1d'] = []
for aq, fr in St['approximants'].items():
    a = Fr(aq); f2 = fr['2']; pSS = Fr(f2.get('SS', '0'))
    assert pSS == max(Fr(0), 2 * a - 1)
    plane['1d'].append((a, pSS, False))
    for u in ('LL', 'LS', 'SL', 'SS'):
        v = Fr(f2.get(u, '0')); pts['1d'].append((pSS, (v - line[u](a)) / dlt[u]))
assert len(St['approximants']) == 1101

# 5. Ammann-Beenker square approximants: star counts minus the chamber law, over the transfer coefficient, per vertex
AB = J('abfam.json')
code = {'F': '00100101', 'E': '00101101', 'D': '01011011', 'C': '01101111', 'B': '01111111', 'A': '11111111', 'X': '01011111'}
law = {'F': (0, 1), 'E': (2, -2), 'D': (-4, 6), 'C': (10, -14), 'B': (-12, 17), 'A': (5, -7), 'X': (0, 0)}
kap = {'F': 0, 'E': 0, 'D': -1, 'C': 2, 'B': -3, 'A': 1, 'X': 1}
pts['ab'] = []; nin = 0
for r in AB['rows']:
    R, Q, N = r['R'], r['Q'], r['N']; st = {k: Fr(r['stars'].get(c, '0')) for k, c in code.items()}
    assert sum(st.values()) == N == R + Q
    X = st['X']
    for k in code:
        dev = st[k] - (law[k][0] * R + law[k][1] * Q)
        assert dev == kap[k] * X, (r['t'], k)
        if kap[k]: pts['ab'].append((X / N, dev / kap[k] / N))
    nin += X == 0
print('AB approximants', len(AB['rows']), 'inside chamber (X = 0)', nin)

# ---------------- figure
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.95), dpi=240, gridspec_kw={'width_ratios': [1.06, 1, 1]})
# (a) one plane for every two-letter word
a = axs[0]; style(a)
a.fill([0, 0.5, 1, 0], [0, 0, 1, 0], color='#f4efe0', zorder=1, lw=0)
pp = plane['per']
a.scatter([float(h) for h, p, r in pp if not r], [float(p) for h, p, r in pp if not r], s=5, color=GREY, alpha=.55, lw=0, zorder=2, label='perovskite polytypes (505)')
a.scatter([float(h) for h, p, r in pp if r], [float(p) for h, p, r in pp if r], s=6, facecolor='none', edgecolor=GREY, lw=.5, zorder=2, label='random stackings (50)')
a.scatter([float(x) for x, p, _ in plane['fk59']], [float(p) for x, p, _ in plane['fk59']], s=9, marker='^', color=BLUE, alpha=.7, lw=0, zorder=3, label='Frank–Kasper slab words (119)')
a.scatter([float(x) for x, p, _ in plane['st']], [float(p) for x, p, _ in plane['st']], s=9, marker='s', color=GREEN, alpha=.7, lw=0, zorder=3, label='square–triangle row words (62)')
a.plot([0, .5, 1], [0, 0, 1], color=GOLD, lw=1.6, zorder=4, label='1D approximants: p = max(0, 2a − 1)')
phi = (1 + 5 ** .5) / 2
a.scatter([1 / phi ** 2], [0], marker='*', s=70, color=RED, zorder=6, label='Fibonacci, a = 1/φ²')
lab = {'3C': (0, 0, (3, 5)), '2H': (1, 1, (-14, -2)), '4H': (.5, 0, (4, 3)), '12R': (.5, .25, (-17, 1)), '10H': (.6, .4, (-18, 2)), "10H′": (.6, .2, (4, -3))}
for t, (x, y, off) in lab.items():
    a.scatter([x], [y], marker='D', s=16, color=GOLD, edgecolor=INK, lw=.6, zorder=7)
    a.annotate(t, (x, y), xytext=off, textcoords='offset points', fontsize=6.6, color=INK)
a.set_xlabel('the one number: h, z, s or a'); a.set_ylabel('the second number: share of hh pairs')
a.set_title('(a) one plane for all two-letter words', fontsize=8, loc='left')
a.set_xlim(-.03, 1.03); a.set_ylim(-.06, 1.05)
a.legend(fontsize=5.3, loc='upper left', frameon=False, handletextpad=.3, borderaxespad=.1, labelspacing=.25)
# (b) collapse, (c) zoom
fam = [('1d', '1D approximants: 4 pairs × 1101', GOLD, 'D', 14), ('per', 'perovskites: 9 counts × 555', GREY, 'o', 7),
       ('st', 'square–triangle rows: 26 counts × 62', GREEN, 's', 6), ('fk59', 'Frank–Kasper slabs: 16 counts × 119', BLUE, '^', 6),
       ('ab', 'Ammann–Beenker: 5 stars × 246', PURPLE, 'v', 8), ('fkz', f'Frank–Kasper Z̄, {len(pts["fkz"])} structures (YK defect a₀)', RED, 'X', 22)]
for ax, lim, title in ((axs[1], (-.1, 1.05), '(b) every family on one diagonal'), (axs[2], (-.085, .16), '(c) close to zero')):
    style(ax); ax.plot(lim, lim, color=INK, lw=.8, zorder=1)
    for k, lbl, col, m, s in fam:
        xs = [float(u) for u, v in pts[k] if lim[0] <= u <= lim[1]]; ys = [float(v) for u, v in pts[k] if lim[0] <= u <= lim[1]]
        ax.scatter(xs, ys, s=s, marker=m, color=col, alpha=.75 if k != 'fkz' else 1, lw=0, zorder=3 if k != 'fkz' else 6, label=lbl)
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_title(title, fontsize=8, loc='left')
    ax.set_xlabel('second number: p, a₀ or X per vertex', fontsize=7.5)
axs[1].set_ylabel('(count − line in the one number) / Δ', fontsize=7.5)
axs[1].legend(fontsize=5.3, loc='upper left', frameon=False, handletextpad=.3, borderaxespad=.1, labelspacing=.25)
axs[2].annotate('three hypothetical\nFrank–Kasper\nstructures', (-.045, -.045), xytext=(-.01, -.075), fontsize=6, color=RED, arrowprops=dict(arrowstyle='-', color=RED, lw=.6))
axs[2].annotate('Ammann–Beenker\nbeyond the walls', (.12, .12), xytext=(-.075, .12), fontsize=6, color=PURPLE, arrowprops=dict(arrowstyle='-', color=PURPLE, lw=.6))
axs[2].annotate('inside the chambers and\nall real phases: zero', (0, 0), xytext=(.05, -.02), fontsize=6, color=INK, arrowprops=dict(arrowstyle='-', color=INK, lw=.6))
fig.tight_layout(rect=(0, .055, 1, 1), w_pad=1.0)
mark(fig); fig.savefig(OUT); print('wrote', OUT)
