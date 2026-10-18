# DICTO 2026-10-19: data for the #36 Golden Bodhi Pyrochlore cover image (dictospheres.com card) -> data/cover-render.json
# Same construction as hole_page.py (piece frame, hole axes, networks); the GBPC panel comes from studies/2026-10-16-ocd-pyrochlore render_adapter.html.
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'hole-piece.json'))); a = d['a']
og = json.load(open(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step23-envelope-meshes.json')))['ocd']
cyc = {0: np.eye(3), 1: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float), 2: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)}
def hole_axis(s):
    odd = [i for i in range(3) if s[i] % 2]; return odd[0] if len(odd) == 1 else [i for i in range(3) if i not in odd][0]
net = lambda s: 0 if (sum(s) % 4) in (0, 3) else 1
def scene(r):
    out = []
    for s in itertools.product(range(-7, 8), repeat=3):
        p = np.array(s) * a / 2
        if np.linalg.norm(p) > r: continue
        if sum(x % 2 for x in s) in (1, 2): out.append(dict(k='piece', p=p.tolist(), m=cyc[hole_axis(s)].ravel().tolist()))
        if len({x % 2 for x in s}) == 1: out.append(dict(k='y' if net(s) == 0 else 'b', p=p.tolist()))
    return out
six = [dict(k='piece', p=[0, 0, 0])] + [dict(k='y' if o['net'] == 0 else 'b', p=o['p']) for o in d['ocds']]
out = dict(meshes=dict(piece=dict(v=d['v'], t=d['t']), og=dict(v=og['v'], t=og['t'])), views=dict(six=six, piece=six[:1], net=scene(1.75 * a)))
json.dump(out, open(os.path.join(H, '..', 'data', 'cover-render.json'), 'w'), separators=(',', ':'))
print({k: len(v) for k, v in out['views'].items()})
