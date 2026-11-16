#!/usr/bin/env python3
"""Microcosm and Macrocosm (scutoid interactions): data/results.json + the prose below -> paper/paper.html (DRAFT for DICTO's read).

Usage: python3 scripts/make_html.py
Write-up only: no computation.

STRUCTURE (DICTO, 16 Nov): opening (the common thread) -> Part I the rule -> II the laboratory -> III microcosm
-> IV the Earth -> V macrocosm -> VI verdicts, open items, closed leads (appendix). One results table per part, same columns.

FOR UPDATES TO THE SUN (other streams edit only these, nothing else):
- the Sun row is ONE entry: data/results.json  rows["sun"]   (its "part" is "V");
- open item 3 is ONE entry: data/results.json  open["sun"]   (open items are numbered in their order in the file);
- the Sun figure caption is the one string SUN_CAPTION below.
Rows are keyed by id and carry their part; the part tables are built from them in file order.

Checks, then prints FINAL ok / FINAL FAIL:
- every verdict is one of the five words; at most 5 open items; every row has a part I to V;
- every source study folder named in a row or in the closed list exists;
- every row's system and verdict, and every open item, appear in README.md (README and PDF say the same);
- every row appears exactly once in the page;
- the one AI line appears exactly once in the page; no model names; no 'universal' wording.
"""
import html, json, re, sys
from pathlib import Path

here = Path(__file__).resolve().parent.parent
studies = here.parent
D = json.loads((here / 'data/results.json').read_text())
readme = (here / 'README.md').read_text()
fails = []
VERDICTS = ['ESTABLISHED', 'CONSISTENT', 'NOT CONFIRMED', 'NOT A TEST', 'PARKED']
PARTS = ['I', 'II', 'III', 'IV', 'V']
AI = 'Computation, proofs, verification and drafting with Claude (Anthropic).'
ROWS = D['rows']    # {id: row}; ROWS['sun'] is the Sun row
OPEN = D['open']    # {id: item}; OPEN['sun'] is open item 3

for k, r in ROWS.items():
    if r['verdict'] not in VERDICTS: fails.append(f'verdict {r["verdict"]}')
    if r.get('part') not in PARTS: fails.append(f'row {k}: part {r.get("part")}')
    for s in re.findall(r'20\d\d-\d\d-\d\d-[\w-]+', r['source']):
        if not (studies / s).is_dir(): fails.append(f'no study folder {s}')
    if r['system'] not in readme: fails.append(f'README lacks row {r["system"]}')
if len(OPEN) > 5: fails.append(f'{len(OPEN)} open items (at most 5)')
if list(OPEN).index('sun') != 2: fails.append('open["sun"] is not open item 3')
for o in OPEN.values():
    if o['item'] not in readme: fails.append(f'README lacks open item {o["item"]}')
for src, _, _ in D['closed']:
    if not any(p.name.endswith(src) for p in studies.iterdir()): fails.append(f'closed list: no study {src}')

e = lambda s: html.escape(s, quote=False)
def sym(s):  # plain ASCII in the data -> typeset symbols
    s = e(s)
    for a, b in (('sqrt 3', '√3'), ('+-', '±'), ('24 pi^2/35', '24π²/35'), ('pi', 'π'), ('^3', '³'), ('^2', '²'), ('<F>', '⟨F⟩'),
                 ('&lt;F&gt;', '⟨F⟩'), ('mu2', 'μ₂'), ('Delta a', 'Δa'), (' um', ' µm'), ("Theorem 1'", 'Theorem 1′')):
        s = s.replace(a, b)
    return s

