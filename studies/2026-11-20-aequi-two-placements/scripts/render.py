# (study 2026-11-20-aequi-two-placements: copy of the 2026-11-19-aequi-complete renderer; labels show D12p as D12′ etc.)
# Per-die renders from the refined data, in the style of study 2026-11-19-aequus-rd-ico (fig_d191_sheet.py, panels a, b):
# (a) the solid: solid faces, crisp edges, no haze; neutral label tones per face orbit (colours are labels only);
# (b) the Vacuus: one plate from the centre to each edge; slate = sloping, pale sand = on a mirror plane of the die's
#     own symmetry group. Then contact sheets by group (solid and Vacuus side by side; group + orbit set + N).
# usage: render.py dice.json exact.jsonl outdir NPROC [sheets SHEETDIR aequi.json]
import json, sys, os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
def save_small(fig, path, colors=96):
    fig.savefig(path, facecolor='white'); Image.open(path).convert('RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import show
TONES = ['#d9c7a3', '#5b6f8a', '#9aa79a', '#b8a89a', '#7f8c8d', '#c9b79c', '#8e9aaf', '#a3a380', '#6d7b74', '#cfc6b8', '#9c8f83', '#748a9c']
CS, CM = '#5b6f8a', '#d9c7a3'
L = np.array([0.45, -0.35, 0.82]); L /= np.linalg.norm(L)
def name(d):
    return '%04d-%s-%s' % (d['sid'], d['group'], '-'.join(x.replace('/', 'x').replace('+', 'p') for x in d['orbit_labels']))
LABELS = {}
def caption(d):
    lab = LABELS.get(d['sid'], show('%s: %s' % (d['group'], ' + '.join(d['orbit_labels']))))
    return '%s  N=%d%s' % (lab, d['N'], '  (two hands)' if d['chiral'] else '')
def draw(args):
    d, e, outdir = args
    V = np.array(e['verts']); faces = e['faces']; N = len(faces)
    forb = np.zeros(N, int)
    for k, O in enumerate(e['face_orbits']):
        for j in O: forb[j] = k
    # orbit tones follow the collect order (orbit k of the die = rec orbit k)
    cut = np.cumsum([0] + d['sizes']); tone_of = np.zeros(N, int)
    for k in range(len(d['sizes'])): tone_of[cut[k]:cut[k + 1]] = k
    R = np.linalg.norm(V, axis=1).max() * 0.82   # same framing for every die: the circumsphere fills the box
    out = []
    # (a) solid
    fig = plt.figure(figsize=(3, 3), dpi=100); ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    polys, cols = [], []
    for f, vi in enumerate(faces):
        P = V[vi]; n = P.mean(0); n /= np.linalg.norm(n)
        base = np.array(matplotlib.colors.to_rgb(TONES[tone_of[f] % len(TONES)]))
        polys.append(P); cols.append(np.clip(base * (0.55 + 0.45 * max(0.0, float(n @ L))), 0, 1))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolors='#1a1a1a', linewidths=0.5))
    for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-R, R)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58); ax.set_axis_off()
    plt.subplots_adjust(0, 0, 1, 1); p1 = os.path.join(outdir, name(d) + '-solid.png'); save_small(fig, p1); plt.close(fig)
    # (b) Vacuus
    M = [np.array(m) / np.linalg.norm(m) for m in e['mirrors']]
    edges = {}
    for vi in faces:
        for i in range(len(vi)):
            a, b = vi[i], vi[(i + 1) % len(vi)]
            k = (min(a, b), max(a, b))
            if k in edges: continue
            nrm = np.cross(V[a], V[b]); nrm /= np.linalg.norm(nrm)
            edges[k] = (V[a], V[b], not any(abs(abs(nrm @ m) - 1) < 1e-8 for m in M))
    fig = plt.figure(figsize=(3, 3), dpi=100); ax = fig.add_subplot(111, projection='3d', computed_zorder=False)
    O = np.zeros(3)
    ax.add_collection3d(Poly3DCollection([[O, a, b] for a, b, s in edges.values() if not s], facecolors=CM, edgecolors='none', alpha=0.35))
    ax.add_collection3d(Poly3DCollection([[O, a, b] for a, b, s in edges.values() if s], facecolors=CS, edgecolors=CS, linewidths=0.2, alpha=0.55))
    ax.add_collection3d(Line3DCollection([[a, b] for a, b, s in edges.values()], colors='#1a1a1a', linewidths=0.6))
    for s in (ax.set_xlim, ax.set_ylim, ax.set_zlim): s(-R, R)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=22, azim=-58); ax.set_axis_off()
    plt.subplots_adjust(0, 0, 1, 1); p2 = os.path.join(outdir, name(d) + '-vacuus.png'); save_small(fig, p2); plt.close(fig)
    return d['sid'], len(edges), sum(1 for x in edges.values() if x[2])
