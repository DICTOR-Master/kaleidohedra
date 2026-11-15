#!/usr/bin/env python3
"""fetch_mccooey.py (15 Nov 2026) - DICTO · dictospheres.com
Polite crawl of David McCooey's "Visual Polyhedra" catalogue (dmccooey.com/polyhedra): every page reachable from the index
inside /polyhedra/ (the Java viewer folder skipped), and the coordinate text file each polyhedron page links to.
Rules: plain requests with the library's own default user agent (no spoofing), DELAY seconds between requests, robots.txt
read first and obeyed, no retries past one, and a full STOP on any refusal (HTTP 403 / 429 / 503 or a challenge page).
The fetched files are a local cache for the comparison only (not redistributed); data/mccooey-manifest.json lists name, URL,
size and sha256 of each text file.
usage: fetch_mccooey.py CACHE_DIR MANIFEST.json [DELAY=2.0] [LIMIT=0]   (LIMIT > 0: pilot, stop after LIMIT requests)"""
import sys, os, re, time, json, hashlib, urllib.request, urllib.error, urllib.robotparser
from collections import deque

BASE = 'https://dmccooey.com/polyhedra/'
CACHE, MAN = sys.argv[1], sys.argv[2]
DELAY = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
LIMIT = int(sys.argv[4]) if len(sys.argv) > 4 else 0
os.makedirs(os.path.join(CACHE, 'html'), exist_ok=True)
os.makedirs(os.path.join(CACHE, 'txt'), exist_ok=True)
T0 = time.time()
nreq = 0
last = 0.0

rp = urllib.robotparser.RobotFileParser('https://dmccooey.com/robots.txt')
rp.read()
if rp.disallow_all or rp.allow_all:      # 15 Nov: robotparser treats a refused robots.txt (465) as allow-all; refuse instead
    try:
        urllib.request.urlopen('https://dmccooey.com/robots.txt', timeout=60).read()
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f'STOP robots.txt answered HTTP {e.code}: the site refuses this client', flush=True); sys.exit(7)
UA = 'Python-urllib/%d.%d' % sys.version_info[:2]      # the library default, stated, not spoofed


def stop(msg):
    print('STOP', msg, flush=True)
    sys.exit(7)


def get(url, path):
    """cached GET; returns text or None (404)"""
    global nreq, last
    if os.path.exists(path):
        return open(path, encoding='latin-1').read()
    if not rp.can_fetch(UA, url):
        print('ROBOTS-SKIP', url, flush=True)
        return None
    if LIMIT and nreq >= LIMIT:
        raise StopIteration
    wait = DELAY - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    last = time.time()
    nreq += 1
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                b = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print('404', url, flush=True)
                return None
            if 400 <= e.code < 600 and e.code not in (500, 502, 504):   # 15 Nov: the site answered 465 "Access Denied"
                stop(f'HTTP {e.code} on {url}: the site refused; crawl ends here')
            if attempt == 2:
                print('HTTPERR', e.code, url, flush=True)
                return None
        except Exception as e:      # network hiccup: one retry after a long pause
            if attempt == 2:
                print('NETERR', url, e, flush=True)
                return None
            time.sleep(30)
    t = b.decode('latin-1')
    low = t[:3000].lower()
    if 'access denied' in low or 'you have been blocked' in low or 'captcha' in low or 'challenge' in low and 'cloudflare' in low or 'checking your browser' in low:
        stop(f'challenge page on {url}: the site blocks scripts; crawl ends here')
    open(path, 'w', encoding='latin-1').write(t)
    return t


LINK = re.compile(r"""href\s*=\s*['"]?([^'" >]+)""", re.I)
seen, txts = set(), {}
q = deque(['index.html'])
seen.add('index.html')
try:
    while q:
        page = q.popleft()
        html = get(BASE + page, os.path.join(CACHE, 'html', page))
        if html is None:
            continue
        for m in LINK.findall(html):
            m = m.strip().strip("'\"")
            if '://' in m or m.startswith('#') or m.startswith('..') or '/' in m:
                continue
            m = m.split('#')[0]
            if m.endswith('.html') and m not in seen:
                seen.add(m)
                q.append(m)
            elif m.endswith('.txt') and m not in txts:
                txts[m] = page
        print(f'PROGRESS {len(seen) - len(q)}/{len(seen)} pages, {len(txts)} text files found, {nreq} requests, '
              f'{time.time() - T0:.0f} s', flush=True)
    done = 0
    for i, (t, page) in enumerate(sorted(txts.items())):
        s = get(BASE + t, os.path.join(CACHE, 'txt', t))
        done += s is not None
        if i % 50 == 0:
            print(f'PROGRESS {0.5 + 0.5 * i / max(1, len(txts)):.3f} text files {i}/{len(txts)}, {nreq} requests, '
                  f'{time.time() - T0:.0f} s', flush=True)
except StopIteration:
    print(f'PILOT LIMIT reached: {nreq} requests in {time.time() - T0:.0f} s', flush=True)

man = []
for t, page in sorted(txts.items()):
    p = os.path.join(CACHE, 'txt', t)
    if os.path.exists(p):
        b = open(p, 'rb').read()
        first = b.decode('latin-1').splitlines()[0].strip() if b else ''
        man.append({'file': t, 'name': first, 'page': BASE + page, 'url': BASE + t, 'bytes': len(b),
                    'sha256': hashlib.sha256(b).hexdigest()})
json.dump({'source': 'David McCooey, Visual Polyhedra, ' + BASE, 'fetched': time.strftime('%Y-%m-%d'),
           'delay_s': DELAY, 'user_agent': UA, 'pages_seen': len(seen), 'text_files': man}, open(MAN, 'w'), indent=1)
print(f'pages {len(seen)}, text files linked {len(txts)}, cached {len(man)}, requests {nreq}, {time.time() - T0:.0f} s', flush=True)
ok = len(man) == len(txts) and len(man) > 0
print('FINAL ok' if ok and not LIMIT else ('PILOT done' if LIMIT else 'FINAL FAIL: missing text files'), flush=True)
