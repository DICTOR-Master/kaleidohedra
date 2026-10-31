import json, os, collections, html
INV = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(INV)
OUT = '/home/dicto/k-research/studies/2026-10-31-transitional-files'
items = json.load(open(os.path.join(INV, 'items.json')))
MN = {'pi': 'Pi', 'node': 'dicto-node', 'dbb': 'dicto-big-brother'}
SCRIPT = {'pi': 'pi', 'node': 'dicto-node', 'dbb': 'dicto-big-brother'}

def fmt(kb):
    if kb >= 1024 * 1024: return '%.1f GB' % (kb / 1048576)
    if kb >= 1024: return '%.0f MB' % (kb / 1024) if kb >= 10240 else '%.1f MB' % (kb / 1024)
    return '%d KB' % kb

for m in MN:
    for x in items:
        assert "'" not in x['path'], x['path']
    L = ['#!/bin/bash',
         '# Transitional files on %s: SAFE items only (inventory of 31 October 2026).' % MN[m],
         '# Each item has a permanent copy (git, Zenodo, or rebuildable). Read before running.',
         '# Generated read-only; nothing has been deleted yet.']
    if m == 'pi':
        L.append('# Tracked files in ~/k-research (drafts, old versions) will show as deleted in git status;')
        L.append('# commit their removal afterwards (git -C /home/dicto/k-research add -u <paths>; commit).')
    if m != 'pi':
        L.append('# Run on %s itself (copy it there, then: bash cleanup-%s.sh).' % (MN[m], SCRIPT[m]))
    L.append('')
    tot = 0
    for x in sorted([i for i in items if i['machine'] == m and i['conf'] == 'SAFE'], key=lambda i: -i['kb']):
        tot += x['kb']
        L.append('# %s · %s · permanent copy: %s' % (fmt(x['kb']), x['why'], x['where']))
        if x['kind'] == 'worktree':
            L.append("git -C /home/dicto/kaleidohedra worktree remove --force '%s'" % x['path'])
        else:
            L.append("rm -rf -- '%s'" % x['path'])
    L.insert(4, '# Total: %s' % fmt(tot))
    p = os.path.join(SP, 'cleanup-%s.sh' % SCRIPT[m])
    open(p, 'w').write('\n'.join(L) + '\n')
    os.chmod(p, 0o644)

# ---------- report ----------
tot = collections.defaultdict(lambda: [0, 0])
for x in items:
    tot[(x['machine'], x['conf'])][0] += 1
    tot[(x['machine'], x['conf'])][1] += x['kb']
E = html.escape
def short(p):
    return p.replace('/home/dicto/', '~/').replace('/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/', '/tmp/claude-1000/…/')

rows = []
rows.append('<table><tr><th>Machine</th><th class="n">SAFE</th><th class="n">CHECK</th><th class="n">KEEP</th><th class="n">All</th></tr>')
G = {'SAFE': [0, 0], 'CHECK': [0, 0], 'KEEP': [0, 0]}
for m in MN:
    cells = []
    s = [0, 0]
    for c in ('SAFE', 'CHECK', 'KEEP'):
        n, kb = tot[(m, c)]
        G[c][0] += n; G[c][1] += kb; s[0] += n; s[1] += kb
        cells.append('<td class="n">%s<br><span class="k">%d items</span></td>' % (fmt(kb) if n else '–', n))
    rows.append('<tr><td><b>%s</b></td>%s<td class="n">%s<br><span class="k">%d items</span></td></tr>' % (MN[m], ''.join(cells), fmt(s[1]), s[0]))
rows.append('<tr><td><b>All</b></td>%s<td class="n"><b>%s</b></td></tr>' % (''.join('<td class="n"><b>%s</b><br><span class="k">%d items</span></td>' % (fmt(G[c][1]), G[c][0]) for c in G), fmt(sum(v[1] for v in G.values()))))
rows.append('</table>')
totals = '\n'.join(rows)

top = sorted(items, key=lambda i: -i['kb'])[:10]
toprows = '<table><tr><th>#</th><th>Item</th><th>Machine</th><th class="n">Size</th><th>Grade</th></tr>' + ''.join(
    '<tr><td>%d</td><td><code>%s</code></td><td>%s</td><td class="n">%s</td><td class="%s">%s</td></tr>' % (i + 1, E(short(x['path'])), MN[x['machine']], fmt(x['kb']), x['conf'].lower(), x['conf']) for i, x in enumerate(top)) + '</table>'

def table(m, c):
    sel = [x for x in items if x['machine'] == m and x['conf'] == c]
    if not sel: return ''
    groups = collections.OrderedDict()
    for x in sorted(sel, key=lambda i: -i['kb']):
        groups.setdefault((x['why'], x['where']), []).append(x)
    out = []
    for (why, where), xs in sorted(groups.items(), key=lambda kv: -sum(x['kb'] for x in kv[1])):
        kb = sum(x['kb'] for x in xs)
        if len(xs) > 3:
            parent = os.path.commonpath([x['path'] for x in xs])
            names = ', '.join(sorted(os.path.relpath(x['path'], parent) for x in xs))
            if len(names) > 420: names = names[:420] + ' …'
            path = '<code>%s/</code> · %d items: <span class="k">%s</span>' % (E(short(parent)), len(xs), E(names))
        else:
            path = '<br>'.join('<code>%s</code>' % E(short(x['path'])) for x in xs)
        out.append('<tr><td>%s</td><td class="n">%s</td><td>%s</td><td>%s</td></tr>' % (path, fmt(kb), E(why), E(where)))
    return ('<h3>%s · %s (%s)</h3><table class="inv"><tr><th style="width:38%%">Path</th><th class="n" style="width:8%%">Size</th><th>Why transitional</th><th style="width:26%%">Permanent copy</th></tr>' % (MN[m], c, fmt(sum(x['kb'] for x in sel)))) + ''.join(out) + '</table>'

