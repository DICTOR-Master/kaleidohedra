# SA batch inventory: for each published DICTO paper (concept DOI from its source), the latest Zenodo record, version, licence, title.
import json, re, socket, urllib.request, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
K = sys.argv[1]
src = {}
for p in sorted(__import__('glob').glob(K + '/papers/**/paper.html', recursive=True)) + [K + '/papers/collected/collected.html',
        K + '/studies/2026-10-13-fused-shells/paper/build_house.py', K + '/studies/2026-10-14-axe-cleo-fuji/paper/build_house.py', K + '/studies/2026-10-14-fuji-family/paper/build_house.py']:
    if '/figures' in p: continue
    t = open(p).read(); m = re.search(r'(?:Version \d+[^\n]*?)zenodo\.(\d+)', t)
    src[p.replace(K + '/', '')] = m.group(1) if m else None
out = []
for p, d in src.items():
    if not d: print('NO DOI', p); continue
    try:
        with urllib.request.urlopen(f'https://zenodo.org/api/records/{d}/versions/latest', timeout=60) as f: r = json.load(f)
    except Exception as e:
        try:
            with urllib.request.urlopen(f'https://zenodo.org/api/records/{d}', timeout=60) as f: r0 = json.load(f)
            with urllib.request.urlopen(f"https://zenodo.org/api/records/{r0['conceptrecid']}/versions/latest", timeout=60) as f: r = json.load(f)
        except Exception as e2: print('ERR', p, d, e2); continue
    md = r['metadata']; out.append(dict(src=p, doi_in_src=d, concept=r['conceptrecid'], latest=r['id'], version=md.get('version'),
        license=(md.get('license') or {}).get('id') if isinstance(md.get('license'), dict) else md.get('license'), title=md['title'], date=md.get('publication_date')))
    print(f"{r['id']:>9} concept {r['conceptrecid']:>9} v{md.get('version')!s:6} {out[-1]['license']!s:10} {md['title'][:60]}  <- {p}")
json.dump(out, open('sa-batch/inventory.json', 'w'), indent=1); print(len(out), 'records')
