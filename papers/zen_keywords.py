# Replace the keywords (subjects) of the latest version of each record in place (DICTO 11 Nov: field terms instead of personal names,
# so researchers in the field find the papers). Usage: zen_keywords.py <keywords.json: {concept id: [keywords]}>. Pattern of zen_applink.py.
import json, urllib.request, socket, os, sys, subprocess
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
done = []
for cid, kws in json.load(open(sys.argv[1])).items():
    rid = req(f'https://zenodo.org/api/records/{cid}/versions/latest')['id']
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    keep = [s for s in d['metadata'].get('subjects', []) if 'id' in s or str(s.get('subject', '')).startswith('MSC')]   # keep MSC classes
    d['metadata']['subjects'] = keep + [{'subject': k} for k in kws]
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
    got = [s.get('subject') for s in p['metadata'].get('subjects', [])]
    print(cid, rid, 'ok' if all(k in got for k in kws) else 'NOT SAVED', len(got), 'subjects', flush=True); done.append(str(rid))
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_postcheck.py')] + done)
