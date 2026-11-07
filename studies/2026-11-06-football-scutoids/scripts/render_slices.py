"""Figure for step 2b: slices of the football crystal's cells parallel to the layers, below the layer's middle plane, at the scutoid move,
and at the middle plane. Cell X(0,0,0) outlined; colours: this layer light/dark (X/Y), layer below and above in two other tones."""
import os, sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '0.12']
exec(open('cut_cells.py').read().split('# slices')[0])
TIGHT = os.environ.get('STACK') == 'tight'
if TIGHT:   # closest stacking: the move sits at the exact corner height (corner_exact.py), marked by rings
    import json
    CW = json.load(open('../data-corners-tight--0.094.json'))
    WS = [(-0.30, 'low'), (-0.13, 'just before the move'), (CW[0]['w'], 'at the scutoid corner: four cells\nmeet in a point (ringed)'), (0.0, 'middle plane: hexagons, 6 neighbours')]
else:
    WS = [(-0.30, 'low: 8 neighbours'), (-0.14, 'just before the move'), (-0.10, 'just after: the diagonal\nneighbours meet, the blue cell is pushed out'), (0.0, 'middle plane: hexagons, 6 neighbours')]
U = np.linspace(-1.6, 2.6, 900); Vv = np.linspace(-1.6, 2.6, 700); uu, vv = np.meshgrid(U, Vv, indexing='ij')
tone = {(0, 0): '#e9d8b4', (1, 0): '#b98f55', (0, -1): '#9fb7c9', (1, -1): '#5f86a6', (0, 1): '#c9a3a3', (1, 1): '#9c6464'}
ref = imgs.index((0, 0, 0, 0))
fig, axs = plt.subplots(1, 4, figsize=(18, 5.2), facecolor='#f6efdf')
for ax, (w, title) in zip(axs, WS):
    X = uu[..., None] * P1 + vv[..., None] * P2 + w * T
    _, idx = tree.query(X.reshape(-1, 3), workers=-1); L = lab[idx].reshape(uu.shape)
    xy = np.stack([X[..., :].reshape(-1, 3) @ (P1 / np.linalg.norm(P1)), X.reshape(-1, 3) @ np.cross(n, P1 / np.linalg.norm(P1))], 1).reshape(*uu.shape, 2)
    col = np.array([[int(tone[(imgs[l][0], int(np.sign(imgs[l][3])))][i:i + 2], 16) / 255 for i in (1, 3, 5)] for l in range(len(imgs))])
    img = col[L]
    edge = np.zeros(L.shape, bool); edge[1:] |= L[1:] != L[:-1]; edge[:, 1:] |= L[:, 1:] != L[:, :-1]
    img[edge] = (0.29, 0.22, 0.14)
    ax.pcolormesh(xy[..., 0], xy[..., 1], img, shading='auto')
    m = L == ref; ax.contour(xy[..., 0], xy[..., 1], m.astype(float), [0.5], colors='#7a1f1f', linewidths=2.2)
    if TIGHT and abs(w - CW[0]['w']) < 1e-6:
        Ein = P1 / np.linalg.norm(P1); Fin = np.cross(n, Ein)
        for c in CW:
            for p_, q_ in itertools.product(range(-3, 4), repeat=2):
                x = np.array(c['x']) + p_ * P1 + q_ * P2
                ax.plot([x @ Ein], [x @ Fin], 'o', ms=13, mfc='none', mec='#c0392b', mew=2.2)
    ax.set_title(f'height w = {w:+.{4 if TIGHT and abs(w - CW[0]["w"]) < 1e-6 else 2}f} (of one layer period)\n{title}', fontsize=12, color='#3a2c1a', family='serif')
    cx, cy = xy[..., 0][m].mean(), xy[..., 1][m].mean()
    ax.set_xlim(cx - 8, cx + 8); ax.set_ylim(cy - 7.5, cy + 7.5)
    ax.set_aspect('equal'); ax.axis('off')
fig.suptitle(('Closest stacking: ' if TIGHT else '') + 'Footballs in pentagon-hexagon layers: the cells sliced parallel to the layers (outlined: one ball\'s cell)',
             fontsize=13, family='serif', color='#3a2c1a')
fig.text(0.5, 0.06, 'sand / brown: this layer (two orientations)   blue: layer below (the panels climb to the middle plane; above it the picture mirrors with the layer above)   DICTO · dictospheres.com',
         ha='center', fontsize=9, family='serif', color='#5a4630')
OUT = '../football-slices-tight.png' if TIGHT else '../football-slices.png'
plt.savefig(OUT, dpi=130, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("FINAL ok" if os.path.getsize(OUT) > 10000 else "FINAL FAIL (figure missing or empty)")