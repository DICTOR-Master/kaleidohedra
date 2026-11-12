# One-off (13 Nov 2026): the References in the new chapter order (each draft chapter mapped to the chapters that now hold its
# text; the draft's Chapter 7 is split into Chapters centre1 and centre2), plus the works first cited in the expanded book.
import re, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ['open', 'three', 'kelvin', 'slider', 'bonds', 'rd', 'scut3', 'web', 'centre1', 'centre2', 'rosettes', 'walls', 'everyn', 'golden', 'family', 'bells']
MAP = {'o1': ['three'], 'o2': ['slider'], 'o3': ['bonds'], 'o4': ['rd'], 'o5': ['scut3'], 'o6': ['web'], 'o7': ['centre1', 'centre2'], 'o8': ['rosettes'], 'o9': ['walls'],
       'o10': ['web'], 'o11': ['everyn'], 'o12': ['golden'], 'o13': ['bells'], 'o14': ['family']}
s = open(os.path.join(H, 'references.html'), encoding='utf8').read()
def chlist(keys):
    keys = sorted(set(keys), key=ORDER.index)
    return ('Chapter ' if len(keys) == 1 else 'Chapters ') + ', '.join('{{ch:%s}}' % k for k in keys)
def expand(txt):
    ks = []
    for m in re.finditer(r'\{\{ch:(o\d+)\}\}–\{\{ch:(o\d+)\}\}|\{\{ch:(o\d+)\}\}', txt):
        if m.group(1):
            for n in range(int(m.group(1)[1:]), int(m.group(2)[1:]) + 1): ks += MAP['o%d' % n]
        else: ks += MAP[m.group(3)]
    return ks
def rep(m):
    whole = m.group(0)
    if 'record only for' in whole:
        a, b = whole.split('; record only for ')
        return chlist(expand(a)) + '; record only for ' + chlist(expand(b))
    return chlist(expand(whole))
s = re.sub(r'Chapters? \{\{ch:o\d+\}\}(?:(?:, |–| and |; record only for Chapters? )\{\{ch:o\d+\}\})*', rep, s)
ADD = [
 ('Debrunner', 'H. E. Debrunner, Über Zerlegungsgleichheit von Pflasterpolyedern mit Würfeln, <i>Arch. Math.</i> 35 (1980) 583–587 (Chapter {{ch:kelvin}}).'),
 ('Dehn', 'M. Dehn, Über den Rauminhalt, <i>Math. Ann.</i> 55 (1901) 465–478 (Chapter {{ch:kelvin}}).'),
 ('Duckworth', 'R. Duckworth and F. Stedman, <i>Tintinnalogia, or, The Art of Ringing</i>, London (1668) (Chapter {{ch:bells}}).'),
 ('Dutour Sikirić', 'M. Dutour Sikirić, A. Schürmann and F. Vallentin, A generalization of Voronoi\'s reduction theory and its application, <i>Duke Math. J.</i> 142 (2008) 127–164 (Chapter {{ch:walls}}).'),
 ('Gelfand', 'I. M. Gelfand, M. M. Kapranov and A. V. Zelevinsky, <i>Discriminants, Resultants, and Multidimensional Determinants</i>, Birkhäuser (1994) (Chapter {{ch:walls}}).'),
 ('McMullen, Representations', 'P. McMullen, Representations of polytopes and polyhedral sets, <i>Geom. Dedicata</i> 2 (1973) 83–99, doi:10.1007/BF00149284 (Chapter {{ch:walls}}).'),
 ('Steinhardt', 'P. J. Steinhardt, D. R. Nelson and M. Ronchetti, Bond-orientational order in liquids and glasses, <i>Phys. Rev. B</i> 28 (1983) 784–805, doi:10.1103/PhysRevB.28.784 (Chapter {{ch:slider}}).'),
 ('Weaire and Phelan', 'D. Weaire and R. Phelan, A counter-example to Kelvin\'s conjecture on minimal surfaces, <i>Phil. Mag. Lett.</i> 69 (1994) 107–110, doi:10.1080/09500839408241577 (Chapter {{ch:kelvin}}).'),
 ('Weaire and Rivier', 'D. Weaire and N. Rivier, Soap, cells and statistics: random patterns in two dimensions, <i>Contemp. Phys.</i> 25 (1984) 59–99, doi:10.1080/00107518408210979 (Chapter {{ch:scut3}}).')]
items = re.findall(r'<li>.*?</li>', s, re.S)
for k, t in ADD: items.append(f'<li>{t}</li>')
def sortkey(li):
    t = re.sub('<[^>]+>', '', li); return re.sub(r'^[A-Z][a-z]?\.(?:-[A-Z][a-z]?\.)?(?: [A-Z][a-z]?\.)*\s*', '', t).lower()
items.sort(key=sortkey)
i = s.index('<ol class="refs">') + len('<ol class="refs">'); j = s.index('</ol>')
s = s[:i] + '\n' + '\n'.join(items) + '\n' + s[j:]
# Kelvin, Gómez-Gálvez, Coxeter and others now also cited in new chapters
for name, keys in (('W. Thomson (Lord Kelvin)', ['kelvin']), ('P. Gómez-Gálvez', ['open', 'scut3', 'centre1']), ('G.-Th. Guilbaud', ['open']), ('P. H. Schoute', ['open']), ('J. E. Humphreys', ['web']), ('E. S. Fedorov', ['family'])):
    m = re.search(r'<li>' + re.escape(name) + r'.*?</li>', s, re.S)
    if not m: print('not found', name); continue
    li = m.group(0); mm = re.search(r'Chapters? (\{\{ch:[a-z0-9]+\}\}(?:, \{\{ch:[a-z0-9]+\}\})*)', li)
    if mm:
        ks = re.findall(r'\{\{ch:([a-z0-9]+)\}\}', mm.group(1)) + keys
        li2 = li.replace(mm.group(0), chlist(ks))
    else: li2 = li.replace('</li>', ' (' + chlist(keys) + ')</li>')
    s = s.replace(li, li2)
open(os.path.join(H, 'references.html'), 'w', encoding='utf8').write(s); print('items', len(items))
