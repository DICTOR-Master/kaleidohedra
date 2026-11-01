# Star Cores book (2026-11-01): the picture of every card, one PNG per shape (2 x 2 panels, 300 dpi, solid faces, dark edges >= 1.5 px).
#   convex shapes:      the solid | its star, centre rule t = phi (#78) | its star, polar spikes rho^2 = phi R^2 (#79) | the polar halo
#   non-convex shapes:  the solid | star, centre rule t = phi | star, centre rule t = 2 | the solid from another side
#   Maedate, Kuwagata:  one piece (t = 2) | Kagemusha with its five notch pieces | star step one at t = 2 | at t = phi
# Painter and construction code from figs_paper_a.py (study 2026-10-30-star-cores), imported, not copied; the notch pieces as built in
# kagemusha_variants.py (study 2026-11-01-star-cores-d). Faces of the solid coloured by face family (sides, distance from the centre).
# Usage: cards.py <dataset-v7 dir> <out dir> <logo png> <star-cores scripts dir> <star-cores.json + new4 json> <kagemusha-variants.json> [jobs]
import sys, os, json
DS, OUT, LOGO, SCR, SCJ, KV = sys.argv[1:7]; JOBS = int(sys.argv[7]) if len(sys.argv) > 7 else 12
sys.argv = [sys.argv[0], DS, OUT, LOGO]; sys.path.insert(0, SCR)
import numpy as np, multiprocessing as mp
import figs_paper_a as A
import matplotlib.pyplot as plt
from star_core import faces_info, load
phi = A.phi
FAM = ['#d4af37', '#8e5bd6', '#2bb3a3', '#c4a6ee', '#e07a3f', '#4a7fc1', '#b8434e', '#7fa34a', '#9aa3b5', '#d77fb3']
def fam_cols(FI):
    keys = [(len(f), round(c, 6)) for f, _, c in FI]; order = sorted(set(keys), key=lambda k: (-keys.count(k), k))
    return [FAM[order.index(k) % len(FAM)] for k in keys]
def oriented(V, F):
    """faces ccw seen from outside (Newell normal points away from the centre for the convex ones; non-convex files are already oriented)"""
    return [list(f) for f in F]
VIEW = A.VIEW
def panel(ax, scene, lim, title):
    scene.draw(ax, lim); ax.set_title(title, fontsize=10)
def card(item):
    slug, label = item
    try:
        d, V, F = load('solids/' + slug + '.json'); V = V - V.mean(0); F = oriented(V, F); FI = faces_info(V, F)
        convex = d.get('convex', d.get('checks', {}).get('convex', True))
        M = A.rot(*VIEW); M2 = A.rot(-28, 63)
        fig, axs = plt.subplots(2, 2, figsize=(8, 6.9), gridspec_kw=dict(wspace=0.03, hspace=0.10))
        R = np.linalg.norm(V, axis=1).max(); cols = fam_cols(FI)
        S = A.Scene(M); S.tris(V, F, cols); panel(axs[0, 0], S, 1.05 * R, 'the solid')
        cs = A.spike_cols(FI)
        def centre_star(ax, t, title):
            tips = [t * c * n for _, n, c in FI]; S = A.Scene(M)
            if min(c for _, _, c in FI) > 1e-9:
                for (f, n, c), tp, col in zip(FI, tips, cs): S.convex(np.vstack([V[f], tp]), col)
                lim = 1.04 * max(R, max(np.linalg.norm(tp) for tp in tips))
            else:
                S.tris(V, F, cols); lim = 1.05 * R; title += ' (no pyramids from the centre)'
            panel(ax, S, lim, title)
        centre_star(axs[0, 1], phi, 'star, centre rule, t = φ')
        if convex:
            g = A.polar('solids/' + slug + '.json'); lim = 1.03 * np.linalg.norm(g['tips'], axis=1).max()
            S = A.Scene(M)
            for Q, c in zip(g['spikes'], A.spike_cols(g['FI'])): S.convex(Q, c)
            panel(axs[1, 0], S, lim, 'star, polar spikes, ρ² = φR²')
            S = A.Scene(M); S.convex(g['tips'], '#d9cff0'); panel(axs[1, 1], S, lim, f'halo: hull of the {len(g["tips"])} tips')
        else:
            centre_star(axs[1, 0], 2.0, 'star, centre rule, t = 2')
            S = A.Scene(M2); S.tris(V, F, cols); panel(axs[1, 1], S, 1.05 * R, 'the solid, seen from below')
        A.mark(fig); fig.savefig(os.path.join(OUT, slug + '.png'), dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.05); plt.close(fig)
        return slug, 'ok'
    except Exception as e:
        import traceback; return slug, 'ERROR ' + traceback.format_exc()[-600:]
