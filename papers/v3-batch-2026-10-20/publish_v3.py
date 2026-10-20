# DICTO 2026-10-20 (DICTO OK: "v3 with additions publish", "v3 stella good also"): new Zenodo versions of #37a and #31a: the paper PDF
# replaced (same name), the study files attached, description and notes updated, licence kept CC BY-SA 4.0.  python3 publish_v3.py [--dry]
import json, os, sys, re, time, socket, urllib.request, html as H
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip(); API = 'https://zenodo.org/api/deposit/depositions'; dry = '--dry' in sys.argv
ME = os.path.dirname(os.path.abspath(__file__)); K = sys.argv[1]
def req(url, method='GET', body=None, raw=None, ctype='application/json'):
    data = raw if raw is not None else (None if body is None else json.dumps(body).encode())
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers={'Authorization': f'Bearer {T}', 'Content-Type': ctype}), timeout=600) as f:
                b = f.read(); return json.loads(b) if b else {}
        except urllib.error.HTTPError as e:
            if e.code < 500: raise RuntimeError(f'{method} {url}: {e.code} {e.read()[:300]}')
            err = e
        except Exception as e: err = e
        time.sleep(5 * (k + 1))
    raise err
def abstract(p):
    s = open(p).read(); a = re.search(r'<div class="abstract"><b>Abstract\.</b>\s*(.*?)</div>', s, re.S).group(1).strip(); return a
G = os.path.join(K, '2026-10-20-og-gyrated-octet', 'paper.html')
jobs = [dict(name='#37a', latest=23484381, pdf='dicto-gyrated-octet.pdf', extra=['og-gyrated-octet-study-56fc236.zip'],
             desc=f"<p>{abstract(G)}</p><p>Companion to The DICTO Ogdoecontahedron on the Octet Truss (#37), DICTO DOI 10.5281/zenodo.23457016. Finding #37a on dictospheres.com. Scripts, exact checks and data: https://github.com/DICTOR-Master/kaleidohedra/tree/56fc236/studies/2026-10-19-og-gyrated-octet, also attached here (og-gyrated-octet-study-56fc236.zip).</p>",
             notes='Version 3 (20 October 2026): adds the DICTO Octahedrally Truncated Triacontahedron (OTT), the DICTO Fill sets (exact), the Penrose-core boundary pieces at twin layers (exact) and the solids packed by themselves (float); the DBT is shown as a solid of its own; DICTO\'s ideas are called his ideas; the study files are attached.'),
        dict(name='#31a', latest=23483449, pdf='dicto-ocd-stella.pdf', extra=['ocd-stella-crystals-studies-918ad50.zip'],
             desc=None, notes='Version 3 (20 October 2026): adds the crystals, exact: with regular octahedra (pyrochlore 1423/32 − 3113√5/160 ≈ 96.33%, rock salt ≈ 91.72%) and the notched OCD Stella, with icosahedra and the four kinds of gap piece; the space groups and the Atom 13 (float); the study files are attached.')]
done = json.load(open(os.path.join(ME, 'published-v3.json'))) if os.path.exists(os.path.join(ME, 'published-v3.json')) else {}
for j in jobs:
    if j['name'] in done: print('skip', j['name']); continue
    r = req(f"{API}/{j['latest']}"); meta = r['metadata']
    assert r['submitted'] and 'cc-by-sa' in json.dumps(meta['license']), j['name']
    if j['desc'] is None:
        d = meta['description']; old = 'the Bodhi Seed\'s pattern. Related prior art'
        assert d.count(old) == 1, 'description anchor'
        d = d.replace(old, "the Bodhi Seed's pattern. With a partner on the second network of the packing it forms crystals, exact: with icosahedra 1523/32 − 669√5/32 ≈ 84.60%; with regular octahedra, whose six tips nest in notches of the OCD Stellas, 1423/32 − 3113√5/160 ≈ 96.33%; and an Atom 13 (float). Related prior art")
        d = d.replace('with its exact data and checks included', 'with its exact data and checks included (the study files are attached: ocd-stella-crystals-studies-918ad50.zip)')
        j['desc'] = d
    meta['description'] = j['desc']; meta['version'] = '3'; meta['publication_date'] = '2026-10-20'; meta['notes'] = j['notes']
    meta.pop('doi', None); meta.pop('prereserve_doi', None)
    files = [f['filename'] for f in r['files']]
    print(f"{'DRY ' if dry else ''}{j['name']}: from {j['latest']} (v{r['metadata']['version']}), files {files} -> replace {j['pdf']}, add {j['extra']}; description {len(j['desc'])} chars")
    if dry: print(j['desc'][:400], '...'); continue
    nv = req(f"{API}/{j['latest']}/actions/newversion", 'POST'); draft = req(nv['links']['latest_draft'])
    hit = [x for x in draft.get('files', []) if x['filename'] == j['pdf']]; assert len(hit) == 1, [x['filename'] for x in draft.get('files', [])]
    req(f"{API}/{draft['id']}/files/{hit[0]['id']}", 'DELETE')
    for fn in [j['pdf']] + j['extra']:
        req(f"{draft['links']['bucket']}/{fn}", 'PUT', raw=open(os.path.join(ME, fn), 'rb').read(), ctype='application/octet-stream')
    req(f"{API}/{draft['id']}", 'PUT', {'metadata': meta}); p = req(f"{API}/{draft['id']}/actions/publish", 'POST')
    done[j['name']] = dict(record=p['id'], doi=p['doi'], files=[f['filename'] for f in p['files']]); json.dump(done, open(os.path.join(ME, 'published-v3.json'), 'w'), indent=1)
    print('published', j['name'], p['id'], p['doi'], [f['filename'] for f in p['files']], flush=True)
