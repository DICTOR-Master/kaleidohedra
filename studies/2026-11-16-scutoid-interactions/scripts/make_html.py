#!/usr/bin/env python3
"""Scutoid interactions: data/results.json + the prose below -> paper/paper.html (DRAFT for DICTO's read).

Usage: python3 scripts/make_html.py
Write-up only: no computation. Checks, then prints FINAL ok / FINAL FAIL:
- every verdict is one of the five words; at most 5 open items;
- every source study folder named in a row or in the closed list exists;
- every row's system and verdict, and every open item, appear in README.md (README and PDF say the same);
- the one AI line appears exactly once in the page; no model names.
"""
import html, json, re, sys
from pathlib import Path

here = Path(__file__).resolve().parent.parent
studies = here.parent
D = json.loads((here / 'data/results.json').read_text())
readme = (here / 'README.md').read_text()
fails = []
VERDICTS = ['ESTABLISHED', 'CONSISTENT', 'NOT CONFIRMED', 'NOT A TEST', 'PARKED']
AI = 'Computation, proofs, verification and drafting with Claude (Anthropic).'

for r in D['rows']:
    if r['verdict'] not in VERDICTS: fails.append(f'verdict {r["verdict"]}')
    for s in re.findall(r'20\d\d-\d\d-\d\d-[\w-]+', r['source']):
        if not (studies / s).is_dir(): fails.append(f'no study folder {s}')
    if r['system'] not in readme: fails.append(f'README lacks row {r["system"]}')
if len(D['open']) > 5: fails.append(f'{len(D["open"])} open items (at most 5)')
for o in D['open']:
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

counts = {v: sum(1 for r in D['rows'] if r['verdict'] == v) for v in VERDICTS}
rows = ''.join(f'<tr><td>{sym(r["system"])}<br><span class="d">{sym(r["data"])}</span></td><td>{sym(r["observed"])}</td><td>{sym(r["expected"])}</td>'
               f'<td class="v">{r["verdict"]}<br><span class="d">{sym(r["own"])}</span></td><td class="d">{sym(r["source"])}</td></tr>' for r in D['rows'])
