import html
E=html.escape
models={a:open(a+'.txt').read().strip() for a in ['A400949','A402231']}
# key, label, required?, what-it-is, paste options (each a complete text), background-only text
F=[
('name','Name',True,'A one-line title saying what the numbers count. Choose one.',
 ['Number of closed non-backtracking walks of length n (cyclically non-backtracking, i.e., tailless) starting and ending at a fixed site of the pyrochlore network.',
  'Number of closed tailless non-backtracking walks of length n at a site of the pyrochlore network.'],None),
('data','Data',True,'The terms, separated by commas.',
 ['0,0,12,12,0,276,756,2988,16104,64800,278916,1286352,5738928,25845036,118098612,540178572,2482501704,11470845192,53186644596,247472898972,1155354197016,5409675441324,25398322598892,119545910744592,563987677987800,2666471876270592,12632008967689620'],None),
('offset','Offset',True,'Where the counting starts. Paste exactly.',['1,3'],None),
('comments','Comments',False,'Extra explanation. The OEIS does not allow AI-written comments, so there is nothing ready to paste here: write it yourself, or leave it empty.',
 [],'What you could say, in your own words: these walks never step straight back, not even across the start; #102 Corollary 2 proves that every site of the pyrochlore network of every close-packed stacking has these same numbers; the pyrochlore network is the line graph of the diamond network.'),
('references','References',False,'Books and papers without a web link. Leave this EMPTY: the source has a link, so it goes under Links.',[],None),
('links','Links',False,'Web links to sources. Paste this line.',
 ['DICTO, <a href="https://doi.org/10.5281/zenodo.24037664">Every Site Hears the Same: the Loop Equality Is a Theorem</a>, Zenodo (2026).'],None),
('formula','Formula',False,'A formula that gives the terms. Option 1 can go in now. Option 2 needs the A-number of your pyrochlore closed-walks entry in place of A??????, so add it once that number is known.',
 ['Sum_{n>=1} a(n)*x^n/n = -2*log(1-x^2) - (1/2)*log(1+6*x^2+25*x^4) + Sum_{k>=1} A002895(k)*(x/(1-2*x+5*x^2))^(2*k)/(4*k) (Ihara-Bass formula for a 6-regular net).',
  'G.f.: 4*x^2/(1-x^2) - 10*x^2/(1+5*x^2) + ((1-5*x^2)/(1+5*x^2))*(P(x/(1+5*x^2)) - 1), where P(x) is the g.f. for A??????.'],None),
('example','Example',False,'Small cases worked out. Paste these lines.',
 ['a(3) = 12: the site lies on 6 triangles, and each triangle can be walked in 2 directions.\na(4) = 12: the site lies on 2 tetrahedra, each with 3 four-cycles through the site, and each four-cycle can be walked in 2 directions.'],None),
('program','Program',False,'Computer code that prints the terms. It has been run and checked.',
 ['(Python)\nfrom math import comb\nfrom fractions import Fraction\ndef domb(m):  # A002895\n    return sum(comb(m,k)**2*comb(2*k,k)*comb(2*m-2*k,m-k) for k in range(m+1))\ndef w(n):  # closed n-step walks per pyrochlore site\n    return (sum(comb(n,2*i)*2**(n-2*i)*domb(i) for i in range(n//2+1)) + (-2)**n)//2\ndef loops(W, q):  # Ihara-Bass per vertex of a (q+1)-regular net; W[i] = closed i-step walks\n    M = len(W)-1; c = [Fraction(0)]*(M+1)\n    for k in range(1, M//2+1): c[2*k] += Fraction(q-1, 2*k)\n    for j in range(1, M+1):\n        for i in range(j+1):\n            if 2*j-i <= M: c[2*j-i] += Fraction(comb(j,i)*W[i]*(-q)**(j-i), j)\n    return [int(m*c[m]) for m in range(1, M+1)]   # lengths 1..M\nprint(loops([w(i) for i in range(28)], 5))'],None),
('xref','Crossrefs',False,'Related sequences. Choose one. Option 2 adds your pyrochlore closed-walks entry once it has its number.',['Cf. A002895, A400949, A402231.','Cf. A002895, A400949 (diamond analog), A402231 (fcc analog), A??????.'],None),
('keyword','Keywords',True,'Short tags. Paste exactly.',['nonn,walk'],None),
]
o=[]
o.append('''<title>Pyrochlore Loops Worksheet</title>
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
<h1>OEIS worksheet: closed tailless walks on the pyrochlore network</h1>
<p class="status">Home paper #102 Corollary 2 (DICTO DOI 10.5281/zenodo.24037664). #102 prints the first 8 terms. Terms checked two independent ways to n = 40 (a direct count with no formula, and the Ihara-Bass formula); not in the OEIS (searched 24 Nov).</p>
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
notes={'A400949':'your own approved entry, the diamond analog: copy the shape of its name, log formula and program.','A402231':'your own approved entry, the fcc analog: its G.f. line and example have the same shape.'}
for a in ['A400949','A402231']:
    o.append(f'<details><summary>{a}: {E(notes[a])}</summary><pre style="margin-top:8px">{E(models[a])}</pre><p><a href="https://oeis.org/{a}" target="_blank" rel="noopener">Open {a} on the OEIS</a></p></details>')
o.append('''</main>
<script>
function flash(b,t){var o=b.id==='all'?'Copy my entry':'Copy';b.textContent=t;b.classList.add('ok');setTimeout(function(){b.textContent=o;b.classList.remove('ok')},1500)}
function copy(text,b,sel){try{navigator.clipboard.writeText(text).then(function(){flash(b,'Copied')},function(){sel&&sel();b.textContent='Selected'})}catch(e){sel&&sel();b.textContent='Selected'}}
document.querySelectorAll('button.cp').forEach(function(b){b.addEventListener('click',function(){var p=b.previousElementSibling;copy(p.innerText,b,function(){var r=document.createRange();r.selectNodeContents(p);var s=getSelection();s.removeAllRanges();s.addRange(r)})})});
document.querySelectorAll('textarea').forEach(function(t){try{var v=localStorage.getItem('pyroloop-'+t.id);if(v)t.value=v}catch(e){}t.addEventListener('input',function(){try{localStorage.setItem('pyroloop-'+t.id,t.value)}catch(e){}})});
document.getElementById('all').addEventListener('click',function(){var s=[];document.querySelectorAll('textarea').forEach(function(t){if(t.value.trim())s.push(t.dataset.label+':\\n'+t.value.trim())});copy(s.join('\\n\\n')||'(nothing written yet)',this)});
</script>''')
open('sweep2-pyrochlore-tailless.html','w').write('\n'.join(o))
print('ok')
