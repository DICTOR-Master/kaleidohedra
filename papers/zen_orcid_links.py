# ORCID audit + Lean/Palomar links (DICTO 2026-11-21, approved: two metadata-only Zenodo tasks). METADATA ONLY: the latest version
# of each record is edited in place (POST draft -> PUT draft -> publish, the zen_auditfix.py pattern); no new versions, files untouched.
# 1. Every record in the DICTO community (all concepts: the community listing plus every zenodo-state.json here): the creator DICTO
#    must carry ORCID 0009-0001-2620-2036 in person_or_org.identifiers; where missing it is added, the name kept exactly as it is.
# 2. The registered papers get related identifiers (relation issupplementedby, scheme url) to their Lean repo and Palomar entry;
#    links already present are skipped, existing related identifiers kept.
# Usage: zen_orcid_links.py --dry | --apply  [--start K] [--budget SECONDS]   Ends with a FINAL line; prints CHANGED ids for zen_postcheck.py.
import json, urllib.request, urllib.parse, socket, os, sys, glob, time
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.inveniordm.v1+json'}
def req(url, method='GET', body=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), method=method, headers=H), timeout=120))
P = os.path.dirname(os.path.abspath(__file__))
ORCID = '0009-0001-2620-2036'
PAL = 'https://data.palomar-registry.org/entries/'
LINKS = {  # concept id -> (paper, urls)
 '24383552': ('#113 The Dehn Canon', ['https://github.com/DICTOR-Master/dehn-canon-lean', PAL + 'PALOMAR-2026-11-20-000003-v1.json']),
 '24393967': ('#116 Dehn-Hadwiger 4D', ['https://github.com/DICTOR-Master/dehn-hadwiger-4d-lean']),   # Palomar id not yet published
 '24389006': ('#115 Grunbaum', ['https://github.com/DICTOR-Master/grunbaum-k10-lean', PAL + 'PALOMAR-2026-11-20-000013-v1.json']),
 '24052633': ('#103 The DICTO Yantra', ['https://github.com/DICTOR-Master/kulaichev-yantra-lean', PAL + 'PALOMAR-2026-11-17-000006-v2.json']),
}
def supp(url): return {'identifier': url, 'scheme': 'url', 'relation_type': {'id': 'issupplementedby', 'title': {'de': 'Wird ergänzt durch', 'en': 'Is supplemented by'}}}

def is_dicto(c): p = c.get('person_or_org', {}); return p.get('name') == 'DICTO' or p.get('family_name') == 'DICTO'
def transform(cid, meta):
    """(new creators, new related, notes, skip reason)."""
    cr = json.loads(json.dumps(meta.get('creators', []))); notes = []
    ds = [c for c in cr if is_dicto(c)]
    if not ds: return None, None, [], 'no creator named DICTO'
    for c in ds:
        ids = c['person_or_org'].setdefault('identifiers', [])
        o = [i for i in ids if i.get('scheme') == 'orcid']
        if any(i.get('identifier') == ORCID for i in o): continue
        if o: return None, None, [], f'DICTO carries a different ORCID {o[0].get("identifier")}'
        ids.append({'identifier': ORCID, 'scheme': 'orcid'}); notes.append('orcid')
    rel = list(meta.get('related_identifiers', []))
    for u in LINKS.get(cid, (None, []))[1]:
        if any(r.get('identifier', '').rstrip('/') == u for r in rel): notes.append(f'have {u}')
        else: rel.append(supp(u)); notes.append(f'add {u}')
    return cr, rel, notes, None

# ---- all concepts ----
concepts = {}
page = 1
while True:
    r = req(f'https://zenodo.org/api/communities/dicto/records?size=100&page={page}&sort=newest')
    for h in r['hits']['hits']: concepts.setdefault(str(h['parent']['id']), h['metadata'].get('title', ''))
    if len(r['hits']['hits']) < 100: break
    page += 1
for st in sorted(glob.glob(f'{P}/**/zenodo-state.json', recursive=True)):
    try: c = json.load(open(st)).get('conceptrecid')
    except Exception: continue
    if c: concepts.setdefault(str(c), os.path.relpath(os.path.dirname(st), P))
for c in LINKS: concepts.setdefault(c, LINKS[c][0])

apply = '--apply' in sys.argv
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
start = int(arg('--start', 0)); budget = float(arg('--budget', 250)); t0 = time.time()
cids = sorted(concepts); n = dict(checked=0, had=0, fixed=0, links=0, skipped=0, failed=0); changed = []; stopped = None
print(f'{"APPLY" if apply else "DRY RUN"}: {len(cids)} concepts', flush=True)
for i, cid in enumerate(cids):
    if i < start: continue
    if time.time() - t0 > budget: stopped = i; break
    try: rec = req(f'https://zenodo.org/api/records/{cid}/versions/latest')
    except Exception as e: n['skipped'] += 1; print(f'[{i}] {cid}: SKIP (latest not readable: {e})', flush=True); continue
    rid = str(rec['id']); n['checked'] += 1
    cr, rel, notes, why = transform(cid, rec['metadata'])
    title = rec['metadata'].get('title', '')[:60]
    if why: n['skipped'] += 1; print(f'[{i}] {cid} -> {rid} {title}: SKIP ({why})', flush=True); continue
    if 'orcid' not in notes: n['had'] += 1
    adds = [x for x in notes if x.startswith('add ')]
    if not ('orcid' in notes or adds):
        if notes: print(f'[{i}] {cid} -> {rid} {title}: links already present', flush=True)
        continue
    print(f'[{i}] {cid} -> {rid} {title}: ' + ' | '.join(notes), flush=True)
    if not apply: n['fixed'] += 'orcid' in notes; n['links'] += len(adds); continue
    d = req(f'https://zenodo.org/api/records/{rid}/draft', 'POST')
    cr2, rel2, notes2, why2 = transform(cid, d['metadata'])
    if why2 or notes2 != notes: print(f'   DRAFT DIFFERS ({why2 or notes2}); left as an open draft for a look', flush=True); n['failed'] += 1; continue
    d['metadata']['creators'] = cr2; d['metadata']['related_identifiers'] = rel2
    req(f'https://zenodo.org/api/records/{rid}/draft', 'PUT', {k: d[k] for k in ('metadata', 'files', 'access', 'pids', 'custom_fields') if k in d})
    p = req(f'https://zenodo.org/api/records/{rid}/draft/actions/publish', 'POST')
    m = p['metadata']; got = {r.get('identifier') for r in m.get('related_identifiers', [])}
    ok = all(any(i.get('identifier') == ORCID for i in c['person_or_org'].get('identifiers', [])) for c in m['creators'] if is_dicto(c)) \
        and all(x[4:] in got for x in adds) and len(m.get('related_identifiers', [])) == len(rel2)
    print('   saved' if ok else '   NOT SAVED', flush=True)
    if ok: n['fixed'] += 'orcid' in notes; n['links'] += len(adds); changed.append(rid)
    else: n['failed'] += 1
    time.sleep(0.3)
print(f'{"" if apply else "would: "}checked {n["checked"]}, already had ORCID {n["had"]}, ORCID fixed {n["fixed"]}, links added {n["links"]}, '
      f'skipped {n["skipped"]}, failed {n["failed"]}' + (f'; budget reached, resume with --start {stopped}' if stopped is not None else ''))
if changed: print('CHANGED ' + ' '.join(changed))
print('FINAL ok' if n['failed'] == 0 and stopped is None else ('FINAL partial: resume with --start %d' % stopped if n['failed'] == 0 else 'FINAL FAIL'))
