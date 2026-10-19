# SA batch publish (only after DICTO's OK): for each record in plan.json, a new Zenodo version that keeps every file except the paper PDF,
# which is replaced by the reprint (same name); metadata: licence cc-by-sa-4.0, new version, date 2026-10-20, a version note.
#   python3 sa_publish.py plan.json newpdf/ [--dry]      (IPv4 only; legacy deposit API)
import json, os, socket, sys, time, urllib.request
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip(); API = 'https://zenodo.org/api/deposit/depositions'
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    for k in range(4):
        try:
            r = urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype})
            with urllib.request.urlopen(r, timeout=300) as f: b = f.read(); return json.loads(b) if b else {}
        except urllib.error.HTTPError as e:
            if e.code < 500: raise RuntimeError(f'{method} {url}: {e.code} {e.read()[:300]}')
            err = e
        except Exception as e: err = e
        time.sleep(5 * (k + 1))
    raise err
plan, pdfdir, dry = json.load(open(sys.argv[1])), sys.argv[2], '--dry' in sys.argv
NOTE = 'Version {v} (20 October 2026): the licence is now CC BY-SA 4.0 (Attribution-ShareAlike); earlier versions keep CC BY 4.0. The paper is otherwise unchanged.'
NOTE38 = ('Version 2 (20 October 2026): corrects one sentence in section 5. Version 1 called the three-sided pyramid of the ID to RT shell DICTO\'s CLEO; '
          'a corner-by-corner shape test shows it is not (it has a lower point). The abstract now says "DICTO specified". The licence is now CC BY-SA 4.0; version 1 keeps CC BY 4.0.')
done = json.load(open('published.json')) if os.path.exists('published.json') else {}
for r in plan:
    if r['src'] in done: print('skip (done)', r['src']); continue
    pdf = [f for f in os.listdir(pdfdir) if f.startswith(f"{r['concept']}-")]; assert len(pdf) == 1, r['src']
    path = os.path.join(pdfdir, pdf[0]); name = pdf[0].split('-', 1)[1]
    old = req(f"{API}/{r['latest']}"); meta = old['metadata']
    meta['license'] = 'cc-by-sa-4.0'; meta['version'] = str(r['new_version']); meta['publication_date'] = '2026-10-20'
    if 'universal-pitet' in r['src']:
        meta['notes'] = NOTE38; assert 'DICTO asked for' in meta['description']; meta['description'] = meta['description'].replace('DICTO asked for', 'DICTO specified', 1)
    elif 'collected' in r['src']:
        a = 'Version 13 adds #38, Universal PiTet: The DICTO PiTet Proposition;'; assert a in meta['description']
        meta['description'] = meta['description'].replace(a, 'Version 14 adds #38a, The DICTO Kepler–Poinsot–UP Cycle, and records that from 20 October 2026 every paper listed here is released under CC BY-SA 4.0 (Attribution-ShareAlike): each has a new version with that licence, and earlier versions keep CC BY 4.0. Version 13 added #38, Universal PiTet: The DICTO PiTet Proposition;')
        meta['notes'] = NOTE.format(v=r['new_version']).replace(' The paper is otherwise unchanged.', ' Adds #38a.')
    else: meta['notes'] = NOTE.format(v=r['new_version'])
    meta.pop('doi', None); meta.pop('prereserve_doi', None)
    if dry: print('DRY', r['src'], name, meta['version'], meta['license'], meta['notes'][:60]); continue
    nv = req(f"{API}/{r['latest']}/actions/newversion", 'POST'); draft = req(nv['links']['latest_draft'])
    files = draft.get('files', []); hit = [f for f in files if f['filename'] == name]; assert len(hit) == 1, (r['src'], [f['filename'] for f in files])
    req(f"{API}/{draft['id']}/files/{hit[0]['id']}", 'DELETE')
    req(f"{draft['links']['bucket']}/{name}", 'PUT', raw=open(path, 'rb').read(), ctype='application/octet-stream')
    req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta})
    p = req(f"{API}/{draft['id']}/actions/publish", 'POST')
    done[r['src']] = dict(record=p['id'], doi=p['doi'], files=len(files)); json.dump(done, open('published.json', 'w'), indent=1)
    print('published', r['src'], p['id'], p['doi'], f'{len(files)} files kept/replaced', flush=True)