body = []
for i, m in enumerate(MN):
    body.append('<h2>%d. %s</h2>' % (i + 4, MN[m]))
    for c in ('SAFE', 'CHECK', 'KEEP'):
        body.append(table(m, c))

page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Transitional files</title>
<link rel="stylesheet" href="../../papers/paper.css">
<style>table{border-collapse:collapse;font-size:8pt;margin:3mm 0;width:100%%} td,th{border-bottom:1px solid #ddd;padding:0.9mm 1.3mm;text-align:left;vertical-align:top} td.n,th.n{text-align:right;white-space:nowrap} table.inv{font-size:7pt} table.inv code{font-size:6.6pt;word-break:break-all} code{font-size:7.4pt;word-break:break-all} .k{color:#666;font-size:6.8pt} td.safe{color:#1d6b2f;font-weight:600} td.check{color:#9a6a00;font-weight:600} td.keep{color:#8a1c1c;font-weight:600} h3{font-size:10pt;margin-top:5mm;break-after:avoid} table.inv{break-inside:auto} table.inv tr{break-inside:avoid}</style>
</head><body>
<img class="watermark" src="../../papers/dicto-logo.png" alt="">
<img class="logo" src="../../papers/dicto-logo.png" alt="DICTO">

<h1>Transitional files</h1>
<p class="sub">Drafts, copies, renders and caches on the three machines, and where each one is kept for good</p>
<div class="meta"><b>DICTO</b> · inventory of 31 October 2026 · for DICTO's decision · not for publication</div>

<h2>1. Totals</h2>
<p>DICTO's rule of 31 October: a transitional file goes once its content is kept for good, on Zenodo, in git, or rebuildable from committed sources. Nothing has been deleted. SAFE means the permanent copy was checked; CHECK means it is likely transitional but needs DICTO's word; KEEP means there is no other copy, so it should move to the LaCie.</p>
%s
<p>The SAFE items are in three scripts, one per machine, in the session scratchpad: <code>cleanup-pi.sh</code>, <code>cleanup-dicto-node.sh</code>, <code>cleanup-dicto-big-brother.sh</code>. Each line is one literal path with its size and reason. The Pi has 4.2 GB free of 29 GB; its SAFE items free about %s. Most of the space is on dicto-node and dicto-big-brother, which have 868 GB and 1.7 TB free.</p>

<h2>2. The ten largest items</h2>
%s

<h2>3. How each copy was checked</h2>
<p><b>Git.</b> Every file in a copy (outside node_modules, dist, test output, caches) was hashed with git and looked up among all 32,536 objects of the Pi repositories (Kaleidohedra with its worktrees and krp-core submodules, krp-core, Rhombiverse, dictospheres, Polyhedraverse). A copy is SAFE when every file was found, or the only extra files are probes, logs, screenshots, or files shown identical (md5) to a Pi copy.</p>
<p><b>Zenodo.</b> Zips and PDFs were checked by md5 against the files of their Zenodo records through the public API. Ten source zips were checked; eight match. The real-materials-2 and two-tiles zips are not on their records (only the PDF is), so they are CHECK. All 78 PDFs in the node batch folder sa-batch match a version of their record.</p>
<p><b>Already done today.</b> Five finished Claude session transcripts (about 800 MB) left the Pi at 11:37 and are now in <code>/mnt/dicto-backup/archive/claude-sessions</code> on the LaCie. Another process is also removing DRAFT PDFs from ~/k-research (they show as deleted, not yet committed). Neither is listed here.</p>
<p><b>Not transitional, but worth a commit.</b> Several current files in ~/k-research are untracked: <code>papers/4d-shadows/paper.html</code> and <code>papers/series-web-of-bonds/paper.html</code> (sources), the cover scripts' fonts and logos in <code>studies/2026-10-30-quanta-cover/scripts/</code>, and the current PDFs of the HexOct and Quanta books, Star Cores A and C, TI Star, Between the Queens, Face to Face and CW v47. They are on Zenodo but not in git.</p>
<p><b>Left out.</b> Tools and environments (Python venvs plotenv and geom, llama.cpp, the 92 GB of models, Antiprism's install), Playwright browsers still in use (chromium 1234, 1243 and 1248 are all referenced by installed test packages), logs older than 14 days (1 MB on the Pi, 2.5 MB on the node), memory, the current session, published final PDFs, and the dicto-deploy, dicto-stats, dicto-watchdog and dicto-backup folders. The Kaleidohedra git store on the Pi is 990 MB; <code>git gc</code> may shrink it, but that is not a deletion.</p>
%s
</body></html>
''' % (totals, fmt(tot[('pi', 'SAFE')][1]), toprows, '\n'.join(body))
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'report.html'), 'w').write(page)
json.dump(items, open(os.path.join(OUT, 'inventory.json'), 'w'), indent=1)
print('ok', {k: (v[0], fmt(v[1])) for k, v in tot.items()})
