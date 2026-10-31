# Splash figures for Splash Rules II (run on dicto-big-brother): python3 figs.py out/splash2_perovskite.json <figdir>
# Floats only for drawing; every value plotted is an exact rational from splash.py.
import sys, os, json
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
D = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = plt.imread(next(p for p in (os.path.join(HERE, 'dicto-logo.png'), os.path.expanduser('~/kres-tmp/dicto-logo.png'), os.path.expanduser('~/k-research/papers/dicto-logo.png')) if os.path.exists(p)))
GOLD, INK, GREY, BLUE, RED, GREEN = '#b8962e', '#222222', '#9a9a9a', '#2f5d8a', '#a8402e', '#4b7a3a'
plt.rcParams.update({'font.size': 8, 'axes.linewidth': 1.0, 'font.family': 'DejaVu Sans'})
W = D['words']; KN = {k['word']: k['name'] for k in D['known']}
def F(s): return float(Fr(s))
def mark(fig):
    ab = AnnotationBbox(OffsetImage(LOGO, zoom=24 / LOGO.shape[0]), (0.995, 0.005), xycoords='figure fraction', box_alignment=(1, 0), frameon=False)
    fig.add_artist(ab); fig.text(0.955, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=6.5, color='#8a6d1c')
def scatter(ax, key, color, label=None, known=True):
    xs = [F(w['stats']['h']) for w in W]; ys = [F(w['Q'][key]) for w in W]
    rx = [F(w['stats']['h']) for w in W if w['random']]; ry = [F(w['Q'][key]) for w in W if w['random']]
    ax.scatter(xs, ys, s=9, color=color, alpha=0.55, linewidths=0, label=label, zorder=3)
    ax.scatter(rx, ry, s=16, facecolors='none', edgecolors=INK, linewidths=0.8, zorder=4)
    if known:
        for k in D['known']:
            if k['name'] in ('3C', '2H', '4H', '6H', '9R'):
                ax.scatter([F(k['stats']['h'])], [F(k['Q'][key])], s=26, marker='D', color=GOLD, edgecolors=INK, linewidths=0.7, zorder=5)

# Figure 1: the four panels of the splash
fig, axs = plt.subplots(2, 2, figsize=(7.4, 6.0), dpi=220)
a = axs[0, 0]
for key, c, lab, f in [('corner partners per B', BLUE, 'corner partners per B = 6(1 − h)', lambda h: 6 * (1 - h)),
                       ('A neighbours per B (r2=3/2)', GREEN, 'A neighbours per B = 8 − 2h', lambda h: 8 - 2 * h),
                       ('face partners per B', RED, 'face partners per B = 2h', lambda h: 2 * h),
                       ('face-sharing clusters per B (incl. single octahedra)', INK, 'face-sharing clusters per B = 1 − h', lambda h: 1 - h)]:
    a.plot([0, 1], [f(0), f(1)], color=c, lw=1.6, zorder=2); scatter(a, key, c, lab)
a.set_xlabel('hexagonality h'); a.set_ylabel('per B (per ABX$_3$)'); a.set_title('(a) straight lines in h (Swap Rule holds)', fontsize=8.5, loc='left')
a.set_ylim(-0.3, 10.8); a.legend(fontsize=6.3, frameon=False, loc='upper right')
b = axs[0, 1]
for key, c, lab in [('B with 0 shared faces', BLUE, 'B with 0 faces (corner-only)'), ('B with 1 shared faces', GREEN, 'B with 1 face (string end)'),
                    ('B with 2 shared faces', RED, 'B with 2 faces (string inside)')]:
    scatter(b, key, c, lab)