def sheets(dice, outdir, sheetdir, per=40):
    import matplotlib.image as mpimg
    from collections import defaultdict
    by = defaultdict(list)
    for d in dice: by[d['group']].append(d)
    made = []
    for g, L_ in by.items():
        L_.sort(key=lambda d: (d['m'], d['N'], d['sid']))
        pages = [L_[i:i + per] for i in range(0, len(L_), per)]
        for pi, page in enumerate(pages):
            cols = 4; rows = (len(page) + cols - 1) // cols
            fig = plt.figure(figsize=(cols * 4.2, rows * 2.35 + 0.5), dpi=80)
            for i, d in enumerate(page):
                for j, kind in enumerate(('solid', 'vacuus')):
                    ax = fig.add_axes([(i % cols + j * 0.5) / cols, 1 - (i // cols + 1) * (2.35 / (rows * 2.35 + 0.5)), 0.5 / cols, 2.0 / (rows * 2.35 + 0.5)])
                    ax.imshow(mpimg.imread(os.path.join(outdir, name(d) + '-%s.png' % kind))); ax.set_axis_off()
                fig.text((i % cols + 0.5) / cols, 1 - (i // cols + 1) * (2.35 / (rows * 2.35 + 0.5)) + 2.02 / (rows * 2.35 + 0.5),
                         caption(d), ha='center', va='bottom', fontsize=min(7.5, 7.5 * 52 / max(1, len(caption(d)))))
            fig.suptitle('Both icosahedron placements: Aequi with symmetry %s (%d dice)%s: solid (orbit tones are labels only) and Vacuus (slate sloping, sand on a mirror)'
                         % (g, len(L_), '' if len(pages) == 1 else ', page %d of %d' % (pi + 1, len(pages))), fontsize=10, y=0.999)
            p = os.path.join(sheetdir, 'sheet-%s%s.png' % (g, '' if len(pages) == 1 else '-p%d' % (pi + 1)))
            save_small(fig, p, 128); plt.close(fig); made.append(p)
    return made
if __name__ == '__main__':
    D = {d['sid']: d for d in json.load(open(sys.argv[1]))['dice']}
    E = {}
    for Lr in open(sys.argv[2]):
        r = json.loads(Lr)
        if r.get('exact_ok'): E[r['sid']] = r
    outdir = sys.argv[3]; os.makedirs(outdir, exist_ok=True)
    dice = [D[s] for s in sorted(E)]
    if len(sys.argv) > 7: LABELS.update({r['sid']: r['label'] for r in json.load(open(sys.argv[7]))})
    if len(sys.argv) > 5 and sys.argv[5] == 'sheets':
        made = sheets(dice, outdir, sys.argv[6]); print('sheets', len(made))
        print('FINAL ok' if made and all(os.path.exists(p) for p in made) else 'FINAL FAIL: sheets missing'); sys.exit()
    todo = [(D[s], E[s], outdir) for s in sorted(E) if not os.path.exists(os.path.join(outdir, name(D[s]) + '-vacuus.png'))]
    print('to render', len(todo), flush=True)
    import multiprocessing as mpc
    with mpc.get_context('fork').Pool(int(sys.argv[4])) as pool:
        for sid, ne, ns in pool.imap_unordered(draw, todo, chunksize=4): pass
    miss = [s for s in E if not all(os.path.exists(os.path.join(outdir, name(D[s]) + '-%s.png' % k)) for k in ('solid', 'vacuus'))]
    print('FINAL ok' if not miss else 'FINAL FAIL: %d dice without pictures' % len(miss))
