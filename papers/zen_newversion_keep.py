# New version of an existing Zenodo record (legacy deposit API, IPv4 only): replaces the files with the given PDF and applies a metadata edit.
#   python3 papers/zen_newversion.py <latest record id> <pdf> <metadata.json>
# Sets the PDF preview and runs the shared post-check itself (11-10).
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
API = 'https://zenodo.org/api/deposit/depositions'
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype})
    with urllib.request.urlopen(r, timeout=1800) as f:
        b = f.read(); return json.loads(b) if b else {}
rid, pdf, meta = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
nv = req(f'{API}/{rid}/actions/newversion', 'POST'); draft = req(nv['links']['latest_draft'])
for f in draft.get("files", []):
    if f["filename"].lower().endswith(".pdf"): req(f"{API}/{draft['id']}/files/{f['id']}", "DELETE")   # keep zips and other attachments
req(f"{draft['links']['bucket']}/{os.path.basename(pdf)}", 'PUT', raw=open(pdf, 'rb').read(), ctype='application/octet-stream')
req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta})
p = req(f"{API}/{draft['id']}/actions/publish", 'POST'); print('published', p['id'], p['doi'], p['links']['html'])
__import__('subprocess').run(stdin=__import__('subprocess').DEVNULL, args=[sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_preview.py'), str(p['id'])])   # PDF preview (11-10: was only a comment here; Yantra v4 went out without it)
__import__('subprocess').run(stdin=__import__('subprocess').DEVNULL, args=[sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_postcheck.py'), str(p['id'])])   # shared post-check (11-10)
__import__('subprocess').run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_community.py'), str(p['id'])])   # join communities/dicto
