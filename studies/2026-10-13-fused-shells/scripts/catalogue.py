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
PIECE = {'cap': 'caps', 'ico': 'icosahedra', 'cleo': 'CLEO', 'axe': 'AXE', 'fuji': 'FUJI', 'core': 'icosahedron', 'nfru3': 'Vajra (twist)',
         'npyr5': 'Stupa', 'npyr3': 'Cleo-low', 'nfru5': 'Monkey Staff', 'nt1': 'Mosseri–Sadoc t1 tiles',
         'ncap': 'caps', 'nwedge': 'Vajra-blade', 'nedge': 'Sevenfold-blade', 'nface': 'Cleo-low 2', 'centre': 'rhombic triacontahedron',
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


CLASSIC = {(('3-gon', 20),): 'Icosahedron', (('5-gon', 12),): 'Dodecahedron', (('3-gon', 20), ('5-gon', 12)): 'Icosidodecahedron',
           (('5-gon', 12), ('6-gon', 20)): 'Truncated icosahedron', (('4-gon', 30),): 'Rhombic triacontahedron',
           (('3-gon', 60), ('4-gon', 30), ('5-gon', 12)): 'Convex, 80 corners (unnamed?)'}
stage_facts = json.load(open(os.path.join(ROOT, 'stages-facts.json')))


def stages_for(view, order):
    P = pieces[view]
    allP = np.array([p for _, V, _ in P for p in V], float); c0 = allP.mean(0)
    ring = [f'{r}@{np.linalg.norm(np.array(V, float).mean(0) - c0):.2f}' for r, V, _ in P]
    within, count = [], {}
    for g in ring: within.append(count.get(g, 0)); count[g] = count.get(g, 0) + 1
    out = []
    for f in stage_facts[view]:
        idx = set(f['pieces'])
        whole = [g for g in set(ring[i] for i in idx) if all(i in idx for i, x in enumerate(ring) if x == g)]
        part = sorted([order.index(ring[i]), within[i]] for i in idx if ring[i] not in whole)
        key = tuple(sorted(f['faceShapes'].items()))
        out.append({'g': sorted(order.index(x) for x in whole), 'p': part, 'how': f['how'], 'convex': f['convex'], 'faces': f['faces'],
                    'shapes': f['faceShapes'], 'planes': f['planes'], 'name': CLASSIC.get(key) if f['convex'] else None})
    return out


def film_order(groups, order):
    centre = groups[order[0]][0]['v']
    C = np.array(centre)
    axis = C[np.argmax(np.linalg.norm(C, axis=1))]  # a corner of the centre solid on a five-fold axis (icosahedron: any; RT: the far ones)
    axis = axis / np.linalg.norm(axis)
    ref = np.cross(axis, [1, 0, 0] if abs(axis[0]) < 0.9 else [0, 1, 0]); ref /= np.linalg.norm(ref); ref2 = np.cross(axis, ref)
    out = [[0, 0]]
    for i, g in enumerate(order[1:], 1):
        cs = [np.array(p['v']).mean(0) for p in groups[g]]
        key = lambda j: (round(float(np.degrees(np.arccos(np.clip(np.dot(cs[j], axis) / np.linalg.norm(cs[j]), -1, 1)))), 1),
                         float(np.arctan2(np.dot(cs[j], ref2), np.dot(cs[j], ref))))
        out += [[i, j] for j in sorted(range(len(cs)), key=key)]
    return out


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
            'note': NOTES[view][i]} for i, (g, s) in enumerate(zip(order, st))],
            # every stage (stages.py, partials.py; facts by stage_facts.py): whole rings as step indices, and for a partial stage the
            # extra pieces as [step index, piece index within that step's ring]
            'stages': stages_for(view, order),
            # growth film: every piece in turn, ring by ring, each ring from the top of a five-fold axis down (by angle, then round)
            'film': film_order(groups, order)})
    return out


APP_VIEWS = [('karma.lotus', 'Chain of Karma · Lotus seed'), ('karma.step2', 'Chain of Karma · Chain step 2'), ('karma.dodeca', 'Chain of Karma · Dodecahedral Chain'),
             ('dharma.cycle', 'Spheres of Dharma · one Ritsudō cycle'), ('dharma.inner', 'Spheres of Dharma · inner half'), ('dharma.outer', 'Spheres of Dharma · outer half'),
             ('dharma.hinge', 'Spheres of Dharma · hinge'), ('bodhi.seed', 'Bodhi Seed · seed'), ('bodhi.kitB', 'Bodhi Seed · Kit B'), ('bodhi.kitA', 'Bodhi Seed · Kit A'),
             ('bodhi.hollow', 'Bodhi Seed · the hollow')]


def app_note(f):
    """A lead from the counts: a classic convex solid, or faces on only a few planes (a stellation or compound look-alike)."""
    key = tuple(sorted(f['faceShapes'].items()))
    if f['convex']: return (CLASSIC.get(key, 'Convex') + '.') if CLASSIC.get(key) else f"Convex, {f['faces']} faces: to identify."
    if f['planes'] <= 30: return f"Lead: its {f['faces']} visible faces lie on only {f['planes']} planes: a stellation or compound look-alike. To check."
    return ''


def app_worlds():
    facts = {**json.load(open(os.path.join(ROOT, 'appstages.json'))), **json.load(open(os.path.join(ROOT, 'appstages2.json')))}
    out = []
    for view, name in APP_VIEWS:
        P = pieces[view]
        allP = np.array([p for _, V, _ in P for p in V], float); c0 = allP.mean(0)
        rad = float(np.linalg.norm(allP - c0, axis=1).max())
        steps_ = []
        for f in facts[view]:
            adds = ' + '.join(f"{n} {PIECE.get(r, r)}" for r, n in f['adds'].items())
            steps_.append({'adds': adds if f['level'] else f'the centre {adds.split(" ", 1)[1]}', 'convex': f['convex'], 'faces': f['faces'],
                           'shapes': f['faceShapes'], 'planes': f['planes'], 'note': app_note(f),
                           'pieces': [{'v': np.round((np.array(P[i][1], float) - c0) / rad, 4).tolist(), 'f': P[i][2]} for i in f['pieces']]})
        out.append({'id': view, 'name': name, 'sub': 'as the app\'s Top shell slider shows it', 'app': True, 'steps': steps_, 'stages': [], 'film': []})
    return out


if __name__ == '__main__':
    tpl = open(os.path.join(HERE, 'catalogue-template.html')).read()
    html = tpl.replace('/*DATA*/null', json.dumps(payload() + app_worlds(), separators=(',', ':')))
    open(os.path.join(ROOT, 'catalogue.html'), 'w').write(html)
    print('catalogue.html', len(html) // 1024, 'KB')
