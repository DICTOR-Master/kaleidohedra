# DICTO 2026-10-17: "is there anything I can see first, artwork-wise, just to make sure the vision is shared — working version".
# Exports one bundle of the stacked hexagonal-prism tiling (scutoid_hexlayers_poly.build) as polygons for render_hexlayers.html:
# every piece's boundary faces (faces shared by two parts of the same piece dropped), plus the lattice vectors to repeat it.
# -> data/scutoid-hexlayers-render.json
import sys, json, numpy as np
exec(open('scripts/scutoid_hexlayers_poly.py').read().rsplit('\nif __name__', 1)[0])
prm = tuple(float(v) for v in sys.argv[1:6]) if len(sys.argv) > 5 else (1.85, 1.95, 2.10, 1.4, 1.1)
# capture each piece's parts: wrap union_measure
cap = {}
_um = union_measure
def um(parts):
    cap.setdefault('list', []).append(parts); return _um(parts)
union_measure = um
r = build(*prm)
keys = list(r['pieces'].keys()); lists = cap['list']
g = np.array([{'P': prm[0], 'Hd': prm[1], 'Ho': prm[2]}[x] for x in G]); rB = max(dA * g / np.linalg.norm(N, axis=1)); a, c = prm[3] * 2 * rB, prm[4] * 2 * rB
A1 = a * np.array([1, -1, 0]) / 2 ** .5; A2 = a * np.array([1, 0, -1]) / 2 ** .5; A3 = c * np.ones(3) / 3 ** .5
out = []
for k, parts in zip(keys, lists):
    faces = []
    for i, p in enumerate(parts):
        for f in p['faces']:
            sh = sum(shared_area(f, g2) for j, q in enumerate(parts) if j != i for g2 in q['faces'] if f[0] @ g2[0] < -1 + 1e-9 and abs(f[1] + g2[1]) < 1e-7)
            if sh < 0.999 * area3(f[2]): faces.append(np.round(f[2], 5).tolist())
    out.append(dict(name=k, psi=round(r['pieces'][k]['psi'], 3), vol=r['pieces'][k]['vol'], faces=faces))
json.dump(dict(mark='DICTO · dictospheres.com', params=prm, A=[A1.tolist(), A2.tolist(), A3.tolist()], pieces=out), open('data/scutoid-hexlayers-render.json', 'w'))
print('pieces', len(out), 'sum/cell', r['sum_vs_cell'], {k: v['psi'] for k, v in list(r['pieces'].items())[:3]})
