#!/usr/bin/env python3
"""(from studies/2026-11-13-swaps-and-fixed-points via 2026-11-14-chat-handoff; header and status box changed, escaped \\| allowed in table cells) README.md -> paper/paper.html for the house print pipeline (headings, paragraphs, lists, pipe tables, **bold**, `code`)."""
import re, html, sys
src, out = sys.argv[1], sys.argv[2]
lines = open(src).read().split('\n')
def inl(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s
title = lines[0].lstrip('# ').strip()
body, i, para, lst = [], 1, [], None
def flush():
    global para, lst
    if para: body.append('<p>' + inl(' '.join(para)) + '</p>'); para = []
    if lst: body.append(f'<{lst[0]}>' + ''.join('<li>' + inl(x) + '</li>' for x in lst[1]) + f'</{lst[0]}>'); lst = None
while i < len(lines):
    l = lines[i]
    if l.startswith('|'):
        flush(); rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = [c.strip().replace('\x00', '|') for c in lines[i].replace('\\|', '\x00').strip().strip('|').split('|')]
            if not all(re.fullmatch(r'-+', c) for c in cells): rows.append(cells)
            i += 1
        h = '<tr>' + ''.join('<th>' + inl(c) + '</th>' for c in rows[0]) + '</tr>'
        b = ''.join('<tr>' + ''.join('<td>' + inl(c) + '</td>' for c in r) + '</tr>' for r in rows[1:])
        cls = ''
        body.append(f'<table{cls}><thead>{h}</thead><tbody>{b}</tbody></table>'); continue
    m = re.match(r'(#+) (.*)', l)
    if m: flush(); n = len(m.group(1)); body.append(f'<h{n}>{inl(m.group(2))}</h{n}>'); i += 1; continue
    m = re.match(r'\s*(- |\d+\. )(.*)', l)
    if m:
        if para: flush()
        kind = 'ul' if m.group(1) == '- ' else 'ol'
        if not lst or lst[0] != kind: flush(); lst = (kind, [])
        lst[1].append(m.group(2)); i += 1; continue
    if lst and l.startswith('   ') and l.strip(): lst[1][-1] += ' ' + l.strip(); i += 1; continue
    if not l.strip(): flush(); i += 1; continue
    if lst: flush()
    para.append(l.strip()); i += 1
flush()
status = ('DRAFT study of 14 November 2026, for DICTO\'s reading; not for publication as it stands. It runs the forced-fixed-points battery '
          '(swap, parity, symmetry, extra symmetry, values) on the DICTO silent zonohedron, the two-pyramid cuboctahedra and three fixed points from the '
          'swaps study\'s leads, with controls, in exact arithmetic on the compute hosts (121 + 15 checks, FINAL ok). Unpublished studies and drafts are named by folder.')
css = ('table{break-inside:auto;border-collapse:collapse;width:100%;font-size:7.6pt;margin:2mm 0} td,th{border:0.3pt solid #999;padding:0.7mm 1.2mm;'
       'vertical-align:top;text-align:left} th{background:#eee} tr{break-inside:avoid} code{font-size:8pt} h2{margin-top:5mm} '
       'table.t5{table-layout:fixed} table.t5 td:nth-child(1),table.t5 th:nth-child(1){width:7%} table.t5 td:nth-child(2),table.t5 th:nth-child(2){width:20%} table.t5 td:nth-child(3),table.t5 th:nth-child(3){width:13%} table.t5 td:nth-child(4),table.t5 th:nth-child(4){width:25%} table.t5 td:nth-child(5),table.t5 th:nth-child(5){width:35%} '
       'table.cat{break-before:page;table-layout:fixed} table.cat td:nth-child(1),table.cat th:nth-child(1){width:3%} table.cat td:nth-child(2),table.cat th:nth-child(2){width:8%} table.cat td:nth-child(3),table.cat th:nth-child(3){width:19%} table.cat td:nth-child(4),table.cat th:nth-child(4){width:15%} table.cat td:nth-child(5),table.cat th:nth-child(5){width:31%} table.cat td:nth-child(6),table.cat th:nth-child(6){width:10%} table.cat td:nth-child(7),table.cat th:nth-child(7){width:14%}')
doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title><link rel="stylesheet" href="../paper.css">'
       f'<style>{css}</style></head><body>\n<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">\n'
       f'<h1>Forced fixed points<br><span style="font-size:0.72em;font-weight:normal">The search for a law-giving shape, with controls</span></h1>\n'
       f'<div class="meta"><b>DICTO</b> · study of 14 November 2026 · with Claude Code (Opus)</div>\n<div class="status">{status}</div>\n'
       + '\n'.join(body[1:] if body and body[0].startswith('<h1') else body) + '\n</body></html>\n')
open(out, 'w').write(doc)
print('wrote', out, len(doc))
