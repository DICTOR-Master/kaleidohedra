import html
E=html.escape
models={a:open(a+'.txt').read().strip() for a in ['A003849','A085002']}
# key, label, required?, what-it-is, paste options (each a complete text), background-only text
F=[
('name', 'Name', True, 'A one-line title saying what the numbers count. Choose one.', ['Position (A, B, C = 0, 1, 2) of layer n in the Fibonacci stacking of close-packed layers: the layer types (c, h) follow the Fibonacci word, a(0) = 0, a(1) = 1.', 'Layer positions A, B, C = 0, 1, 2 of the close-packed stacking whose cubic and hexagonal layers follow the Fibonacci word, starting A, B.'], None),
('data', 'Data', True, 'The terms, separated by commas (130 terms, 259 characters).', ['0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2,0,1,2,1,0,2,0,1,0,2,1,2,0,1,0,2,0,1,2,1,0,1,2,0,2,1,0,1,2,1,0,2,0,1,0,2,1,2,0,1,0,2,0,1,2,1,0,2,0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2,1,2,0,2,1,0,1,2,1,0,2,0,1,2,1,0,1,2,0,2,1,2,0,1,0,2,1,2,0,2,1,0,1,2,0,2,1,2,0,1,0,2'], None),
('offset', 'Offset', True, 'Where the counting starts. Paste exactly.', ['0,4'], None),
('comments', 'Comments', False, 'Extra explanation. The OEIS does not allow AI-written comments, so there is nothing ready to paste here: write it yourself, or leave it empty.', [], "Facts you could put in your own words: a layer is hexagonal (h) when its two neighbours have the same position, cubic (c) otherwise (Jagodzinski); here layer n is h exactly when A003849(n) = 1, so the types follow the Fibonacci word c -> ch, h -> c; each step is +1 or -1 mod 3, a cubic layer repeats the step and a hexagonal one reverses it; first layer A and first step forward (the other choices permute 0, 1, 2); hexagonal layers never touch and their share is 1/phi^2 (#69); the first 16 terms, ABACBCACBABCACBC, are #69's 16-layer approximant."),
('references', 'References', False, 'Leave EMPTY: the source has a link, so it goes under Links only (a work goes in References or Links, never both).', [], None),
('links', 'Links', False, 'Web link to the source. Paste this line.', ['DICTO, <a href="https://doi.org/10.5281/zenodo.23721038">The Hexagonality Law and the Fibonacci Stacking</a>, Zenodo (2026).'], None),
('formula', 'Formula', False, 'A formula that gives the terms.', ['a(n) = (2*Sum_{k=2..n+1} A085002(k) - n) mod 3, i.e., the step from layer k to layer k+1 is 2*A085002(k+2) - 1.'], None),
('example', 'Example', False, 'A small case worked out. Paste these lines.', ['Layers 0..8 are A, B, A, C, B, C, A, C, B; layer types from layer 1 on: h, c, c, h, c, h, c, c (the Fibonacci word).'], None),
('program', 'Program', False, 'Computer code that prints the terms. It has been run and checked.', ["(Python)\ndef fib_stacking(N):   # a(0..N-1)\n    w = 'c'\n    while len(w) < N: w = ''.join('ch' if t == 'c' else 'c' for t in w)   # Fibonacci word\n    a = [0, 1]; s = 1\n    for k in range(1, N-1):\n        if w[k] == 'h': s = -s          # a hexagonal layer reverses the step\n        a.append((a[-1] + s) % 3)\n    return a[:N]\nprint(fib_stacking(130))"], None),
('xref', 'Crossrefs', False, 'Related sequences. Paste exactly.', ['Cf. A000201, A003849, A005614, A085002.'], None),
('keyword', 'Keywords', True, 'Short tags. Paste exactly.', ['nonn,easy'], None),
]
o=[]
o.append('''<title>Fibonacci Stacking Worksheet</title>
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
<h1>OEIS worksheet: the Fibonacci stacking of close-packed layers</h1>
<p class="status">Home paper #69, The Hexagonality Law and the Fibonacci Stacking (DICTO DOI 10.5281/zenodo.23721038), which prints the rule and the first 26 letters. Terms checked two independent ways to n = 1999 (the Fibonacci-word program, and the rule applied to the exact Beatty form of the Fibonacci word, with the Jagodzinski types recovered from the letters); not in the OEIS (searched 25 Nov).</p>
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
notes={'A003849':'the Fibonacci word itself: your layer types (h = 1).','A085002':'the sequence your Formula line uses for the steps.'}
for a in ['A003849','A085002']:
    o.append(f'<details><summary>{a}: {E(notes[a])}</summary><pre style="margin-top:8px">{E(models[a])}</pre><p><a href="https://oeis.org/{a}" target="_blank" rel="noopener">Open {a} on the OEIS</a></p></details>')
o.append('''</main>
<script>
function flash(b,t){var o=b.id==='all'?'Copy my entry':'Copy';b.textContent=t;b.classList.add('ok');setTimeout(function(){b.textContent=o;b.classList.remove('ok')},1500)}
function copy(text,b,sel){try{navigator.clipboard.writeText(text).then(function(){flash(b,'Copied')},function(){sel&&sel();b.textContent='Selected'})}catch(e){sel&&sel();b.textContent='Selected'}}
document.querySelectorAll('button.cp').forEach(function(b){b.addEventListener('click',function(){var p=b.previousElementSibling;copy(p.innerText,b,function(){var r=document.createRange();r.selectNodeContents(p);var s=getSelection();s.removeAllRanges();s.addRange(r)})})});
document.querySelectorAll('textarea').forEach(function(t){try{var v=localStorage.getItem('fibstack-'+t.id);if(v)t.value=v}catch(e){}t.addEventListener('input',function(){try{localStorage.setItem('fibstack-'+t.id,t.value)}catch(e){}})});
document.getElementById('all').addEventListener('click',function(){var s=[];document.querySelectorAll('textarea').forEach(function(t){if(t.value.trim())s.push(t.dataset.label+':\\n'+t.value.trim())});copy(s.join('\\n\\n')||'(nothing written yet)',this)});
</script>''')
open('entry6-fibonacci-stacking.html','w').write('\n'.join(o))
print('ok')
