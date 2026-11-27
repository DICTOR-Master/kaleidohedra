import html
E=html.escape
models={a:open(a+'.txt').read().strip() for a in ['A002580','A005480','A270714']}
# key, label, required?, what-it-is, paste options (each a complete text), background-only text
F=[
('name','Name',True,'A one-line title saying what the number is. Choose one.',['Decimal expansion of 2/(3*(2^(1/3) - 1)).','Decimal expansion of (2/3)*(1 + 2^(1/3) + 2^(2/3)).'],None),
('data','Data',True,'The digits, separated by commas (105 digits, 209 characters).',['2,5,6,4,8,8,1,4,0,1,2,4,2,0,4,8,4,2,6,3,4,5,9,4,4,1,6,4,3,6,7,0,2,4,4,0,7,3,0,7,8,2,9,8,6,1,7,3,4,2,4,0,6,5,9,9,2,6,8,4,0,5,8,2,6,5,3,6,7,7,4,5,4,7,5,8,7,8,5,7,7,1,3,3,5,2,9,3,8,5,0,4,6,5,6,5,0,7,0,0,7,8,4,8,3'],None),
('offset','Offset',True,'Where the counting starts (the number is between 1 and 10). Paste exactly.',['1,1'],None),
('comments','Comments',False,'Extra explanation. The OEIS does not allow AI-written comments, so there is nothing ready to paste here: write it yourself, or leave it empty.',[],"Facts you could put in your own words: Samson (#51, The Delian Bond) is the cube with four alternate corners cut off at depth 2^(-1/3) (A270714) along the edges. Under the Star Cores core rule (#78) its first core is a truncated tetrahedron, and every later core is the same shape mirrored and scaled by t/3. In that truncated tetrahedron, the long side of each hexagon divided by the side of each triangle is this constant. Exact derivation: a cut at depth a gives the ratio 2a/(3(1 - a)); a = 2^(-1/3) gives 2/(3(2^(1/3) - 1))."),
('references','References',False,'Leave EMPTY: the sources have links, so they go under Links only.',[],None),
('links','Links',False,'Web links to the sources. NOT READY YET: the derivation must first be printed in a released paper (the link has to contain the claim).',["DICTO, <a href=\"https://doi.org/10.5281/zenodo.23529497\">The Delian Bond: Samson, Delilah and the Octet Between Kepler's Rhombic Dodecahedron and the Cube</a>, Zenodo (2026)."],"The Delian Bond link defines Samson and its cut. A second link, to the paper that prints the derivation, is added once that paper is released."),
('formula','Formula',False,'Exact formulas for the number. Choose one or both lines.',['Equals 2/(3*(2^(1/3) - 1)) = (2/3)*(1 + 2^(1/3) + 2^(2/3)).','Largest root of 27*x^3 - 54*x^2 - 36*x - 8 = 0.'],None),
('example','Example',False,'The number written out. Paste this line.',['2.564881401242048426345944164367024407307829861734241...'],None),
('program','Program',False,'Computer code that prints the digits. It has been run and checked against the Data line.',["(Python)\nfrom mpmath import mp, cbrt, floor\nmp.dps = 120\nx = 2/(3*(cbrt(2) - 1))\nd = []\nfor n in range(105):\n    k = int(floor(x)); d.append(k); x = (x - k)*10\nprint(d)"],None),
('xref','Crossrefs',False,'Related sequences. Paste exactly.',['Cf. A002580, A005480, A270714.'],None),
('keyword','Keywords',True,'Short tags. Paste exactly.',['nonn,cons,easy'],None),
]
o=[]
o.append('''<title>Samson Constant Worksheet</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
/* Layout: one column in OEIS form order; each field: what it is, paste-ready choices, your box. */
:root{--bg:#f6f7f9;--panel:#fff;--fg:#1d232b;--muted:#5a6573;--line:#d9dee5;--accent:#2f5d8a;--code:#eef1f5;--ok:#2e7d4f;--req:#a3461f;--note:#fbf6e8;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#13171c;--panel:#1b2128;--fg:#e4e8ee;--muted:#9aa5b2;--line:#2c343e;--accent:#8db7e0;--code:#222a33;--ok:#6cc08f;--req:#e59a74;--note:#2a2618;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#13171c;--panel:#1b2128;--fg:#e4e8ee;--muted:#9aa5b2;--line:#2c343e;--accent:#8db7e0;--code:#222a33;--ok:#6cc08f;--req:#e59a74;--note:#2a2618;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.55 var(--sans);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 48px}
main{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:18px}
h1{font-size:1.5rem;margin:0;text-wrap:balance}h2{font-size:1.1rem;margin:10px 0 0;color:var(--accent)}p{margin:0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:flex;flex-direction:column;gap:9px;min-width:0}
.top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.lab{font-weight:600;font-size:1.05rem}
.tag{font:600 .72rem var(--sans);letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:99px;border:1px solid}
.tag.r{color:var(--req);border-color:var(--req)}.tag.o{color:var(--muted);border-color:var(--line)}
.what{color:var(--muted)}
.sub{font:600 .78rem var(--sans);letter-spacing:.05em;text-transform:uppercase;color:var(--accent)}
.opt{display:flex;gap:8px;align-items:flex-start}
.n{font:600 .8rem var(--sans);color:var(--muted);padding-top:9px;min-width:1.4em}
pre{flex:1;min-width:0;margin:0;background:var(--code);border-radius:6px;padding:8px 10px;font:.86rem/1.5 var(--mono);white-space:pre-wrap;word-break:break-word}
.bg{background:var(--note);border-radius:6px;padding:8px 10px}
textarea{width:100%;box-sizing:border-box;min-height:3.4em;font:.9rem/1.5 var(--mono);color:var(--fg);background:var(--bg);border:1px dashed var(--line);border-radius:6px;padding:8px}
button{font:600 .8rem var(--sans);color:var(--accent);background:none;border:1px solid var(--accent);border-radius:6px;padding:4px 10px;cursor:pointer;white-space:nowrap}
button.ok{color:var(--ok);border-color:var(--ok)}button:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
details{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 14px}summary{cursor:pointer;font-weight:600}
.status{border-left:3px solid var(--accent);padding-left:12px}
</style>
<main>
<header style="display:flex;flex-direction:column;gap:8px">
<h1>OEIS worksheet: Samson's fixed-shape ratio 2/(3(&#8731;2 &minus; 1))</h1>
<p class="status">PREPARED, NOT YET TO SUBMIT. It waits for (1) a free place (three entries are open, the limit) and (2) a released paper that prints the derivation, for the Links line. Digits checked two independent ways to 140 places (the formula, and the root of the cubic, which is irreducible); the program prints exactly the Data line; not in the OEIS (searched 27 Nov: these digits, and those of 1 + &#8731;2 + &#8731;4 and &#8731;2 + &#8731;4).</p>
<p>How to use it: the fields are in the same order as the OEIS submission form. Each field says what it is and whether it is <b>required</b> or <b>optional</b>. Under <b>Ready to paste</b> are complete texts: choose one and press Copy. The box at the bottom of each field is yours to write in. At the end, <b>Copy my entry</b> collects what you wrote.</p>
</header>
''')
for key,lab,req,what,opts,bg in F:
    o.append(f'<div class="card"><div class="top"><span class="lab">{E(lab)}</span><span class="tag {"r" if req else "o"}">{"required" if req else "optional"}</span></div><p class="what">{E(what)}</p>')
    if opts:
        o.append(f'<p class="sub">Ready to paste{" — choose one" if len(opts)>1 and key not in ("program",) else ""}</p>')
        for i,t in enumerate(opts):
            num=f'<span class="n">{i+1}</span>' if len(opts)>1 else ''
            o.append(f'<div class="opt">{num}<pre>{E(t)}</pre><button type="button" class="cp">Copy</button></div>')
    if bg:
        o.append(f'<p class="sub">Background for you (not for pasting)</p><p class="bg">{E(bg)}</p>')
    o.append(f'<textarea id="f-{key}" data-label="{E(lab)}" aria-label="Your {E(lab)}" placeholder="Your {E(lab.lower())} (paste or write here)"></textarea></div>')
