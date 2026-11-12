"""Cover square for The Permutohedron Paradigm (DICTO 13 Nov 2026: "cover c" = Figure 13.1, Plain Bob Minimus as a red tour over the
labelled truncated octahedron). Re-draws Figure 13.1 with the chapter's own drawing code (studies/2026-11-12-change-ringing/scripts/figs.py,
executed from its file, not retyped) on a 1000 x 1000 square, without the figure's title line, with the DICTO mark.
Usage: python cover_svg.py <change-ringing study dir> <out.svg>"""
import sys, os
study, out = sys.argv[1], sys.argv[2]
src = open(os.path.join(study, 'scripts', 'figs.py')).read()
head = src[:src.index("F = D['figures']")]
sys.argv = ['figs.py', study]; g = {'__name__': 'figs'}; exec(compile(head, 'figs.py', 'exec'), g)
tour = g['D']['figures']['Plain Bob Minimus'][:24]
b = []; g['solid'](b, 500, 520, 172, 0.62, 0.18, tour, '', k=1.55)
W = H = 1000
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="white"/>'] + b
s.append(f'<text x="{W - 18}" y="{H - 18}" font-size="17" text-anchor="end" fill="#9a7b2f" font-family="Helvetica, Arial, sans-serif">DICTO · dictospheres.com</text></svg>')
open(out, 'w').write('\n'.join(s)); print('wrote', out, 'rows', len(tour))
