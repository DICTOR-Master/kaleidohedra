# SA batch source edits (2026-10-20): meta line -> next version, 20 October 2026, Licence CC BY-SA 4.0, DICTO DOI label; #38 V2 fixes;
# Collected Works v14 (#38a row + licence statement). Prints every changed line for review.
import json, re, sys
K = sys.argv[1] + '/'
inv = json.load(open('sa-batch/inventory.json')); plan = []
SPECIAL = {'papers/2026-10-19-universal-pitet/paper.html': 'corrects one sentence in §5 and one word in the abstract; licence now CC BY-SA 4.0',
           'papers/collected/collected.html': None}
for r in inv:
    p = K + r['src']; t = open(p).read(); v = int(r['version']); nv = v + 1
    note = SPECIAL.get(r['src'], 'licence now CC BY-SA 4.0') or 'licence now CC BY-SA 4.0'
    m = re.search(r'Version (\d+) · ([^·<]+?) · ', t); assert m and int(m.group(1)) == v, r['src']
    line_start = t.rfind('\n', 0, m.start()) + 1; line_end = t.index('\n', m.end()); old_line = t[line_start:line_end]
    new_line = old_line.replace(m.group(0), f'Version {nv} · 20 October 2026 ({note}) · ', 1)
    assert new_line.count('Licence CC BY 4.0') == 1, r['src']; new_line = new_line.replace('Licence CC BY 4.0', 'Licence CC BY-SA 4.0')
    new_line = re.sub(r'· DOI (10\.5281/)', r'· DICTO DOI: \1', new_line)
    t = t[:line_start] + new_line + t[line_end:]
    assert 'CC BY 4.0' not in t.replace('CC BY-SA 4.0', ''), ('stray CC BY 4.0', r['src'])
    if r['src'] == 'papers/2026-10-19-universal-pitet/paper.html':
        a = "DICTO asked for a five-fold version of the octet"; assert t.count(a) == 1; t = t.replace(a, "DICTO specified a five-fold version of the octet")
        b = "; the three-sided pyramid is DICTO's CLEO, a piece appearing again."; assert t.count(b) == 1
        t = t.replace(b, ". (Version 1 called the three-sided pyramid DICTO's CLEO. A corner-by-corner shape test shows it is not: it has a lower point, about 2.17 times its base radius high against CLEO's φ² ≈ 2.618.)")
    if r['src'] == 'papers/collected/collected.html':
        a = "Version 13 adds #38, Universal PiTet: The DICTO PiTet Proposition;"; assert t.count(a) == 1
        t = t.replace(a, "Version 14 adds #38a, The DICTO Kepler–Poinsot–UP Cycle, and records that from 20 October 2026 every paper listed here is released under CC BY-SA 4.0 (Attribution-ShareAlike): each has a new version with that licence, and earlier versions keep CC BY 4.0. Version 13 added #38, Universal PiTet: The DICTO PiTet Proposition;")
        row = '<tr><td class="n">#38</td>'; assert t.count(row) == 1
        t = t.replace(row, '<tr><td class="n">#38a</td><td><b>The DICTO Kepler–Poinsot–UP Cycle</b> (2026)</td><td>The tall companion to Universal PiTet: the great and small stellated dodecahedra in an endless φ³ cycle, every shell filled exactly by one pattern, in golden reciprocity.</td><td class="doi">DICTO DOI: 10.5281/zenodo.23464021</td></tr>' + row)
    if 'build_house.py' in r['src']:   # markdown papers: the italic meta line in paper.md and the print footer
        md = p.replace('build_house.py', 'paper.md'); s = open(md).read(); s2 = re.sub(r'\*Version \d+, [^·]+· doi:10\.5281/zenodo\.(\d+) · CC BY 4\.0\.', lambda mm: f'*Version {nv}, 20 October 2026 ({note}) · DICTO DOI: 10.5281/zenodo.{mm.group(1)} · CC BY-SA 4.0.', s)
        if s2 != s: open(md, 'w').write(s2); print('   md:', md.replace(K, ''))
        pm = p.replace('build_house.py', 'print.mjs'); s = open(pm).read(); s2 = re.sub(r' · v\d+</span>', f' · v{nv}</span>', s).replace('· doi:10.5281/', '· DICTO DOI: 10.5281/')
        assert s2 != s; open(pm, 'w').write(s2)
    open(p, 'w').write(t); plan.append(dict(r, new_version=nv))
    print(f"{r['src']}\n   - {old_line.strip()[:170]}\n   + {new_line.strip()[:170]}")
json.dump(plan, open('sa-batch/plan.json', 'w'), indent=1); print(len(plan), 'sources edited')
