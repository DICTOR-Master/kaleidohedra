# DICTO 2026-10-18 octet study -- STEP 12 (stage 2): every face of every piece, exactly, and which are golden / Penrose shapes.
# The step-10 meshes give the faces (coplanar triangles merged into boundary loops). Each face is matched to its exact source plane
# (OCD kite/hexagon, key, star hull, octahedron, cap cut, tetrahedron) and every corner is snapped to the exact meeting point of 3 such
# planes (checked exactly). Then exact squared edge lengths and exact cos^2 of the corner angles name the shapes:
# golden rhombus (cos^2 = 1/5, 63.43/116.57), Penrose thick (72/108) and thin (36/144) angles, regular-polygon angles.
# -> data/step12-faces.json
import itertools, math, numpy as np
from collections import defaultdict
from exactpoly import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json'); mesh = load('step10-meshes.json')
V = [[q(x) for x in v] for v in S1['V']]; R = q(S1['R']); L = [[q(x) for x in v] for v in S2['lattice']]
PO = planes_of(V); KP = {k: planes_of([[q(x) for x in p] for p in K]) for k, K in S5['keys'].items()}
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
def sgnv(c): return [R if sgn(x) > 0 else (qn(R) if sgn(x) < 0 else Z) for x in c]
HP = []
for i in five:
    o = sgnv(V[i]); star = [V[j] for j in sorted({j for f in S1['faces'] if i in f for j in f})]
    HP.append((o, planes_of(star + [vsub(o, p) for p in star])))
octa = [[R if (i == j and s > 0) else (qn(R) if i == j else Z) for j in range(3)] for i in range(3) for s in (1, -1)]; POC = planes_of(octa)
TP = planes_of([[q(x) for x in v] for v in S2['Tplus']])
cut = [([qn(ONE) if k == a else (ONE if k == 2 else Z) for k in range(3)], Z) for a in (0, 1)] + [([ONE if k == a else (ONE if k == 2 else Z) for k in range(3)], Z) for a in (0, 1)]
cut = [([qn(x) for x in n], d) for n, d in cut]   # z >= |x|, |y|  as  -z + x <= 0 etc: n.x <= 0 with n = (+-1 on x or y, -1 on z)
cut = [([ONE if k == a else (qn(ONE) if k == 2 else Z) for k in range(3)], Z) for a in (0, 1)] + [([qn(ONE) if k == a else (qn(ONE) if k == 2 else Z) for k in range(3)], Z) for a in (0, 1)]
cat = []                                              # (label, n, d)
centres = [[Z, Z, Z]] + [[sum((qm(L[t][k], qr(c[t])) for t in range(3)), Z) if False else qa(qa(qm(L[0][k], qr(c[0])), qm(L[1][k], qr(c[1]))), qm(L[2][k], qr(c[2]))) for k in range(3)]
                          for c in itertools.product((-1, 0, 1), repeat=3) if c != (0, 0, 0)]
for c in centres:
    cat += [('OCD face', n, d) for n, d in shift(PO, c)]
    for k, P in KP.items(): cat += [('key face', n, d) for n, d in shift(P, c)]
    for o, P in HP: cat += [('star-hull face', n, d) for n, d in shift(P, c)]
    cat += [('octahedron face', n, d) for n, d in shift(POC, c)]
cat += [('cap cut plane', n, d) for n, d in cut] + [('tetrahedron face', n, d) for n, d in TP]
cf = [(lab, np.array([qf(x) for x in n]), qf(d)) for lab, n, d in cat]
def on_planes(p, tol=5e-5): return [i for i, (lab, nf, df) in enumerate(cf) if abs(nf @ p - df) < tol * np.linalg.norm(nf)]
NAMED = [('golden 63.43', (Fr(1, 5), Fr(0)), 1), ('golden 116.57', (Fr(1, 5), Fr(0)), -1), ('Penrose 36', (Fr(3, 8), Fr(1, 8)), 1), ('Penrose 144', (Fr(3, 8), Fr(1, 8)), -1),
         ('Penrose 72', (Fr(3, 8), Fr(-1, 8)), 1), ('Penrose 108', (Fr(3, 8), Fr(-1, 8)), -1), ('90', Z, 0), ('60', (Fr(1, 4), Fr(0)), 1), ('120', (Fr(1, 4), Fr(0)), -1)]
def angle_name(u, w):
    uw = dot(u, w); c2 = qd(qm(uw, uw), qm(dot(u, u), dot(w, w))); s = sgn(uw)
    for nm, val, sg in NAMED:
        if c2 == val and s == sg: return nm
    cf_ = qf(uw) / math.sqrt(qf(dot(u, u)) * qf(dot(w, w))); return f'{math.degrees(math.acos(max(-1, min(1, cf_)))):.2f}'
