# Render data for bundle A of the two thin layers (exact check: scutoid_two_exact.py): every cell as float corners + polygon faces.
# -> data/scutoid-two-render.json  {core, layer1[], layer2[], close[]} each cell {g, v, f, n}
import numpy as np, json
from scipy.spatial import ConvexHull
exec(open('scripts/scutoid_two_layers.py').read().rsplit("\nR = []", 1)[0])
a1, k1, a2, k2, tf = 11/10, 8/7, 7/6, 21/20, 23/20
dM = planes(a1, k1); dB = planes(a1 * a2, k2)
def poly(V):
    V = np.asarray(V); h = ConvexHull(V); F = []; seen = []
    for eq in h.equations:
        if any(np.allclose(eq, s, atol=1e-7) for s in seen): continue
        seen.append(eq); idx = [i for i in range(len(V)) if abs(eq[:3] @ V[i] + eq[3]) < 1e-7]
        c = V[idx].mean(0); n = eq[:3]; u = V[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u)); F.append(idx)
    return dict(v=np.round(V, 6).tolist(), f=F)
def pack(cells, Nl):
    out = []
    for (g, V), i in zip(cells, range(len(Nl))):
        if V is None: continue
        d = poly(V); d['g'] = g; d['n'] = (Nl[i] / np.linalg.norm(Nl[i])).round(6).tolist(); out.append(d)
    return out
VB = corners(N, dB); r = (VB @ RDN.T).max() * tf
RDV = np.array([[s * r, 0, 0] for s in (1, -1)] + [[0, s * r, 0] for s in (1, -1)] + [[0, 0, s * r] for s in (1, -1)] + [[a * r / 2, b * r / 2, c * r / 2] for a in (1, -1) for b in (1, -1) for c in (1, -1)])
J = dict(core=poly(TI), layer1=pack(sweep_cells(N, dA, dM, G), N), layer2=pack(sweep_cells(N, dM, dB, G), N),
         close=pack(sweep_cells(NR, np.r_[dB, (VB @ RDN.T).max(0)], np.r_[(RDV @ N.T).max(0), np.full(12, r)], GR), NR), r=r)
print({k: len(v) for k, v in J.items() if isinstance(v, list)}, 'r', round(r, 4))
json.dump(J, open('data/scutoid-two-render.json', 'w'))
