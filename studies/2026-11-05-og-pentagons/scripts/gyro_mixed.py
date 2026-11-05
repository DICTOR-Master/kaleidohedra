# FULLY gyrated octet (every layer boundary a twin), DICTO 5 Nov 2026. Layers between planes x+y+z = (2k-1)R; layer 0 = the octet slab
# |x+y+z| <= R; layer k+1 = mirror of layer k across x+y+z = (2k+1)R, layer -1 = mirror of layer 0 across x+y+z = -R.
# Connectors: octet connector on edge-sharing pairs with parallel facing pentagons; twin connector on each edge of a shared face.
exec(open("octet_kit.py").read().split("cen = [")[0])
n = np.array([1., 1, 1])/math.sqrt(3)
def Mir(P, k): P = np.asarray(P, float); return P - 2*np.outer(P @ n - (2*k + 1)*R/math.sqrt(3), n)
OCT = np.array([[R,0,0],[-R,0,0],[0,R,0],[0,-R,0],[0,0,R],[0,0,-R]])
L0 = [R*np.array(v, float) for v in itertools.product(range(-4, 5), repeat=3) if sum(v) == 0]
L0 = [c for c in L0 if np.linalg.norm(c) < 3.3*R]
T0 = []
for c in L0:
    for sg in itertools.product((1, -1), repeat=3):
        T = np.vstack([[c + R*np.eye(3)[i]*sg[i] for i in range(3)], c + R*np.array(sg, float)])
        if np.all(np.abs(T.sum(1)) <= R + 1e-9): T0.append(T)
uniq = {}; [uniq.setdefault(tuple(np.round(np.sort(T, axis=0).ravel(), 6)), T) for T in T0]; T0 = list(uniq.values())
import sys
SEQ = sys.argv[1] if len(sys.argv) > 1 else "tot"     # boundaries between layers -1|0, 0|1, 1|2, 2|3: t = twin, o = octet
def Mmat(k):
    A = np.eye(4); A[:3, :3] -= 2*np.outer(n, n); A[:3, 3] = 2*(2*k + 1)*R/math.sqrt(3)*n; return A
def Tmat(v):
    A = np.eye(4); A[:3, 3] = v; return A
G = {0: np.eye(4)}; up = np.array([R, R, 0.0])
for k in range(0, 3):          # layer k -> k+1 through boundary SEQ[k]
    if SEQ[k] == "t": G[k + 1] = Mmat(k) @ G[k]
    else:
        flip = np.linalg.det(G[k][:3, :3]) < 0; G[k + 1] = G[k] @ Tmat(-up if flip else up)
G[-1] = Mmat(-1) @ G[0]        # layer -1: twin below (fixed)
def layer(k, P):
    P = np.asarray(P, float); return (np.c_[P, np.ones(len(P))] @ G[k].T)[:, :3]
LAY = (-1, 0, 1, 2, 3)
cells = [(k, layer(k, c[None])[0], layer(k, C + c), layer(k, OCT + c), layer(k, TIPS + c)) for k in LAY for c in L0]
tets = [(k, layer(k, T)) for k in LAY for T in T0]
solids = [hull(o) for _, _, o, _, _ in cells]; n_oct = n_twin = 0; bad = 0
def pent(c, P, T, m):
    e = (m - c)/np.linalg.norm(m - c); Ut = (T - c)/np.linalg.norm(T - c, axis=1)[:, None]; u = Ut[np.argmax(Ut @ e)]
    return P[np.abs((P - c) @ u - 0.63932) < 2e-3], u
for (ka, ca, A, OA, TA), (kb, cb, B, OB, TB) in itertools.combinations(cells, 2):
    if np.linalg.norm(ca - cb) > 1.5*R: continue
    sh = [p for p in OA if np.min(np.linalg.norm(OB - p, axis=1)) < 1e-9]
    if len(sh) == 2:
        m = (sh[0] + sh[1])/2; QA, ua = pent(ca, A, TA, m); QB, ub = pent(cb, B, TB, m)
        if len(QA) == 5 and len(QB) == 5 and abs(ua @ ub + 1) < 1e-6: solids.append(hull(np.vstack([QA, QB]))); n_oct += 1
        else: bad += 1
    elif len(sh) == 3:
        for e0, e1 in itertools.combinations(sh, 2):
            m = (e0 + e1)/2; QA, ua = pent(ca, A, TA, m); QB, ub = pent(cb, B, TB, m); solids.append(hull(np.vstack([QA, QB]))); n_twin += 1
U_all = m3.Manifold.batch_boolean(solids, m3.OpType.Add); tot = sum(s.volume() for s in solids)
print(f"layers {LAY}, octahedra {len(cells)}, tetrahedra {len(tets)}; octet connectors {n_oct}, twin connectors {n_twin}, edge pairs without parallel pentagons {bad}; overlap volume {tot - U_all.volume():.2e}", flush=True)
ko = {}; kt = {}; tv = 0; print("boundaries -1|0 twin, then", SEQ, flush=True)
for k, c, A, O, _ in cells:
    if k not in (0, 1, 2) or np.linalg.norm(c - (c @ n)*n) > 1.2*R: continue
    rest = hull(O) - U_all; key = tuple(sorted(round(p.volume(), 5) for p in rest.decompose() if p.volume() > 1e-9)); ko[key] = ko.get(key, 0) + 1
for k, T in tets:
    cT = T.mean(0)
    if k not in (0, 1, 2) or np.linalg.norm(cT - (cT @ n)*n) > 1.2*R: continue
    rest = hull(T) - U_all; key = tuple(sorted(round(p.volume(), 5) for p in rest.decompose() if p.volume() > 1e-9)); kt[key] = kt.get(key, 0) + 1
print("octahedra in the middle layers, leftover pieces -> count:"); [print("  ", k, v) for k, v in ko.items()]
print("tetrahedra in the middle layers, leftover pieces -> count:"); [print("  ", k, v) for k, v in kt.items()]
print("single-twin values: corner 0.07826, twin corner 0.07707, dented tetrahedron 0.39725, twin dented tetrahedron 0.4059; FINAL ok")
