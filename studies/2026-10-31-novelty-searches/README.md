# Prior-art searches, 31 October 2026

Requested by the main session for DICTO's decision: decide, as firmly as the evidence allows, whether six of DICTO's findings are known, partly known or not found, and search three earlier "not found" items more narrowly. Not for publication.

**Conclusion:** none of the six is fully in print, and each has known parts. The specific shapes of items 1–3 (leaning blue prism and blocks, DICTO FCC and the flattened rhombohedron, the other Bain elongated dodecahedron and the two skewed ones) were not found. Their families are classical (Fedorov 1885). The nearest work is Kostick 2020 (equal-edged Zome zonohedra) and Bilinski 1960. Keyed faces on golden rhombohedra go back to Ammann 1976, so RHOMBITURE should credit him; DICTO's one-mark rule and dowel pattern were not found. RVCMG's operation goes back to Kirkman ("convanesce") and Fuller's jitterbug. The Palintriacontahedron is a pentakis dodecahedron (known family). B1NR has the face pattern of the rectified 3D associahedron. HexOct: still not found.

**Status:** report typeset (`report.html`, PDF in ~/Documents/papers-to-read/novelty-searches.pdf); waiting for DICTO's read.

## Method

- DICTO's library: `ask-library` on dicto-big-brother, 21 queries (`data/library-queries.txt`, full output `data/library-results.txt`). dicto-big-brother answered ping but not SSH at first, so the 115 local PDFs of `~/Documents/kaleidohedra-references` were also searched by keyword after `pdftotext` (text kept in the session scratchpad only, not in git).
- Web: 30 searches (two in Japanese), 14 pages read. Every query and page is listed in the report, item by item.
- Not reached: zbMATH (HTTP 403), J-PlatPat (one Japanese patent-word web search stood in), Google Scholar (no direct access). Coxeter's *Regular Polytopes*, Socolar–Steinhardt 1986 and Katz 1988 are in copyright and were not read.

## Verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | Leaning blue hexagonal prism + blocks | PARTLY KNOWN (type: Fedorov 1885; Zome sub-cells: Kostick 2020; this member not found) |
| 2 | DICTO FCC + flattened rhombohedron | PARTLY KNOWN (type: Fedorov; analogue Bilinski 1960; cell not found) |
| 3 | Bain elongated dodecahedra | regular-hexagon form KNOWN (Grünbaum 2010 Fig. 2b); other one and the φ²+2, φ³+½ ones not found |
| 4 | EKP cell and network | PARTLY KNOWN (parts classical; Pm3̄ cluster crystals known; cell and network not found) |
| 5 | RHOMBITURE keyed dowels | PARTLY KNOWN (Ammann 1976 keyed faces; Longuet-Higgins 1987; Halfbakery 2026-09-01; DICTO's rule and pattern not found) |
| 6 | RVCMG | PARTLY KNOWN (Kirkman; jitterbug; Hoppe; Garland–Heckbert; connector state system not found) |
| A | HexOct | NOT FOUND (10 more sources) |
| B | DICTO Palintriacontahedron | KNOWN FAMILY (pentakis dodecahedron; ratio 3/√5 and name DICTO's) |
| C | B1NR straightened | PARTLY KNOWN (rectified associahedron pattern; equal-edged form not found; numerical) |

## Files

- `report.html`: the typeset report (uses ../../papers/paper.css and dicto-logo.png).
- `data/library-queries.txt`, `data/library-results.txt`: library queries and raw output.
