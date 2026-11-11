# twin_vacuus.py, DICTO 11 Nov 2026 ("what would a vacuus form of the og look like" -> "do the twin vacuus"). Galois twin of the OG
# (sqrt5 -> -sqrt5 on the exact coordinates). Two readings: (i) TWIN HULL = convex hull of the 102 twin points (a convex icosahedral
# solid); (ii) STAR TWIN = the OG's own faces and edges carried to the twin points (coplanarity is preserved by the swap; faces may
# cross themselves). For each: the Vacuus (#87): one fin per edge from the centre O, apex angles, fin classes, fin planes (planes
# through O), flat sheets (coplanar fins joined along a strut), struts (centre -> corner) and their lengths; face shapes (convex,
# non-convex, self-crossing star). Controls: OG itself reproduces the census (180 fins, 45 fin planes, 120 sheets, 2 strut lengths).
# usage: python3 twin_vacuus.py <five-fold-octet dir> <out.json> <figure.png>
import sys, os, json, numpy as np
from collections import Counter
D, OUTJ, FIG = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
sys.path.insert(0, D); os.chdir(D); exec(open('exact_upward.py').read().split("def kinds(S)")[0])
from scipy.spatial import ConvexHull
S5 = 5 ** .5
real = np.array([[float(x.a) + float(x.b) * S5 for x in v] for v in OG])
twin = np.array([[float(x.a) - float(x.b) * S5 for x in v] for v in OG])
def hull_faces(P, tol=1e-9):
    h = ConvexHull(P); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    faces = []
    for pts in grp.values():
        idx = np.array(sorted(pts)); Q = P[idx]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T
        faces.append(list(idx[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]))
    return faces
def edges_of(faces):
    E = set()
    for f in faces:
        for a, b in zip(f, f[1:] + f[:1]): E.add((min(a, b), max(a, b)))
    return sorted(E)
def shape(P, cyc):
    Q = P[cyc]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T
    e = np.roll(q, -1, 0) - q; cr = e[:, 0] * np.roll(e, -1, 0)[:, 1] - e[:, 1] * np.roll(e, -1, 0)[:, 0]
    ang = np.arctan2(cr, (e * np.roll(e, -1, 0)).sum(1)); turn = round(abs(ang.sum()) / (2 * np.pi))
    if turn != 1: return 'star'
    return 'convex' if (cr > 1e-12).all() or (cr < -1e-12).all() else 'nonconvex'
def vacuus(P, faces, tag):
    E = edges_of(faces); fins = []
    for a, b in E:
        u, v = P[a], P[b]; apex = np.degrees(np.arccos(np.clip(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1)))
        n = np.cross(u, v); n = n / np.linalg.norm(n); n = n * np.sign(n[np.argmax(np.abs(n) > 1e-9)])
        fins.append(dict(a=a, b=b, apex=apex, n=n))
    cls = Counter(round(f['apex'], 4) for f in fins)
    planes = np.unique(np.round(np.array([f['n'] for f in fins]), 8), axis=0)
    # flat sheets: fins in the same plane sharing a strut (corner)
    par = list(range(len(fins)))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    by = {}
    for i, f in enumerate(fins):
        for c in (f['a'], f['b']): by.setdefault(c, []).append(i)
    for c, ids in by.items():
        for i in ids:
            for j in ids:
                if i < j and np.allclose(fins[i]['n'], fins[j]['n'], atol=1e-8): par[find(i)] = find(j)
    sheets = Counter(Counter(find(i) for i in range(len(fins))).values())
    struts = np.unique(np.round(np.linalg.norm(P[sorted({c for f in faces for c in f})], axis=1), 8))
    shapes = Counter((len(f), shape(P, f)) for f in faces)
    r = dict(tag=tag, corners=len({c for f in faces for c in f}), edges=len(E), faces=len(faces), face_types=dict(Counter(len(f) for f in faces)),
             face_shapes={f'{k[0]}-gon {k[1]}': v for k, v in shapes.items()}, fins=len(fins), fin_classes={str(k): v for k, v in sorted(cls.items())},
             fin_planes=len(planes), flat_sheets=sum(sheets.values()), sheet_sizes={str(k): v for k, v in sorted(sheets.items())},
             strut_lengths=len(struts), struts=[float(x) for x in struts])
    print(f"{tag}: corners {r['corners']}, edges {r['edges']}, faces {r['faces']} {r['face_types']} | shapes {r['face_shapes']}\n   VACUUS: {r['fins']} fins, apex angles (deg: count) {r['fin_classes']}, {r['fin_planes']} fin planes through O, {r['flat_sheets']} flat sheets {r['sheet_sizes']}, {r['strut_lengths']} strut lengths {[round(x, 6) for x in struts]}", flush=True)
    return r, fins
