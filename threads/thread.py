#!/usr/bin/env python3
# DICTO threads (26 Nov 2026): work as short cards, at most three active, every parked thread with a wake-up, one map, and a
# separate list of what waits on DICTO. With Claude (Anthropic). DICTO: "a method for threads of the concordance to follow lower
# context creating flow"; "parking makes it easy to forget for me" (wake-ups, map, weekly review); "todo list decisions are outside
# the threads triage" (WAITING.md, his list).
# Usage: thread.py            resume view: waiting on DICTO, the active cards (state + next), threads waking today
#        thread.py show ID     one card in full          thread.py map       write MAP.html (every thread, one line each)
#        thread.py done ID     close (DICTO's word only) thread.py promote ID   make a queued/parked thread active (cap 3)
#        thread.py review      every parked and queued thread, one line each, for the weekly review
import json, os, sys, datetime, html
HERE = os.path.dirname(os.path.abspath(__file__)); IDX = os.path.join(HERE, 'threads.json'); CAP = 3
T = json.load(open(IDX)); today = datetime.date.today().isoformat()
def save(): json.dump(T, open(IDX, 'w'), indent=1, ensure_ascii=False)
def card(t): return open(os.path.join(HERE, 'cards', t['id'] + '.md')).read()
def section(txt, head):
    out, on = [], False
    for line in txt.splitlines():
        if line.startswith('## '): on = line[3:].strip().lower().startswith(head)
        elif on and line.strip(): out.append(line)
    return out
def waking(t):
    w = t.get('wake', '')
    return t['status'] in ('queued', 'parked') and w[:10] <= today and w[:4].isdigit()
cmd = sys.argv[1] if len(sys.argv) > 1 else 'resume'
if cmd == 'resume':
    print(open(os.path.join(HERE, 'WAITING.md')).read().strip()); print()
    act = [t for t in T if t['status'] == 'active']
    print(f'ACTIVE THREADS ({len(act)} of {CAP})')
    for t in act:
        c = card(t); print(f"  {t['id']}  {t['title']}  -> {t['dest']}")
        for l in section(c, 'state')[:3]: print('     state:', l.lstrip('- '))
        for l in section(c, 'next')[:1]: print('     next: ', l.lstrip('- '))
    w = [t for t in T if waking(t)]
    print('WAKING TODAY:', ', '.join(f"{t['id']} {t['title']}" for t in w) if w else 'none')
    trig = [t for t in T if t['status'] in ('queued', 'parked') and not t.get('wake', '')[:4].isdigit()]
    if trig: print('WAITING ON A TRIGGER:', '; '.join(f"{t['id']} ({t['wake']})" for t in trig))
elif cmd == 'show': print(card(next(t for t in T if t['id'] == sys.argv[2])))
elif cmd == 'promote':
    t = next(t for t in T if t['id'] == sys.argv[2])
    if sum(x['status'] == 'active' for x in T) >= CAP: sys.exit(f'cap of {CAP} active threads reached: close or park one first')
    t['status'] = 'active'; save(); print('active:', t['id'])
elif cmd == 'done':
    t = next(t for t in T if t['id'] == sys.argv[2]); t['status'] = 'done'; t['closed'] = today; save(); print('done:', t['id'])
elif cmd in ('map', 'review'):
    order = ['active', 'queued', 'parked', 'done'] if cmd == 'map' else ['queued', 'parked']
    if cmd == 'review':
        for st in order:
            for t in [t for t in T if t['status'] == st]: print(f"{st:7s} {t['id']:4s} {t['title']}  (wake: {t.get('wake','')}; -> {t['dest']})")
        sys.exit(0)
    rows = ''.join(f"<tr class='{t['status']}'><td>{t['id']}</td><td>{html.escape(t['title'])}</td><td>{t['status']}</td><td>{html.escape(t.get('wake',''))}</td><td>{html.escape(t['dest'])}</td></tr>"
                   for st in order for t in T if t['status'] == st)
    W = html.escape(open(os.path.join(HERE, 'WAITING.md')).read())
    open(os.path.join(HERE, 'MAP.html'), 'w').write(f"""<!doctype html><meta charset=utf-8><title>DICTO threads</title>
<style>body{{font:13px/1.4 system-ui;margin:28px}}h1{{font-size:20px}}table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #ddd;padding:4px 6px;vertical-align:top}}
tr.active td{{background:#fff4d6}} tr.done td{{color:#999}} pre{{white-space:pre-wrap;background:#f4f1ea;padding:10px;font:12px/1.4 system-ui}}</style>
<h1>DICTO threads · {today}</h1><h2>Waiting on DICTO</h2><pre>{W}</pre><h2>Every thread</h2>
<table><tr><td><b>id</b></td><td><b>thread</b></td><td><b>status</b></td><td><b>wake-up</b></td><td><b>home</b></td></tr>{rows}</table>
<p>DICTO · dictospheres.com · with Claude (Anthropic). At most {CAP} active; every parked thread has a wake-up; only DICTO closes a thread.</p>""")
    print('MAP.html written:', len(T), 'threads')
