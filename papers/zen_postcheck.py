# Shared post-check after ANY Zenodo publish or edit (DICTO 2026-11-10: "set up to succeed … not micromanage"). For each record id:
# the PDF is the default preview; the description has no banned wording (print.mjs BAN) or machine detail. On a failure: prints
# POSTCHECK FAIL and writes ~/dicto-alerts/zenodo-<id>.txt (shown before every message until fixed). Usage: zen_postcheck.py ID [ID …]
import json, urllib.request, socket, os, sys, re
orig = socket.getaddrinfo; socket.getaddrinfo = lambda *a, **k: [x for x in orig(*a, **k) if x[0] == socket.AF_INET]
T = open(os.path.expanduser('~/.config/zenodo/token')).read().strip()
H = {'Authorization': f'Bearer {T}', 'Accept': 'application/vnd.inveniordm.v1+json'}
P = os.path.dirname(os.path.abspath(__file__))
BAN = re.compile(re.search(r'const BAN = /(.*?)/gi;', open(f'{P}/print.mjs').read()).group(1), re.I)
bad_all = 0
for rid in sys.argv[1:]:
    r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://zenodo.org/api/records/{rid}', headers=H), timeout=60))
    probs = []; f = r.get('files', {}); pdfs = [k for k in f.get('entries', {}) if k.endswith('.pdf')]
    if pdfs and f.get('default_preview') not in pdfs: probs.append(f"PDF not the default preview (preview = {f.get('default_preview')})")
    desc = re.sub(r'<[^>]+>', ' ', r['metadata'].get('description', ''))
    for m in list(BAN.finditer(desc))[:3]: probs.append(f"banned wording in description: …{desc[max(0, m.start() - 40):m.end() + 40]}…")
    alert = os.path.expanduser(f'~/dicto-alerts/zenodo-{rid}.txt')
    if probs:
        bad_all += 1; print(f'POSTCHECK FAIL {rid}: ' + ' | '.join(probs))
        open(alert, 'w').write(f'Zenodo record {rid} failed its post-check:\n' + '\n'.join(probs) + '\n')
    else:
        print(f'POSTCHECK ok {rid}'); 
        if os.path.exists(alert): os.remove(alert)
sys.exit(1 if bad_all else 0)
