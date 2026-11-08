"""Search each candidate list of DICTO's (candidates.json) in the OEIS, politely (one request every 3 s, IPv4, plain client name).
Query: up to 10 terms, leading 0s and 1s dropped (OEIS hints). Result per list: FOUND (A-numbers + names; our terms appear in
order), or NOT FOUND. Writes matches.json and a heartbeat line every 10 queries; final line FINAL ok / FINAL FAIL.
Usage: match.py [limit]"""
import json, sys, time, urllib.request, urllib.parse, socket
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9
C = json.load(open('candidates.json'))[:LIMIT]
out = []; errors = 0
def q(terms):
    url = 'https://oeis.org/search?' + urllib.parse.urlencode({'q': ','.join(map(str, terms)), 'fmt': 'json'})
    req = urllib.request.Request(url, headers={'User-Agent': 'dicto-research-oeis-matcher/1.0'})
    with urllib.request.urlopen(req, timeout=40) as r: j = json.load(r)
    rs = j if isinstance(j, list) else ((j or {}).get('results') or [])
    return [{'a': 'A%06d' % x['number'], 'name': x['name'][:160]} for x in rs[:5]]
for i, c in enumerate(C):
    s = c['seq'][:]
    while s and s[0] in (0, 1) and len(s) > 6: s = s[1:]
    terms = s[:10]
    for attempt in range(3):
        try: hits = q(terms); break
        except Exception as e:
            hits = None; time.sleep(10)
    if hits is None: errors += 1
    out.append({**c, 'query': terms, 'hits': hits, 'status': 'ERROR' if hits is None else ('FOUND' if hits else 'NOT FOUND')})
    if (i + 1) % 10 == 0: print(f'heartbeat {i + 1}/{len(C)} errors {errors}', flush=True); json.dump(out, open('matches.json', 'w'), indent=1)
    time.sleep(3)
json.dump(out, open('matches.json', 'w'), indent=1)
n = len(out); f = sum(o['status'] == 'FOUND' for o in out)
print(f'{n} lists: {f} found, {n - f - errors} not found, {errors} errors')
print('FINAL ok' if n and errors <= n // 10 else 'FINAL FAIL: too many errors')