og_faces = hull_faces(real)
r0, f0 = vacuus(real, og_faces, 'OG (control: census 180 fins, 45 planes, 120 sheets, 2 strut lengths)')
ok = r0['fins'] == 180 and r0['fin_planes'] == 45 and r0['flat_sheets'] == 120 and r0['strut_lengths'] == 2
tw_faces = hull_faces(twin)
r1, f1 = vacuus(twin, tw_faces, '(i) TWIN HULL')
r2, f2 = vacuus(twin, og_faces, '(ii) STAR TWIN (OG faces on twin points)')
# coplanarity preserved?
plan = max(np.abs((twin[f] - twin[f].mean(0)) @ np.linalg.svd(twin[f] - twin[f].mean(0))[2][2]).max() for f in og_faces)
print(f'star twin faces flat (Galois keeps coplanarity): max off-plane {plan:.1e}', flush=True); ok &= plan < 1e-9
json.dump(dict(og=r0, twin_hull=r1, star_twin=r2), open(OUTJ, 'w'), indent=1)
# figure: three panels (OG Vacuus, twin hull Vacuus, star twin Vacuus): fins as translucent triangles, struts, outline
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(18, 6.4), facecolor='#14110e')
for i, (P, fins, faces, title) in enumerate(((real, f0, og_faces, 'OG Vacuus'), (twin, f1, tw_faces, '(i) twin hull Vacuus'), (twin, f2, og_faces, '(ii) star twin Vacuus'))):
    ax = fig.add_subplot(1, 3, i + 1, projection='3d', facecolor='#14110e'); ax.set_axis_off()
    tri = [[np.zeros(3), P[f['a']], P[f['b']]] for f in fins]
    ap = np.array([f['apex'] for f in fins]); levels = sorted(set(np.round(ap, 4)))
    cols = ['#9b6fe0', '#e3b341', '#4fb3a9', '#e06f6f', '#6fa0e0', '#c0c0c0']
    fc = [cols[levels.index(round(a, 4)) % len(cols)] for a in ap]
    pc = Poly3DCollection(tri, facecolors=fc, edgecolors='#f2ead8', linewidths=0.25, alpha=0.55); ax.add_collection3d(pc)
    for f in faces:
        q = P[f + [f[0]]]; ax.plot(q[:, 0], q[:, 1], q[:, 2], color='#f2ead8', lw=0.6)
    m = np.abs(P).max() * 1.05; ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 30)
    ax.set_title(title, color='#f2ead8', fontsize=14)
fig.text(0.99, 0.02, 'DICTO · dictospheres.com', color='#e3b341', ha='right', fontsize=10)
fig.text(0.01, 0.02, 'Fins from the centre to every edge, coloured by apex angle; outline = faces. Twin: sqrt5 -> -sqrt5. DICTO 2026', color='#bdb3a0', fontsize=10)
plt.savefig(FIG, dpi=110, facecolor=fig.get_facecolor(), bbox_inches='tight')
print('FINAL ok' if ok else 'FINAL FAIL: OG control or twin coplanarity')
