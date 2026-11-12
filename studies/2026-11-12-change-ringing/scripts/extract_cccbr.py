"""Extract the stage 3-6 methods of the Central Council Collection of Methods (XML, CCCBR Methods Library,
https://methods.cccbr.org.uk/xml/CCCBR_methods.xml.zip, collection dated 2026-11-10, downloaded 12 Nov 2026) into a TSV:
id, stage, classification (+ little / differential / plain / trebleDodging flags), hunts, lead length, title, notation, lead head.
Usage: python3 extract_cccbr.py <zip> <out.tsv>.   DICTO · dictospheres.com - change-ringing study, 12 Nov 2026."""
import sys, zipfile, xml.etree.ElementTree as ET
zp, out = sys.argv[1], sys.argv[2]
NS = '{http://www.cccbr.org.uk/methods/schemas/2007/05/methods}'
z = zipfile.ZipFile(zp); name = z.namelist()[0]
root = ET.parse(z.open(name)).getroot()
print('collection date', root.get('date'))
rows = []
for ms in root.iter(NS + 'methodSet'):
    p = ms.find(NS + 'properties')
    stage = int(p.findtext(NS + 'stage'))
    if stage not in (3, 4, 5, 6): continue
    c = p.find(NS + 'classification')
    cls = (c.text or '').strip() if c is not None else ''
    flags = ','.join(k for k in sorted(c.attrib) if c.attrib[k] == 'true') if c is not None else ''
    lol = p.findtext(NS + 'lengthOfLead'); hunts = p.findtext(NS + 'numberOfHunts')
    for m in ms.findall(NS + 'method'):
        rows.append((m.get('id'), str(stage), cls or 'Principle', flags, hunts or '', lol or '', m.findtext(NS + 'title'),
                     m.findtext(NS + 'notation'), m.findtext(NS + 'leadHead') or ''))
with open(out, 'w') as f:
    f.write('# Central Council Collection of Methods (CCCBR), collection date %s; stages 3-6; source https://methods.cccbr.org.uk/ ; extracted for the DICTO change-ringing study (dictospheres.com)\n' % root.get('date'))
    f.write('id\tstage\tclass\tflags\thunts\tlead_length\ttitle\tnotation\tlead_head\n')
    for r in rows: f.write('\t'.join(r) + '\n')
from collections import Counter
print('methods by stage', dict(sorted(Counter(r[1] for r in rows).items())))
print('extract ok' if rows else 'extract FAIL no rows'); sys.exit(0 if rows else 1)