opens = ''.join(f'<li><b>{sym(o["item"])}.</b> {sym(o["why"][0].upper() + o["why"][1:])}. <i>Next:</i> {sym(o["next"])}.</li>' for o in D['open'])
closed = ''.join(f'<tr><td>{e(s)}</td><td>{sym(l)}</td><td>{sym(c)}</td></tr>' for s, l, c in D['closed'])

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Scutoid Interactions</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;width:100%;font-size:7.6pt;margin:2mm 0;break-inside:auto}} td,th{{border:0.3pt solid #999;padding:0.7mm 1.2mm;vertical-align:top;text-align:left}} th{{background:#eee}} tr{{break-inside:avoid}} td.v{{font-weight:bold;white-space:normal}} .d{{font-weight:normal;color:#444;font-size:7pt}} table.r td:first-child{{width:20%}} table.r td:nth-child(2){{width:27%}} table.r td:nth-child(3){{width:19%}} table.r td:nth-child(4){{width:20%}} table.c td:first-child{{width:20%}} table.c td:nth-child(2){{width:36%}} figure{{margin:3mm 0;text-align:center;break-inside:avoid}} figure img{{max-width:100%}} figcaption{{font-size:8.5pt;color:#444;text-align:left}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Scutoid Interactions<br><span style="font-size:0.72em;font-weight:normal">Neighbour swaps in changing tilings, from 4D polytopes to plates, granules, voids, grains and eyes: what holds, what does not, and the five things left</span></h1>
<div class="meta"><b>DICTO</b> · study of 16 November 2026 · consolidates the scutoid streams of 15 and 16 November 2026</div>
<div class="status">DRAFT for DICTO's read; not for publication. DICTO, 16 November 2026: "narrow our focus back to core study objectives and drop any avenues that are not supportive of the scutoid interactions and pull what we have into a study that has as few loose ends to tie up as possible". The narrowing covers the scutoid streams only.
<br><b>What this is.</b> A write-up of results already obtained: no new computation, data or jobs. Every number is copied from the source study named in its row (folders under studies/); each verdict is that study's own, never upgraded.
<br><b>Open for DICTO.</b> The title is a placeholder name, his to choose. Whether the five open items in Section 4 are the right five. The figure is reused from the Sun study (simulation data, public).</div>

<h2>1. Conclusion</h2>
<p><b>Established:</b> the geometry. In a generic sweep of a simple 4-polytope the slice is a tissue whose cells are born, swap neighbours (the scutoid move) and die, counted exactly by the h-vector; in higher dimensions contacts are gained and lost one at a time (#104, Theorems 1, 1′ and 2). The shared event logger recovers these counts exactly, and the reference values for moving Voronoi tilings are fixed exactly or by two methods that agree (2D T1 rate 3.04 ± 0.005 against the integral 3.058 ± 0.005; 3D 15.53 ± 0.07 against 15.61 ± 0.03). <b>Consistent, at the strength of computation:</b> generic moving toy foams change one contact at a time (30,758 events, none simultaneous); a 2D froth in its scaling state gives 0.48 ± 0.02 macroscopic T1 per T2 against Rutenberg and McCurdy's 0.53 ± 0.05, but only at the natural cut-off; 3D grain growth obeys the contact identity. <b>Not established:</b> no natural tiling yet has a swap rate that is stable and comparable across scales (granules and cloud cells depend on the time step or the settings; the plate agreement within one model family does not carry over to an independent history), and no scutoid has been observed in a real compound eye (the butterfly traces are not a test of the prediction). The cross-scale comparison of the plan "One tissue, three scales" therefore cannot yet be made. Section 4 lists the five open items that lead to it.</p>

<h2>2. One counting rule, one null model</h2>
<p><b>Counting rule.</b> One logger and one tiling format for 2D and 3D (studies/2026-11-15-event-logger), with Euler, triple-junction and balance checks and a negative control in every run. A swap is the 2-2 move: two cells stop touching and two others start. Three layers, fixed before counting: <i>pairing</i> (a lost contact a–b and a gained contact c–d make one swap if the four cells are distinct, c and d both touched a and b just before, and the two times differ by at most W); <i>persistence</i> (a change counts only if the new state lasts at least P; a back-and-forth within P cancels); <i>macroscopic</i> swaps by Rutenberg and McCurdy's own area rule (a T1 counts if all four cells exceed l² = r<sub>c</sub>√⟨A⟩). Pairing and persistence remove flicker but do not make raw swap counts step-independent: at a coarse step a swap falls into the same interval as a neighbouring cell's vanishing.</p>
<p><b>Null model.</b> Poisson–Voronoi throughout: moving seeds with linear motion for rates (2D T1 per cell per spacing 3.058; 3D contact changes 15.61), and swept Poisson–Voronoi for swaps per birth (24π²/35 − 2 = 4.7677 for sections of a 3D tessellation; for any normal 3D tessellation k̄/2 − 3) (studies/2026-11-15-tissue-null-models; Meijering 1953, Miles 1970, Møller 1989). For coarsening froths the reference is the literature value 0.53 ± 0.05 macroscopic T1 per T2 (Rutenberg and McCurdy, arXiv cond-mat/0502287) and 3/2 with side-shedding (Herdtle and Aref 1992). Brownian seed motion gives no rate (counts scale as 1/δ); only the net change, which saturates, is frame-rate free.</p>
<p><b>Streams that used a different setting.</b> Earth: contacts counted per boundary on a fixed 15 km mesh, two-sided persistence of 5 Myr (its own swaps.py). Sun: persistence 60 s at 10 s steps. Clouds: two-sided persistence 10 min. 2D grains: exact events from the vertex model, persistence by area fraction. Void toy: exact event times. Compound eyes: Delaunay neighbour sets compared between depths, not the logger. Jupiter: cyclic order of the published cyclone centres per epoch. None of these has a null rate of its own; only the toy, the froth and the 3D grains are compared with a reference value.</p>

<h2>3. Results</h2>
<p>One row per system. Verdicts: ESTABLISHED {counts["ESTABLISHED"]}, CONSISTENT {counts["CONSISTENT"]}, NOT CONFIRMED {counts["NOT CONFIRMED"]}, NOT A TEST {counts["NOT A TEST"]}, PARKED {counts["PARKED"]}. Under each verdict, the source study's own wording.</p>
<table class="r"><tr><th>system · data</th><th>swaps observed</th><th>null or expectation</th><th>verdict · own wording</th><th>source (studies/)</th></tr>{rows}</table>
<figure><img src="figures/sun_swaps.png" alt="granulation tiling with swaps, and swap rate against time step"><figcaption>Figure 1. The Sun row. Left: one frame of the Bifrost simulation en024048_hion (Gudiksen et al. 2011; Carlsson et al. 2016), vertical velocity 0.1 Mm below mean τ = 1, segmented into 206 granules; red: cells in a swap within the next 10 s, blue: split or merge. Right: persistent swaps per cell lifetime against time step, every setting. Every curve falls with the step: no stable rate yet (open item 3). From studies/2026-11-15-sun-granulation.</figcaption></figure>

<h2>4. Open (five)</h2>
<ol>{opens}</ol>

<h2>5. Closed</h2>
<p>Every lead of every source study. Where nothing else applies, the reason is DICTO's narrowing of 16 November 2026.</p>
<table class="c"><tr><th>source study</th><th>lead</th><th>closed: done, or dropped and why</th></tr>{closed}</table>

<h2>6. Theory cited</h2>
<p>DICTO, Scutoid Tissues in Four Dimensions, Paper #104 (Version 3, 11 November 2026; DICTO DOI 10.5281/zenodo.24111864): Theorem 1 (a generic sweep of a simple 4-polytope changes by births, swaps and deaths, h₁, h₂, h₃ of them), Theorem 1′ (for a simple d-polytope, d ≥ 4, a corner changes the facets' contacts only by a birth, one contact gained, one contact lost, or a death; for d = 4 the gain and the loss come together as the swap, for d = 5 they are separate moves), Theorem 2 (the counts for the 120-cell, truncated 120-cell and bitruncated 600-cell). Moving 3D tilings are read as slices of a 5D sweep; the toy row checks that reading by computation, not proof. DICTO, The Permutohedron Paradigm: Every Possible Order (DICTO DOI 10.5281/zenodo.24239019), Part Two, "Swaps inside cells: scutoid tissues": Chapter 6 (the swap of neighbours in a tissue is the scutoid) and Chapter 8 (the 4D permutohedron swept: 26 births, 66 swaps, 26 deaths), the neighbour-swap spine of the book. Scutoids: Gómez-Gálvez et al. 2018 (Nat. Commun. 9, 2960); between concentric surfaces in foams: Mughal, Cox, Weaire, Burke and Hutzler 2018.</p>

<h2>7. Credits</h2>
<p>Data and results of others, by row. Froth: cellular Potts model of Glazier, Gross and Stavans 1987; Stavans and Glazier 1989. Grains: Mason et al. 2015 (front tracking); Sprague, Patterson and Grandhi 2009; Wakai et al. 2001. Earth: plate models of Müller et al. 2016 and 2019, Matthews et al. 2016, Merdith et al. 2021, Scotese and Wright 2018 (PALEOMAP), Domeier and Torsvik 2014, read with pyGPlates (Müller et al. 2018) and GPlately (Mather et al. 2024); boundary formulas of Bird 2003. Sun: Bifrost (Gudiksen et al. 2011), runs of Carlsson, Hansteen, Gudiksen, Leenaarts and De Pontieu 2016 (Hinode Science Data Centre Europe); segmentation with scikit-image (van der Walt et al.). Clouds: Himawari-9 imagery observed by the Japan Meteorological Agency, mirrored by NOAA. Voids: pmwd (Li, Lanusse, Modi et al. 2022); basin tracking after Wojtak, Powell and Abel 2016; Meijering 1953. Eyes: ODA-3D tables of Currea, Sondhi, Kawahara and Theobald 2023 (CC BY 4.0; bee stack from Taylor et al.); X-ray volumes of Paukner et al. 2024 (BossDB, no licence stated: no images of them are reproduced here); Makarova et al. 2025; Kim et al. 2016. Jupiter: Mura et al. 2021, cyclone centres as supplied by Gavriel and Kaspi 2022 (Zenodo 6611745, CC BY 4.0); Adriani et al. 2020. Cambium: CoLuS (Katzenmaier and co-workers, Zenodo, CC BY 4.0). Froth reference values: Rutenberg and McCurdy; Herdtle and Aref 1992; Hinde and Miles 1980.</p>
<p>DICTO: ideas, names, constructions and direction, including the scutoid tissue, the swap theorem and the compound-eye prediction. {AI}</p>
</body></html>
'''
if page.count(AI) != 1: fails.append('AI line count')
if re.search(r'Opus|Sonnet|Haiku|Fable|claude-', page): fails.append('model name in page')
(here / 'paper/paper.html').write_text(page)
print(f'rows {len(D["rows"])}, open {len(D["open"])}, closed {len(D["closed"])}; verdicts {counts}')
for f in fails: print('FAIL', f)
print('FINAL ' + ('FAIL' if fails else 'ok'))
sys.exit(1 if fails else 0)