o.append('<div class="card"><div class="top"><span class="lab">Your whole entry</span><button type="button" id="all">Copy my entry</button></div><p class="what">Copies every field you filled in, labelled, in form order. Paste it back to me and I check it field by field.</p></div>')
o.append('<h2>Model entries to look at</h2><p class="what">Existing entries of the same kind, in full as the OEIS shows them. The letters mean: %N name, %S data, %F formula, %H links, %o program, %Y crossrefs, %K keywords, %O offset.</p>')
notes={'A002580':'cube root of 2: look at Name, Offset and the RealDigits / PARI lines.','A005480':'cube root of 4: the same short form, Offset 1,2.','A270714':"(1/2)^(1/3), Samson's cut depth: the shortest model (Name, %o, Keywords)."}
for a in ['A002580','A005480','A270714']:
    o.append(f'<details><summary>{a}: {E(notes[a])}</summary><pre style="margin-top:8px">{E(models[a])}</pre><p><a href="https://oeis.org/{a}" target="_blank" rel="noopener">Open {a} on the OEIS</a></p></details>')
o.append('''</main>
<script>
function flash(b,t){var o=b.id==='all'?'Copy my entry':'Copy';b.textContent=t;b.classList.add('ok');setTimeout(function(){b.textContent=o;b.classList.remove('ok')},1500)}
function copy(text,b,sel){try{navigator.clipboard.writeText(text).then(function(){flash(b,'Copied')},function(){sel&&sel();b.textContent='Selected'})}catch(e){sel&&sel();b.textContent='Selected'}}
document.querySelectorAll('button.cp').forEach(function(b){b.addEventListener('click',function(){var p=b.previousElementSibling;copy(p.innerText,b,function(){var r=document.createRange();r.selectNodeContents(p);var s=getSelection();s.removeAllRanges();s.addRange(r)})})});
document.querySelectorAll('textarea').forEach(function(t){try{var v=localStorage.getItem('samson-'+t.id);if(v)t.value=v}catch(e){}t.addEventListener('input',function(){try{localStorage.setItem('samson-'+t.id,t.value)}catch(e){}})});
document.getElementById('all').addEventListener('click',function(){var s=[];document.querySelectorAll('textarea').forEach(function(t){if(t.value.trim())s.push(t.dataset.label+':\\n'+t.value.trim())});copy(s.join('\\n\\n')||'(nothing written yet)',this)});
</script>''')
open('samson-constant.html','w').write('\n'.join(o))
print('ok')
