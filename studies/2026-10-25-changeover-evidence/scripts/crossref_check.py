"""Look up every cited DOI on api.crossref.org and compare title / journal / volume / year with the citation.
Writes ../data/raw/crossref.json and ../data/checks/crossref-checks.txt.  'how read' records how each source was used."""
import json, os, time, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
REFS = [  # doi, expected title fragment, journal fragment, volume, year, how read
 ('10.1107/S0567739476001551', 'Revised effective ionic radii', 'Acta Cryst', '32', 1976, 'secondary: values via the Imperial College transcription (abulafia.mt.ic.ac.uk/shannon), not the printed table'),
 ('10.1021/ja01379a006', 'principles determining the structure of complex ionic crystals', 'American Chemical Society', '51', 1929, 'not re-read; limits derived exactly here'),
 ('10.6028/jres.068A.009', 'Lattice parameters and lattice energies of high-pressure polymorphs', 'Journal of Research', '68A', 1964, 'full text (NIST PDF; Table 2 read from the page image)'),
 ('10.1063/1.1655752', 'Pressure-Induced Phase Transformation in NaCl', 'Journal of Applied Physics', '39', 1968, 'not read; cited by Xu et al. for ~30 GPa'),
 ('10.1063/5.0231544', 'B1', 'Applied Physics Letters', '125', 2024, 'full text of the arXiv version 2209.10899 (NaCl B1->B2 at about 30 GPa)'),
 ('10.1002/anie.202000829', 'limited predictive power of the Pauling rules', 'Angewandte', '59', 2020, 'full text (DICTO library PDF): rule 1 holds for 66 % of environments'),
 ('10.1039/C5SC04845A', 'tolerance factor', 'Chemical Science', '7', 2016, 'full text (open access): 0.8 <= t <= 1 perovskites form, tilts in the lower part; mu > 0.41'),
 ('10.1016/j.jallcom.2003.10.017', 'Formability of ABO3 perovskites', 'Journal of Alloys and Compounds', '372', 2004, 'secondary (via Travis et al. 2016): 163/192 classified with 0.8 <= t <= 1'),
 ('10.1007/BF01507527', 'Gesetze der Krystallochemie', 'Naturwissenschaften', '14', 1926, 'not read; origin of t'),
 ('10.1088/1361-6633/aa892d', 'SrTiO', 'Reports on Progress in Physics', '81', 2018, 'full text of arXiv 1702.07690: SrTiO3 cubic at room T; t = 1.063 BaTiO3, 0.946 CaTiO3'),
 ('10.1103/PhysRevB.97.174108', 'First-principles study', 'Physical Review B', '97', 2018, 'full text of arXiv 1801.08886: BaTiO3 cubic -> P4mm at ~393 K; CaTiO3 Pnma'),
 ('10.1063/1.4729468', 'Transferable pair potentials for CdS and ZnS crystals', 'Journal of Chemical Physics', '136', 2012, 'full text of arXiv 1201.2992: experimental wurtzite->rock salt ~2.5 (CdSe), 2.5-3.2 (CdS), ~12 GPa (ZnS), secondary'),
 ('10.1063/1.5028279', 'From close-packed to topologically close-packed', 'Journal of Chemical Physics', '148', 2018, 'full text of arXiv 1803.03327: hard-sphere Laves for diameter ratio 1.19-1.35 (citing Hynninen et al. 2007)'),
 ('10.1038/nmat1841', 'Self-assembly route for photonic crystals', 'Nature Materials', '6', 2007, 'not read; source of the 1.19-1.35 hard-sphere Laves window per Lindquist et al.'),
 ('10.1107/S0365110X56002515', 'coordination number (12) radii for the', 'Acta Crystallographica', '9', 1956, 'not read; A15 radii exist here but were not available'),
 ('10.1016/j.physc.2015.02.013', 'Superconductivity in the A15 structure', 'Physica C', '514', 2015, 'full text of arXiv 1505.06393: no radius-ratio stability boundary given'),
]
out, lines = [], []
for doi, ti, jo, vol, yr, how in REFS:
    time.sleep(2)
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works/' + doi, headers={'User-Agent': 'k-research'}), timeout=30))['message']
        title = ' '.join(r.get('title') or ['']); cont = ' '.join(r.get('container-title') or ['']); v = r.get('volume'); y = (r.get('issued', {}).get('date-parts') or [[None]])[0][0]
        ok = ti.lower() in title.lower() and jo.lower() in cont.lower() and str(v) == vol and y == yr
        out.append(dict(doi=doi, title=title, journal=cont, volume=v, page=r.get('page'), year=y, ok=ok, how_read=how))
    except Exception as e:  # noqa
        ok = False; out.append(dict(doi=doi, error=str(e), ok=False, how_read=how))
    lines.append(f"{'PASS' if ok else 'FAIL'}  crossref {doi}  {out[-1].get('title', out[-1].get('error'))[:90]} | {out[-1].get('journal', '')} {out[-1].get('volume', '')} ({out[-1].get('year', '')})")
json.dump(out, open(os.path.join(here, '..', 'data', 'raw', 'crossref.json'), 'w'), indent=1)
open(os.path.join(here, '..', 'data', 'checks', 'crossref-checks.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
