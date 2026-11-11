# One aiXiv drip-feed submission (DICTO 12 Nov 2026: drip-feed the older papers, "two or three a day at intervals", label (a)).
# usage: aixiv_drip.py <paper number> <paper dir> [--dry]
# Steps: (1) title search on aiXiv: STOP if a paper with this title already exists (the Zenodo importer may have taken it);
# (2) dry run (validates, publishes nothing); (3) real submit; account paper count must rise by exactly 1; (4) result saved in
# <dir>/aixiv-packet/aixiv-submit-result.json and the queue entry marked submitted. Privacy: the fields are scanned first with the
# commit guard's private pattern list (kept outside the repository).
import json, os, sys, base64, re, time, urllib.request, urllib.parse
n, d = sys.argv[1], sys.argv[2]; DRY = '--dry' in sys.argv
B = os.path.expanduser('~/k-research/papers'); Q = os.path.join(B, 'aixiv-queue', 'queue.json')
T = open(os.path.expanduser('~/.config/aixiv/token')).read().strip(); H = {'Authorization': 'Bearer ' + T, 'User-Agent': 'research-client'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
def post(u, body):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(u, data=json.dumps(body).encode(), headers={**H, 'Content-Type': 'application/json'}, method='POST'), timeout=300))
    except urllib.error.HTTPError as e: return {'ok': False, 'http': e.code, 'body': e.read().decode()[:1500]}
pk = json.load(open(f'{B}/{d}/aixiv-packet/fields.json')); f = dict(pk['fields'])
P = open(os.path.expanduser('~/dicto-alerts/privacy-pattern.txt')).read().strip()   # private list, same as the commit guard
bad = re.findall(P, json.dumps(f, ensure_ascii=False))
if bad: sys.exit(f'STOP privacy: {bad}')
assert f['ai_contribution'] == 'ai-assisted' and f['license'] == 'CC BY-SA 4.0' and f['external_url'].startswith('https://doi.org/10.5281/zenodo.')
hits = get('https://aixiv.online/api/v1/papers?' + urllib.parse.urlencode({'q': f['title'], 'limit': 20}))
L = hits.get('papers', hits) if isinstance(hits, dict) else hits
same = [p.get('id') or p.get('aixiv_id') for p in L if (p.get('title') or '').strip().lower() == f['title'].strip().lower()]
if same: sys.exit(f'STOP: already on aiXiv as {same}')
f['pdf_b64'] = base64.b64encode(open(f"{B}/{d}/aixiv-packet/{pk['pdf']}", 'rb').read()).decode()
n0 = get('https://aixiv.online/api/v1/me')['papers']
r = post('https://aixiv.online/api/v1/submit?dry_run=1', f)
json.dump({k: v for k, v in r.items() if k != 'pdf_b64'}, open(f'{B}/{d}/aixiv-packet/dry-run-result.json', 'w'), indent=1, ensure_ascii=False)
time.sleep(5); n1 = get('https://aixiv.online/api/v1/me')['papers']
print(f"#{n} dry run ok={r.get('ok')} papers {n0}->{n1} {str(r.get('body', ''))[:400]}", flush=True)
if not r.get('ok') or n1 != n0: sys.exit('STOP: dry run failed or changed the account')
if DRY: print('FINAL ok (dry only)'); sys.exit()
r = post('https://aixiv.online/api/v1/submit', f)
json.dump(r, open(f'{B}/{d}/aixiv-packet/aixiv-submit-result.json', 'w'), indent=1, ensure_ascii=False)
time.sleep(20); n2 = get('https://aixiv.online/api/v1/me')['papers']
print(f"#{n} submit ok={r.get('ok')} id={r.get('aixiv_id')} url={r.get('abs_url')} papers {n1}->{n2} {str(r.get('body', ''))[:400]}", flush=True)
ok = bool(r.get('ok')) and n2 == n1 + 1
q = json.load(open(Q))
for e in q['queue']:
    if e['n'] == n: e.update(status='submitted' if ok else 'FAILED', aixiv=r.get('aixiv_id'), date=time.strftime('%Y-%m-%d %H:%M'))
json.dump(q, open(Q, 'w'), indent=1, ensure_ascii=False)
print('FINAL ok' if ok else 'FINAL FAIL')
