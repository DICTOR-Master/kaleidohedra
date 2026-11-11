#!/usr/bin/env python3
"""Roadmap: an everyday first line for the ten hardest paper cards (audit, section 3). The card text stays as it is;
the new line goes above it. Current card text is read live from ~/dictospheres/index.html (whole, never cut)."""
import re, html
s = open('~/dictospheres/index.html').read()
NEW = {
 '#38a': "Two of Kepler's spiky stars, one inside the other like Russian dolls, and the nesting goes on for ever, each doll the same golden step larger.",
 '#31a': "Around one of DICTO's Ogdoecontahedra, packed in its crystal, small golden pieces gather into a 50-faced star, the OCD Stella; copies of it fill about 87% of a room.",
 '#91': "Grow a shape inside its partner shape and watch the overlap change: DICTO played this game into four dimensions, where it gives solids that are golden in every cell.",
 '#89': "Slice a four-dimensional solid like a loaf of bread, and the golden pairs of the five perfect shapes turn up among the slices: DICTO found all five.",
 '#78': "Cut the truncated icosahedron from its centre into 32 pyramids, turn them inside out, and you have a star; DICTO found the truncated icosahedron and the star in one endless cycle.",
 '#74': "Tiny magnets in spin ice keep a two-in, two-out rule, like the hydrogen in water ice; DICTO showed their loops, and so their frozen-in disorder, stay the same however the layers are stacked.",
 '#54': "A gnomon is the piece that turns a shape into a bigger copy of itself, as each new chamber of a seashell does; DICTO carried it into three dimensions.",
 '#22': "An icosahedron and a dodecahedron, each filling the shell around the other, again and again like Russian dolls without end; DICTO built it to 20,497 pieces.",
 '#65': "A four-dimensional solid seen as layers, like the rings of an onion: 120 dodecahedra in nine layers, the same read forwards or backwards.",
 '#99': "All five perfect shapes nest one inside another, like dolls, in every cell of the octet climbing frame, and the nest repeats smaller and smaller for ever.",
}
ORDER = ['#38a', '#31a', '#91', '#89', '#78', '#74', '#54', '#22', '#65', '#99']
cards = {}
for m in re.finditer(r'<div class="paper[^"]*"[^>]*>(.*?)</div>', s, re.S):
    c = m.group(1); num = re.search(r'<span class="num">([^<]*)</span>', c)
    if not num or num.group(1).strip() not in NEW: continue
    t = lambda cls: html.unescape(re.sub(r'<[^>]+>', ' ', (re.search(rf'<span class="{cls}">(.*?)</span>', c, re.S) or [None, ''])[1])).strip()
    cards[num.group(1).strip()] = (re.sub(r'\s+', ' ', t('t')), re.sub(r'\s+', ' ', t('s')))
assert set(cards) == set(NEW), set(NEW) - set(cards)
rows = ''.join(f'''<div class="card"><p class="h">{html.escape(cards[k][0])}</p>
<p class="new">{html.escape(NEW[k])}</p><p class="old">{html.escape(cards[k][1])}</p></div>''' for k in ORDER)
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Everyday First Lines</title><link rel="stylesheet" href="../paper.css">
<style>.card{{border:1px solid #ddd;border-radius:2mm;padding:2.5mm 4mm;margin:3mm 0;page-break-inside:avoid}} .card .h{{font-weight:bold;margin:0 0 1.5mm}}
.card .new{{font-size:11.5pt;background:#faf4e4;border-left:3px solid #b8892a;padding:1.5mm 3mm;margin:0 0 1.5mm}} .card .old{{font-size:9pt;color:#555;margin:0}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Everyday First Lines<br><span style="font-size:0.72em;font-weight:normal">The ten hardest paper cards on dictospheres.com, each with a way in</span></h1>
<div class="meta"><b>DICTO</b> · dictospheres.com · 8 November 2026 · The ten cards the audit found hardest (formulas and technical words). Prepared by Claude (Anthropic) for DICTO.</div>
<div class="status">DRAFT for DICTO, not on the site. Each card keeps its text exactly; one new line in everyday words goes above it (gold box). Every line is DICTO's to keep, change or strike. Also proposed: #22's title loses the DOI it carries inside it (the DOI stays in its badge). After DICTO's yes: the lines in the six other languages, then the deploy queue.</div>
<p>How to read each card: the gold line is new and would open the card; the grey text below is the card as it is today, unchanged. The pictures come from the everyday-words glossary: Russian dolls, a loaf of bread, a football, onion rings, a seashell, water ice, a climbing frame.</p>
{rows}
</body></html>'''
open('~/k-research/papers/card-first-lines/paper.html', 'w').write(out)
print('ok', len(cards))
