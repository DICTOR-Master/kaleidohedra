# New version of an existing Zenodo record with SEVERAL files (legacy deposit API, IPv4 only), e.g. a Lean archive zip plus
# a README for display. zen_newversion.py is PDF-centric (one PDF first, then zen_preview.py picks the PDF); this one keeps
# no inherited file, uploads the given files in the order given, sets --preview (default: the first file) as the default
# preview through the InvenioRDM draft API, publishes, and then checks each published file's md5 against the local bytes.
#   python3 papers/zen_newversion_files.py <latest record id> <metadata.json> [--preview NAME] FILE [FILE ...]
# metadata.json is the legacy metadata dict (no doi / prereserve_doi). Afterwards it joins communities/dicto and runs
# zen_postcheck.py. Written 2026-11-24 for the Yantra Lean archive (zip of 1386 files is over Zenodo's 1000-file preview).
import json, urllib.request, socket, os, sys, hashlib, subprocess
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
API = 'https://zenodo.org/api/deposit/depositions'
RDM = 'https://zenodo.org/api/records'
HERE = os.path.dirname(os.path.abspath(__file__))
def req(url, method='GET', body=None, raw=None, ctype='application/json', accept='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype, 'Accept': accept})
    with urllib.request.urlopen(r, timeout=1800) as f:
        b = f.read(); return json.loads(b) if b else {}
args = sys.argv[1:]; preview = None
if '--preview' in args: i = args.index('--preview'); preview = args[i + 1]; del args[i:i + 2]
rid, meta, files = args[0], json.load(open(args[1])), args[2:]
if not files: sys.exit('no files given')
preview = preview or os.path.basename(files[0])
if preview not in [os.path.basename(f) for f in files]: sys.exit(f'--preview {preview} is not among the files')
md5 = {os.path.basename(f): hashlib.md5(open(f, 'rb').read()).hexdigest() for f in files}
nv = req(f'{API}/{rid}/actions/newversion', 'POST'); draft = req(nv['links']['latest_draft'])
for f in draft.get('files', []): req(f"{API}/{draft['id']}/files/{f['id']}", 'DELETE')   # inherited files out; re-uploaded below
for up in files:   # in the given order (the first is the fallback preview if default_preview cannot be set)
    req(f"{draft['links']['bucket']}/{os.path.basename(up)}", 'PUT', raw=open(up, 'rb').read(), ctype='application/octet-stream')
req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta})
rdm = 'application/vnd.inveniordm.v1+json'
d = req(f"{RDM}/{draft['id']}/draft", accept=rdm); d['files']['default_preview'] = preview
req(f"{RDM}/{draft['id']}/draft", 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d}, accept=rdm)
p = req(f"{RDM}/{draft['id']}/draft/actions/publish", 'POST', accept=rdm)
print('published', p['id'], p['pids']['doi']['identifier'], p['links']['self_html'], 'preview ->', p['files'].get('default_preview'))
r = req(f"{RDM}/{p['id']}", accept=rdm); bad = 0
for k, e in r['files']['entries'].items():
    ok = e['checksum'] == f'md5:{md5.get(k)}'; bad += not ok; print('md5', 'match' if ok else 'MISMATCH', k, e['checksum'])
if set(r['files']['entries']) != set(md5): bad += 1; print('FILE SET DIFFERS', sorted(r['files']['entries']), sorted(md5))
subprocess.run([sys.executable, os.path.join(HERE, 'zen_community.py'), str(p['id'])], stdin=subprocess.DEVNULL)   # join communities/dicto
subprocess.run([sys.executable, os.path.join(HERE, 'zen_postcheck.py'), str(p['id'])], stdin=subprocess.DEVNULL)   # shared post-check (11-10)
sys.exit(1 if bad else 0)
