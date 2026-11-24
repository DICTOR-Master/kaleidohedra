# DICTO · dictospheres.com — compose the four new Amber-Ammann renders of #118 Version 2 (shots of ammann_scenes2.py, written by shots.mjs)
# in the house card style: figure() and its helpers are taken unchanged from the scutoid stand-in compose.py, as in ammann_compose.py.
# Every number on the cards is read from html/info2.json (written by ammann_scenes2.py from the study data).
import os, json
H = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.join(H, '..')
src = open(os.path.join(H, '..', '..', '..', '2026-11-21-scutoid-stand-in', 'renders', 'scripts', 'compose.py')).read()
exec(src[:src.index("s = lambda sc, i")].replace("H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, 'figures')",
                                                 "R = os.path.join(BASE, 'shots'); OUT = BASE"))
s = lambda sc, i: os.path.join(R, sc, f'p{i}.png')
I = json.load(open(os.path.join(BASE, 'html', 'info2.json')))
SAND, SLATE = (214, 180, 106), (127, 147, 168); PEARL = (226, 222, 214); BLUE = (58, 112, 205); VIOLET = (138, 92, 196); GLASS = (120, 128, 132)
GREY = (207, 216, 220); WALL = (214, 180, 106)    # GLASS '#cfd8dc' (the piece's face on the mould), KIND[kind of face 0] = '#d6b46a' in ammann_scenes2.py
n, nP, nO, nor = I['A']
figure('RENDER-ammann-patch402.png', 'The exact patch of Lemma 2: 402 golden rhombohedra',
       f'{nP} prolate and {nO} oblate cells in all {nor} orientations, face to face · cells drawn slightly shrunk',
       [(s('patch402', 0), 'the whole patch', f'{n} cells · {nP} prolate + {nO} oblate')],
       [(SAND, 'prolate golden rhombohedron'), (SLATE, 'oblate golden rhombohedron')], cell=760)
figure('RENDER-ammann-cores5.png', 'Five icosahedral cores in the prolate golden rhombohedron',
       'Prolate cell 134 at 6/5 S0 with projected seeds, a setting valid for all five · moulds drawn at one size, far side see-through',
       [(s('cores5', i), nm, f'{a} of {b} Scutoid-Frusta · {y} Y vertices') for i, (nm, a, b, y, *_) in enumerate(I['B'])],
       [(BLUE, 'icosahedron colour'), (VIOLET, 'dodecahedron colour'), (PEARL, 'other faces'), (GLASS, 'mould')], cell=520)
c, cP, cO, cor, npc = I['C']
figure('RENDER-ammann-slab.png', 'The never-repeating Scutoid-Frusta layer, one slab',
       f'{c} cells of the exact patch near one plane · each cell shows the tops of its 72 Scutoid-Frusta on its walls',
       [(s('slab', 0), f'one slab: {cP} prolate + {cO} oblate cells', f'{npc} Scutoid-Frusta · {cor} orientations')],
       [(SAND, 'prolate cell'), (SLATE, 'oblate cell')], cell=760)
ni, no, ny, nv, ne, nf, vol, nyd = I['D']
figure('RENDER-ammann-piece.png', 'One Scutoid-Frustum of a Rollerball-Amber Cell',
       f'Prolate cell 134, the piece on a decagon of the Rollerball: {ni} neighbours on the core side, {no} on the mould side, {ny} Y vertices',
       [(s('piece', 0), 'whole', f'{nv} vertices · {ne} edges · {nf} flat faces'), (s('piece', 1), 'pulled apart', 'ends moved along the axis, sides outwards')],
       [(PEARL, 'face on the Rollerball (decagon)'), (GREY, 'face on the mould (pentagon)'), (WALL, 'side walls'), ((255, 255, 255), 'Y vertex')], cell=760)
