# Fable review 4 (2026-10-18): 3D page for the keyed star-centred W, same template as renders/p4-golden-octet-adaptor.html
# (scripts/kit_viewer_template.html: placements [piece, flip, pos, 3x3 matrix]). -> renders/p4-keyed-W.html (study renders) + a copy in fable-review-4/renders
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(H, '..', '..')
N = json.load(open(os.path.join(H, '..', 'data', 'fable4-node.json'))); Gm = json.load(open(os.path.join(H, '..', 'data', 'keyed-W-geometry.json')))
R = Gm['R']; m = np.array(Gm['m']); mm = Gm['mm']
P = {'ocd': dict(v=N['ocd_mesh']['v'], t=N['ocd_mesh']['t'], colour='#d9a21b'),
     'Wk': dict(v=N['keyed_W_mesh']['v'], t=N['keyed_W_mesh']['t'], colour='#ec407a'),
     'Wk2': dict(v=N['keyed_W_mesh']['v'], t=N['keyed_W_mesh']['t'], colour='#26a69a'),
     'Ws': dict(v=N['W_star_mesh']['v'], t=N['W_star_mesh']['t'], colour='#b0bec5')}
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
ring = {}
for G in ops:
    k = tuple(np.round(G @ m, 6))
    if k not in ring: ring[k] = G
ring_place = [['Wk' if i % 2 == 0 else 'Wk2', False, (G @ m).tolist(), G.ravel().tolist()] for i, G in enumerate(ring.values())]
Gn = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)                     # neighbour across bump face 1: g(m) = (R/2, R/2, 0)
c = (m + Gn @ m) / 2
pair = [['Wk', False, (m - c).tolist()], ['Wk2', False, (Gn @ m - c).tolist(), Gn.ravel().tolist()]]
# a small network: OCDs on the fcc sites near the origin and keyed W on all edge midpoints within reach
L = np.array([[R, R, 0], [R, 0, R], [0, R, R]]); fcc = [(np.array(cc) @ L) for cc in itertools.product(range(-2, 3), repeat=3)]
fcc = [p for p in fcc if np.linalg.norm(p) <= 1.6 * R]
net = []
for t in fcc:
    for G in ring.values():
        s = G @ m + t
        if np.linalg.norm(s) <= 1.35 * R and not any(np.allclose(s, q[2]) for q in net): net.append(['Wk', False, s.tolist(), G.ravel().tolist()])
views = {
    'one': dict(label='Keyed W, one piece', text='star-centred W with its 8 keys: 4 kite bumps (faces at the edge ends E0/E1 with A0E0, A1E1) and 4 kite dents, each kite = the star kite (edges 9.4 / 7.8 mm at 60 mm octahedron edge), relief 2.0 mm', radius=0.95, place=[['Wk', False, [0, 0, 0]]]),
    'pair': dict(label='Bump meets dent', text='two identical keyed W across one shared face: the pink piece\'s bump sits exactly in the teal piece\'s dent (overlap 0, gap 0). Pull apart along the face normal', radius=1.3, place=pair),
    'ring': dict(label='12 round one OCD', text='the OCD held by its 12 keyed W (alternate colours), every W keyed to its 4 ring neighbours: no single W can be translated out while the others stay (0 of 600 directions; 41 free for the unkeyed W)', radius=2.0, place=[['ocd', False, [0, 0, 0]]] + ring_place),
    'set': dict(label='The set', text='the two shapes: OCD (gold) and the keyed star-centred W (pink); volume (1412 − 164√5)/4617 = 0.226399 unchanged (bumps = dents), one solid, genus 0', radius=1.1, place=[['ocd', False, [-0.75, 0, 0]], ['Wk', False, [0.6, 0, 0]]]),
    'plain': dict(label='Unkeyed W for comparison', text='the plain star-centred W (grey) next to the keyed one (pink)', radius=1.1, place=[['Ws', False, [-0.55, 0, 0]], ['Wk', False, [0.55, 0, 0]]]),
    'net': dict(label='Network', text='OCDs on the fcc sites with keyed W on every octahedron-edge midpoint: fills space exactly (sampled 6,000,000 points: 0 uncovered, 0 double)', radius=2.9, place=[['ocd', False, p.tolist()] for p in fcc] + net),
}
kw = N['keyed_W']; pr = N['pair_separation']; rr = N['ring12_piece_removal']; smp = N.get('sampling', {})
facts = [f"Keyed W = star-centred W (Voronoi octahedron of an octahedron-edge midpoint minus its two OCDs) with 4 kite bumps and 4 kite dents on its 8 flat faces. Faces pair bipartitely across the structure (bump faces carry the socket's A0E0 / A1E1 edges, dent faces A0E1 / A1E0), so one identical piece keys with itself everywhere.",
         f"The key tile is the OCD's own star kite (long edge {mm['kite_long_edge']:.1f} mm, short edge {mm['kite_short_edge']:.1f} mm, long diagonal {mm['kite_long_diagonal']:.1f} mm at a 60 mm octahedron edge): on each bump face two rim edges of the socket's five-fold star pierce the face; the kite's 55.7° apex sits {mm['kite_shift_along_edge']:.1f} mm beyond the piercing point and its long edge runs {mm['kite_offset_beside_star_edge_line']:.1f} mm beside the pierced edge's line, turned {abs(Gm['chosen']['rho_deg']):.0f}°: the star's kite pattern continues across the flat face.",
         f"Relief {mm['relief_height']:.1f} mm, walls 30° off the face normal (top kite {mm['top_kite_long_edge']:.1f} mm long edge); clearance {mm['clearance_to_socket_shadow']:.1f} mm from the OCD and {mm['clearance_to_cell_edges']:.1f} mm from the piece's edges; sharpest edge {kw['sharpest_edge_deg']:.1f}° (the cell's own), no slivers.",
         f"Checks (dicto-node, manifold3d): one solid, genus {kw['genus']}, volume = unkeyed W to 1e-15 (bumps {kw['bump_volume_total']:.6f} = dents {kw['dent_volume_total']:.6f}); pair across a face: overlap 0, union = both cells minus OCDs (no gap); 12 round one OCD: 66 pairs, overlap 0, union = 12 W + OCD.",
         f"Locking: a pair separates only within {pr['max_angle_from_face_normal_deg']:.0f}° of the face normal ({pr['free_directions']} of {pr['directions_tested_outward']} outward directions); in the 12-ring round an OCD no W can be translated out ({rr['free_directions']} of {rr['directions_tested']} directions; unkeyed W: {rr['free_directions_unkeyed_W_star']}). Assembly: place the OCD, then add W pieces one by one, each pushed on along its bump-face normals.",
         'Tiling: ' + (', '.join(f"{k}: {v['n']:,} points, {v['in_no_piece']} uncovered, {v['in_two_or_more']} double" for k, v in smp.items()) if smp else 'sampling in progress') + '.',
         'Fable review 4, 2026-10-18 · studies/2026-10-18-p4-golden-octet-adaptor/fable-review-4']
html = open(os.path.join(ST, 'scripts', 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Keyed Star W', '__SUB__': 'DICTO 2026-10-18: the star-centred W with the star\'s kite pattern continued across its flat faces as keys. One piece, keys with itself. Drag to turn, pull apart with the slider.',
             '__MARK__': 'fable-review-4', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts), '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
for path in (os.path.join(ST, 'renders', 'p4-keyed-W.html'), os.path.join(H, '..', 'renders', 'p4-keyed-W.html')):
    open(path, 'w').write(html)
print('ok', len(html), 'ring', len(ring_place), 'net', len(net))
