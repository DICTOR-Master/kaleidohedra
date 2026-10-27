# Japanese versions (DICTO 2026-10-27): collect title + description of every published DICTO record (latest versions) -> records.json
import json, urllib.request, urllib.parse, socket, os, re, html
o = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in o(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
out = []
for page in range(1, 6):
    u = 'https://zenodo.org/api/deposit/depositions?' + urllib.parse.urlencode({'size': 100, 'page': page})
    D = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + T}), timeout=120))
    for h in D:
        if not h.get('submitted'): continue
        m = h['metadata']; txt = re.sub(r'<[^>]+>', ' ', m.get('description', '')); txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()
        out.append({'id': h['id'], 'concept': h.get('conceptrecid'), 'doi': m.get('doi'), 'title': m['title'], 'type': m.get('upload_type'),
                    'version': m.get('version'), 'description': txt})
    if len(D) < 100: break
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'records.json'), 'w'), ensure_ascii=False, indent=1)
print(len(out), 'records'); [print(r['id'], r['type'], r['title'][:80]) for r in out[:80]]
