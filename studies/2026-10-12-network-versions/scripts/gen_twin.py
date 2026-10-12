# Data for the 3D page's Twin network tab (2026-10-12): the inner half (I(1/phi) to D(1)) and the outer half (D(1) to I(phi^2)),
# each as the Lotus seed's pieces or the twin network's, all in the Lotus frame (dodecahedron edge 1). Checks the volumes of all four.
import json, itertools, sys, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
SW = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])          # network frame -> Lotus frame (swap y, z)
def F(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
def edges(V, d=None):
    d = d or min(np.linalg.norm(V[0] - w) for w in V[1:]); return [(a, b) for a, b in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[a] - V[b]) - d) < 1e-9]
net_in, net_out = [], []
Ic = ref['I'] / PHI; ID = ref['ID'] * PHI / 2; D = ref['D']; TI = ref['TI'] / PHI; RT = ref['RT'] * np.sqrt(45 - 18 * np.sqrt(5)) / 2; I2 = ref['I'] * PHI ** 2
FID, FIc, FD, FT, FR, FI = F(ID), F(Ic), F(D), F(TI), F(RT), F(I2)
net_in.append(('core', Ic))
for f in FID:
    on = ID[np.abs(ID @ f[:3] + f[3]) < 1e-9]; n = f[:3] / np.linalg.norm(f[:3])
    if len(on) == 5: net_in.append(('npyr5', np.vstack([on, Ic[np.argmax(Ic @ n)]])))
    else:
        g = FIc[np.argmax(FIc[:, :3] @ n)]; net_in.append(('nfru3', np.vstack([on, Ic[np.abs(Ic @ g[:3] + g[3]) < 1e-9]])))
ED = edges(D, 1.0)
for k in range(20): net_in.append(('npyr3', np.vstack([D[k]] + [(D[a] + D[b]) / 2 for a, b in ED if k in (a, b)])))
for f in FT:
    on = TI[np.abs(TI @ f[:3] + f[3]) < 1e-9]; n = f[:3] / np.linalg.norm(f[:3])
    if len(on) == 5:
        g = FD[np.argmax(FD[:, :3] @ n)]; net_out.append(('nfru5', np.vstack([on, D[np.abs(D @ g[:3] + g[3]) < 1e-9]])))
ET = edges(TI); hexT = [f for f in FT if np.sum(np.abs(TI @ f[:3] + f[3]) < 1e-9) == 6]; penT = [f for f in FT if np.sum(np.abs(TI @ f[:3] + f[3]) < 1e-9) == 5]
onf = lambda x, f: abs(x @ f[:3] + f[3]) < 1e-9
for a, b in ED:
    ha = [f for f in hexT if onf(D[a], f)][0]; hb = [f for f in hexT if onf(D[b], f)][0]
    p, q = [(p, q) for p, q in ET if all(onf(TI[x], h) for x in (p, q) for h in (ha, hb))][0]
    net_out.append(('nt1', np.vstack([D[a], D[b], TI[p], TI[q]])))
apexR = lambda f: RT[np.argmax(RT @ (f[:3] / np.linalg.norm(f[:3])))]
for f in FT:
    on = TI[np.abs(TI @ f[:3] + f[3]) < 1e-9]; net_out.append(('ncap', np.vstack([on, apexR(f)])))
for a, b in ET:
    ps = [f for f in penT if onf(TI[a], f) and onf(TI[b], f)]; hs = [f for f in hexT if onf(TI[a], f) and onf(TI[b], f)]
    if len(ps) == 1 and len(hs) == 1: net_out.append(('nwedge', np.vstack([TI[a], TI[b], apexR(ps[0]), apexR(hs[0])])))
EI = edges(I2)
for f in FR:
    n = f[:3] / np.linalg.norm(f[:3]); rh = RT[np.abs(RT @ f[:3] + f[3]) < 1e-9]
    a, b = max(EI, key=lambda e: (I2[e[0]] + I2[e[1]]) @ n); net_out.append(('nedge', np.vstack([rh, I2[a], I2[b]])))
for f in FI:
    n = f[:3] / np.linalg.norm(f[:3]); tri = I2[np.abs(I2 @ f[:3] + f[3]) < 1e-9]; net_out.append(('nface', np.vstack([tri, RT[np.argmax(RT @ n)]])))
net_in = [(r, V @ SW.T) for r, V in net_in]; net_out = [(r, V @ SW.T) for r, V in net_out]
# Lotus halves from the Lotus seed's own pieces
L = json.load(open(sys.argv[1]))[:113]
st = json.load(open(sys.argv[2]))
Dl = np.array(st['dodecahedron']); FDl = F(Dl)
ins = lambda V: np.all(np.array(V) @ FDl[:, :3].T + FDl[:, 3] <= 1e-5)
lot_in = [('core', np.array(p['v'])) for p in st['pieces'] if p['r'] == 'ico'] + [('lcap', np.array(p['v'])) for p in st['pieces'] if p['r'] == 'cap'] + \
         [('l' + p['r'], np.array(p['v'])) for p in st['pieces'] if p['r'] in ('axe', 'cleo')]
lot_out = []
for p in L:
    V = np.array(p['vertices'])
    if p['role'] == 'ico':
        if ConvexHull(V).volume < 1: continue
        keep = V[~np.array([np.min(np.linalg.norm(np.array([c[0] for c in [x['v'] for x in st['pieces'] if x['r'] == 'cap']]) - v, axis=1)) < 1e-4 for v in V])]
        lot_out.append(('lj11', keep))
    elif p['role'] in ('axe', 'fuji') and not ins(V): lot_out.append(('l' + p['role'], V))
# frame check: the network's D must coincide with the Lotus seed's D(1)
Dn = D @ SW.T
print('network D = Lotus D(1):', all(np.min(np.linalg.norm(Dl - d, axis=1)) < 1e-4 for d in Dn))
vol = lambda P: sum(ConvexHull(V).volume for _, V in P)
vD, vI2 = ConvexHull(Dl).volume, ConvexHull(I2).volume
for nm, P in (('Lotus inner', lot_in), ('network inner', net_in)): print(f'{nm}: {len(P)} pieces, volume {vol(P):.6f} vs D(1) {vD:.6f}')
for nm, P in (('Lotus outer', lot_out), ('network outer', net_out)): print(f'{nm}: {len(P)} pieces, volume {vol(P):.6f} vs I(phi^2) - D(1) {vI2 - vD:.6f}')
def poly(V):
    V = np.array(V); H = ConvexHull(V); tris = H.simplices.tolist(); eq = H.equations
    from collections import defaultdict
    adj = defaultdict(list)
    for t, (a, b, c) in enumerate(tris):
        for e in ((a, b), (b, c), (a, c)): adj[tuple(sorted(e))].append(t)
    ed = [list(e) for e, ts in adj.items() if len(ts) == 2 and np.linalg.norm(eq[ts[0], :3] - eq[ts[1], :3]) > 1e-4]
    return [[round(x, 5) for x in v] for v in V.tolist()], tris, ed
out = {k: [[r, *poly(V)] for r, V in P] for k, P in (('twLi', lot_in), ('twNi', net_in), ('twLo', lot_out), ('twNo', net_out))}
json.dump(out, open(sys.argv[3], 'w'), separators=(',', ':'))
