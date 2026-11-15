"""Pilot pictures: field and segmentation boundaries for a few thresholds; prints the field ranges, the sign check of uz
(correlation of temperature and uz at the surface: positive = upflow positive), and cell counts per threshold.
Usage: render_pilot.py DATA RUN OUTDIR"""
import sys, os, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tiles as TL
data, run, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
T = 10 ** np.load(f'{data}/{run}_lgtg_dz0.0.npy', mmap_mode='r')[0].astype(float)
U = np.load(f'{data}/{run}_uz_dz0.1.npy', mmap_mode='r')[0].astype(float)
U0 = np.load(f'{data}/{run}_uz_dz0.0.npy', mmap_mode='r')[0].astype(float)
print('T range', T.min(), T.max(), 'std', T.std())
print('uz range', U.min(), U.max(), 'std', U.std(), 'corr(T, uz at tau1)', np.corrcoef(T.ravel(), U0.ravel())[0, 1])
res = {}
fig, ax = plt.subplots(2, 3, figsize=(15, 10))
for i, (name, img, hs) in enumerate((('T', T, [0.02, 0.05, 0.1]), ('uz', U, [0.02, 0.05, 0.1]))):
    for j, hr in enumerate(hs):
        h = hr * img.std() * 10 if False else hr * (img.max() - img.min())
        lab = TL.segment(img, 1.5, h)
        G = TL.graph(lab); n = len(np.unique(lab))
        res[f'{name}_h{hr}'] = dict(h=h, cells=n, euler=TL.torus_euler(n, G), loops=G['loops'], odd=G['odd'],
                                    jdeg={k: sum(1 for c, _ in G['junctions'] if len(c) == k) for k in (3, 4, 5)})
        b = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
        a = ax[i, j]; a.imshow(img, origin='lower', cmap='gray'); a.imshow(np.ma.masked_where(~b, b), origin='lower', cmap='autumn', alpha=0.8)
        a.set_title(f'{name}  h = {hr} x range  cells {n}'); a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(f'{out}/pilot_segmentation.png', dpi=70)
print('SEG', json.dumps(res))
