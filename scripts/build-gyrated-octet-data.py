# Builds src/app/gyrated-octet-data.js for the "Octet ↔ gyrated" family of the world "The OG on the Octet Truss" (DICTO 2026-10-20;
# paper #37a, DICTO DOI 10.5281/zenodo.23484012). Pieces are float copies of the exact solids of the research study
# studies/2026-10-19-og-gyrated-octet: the OG (step1-ocd-exact.json), the OCD Stella turned into the #37 frame (stella-37frame.json),
# the DICTO Belted Triacontahedron (dbt-exact.json); caps, twin cap and bipyramid are cut here with manifold3d.
# Each kit: its set (one of each piece), its twin pair across x+y+z = R, and the pieces of one cell of layer 0 (octahedra centred on
# R(a,b,c), a+b+c = 0, repeated by R(1,-1,0) and R(0,1,-1)) together with that cell mirrored in x+y+z = R (layer 1 of the gyrated octet;
# a mirrored left cap is a right cap). The world stacks layers: octet = layer 0 moved by R(1,1,0) per layer; gyrated = layers 0 and 1
# alternating, moved by (4R/3)(1,1,1) per two layers.
# Usage (dicto-node, manifold3d): python3 scripts/build-gyrated-octet-data.py <study folder> [out]
import sys, os, json, math, itertools, numpy as np, manifold3d as m3
STUDY = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else 'src/app/gyrated-octet-data.js'
OCTET = os.path.join(STUDY, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')
fq = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
D = json.load(open(OCTET)); V = np.array([[fq(c) for c in v] for v in D['V']]); R = fq(D['R'])
ST = np.array(json.load(open(os.path.join(STUDY, 'stella-37frame.json')))['V'])
DB = np.array([[fq(c) for c in v] for v in json.load(open(os.path.join(STUDY, 'dbt-exact.json')))['V']])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
J = np.ones((3, 3)); MIR = np.eye(3) - 2 / 3 * J; MT = 2 * R / 3 * np.ones(3)          # mirror in x+y+z = R: x -> MIR x + MT
def mesh(mf):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
    return P, T
OG = hull(V); face = np.array([[R, 0, 0], [0, R, 0], [0, 0, R]])
capL = hull(np.vstack([face, [[0, 0, 0]]])) - OG
def mirrored(mf):
    P, T = mesh(mf); P = P @ MIR.T + MT
    return m3.Manifold(m3.Mesh(vert_properties=np.ascontiguousarray(P, dtype=np.float32), tri_verts=np.ascontiguousarray(T[:, ::-1], dtype=np.uint32)))
twin = capL + mirrored(capL)
pts = [np.array(c) * R for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2]
e2 = 2 * R * R
def tets_in_slab():   # regular tetrahedra of the octet with all corners on x+y+z = +-R (layer 0), near the origin
    out = []
    near = [p for p in pts if abs(abs(p.sum()) - R) < 1e-9 and np.linalg.norm(p) < 2.6 * R]
    for q in itertools.combinations(range(len(near)), 4):
        Q = [near[i] for i in q]
        if all(abs(np.dot(a - b, a - b) - e2) < 1e-9 for a, b in itertools.combinations(Q, 2)): out.append(np.array(Q))
    return out
TS = tets_in_slab(); T0 = TS[0]; tet = hull(T0 - T0.mean(0))
# a bipyramid: a layer-0 tetrahedron with a face on x+y+z = R, and its mirror
up = [Q for Q in TS if sum(abs(p.sum() - R) < 1e-9 for p in Q) == 3][0]
B = np.vstack([up, up @ MIR.T + MT]); bip = hull(B - B.mean(0))
stella, dbt = hull(ST), hull(DB)
pieces, pid = [], {}
def piece(name, mf, colour, glass=False):
    P, T = mesh(mf); pid[name] = len(pieces)
    pieces.append(dict(name=name, c=colour, o=0.4 if glass else 1, v=np.round(P, 6).tolist(), t=T.tolist()))
piece('og', OG, 0xd9a521); piece('capL', capL, 0x3f9a5b); piece('capR', m3.Manifold(m3.Mesh(vert_properties=np.ascontiguousarray(-mesh(capL)[0], dtype=np.float32),
      tri_verts=np.ascontiguousarray(mesh(capL)[1][:, ::-1], dtype=np.uint32))), 0x2a9d9a)
piece('twinCap', twin, 0x8e5bd0); piece('tet', tet, 0xc8382f); piece('bipyramid', bip, 0xe07b39)
piece('stella', stella, 0xe8c33a); piece('dbt', dbt, 0xd9a521, glass=True)
# mirror twins (layer 1, the far side of a twin pair) in blue, as in the paper's figures
piece('ogTwin', OG, 0x5b8fd0); piece('stellaTwin', stella, 0x6aa5e0); piece('dbtTwin', dbt, 0x5b8fd0, glass=True)
CHIRAL = {pid['capL']: pid['capR'], pid['capR']: pid['capL']}
TWIN = {pid['og']: pid['ogTwin'], pid['stella']: pid['stellaTwin'], pid['dbt']: pid['dbtTwin']}
def vol_centre(p, A, t):
    P = np.array(pieces[p]['v']) @ np.array(A).T + t; T = pieces[p]['t']; v = 0; c = np.zeros(3)
    for a, b, d in T:
        x = np.linalg.det(np.array([P[a], P[b], P[d]])) / 6; v += x; c += x * (P[a] + P[b] + P[d]) / 4
    return abs(v), (c / v)
def item(name, A=np.eye(3), t=(0, 0, 0)):
    p = pid[name]; A = np.asarray(A, float); t = np.asarray(t, float); _, c = vol_centre(p, A, t)
    return [p, *np.round(A.ravel(), 6).tolist(), *np.round(t, 6).tolist(), *np.round(c, 6).tolist()]
def mirror_item(it):   # the item mirrored in x+y+z = R; a mirrored left cap is drawn as a right cap
    p, A, t = it[0], np.array(it[1:10]).reshape(3, 3), np.array(it[10:13])
    A2, t2 = MIR @ A, MIR @ t + MT
    if p in CHIRAL: p, A2 = CHIRAL[p], -A2      # capR = -capL, so MIR A capL = (-MIR A) capR
    p = TWIN.get(p, p)   # the same solid, drawn in the twin colour
    _, c = vol_centre(p, A2, t2)
    return [p, *np.round(A2.ravel(), 6).tolist(), *np.round(t2, 6).tolist(), *np.round(c, 6).tolist()]
LFACES = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
caps = [item('capL', np.diag(s)) for s in LFACES] + [item('capR', np.diag(s)) for s in LFACES]   # capR under -s
# the two tetrahedra of layer 0 that belong to the cell of the origin octahedron (one class each modulo R(1,-1,0), R(0,1,-1))
U1, U2 = np.array([1, -1, 0]) * R, np.array([0, 1, -1]) * R
def cls(c):
    for i in range(-4, 5):
        for j in range(-4, 5):
            yield tuple(np.round(c + i * U1 + j * U2, 5))
seen, cell_tets = set(), []
for Q in sorted(TS, key=lambda Q: np.linalg.norm(Q.mean(0))):
    k = tuple(np.round(Q.mean(0), 5))
    if k in seen: continue
    seen.update(cls(Q.mean(0))); cell_tets.append(item('tet', np.eye(3), Q.mean(0)))
assert len(cell_tets) == 2, len(cell_tets)
cellv = (64 + 32 * 5 ** .5) / 81 + 2 * (16 + 8 * 5 ** .5) / 81
kits = {
  'gOG': [item('og')],
  'gCaps': [item('og')] + caps + cell_tets,
  'gStella': [item('stella')],
  'gDBT': [item('dbt'), item('og')],
}
s = sum(vol_centre(it[0], np.array(it[1:10]).reshape(3, 3), np.array(it[10:13]))[0] for it in kits['gCaps'])
print(f'cell kit volume {s:.6f} vs cell (32 + 16√5)/27 = {cellv:.6f}'); assert abs(s - cellv) < 1e-3
def layout(names):
    out, x = [], 0.0; rs = []
    for n in names:
        P = np.array(pieces[pid[n]]['v']); c = P.mean(0); r = np.max(np.linalg.norm(P - c, axis=1)); rs.append((n, c, r))
    for i, (n, c, r) in enumerate(rs):
        if i: x += r
        out.append(item(n, np.eye(3), np.array([x, 0, 0]) - c)); x += r + 0.15
    mid = (x - 0.15) / 2
    return [it[:10] + [it[10] - mid, it[11], it[12], it[13] - mid, it[14], it[15]] for it in out]
SETS = {'gOG': ['og'], 'gCaps': ['og', 'capL', 'capR', 'twinCap', 'tet', 'bipyramid'], 'gStella': ['stella'], 'gDBT': ['dbt']}
out = {'R': R, 'pieces': pieces, 'kits': {}}
for k, unit in kits.items():
    st = layout(SETS[k])
    if k == 'gDBT': st = st + [item('og', np.eye(3), np.array(st[0][13:16]))]   # the DBT holds its OG
    pair = [it for it in unit if it[0] not in (pid['tet'],)] if k == 'gCaps' else unit
    pair = [it for it in pair] + [mirror_item(it) for it in pair]
    out['kits'][k] = dict(set=st, pair=pair, unit0=unit, unit1=[mirror_item(it) for it in unit])
hdr = ('// Generated by scripts/build-gyrated-octet-data.py (Octet ↔ gyrated, DICTO 2026-10-20; paper #37a). Do not edit.\n'
       '// Items: [piece, 3×3 linear part by rows, translation, centre].\n')
open(OUT, 'w').write(hdr + 'export default ' + json.dumps(out, separators=(',', ':')) + ';\n')
print('wrote', OUT, os.path.getsize(OUT), 'bytes;', {k: len(v['unit0']) for k, v in out['kits'].items()})
