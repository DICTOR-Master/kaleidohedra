# Zenodo SOFTWARE drafts for the Palomar-registered Lean repos (legacy deposit API, IPv4 only), same pattern as papers/zen_new.py.
#   python3 zen_software.py reserve <meta-REPO.json>   -> draft with reserved DOI, zip uploaded, metadata set; NOT published
#   python3 zen_software.py publish <meta-REPO.json>   -> refreshes metadata, publishes, joins communities/dicto (only on DICTO's word)
# Zips come from https://github.com/DICTOR-Master/<repo>/archive/<commit>.zip into work/ (git-ignored).
import json, urllib.request, urllib.error, socket, os, sys, subprocess
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
API = 'https://zenodo.org/api/deposit/depositions'
HERE = os.path.dirname(os.path.abspath(__file__))
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype})
    try:
        with urllib.request.urlopen(r, timeout=250) as f: return json.load(f)
    except urllib.error.HTTPError as e: sys.exit(f'HTTP {e.code}: {e.read().decode()[:800]}')
cmd, mf = sys.argv[1], sys.argv[2]; M = json.load(open(mf))
state = os.path.join(HERE, f"state-{M['repo']}.json")
if cmd == 'reserve':
    if os.path.exists(state): sys.exit('already reserved: ' + open(state).read())
    d = req(API, 'POST', {'metadata': dict(M['metadata'], prereserve_doi=True)})
    s = dict(id=d['id'], doi=d['metadata']['prereserve_doi']['doi'], conceptrecid=d['conceptrecid'], bucket=d['links']['bucket'],
             edit=f"https://zenodo.org/uploads/{d['id']}", published=False)
    json.dump(s, open(state, 'w'), indent=1)
    zp = os.path.join(HERE, 'work', M['zip'])
    req(f"{s['bucket']}/{M['zip']}", 'PUT', raw=open(zp, 'rb').read(), ctype='application/octet-stream')
    print(json.dumps(s))
elif cmd == 'publish':
    s = json.load(open(state))
    req(f"{API}/{s['id']}", 'PUT', {'metadata': dict(M['metadata'], prereserve_doi=True)})
    p = req(f"{API}/{s['id']}/actions/publish", 'POST')
    s.update(published=True, doi=p['doi']); json.dump(s, open(state, 'w'), indent=1); print('published', p['doi'], p['links']['html'])
    subprocess.run([sys.executable, os.path.expanduser('~/k-research/papers/zen_community.py'), str(p['id'])], stdin=subprocess.DEVNULL)
