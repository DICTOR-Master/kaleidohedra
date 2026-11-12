# One-off (13 Nov 2026): compose the chapter sources of the expanded book (PROPOSAL.html, the arc on the neighbour swap)
# from the migrated old chapters (tools/old, made by migrate_v1.py). Lines are the blocks of the old chapters; NEW marks
# where new text is written by hand afterwards. Run once; afterwards chapters/*.html are the sources.
import os, json
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.join(H, 'tools', 'old'); C = os.path.join(H, 'chapters')
L = {}
def old(ch, a, b=None):
    if ch not in L: L[ch] = open(os.path.join(O, f'{ch}.html'), encoding='utf8').read().split('\n')
    return '\n'.join(L[ch][a - 1:(b or a)])
def NEW(what): return f'<!--NEW {what}-->'
def write(n, key, title, sub, frm, parts):
    meta = json.dumps({'key': key, 'title': title, 'sub': sub, 'from': frm}, ensure_ascii=False)
    open(os.path.join(C, f'{n:02d}-{key}.html'), 'w', encoding='utf8').write(f'<!--META {meta}-->\n' + '\n'.join(parts) + '\n')
write(1, 'three', 'Orderings of Three: the Truncated Triangle', 'Every truncated triangle is the permutohedron of three values, and every 2-dimensional face of every permutohedron is a truncated triangle or a rectangle',
      'Retold from {D:88} and {D:20}, with #48 and #105. Lemma {{s:o1.1}} and its reading of DICTO\'s solids as gap ratios are new in this book.',
      [NEW('opener'), old(1, 9, 31), NEW('worked example, figure, hand-off'), old(1, 32, 33)])
write(2, 'kelvin', "Orderings of Four: Kelvin's Cell", 'The 24 orders of four values, joined by 36 swaps of three kinds, are Kelvin\'s cell, the one permutohedron that fills space alone',
      'Retold from {D:100}, {D:26} and {D:58}, with #48 and #105. The reading of the 36 edges by the pair they swap is new in this book.', [NEW('chapter')])
write(3, 'slider', 'The Slider and Its Silent Station', 'The permutohedra of four values spaced symmetrically are the solids of DICTONIC\'s golden loop; each fills space with its reciprocal in one way only, and at the golden stop the fourth harmonic falls silent',
      'Retold from {D:48}, {D:105}, {D:93} and {D:94}. Proposition {{s:o2.1}} and the reading of the golden loop as symmetric spacings are new in this book.',
      [NEW('opener'), old(2, 9, 25), NEW('#94 section, figures, worked example, hand-off'), old(2, 26, 27)])
write(4, 'bonds', 'The Bonds as Spacing', 'The weight that drives the web of bonds is the relative difference of the gaps between four values',
      'Retold from {D:52}, {D:53} and {D:90}, with #105. The reading of the weight as the spacing, d = (g − m)/(g + m), is new in this book.',
      [NEW('opener'), old(3, 9, 24), NEW('worked example, figures, hand-off'), old(3, 26, 27)])
write(5, 'rd', 'Where the Paradigm Stops: the RD Taken Apart', 'Fourteen half rhombic dodecahedra close into the chamfered cube, a zonohedron that is not a permutohedron, and with cube pyramids it fills space',
      'New in this book, from DICTO\'s Hemi RD build in Polyhedraverse (11 November 2026); background in {D:58} and {D:87}.',
      [NEW('opener'), old(4, 9, 23), NEW('figures, worked example, hand-off'), old(4, 25, 26)])
write(6, 'scut3', 'Scutoids in Three Dimensions', 'The swap of neighbours in living tissue: flat-faced scutoid shells, their polar flip and the cycle that fills space',
      'Re-edited from DICTO\'s draft Scutoids: Layers, Shells and Cycles (10 November 2026, not published) and {D:104}.',
      [NEW('opener'), old(5, 9), NEW('one swap section, figure'), old(5, 15, 37), NEW('hand-off'), old(5, 39, 40)])
write(7, 'web', 'Five Values: the Web of Swaps and Its Vacuus', 'The 120 orderings of five values, the rules among their swaps, the 65 central slices of the 4D permutohedron with five DICTO 1:2 Truncated Octahedra at its heart, and the Mirror Law',
      'Re-edited from {D:105}, Sections 1–3, and {D:107}, Sections 1–5, with {D:108}, {D:87} and {D:91}.',
      [NEW('opener'), old(6, 8, 33), NEW('mirror law intro'), old(10, 10, 49), NEW('#91, worked example, hand-off'), old(6, 34, 35), old(10, 50, 51)])
