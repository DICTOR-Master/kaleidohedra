# New Zenodo record for a paper (legacy deposit API, IPv4 only). Two steps, so the DOI can be printed into the PDF first:
#   python3 papers/zen_new.py reserve <folder>                      -> <folder>/zenodo-state.json (draft id, record DOI, concept DOI)
#   python3 papers/zen_new.py publish <folder> <pdf> <metadata.json> -> uploads the PDF, sets metadata, publishes
# Afterwards: python3 papers/zen_preview.py <record id>   (PDF preview; DICTO rule)
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
API = 'https://zenodo.org/api/deposit/depositions'
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype})
    with urllib.request.urlopen(r, timeout=300) as f: return json.load(f)
cmd, folder = sys.argv[1], sys.argv[2]; state = os.path.join(folder, 'zenodo-state.json')
if cmd == 'reserve':
    if os.path.exists(state): sys.exit('already reserved: ' + open(state).read())
    d = req(API, 'POST', {})
    s = dict(id=d['id'], doi=d['metadata']['prereserve_doi']['doi'], conceptrecid=d['conceptrecid'], bucket=d['links']['bucket'], published=False)
    json.dump(s, open(state, 'w')); print(json.dumps(s))
elif cmd == 'publish':
    s = json.load(open(state)); pdf, meta = sys.argv[3], json.load(open(sys.argv[4]))
    name = os.path.basename(pdf)
    req(f"{s['bucket']}/{name}", 'PUT', raw=open(pdf, 'rb').read(), ctype='application/octet-stream')
    req(f"{API}/{s['id']}", 'PUT', {'metadata': meta})
    p = req(f"{API}/{s['id']}/actions/publish", 'POST')
    s.update(published=True, doi=p['doi']); json.dump(s, open(state, 'w')); print('published', p['doi'], 'concept', p['conceptdoi'], p['links']['html'])
    __import__('subprocess').run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_community.py'), str(p['id'])])   # join communities/dicto
