# Add a published Zenodo record to the DICTO community (communities/dicto) and accept the request (DICTO 2026-10-29: nine
# records published since #67 were never added). Called by zen_new.py and zen_newversion.py after every publish.
#   python3 papers/zen_community.py <record id>
import json, os, socket, sys, urllib.request, urllib.error
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
COMMUNITY = 'f635b013-5631-43da-a274-1ac3440309ed'   # communities/dicto
def req(u, method='GET', body=None):
    r = urllib.request.Request(u, method=method, data=json.dumps(body).encode() if body is not None else None,
                               headers={'Authorization': f'Bearer {T}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=90) as f:
            b = f.read(); return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        return {'HTTP': e.code, 'body': e.read().decode()[:300]}
def add(rid):
    r = req(f'https://zenodo.org/api/records/{rid}/communities', 'POST', {'communities': [{'id': COMMUNITY}]})
    out = []
    for it in r.get('processed', []):
        rq, st = it.get('request_id') or (it.get('request') or {}).get('id'), (it.get('request') or {}).get('status')
        if rq and st != 'accepted':
            st = req(f'https://zenodo.org/api/requests/{rq}/actions/accept', 'POST', {}).get('status')
        out.append(st)
    if not out:   # already a member comes back as an error on the record, not a request
        out = [str(r.get('errors') or r)[:160]]
    print('community dicto:', rid, ', '.join(map(str, out)))
if __name__ == '__main__':
    add(sys.argv[1])
