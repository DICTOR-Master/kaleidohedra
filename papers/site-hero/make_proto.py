#!/usr/bin/env python3
"""Roadmap: art-first homepage hero, PROTOTYPE ONLY. Reads ~/dictospheres/index.html (never writes it),
writes proto/index.html beside a copy of the site's assets for screenshots. Emblem/nameband untouched."""
import re, sys
src = open('~/dictospheres/index.html').read()
out = sys.argv[1] if len(sys.argv) > 1 else 'proto-index.html'
LIVE = '--live' in sys.argv  # live: no video box until DICTO's footage exists

old_bio = re.search(r'\s*<p class="bio">.*?</p>', src, re.S).group(0)
old_doi = re.search(r'\s*<!-- Zenodo DOI badge.*?</div>', src, re.S).group(0)
old_start = re.search(r'\s*<p class="start">.*?</p>', src, re.S).group(0)
for x in (old_bio, old_doi, old_start): assert src.count(x) == 1

hero = '''
      <p class="tagline">Sculptures from recycled PET bottles, built on the five perfect shapes, and the new geometry they led to.</p>
      <div class="hero-media" role="img" aria-label="Video placeholder">
        <span>VIDEO: B1NR “Int-aerium &amp; Ext-aerium”, Fumin Hall ALTI, Kyoto<br><small>DICTO's own footage: the sculpture turning, the light through the bottles, or the build</small></span>
      </div>
      <p class="bio">Geometric sculptor in Osaka · Modular systems: <b>B1NR</b> / <b>DICTOspheres</b> · six registered Japanese designs for joining PET bottles</p>
      <p class="start"><a class="main" href="start-here/">Start Here</a><a href="https://rhombiverse.dictospheres.com/rhombis.html">Play RHOMBIS</a><a href="#books">Read the books and papers</a></p>''' + old_doi
if LIVE: hero = re.sub(r'\s*<div class="hero-media".*?</div>', '', hero, flags=re.S); assert 'hero-media' not in hero
s = src.replace(old_bio, '', 1).replace(old_doi, '', 1).replace(old_start, hero, 1)

rules = '''
    <h2>Start Here: three rules</h2>
    <ul class="rules">
      <li><a href="start-here/#rule-1"><b>1</b><span class="t">There are five perfect shapes</span><span class="s">The five dice: Dodecahedron, Icosahedron, Cube, Tetrahedron, Octahedron</span></a></li>
      <li><a href="start-here/#rule-2"><b>2</b><span class="t">Fill space with no gaps</span><span class="s">Like packing a car boot with no air left between the boxes</span></a></li>
      <li><a href="start-here/#rule-3"><b>3</b><span class="t">Layers can stack in any order</span><span class="s">Oranges on a market stall: each layer carries straight on, or turns back</span></a></li>
    </ul>
'''
# move Work up: right after the header, then the three rules, then the apps
work = re.search(r'\n    <h2>Work</h2>\s*<ul class="links">.*?</ul>\n', s, re.S).group(0)
s = s.replace(work, '\n', 1)
# art first inside Work too: the sculpture and the registered designs lead
lis = re.findall(r'\s*<li>.*?</li>', work, re.S); assert len(lis) == 4
order = [l for l in lis if 'B1NR' in l] + [l for l in lis if 'Design Registration' in l] + [l for l in lis if 'RHOMBITURE' in l] + [l for l in lis if 'Kaleidohedra by DICTO' in l]
assert len(order) == 4
work = work.replace(''.join(lis), ''.join(order))
s = s.replace('</header>\n', '</header>\n' + work + rules, 1)
css = '''
  .tagline{font-size:1.35rem;line-height:1.4;max-width:34rem;margin:.6rem auto 1rem;text-align:center;color:var(--text)}
  .hero-media{aspect-ratio:16/9;width:100%;max-width:880px;margin:0 auto 1rem;border-radius:14px;border:2px dashed rgba(var(--gold-rgb),.55);
    background:radial-gradient(ellipse at center,rgba(var(--gold-rgb),.14),transparent 70%);display:flex;align-items:center;justify-content:center;text-align:center;color:var(--gold);padding:16px;font-weight:600}
  .hero-media small{color:var(--muted);font-weight:400}
  ul.rules{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:12px}
  ul.rules a{display:block;border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--text);height:100%}
  ul.rules b{display:inline-block;width:30px;height:30px;border:2px solid var(--gold);border-radius:50%;text-align:center;line-height:26px;color:var(--gold);margin-bottom:6px}
  ul.rules .t{display:block;font-weight:700} ul.rules .s{display:block;color:var(--muted);font-size:.92rem}
  .doi-badges{margin-top:.8rem;transform:scale(.85)}
'''
s = s.replace('</style>', css + '</style>', 1)
open(out, 'w').write(s)
print('written', out, len(s))
