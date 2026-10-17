# DICTO 2026-10-18 octet study, step 10 (+15 Penrose core, +20 keyless kit with three cores, +23 envelope kit) render: the pieces in 3D (gallery + exploded assembly round one OCD) -> renders/step10-pieces.html
import json, os
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'step15-meshes.json' if os.path.exists(os.path.join(H, '..', 'data', 'step15-meshes.json')) else 'step10-meshes.json')))
keep = {k: dict(v=d[k]['v'], t=d[k]['t'], vol=d[k]['volume']) for k in ('keyed_OCD', 'cap', 'middle', 'tet_dented', 'tet_notched', 'core', 'rest') if k in d}
kl = os.path.join(H, '..', 'data', 'step20-keyless-meshes.json')
k3 = {k: dict(v=x['v'], t=x['t'], vol=x['volume']) for k, x in json.load(open(kl)).items()} if os.path.exists(kl) else {}
el = os.path.join(H, '..', 'data', 'step23-envelope-meshes.json')
e4 = {k: dict(v=x['v'], t=x['t'], vol=x['volume']) for k, x in json.load(open(el)).items()} if os.path.exists(el) else {}
data = json.dumps(dict(p=keep, k=k3, e=e4, c=d['centres']), separators=(',', ':'))
html = open(os.path.join(H, 'step10_template.html')).read().replace('/*DATA*/', 'const D=' + data + ';')
open(os.path.join(H, '..', 'renders', 'step10-pieces.html'), 'w').write(html); print('ok', len(html))