counts = {v: sum(1 for r in ROWS.values() if r['verdict'] == v) for v in VERDICTS}
HEAD = '<tr><th>system · data</th><th>swaps observed</th><th>null or expectation</th><th>verdict · own wording</th><th>source (studies/)</th></tr>'
def table(part, caption):
    body = ''.join(f'<tr id="row-{k}"><td>{sym(r["system"])}<br><span class="d">{sym(r["data"])}</span></td><td>{sym(r["observed"])}</td><td>{sym(r["expected"])}</td>'
                   f'<td class="v">{r["verdict"]}<br><span class="d">{sym(r["own"])}</span></td><td class="d">{sym(r["source"])}</td></tr>'
                   for k, r in ROWS.items() if r['part'] == part)
    return f'<p class="tcap"><b>Table {part}.</b> {caption}</p><table class="r">{HEAD}{body}</table>'
summary = ''.join(f'<tr><td>{p}</td><td>{sym(r["system"])}</td><td class="v">{r["verdict"]}</td></tr>'
                  for p in PARTS for r in ROWS.values() if r['part'] == p)
opens = ''.join(f'<li id="open-{k}"><b>{sym(o["item"])}.</b> {sym(o["why"][0].upper() + o["why"][1:])}. <i>Next:</i> {sym(o["next"])}.</li>' for k, o in OPEN.items())
closed = ''.join(f'<tr><td>{e(s)}</td><td>{sym(l)}</td><td>{sym(c)}</td></tr>' for s, l, c in D['closed'])

