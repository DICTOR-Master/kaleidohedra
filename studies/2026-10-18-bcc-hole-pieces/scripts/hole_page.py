# DICTO 2026-10-18 bcc hole pieces -- 3D page -> renders/bcc-hole-pieces.html (kit viewer template)
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'hole-piece.json'))); a = d['a']
P = {'piece': dict(v=d['v'], t=d['t'], colour='#ffb74d'), 'y': dict(v=d['ocd_mesh']['v'], t=d['ocd_mesh']['t'], colour='#ffc857'),
     'b': dict(v=d['ocd_mesh']['v'], t=d['ocd_mesh']['t'], colour='#6fa8ff')}
cyc = {0: np.eye(3), 1: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float), 2: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)}   # x axis -> x, y, z
def hole_axis(s):
    odd = [i for i in range(3) if s[i] % 2]; return odd[0] if len(odd) == 1 else [i for i in range(3) if i not in odd][0]
net = lambda s: 0 if (sum(s) % 4) in (0, 3) else 1
def scene(r_h, r_o, centre=np.zeros(3)):
    out = []
    for s in itertools.product(range(-6, 7), repeat=3):
        p = np.array(s) * a / 2
        if sum(x % 2 for x in s) in (1, 2) and np.linalg.norm(p - centre) <= r_h:
            out.append(['piece', False, (p - centre).tolist(), cyc[hole_axis(s)].ravel().tolist()])
        if len({x % 2 for x in s}) == 1 and np.linalg.norm(p - centre) <= r_o:
            out.append(['y' if net(s) == 0 else 'b', False, (p - centre).tolist()])
    return out
h0 = np.array(d['centre'])
six = [['piece', False, [0, 0, 0]]] + [['y' if o['net'] == 0 else 'b', False, o['p']] for o in d['ocds']]
views = {
    'piece': dict(label='The hole piece', text='resin between 6 OCDs, one piece: the double-T / double-crescent shape', radius=0.9, place=[['piece', False, [0, 0, 0]]]),
    'six': dict(label='With its 6 OCDs', text='narrow pair (across the slab, 0.719 apart from the centre) and the wide four (1.017): yellow and blue = the two networks', radius=1.8, place=six),
    'net': dict(label='Network', text='yellow and blue OCDs (bcc double network) with every hole piece in place: fills space exactly', radius=3.4, place=scene(1.6 * a, 1.6 * a)),
    'resin': dict(label='Resin only', text='the hole pieces alone: the whole resin web cut into identical pieces, 3 per OCD', radius=3.0, place=[x for x in scene(1.6 * a, -1) if x[0] == 'piece']),
}
facts = ['Exact cut: every point of resin goes to its nearest 6-OCD hole (bcc octahedral hole). The holes are all alike, so <b>one piece shape fills all the resin</b>: 3 pieces per OCD.',
         f'Piece volume {d["volume"]:.6f} = (gap per OCD)/3 (gap = 22.57% of space); one solid (no holes through it); sphericity {d["sphericity"]:.3f}; centrosymmetric with a mirror — no left/right versions.',
         'Its 6 OCDs: a narrow pair across the slab (the central double-T) and a wide ring of four; the cell round the hole has 10 corners.']
html = open(os.path.join(H, 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Resin Hole Pieces', '__SUB__': 'DICTO 2026-10-18: the resin round the Golden Bodhi Pyrochlore double network, cut at the holes between 6 OCDs. Drag to turn.',
             '__MARK__': 'studies/2026-10-18-bcc-hole-pieces', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
open(os.path.join(H, '..', 'renders', 'bcc-hole-pieces.html'), 'w').write(html); print('ok', len(html))
