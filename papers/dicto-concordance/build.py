#!/usr/bin/env python3
"""Build paper.html of The DICTO Concordance from concordance.json.
Each new paper is one small edit to concordance.json (papers, a strand line, names, concepts); then run: python3 build.py"""
import json, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'concordance.json')))
P, ST = D['papers'], {s['id']: s for s in D['strands']}
MON = {'09': 'September', '10': 'October', '11': 'November'}
e = html.escape


def date(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MON[m]} {y}'


def key(n):
    m = re.match(r'(\d+)(\w*)', n)
    return (int(m.group(1)), m.group(2))


def ref(n, title=False):
    p = P.get(n)
    s = f'<b>#{e(n)}</b>'
    if title and p:
        s += ' ' + e(p['title'])
        if p.get('draft'):
            s += ' <span class="dr">(draft)</span>'
    return s


def when(n):
    p = P.get(n, {})
    if p.get('draft'):
        return 'draft, ' + date(p['date']) if p.get('date') else 'draft'
    if not p.get('date'):
        return 'date to check'
    return date(p['date']) if p.get('date_first') else 'current version ' + date(p['date'])


def first_cell(f):
    m = re.match(r'#(\w+)(.*)', f)
    return f'<b>#{e(m.group(1))}</b>{e(m.group(2))}' if m else e(f)


out = []
w = out.append
w('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>The DICTO Concordance</title>\n<link rel="stylesheet" href="../paper.css">\n<style>'
  'p.hook{font-style:italic;color:#4a3f2a;border-left:2px solid #c9a24a;padding-left:3mm}'
  'table.grid{font-size:7.4pt;border-collapse:collapse;width:100%;table-layout:fixed}table.grid td,table.grid th{overflow-wrap:anywhere;word-break:break-word}table.grid td,table.grid th{border:1px solid #ccc;padding:0.6mm 1mm}td.gap{background:#fbeede}ol.rk li{margin-bottom:1mm}span.out{color:#4a3f2a}'
  '.status{border:2px solid #a00;border-radius:2mm;padding:2mm 3mm;margin:3mm 0;font-size:8.6pt;color:#300;background:#fff6f6}.status ul{margin:1mm 0 0 4mm;padding:0}'
  'h2{break-before:page}h2.first{break-before:auto}h3{font:600 10.5pt "DejaVu Sans",sans-serif;color:#6b5310;margin:9pt 0 2pt;break-after:avoid}'
  'p.about{margin:0 0 2pt;font-style:italic}ul.th{margin:0 0 2pt;padding-left:4mm;font-size:9.2pt}ul.th li{margin:0 0 1pt;break-inside:avoid}'
  'p.lk{font:8.4pt/1.35 "DejaVu Sans",sans-serif;color:#40350f;margin:1pt 0 1pt 4mm;break-inside:avoid}'
  'table{width:100%}table.big{font-size:7.6pt;break-inside:auto}table.big tr{break-inside:avoid}table.big td,table.big th{padding:0.6mm 1.2mm 0.6mm 0}thead{display:table-header-group}'
  '.dr{color:#a00}.cc{break-inside:avoid;margin:0 0 4pt;font-size:9.2pt}.cc .df{margin:0}.cc .mt{font:8pt/1.35 "DejaVu Sans",sans-serif;color:#333;margin:0 0 0 4mm}'
  'table.tri td.x{text-align:center;color:#6b5310;font-weight:600}table.tri th.x{text-align:center}table.tri{font-size:8.4pt}'
  'figure.f1 img{width:100%;display:block}figcaption{font-size:8.2pt}'
  '</style>\n</head><body>')
w('<img class="watermark" src="../dicto-logo.png" alt="">\n<img class="logo" src="../dicto-logo.png" alt="DICTO">')
w('<h1>The DICTO Concordance</h1>')
w('<p class="sub">A map and almanac of the work: threads, names, concepts and the one triangle</p>')
w(f'<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com · ORCID 0009-0001-2620-2036<br>'
  f'{date(D["date"])} · {e(D["version"])} · DICTO DOI: {D.get("doi", "to be reserved")} (concept) · Licence CC BY-SA 4.0 · Compiled with Claude (Anthropic) from the papers, the site cards and the DICTOnary, generated from concordance.json by build.py<br>'
  'The work, its ideas and its names are DICTO\'s, as each paper\'s credit line says; this map only gathers them.</div>')

