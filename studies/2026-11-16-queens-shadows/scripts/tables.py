#!/usr/bin/env python3
"""Print the README tables from data/shadows.json (no new computation). Usage: tables.py data/shadows.json"""
import sys, json
from collections import Counter, defaultdict
js = json.load(open(sys.argv[1]))
def t(d): return ' + '.join(f'{v} {k}' for k, v in sorted(d.items())) if d else '-'
def nm(L): return L['name'].split(' (')[0]
for s in js['shadows']:
    print(f"\n### {'White' if s['queen'] == '600' else 'Red'} Queen, {s['direction']}: {s['walls']['mirror']} mirrors + {s['walls']['cross']} cross walls; "
          f"group on the shadow of order {s['group_on_shadow']}")
    print('plane orbits: ' + '; '.join(f"{o['planes']} {o['kind']} (normal-line stabiliser {o['normal_line_stabiliser']})" for o in s['plane_orbits']))
    print('\n| outline | heights | shape | edges | fins (shadow centre) | verdict | own centre |')
    print('|---|---|---|---|---|---|---|')
    groups = defaultdict(list)
    for L in s['layers']:
        key = (L['name'], L['edges'], json.dumps(L['plates_O'], sort_keys=True), L['verdict_O'], json.dumps(L['own'], sort_keys=True))
        groups[key].append(L['height'])
    for (name, ne, po, v, own), hs in groups.items():
        if ne == 0: continue
        o = json.loads(own)
        print(f"| layer | {', '.join(hs)} | {name} | {ne} | {t(json.loads(po))} | {v} | {(t(o['plates']) + ' -> ' + o['verdict']) if o else 'same (centred)'} |")
    H = s['hull']
    print(f"| hull | all | {H['name']} | {H['edges']} | {t(H['plates_O'])} | {H['verdict_O']} | same (centred) |")
    print(f"\nhull faces parallel to kept walls: {t(H.get('faces_parallel_to_kept_walls', {}))}")
    print(f"\ncells: {t(s['side_counts'])}; {s['cell_orbits']} orbits, {s['cell_classes']} congruence classes ({s['front_classes']} among front cells)")
    print('\n| class | cells | front/back/side-on | fins at shadow centre | verdict | fins at own centre | verdict | own fins in a wall |')
    print('|---|---|---|---|---|---|---|---|')
    by = defaultdict(list)
    for r in s['cells']: by[r['class']].append(r)
    for c in sorted(by):
        rs = by[c]; n = sum(r['orbit_size'] for r in rs); sd = Counter()
        for r in rs: sd.update(r['sides'])
        vs = Counter((json.dumps(r['plates_O'], sort_keys=True), r['verdict_O'], json.dumps(r['plates_own'], sort_keys=True), r['verdict_own'], r['own_fins_in_wall']) for r in rs)
        for (po, vo, pw, vw, iw), k in vs.items():
            print(f"| {c} | {n} | {sd.get('front', 0)}/{sd.get('back', 0)}/{sd.get('side-on', 0)} | {t(json.loads(po))} | {vo} | {t(json.loads(pw))} | {vw} | {iw} |")
print('\nLATTICE', json.dumps({k: js[k] for k in ('wall_contains_lines', 'walls_reached_by_type', 'shadow_graph_components', 'wall_graph_components', 'turnings')}))
print('SHARED', json.dumps(js['shared_walls_pairs']))
