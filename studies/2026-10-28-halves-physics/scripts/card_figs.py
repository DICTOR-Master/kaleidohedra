# Site card pictures (1440x1080) for #64 (Swap Rule) and #66 (Hexagonality Law): rock salt / NiAs octahedral pieces
# at weight lam = 1/3 (window 7/24..3/8), exact volumes from run 2 (out/rocksalt_mix.json), evaluated as fractions.
import json, os
from fractions import Fraction as F
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', '2026-10-27-splash-rules', 'run2', 'out', 'rocksalt_mix.json')))
lam = F(1, 3)
w = next(w for w in d['windows'] if F(w['lo']) < lam < F(w['hi']))
V = {k: eval(e.replace('lam', '(F(1,3))').replace('/', '*F(1,1)/'), {'F': F}) for k, e in w['roles']['O']['volumes'].items()}
BG, INK, MUTED, GOLD, BLUE = '#0b0d12', '#e8e4d8', '#9a9a9a', '#a9862a', '#3f7cb8'
def style(ax):
    ax.set_facecolor(BG)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'): ax.spines[s].set_color('#444')
    ax.tick_params(colors=MUTED, labelsize=13); ax.set_axisbelow(True); ax.grid(axis='y', color='#222', lw=0.8)
# #66: per-layer octahedral volume against hexagonality, six stackings on one line
words = {'ABC (3C)': F(0), 'ABCACB (6H)': F(1, 3), 'ABACB (10H)': F(2, 5), 'ABCB (4H)': F(1, 2), 'ABCBAB (6H)': F(2, 3), 'AB (2H)': F(1)}
a, b = V['cc'], V['hh']
fig, ax = plt.subplots(figsize=(14.4, 10.8), dpi=100, facecolor=BG); style(ax)
ax.plot([0, 1], [float(a), float(b)], color=GOLD, lw=2, zorder=1)
for name, x in words.items():
    y = a + x * (b - a)
    ax.scatter([float(x)], [float(y)], s=110, color=GOLD, edgecolor=BG, linewidth=2, zorder=2)
    ax.annotate(name, (float(x), float(y)), xytext=(10, 10), textcoords='offset points', color=INK, fontsize=13)
ax.set_xlabel('hexagonality (share of hexagonal layers)', color=INK, fontsize=15)
ax.set_ylabel('octahedral piece volume per layer', color=INK, fontsize=15)
ax.set_title('The Hexagonality Law: every stacking on one straight line\nrock salt / nickel arsenide, octahedral pieces, weight λ = 1/3, exact',
             color=INK, fontsize=19, pad=18, loc='left')
fig.text(0.97, 0.03, 'DICTO', color='#d4af37', fontsize=22, ha='right', family='serif', weight='bold')
fig.subplots_adjust(left=0.12, right=0.95, top=0.85, bottom=0.12)
fig.savefig(os.path.join(HERE, '..', 'figures', 'hexagonality-law.png'), facecolor=BG); plt.close(fig)
# #64: Swap Rule, two stacked bars of equal height
fig, ax = plt.subplots(figsize=(14.4, 10.8), dpi=100, facecolor=BG); style(ax)
bars = [('mixed pieces', V['ch'], V['hc'], 'c under h', 'h under c'), ('pure pieces', V['cc'], V['hh'], 'c under c', 'h under h')]
for i, (lab, lo, hi, l1, l2) in enumerate(bars):
    ax.bar(i, float(lo), width=0.5, color=GOLD if i else BLUE, edgecolor=BG, linewidth=2)
    ax.bar(i, float(hi), bottom=float(lo), width=0.5, color=GOLD if i else BLUE, edgecolor=BG, linewidth=2, alpha=0.7)
    ax.text(i, float(lo) / 2, l1, ha='center', va='center', color=INK, fontsize=15)
    ax.text(i, float(lo) + float(hi) / 2, l2, ha='center', va='center', color=INK, fontsize=15)
    ax.text(i, float(lo + hi) + 0.02, f'{float(lo + hi):.4f}', ha='center', color=INK, fontsize=14)
assert V['ch'] + V['hc'] == V['cc'] + V['hh']
ax.set_xticks([0, 1]); ax.set_xticklabels([b[0] for b in bars], color=INK, fontsize=16); ax.set_xlim(-0.6, 1.6)
ax.set_ylabel('octahedral piece volume', color=INK, fontsize=15)
ax.set_title('The Swap Rule in crystals: the two mixed pieces add up to the two pure ones\nrock salt / nickel arsenide, octahedral pieces, weight λ = 1/3, exact',
             color=INK, fontsize=19, pad=18, loc='left')
fig.text(0.97, 0.03, 'DICTO', color='#d4af37', fontsize=22, ha='right', family='serif', weight='bold')
fig.subplots_adjust(left=0.12, right=0.95, top=0.85, bottom=0.1)
fig.savefig(os.path.join(HERE, '..', 'figures', 'swap-crystals.png'), facecolor=BG); plt.close(fig)
print('ok', {k: float(v) for k, v in V.items()})