w('<p class="hook">This is a map of DICTO\'s work in one place, so that no detail has to be carried in the head. '
  '<b>Threads</b> follow one idea from paper to paper; <b>Names</b> lists every named solid, piece, family and rule with who named it and where it first appears; '
  'the <b>Almanac of Concepts</b> says what each operation, law and method is and where it is used; '
  'the last page puts every thread on the one triangle of mirrors. To find anything, look it up in Names or the Almanac and follow the paper numbers.</p>')

# 1. Threads
w('<h2 class="first">1. Threads</h2>')
w(f'<p>{len(D["strands"])} threads run through the papers. Each paper is listed, in the order of its number, with one line on what it adds to the thread; '
  'a paper can sit on several threads. Lines marked → are the verified cross-links of the audit of 4 November 2026 (study 2026-11-04-cross-links, section A).</p>')
for i, s in enumerate(D['strands'], 1):
    w(f'<h3>1.{i} {e(s["name"])}</h3><p class="about">{e(s["about"])}</p><ul class="th">')
    for x in sorted(s['papers'], key=lambda x: key(x['n'])):
        w(f'<li>{ref(x["n"], True)}: {e(x["adds"])}</li>')
    w('</ul>')
    for l in s['links']:
        w(f'<p class="lk">→ {e(l)}</p>')

# 2. Names
w('<h2>2. Names</h2>')
w(f'<p>{len(D["names"])} entries, alphabetical (a leading “DICTO” is passed over in the order). “Named by” is taken from the paper\'s credit line or text; '
  '“see #N” means the text read for this draft does not say who chose the name; '
  'First: the paper or finding (F) where the name first appears; D: the number in the DICTOnary.</p>')
w('<table class="big"><thead><tr><th>Name</th><th>Named by</th><th>First</th><th>D</th><th>Also called · note</th></tr></thead><tbody>')
for x in D['names']:
    note = '; '.join(e(v) for v in (x.get('aka'), x.get('note')) if v)
    w(f'<tr><td>{e(x["name"])}</td><td>{e(x["by"])}</td><td>{first_cell(x["first"])}</td><td>{e(x.get("d", ""))}</td><td>{note}</td></tr>')
w('</tbody></table>')

# 3. Almanac
w('<h2>3. Almanac of Concepts</h2>')
w(f'<p>{len(D["concepts"])} concepts: operations, constructions, laws, theorems and methods, as distinct from the named shapes. '
  'Each definition is taken from the wording of the paper cited; then the first paper and its date, the papers that use it, its threads, and who proposed it.</p>')
for c in sorted(D['concepts'], key=lambda c: c['name'].lower()):
    used = ', '.join(f'#{n}' for n in sorted(c['used'], key=key)) or '—'
    th = '; '.join(ST[t]['name'] for t in c['strands'])
    w(f'<div class="cc" id="c-{e(c["id"])}"><p class="df"><b>{e(c["name"])}</b>. {e(c["definition"])}</p>'
      f'<p class="mt">First: {ref(c["first"], True)} ({when(c["first"])}) · Used in: {used} · Threads: {e(th)} · Proposed: {e(c["by"])}</p></div>')

# 4. Singularity
w('<h2>4. The Singularity: One Triangle</h2>')
w('<p>The Golden Ladder, chapter 1 (One Triangle, Three Numbers; The Golden Ladder, DICTO DOI: 10.5281/zenodo.23966554) shows that the five Platonic solids come from three kaleidoscopes, '
  'the spherical triangles with angles 90°, 60° and 180°/p for p = 3, 4, 5, and that each carries one number, 2 cos(180°/p): φ for the dodecahedron and icosahedron (p = 5), '
  '√2 for the cube and octahedron (p = 4), 1 for the tetrahedron (p = 3). At p = 6 the triangle is flat and tiles the plane under the close-packed layer of balls, the setting of the stacking papers. '
  'The table places each thread by its number world and by the dimensions its papers reach.</p>')
w('<figure class="f1"><img src="figures/fig1-kaleidoscopes.png" alt="The three spherical kaleidoscope triangles p = 3, 4, 5 and the flat one p = 6">'
  '<figcaption>The (2, 3, p) triangle for p = 3, 4, 5 on the sphere and p = 6 in the plane, with the number 2 cos(180°/p) of each (figure 1 of The Golden Ladder, chapter 1).</figcaption></figure>')
