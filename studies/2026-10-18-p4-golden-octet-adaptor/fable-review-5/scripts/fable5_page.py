# Fable review 5, PHASE 2: 3D page for the W with the continuous creased-kite relief (same template as the other kit pages, plus a low raking
# light so the 1-2 mm relief reads). -> renders/p4-continuous-W.html (study renders + fable-review-5/renders)
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(H, '..', '..')
N = json.load(open(os.path.join(H, '..', 'data', 'fable5-node.json'))); Gm = json.load(open(os.path.join(H, '..', 'data', 'relief-geometry.json'))); R = Gm['R']; m = np.array(Gm['m']); pr = Gm['params']
P = {'ocd': dict(v=N['ocd_mesh']['v'], t=N['ocd_mesh']['t'], colour='#d9a21b'), 'Wk': dict(v=N['W_mesh']['v'], t=N['W_mesh']['t'], colour='#ec407a'),
     'Wk2': dict(v=N['W_mesh']['v'], t=N['W_mesh']['t'], colour='#26a69a'), 'Ws': dict(v=N['W_star_mesh']['v'], t=N['W_star_mesh']['t'], colour='#b0bec5')}
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
Gn = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float); c = (m + Gn @ m) / 2
pair = [['Wk', False, (m - c).tolist()], ['Wk2', False, (Gn @ m - c).tolist(), Gn.ravel().tolist()]]
L = np.array([[R, R, 0], [R, 0, R], [0, R, R]]); fcc = [np.array(cc) @ L for cc in itertools.product(range(-2, 3), repeat=3)]; fcc = [p for p in fcc if np.linalg.norm(p) <= 1.6 * R]
net = []
for t in fcc:
    for G in ring.values():
        s_ = G @ m + t
        if np.linalg.norm(s_) <= 1.35 * R and not any(np.allclose(s_, q[2]) for q in net): net.append(['Wk', False, s_.tolist(), G.ravel().tolist()])
w = N['W']; rg = N['ring12']; sm = N['sampling']; sy = N['symmetry']; sc = Gm['scale_mm']
views = {
    'one': dict(label='One W, close up', text=f"star-centred W with the OCD's kite rows continued over all 8 flat faces: {pr['d_rim_mm']:.1f} mm deep at the sockets fading to {pr['d_far_mm']:.1f} mm, zero on the oblique edges; raking light from the left", radius=0.8, place=[['Wk', False, [0, 0, 0]]]),
    'pair': dict(label='Two W across a seam', text='two identical W sharing one flat face: the kite rows raised on the pink piece are sunk on the teal one, the seam kites half and half. Pull apart along the face normal', radius=1.3, place=pair),
    'ring': dict(label='12 round one OCD', text=f"the OCD held by its 12 W (alternate colours): pairwise overlap {rg['max_pairwise_overlap']:.1e}, union = 12 W + OCD (gap {rg['gap']:.1e})", radius=2.0, place=[['ocd', False, [0, 0, 0]]] + ring_place),
    'net': dict(label='Network', text=f"OCDs on the fcc sites, W on every octahedron-edge midpoint: sampled {sm['uniform']['n']:,} uniform + {sm['near_faces']['n']:,} near-face points, {sm['uniform']['in_no_piece'] + sm['near_faces']['in_no_piece']} uncovered, {sm['uniform']['in_two_or_more'] + sm['near_faces']['in_two_or_more']} double", radius=2.9, place=[['ocd', False, p.tolist()] for p in fcc] + net),
    'plain': dict(label='Plain W for comparison', text='the unkeyed star-centred W (grey) beside the patterned one (pink)', radius=1.1, place=[['Ws', False, [-0.55, 0, 0]], ['Wk', False, [0.55, 0, 0]]]),
}
facts = [f"Pattern: the OCD's own star kite ({pr['kite_long_edge'] * sc:.1f} / {pr['kite_short_edge'] * sc:.1f} mm edges at a 60 mm octahedron edge) in rows parallel to each seam edge, one row axis on the seam (forced by the half-turn that places the W behind the seam); rows alternate roof / trough, each kite creased along its long diagonal; the seam kites are half raised, half sunk.",
         f"Depth transition: ridge-to-valley {pr['d_rim_mm']:.1f} mm at the socket rim, fading linearly to {pr['d_far_mm']:.1f} mm at {pr['rho_far'] * sc:.0f} mm from the OCD centre (the imprint's own relief is 1.1 mm: star centre 1.12 mm above its neighbours, facets folding 23.8°); relief fades to zero within {pr['fade_mm']:.1f} mm of the oblique edges so the faces close into one solid. Bump faces A0E0T±, A1E1T±; dent faces A0E1T±, A1E0T± (the exact g⁻¹ / σ / ι images).",
         f"Checks (manifold3d, dicto-node): one solid ({w['solid_parts']} part, genus {w['genus']}), volume {w['volume']:.6f} vs plain W {w['W_star_volume']:.6f} (raised = sunk); the piece has its 2/m symmetry (σ and ι symmetric-difference volumes {sy['sigma_symdiff']:.1e}, {sy['iota_symdiff']:.1e}) so every placed W is the same solid; pair across a face: overlap {N['pair_face1']['overlap']:.1e}, gap {N['pair_face1']['gap']:.1e}; 12 round one OCD: max overlap {rg['max_pairwise_overlap']:.1e}, union = 12 W + OCD; tiling sampled {sm['uniform']['n'] + sm['near_faces']['n']:,} points: {sm['uniform']['in_no_piece'] + sm['near_faces']['in_no_piece']} uncovered, {sm['uniform']['in_two_or_more'] + sm['near_faces']['in_two_or_more']} double.",
         'Fable review 5 (phase 2), 2026-10-18 · studies/2026-10-18-p4-golden-octet-adaptor/fable-review-5 · drawing: claude.ai/artifact/GLvBq8Fwv2LMT2TBXkkmyG']
html = open(os.path.join(ST, 'scripts', 'kit_viewer_template.html')).read()
# raking light: a strong low directional light fixed in the scene from the left, weaker ambient, so the shallow relief reads
html = html.replace("scene.add(new THREE.HemisphereLight(0xffffff,0x445566,.7));const dl=new THREE.DirectionalLight(0xffffff,.75);dl.position.set(3,5,4);cam.add(dl);scene.add(cam);",
                    "scene.add(new THREE.HemisphereLight(0xffffff,0x445566,.35));const dl=new THREE.DirectionalLight(0xffffff,.45);dl.position.set(3,5,4);cam.add(dl);scene.add(cam);const rake=new THREE.DirectionalLight(0xffffff,1.1);rake.position.set(-6,1.2,2);scene.add(rake);")
for k, v in {'__TITLE__': 'Continuous Kite W', '__SUB__': "DICTO 2026-10-18: the star-centred W with the OCD's kite pattern continued over its flat faces and seams, deepest at the sockets, fading outward; every W identical and keyed to its neighbours. Drag to turn, pull apart with the slider.",
             '__MARK__': 'fable-review-5', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts), '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
for path in (os.path.join(ST, 'renders', 'p4-continuous-W.html'), os.path.join(H, '..', 'renders', 'p4-continuous-W.html')): open(path, 'w').write(html)
print('ok', len(html), 'net', len(net))
