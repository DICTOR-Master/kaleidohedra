# Builds catalogue.html: every step of Chain of Karma, Spheres of Dharma and Bodhi Kit B as one fused solid, with a
# turnable view and its counted facts (steps.json). Names are leads to check, never claims.
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
pieces = json.load(open(os.path.join(ROOT, 'pieces.json')))
steps = json.load(open(os.path.join(ROOT, 'steps.json')))

WORLD = {
    'karma.lotus': ('Chain of Karma', 'Lotus seed, DISCOVERIES #22'),
    'dharma.cycle': ('Spheres of Dharma', 'one Ritsudō cycle, DISCOVERIES #23'),
    'bodhi.kitB': ('Bodhi Seed', 'Kit B, DISCOVERIES #24'),
}
PIECE = {'ico': 'icosahedra', 'cleo': 'CLEO', 'axe': 'AXE', 'fuji': 'FUJI', 'core': 'icosahedron', 'nfru3': 'twisted triangular frusta',
         'npyr5': 'pentagonal pyramids', 'npyr3': 'triangular pyramids', 'nfru5': 'twisted pentagonal frusta', 'nt1': 'Mosseri–Sadoc t1 tiles',
         'ncap': 'caps', 'nwedge': 'edge wedges', 'nedge': 'edge pieces', 'nface': 'face pieces', 'centre': 'rhombic triacontahedron',
         'B1': 'Vajras', 'copy': 'triacontahedra', 'B5L': 'Diadems (left)', 'B5R': 'Diadems (right)', 'B4': 'Crown Jewels'}
# What each step is or may be. Convex steps: the classic solid (checked by face counts). Others: leads to check.
NOTES = {
    'karma.lotus': ['Icosahedron.',
                    'Lead: all 60 visible triangles lie on just 12 planes, in the dodecahedron\'s face directions, round an icosahedron core: the look of Kepler\'s great stellated dodecahedron. To check.',
                    'Lead: all 60 visible triangles lie on the 20 face planes of the centre icosahedron, so this is a stellation of the icosahedron. Which one: to check.',
                    '', '',
                    'Icosahedron, φ³ times the centre one.'],
    'dharma.cycle': ['Icosahedron.', '', 'Icosidodecahedron.', 'Dodecahedron.', '', 'Truncated icosahedron.',
                     'Convex, 80 corners: 60 triangles, 30 rectangles, 12 pentagons. Not one of the named convex solids I know; to check.',
                     '', 'Rhombic triacontahedron.',
                     'Lead: 60 triangles on 60 planes, all at one distance from the centre: one family of planes, like a stellation of a 60-faced solid. To check.',
                     'Icosahedron, φ³ times the centre one.'],
    'bodhi.kitB': ['Rhombic triacontahedron.',
                   'Lead: all 60 visible rhombi lie on the 30 face planes of the centre triacontahedron, so this is a stellation of the rhombic triacontahedron. Which one: to check.',
                   '', '', '', 'Rhombic triacontahedron, φ³ times the centre one.'],
}


def payload():
    out = []
    for view, (name, sub) in WORLD.items():
        P = pieces[view]
        allP = np.array([p for _, V, _ in P for p in V], float); c0 = allP.mean(0)
        rad = float(np.linalg.norm(allP - c0, axis=1).max())
        groups = {}
        for r, V, F in P:
            Q = (np.array(V, float) - c0) / rad
            k = f'{r}@{np.linalg.norm(Q.mean(0) * rad):.2f}'
            groups.setdefault(k, []).append({'v': np.round(Q, 5).tolist(), 'f': F})
        st = steps[view]
        order = [s['added'].split(' ')[0] for s in st]  # the steps' own order (steps.py)
        assert sorted(order) == sorted(groups), (order, list(groups))
        out.append({'id': view.split('.')[0], 'name': name, 'sub': sub, 'steps': [{
            'adds': f"{len(groups[g])} {PIECE.get(g.split('@')[0], g.split('@')[0])}" if i else f"the centre {PIECE.get(g.split('@')[0], '')}",
            'pieces': groups[g], 'convex': s['convex'], 'faces': s['faces'], 'shapes': s['faceShapes'], 'planes': s['planes'],
            'note': NOTES[view][i]} for i, (g, s) in enumerate(zip(order, st))]})
    return out


if __name__ == '__main__':
    tpl = open(os.path.join(HERE, 'catalogue-template.html')).read()
    html = tpl.replace('/*DATA*/null', json.dumps(payload(), separators=(',', ':')))
    open(os.path.join(ROOT, 'catalogue.html'), 'w').write(html)
    print('catalogue.html', len(html) // 1024, 'KB')