dims = ['2D', '3D', '4D', '6D', '8D']
w('<table class="tri"><thead><tr><th>Thread</th><th>Number world</th>' + ''.join(f'<th class="x">{d}</th>' for d in dims) + '<th>From</th></tr></thead><tbody>')
for r in D['triangle']:
    w(f'<tr><td>{e(ST[r["strand"]]["name"])}</td><td>{e(r["world"])}</td>' + ''.join(f'<td class="x">{"●" if d in r["dims"] else ""}</td>' for d in dims) + f'<td>{e(r["why"])}</td></tr>')
w('</tbody></table>')
w('<p>The golden cuts reach furthest, to the E8 lattice in eight dimensions (#90); OG and the cube–octahedron sweep reach six (#90, #91). '
  'The flat triangle (p = 6) carries the stackings, where φ enters through the Fibonacci stacking (#69). The placement is the compiler\'s reading of the papers named in the last column.</p>')
# 5. What is missing
G = D['gaps']
w('<h2>5. What Is Missing</h2>')
w('<p class="hook">Parts 1–4 hold what we know. This part holds what we do not: gaps inside the work, the open points the papers left, and, from other fields, '
  'results we did not know of that bear on ours. DICTO\'s point: the Concordance, the reference library and the Kaleidohedra engine together are the tool. '
  'Each entry is to carry three legs, the map (threads and papers it touches), the source (a library copy) and the engine (a view or test in the app); '
  'a missing leg is itself a gap (draft 2 carries the library leg for the outside finds; the engine leg follows), and each outside find moves from <i>to read</i> to <i>credited</i>, <i>tested</i>, and finally <i>ours</i>.</p>')
w('<h3>5.1 The grid: solids against operations</h3>')
w(f'<p>Papers where each operation is done for each solid; — marks a gap, ? an unsure entry. {e(G["colnames"])}.</p>')
w('<table class="grid"><thead><tr><th>Solid</th>' + ''.join(f'<th>{e(x)}</th>' for x in G['cols']) + '</tr></thead><tbody>')
for r in G['rows']:
    w('<tr><td>' + e(r[0]) + '</td>' + ''.join(f'<td class="{"gap" if v == "—" else ""}">{e(v)}</td>' for v in r[1:]) + '</tr>')
w('</tbody></table>')
w('<h3>5.2 The nearest gaps, ranked, inside and outside</h3><p>Ranked by how directly each follows from what is already proved (DICTO: most of the calculations are already done; the rest is arrangement and interpretation). '
  'DICTO\'s observation: the gaps inside the work are directly analogous to the gaps outside it, so it is one study. Each gap therefore names the outside work that bears on it (5.5); a gap with none is where to search outside next.</p><ol class="rk">')
def short(x):
    return e(x['cite'].split(',')[0] + ' … ' + x['cite'].split(',')[-1].strip() if x['cite'].count(',') > 1 else x['cite'])
for a, why, to, outs in G['ranked']:
    o = '; '.join(short(D['outside'][i]) for i in outs) if outs else '<i>none found yet: a search target</i>'
    w(f'<li><b>{e(a)}</b>. Why near: {e(why)}. Leads to: {e(to)}. <span class="out">Outside: {o}.</span></li>')
w('</ol>')
w('<h3>5.3 Open points left by the papers</h3>')
w(f'<p>{e(G["open_count"])}</p><table class="big"><thead><tr><th>Paper</th><th>Open point</th><th>Status</th></tr></thead><tbody>')
for x in G['loose']:
    w(f'<tr><td>{e(x["src"])}</td><td>{e(x["what"])}</td><td>{e(x["status"])}</td></tr>')
w('</tbody></table>')
w('<h3>5.4 Weak joins</h3><ul class="th">' + ''.join(f'<li>{e(x)}</li>' for x in G['weak']) + '</ul>')
w('<h3>5.5 From elsewhere: what other fields hold</h3>')
w('<p>Results from other fields, under other names, that bear on the threads and are not cited in any paper. Kind: <b>credit</b>, earlier or parallel work to cite; '
  '<b>test</b>, a check to run in the engine; <b>lead</b>, a direction to follow; <b>anchor</b>, the same mathematics in a real object or measurement. '
  'The strongest: the big bang billiard is the one triangle at p = ∞, so the ladder runs sphere (p = 3, 4, 5), plane (6), hyperbolic (7 and up), big bang (∞); '
  'the numbers 2 cos(π/p) are measured particle and anyon dimensions; and diamond growers\' shape dial is α = 3/μ, our core turn.</p>')
