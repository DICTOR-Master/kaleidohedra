# Packet screen 2026-11-21, step 5: tables for the README (data/table.md, data/leads.json) from data/packets.json.
# Light: reads JSON only.
import os, json
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(HERE, 'data', 'packets.json')))
pieces = json.load(open(os.path.join(HERE, 'data', 'pieces.json')))
angles = json.load(open(os.path.join(HERE, 'data', 'angles.json')))
rel = json.load(open(os.path.join(HERE, 'data', 'relations.json')))
byid = {p['id']: p for p in pieces}
akey = {(o[0], o[1], tuple(o[2])): a['id'] for a in angles for o in a['occurs']}
expr = {b: {b: Fr(1)} for b in rel['basis']}
for r in rel['relations']:
    R = {int(k) if k != 'pi' else k: v for k, v in r['relation'].items()}; a = r['angle']
    expr[a] = {b: Fr(-v, R[a]) for b, v in R.items() if b not in ('pi', a)}

def nice(pid):
    p = byid[pid]; s = p['solid'].replace('_', ' ')
    if p['kind'] == 'solid': return s
    poly = {3: 'triangle', 4: 'square' if p['family'] in ('Platonic', 'Archimedean') else 'quadrilateral', 5: 'pentagon', 6: 'hexagon', 8: 'octagon', 10: 'decagon'}[p['face_sides']]
    if p['family'] == 'Catalan':
        poly = {3: 'triangle', 4: 'kite' if 'deltoidal' in s else 'rhombus', 5: 'pentagon'}[p['face_sides']]
    return f'{s} {poly} pyramid'

def irr_angles(pid):
    p = byid[pid]; out = set()
    for e in p['edges']:
        a = akey[(p['field'], e[2], tuple(e[3]))]
        if not angles[a]['rational']: out.add(a)
    return out

def complements(pid, hid):
    """pairs (theta in P, theta' in H) with theta + theta' a rational multiple of pi (exact, from the proved relations)"""
    n = 0
    for a in irr_angles(pid):
        for b in irr_angles(hid):
            s = dict(expr[a])
            for k, v in expr[b].items(): s[k] = s.get(k, 0) + v
            if all(v == 0 for v in s.values()): n += 1
    return n

def trivial(pid, hid):
    p, h = byid[pid], byid[hid]
    if h['kind'] == 'pyramid' and h['solid'] == p['solid']: return 'sibling pyramid (same solid)'
    if h['kind'] == 'solid' and h['id'] == p['solid']: return 'its own solid'
    return ''

ORDER = []
for p in pieces:
    if p['kind'] == 'pyramid': ORDER.append(p['id'])
S = D['screen']
lines = ['| centre pyramid | faces | packet | cancelling helpers (free scale), best edge-matched proportion pyramid:helper |', '|---|---|---|---|']
leads = []; leads2 = []; counts = {'zero': 0, 'one': 0, 'two': 0, 'none': 0}
for pid in ORDER:
    r = S[pid]; p = byid[pid]
    if r['zero']:
        counts['zero'] += 1
        lines.append(f"| {nice(pid)} | {p['face_count']} | **zero** (fills alone as far as Dehn can tell) | not needed |"); continue
    hs = r['one_helper']
    if hs:
        counts['one'] += 1; parts = []
        for h in hs:
            pr = h['proportions']; tag = trivial(pid, h['helper'])
            prs = f"{pr[0]['n']}:{pr[0]['m']}" if pr else f"scale-dependent (mu = {h['mu']:.6g})"
            ex = '' if h['exact'] else (' [cross-field: numerical only]' if h['cross_field'] else ' [numerical]')
            parts.append(f"{nice(h['helper'])} {prs}{' (' + tag + ')' if tag else ''}{ex}")
            leads.append({'pyramid': pid, 'helper': h['helper'], 'exact': h['exact'], 'mu': h['mu'], 'proportions': pr[:3], 'trivial': tag,
                          'complements': complements(pid, h['helper']), 'helper_faces': byid[h['helper']].get('faces', byid[h['helper']].get('face_sides'))})
        lines.append(f"| {nice(pid)} | {p['face_count']} | nonzero, {len(r['support'])} basis angle(s) | {len(hs)}: " + '; '.join(parts) + ' |')
    elif r['two_helpers']:
        counts['two'] += 1; t = r['two_helpers']
        ex = sum(1 for x in t if x['exact'])
        best = sorted(t, key=lambda x: sum(byid[h].get('faces', byid[h].get('face_sides', 0)) for h in x['helpers']))[:4]
        lines.append(f"| {nice(pid)} | {p['face_count']} | nonzero, {len(r['support'])} basis angle(s) | no single helper; {len(t)} two-helper sets ({ex} exact), e.g. " +
                     '; '.join(' + '.join(nice(h) for h in x['helpers']) + (f" {x['proportion'][0]}:{x['proportion'][1]}:{x['proportion'][2]}" if x.get('proportion') else f" (scale-dependent: a = {x['a'][0]:.4g}, {x['a'][1]:.4g})") for x in best) + ' |')
        for x in t:
            leads2.append({'pyramid': pid, 'helpers': x['helpers'], 'exact': x['exact'], 'proportion': x.get('proportion'), 'a': x['a'],
                           'trivial': ', '.join(filter(None, [trivial(pid, h) for h in x['helpers']]))})
    else:
        counts['none'] += 1
        lines.append(f"| {nice(pid)} | {p['face_count']} | nonzero, {len(r['support'])} basis angle(s) | none in the library (needs basis independence: numerical) |")

def score(l):
    pr = l['proportions']; s = (0 if l['exact'] else 100) + (50 if l['trivial'] else 0)
    s += (pr[0]['n'] + pr[0]['m']) if pr else 40
    s -= 3 * l['complements']
    return s
leads.sort(key=score)
open(os.path.join(HERE, 'data', 'table.md'), 'w').write('\n'.join(lines) + '\n')
json.dump({'counts': counts, 'leads': leads, 'two_helper': leads2}, open(os.path.join(HERE, 'data', 'leads.json'), 'w'), indent=1)
print(counts)
for l in leads[:40]:
    pr = l['proportions']
    print(f"{nice(l['pyramid'])} + {nice(l['helper'])}: " + (f"{pr[0]['n']}:{pr[0]['m']} (edges {pr[0]['P_edge']:.4f}={pr[0]['H_edge']:.4f} scaled)" if pr else f"mu={l['mu']:.5g}") +
          f"; complements {l['complements']}{'; ' + l['trivial'] if l['trivial'] else ''}{'' if l['exact'] else ' NUMERICAL'}")
print('--- two-helper sets, non-trivial (no sibling pyramid / own solid), exact:')
for x in leads2:
    if x['exact'] and not x['trivial']:
        print(f"{nice(x['pyramid'])} + {nice(x['helpers'][0])} + {nice(x['helpers'][1])}: " + (':'.join(map(str, x['proportion'])) if x['proportion'] else f"a = {x['a'][0]:.5g}, {x['a'][1]:.5g} (irrational at canonical scale)"))
ok1 = sum(counts.values()) == len(ORDER) == 47
ok2 = all(l['exact'] for l in leads) and all(x['exact'] for x in leads2)
print(('ok   ' if ok1 else 'FAIL ') + 'every one of the 47 centre pyramids is in exactly one row'); print(('ok   ' if ok2 else 'FAIL ') + 'every cancellation listed is proved exactly')
print('FINAL ok' if (ok1 and ok2) else 'FINAL FAIL')
