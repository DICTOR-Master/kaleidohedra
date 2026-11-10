# Add "View in the app" to each record's description (DICTO 2026-10-27: Zenodo is where the readers are; give them a way into the app).
# Usage: zen_applink.py <links.json: {concept id: "world[:kind]"}>. Edits the latest version in place (edit -> PUT draft -> publish,
# the zen_preview.py pattern); skips a record whose description already links into the app.
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
for cid, open_ in json.load(open(sys.argv[1])).items():
    rid = req(f'https://zenodo.org/api/records/{cid}/versions/latest')['id']
    url = f'https://kaleidohedra.dictospheres.com/?open={open_}'
    if 'kaleidohedra.dictospheres.com/?open=' in req(f'https://zenodo.org/api/records/{rid}')['metadata'].get('description', ''):
        print(cid, rid, 'already links into the app'); continue   # checked before opening an edit draft, so none is left open
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    desc = d['metadata'].get('description', '')
    d['metadata']['description'] = desc + f'<p>View in the app: <a href="{url}">{url}</a></p>'
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
    print(cid, rid, 'ok' if url in p['metadata']['description'] else 'NOT SAVED', url, flush=True)

# shared post-check (11-10) over every record this run touched
import subprocess as _sp
_ids = [a for a in sys.argv[1:] if a.isdigit()]
if _ids and os.path.basename(__file__) == 'zen_preview.py': _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_postcheck.py')] + _ids)