srcs = {}
def faces_of(pm):
    Vm = np.array(pm['v']); T = np.array(pm['t']); groups = defaultdict(list)
    for t in T:
        a, b, c = Vm[t]; n = np.cross(b - a, c - a); A = np.linalg.norm(n)
        if A < 1e-12: continue
        n /= A; key = None
        for i, (lab, nf, df) in enumerate(cf):
            nn = np.linalg.norm(nf)
            if abs(nf @ n) / nn > 0.999 and all(abs(nf @ x - df) < 3e-5 * nn for x in (a, b, c)):
                if key is None: key = i
                srcs.setdefault(key, set()).add(lab)
        groups[key].append(t)
    return Vm, groups
snap_cache = {}
def snap(p):
    k = tuple(np.round(p, 5))
    if k in snap_cache: return snap_cache[k]
    act = on_planes(p); x = None
    for i, j, l in itertools.combinations(act, 3):
        x = solve3([cat[i][1], cat[j][1], cat[l][1]], [cat[i][2], cat[j][2], cat[l][2]])
        if x is not None and np.allclose([qf(y) for y in x], p, atol=1e-4): break
        x = None
    snap_cache[k] = x; return x
report = {}
for piece in ('keyed_OCD', 'middle', 'cap', 'tet_notched'):
    Vm, groups = faces_of(mesh[piece]); faces = []
    for pid, tris in groups.items():
        ec = defaultdict(int)
        for t in tris:
            for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): ec[(min(a, b), max(a, b))] += 1
        bnd = [e for e, c in ec.items() if c == 1]
        area = sum(np.linalg.norm(np.cross(Vm[t[1]] - Vm[t[0]], Vm[t[2]] - Vm[t[0]])) / 2 for t in tris)
        if area < 1e-9: continue
        # boundary loops (merge vertices at the same position)
        pos = {}; idmap = {}
        for e in bnd:
            for v in e:
                k = tuple(np.round(Vm[v], 5)); idmap[v] = pos.setdefault(k, len(pos))
        adj = defaultdict(list)
        for a, b in bnd: adj[idmap[a]].append(idmap[b]); adj[idmap[b]].append(idmap[a])
        P = {i: np.array(k) for k, i in pos.items()}; seen = set(); loops = []
        for s in adj:
            if s in seen: continue
            loop = [s]; seen.add(s); prev, cur = None, s
            while True:
                nx = [v for v in adj[cur] if v != prev and (v not in seen or (v == s and len(loop) > 2))]
                if not nx: break
                if nx[0] == s: break
                prev, cur = cur, nx[0]; loop.append(cur); seen.add(cur)
            loops.append(loop)
        for loop in loops:
            X = [snap(P[i]) for i in loop]
            if any(x is None for x in X): faces.append(dict(source=' = '.join(sorted(srcs.get(pid, {'?'}))), corners=len(loop), exact=False, area=area)); continue
            # drop straight-through corners (exactly collinear)
            keep = True
            while keep:
                keep = False
                for i in range(len(X)):
                    a, b, c = X[i - 1], X[i], X[(i + 1) % len(X)]
                    if all(x == Z for x in cross(vsub(b, a), vsub(c, b))): X.pop(i); keep = True; break
            e2 = [dot(vsub(X[(i + 1) % len(X)], X[i]), vsub(X[(i + 1) % len(X)], X[i])) for i in range(len(X))]
            angs = [angle_name(vsub(X[i - 1], X[i]), vsub(X[(i + 1) % len(X)], X[i])) for i in range(len(X))]
            eq_edges = len({qs_(e) for e in e2}) == 1
            name = f'{len(X)}-gon'
            if len(X) == 4 and eq_edges and sorted(angs) == sorted(['golden 63.43', 'golden 116.57'] * 2): name = 'GOLDEN RHOMBUS'
            elif len(X) == 4 and eq_edges and sorted(angs) == sorted(['Penrose 72', 'Penrose 108'] * 2): name = 'PENROSE THICK RHOMBUS'
            elif len(X) == 4 and eq_edges and sorted(angs) == sorted(['Penrose 36', 'Penrose 144'] * 2): name = 'PENROSE THIN RHOMBUS'
            elif len(X) == 3 and eq_edges: name = 'equilateral triangle'
            elif any(a.startswith('golden') or a.startswith('Penrose') for a in angs): name += ' with golden/Penrose angles'
            faces.append(dict(source=' = '.join(sorted(srcs.get(pid, {'?'}))), name=name, corners=len(X), angles=angs, edges2=[qs_(e) for e in e2],
                              edges=[round(qf(e) ** .5, 6) for e in e2], area=round(float(area), 6), exact=True))
    report[piece] = faces
    from collections import Counter
    print(f'\n== {piece}: {len(faces)} faces'); print(Counter((f['source'], f.get('name', '?')) for f in faces))
save('step12-faces.json', dict(mark=MARK, step=12, pieces=report))