# The Sun figure caption (part of the Sun entry; edit with rows["sun"] and open["sun"]).
SUN_CAPTION = ('Figure 1. The Sun row. Left: one frame of the Bifrost simulation en024048_hion (Gudiksen et al. 2011; Carlsson et al. 2016), '
               'vertical velocity 0.1 Mm below mean τ = 1, segmented into 206 granules; red: cells in a swap within the next 10 s, blue: split or merge. '
               'Right: persistent swaps per cell lifetime against time step, every setting. Every curve falls with the step: no stable rate yet '
               '(open item 3). From studies/2026-11-15-sun-granulation.')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Microcosm and Macrocosm</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;width:100%;font-size:7.6pt;margin:1mm 0 3mm;break-inside:auto}} td,th{{border:0.3pt solid #999;padding:0.7mm 1.2mm;vertical-align:top;text-align:left}} th{{background:#eee}} tr{{break-inside:avoid}} td.v{{font-weight:bold;white-space:normal}} .d{{font-weight:normal;color:#444;font-size:7pt}} table.r td:first-child{{width:20%}} table.r td:nth-child(2){{width:27%}} table.r td:nth-child(3){{width:19%}} table.r td:nth-child(4){{width:20%}} table.c td:first-child{{width:20%}} table.c td:nth-child(2){{width:36%}} table.s td:first-child{{width:7%}} table.s td:nth-child(2){{width:63%}} p.tcap{{font-size:8.5pt;margin:3mm 0 0;break-after:avoid}} h3{{font-size:10pt;margin:8pt 0 2pt;break-after:avoid}} p.why{{font-style:italic}} .opening p{{font-size:10.5pt}} h2.part{{break-before:page}} figure{{margin:3mm 0;text-align:center;break-inside:avoid}} figure img{{max-width:100%}} figcaption{{font-size:8.5pt;color:#444;text-align:left}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Microcosm and Macrocosm<br><span style="font-size:0.72em;font-weight:normal">Scutoid studies from cells to stars, planets and the cosmos</span></h1>
<div class="meta"><b>DICTO</b> · study of 16 November 2026 · consolidates the scutoid streams of 15 and 16 November 2026</div>
<div class="status">DRAFT for DICTO's read; not for publication. DICTO, 16 November 2026: "narrow our focus back to core study objectives and drop any avenues that are not supportive of the scutoid interactions and pull what we have into a study that has as few loose ends to tie up as possible". The narrowing covers the scutoid streams only.
<br><b>What this is.</b> A write-up of results already obtained: no new computation, data or jobs. Every number is copied from the source study named in its row (folders under studies/); each verdict is that study's own, never upgraded.
<br><b>Open for DICTO.</b> Title by DICTO (16 November 2026). Structure by DICTO (16 November 2026): an opening, then five parts from small to vast, then the verdicts. Whether the five open items in Part VI are the right five. The figure is reused from the Sun study (simulation data, public).</div>

<div class="opening">
<h2>The common thread</h2>
<p>This study sets side by side things that at first glance have nothing in common: the facets of an insect's eye, the growing layer of a yew, a soap froth and the grains of a metal, the plates of the Earth's crust, the cells of cloud over a cold sea, sea ice, the boiling surface of the Sun, the ring of storms at Jupiter's south pole, the bubbles blown by stars in the gas of the galaxy, and the great empty voids between the galaxies. They share one thing. Each is a space divided into cells, and the cells change over time: they grow, shrink, drift, appear and vanish.</p>
<p>When cells move against one another, their neighbours change. In a generic flat tiling, while no cell is born or dies, there is only one way this can happen at a single place: two cells that touched pull apart, and the two cells beside them come into contact. This is the swap of neighbours. (In a solid three-dimensional tiling the loss and the gain come apart, and contacts change one at a time.) Followed through a layer, a cell caught in a swap has a different number of sides at top and bottom, and the solid it fills is a scutoid. Biologists call the move T1; geometers call it the 2-2 move.</p>
<p>Geometry says how often the swap should happen. For cells placed at random and drifting apart, the rate is a fixed number that can be worked out in advance. For a tiling that is a slice through a solid in four dimensions, the number of swaps is fixed exactly by the shape of that solid.</p>
<p>So the same question can be asked at every scale. Do the swaps come one at a time, and how often do they come, measured against what the geometry expects?</p>
<p>This is a question about common geometric laws, or common denominators, and nothing more: the swap move itself, how swaps are counted, and the rate that geometry alone would give. The study does not claim a universal law of nature linking cells, the Earth and the stars. Different physics drives each system: growth in a tissue, surface tension in a froth, mantle flow under the plates, convection in clouds and in the Sun, gravity among the voids. What they can share is only the geometry of cells that divide a space and rearrange.</p>
<p>The parts follow in order of size. Part I sets out the rule and the yardstick. Part II tests the method on froths, grains and model foams, where the answer is known. Parts III to V apply it to living cells measured in micrometres, to the Earth in kilometres, and to the Sun and the cosmos in megametres and megaparsecs. Each part opens by saying why its systems belong, how large they are, and what they can and cannot test. Part VI says what holds, what does not, and the five things left to do.</p>
</div>

<h2 class="part">Part I. The rule</h2>
<p class="why">Before any system is measured, the yardstick: what a swap is, where it comes from, how it is counted, and what count to expect when nothing but the geometry of random cells is at work. Part I has no physical scale: its objects are polytopes and random tilings, measured in units of the cell spacing. It can fix the exact counts and the reference values; it cannot say whether any real system follows them.</p>
<h3>Where swaps come from</h3>
<p>Scutoids: Gómez-Gálvez et al. 2018 (Nat. Commun. 9, 2960); between concentric surfaces in foams: Mughal, Cox, Weaire, Burke and Hutzler 2018. DICTO, Scutoid Tissues in Four Dimensions, Paper #104 (Version 3, 11 November 2026; DICTO DOI 10.5281/zenodo.24111864), reads a tissue as a slice of a 4-polytope swept through space: Theorem 1 (a generic sweep of a simple 4-polytope changes by births, swaps and deaths, h₁, h₂, h₃ of them), Theorem 1′ (for a simple d-polytope, d ≥ 4, a corner changes the facets' contacts only by a birth, one contact gained, one contact lost, or a death; for d = 4 the gain and the loss come together as the swap, for d = 5 they are separate moves), Theorem 2 (the counts for the 120-cell, truncated 120-cell and bitruncated 600-cell). Moving 3D tilings are read as slices of a 5D sweep; the toy row (Part II) checks that reading by computation, not proof. DICTO, The Permutohedron Paradigm: Every Possible Order (DICTO DOI 10.5281/zenodo.24239019), Part Two, "Swaps inside cells: scutoid tissues": Chapter 6 (the swap of neighbours in a tissue is the scutoid) and Chapter 8 (the 4D permutohedron swept: 26 births, 66 swaps, 26 deaths), the neighbour-swap spine of the book.</p>
<h3>Counting rule</h3>
<p>One logger and one tiling format for 2D and 3D (studies/2026-11-15-event-logger), with Euler, triple-junction and balance checks and a negative control in every run. A swap is the 2-2 move: two cells stop touching and two others start. Three layers, fixed before counting: <i>pairing</i> (a lost contact a–b and a gained contact c–d make one swap if the four cells are distinct, c and d both touched a and b just before, and the two times differ by at most W); <i>persistence</i> (a change counts only if the new state lasts at least P; a back-and-forth within P cancels); <i>macroscopic</i> swaps by Rutenberg and McCurdy's own area rule (a T1 counts if all four cells exceed l² = r<sub>c</sub>√⟨A⟩). Pairing and persistence remove flicker but do not make raw swap counts step-independent: at a coarse step a swap falls into the same interval as a neighbouring cell's vanishing.</p>
<p><b>Streams that used a different setting.</b> Earth: contacts counted per boundary on a fixed 15 km mesh, two-sided persistence of 5 Myr (its own swaps.py). Sun: persistence 60 s at 10 s steps. Clouds: two-sided persistence 10 min. 2D grains: exact events from the vertex model, persistence by area fraction. Void toy: exact event times. Compound eyes: Delaunay neighbour sets compared between depths, not the logger. Jupiter: cyclic order of the published cyclone centres per epoch. None of these has a null rate of its own; only the toy, the froth and the 3D grains are compared with a reference value.</p>
<h3>Null model: the yardstick</h3>
<p>Poisson–Voronoi throughout: moving seeds with linear motion for rates (2D T1 per cell per spacing 3.058; 3D contact changes 15.61), and swept Poisson–Voronoi for swaps per birth (24π²/35 − 2 = 4.7677 for sections of a 3D tessellation; for any normal 3D tessellation k̄/2 − 3) (studies/2026-11-15-tissue-null-models; Meijering 1953, Miles 1970, Møller 1989). For coarsening froths the reference is the literature value 0.53 ± 0.05 macroscopic T1 per T2 (Rutenberg and McCurdy, arXiv cond-mat/0502287) and 3/2 with side-shedding (Herdtle and Aref 1992). Brownian seed motion gives no rate (counts scale as 1/δ); only the net change, which saturates, is frame-rate free.</p>
<p>The results tables of Parts I to V share one set of columns. Under each verdict stands the source study's own wording.</p>
{table('I', 'The rule: exact counts and the null model.')}

<h2 class="part">Part II. The laboratory</h2>
<p class="why">Froths, metal grains and model foams are the testing ground. A real soap froth has bubbles millimetres across and a metal has grains of micrometres, but here all of them are computer models, measured in pixels or cell spacings. In these models the swaps are read from the model itself rather than from pictures, and for the toy foams, the froth and the grains a reference value is known in advance. So the method is tested where the answer is known before it is used anywhere else. This part can test the counting rule and the reference values; it says nothing yet about living tissue, the Earth or the sky.</p>
{table('II', 'The laboratory: model foams, froth and grain growth in 2D and 3D.')}

<h2 class="part">Part III. Microcosm: living cells</h2>
<p class="why">Living tissue is where scutoids were first found, in curved sheets of cells (Gómez-Gálvez et al. 2018). A compound eye is a curved sheet of near-identical units, facets tens of µm across, traced here in X-ray volumes at 0.6 µm voxels; where the eye is curved unevenly, the geometry says the units must swap neighbours between the outer and inner surfaces. It is the one place in this study where a scutoid prediction was stated before the data were seen. The yew's cambium is the growing sheet of wood cells under the bark, cells tens of µm wide. Spectacle and lens hole arrays, with holes around a millimetre, are the made counterpart: columns of holes between two curved surfaces, showing how much curvature a regular array needs before it swaps. This part can test the geometric law of where swaps must begin; it cannot yet show a swap observed in a real eye.</p>
{table('III', 'Microcosm: compound eyes, yew cambium, spectacle hole arrays.')}

<h2 class="part">Part IV. The Earth</h2>
<p class="why">The Earth's surface is divided into cells at very different scales: tectonic plates thousands of km across that rearrange over hundreds of millions of years; open cells of cloud tens of km across that change within hours; and sea ice floes, from metres to kilometres. Here no answer is known in advance and there is no null rate, so the test is whether a count is stable: unchanged under a finer time step, and the same in independent records. The plates can test agreement between independent reconstructions of the past; the clouds and the ice test whether satellite pictures yield a stable rate at all. Neither can compare a rate with a reference value.</p>
{table('IV', 'The Earth: tectonic plates, cloud cells, sea ice.')}

<h2 class="part">Part V. Macrocosm: the sky</h2>
<p class="why">Beyond the Earth the cells grow vast. The Sun's surface is tiled by granules, convection cells about 1 Mm (1000 km) across that live for minutes, simulated here in a box 24 Mm wide: the only natural 2D tiling in this study with thousands of swaps. Jupiter's south pole holds a ring of five cyclones, each thousands of km across, watched by Juno for years. Interstellar bubbles, blown into the gas of the galaxy by stars, are tens of parsecs across. Cosmic voids, the empty basins of the galaxies' web, span Mpc; here they are basins smoothed at 3 to 6 Mpc/h in a simulated box of 256 Mpc/h. This part asks whether the same geometric rule can be read at astronomical sizes: whether contacts change one at a time and whether a rate is stable. Few of these systems can give a rate: the ring has too few cells, the bubbles have no time series, and the voids are built of voxels, which are not a generic tiling.</p>
{table('V', 'Macrocosm: the Sun, Jupiter, interstellar bubbles, cosmic voids.')}
<figure><img src="figures/sun_swaps.png" alt="granulation tiling with swaps, and swap rate against time step"><figcaption>{SUN_CAPTION}</figcaption></figure>

<h2 class="part">Part VI. What holds, what doesn't, and the five things left</h2>
<p class="why">The question throughout has been whether these systems share common geometric laws or denominators (the swap move, its counting, its expected rate from geometry), not whether one universal law of nature governs cells, the Earth and the stars.</p>
<h3>Verdicts</h3>
<p><b>Established:</b> the geometry. In a generic sweep of a simple 4-polytope the slice is a tissue whose cells are born, swap neighbours (the scutoid move) and die, counted exactly by the h-vector; in higher dimensions contacts are gained and lost one at a time (#104, Theorems 1, 1′ and 2). The shared event logger recovers these counts exactly, and the reference values for moving Voronoi tilings are fixed exactly or by two methods that agree (2D T1 rate 3.04 ± 0.005 against the integral 3.058 ± 0.005; 3D 15.53 ± 0.07 against 15.61 ± 0.03). <b>Consistent, at the strength of computation:</b> generic moving toy foams change one contact at a time (30,758 events, none simultaneous); a 2D froth in its scaling state gives 0.48 ± 0.02 macroscopic T1 per T2 against Rutenberg and McCurdy's 0.53 ± 0.05, but only at the natural cut-off; 3D grain growth obeys the contact identity. <b>Not established:</b> no natural tiling yet has a swap rate that is stable and comparable across scales (granules and cloud cells depend on the time step or the settings; the plate agreement within one model family does not carry over to an independent history), and no scutoid has been observed in a real compound eye (the butterfly traces are not a test of the prediction). The cross-scale comparison of the plan "One tissue, three scales" therefore cannot yet be made. The five open items below lead to it.</p>
<p>Verdicts over all {len(ROWS)} rows: ESTABLISHED {counts["ESTABLISHED"]}, CONSISTENT {counts["CONSISTENT"]}, NOT CONFIRMED {counts["NOT CONFIRMED"]}, NOT A TEST {counts["NOT A TEST"]}, PARKED {counts["PARKED"]}. By part, from small to vast (numbers and sources in Tables I to V):</p>
<table class="s"><tr><th>part</th><th>system</th><th>verdict</th></tr>{summary}</table>
<h3>Open (five)</h3>
<ol>{opens}</ol>

<h2 class="part">Appendix A. Closed leads</h2>
<p>Every lead of every source study. Where nothing else applies, the reason is DICTO's narrowing of 16 November 2026.</p>
<table class="c"><tr><th>source study</th><th>lead</th><th>closed: done, or dropped and why</th></tr>{closed}</table>

<h2>Credits</h2>
<p>Data and results of others, by row. Froth: cellular Potts model of Glazier, Gross and Stavans 1987; Stavans and Glazier 1989. Grains: Mason et al. 2015 (front tracking); Sprague, Patterson and Grandhi 2009; Wakai et al. 2001. Earth: plate models of Müller et al. 2016 and 2019, Matthews et al. 2016, Merdith et al. 2021, Scotese and Wright 2018 (PALEOMAP), Domeier and Torsvik 2014, read with pyGPlates (Müller et al. 2018) and GPlately (Mather et al. 2024); boundary formulas of Bird 2003. Sun: Bifrost (Gudiksen et al. 2011), runs of Carlsson, Hansteen, Gudiksen, Leenaarts and De Pontieu 2016 (Hinode Science Data Centre Europe); segmentation with scikit-image (van der Walt et al.). Clouds: Himawari-9 imagery observed by the Japan Meteorological Agency, mirrored by NOAA. Voids: pmwd (Li, Lanusse, Modi et al. 2022); basin tracking after Wojtak, Powell and Abel 2016; Meijering 1953. Eyes: ODA-3D tables of Currea, Sondhi, Kawahara and Theobald 2023 (CC BY 4.0; bee stack from Taylor et al.); X-ray volumes of Paukner et al. 2024 (BossDB, no licence stated: no images of them are reproduced here); Makarova et al. 2025; Kim et al. 2016. Jupiter: Mura et al. 2021, cyclone centres as supplied by Gavriel and Kaspi 2022 (Zenodo 6611745, CC BY 4.0); Adriani et al. 2020. Cambium: CoLuS (Katzenmaier and co-workers, Zenodo, CC BY 4.0). Froth reference values: Rutenberg and McCurdy; Herdtle and Aref 1992; Hinde and Miles 1980.</p>
<p>DICTO: ideas, names, constructions and direction, including the scutoid tissue, the swap theorem and the compound-eye prediction. {AI}</p>
</body></html>
'''
if page.count(AI) != 1: fails.append('AI line count')
if re.search(r'Opus|Sonnet|Haiku|Fable|claude-', page): fails.append('model name in page')
for k in ROWS:
    if page.count(f'id="row-{k}"') != 1: fails.append(f'row {k} not exactly once')
# 'universal' only where the text says the study does NOT claim it
for m in re.finditer(r'[^.]*\b(universal|nature obeys|same law everywhere)\b[^.]*\.', page, re.I):
    if not re.search(r'does not claim|not whether', m.group(0)): fails.append(f'universal wording: {m.group(0)[:80]}')
(here / 'paper/paper.html').write_text(page)
print(f'rows {len(ROWS)}, open {len(OPEN)}, closed {len(D["closed"])}; verdicts {counts}')
for f in fails: print('FAIL', f)
print('FINAL ' + ('FAIL' if fails else 'ok'))
sys.exit(1 if fails else 0)
