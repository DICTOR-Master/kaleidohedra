#!/usr/bin/env python3
"""Typeset sheet for DICTO: the homepage today vs the art-first prototype (screenshots from shot.mjs)."""
page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Art-First Homepage</title><link rel="stylesheet" href="../paper.css">
<style>.pair{display:flex;gap:4mm;align-items:flex-start}.pair figure{margin:0;flex:1;min-width:0;text-align:center}.pair img{width:100%;box-sizing:border-box;border:1px solid #ccc}
.pair figcaption{font-size:8.5pt;color:#555;margin-top:1mm} li{margin:1mm 0} .ph img{max-height:225mm;width:auto;max-width:100%}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Art-First Homepage<br><span style="font-size:0.72em;font-weight:normal">A prototype of the top of dictospheres.com (roadmap: art-first hero)</span></h1>
<div class="meta"><b>DICTO</b> · dictospheres.com · 8 November 2026 · Prototype built from the current page; the live page is unchanged. Prepared by Claude (Anthropic) for DICTO.</div>
<div class="status">Working document for DICTO, not on the site. Nothing changes on dictospheres.com until DICTO says so. The emblem, the name band and the D·I·C·T·O line are untouched. The video box waits for DICTO's own footage.</div>
<h2>What changes</h2>
<ul>
<li><b>A sentence first.</b> Under the name: "Sculptures from recycled PET bottles, built on the five perfect shapes, and the new geometry they led to."</li>
<li><b>The sculpture, large.</b> A 16:9 box for a video of B1NR "Int-aerium &amp; Ext-aerium" at Fumin Hall ALTI (the sculpture turning, light through the bottles, or the build). On a phone it fills the width of the screen.</li>
<li><b>One line about DICTO</b>, now with the six registered Japanese designs for joining PET bottles.</li>
<li><b>Three doors:</b> Start Here (main), Play RHOMBIS, Read the books and papers. The DICTO DOI badge stays, just below them.</li>
<li><b>Work moves from sixth place to first</b>, and inside it the sculpture and the registered designs now lead, then RHOMBITURE, then Kaleidohedra.</li>
<li><b>Start Here: three rules</b>, three cards that open the Start Here page at each rule. After them, the page continues as today: apps, books, papers, what's new, discoveries, follow, before you go.</li>
</ul>
<h2>Still needed before it can go live</h2>
<ul>
<li>DICTO's video (or a photo until then), and his two photos for the Start Here page.</li>
<li>The new lines in the site's other six languages (ja, es, fr, ko, zh, ru), as for every card today.</li>
<li>The Start Here page itself on the site (dictospheres.com/start-here/), with the nets as downloads.</li>
</ul>
<h2>Computer screen: today and the prototype</h2>
<div class="pair"><figure><img src="now-desk-c.png" alt="The homepage today"><figcaption>Today</figcaption></figure><figure><img src="proto-desk-c.png" alt="The art-first prototype"><figcaption>Prototype</figcaption></figure></div>
<h2>Phone: today and the prototype</h2>
<div class="pair ph"><figure><img src="now-phone.png" alt="The homepage today on a phone"><figcaption>Today</figcaption></figure><figure><img src="proto-phone.png" alt="The prototype on a phone"><figcaption>Prototype</figcaption></figure></div>
</body></html>'''
open('paper.html', 'w').write(page)
