# Set each record's default_preview to its dicto-*.pdf (DICTO 2026-10-17 rule): edit -> PUT draft -> publish (InvenioRDM API).
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
for rid in sys.argv[1:]:
    r = req(f'https://zenodo.org/api/records/{rid}')
    pdf = [k for k in r['files']['entries'] if k.startswith('dicto-') and k.endswith('.pdf')][0]
    if r['files'].get('default_preview') == pdf: print(rid, 'already', pdf); continue
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    d['files']['default_preview'] = pdf
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST'); print(rid, 'preview ->', p['files'].get('default_preview'))
