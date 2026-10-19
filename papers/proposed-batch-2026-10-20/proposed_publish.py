# "DICTO proposed" batch publish (only after DICTO's OK): new Zenodo version of each paper, the paper PDF replaced (same name), all other
# files kept; the description gets the same old -> new pairs; licence stays cc-by-sa-4.0.  python3 proposed_publish.py [--dry]
import json, os, sys, time, socket, urllib.request, html as H
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
sys.path.insert(0, sys.argv[1]); from edits import EDITS
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip(); API = 'https://zenodo.org/api/deposit/depositions'; dry = '--dry' in sys.argv
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype}), timeout=300) as f:
                b = f.read(); return json.loads(b) if b else {}
        except urllib.error.HTTPError as e:
            if e.code < 500: raise RuntimeError(f'{method} {url}: {e.code} {e.read()[:300]}')
            err = e
        except Exception as e: err = e
        time.sleep(5 * (k + 1))
    raise err
NOTE = "Version {v} (20 October 2026): DICTO's ideas are now credited as his proposals (\"DICTO proposed …\" in place of \"DICTO asked …\"); the results are unchanged."
plan = json.load(open('plan-proposed.json')); done = json.load(open('published-proposed.json')) if os.path.exists('published-proposed.json') else {}
for r in plan:
    if r['src'] in done: print('skip', r['src']); continue
    f = r['src'].split('/')[1]; pdf = [x for x in os.listdir('newp') if x.startswith(r['concept'] + '-')]; assert len(pdf) == 1, f
    name = pdf[0].split('-', 1)[1]; meta = req(f"{API}/{r['latest']}")['metadata']; d = meta['description']; hits = 0
    for a, b in EDITS[f]:
        for A, Bb in ((a, b), (H.escape(a, quote=False), H.escape(b, quote=False)), (H.escape(a), H.escape(b))):
            if A in d: d = d.replace(A, Bb); hits += 1; break
    left = d.count('DICTO asked'); meta['description'] = d
    meta['version'] = str(r['new_version']); meta['publication_date'] = '2026-10-20'; meta['notes'] = NOTE.format(v=r['new_version'])
    assert meta['license'] in ('cc-by-sa-4.0', {'id': 'cc-by-sa-4.0'}) or 'cc-by-sa' in json.dumps(meta['license']), f
    meta.pop('doi', None); meta.pop('prereserve_doi', None)
    print(f"{'DRY ' if dry else ''}{f}: description edits {hits}, 'DICTO asked' left {left}, file {name}, v{meta['version']}")
    if dry: continue
    assert left == 0, f
    nv = req(f"{API}/{r['latest']}/actions/newversion", 'POST'); draft = req(nv['links']['latest_draft'])
    files = draft.get('files', []); hit = [x for x in files if x['filename'] == name]; assert len(hit) == 1, (f, [x['filename'] for x in files])
    req(f"{API}/{draft['id']}/files/{hit[0]['id']}", 'DELETE')
    req(f"{draft['links']['bucket']}/{name}", 'PUT', raw=open(os.path.join('newp', pdf[0]), 'rb').read(), ctype='application/octet-stream')
    req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta}); p = req(f"{API}/{draft['id']}/actions/publish", 'POST')
    done[r['src']] = dict(record=p['id'], doi=p['doi'], files=len(files)); json.dump(done, open('published-proposed.json', 'w'), indent=1)
    print('published', f, p['id'], f'{len(files)} files', flush=True)
