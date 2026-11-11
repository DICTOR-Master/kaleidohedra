# Referee's independent census: every hexagonal face of every dataset solid, symmetry group of the hexagon (as a planar polygon),
# truncated-triangle test, exact ratio; plus cutting depths for the six solids of Section 7.
import glob, json, os, itertools, numpy as np, sympy as sp
DS = os.path.expanduser('~/work/dataset-v7/solids')
g = (1+5**.5)/2
def hex_sym(P):
    # symmetry of planar hexagon P (6x3, cyclic order): count isometries of the plane mapping the vertex cycle to itself
    c = P.mean(0); Q = P - c
    n = np.cross(Q[1]-Q[0], Q[2]-Q[0]); n /= np.linalg.norm(n)
    e1 = Q[0]/np.linalg.norm(Q[0]); e2 = np.cross(n, e1); X = np.stack([Q@e1, Q@e2], 1)
    D = np.linalg.norm(X[:,None]-X[None], axis=2)
    syms = 0; rot3 = False; mirror=False
    for k in range(6):
        for s in (1,-1):
            perm = [(s*i + k) % 6 for i in range(6)]
            if np.allclose(D[np.ix_(perm,perm)], D, atol=1e-9):
                syms += 1
                if s == 1 and k in (2,4): rot3 = True
                if s == -1: mirror = True
    return syms, rot3, mirror
def is_tt(P):
    L = np.linalg.norm(np.roll(P,-1,0)-P, axis=1)
    ang = [np.degrees(np.arccos(np.dot(P[i-1]-P[i], P[(i+1)%6]-P[i])/(L[i-1]*L[i]))) for i in range(6)]
    return all(abs(a-120)<1e-7 for a in ang) and all(abs(L[i]-L[(i+2)%6])<1e-9 for i in range(6))
rows = {}
for f in sorted(glob.glob(DS+'/*.json')):
    d = json.load(open(f)); V = np.array([[float(c) for c in v['decimal']] for v in d['vertices']])
    cnt = {}
    for fc in d['faces']:
        if len(fc)!=6: continue
        P = V[fc]; syms, r3, mir = hex_sym(P); tt = is_tt(P)
        L = np.linalg.norm(np.roll(P,-1,0)-P, axis=1); ratio = L.max()/L.min()
        key = (syms, r3, mir, tt, round(ratio,6)); cnt[key] = cnt.get(key,0)+1
    if cnt: rows[d['name']] = cnt
for k,v in rows.items(): print(k, v)
print('total solids', len(glob.glob(DS+'/*.json')))
# exact ratios for the nine
print('--- exact ratios')
for fn in ['dicto-icosaxes-hexa','dicto-white-knight','dicto-icosaxes','dicto-unborn-axes','dicto-ti-star-core','dicto-gti','dicto-golden-clasp','dicto-haigha','dicto-hatta']:
    d = json.load(open(f'{DS}/{fn}.json')); V = [sp.Matrix([sp.sympify(c) for c in v['exact']]) for v in d['vertices']]
    Vd = np.array([[float(c) for c in v['decimal']] for v in d['vertices']]); seen=set()
    for fc in d['faces']:
        if len(fc)!=6 or not is_tt(Vd[fc]): continue
        P=[V[i] for i in fc]; L2=[sp.expand((P[(i+1)%6]-P[i]).dot(P[(i+1)%6]-P[i])) for i in range(6)]
        a2,b2 = sorted(L2[:2], key=lambda e: float(e)); r2 = sp.radsimp(sp.simplify(b2/a2)); r = sp.sqrt(r2)
        r = sp.radsimp(sp.sqrtdenest(sp.simplify(r))); seen.add(str(sp.nsimplify(r)))
    print(fn, d['f_vector'], d['faces_by_sides'], d['symmetry']['schoenflies'], 'ratios', seen)
# cutting depths numerically
print('--- depths (squared ratio of plane distances by face size)')
for fn in ['dicto-gti','dicto-ti-star-core','dicto-icosaxes','dicto-unborn-axes','dicto-white-knight','dicto-golden-clasp']:
    d = json.load(open(f'{DS}/{fn}.json')); V = np.array([[float(c) for c in v['decimal']] for v in d['vertices']]); V -= V.mean(0)
    dist = {}
    for fc in d['faces']:
        P=V[fc]; n=np.cross(P[1]-P[0],P[2]-P[0]); n/=np.linalg.norm(n); dist.setdefault(len(fc),set()).add(round(abs(n@P[0]),9))
    print(fn, {k:sorted(v) for k,v in dist.items()}, {(a,b): round((list(dist[a])[0]/list(dist[b])[0])**2,6) for a,b in itertools.combinations(sorted(dist),2)})
print('targets: 3/phi^2', 3/g**2, '3phi^2/5', 3*g**2/5, 'phi sqrt5/3', g*5**.5/3, '(195+66r5)/361', (195+66*5**.5)/361, '13/3-22r5/15', 13/3-22*5**.5/15)
