# Fix banned wording in published Zenodo descriptions (DICTO 2026-11-10: "yes fix the zenodo descriptions"). Metadata only: the latest
# version is edited in place (edit -> PUT draft -> publish, the zen_applink.py pattern); no new version, files untouched.
# Usage: zen_fixdesc.py --dry | --apply.  Automatic rewrite: the 'In short.' label is removed (with any <b>/<strong> around it).
# Any other banned hit is listed as MANUAL with its context and the record is left alone (use MANUAL_FIXES below).
import json, urllib.request, socket, os, sys, re, glob, time
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
P = os.path.dirname(os.path.abspath(__file__))
BAN = re.compile(re.search(r'const BAN = /(.*?)/gi;', open(f'{P}/print.mjs').read()).group(1), re.I)
LABEL = re.compile(r'(<(b|strong|em|i)>\s*)?\bIn short\s*[:.]\s*(</(b|strong|em|i)>\s*)?', re.I)
MANUAL_FIXES = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}      # {"old text": "new text"}
apply = '--apply' in sys.argv; seen = set(); changed = manual = 0
for st in sorted(glob.glob(f'{P}/**/zenodo-state.json', recursive=True)):
    try: c = json.load(open(st)).get('conceptrecid')
    except Exception: continue
    if not c or c in seen: continue
    seen.add(c)
    rid = req(f'https://zenodo.org/api/records/{c}/versions/latest')['id']
    desc = req(f'https://zenodo.org/api/records/{rid}')['metadata'].get('description', '')
    new = LABEL.sub('', desc)
    for a, b in MANUAL_FIXES.items(): new = new.replace(a, b)
    left = [new[max(0, m.start() - 80):m.end() + 80] for m in BAN.finditer(re.sub(r'<[^>]+>', ' ', new))]
    if new == desc and not left: continue
    name = os.path.relpath(os.path.dirname(st), P)
    if left:
        manual += 1; print(f'MANUAL {rid} {name}: ' + ' || '.join(left)); continue
    i = next(k for k in range(len(desc)) if k >= len(new) or desc[k] != new[k])
    print(f'{"FIX" if apply else "WOULD FIX"} {rid} {name}: …{desc[max(0, i - 40):i + 60]}…  ->  …{new[max(0, i - 40):i + 60]}…', flush=True)
    if apply:
        d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST'); d['metadata']['description'] = new
        req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
        p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
        okk = not BAN.search(re.sub(r'<[^>]+>', ' ', p['metadata']['description'])); print('   saved' if okk else '   NOT SAVED', flush=True)
        changed += okk
    time.sleep(0.3)
print(f'{"changed" if apply else "would change"}: {changed if apply else "see above"}; manual: {manual}')
print('FINAL ok' if manual == 0 else 'FINAL FAIL: manual fixes needed')
