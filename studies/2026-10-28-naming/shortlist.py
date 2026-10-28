# Naming shortlist (DICTO approved 10-28): standout slices of the White Queen (#63) and Red Queen (#65) with codes
# W1-W62 / R1-R124 (appendix rows) and placeholder names. Renders each slice from the exact atlas hulls.
# Run on dicto-big-brother: ~/geom/bin/python shortlist.py
import json, pickle, os, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
H = os.path.expanduser('~/kres-tmp')
W = pickle.load(open(f'{H}/4d/data/atlas600.pkl', 'rb'))
R = pickle.load(open(f'{H}/studies/2026-10-27-white-queen-polar/data/atlas120.pkl', 'rb'))
ORDER = ['vertex-first', 'edge-first', 'face-first', 'cell-first']
def coded(K, P):
    items = [k for k in K]
    def it(k): return k['item'] if 'item' in k else k
    out = {}; n = 0
    allitems = json.load(open(f'{H}/4d/data/atlas600.json')) if P == 'W' else json.load(open(f'{H}/studies/2026-10-27-white-queen-polar/data/atlas120.json'))['slices']
    for d in ORDER:
        for o in sorted([o for o in allitems if o['direction'] == d], key=lambda o: o['h']):
            n += 1
            m = [k for k in K if it(k)['direction'] == d and it(k)['height'] == o['height'] and it(k)['at_vertex_layer'] == o['at_vertex_layer']]
            if m: out[P + str(n)] = m[0]
    return out
CW, CR = coded(W, 'W'), coded(R['slices'], 'R')
LIST = [  # code, placeholder name, note
    ('W1', 'Lion', 'the central slice, vertex-first; 42 corners, 80 triangles; twin counts with W58'),
    ('W58', 'Unicorn', 'cell-first; 42 corners, 80 triangles; same counts as the Lion; congruence not yet checked'),
    ('W5', 'Tweedledum', 'vertex-first; 32 corners, 60 triangles; twin counts with W22'),
    ('W22', 'Tweedledee', 'edge-first; 32 corners, 60 triangles'),
    ('W3', 'Jabberwock', 'vertex-first; 72 corners, 140 triangles: the largest all-triangle slice'),
    ('W43', 'Jubjub', 'face-first; 30 corners, 56 triangles'),
    ('W60', 'Bandersnatch', 'cell-first; 28 corners, 52 triangles'),
    ('W49', '(hold)', 'cell-first; 144 corners, the largest slices: W28, W30, W49, W51 share 144 corners and 218 faces; congruence to check before naming'),
    ('R77', 'Red King', 'pentagon-first central slice; 80 corners; two regular decagons; the polar of the White Queen\'s edge-first shadow'),
    ('R80', 'Walrus', 'pentagon-first; 120 corners, 62 faces of 3, 5, 6, 7 and 8 sides'),
    ('R113', 'Red Knight', 'cell-first; 120 corners; 20 triangles, 12 pentagons, 30 octagons'),
    ('R115', 'White Knight', 'cell-first; 120 corners; 30 squares, 20 hexagons, 12 decagons'),
    ('R33', 'Haigha', 'edge-first; 114 corners; the only slice with nine-sided faces (six of them)'),
    ('R35', 'Hatta', 'edge-first; 114 corners; the other 114-corner slice; faces of 3, 4, 6, 7 and 8 sides'),
]
fig = plt.figure(figsize=(16, 22), facecolor='#0b0d12')
fig.suptitle('Naming shortlist: standout slices of the White Queen (W) and the Red Queen (R)\nplaceholder names; codes = rows of the appendix tables of #63 v3 and #65 v2',
             color='white', fontsize=15, y=0.985)
cols = 4
for k, (code, name, note) in enumerate(LIST):
    rec = (CW if code[0] == 'W' else CR)[code]
    P = np.array(rec['fV'], float); P = P - P.mean(0); P /= np.abs(P).max()
    ax = fig.add_subplot(4, cols, k + 1, projection='3d'); ax.set_facecolor('#0b0d12'); ax.set_axis_off()
    col = '#e8e4d8' if code[0] == 'W' else '#c8423a'
    polys = [P[f] for f in rec['faces']]
    ax.add_collection3d(Poly3DCollection(polys, facecolor=col, edgecolor='#333', linewidths=0.4, alpha=0.95))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1); ax.view_init(22, 35); ax.set_box_aspect((1, 1, 1))
    ax.set_title(f'{code}  {name}', color='#d4af37', fontsize=13, pad=0)
    ax.text2D(0.5, -0.04, '\n'.join(__import__('textwrap').wrap(note, 44)), transform=ax.transAxes, ha='center', va='top', color='#ccc', fontsize=8)
fig.text(0.97, 0.01, 'DICTO', color='#d4af37', fontsize=16, ha='right', family='serif', weight='bold')
plt.subplots_adjust(hspace=0.35, wspace=0.05, top=0.94, bottom=0.04)
fig.savefig('naming-shortlist.png', dpi=110, facecolor=fig.get_facecolor())
fig.savefig('naming-shortlist.pdf', facecolor=fig.get_facecolor())
print('ok', [c for c, _, _ in LIST if c not in CW and c not in CR])
