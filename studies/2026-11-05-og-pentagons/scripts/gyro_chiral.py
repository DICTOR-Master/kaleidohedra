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
def layer(k, P):           # carry layer-0 points into layer k by successive mirrors
    if k == 0: return P
    if k > 0: return layer(k - 1, Mir(P, k - 1)) if False else Mir(layer(k - 1, P), k - 1)
    return Mir(layer(k + 1, P), k)
LAY = (-1, 0, 1, 2)
cells = [(k, layer(k, c[None])[0], layer(k, C + c), layer(k, OCT + c), layer(k, TIPS + c)) for k in LAY for c in L0]
tets = [(k, layer(k, T)) for k in LAY for T in T0]
TW = []; solids = [hull(o) for _, _, o, _, _ in cells]; n_oct = n_twin = 0; bad = 0
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
            m = (e0 + e1)/2; QA, ua = pent(ca, A, TA, m); QB, ub = pent(cb, B, TB, m); solids.append(hull(np.vstack([QA, QB]))); TW.append(solids[-1]); n_twin += 1
U_all = m3.Manifold.batch_boolean(solids, m3.OpType.Add); tot = sum(s.volume() for s in solids)
print(f"layers {LAY}, octahedra {len(cells)}, tetrahedra {len(tets)}; octet connectors {n_oct}, twin connectors {n_twin}, edge pairs without parallel pentagons {bad}; overlap volume {tot - U_all.volume():.2e}", flush=True)

exec(open("octet_kit3.py").read().split("def same_shape")[0].split("exec(")[0]) if False else None
import itertools
def pts(M):      # true corners only: drop vertices lying on a flat face or a straight edge (boolean mesh artefacts)
    m = M.to_mesh(); V = np.array(m.vert_properties)[:, :3]; Tr = np.array(m.tri_verts); NS = {}
    for t in Tr:
        a, b, c = V[t]; nn = np.cross(b - a, c - a); L = np.linalg.norm(nn)
        if L < 1e-12: continue
        for i in t: NS.setdefault(i, []).append(nn/L)
    keep = [i for i, N in NS.items() if np.linalg.svd(np.array(N), compute_uv=False)[-1] > 1e-3] if True else []
    keep = [i for i in keep if len(NS[i]) >= 3]
    return np.unique(np.round(V[keep], 9), axis=0)
SRC = open("octet_kit3.py").read(); exec(("def same_shape" + SRC.split("def same_shape")[1].split("O0 = ")[0]).replace("> 1e-9: return None","> 1e-6: return None").replace("atol=1e-6","atol=1e-4").replace("< 1e-5","< 1e-4"))
mirror = lambda M: M.transform(np.array([[-1.,0,0,0],[0,1,0,0],[0,0,1,0]]))
TC, TT = [], []
for k, c, A, O, _ in cells:
    if k in (0, 1) and np.linalg.norm(c - (c @ n)*n) < 1.2*R:
        TC += [p for p in (hull(O) - U_all).decompose() if abs(p.volume() - 0.07707) < 1e-4]
for k, T in tets:
    cT = T.mean(0)
    if k in (0, 1) and np.linalg.norm(cT - (cT @ n)*n) < 1.2*R:
        TT += [p for p in (hull(T) - U_all).decompose() if p.volume() > 1e-9]
for name, L in (("twin connector", TW[:40]), ("twin corner piece", TC), ("twin dented tetrahedron", TT)):
    cls = []
    for X in L:
        for c in cls:
            if same_shape(c[0], X, "rotation"): c.append(X); break
        else: cls.append([X])
    ref = L[0]; kinds = [ (len(c), round(c[0].volume(),6), len(pts(c[0])), same_shape(cls[0][0], c[0])) for c in cls]
    self_m = same_shape(ref, mirror(ref), "rotation")
    print(f"{name}: n={len(L)} vol={ref.volume():.6f} corners={len(pts(ref))}; vs first: {kinds}; mirror image by rotation: {self_m}", flush=True)
print("FINAL ok")
