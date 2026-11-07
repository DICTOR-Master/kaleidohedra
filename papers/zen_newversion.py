# New version of an existing Zenodo record (legacy deposit API, IPv4 only): replaces the files with the given PDF and applies a metadata edit.
#   python3 papers/zen_newversion.py <latest record id> <pdf> <metadata.json>
# Afterwards: python3 papers/zen_preview.py <new record id>
import json, urllib.request, socket, os, sys
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
API = 'https://zenodo.org/api/deposit/depositions'
# NATIVE-REVIEW GUARD (DICTO 11-07: a reader found the Japanese Quanta "reads like machine translation"). A record in a language other
# than English is only released with <folder>/native-review.json {"reviewer": ..., "date": ..., "verdict": "ok"} from a native reader.
def _native_guard(meta, folder):
    lang = meta.get('language', 'eng')
    if lang in ('eng', 'en'): return
    f = os.path.join(folder, 'native-review.json')
    ok = os.path.exists(f) and json.load(open(f)).get('verdict') == 'ok' and json.load(open(f)).get('reviewer')
    if not ok: sys.exit(f"GUARD: language {lang} needs {f} with a native reader's verdict ok - not released")
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype})
    with urllib.request.urlopen(r, timeout=1800) as f:
        b = f.read(); return json.loads(b) if b else {}
rid, pdf, meta = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
_native_guard(meta, os.path.dirname(os.path.abspath(sys.argv[3])))
nv = req(f'{API}/{rid}/actions/newversion', 'POST'); draft = req(nv['links']['latest_draft'])
for f in draft.get('files', []): req(f"{API}/{draft['id']}/files/{f['id']}", 'DELETE')
req(f"{draft['links']['bucket']}/{os.path.basename(pdf)}", 'PUT', raw=open(pdf, 'rb').read(), ctype='application/octet-stream')
req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta})
p = req(f"{API}/{draft['id']}/actions/publish", 'POST'); print('published', p['id'], p['doi'], p['links']['html'])
__import__('subprocess').run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zen_community.py'), str(p['id'])])   # join communities/dicto
