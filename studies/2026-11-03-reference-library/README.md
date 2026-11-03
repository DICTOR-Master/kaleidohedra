# 2026-11-03 Reference library: every work cited in DICTO's papers

DICTO's idea (3 November 2026): "perhaps every single reference paper and book can go into our collected works library". This study gathers every work cited in papers #1–#88 and the books, matches each against the private reference library (`~/Documents/kaleidohedra-references`), files a legal copy or a link entry for every work the library did not have, and drafts one bibliography for the Collected Works Version 50.

## Results

| | |
|---|---|
| Sources read | 81 paper and book texts (papers/*/paper.src.html or paper.html; #19, #20, #27 from their study folders; the six books) |
| Citations found | 2289: 1032 reference-list items, 83 "Data and code" references, 1174 items of "Sources checked" notes |
| Unique works | 545: 479 by others (290 in reference lists, 189 named only in prior-art checks) and 66 of DICTO's own records |
| Already in the library | 95 held as a copy, 139 held as a link entry |
| Newly filed (library `cited/`) | 219 entries: 122 copies (70 + 4 arXiv, 35 Wikipedia pages, 4 US patents, 9 open-access, public-domain or institutional copies), 97 link entries |
| Too vague to file | 26 author–year mentions in prior-art notes (`data/vague-mentions.json`) |
| DICTO's own | 65 records (papers by number, books, data set) in `cited/dicto-own.json`, DICTO DOIs, not copied |
| Disk | Pi: 191 MB in `cited/`. dicto-big-brother: 29 MB (Heath 1921, over the 20 MB limit) in `~/reference-library-incoming/cited/`, entry written as if in place, with `copy_on` |

The draft bibliography is `bibliography-draft.html` (Part A: 290 works cited in reference lists; Part B: 111 identified works named only in prior-art checks; Part C: 65 of DICTO's own works). Not published.

## Pipeline (`scripts/`, run from this folder with `python3 -I`)

1. `extract.py` → `data/raw-references.json`: every reference-list item, "Data and code" reference and "Sources checked" item, with the citing paper's number (from the dictospheres.com cards, checked against each folder's Zenodo concept DOI; the map is in the script).
2. `normalise.py` → `data/works.json`: one work per DOI / arXiv id / US patent / Wikipedia article / DICTO Zenodo record, otherwise first author + year + title words; works sharing an identifier are merged; hand merges in `data/overrides.json`. "Sources checked" items attach to known works by identifier or author + year; the rest stay in `data/checked-unresolved.json` (mostly search phrases and web pages).
3. `match.py` → `data/matched.json`: held / link / missing / own against every manifest of the library as it was before this study.
4. `fetch.py resolve | plan | download N | manifest`: arXiv API and OpenAlex metadata (cached in `data/cache/`, not committed); legal-copy decision per work (`data/plan.json`; hand-found copies in `data/manual-copies.json`); downloads one at a time with 3 s pauses (`data/downloads.json`, sha256 per file); writes `cited/MANIFEST.json` and `cited/dicto-own.json` in the library.
5. In the library: `python3 -I tools/build_index.py` (new sections "Cited in DICTO's papers" and "DICTO's own papers, as cited"); INDEX.pdf printed on dicto-big-brother with `tools/print_pdf.mjs` (219 pages).
6. `bibliography.py` → `bibliography-draft.html`.

Legal sources only: arXiv; repository or CC-licensed open-access copies listed by OpenAlex; public-domain scans; US patents (Google Patents images); Wikipedia (CC BY-SA, its own PDF service). No shadow libraries. Everything in copyright is a link entry.

## Checks and doubtful points

- Every cited DOI was looked up in OpenAlex and every arXiv id in the arXiv API (`data/citation-flags.json`). All 115 arXiv ids exist. Flags: #27, #28, #34, #35 cite *The Symmetries of Things* as 2008 with doi:10.1201/b21368, which is the 2016 CRC reissue; #13 shortens the Fang–Irwin title (harmless). The #83 flag is a false alarm (a list item holding several sources).
- Two open copies could not be fetched (Bezdek–Carrigan 2016, server closed; Gražulis et al. 2009, IUCr 403); both are link entries.
- Citation forms are kept as each paper gives them; spellings are not unified (for example Žitko / Zitko, Kelvin / Thomson).
- Matching of bare "Author YEAR" mentions in prior-art notes to library entries is by author and year only; a few may be loose.

## Decisions

- DICTO: every cited work goes into the library (3 November 2026). Coordinator, for DICTO, same day: files over 20 MB and all further files to dicto-big-brother; the library is moving there.