write(8, 'centre1', 'Centre I. The 4D Permutohedron Swept: a Scutoid Tissue', 'Sweep the solid of all orders of five values and its slice is a tissue of cells that are born, swap neighbours and die: 26 births, 66 swaps, 26 deaths, counted by the Eulerian numbers',
      'Re-edited from {D:104}, Section 1 and Theorem 1, with Proposition {{s:o5.1}} of the draft. The 3D warm-up and the reading of the swap as the one self-reverse event are new in this book.',
      [NEW('opener, warm-up'), old(7, 9), old(5, 12, 13), old(7, 10, 13), NEW('prior-art sentence'), old(7, 38, 39), NEW('self-reverse, figures, hand-off'), old(7, 42, 43)])
write(9, 'centre2', 'Centre II. Every Simple 4-Polytope Is a Scutoid Tissue', 'Every simple 4-polytope, swept, is a scutoid tissue counted by its h-vector; between the Queens the swaps balance, 601 each way',
      'Re-edited from {D:104}, Section 1, Theorems 1′, 2, 4 and Lemma 5, and {D:108}, Theorems 1 and 3, with #63, #65 and #76.',
      [NEW('opener'), old(7, 14, 37), old(7, 40, 41), NEW('worked example, figures, hand-off'), old(7, 42, 43)])
write(10, 'rosettes', 'Rosettes: Many Neighbours Swapping at Once', 'Which uniform 4-polytopes sweep as clean scutoid tissues and which only in rosettes, read from the Coxeter chain; the rosettes balance by symmetry, and without symmetry they do not',
      'New in this book, from {D:104}, Lemma 5, and the Atlas of {D:108}; Section {{sec:o8.2}} from the study of 13 November 2026.',
      [NEW('opener'), old(8, 9, 42), NEW('figures, worked example, hand-off'), old(8, 44, 45)])
write(11, 'walls', '4D Scutoids: the Swap Rule and Its Walls', 'The Swap Rule of close packing below s = 1/4, proved stacking by stacking, and its walls as swaps of neighbours one dimension up',
      'Re-edited from {D:104}, Sections 2 and 3, which prove below s = 1/4 the Swap Rule of {D:61}; Section on cones of heights from DICTO\'s draft The Permutohedron Family, Section 9.',
      [NEW('opener'), old(9, 8, 31), NEW('family section 9, worked example, hand-off'), old(9, 32, 33)])
write(12, 'everyn', 'Every Number of Values', 'The permutohedron of n values in every dimension: its central slices counted, and its sweep counted by the Eulerian numbers',
      'Re-edited from {D:105}, Section 4, and {D:104}, Theorem 1′. Proposition {{s:o11.2}} for every n is new in this book.',
      [NEW('opener'), old(11, 8, 22), NEW('worked example, figure, hand-off'), old(11, 23, 24)])
write(13, 'golden', 'The Golden Slice', 'Cutting the 4D permutohedron filling in the golden direction gives a non-periodic filling of space (it repeats along a plane, never in a third direction) by cells of exactly 35 kinds, in endlessly many shapes',
      'New in this book. It answers the second lead of {D:105}.', [NEW('opener'), old(12, 9, 20), NEW('figures, worked example, hand-off'), old(12, 22, 23)])
write(14, 'family', 'The Permutohedron Family', 'Slide the walls of the permutohedron without turning them and every edge stays a swap: one cone of shapes from Kelvin\'s cell, which fills space, to the associahedron, whose canonical form is a scattering amplitude',
      'New in this book, retold from DICTO\'s draft paper The Permutohedron Family (12–13 November 2026, held as a paper, not published), with {D:49}, {D:50}, {D:89} and #87.',
      [NEW('opener'), old(14, 9, 58), NEW('one cone, #49, #50, #89'), old(14, 59, 60), NEW('hand-off, pointer'), old(14, 62, 63)])
write(15, 'bells', 'Change, Rhythm, Harmony', 'Ringers may only swap neighbours: every extent is a tour of a permutohedron, three bells ring the hexagon of the first page, and the three principles of Kyushindo can be read off the tours exactly',
      'New in this book. It reads the three principles of Kyushindo, as {D:43} gives them, in English change ringing.',
      [NEW('opener'), old(13, 9, 100), NEW('closing, pointer'), old(13, 102, 107)])
print(sorted(os.listdir(C)))
