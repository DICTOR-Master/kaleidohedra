# DICTO 2026-10-20 gyrated octet: meshes (manifold3d, float from the exact data) + 3D page for the companion paper's figures.
# usage (dicto-node): ~/plotenv/bin/python3 gyr_page.py  ->  renders/gyrated-octet.html
import os, json, itertools, math, numpy as np, manifold3d as m3
H = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(H, 'renders'), exist_ok=True)
D = json.load(open(os.path.join(H, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
V = np.array([[fq(c) for c in v] for v in D['V']]); R = fq(D['R'])
n1 = np.ones(3) / math.sqrt(3)
def mir(P, level=R): P = np.asarray(P, float); return P - 2 * ((P @ n1 - level / math.sqrt(3))[..., None]) * n1
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def reflect(mf, level=R):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)[:, ::-1]
    return m3.Manifold(m3.Mesh(vert_properties=np.ascontiguousarray(mir(P, level), dtype=np.float32), tri_verts=np.ascontiguousarray(T, dtype=np.uint32)))
OCT = np.array([[s * R if i == j else 0 for j in range(3)] for i in range(3) for s in (1, -1)])
OG = hull(V); octa = hull(OCT)
face = np.array([[R, 0, 0], [0, R, 0], [0, 0, R]])
capL = hull(np.vstack([face, [[0, 0, 0]]])) - OG
twin_cap = capL + reflect(capL)
# a lower-layer tetrahedron with a face on the twin plane x+y+z = R (vertices of the octet: R(i,j,k), i+j+k odd)
pts = [np.array(c) * R for c in itertools.product(range(-2, 3), repeat=3) if sum(c) % 2]
e2 = 2 * R * R; T = None
for a, b, c in itertools.combinations([p for p in pts if abs(p.sum() - R) < 1e-9 and np.linalg.norm(p) < 2.1 * R], 3):
    if all(abs(np.dot(x - y, x - y) - e2) < 1e-9 for x, y in ((a, b), (b, c), (a, c))):
        for d in pts:
            if abs(d.sum() + R) < 1e-9 and all(abs(np.dot(d - x, d - x) - e2) < 1e-9 for x in (a, b, c)):
                T = np.array([a, b, c, d]); break
    if T is not None: break
tet = hull(T); bip = tet + reflect(tet)
ST = np.array(json.load(open(os.path.join(H, 'stella-37frame.json')))['V']); stella = hull(ST)
DB = np.array([[fq(c) for c in v] for v in json.load(open(os.path.join(H, 'dbt-exact.json')))['V']]); dbt = hull(DB)
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
i1 = [i for i in five if V[i, 0] > 1e-9 and V[i, 1] > 1e-9 and abs(V[i, 2]) < 1e-9][0]
star = V[sorted({j for f in D['faces'] if i1 in f for j in f})]
Mg = hull(np.vstack([star, mir(star)])) - OG - reflect(OG)
def mesh(mf, colour, **kw):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); c = P.mean(0)
    return dict(v=np.round(P - c, 5).tolist(), t=np.asarray(me.tri_verts).tolist(), colour=colour, **kw), c.tolist()
pieces, home = {}, {}
for k, mf, col, kw in [('og', OG, '#d9a521', {}), ('ogT', reflect(OG), '#5b8fd0', {}), ('oct', octa, '#9aa7b8', dict(glass=True)), ('octT', reflect(octa), '#9aa7b8', dict(glass=True)),
                       ('cap', capL, '#3f9a5b', dict(colour2='#2a9d9a')), ('tcap', twin_cap, '#8e5bd0', {}), ('tet', tet, '#c8382f', {}), ('bip', bip, '#e07b39', {}),
                       ('st', stella, '#e8c33a', {}), ('stT', reflect(stella), '#6aa5e0', {}), ('dbt', dbt, '#d9a521', dict(glass=True)), ('dbtT', reflect(dbt), '#5b8fd0', dict(glass=True)),
                       ('mg', Mg, '#c8382f', {})]:
    pieces[k], home[k] = mesh(mf, col, **kw)
at = lambda k, off=(0, 0, 0), flip=False: [k, flip, (np.array(home[k]) * (-1 if flip else 1) + np.array(off)).tolist()]
t2 = 2 * R / 3 * np.ones(3)
# a gyrated stack: layer 0 = octet octahedra with centres R(i,j,k), i+j+k = 0; the next layer up is its mirror image in x+y+z = R
lay0 = [np.array(c) * R for c in itertools.product(range(-2, 3), repeat=3) if sum(c) == 0 and np.linalg.norm(np.array(c)) <= 1.5]
lay_m1 = [['ogT', False, (mir(np.array(home['og']) + c, -R)).tolist()] for c in lay0]
Vd = np.array([1, -1, 0.9]); Vd /= np.linalg.norm(Vd); U = np.cross([0, 1, 0], Vd); U /= np.linalg.norm(U); W = np.cross(Vd, U)  # screen right and up (camera up = y)
ax = np.cross(n1, Vd); sa = np.linalg.norm(ax); ca = n1 @ Vd; K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]) / sa
ROT = np.eye(3) + sa * K + (1 - ca) * K @ K   # turns the caps' face normal (1,1,1) towards the camera (display only)
views = {
  'twin': dict(label='Twin OGs', text='the OG (gold) and its twin across a shared octahedron face (blue): the twin is the OG turned 60°', radius=1.25, target=(t2 / 2).tolist(), dir=[1, -1, 0.35],
               place=[at('og'), ['ogT', False, home['ogT']], at('oct'), ['octT', False, home['octT']]]),
  'stack': dict(label='Gyrated stack', text='OGs in three layers of the gyrated octet (A B A): each layer is the mirror image of the one before', radius=2.4, target=(t2 / 2).tolist(), dir=[1, -1, 0.5],
                place=[at('og', c) for c in lay0] + [['ogT', False, (np.array(home['ogT']) + c).tolist()] for c in lay0] + lay_m1),
  'kit': dict(label='Cell kit', text='OG · left cap (green) and right cap (teal) · twin cap (violet) · tetrahedron (red) · bipyramid (orange)', radius=1.5, dir=[1, -1, 0.9],
              place=[[k, fl, (a * U + b * W).tolist()] + ([ROT.ravel().tolist()] if k in ('cap', 'tcap') else []) for k, fl, a, b in [('og', False, -1.45, 0.55), ('cap', False, -0.45, 0.7), ('cap', True, 0.45, 0.7), ('tcap', False, 1.45, 0.6), ('tet', False, -0.7, -0.8), ('bip', False, 0.7, -0.8)]]),
  'stella': dict(label='Twin OCD Stellas', text='the OCD Stella (gold) and its twin (blue) meeting on the whole joint triangle', radius=1.3, target=(t2 / 2).tolist(), dir=[1, -1, 0.35],
                 place=[at('st'), ['stT', False, home['stT']], at('oct'), ['octT', False, home['octT']]]),
  'dbt': dict(label='Twin DBTs', text='DICTO Belted Triacontahedra pole to pole across a twin plane, each holding its OG', radius=1.3, target=(t2 / 2).tolist(), dir=[1, -1, 0.35],
              place=[at('dbt'), ['dbtT', False, home['dbtT']], at('og'), ['ogT', False, home['ogT']]]),
  'mg': dict(label='Mirror middle piece', text='the mirror middle piece (red) between an OG and its twin at an edge of the twin plane', radius=0.9, target=home['mg'], dir=[1, 1, -2.2],
             place=[['mg', False, home['mg']], at('og'), ['ogT', False, home['ogT']]]),
}
facts = ['All numbers are exact in Q(√5) (gyr_exact.py, stella_twin_exact.py, dbt_exact.py, twin.py, kit.py); the meshes here are float copies.']
tpl = open(os.path.join(H, 'gyr_viewer_template.html')).read()
for k, v in {'__TITLE__': 'The OG on the Gyrated Octet', '__SUB__': 'Twins, the cell kit, OCD Stellas, DICTO Belted Triacontahedra and the mirror middle piece (DICTO 2026-10-20). Drag to turn.',
             '__MARK__': 'studies/2026-10-19-og-gyrated-octet', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=pieces, views=views), separators=(',', ':'))}.items(): tpl = tpl.replace(k, v)
open(os.path.join(H, 'renders', 'gyrated-octet.html'), 'w').write(tpl)
print('ok', len(tpl), {k: round(m.volume(), 6) for k, m in [('og', OG), ('cap', capL), ('tcap', twin_cap), ('tet', tet), ('bip', bip), ('stella', stella), ('dbt', dbt), ('mg', Mg)]})
