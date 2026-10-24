"""Verify every cited DOI on api.crossref.org; find DOIs by title (bibliographic query) where only the title was known.
Writes ../data/raw/crossref.json. A title query is accepted only if the returned title matches (checked by hand in README)."""
import json, os, urllib.request, urllib.parse, time
here = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'k-research scale-anomalies study (mailto:none)'}
dois = ["10.1107/S0567739476001551", "10.1021/ja01379a006", "10.1002/anie.202000829", "10.1103/PhysRevB.70.014113",
        "10.1103/PhysRevB.38.7755", "10.1103/PhysRevB.73.184120", "10.3389/fchem.2021.723507", "10.1103/PhysRevB.48.10074"]
titles = ["Accurate lattice parameter measurements of stoichiometric uranium dioxide",
          "The crystal structure of baddeleyite (monoclinic ZrO2)",
          "Phase transitions in lead(II) fluoride upon milling",
          "The thermal expansion of solid UO2 and (U, Pu) mixed oxides a review and recommendations",
          "High-temperature studies of UO2 and ThO2 using neutron scattering techniques",
          "Phase transitions and equations of state of alkaline earth fluorides CaF2, SrF2, and BaF2 to Mbar pressures",
          "Average structure and local configuration of excess oxygen in UO2+x",
          "Evidence of the negative thermal expansion of the UO2.00 fluorite local structure"]
def rec(m, q):
    return dict(query=q, ok=True, doi=m.get('DOI'), title=(m.get('title') or [''])[0], journal=(m.get('container-title') or [''])[0],
                year=(m.get('issued', {}).get('date-parts') or [[None]])[0][0], volume=m.get('volume'), page=m.get('page') or m.get('article-number'),
                authors=[(a.get('family') or a.get('name')) for a in m.get('author', [])][:8])
out = []
for d in dois:
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(d), headers=H), timeout=30))['message']
        r = rec(m, d)
    except Exception as e:
        r = dict(query=d, ok=False, error=str(e))
    out.append(r); print(json.dumps(r, ensure_ascii=False)); time.sleep(0.5)
for t in titles:
    try:
        u = "https://api.crossref.org/works?rows=2&query.bibliographic=" + urllib.parse.quote(t)
        items = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30))['message']['items']
        r = dict(query=t, candidates=[rec(m, t) for m in items])
    except Exception as e:
        r = dict(query=t, ok=False, error=str(e))
    out.append(r); print(json.dumps(r, ensure_ascii=False)); time.sleep(0.5)
json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'crossref.json'), 'w'), indent=1, ensure_ascii=False)
