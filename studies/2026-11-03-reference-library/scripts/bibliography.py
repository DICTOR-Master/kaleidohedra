#!/usr/bin/env python3
"""Step 6: draft "Bibliography of the Collected Works" (HTML, for CW v50).

Each work once, with the papers that cite it.  Part A: works by others cited
in reference lists.  Part B: works by others named only in prior-art checks
(identified ones).  Part C: DICTO's own papers, books and data set as cited.
Reads data/matched.json, data/plan.json, data/arxiv-meta.json, cited/MANIFEST.json.
Writes bibliography-draft.html in the study folder.  Nothing is published.

Run: python3 -I scripts/bibliography.py
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalise import fold  # noqa: E402
from fetch import best_form  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
SITE = os.path.expanduser("~/dictospheres/index.html")
esc = html.escape

BOOKS = {"DICTONIC Bonds: from the Octet to the Rule of Halves": "Bonds", "The Golden Cycle": "Golden Cycle",
         "HexOct: The Hexagonality Law": "HexOct", "Quanta of Space: A Manifesto": "Quanta",
         "Alicia in Wonderland: The Red & White Queens": "Alicia", "Star Cores": "Star Cores"}


def label(c):
    return BOOKS.get(c, c)


def sort_cites(cs):
    nums = sorted({int(c[1:]) for c in cs if re.fullmatch(r"#\d+", c)})
    rest = sorted({label(c) for c in cs if not re.fullmatch(r"#\d+", c)})
    return [f"#{n}" for n in nums] + rest


def link_for(w, plan, ax):
    i = w.get("ids", {})
    if "doi" in i:
        return f"https://doi.org/{i['doi']}"
    if "arxiv" in i:
        return f"https://arxiv.org/abs/{i['arxiv']}"
    p = plan.get(w["key"])
    if p and p.get("url"):
        return p["url"]
    lib = w.get("library") or {}
    return lib.get("link")


def display(w, plan, ax):
    """The citation as the papers give it; for works only named in checks, a citation built from metadata."""
    if w["kinds"] != ["checked"]:
        return esc(best_form(w))
    i = w.get("ids", {})
    if "arxiv" in i and i["arxiv"] in ax:
        m = ax[i["arxiv"]]
        a = ", ".join(m["authors"][:4]) + (" et al." if len(m["authors"]) > 4 else "")
        return f"{esc(a)}, “{esc(m['title'])}”, arXiv:{esc(i['arxiv'])} ({m['year']})."
    lib = w.get("library")
    if lib:
        return f"{esc(lib['authors'])}, “{esc(lib['title'])}” ({esc(str(lib['year']))})."
    p = plan.get(w["key"])
    if p and p.get("title"):
        return f"{esc(p.get('authors', ''))}, “{esc(p['title'])}” ({esc(str(p.get('year') or 'n.d.'))})."
    if "wiki" in i:
        return f"Wikipedia, “{esc(i['wiki'][:1].upper() + i['wiki'][1:])}”."
    if "patent" in i:
        return f"US Patent {esc(i['patent'][2:])}."
    return None


def sortkey(w, plan, ax):
    lib = w.get("library") or {}
    p = plan.get(w["key"]) or {}
    s = w.get("surname") or fold((lib.get("authors") or p.get("authors") or "~").split(",")[0].split()[-1:][0] if (lib.get("authors") or p.get("authors")) else "~")
    if s in ("wikipedia", "contributors", ""):
        s = "~wikipedia"
    return (s, w.get("year") or 0)


def main():
    works = json.load(open(os.path.join(DATA, "matched.json")))
    plan = {p["key"]: p for p in json.load(open(os.path.join(DATA, "plan.json")))} if os.path.exists(os.path.join(DATA, "plan.json")) else {}
    ax = json.load(open(os.path.join(DATA, "arxiv-meta.json"))) if os.path.exists(os.path.join(DATA, "arxiv-meta.json")) else {}
    h = open(SITE, encoding="utf-8").read()
    titles = {}
    for m in re.finditer(r'<span class="num">#(\d+)</span>\s*(.*?)</span>', h):
        titles.setdefault(int(m.group(1)), re.sub(r"<[^>]+>", "", html.unescape(m.group(2))).strip())

    others = [w for w in works if not w["own"] and not w["key"].startswith("mention:")]
    formal = sorted([w for w in others if w["kinds"] != ["checked"]], key=lambda w: sortkey(w, plan, ax))
    checked = [w for w in others if w["kinds"] == ["checked"]]
    checked = sorted([w for w in checked if display(w, plan, ax)], key=lambda w: sortkey(w, plan, ax))
    vague = [w for w in works if w["key"].startswith("mention:") and w["status"] == "missing"]
    own = [w for w in works if w["own"] and w["key"] != "own:study"]

    def rows(ws):
        out = ""
        for n, w in enumerate(ws, 1):
            lk = link_for(w, plan, ax)
            cit = display(w, plan, ax)
            link = f' <a href="{esc(lk)}">{esc(lk)}</a>' if lk and lk not in html.unescape(cit) else ""
            out += f'<li><span class="c">{cit}</span>{link} <span class="by">Cited in {esc(", ".join(sort_cites(w["cites"])))}.</span></li>\n'
        return out

    def own_key(w):
        m = re.match(r"own:#(\d+)", w["key"])
        return (0, int(m.group(1)), "") if m else (1, 0, w.get("title") or "")
    own.sort(key=own_key)
    own_rows = ""
    for w in own:
        m = re.match(r"own:#(\d+)", w["key"])
        z = w["ids"].get("zenodo")
        t = titles.get(int(m.group(1))) if m else None
        t = t or w.get("title") or best_form(w)
        doi = f' DICTO DOI: <a href="https://doi.org/10.5281/zenodo.{z}">10.5281/zenodo.{z}</a>.' if z else ""
        own_rows += f'<li><b>{esc(m.group(0)[4:] + " ") if m else ""}</b>{esc(t)}.{doi} <span class="by">Cited in {esc(", ".join(sort_cites(w["cites"])))}.</span></li>\n'

    n_cites = sum(len(w["cites"]) for w in formal)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bibliography of the Collected Works (draft)</title>
<link rel="stylesheet" href="../../papers/paper.css">
<style>.logo {{ float: right; width: 28mm; margin: 0 0 4mm 6mm; }} ol.bib {{ font-size: 8.8pt; padding-left: 7mm; }} ol.bib li {{ margin: 0 0 1.2mm; break-inside: avoid; }}
.by {{ color: #6b5310; }} a {{ word-break: break-all; }} .status {{ border: 1px solid #c9a227; background: #fffaf0; padding: 3mm 4mm; margin: 4mm 0; font-size: 9pt; }}</style></head><body>
<img class="logo" src="../../papers/dicto-logo.png" alt="DICTO">
<h1>Bibliography of the Collected Works</h1>
<p class="sub">Every work cited in DICTO's papers #1–#88 and books, each listed once, with the papers that cite it</p>
<div class="meta"><b>DICTO</b> (artist, Osaka, Japan) · https://dictospheres.com · for DICTO: Collected Geometric Works, Version 50<br>
All works, findings and names are DICTO's. Gathered with Claude (Anthropic).</div>
<div class="status"><b>Status: draft, {date.today().strftime('%-d %B %Y')}.</b> Not published. For the Collected Works Version 50 (weekly batch, about 9 November 2026).
Built by script from the papers' own reference lists (study 2026-11-03-reference-library); the citations are given as the papers give them, so
spellings and details have not been unified. Open items: Part B lists works named only in prior-art checks; decide whether it goes into v50.
Works named only by author and year ({len(vague)}) are not listed; see the study's data/vague-mentions.json.</div>

<p>Numbers #1, #2 … are DICTO's paper numbers on dictospheres.com. Books: Bonds = <i>DICTONIC Bonds</i>; Golden Cycle = <i>The Golden Cycle</i>;
HexOct = <i>HexOct: The Hexagonality Law</i>; Quanta = <i>Quanta of Space</i>; Alicia = <i>Alicia in Wonderland: The Red &amp; White Queens</i>;
Star Cores = <i>Star Cores</i>. Papers without a number are companions, named by title.</p>

<h2>A. Works cited ({len(formal)} works, {n_cites} citing papers and books)</h2>
<ol class="bib">
{rows(formal)}</ol>

<h2>B. Also consulted in prior-art checks ({len(checked)} works)</h2>
<p>Works named in the papers' “Sources checked” notes but not in their reference lists.</p>
<ol class="bib">
{rows(checked)}</ol>

<h2>C. DICTO's own works cited ({len(own)})</h2>
<p>Each has its own DICTO DOI, which always opens the newest version.</p>
<ol class="bib">
{own_rows}</ol>
</body></html>"""
    out = os.path.join(HERE, "bibliography-draft.html")
    open(out, "w").write(doc)
    json.dump([{"mention": w["key"][8:], "cites": w["cites"], "context": w["forms"][0][:300]} for w in vague],
              open(os.path.join(DATA, "vague-mentions.json"), "w"), ensure_ascii=False, indent=1)
    print(f"bibliography-draft.html: A {len(formal)}, B {len(checked)}, C {len(own)}; vague mentions {len(vague)}")


if __name__ == "__main__":
    main()