def notch_cards():
    """Maedate (conjoined piece) and Kuwagata (sloping-base pair) on Kagemusha (D86), as in kagemusha_variants.py"""
    d, V0, F0 = load('solids/dicto-shadow-17.json'); V0 = V0 - V0.mean(0); FI = faces_info(V0, F0)
    E = {}
    for i, (f, n, c) in enumerate(FI):
        for k in range(3): E.setdefault(tuple(sorted((f[k], f[(k + 1) % 3]))), []).append(i)
    def runs(i, e): f = F0[i]; k = f.index(e[0]); return f[(k + 1) % 3] == e[1]
    notches = [(e, i, j) for e, (i, j) in E.items()
               if np.cross(FI[i][1], FI[j][1]) @ ((V0[e[1]] - V0[e[0]]) if runs(i, e) else (V0[e[0]] - V0[e[1]])) < -1e-12]
    assert len(notches) == 5
    KVd = json.load(open(KV)); info = {}
    for variant, name in (('conjoined', 'maedate'), ('sloping', 'kuwagata')):
        def pieces(t):
            tip = lambda i: t * FI[i][2] * FI[i][1]; out = []
            for e, i, j in notches:
                a, b = V0[e[0]], V0[e[1]]; c = V0[[v for v in F0[i] if v not in e][0]]; c2 = V0[[v for v in F0[j] if v not in e][0]]
                if variant == 'conjoined': out.append([np.vstack([a, b, c, c2, tip(i), tip(j)])])
                else:
                    m = np.cross(b - a, -a); m /= np.linalg.norm(m); X = []
                    for cc, T in ((c, tip(i)), (c2, tip(j))):
                        s_ = (cc @ m) / ((cc - T) @ m); X.append(cc + s_ * (T - cc))
                    out.append([np.vstack([a, b, c, X[0]]), np.vstack([a, b, c2, X[0]])])
            return out
        P2 = pieces(2.0); M = A.rot(*VIEW)
        fig, axs = plt.subplots(2, 2, figsize=(8, 6.9), gridspec_kw=dict(wspace=0.03, hspace=0.10))
        S = A.Scene(A.rot(12, 40)); one = P2[0]; ctr = np.vstack(one).mean(0)
        for q, Q in enumerate(one): S.convex(Q - ctr + (0 if len(one) == 1 else 0.06 * (Q.mean(0) - ctr) / max(1e-9, np.linalg.norm(Q.mean(0) - ctr))), A.TEAL if q == 0 else '#5fd0c2')
        lim = 1.1 * max(np.linalg.norm(np.vstack(one) - ctr, axis=1)); panel(axs[0, 0], S, lim, ('Maedate, one piece, t = 2' if name == 'maedate' else 'Kuwagata, one pair, t = 2'))
        S = A.Scene(M); S.tris(V0, F0, [A.GOLD] * len(F0))
        for grp in P2:
            for Q in grp: S.convex(Q, A.TEAL)
        R = np.linalg.norm(V0, axis=1).max(); panel(axs[0, 1], S, 1.25 * R, 'Kagemusha with its five notch pieces (t = 2)')
        for ax, r in zip((axs[1, 0], axs[1, 1]), [r for r in KVd if r['variant'] == variant]):
            V = np.array(r['step1']['V']); V = V - 0; F = r['step1']['F']; kind = r['step1']['kind']
            col = {'solid': A.GOLD, 'spike': A.VIOLET, 'notch': A.TEAL}
            S = A.Scene(M); S.tris(V, F, [col[k] for k in kind])
            panel(ax, S, 1.04 * np.linalg.norm(V, axis=1).max(), f"star, step one, t = {'φ' if r['t'] == 'phi' else '2'}: ×{r['steps'][0]['volume_over_last']:.4f}")
        A.mark(fig); fig.savefig(os.path.join(OUT, name + '.png'), dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.05); plt.close(fig)
        info[name] = dict(piece_volume_t2=[float(A.vol(Q)) for Q in P2[0]])
    return info
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    items = []
    for f in SCJ.split(','):
        for r in json.load(open(f)): items.append((os.path.basename(r['file'])[:-5], r['name']))
    only = os.environ.get('ONLY'); items = [it for it in items if not only or it[0] in only.split(',')]
    with mp.get_context("fork").Pool(JOBS) as pool:
        for slug, st in pool.imap_unordered(card, items): print(slug, st, flush=True)
    if not only or 'notch' in only: print('notch', notch_cards(), flush=True)
    print('done', len(items))