w('<table class="big"><thead><tr><th>Field</th><th>Source</th><th>What it holds</th><th>Touches</th><th>Kind</th><th>Library</th><th>Checked</th><th>Status</th></tr></thead><tbody>')
for x in D['outside']:
    w(f'<tr><td>{e(x["field"])}</td><td>{e(x["cite"])}</td><td>{e(x["says"])}</td><td>{e(x["touches"])}</td><td>{e(x["kind"])}</td>'
      f'<td>{"yes" if x["lib"] else "to fetch"}</td><td>{e(x["conf"])}</td><td>{e(x["status"])}</td></tr>')
w('</tbody></table>')
w('<h3>5.6 Waiting for their volume</h3><p>Results found since the last version, with their study folder and the volume or version they go into (released as soon as DICTO has read them).</p><table class="big"><thead><tr><th>Result</th><th>Study</th><th>Goes to</th></tr></thead><tbody>' + ''.join(f'<tr><td>{e(str(x.get("result", "")))}</td><td>{e(str(x.get("study", "")))}</td><td>{e(str(x.get("goes_to", "")))}</td></tr>' for x in G.get('waiting', [])) + '</tbody></table>')
w('<p>Fields not yet consulted, named by the search: dislocation theory (each h ↔ c swap is a partial-dislocation glide); commensurate–incommensurate transitions; '
  'semi-discrete optimal transport (the weight walk); martensitic paths (Burgers, Kurdjumov–Sachs); topological interlocking and architected materials; '
  'realisation spaces of polytopes; hypersimplices (the octahedron is Δ(2, 4)); fulleride and cluster chemistry; multiply-twinned nanoparticles; hyperbolic tilings and holography.</p>')
w('<h2>Notes on this version</h2><ul class="th">' + ''.join(f'<li>{x}</li>' for x in D['status']) + '</ul>')
if D.get('overlaps_note'):
    w('<h3>5.7 Overlaps across threads (4 November 2026)</h3><p>' + e(D['overlaps_note']) + '</p>')
# 6. Methods and code map
import os as _os
_cm = _os.path.join(HERE, 'code_map.json')
if _os.path.exists(_cm):
    CM = json.load(open(_cm))
    w('<h2>6. Methods and Code Map</h2>')
    w('<p class="hook">DICTO\'s idea: a map of which methods the studies share, so that when a method improves, or a fault is found in it, every result that rests on it can be found and re-checked, and so that shared methods can live in one library.</p>')
    w(f'<p>Scanned: {CM["scanned_files"]} study scripts. Only {len(CM["scripts_using_studies_lib"])} import the shared library studies/_lib; most methods exist as copies.</p>')
    w('<table class="big"><thead><tr><th>Method</th><th>Scripts</th><th>Studies</th><th>Studies using it (first 8)</th></tr></thead><tbody>')
    for m, v in CM['methods'].items():
        w(f'<tr><td>{e(m)}</td><td>{len(v["scripts"])}</td><td>{len(v["studies"])}</td><td>{e(", ".join(v["studies"]))}</td></tr>')
    w('</tbody></table>')
    top = list(CM['duplicated_functions_3plus_studies'].items())[:15]
    w('<p>Functions defined separately in three or more studies (most copied first): ' + e('; '.join(f'{k} ({len(v)})' for k, v in top)) + '.</p>')
    w('<p>Plan: move the core methods (harmonic fingerprint, forced-sector search, overlap test, polar sweeps, symmetric point sets, exact-check ledger) into studies/_lib with their own tests and calibrations; new studies import them; finished studies keep their copies so their published results stay reproducible. Matching is by function name and approximate (generated by code_map.py).</p>')
T_ = D.get('tests')
if T_:
    w('<h3>6.1 Tests against families: sets, subsets and gaps</h3>')
    w(f'<p>{e(T_["note"])}</p><table class="grid"><thead><tr><th>Family</th>' + ''.join(f'<th>{e(t)}</th>' for t in T_['tests']) + '</tr></thead><tbody>')
    for fam, cells in T_['families'].items():
        w('<tr><td>' + e(fam) + '</td>' + ''.join(f'<td class="{"gap" if v == "—" else ""}">{e(v)}</td>' for v in cells) + '</tr>')
    w('</tbody></table>')
w('</body></html>')
open(os.path.join(HERE, 'paper.html'), 'w').write('\n'.join(out))
print('paper.html:', len(D['strands']), 'threads,', len(D['names']), 'names,', len(D['concepts']), 'concepts')
