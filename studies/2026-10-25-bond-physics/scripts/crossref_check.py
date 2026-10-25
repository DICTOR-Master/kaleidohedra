"""Verify candidate prior-art references on Crossref (api.crossref.org).
For each candidate: a DOI is looked up directly; the returned title/journal/
year/volume/page are stored and compared by hand in the README."""
import json, os, urllib.request, urllib.parse, time
here = os.path.dirname(os.path.abspath(__file__))
dois = [
 "10.1107/S0567739479001765",   # O'Keeffe 1979 coordination number definition (link 1)
 "10.1524/zkri.1979.150.1-4.23",# Hoppe 1979 ECoN (link 1)
 "10.1080/08893110412331323170",# Blatov 2004 VDP review (link 1)
 "10.3389/fchem.2021.723507",   # Fossati, Chartier, Boulle 2021 superionic fluorites (link 2)
 "10.1107/S0108768185002063",   # Brown & Altermatt 1985 bond valence parameters (link 3)
 "10.1021/cr900053k",           # Brown 2009 bond valence model review (link 3)
 "10.1063/1.1713597",           # Vallin, Beckman, Salama 1964 CsBr CsI elastic constants (link 4)
 "10.1063/1.1709358",           # Slagle & McKinstry 1967 CsCl CsBr CsI elastic constants (link 4)
 "10.1143/JPSJ.33.1361",        # TlCl elastic constants vs pressure 1972 (link 4, not read)
 "10.1016/0038-1098(67)90019-1",# TlBr elastic constants 1967 (link 4, not read)
 "10.1016/S0378-4371(98)00323-9",# Richard, Oger, Troadec, Gervois 1998 binary sphere tessellation (link 5)
 "10.1016/0022-3093(82)90093-X",# Gellatly & Finney 1982 radical tessellation (link 5)
 "10.1038/nature03946",         # Leunissen et al 2005 ionic colloidal crystals (link 5)
 "10.1107/S0567739476001551",   # Shannon 1976 radii (inputs)
]
out = []
for d in dois:
    u = "https://api.crossref.org/works/" + urllib.parse.quote(d)
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'k-research study (mailto:none)'}), timeout=30))['message']
        rec = dict(doi=d, ok=True, title=(m.get('title') or [''])[0], journal=(m.get('container-title') or [''])[0],
                   year=(m.get('issued', {}).get('date-parts') or [[None]])[0][0], volume=m.get('volume'), page=m.get('page'),
                   authors=[(a.get('family') or a.get('name')) for a in m.get('author', [])][:8])
    except Exception as e:
        rec = dict(doi=d, ok=False, error=str(e))
    out.append(rec); print(json.dumps(rec, ensure_ascii=False)); time.sleep(0.5)
json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'crossref.json'), 'w'), indent=1, ensure_ascii=False)

