# Book/catalogue check (DICTO: "check the book catalogues for the Ogdoecontahedron"). Scans every solid on David McCooey's Visual
# Polyhedra (dmccooey.com/polyhedra, every category page linked from the index): parses each embedded vertex and face list, counts
# V, E, F and face sizes, and tests any solid with the OCD's counts (or its dual's) for the same face arrangement with the exact
# map-isomorphism search of ocd_dl0d.py. Pages are fetched once into a cache folder (read-only use; nothing redistributed).
import re, os, sys, json, subprocess, collections
CACHE = sys.argv[1]; BASE = 'https://dmccooey.com/polyhedra/'
def get(name):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p): subprocess.run(['curl', '-4', '-s', '-o', p, BASE + name], check=True)
    return open(p, encoding='latin-1').read()
idx = get('index.html')
pages = sorted(set(re.findall(r"href=['\"]?([A-Za-z0-9]+\.html)", idx) + re.findall(r"location\.href='([A-Za-z0-9]+\.html)'", idx)) - {'index.html'})
more = set()
for pg in pages:
    s = get(pg); more |= set(re.findall(r"location\.href='([A-Za-z0-9]+Page\d\.html)'", s))
pages = sorted(set(pages) | more)
solids = []; seen = set()
for pg in pages:
    s = get(pg)
    for m in re.finditer(r"<!--\s*\n\s*([^\n]+?)\s*\n(.*?)class=Vertices value=\"(.*?)\">\s*<INPUT type=hidden class=Faces value=\"(.*?)\">", s, re.S):
        name = m.group(1).strip()
        if name in seen: continue
        seen.add(name); fs = [list(map(int, re.findall(r'-?\d+', f.split('#')[0]))) for f in m.group(4).replace('\n', ' ').split(',') if f.strip()]
        fs = [f for f in fs if len(f) >= 3]
        V = len({v for f in fs for v in f}); E = sum(len(f) for f in fs) // 2
        solids.append((pg, name, V, E, len(fs), dict(sorted(collections.Counter(len(f) for f in fs).items())), fs))
exec(open('scripts/ocd_dl0d.py').read().split('# controls:')[0].replace("print('\\n'.join(out)); open('data/ocd-dl0d.txt', 'w').write('\\n'.join(out) + '\\n')", ''))
target = (102, 180, 80); dtarget = (80, 180, 102)
hits = [s for s in solids if (s[2], s[3], s[4]) in (target, dtarget)]
out = [f'McCooey Visual Polyhedra: {len(pages)} pages scanned, {len(solids)} solids parsed (all names: data/ocd-catalogue-names.txt)',
       f'solids with the OCD counts (V 102, E 180, F 80) or its dual\'s (V 80, E 180, F 102): {len(hits)}']
for pg, name, V, E, F, fz, fs in hits:
    mine = OFo if (V, E, F) == target else dual(OFo)
    out.append(f'  {name} ({pg}): V {V}, E {E}, F {F}, faces {fz}; same face arrangement: {iso(mine, fs)}')
near = sorted([s for s in solids if s[3] == 180], key=lambda s: s[1])
out.append(f'all solids with 180 edges ({len(near)}): ' + '; '.join(f'{s[1]} [V{s[2]} F{s[4]} {s[5]}]' for s in near))
print('\n'.join(out)); open('data/ocd-catalogue.txt', 'w').write('\n'.join(out) + '\n')
open('data/ocd-catalogue-names.txt', 'w').write('\n'.join(f'{s[0]}\t{s[1]}\tV{s[2]} E{s[3]} F{s[4]}' for s in solids) + '\n')
# control: the parser and the test on known pairs (expect True, True, False)
S = {s[1]: s[6] for s in solids}
c1 = iso(S['Truncated Icosahedron'], dual(S['Pentakis Dodecahedron'])); c2 = iso(S['Icosidodecahedron'], dual(S['Rhombic Triacontahedron']))
c3 = iso(S['Truncated Icosahedron'], dual(S['Triakis Icosahedron']))
ctl = f'controls: truncated icosahedron = dual of pentakis dodecahedron {c1}; icosidodecahedron = dual of rhombic triacontahedron {c2}; truncated icosahedron = dual of triakis icosahedron {c3} (expect True, True, False)'
print(ctl); open('data/ocd-catalogue.txt', 'a').write(ctl + '\n')
