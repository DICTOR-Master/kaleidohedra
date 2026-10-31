# Figures for Star Cores paper D, "Eccentric Pieces" (2026-11-01).
#   valley-law.png  the valley at an edge of the solid, cut square to the edge, t = 2: the solid's dihedral angle delta, then the spikes of
#                   steps 1, 2, 3 on each side, each at the angle alpha, alpha' of the centre pyramids; left delta = 100 deg (open through
#                   step 2), right delta = 140 deg (closes at step 2)
#   pieces.png      the seven eccentric pieces and the FPD (D41) for contrast: the solid and its star after three steps of DICTO's valley
#                   rule at t = 2 (star_valley.py's rule, rebuilt by figs_paper_a.valley_build)
# Rendering from figs_paper_a.py (imported). Usage: figs_paper_d.py <dataset dir> <out dir> <logo png>
import json, os, sys, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../2026-10-30-star-cores/scripts'))   # star_core, star_valley, figs_paper_a
import figs_paper_a as FA
from figs_paper_a import plt, Scene, rot, mark, load, polyvol, GOLD, VIOLET, TEAL, LILAC, EDGE
from matplotlib.patches import Wedge
OUT = FA.OUT
def fig_law():
    fig, axs = plt.subplots(1, 2, figsize=(8, 4.1)); info = []
    for ax, delta in zip(axs, (100.0, 140.0)):
        a = delta / 2; start = 90 - delta / 2           # solid wedge centred on straight down... drawn pointing down
        base = 270 - delta / 2                          # the solid occupies [base, base + delta]
        ax.add_patch(Wedge((0, 0), 1, base, base + delta, fc='#e7e2d0', ec=EDGE, lw=0.8))
        cols = {1: VIOLET, 2: TEAL, 3: LILAC}; lo, hi = base, base + delta; over = None
        for k in (1, 2, 3):
            lo2, hi2 = lo - a, hi + a                     # f' side turns clockwise, f side anticlockwise
            ok = (hi2 - lo2) <= 360 + 1e-9
            for th1, th2 in ((lo2, lo), (hi, hi2)):
                ax.add_patch(Wedge((0, 0), 1 - 0.07 * k, th1, th2, fc=cols[k], ec=EDGE, lw=0.6, alpha=0.85 if ok else 0.35))
            if not ok and over is None: over = k; ax.add_patch(Wedge((0, 0), 1.02, lo2, hi2 - 360, fc='none', ec='#c0392b', lw=1.6, ls='--'))
            lo, hi = lo2, hi2
            if not ok: break
        ax.plot([0], [0], 'o', color=EDGE, ms=4)
        ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15); ax.set_aspect('equal'); ax.axis('off')
        k_open = int(360 // delta) - 1
        ax.set_title(f'δ = {delta:.0f}°: open through step {k_open}\nstep {k_open + 1} would overlap by {(k_open + 2) * delta - 360:.0f}° (dashed)', fontsize=9)
        info.append(dict(delta=delta, open_through=k_open))
    fig.text(0.5, 0.02, 'cut square to an edge e of the solid, t = 2: the solid (sand), spikes of step 1 violet, step 2 teal, step 3 lilac;\n'
             'every spike meets e at the angle α (or α′) of the centre pyramid on its side, so step k uses (k + 1)δ of the 360° round e', ha='center', fontsize=8.2)
    mark(fig); fig.savefig(os.path.join(OUT, 'valley-law.png'), dpi=300, facecolor='white'); plt.close(fig); return info
PIECES = [('dicto-lahdeli.json', 'Lahdeli (D77)'), ('dicto-chucky.json', 'Chucky (D80)'), ('dicto-triskelion-tetrahedron.json', 'Triskelion\nTetrahedron (D82)'),
          ('dicto-dodeca-13-wedge.json', 'Dodeca-13 Wedge (D6)'), ('dicto-samson.json', 'Samson (D71)'), ('dicto-fang.json', 'Fang (D81)'),
          ('dicto-shadow-17.json', 'Kagemusha (D86)'), ('dicto-fpd.json', 'FPD (D41), for contrast')]
def fig_pieces(t=2.0):
    fig, axs = plt.subplots(3, 6, figsize=(10, 6.0), gridspec_kw=dict(wspace=0.03, hspace=0.42)); M = rot(*FA.VIEW); info = []
    STEPC = {0: GOLD, 1: VIOLET, 2: TEAL, 3: LILAC}
    for i, (fn, nm) in enumerate(PIECES):
        r, c = i // 3, 2 * (i % 3)
        _, V0, F0 = load('solids/' + fn); V0 = V0 - V0.mean(0); st = FA.valley_build('solids/' + fn, t)
        lim = 1.04 * max(s['R'] for s in st)
        S = Scene(M); S.tris(V0, [list(f) for f in F0], [GOLD] * len(F0)); S.draw(axs[r, c], lim)
        s = st[-1]; S = Scene(M); S.tris(s['V'], s['F'], [STEPC[x] for x in s['tag']]); S.draw(axs[r, c + 1], lim)
        g23 = st[2]['vol'] / st[0]['vol']; v0 = polyvol(V0, F0)
        axs[r, c].set_title(nm, fontsize=7.6, loc='left', x=0.0)
        axs[r, c + 1].set_title(f'after 3 steps: volume ×{s["vol"] / v0:.2f}\nsteps 2–3 ×{g23:.2f}', fontsize=7.0)
        info.append(dict(shape=nm, vol_over_solid=s['vol'] / v0, growth23=g23, full=[x['full'] for x in st], spikes=[x['spikes'] for x in st]))
    axs[2, 4].axis('off'); axs[2, 5].axis('off')
    fig.text(0.5, 0.012, 'each pair: the solid (gold) and its star after three steps of DICTO\'s valley rule at t = 2;\n'
             'spikes of step 1 violet, step 2 teal, step 3 lilac. Same scale within each pair.', ha='center', fontsize=8.2)
    mark(fig); fig.savefig(os.path.join(OUT, 'pieces.png'), dpi=300, facecolor='white'); plt.close(fig); return info
if __name__ == '__main__':
    W = os.environ.get('FIGS', 'law,pieces').split(',')
    rep = dict(law=fig_law() if 'law' in W else None, pieces=fig_pieces() if 'pieces' in W else None)
    json.dump(rep, open(os.path.join(OUT, 'figs-info-' + '-'.join(W) + '.json'), 'w'), indent=1, default=float); print(json.dumps(rep, indent=1, default=float))
