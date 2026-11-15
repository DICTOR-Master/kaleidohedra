"""README.md of studies/2026-11-15-stanley-check -> paper.html for print.mjs (formatting only)."""
import re, html
src = open('../../studies/2026-11-15-stanley-check/README.md').read().split('\n')
def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s); s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s); return s.replace('\\|', '|')
out = []; i = 1
while i < len(src):
    l = src[i]
    if l.startswith('## '):
        h = inl(l[3:]); out.append(f'<h2 style="break-before:page">{h}</h2>' if h.startswith('1. Sources') else f'<h2>{h}</h2>')
    elif l.startswith('|'):
        rows = []
        while i < len(src) and src[i].startswith('|'):
            cells = [c.strip() for c in re.split(r'(?<!\\)\|', src[i].strip())[1:-1]]
            if not all(re.fullmatch(r'-+', c) for c in cells): rows.append(cells)
            i += 1
        t = '<table><tr>' + ''.join(f'<th>{inl(c)}</th>' for c in rows[0]) + '</tr>'
        for r in rows[1:]: t += '<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>'
        out.append(t + '</table>'); continue
    elif re.match(r'\d+\. ', l):
        items = []
        while i < len(src) and re.match(r'\d+\. ', src[i]): items.append(re.sub(r'^\d+\. ', '', src[i])); i += 1
        out.append('<ol>' + ''.join(f'<li>{inl(x)}</li>' for x in items) + '</ol>'); continue
    elif l.strip() and l.strip() != 'DICTO · dictospheres.com': out.append(f'<p>{inl(l)}</p>')
    i += 1
verdict = out.pop(0)
hook = ("<p><i>A slice moving through a four-dimensional solid sees its cells born, trade neighbours and die. DICTO found that the trades "
        "balance: as many go one way as the other. This note checks, against the original papers, how much of that law mathematicians "
        "already knew, and in what words, and what stays DICTO's.</i></p>")
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Stanley check</title><link rel="stylesheet" href="../paper.css">
<style>table{{break-inside:auto;border-collapse:collapse;width:100%;font-size:8pt;margin:2mm 0}} td,th{{border:0.3pt solid #999;padding:0.8mm 1.4mm;vertical-align:top;text-align:left}} th{{background:#eee}} tr{{break-inside:avoid}} code{{font-size:8pt}} li{{margin-bottom:1.5mm}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>The Balance Laws against Stanley and Bayer–Billera<br><span style="font-size:0.72em;font-weight:normal">study of 15 November 2026; DICTO: "have we done the Stanley law check against our laws"</span></h1>
<div class="meta"><b>DICTO</b> · study note of 15 November 2026 · studies/2026-11-15-stanley-check</div>
<div class="status">DRAFT study note, for DICTO's reading; not for publication. The credit sentences of Section 5 are proposals: nothing in the books or papers has been edited. Revised 15 November after reading Stanley 1979 in full (DICTO's download).</div>
{hook}
{verdict}
{chr(10).join(out)}
<p>DICTO · dictospheres.com</p></body></html>'''
open('paper.html', 'w').write(doc)
