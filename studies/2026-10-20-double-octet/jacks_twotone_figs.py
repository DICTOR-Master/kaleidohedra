# DICTO 2026-10-21: the swapped Tetoktjiru (slim Oktjiru, strong Tetjiru; run with args 0.14 0.05 0.24 0.08 and TET_LEN=0.72) seen as
# coral creatures: "the Tetjiru are the bodies and the Oktjiru are the legs". Two tones: the up Tetjiru and the side of every Oktjiru
# leg facing them share one tone, the down Tetjiru and the side facing them the other (an Oktjiru point takes the tone of the Tetjiru
# in its octant: the 8 octants round an Oktjiru alternate up and down), so the block reads as two creatures woven through each other.
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'jacks_octet.py')).read().split(MAIN)[0])
TONE = {0: '#b8452f', 1: '#eea58c'}             # up bodies: deep coral; down bodies: pale coral
orient = lambda t: int(round(np.sum(t) - 1.5)) % 2
def part(mf, centre, shift=(0, 0, 0), turn=0):
    """colour per triangle (Tetjiru: its own tone; Oktjiru: the tone of the Tetjiru in that octant), then move by shift"""
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts); c = np.array(centre, float)
    if np.allclose(c, np.round(c)):
        X = P[T].mean(1); s = np.where(X - c >= 0, 1.0, -1.0); cols = [TONE[orient(c + .5 * v)] for v in s]
    else: cols = [TONE[orient(c)]] * len(T)
    if turn:                                   # turn about the vertical through the centre, after colouring
        a = np.radians(turn); R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]); P = (P - c) @ R.T + c
    return {'v': np.round(P + np.array(shift, float), 5).tolist(), 't': T.tolist(), 'c': cols, 'e': None, 'a': 1.0}
scenes = []; add = lambda t_, s_, parts: scenes.append({'title': t_, 'sub': s_, 'parts': parts})
O = np.array([1.0, 0, 0]); TU, TD = np.array([.5, .5, .5]), np.array([1.5, .5, .5])
add('DICTO Oktjiru: the legs', 'each leg half one tone, half the other', [part(jack(O), O)])
add('Oktjiru, turned', 'turned 45°', [part(jack(O), O, turn=45)])
add('Tetjiru bodies', 'up and down, one tone each', [part(tetrapod_at(TU), TU, (-.7, 0, 0)), part(tetrapod_at(TD), TD, (.7, 0, 0))])
ps = [part(jack(O), O)]
for sg in itertools.product((1, -1), repeat=3):
    t = O + .5 * np.array(sg, float); ps.append(part(tetrapod_at(t), t, .5 * np.array(sg, float)))
add('One Oktjiru among eight bodies', 'drawn apart', ps)
blk = [part(tetrapod_at(t), t, (t - 1) * 0.3) for t, _ in tets_in(range(0, 2))]
for p_ in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
    p = np.array(p_, float); blk.append(part(jack(p), p, (p - 1) * 0.3))
add('A block', 'two coral creatures woven through each other', blk)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'jacks-twotone.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'jacks-twotone-labels.json'), 'w'), indent=1)
print('jacks-twotone.html', len(scenes))
