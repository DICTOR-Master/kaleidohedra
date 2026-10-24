"""Verify candidate prior-art references on Crossref (api.crossref.org).
For each candidate: a DOI is looked up directly; the returned title/journal/
year/volume/page are stored and compared by hand in the README."""
import json, os, urllib.request, urllib.parse, time
here = os.path.dirname(os.path.abspath(__file__))
dois = [
 "10.1107/S0567739476001551",   # Shannon 1976
 "10.1021/ja01379a006",         # Pauling 1929 principles
 "10.1016/0022-3093(82)90093-X",# Gellatly & Finney 1982
 "10.1137/0216006",             # Aurenhammer 1987 power diagrams
 "10.1137/0214006",             # Imai Iri Murota 1985 Laguerre geometry
 "10.1080/08893110412331323170",# Blatov 2004 VDP crystal chemistry review
 "10.1038/nature03946",         # Leunissen et al 2005 ionic colloidal crystals (first guess 10.1038/nature04086 was wrong: found by Crossref query)
 "10.2172/4789465",             # Teatum, Gschneidner, Waber 1968 metallic radii report (OSTI; values not read)
 "10.1038/nature04414",         # Shevchenko et al 2006 binary NP superlattices
 "10.1126/science.1210493",     # Macfarlane et al 2011 NP superlattice engineering with DNA
 "10.1038/nature06560",         # Park et al 2008 DNA-programmable NP crystallization
 "10.1038/nature06508",         # Nykypanchuk et al 2008 DNA-guided crystallization
 "10.1103/PhysRevLett.96.018303",# Hynninen et al 2006 CuAu / CsCl oppositely charged colloids
 "10.1016/0022-2836(74)90570-1",# Richards 1974 protein volumes
 "10.1107/S0567739479001765",   # O'Keeffe 1979 coordination number def
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