b.set_xlabel('hexagonality h'); b.set_ylabel('share of B'); b.set_title('(b) not lines in h: a band for each h', fontsize=8.5, loc='left')
b.set_ylim(-0.04, 1.4); b.legend(fontsize=6.3, frameon=False, loc='upper center')
c_ = axs[1, 0]
for key, c, lab in [('B with 0 shared faces', BLUE, '0 faces: 1 − 2h + p$_{hh}$'), ('B with 1 shared faces', GREEN, '1 face: 2h − 2p$_{hh}$'),
                    ('B with 2 shared faces', RED, '2 faces: p$_{hh}$'), ('B-B at r2=4', GOLD, 'B–B at r² = 4: (12 − 6p$_{hh}$)/12'),
                    ('strings (2 or more octahedra) per B', INK, 'strings per B: h − p$_{hh}$')]:
    fit = D['fits'][key]; scale = 12 if key == 'B-B at r2=4' else 1
    pred = [(F(fit['a']) + F(fit['b']) * F(w['stats']['h']) + F(fit['c']) * F(w['stats']['p_hh'])) / scale for w in W]
    ys = [F(w['Q'][key]) / scale for w in W]
    c_.scatter(pred, ys, s=9, color=c, alpha=0.6, linewidths=0, label=lab, zorder=3)
c_.plot([0, 1], [0, 1], color=GREY, lw=1.5, zorder=1)
c_.set_xlabel('a + b·h + c·p$_{hh}$ (exact fit)'); c_.set_ylabel('value'); c_.set_title('(c) exact on the plane in (h, p$_{hh}$): all 555 stackings', fontsize=8.5, loc='left')
c_.legend(fontsize=6.0, frameon=False, loc='upper left')
d = axs[1, 1]
for L, c in [(1, BLUE), (2, GREEN), (3, RED), (4, GOLD), (5, INK)]:
    key = f'clusters of {L} octahedra per B'
    scatter(d, key, c, f'{L} octahedr{"on" if L == 1 else "a"}: window {L + 1} layers ({"c" + "h" * (L - 1) + "c"})', known=False)
d.set_xlabel('hexagonality h'); d.set_ylabel('clusters per B'); d.set_title('(d) cluster sizes: each needs its own window', fontsize=8.5, loc='left')
d.set_ylim(-0.04, 1.5); d.legend(fontsize=6.0, frameon=False, loc='upper right')
for ax in axs.flat:
    ax.grid(color='#e6e6e6', lw=0.6, zorder=0)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.tight_layout(rect=(0, 0.035, 1, 1)); mark(fig); fig.savefig(os.path.join(out, 'splash2-perovskite.png')); plt.close(fig)

# Figure 2: B-B distance shells, coloured by the number of layers g between the two B (window g)
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=220)
cols = {1: RED, 2: GREEN, 3: BLUE, 4: GOLD}
shells = [k for k in D['keys'] if k.startswith('B-B at r2=')]
for key in shells:
    m = D['fits'][key]['m']; r2 = Fr(key.split('=')[1])
    xs = [float(r2)] * len(W); ys = [F(w['Q'][key]) for w in W]
    ax[0].scatter(xs, ys, s=7, color=cols.get(m, INK), alpha=0.35, linewidths=0, zorder=3)
for m, c in cols.items(): ax[0].scatter([], [], s=12, color=c, label=f'window {m} layer{"s" if m > 1 else ""}')
ax[0].set_xlabel('B–B squared distance r² (X–X = 1)'); ax[0].set_ylabel('B neighbours per B'); ax[0].legend(fontsize=6.5, frameon=False)
ax[0].set_title('(a) each shell: spread over all stackings', fontsize=8.5, loc='left')
for key, c in [('B-B at r2=2/3', RED), ('B-B at r2=8/3', GREEN), ('B-B at r2=32/3', GOLD)]:
    scatter(ax[1], key, c, key.replace('B-B at r2=', 'B–B at r² = '), known=False)
ax[1].set_xlabel('hexagonality h'); ax[1].set_ylabel('per B'); ax[1].legend(fontsize=6.5, frameon=False)
ax[1].set_title('(b) B straight above: 1, 2 and 4 gaps apart', fontsize=8.5, loc='left')
for a_ in ax:
    a_.grid(color='#e6e6e6', lw=0.6, zorder=0)
    for s in ('top', 'right'): a_.spines[s].set_visible(False)
fig.tight_layout(rect=(0, 0.08, 1, 1)); mark(fig); fig.savefig(os.path.join(out, 'shells.png')); plt.close(fig)
print('ok')
