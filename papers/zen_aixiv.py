# Link a Zenodo record to its aiXiv copy (DICTO 2026-11-12: "yes do 1"): adds related identifier https://aixiv.online/abs/<id>,
# relation "is identical to", type preprint, on the LATEST version, in place (edit -> PUT draft -> publish, the zen_preview.py pattern;
# no new version, no new DOI). Skips a record that already carries the link (checked before opening a draft).
# Usage: zen_aixiv.py <zenodo id (concept or record)>=<aixiv id> ...
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
ok = True
for arg in sys.argv[1:]:
    zid, aid = arg.split('='); url = f'https://aixiv.online/abs/{aid}'
    rid = req(f'https://zenodo.org/api/records/{zid}/versions/latest')['id']
    cur = req(f'https://zenodo.org/api/records/{rid}')['metadata'].get('related_identifiers', [])
    if any(x.get('identifier') == url for x in cur): print(zid, rid, 'already linked', url); continue
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    ri = d['metadata'].setdefault('related_identifiers', [])
    ri.append({'identifier': url, 'scheme': 'url', 'relation_type': {'id': 'isidenticalto'}, 'resource_type': {'id': 'publication-preprint'}})
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
    got = [x for x in p['metadata'].get('related_identifiers', []) if x.get('identifier') == url]
    n_before, n_after = len(cur), len(p['metadata'].get('related_identifiers', []))
    good = bool(got) and n_after == n_before + 1
    ok &= good
    print(zid, rid, 'ok' if good else 'NOT SAVED', url, f'related {n_before} -> {n_after}', flush=True)
import subprocess as _sp
_sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_postcheck.py')] + [a.split('=')[0] for a in sys.argv[1:]])
print('FINAL ok' if ok else 'FINAL FAIL')
