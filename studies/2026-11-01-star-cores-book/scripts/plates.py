# Star Cores book (2026-11-01): full-page plates (one large picture each, 300 dpi, solid faces, dark edges >= 1.5 px).
#   plate-gti.png       DICTO GTI (D40), polar spikes rho^2 = phi R^2, spikes by face family
#   plate-og.png        DICTO Ogdoecontahedron (D28), polar spikes
#   plate-ocd.png       OCD Stella (D29), polar spikes
#   plate-clasp.png     Golden Clasp (D107), polar spikes
#   plate-lahdeli.png   Lahdeli (D77), valley rule t = 2 after three steps (step colours as #79 Figure 3)
#   plate-kuwagata.png  Kagemusha (D86) with Kuwagata in its notches, step one, t = 2 (from kagemusha-variants.json)
# Usage: plates.py <dataset-v7 dir> <out dir> <logo png> <star-cores scripts dir> <kagemusha-variants.json>
import sys, os, json
DS, OUT, LOGO, SCR, KV = sys.argv[1:6]
sys.argv = [sys.argv[0], DS, OUT, LOGO]; sys.path.insert(0, SCR)
import numpy as np, multiprocessing as mp
import figs_paper_a as A
import matplotlib.pyplot as plt
def save(fig, name): A.mark(fig); fig.savefig(os.path.join(OUT, name), dpi=300, facecolor='white', bbox_inches='tight', pad_inches=0.04); plt.close(fig)
def polar_plate(args):
    slug, name, view = args
    g = A.polar('solids/' + slug + '.json'); lim = 1.02 * np.linalg.norm(g['tips'], axis=1).max()
    fig, ax = plt.subplots(figsize=(7.2, 8)); S = A.Scene(A.rot(*view))
    for Q, c in zip(g['spikes'], A.spike_cols(g['FI'])): S.convex(Q, c, lw=0.6)
    S.draw(ax, lim); save(fig, name); return name
def lahdeli(_):
    st = A.valley_build('solids/dicto-lahdeli.json', 2.0); s = st[-1]; C = {0: A.GOLD, 1: A.VIOLET, 2: A.TEAL, 3: A.LILAC}
    fig, ax = plt.subplots(figsize=(7.2, 8)); S = A.Scene(A.rot(*A.VIEW)); S.tris(s['V'], s['F'], [C[x] for x in s['tag']], lw=0.6)
    S.draw(ax, 1.03 * s['R']); save(fig, 'plate-lahdeli.png'); return 'plate-lahdeli.png'
def kuwagata(_):
    r = [r for r in json.load(open(KV)) if r['variant'] == 'sloping' and r['t'] == '2'][0]
    V = np.array(r['step1']['V']); C = dict(solid=A.GOLD, spike=A.VIOLET, notch=A.TEAL)
    fig, ax = plt.subplots(figsize=(7.2, 8)); S = A.Scene(A.rot(*A.VIEW)); S.tris(V, r['step1']['F'], [C[k] for k in r['step1']['kind']], lw=0.6)
    S.draw(ax, 1.03 * np.linalg.norm(V, axis=1).max()); save(fig, 'plate-kuwagata.png'); return 'plate-kuwagata.png'
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    jobs = [(polar_plate, ('dicto-gti', 'plate-gti.png', A.VIEW)), (polar_plate, ('dicto-ogdoecontahedron', 'plate-og.png', A.VIEW)),
            (polar_plate, ('dicto-ocd-stella', 'plate-ocd.png', A.VIEW)), (polar_plate, ('dicto-golden-clasp', 'plate-clasp.png', A.VIEW)),
            (lahdeli, None), (kuwagata, None)]
    with mp.get_context('fork').Pool(6) as pool:
        rs = [pool.apply_async(f, (a,)) for f, a in jobs]
        for r in rs: print(r.get(), flush=True)
    print('done')
