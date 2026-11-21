# DICTO · dictospheres.com — compose the three Amber-Ammann renders in the house card style of the scutoid stand-in compose.py
# (its helper functions are taken from that file unchanged; shots from ../shots/<scene>/p<i>.png, written by shots.mjs).
import os, json
H = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.join(H, '..')
src = open(os.path.join(H, '..', '..', '..', '2026-11-21-scutoid-stand-in', 'renders', 'scripts', 'compose.py')).read()
exec(src[:src.index("s = lambda sc, i")].replace("H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, 'figures')",
                                                 "R = os.path.join(BASE, 'shots'); OUT = BASE"))
s = lambda sc, i: os.path.join(R, sc, f'p{i}.png')
I = json.load(open(os.path.join(BASE, 'html', 'info.json')))
SAND, SLATE = (214, 180, 106), (127, 147, 168); PEARL = (226, 222, 214); BLUE = (58, 112, 205); GLASS = (120, 128, 132)
KINDS = [(214, 180, 106), (156, 116, 72), (127, 147, 168), (201, 158, 149), (143, 138, 128), (185, 176, 138), (163, 156, 176), (138, 163, 154)]
CORE = [(PEARL, 'Rollerball decagon faces'), (BLUE, 'Rollerball pyramids (icosahedron)')]
figure('RENDER-ammann-patch.png', 'A patch of the 3D Penrose tiling with a Rollerball in every cell',
       f"{I['nP']} prolate and {I['nO']} oblate golden rhombohedra (cells drawn slightly shrunk) from an exact patch of 402 · one Rollerball at each cell centre, one size, one orientation",
       [(s('patch', 0), 'never-repeating setting', 'prolate : oblate = golden ratio, so no period')],
       [(SAND, 'prolate golden rhombohedron'), (SLATE, 'oblate golden rhombohedron')] + CORE, cell=1000)
figure('RENDER-ammann-cells.png', 'Rollerball-Amber Cells: a prolate and an oblate golden rhombohedron',
       "DICTO's combined method, centroid seeds · each Rollerball core with its 72 scutoid pieces pulled apart from the centre, mould far side see-through · colours label the 8 kinds in each cell",
       [(s('cells', 0), 'prolate golden rhombohedron', '72 scutoids · 8 kinds · 30 Y vertices'), (s('cells', 1), 'oblate golden rhombohedron', '72 scutoids · 8 kinds · 30 Y vertices')],
       [(KINDS[i], f'kind {i + 1}') for i in range(8)] + CORE + [((255, 255, 255), 'Y vertex'), (GLASS, 'mould')], cell=760)
nm = {'P': 'prolate', 'O': 'oblate'}
a, b = I['seams'][0][0][0], I['seams'][0][0][1]; assert I['seams'][0][1] is False and I['seams'][1][1] is True
figure('RENDER-ammann-seam.png', 'Where two Rollerball-Amber Cells meet: the pieces on a shared wall',
       'Top pieces of both cells drawn on the one wall (sand: first cell, slate: second cell) · left: prolate meets oblate · right: two prolate cells',
       [(s('seam', 0), f'{nm[a]}–{nm[b]} wall: the patterns do not line up', f'{I["seams"][0][2]} + {I["seams"][0][3]} regions, tops differ'),
        (s('seam', 1), 'prolate–prolate wall: the patterns agree', f'{I["seams"][1][2]} regions, edge to edge')],
       [(SAND, f'{nm[a]} cell, first (left)'), (SLATE, f'{nm[b]} cell, second (left)'), ((226, 222, 214), 'both prolate (right): lines coincide')], cell=760)
