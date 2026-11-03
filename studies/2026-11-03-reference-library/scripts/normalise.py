#!/usr/bin/env python3
"""Step 2: normalise and de-duplicate the citations into works.

Reads data/raw-references.json (extract.py) and data/overrides.json (hand
decisions: merges, canonical citations, DICTO's own records); writes
data/works.json, one entry per work with the papers that cite it.

Identity, strongest first: DOI, arXiv id, US patent number, Wikipedia
article, DICTO Zenodo record; otherwise first author + year + title words.
Formal reference-list items ("ref", "dataref") make works directly.  Items
from "Sources checked" paragraphs ("checked") are attached to a work only
when they name one already found (identifier, or author + year); the rest
are listed in data/checked-unresolved.json for review, not guessed.

Run: python3 -I scripts/normalise.py
"""
import html
import json
import os
import re
import unicodedata
import urllib.parse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
KR = os.path.expanduser("~/k-research")
SITE = os.path.expanduser("~/dictospheres/index.html")

DOI = re.compile(r"\b(10\.\d{4,9}/\(SICI\)[^\s,]+|10\.\d{4,9}/[^\s,;\"<>]+)", re.I)
ARX = re.compile(r"arXiv[:\s]*(?:abs/)?((?:\d{4}\.\d{4,5})|(?:[a-z\-]+(?:\.[A-Z]{2})?/\d{7}))(?:v\d+)?|arxiv\.org/(?:abs|pdf)/((?:\d{4}\.\d{4,5})|(?:[a-z\-]+(?:\.[A-Z]{2})?/\d{7}))", re.I)
ARX_BARE = re.compile(r"\barXiv\s+((?:\d{4}\.\d{4,5})|(?:cond-mat|math|hep-th|gr-qc|quant-ph|math-ph)/\d{7})")
PAT = re.compile(r"\b(?:US|U\.S\.)\s*(?:[Pp]at(?:ent)?s?\.?\s*(?:No\.?)?\s*)?(\d{1,2},?\d{3},?\d{3})\b")
YEAR = re.compile(r"\b(1[4-9]\d\d|20[0-2]\d)\b")
ZEN = re.compile(r"10\.5281/zenodo\.(\d+)")
STOP = set("a an the of on in and for to by with from as at its is are be or into their two three new some".split())


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def words(t):
    return {w for w in re.findall(r"[a-z0-9]+", fold(t or "")) if w not in STOP and len(w) > 2}


def sim(a, b):
    A, B = words(a), words(b)
    if not A or not B:
        return 0.0
    return len(A & B) / min(len(A), len(B))


def clean_doi(d):
    d = d.rstrip(".)]")
    return d.lower()


def title_of(text, raw):
    m = re.search(r"[\"“]([^\"”]{6,})[\"”]", raw or text)
    if m:
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip(" ,.")
    m = re.search(r"<i>(.*?)</i>", raw or "")
    if m:
        return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip(" ,.")
    if " | " in text:                                  # table rows: authors | year | title
        parts = [p.strip() for p in text.split(" | ")]
        if len(parts) >= 3:
            return parts[2]
    parts = [p.strip() for p in re.split(r",\s+", text)]
    # skip the author run: initials or 'and'
    i = 0
    while i < len(parts) and (re.match(r"^(?:[A-Z]\.\s?)+[\w'’\-ÀÄÖÜ-ž ]+$", parts[i]) or re.match(r"^(and |et al)", parts[i]) or re.search(r"\bet al\.?$", parts[i])):
        i += 1
    if i == 0:
        i = 1
    return parts[i] if i < len(parts) else ""


def first_surname(text):
    t = text.split(" | ")[0]
    t = re.sub(r"^(?:Sir |Prof\. )", "", t)
    head = re.split(r",|\band\b|&|\(|\set al", t)[0].strip()
    head = re.sub(r"[“\"].*", "", head).strip()
    toks = [w for w in re.findall(r"[^\s.]+", head) if not re.match(r"^[A-Z]$", w)]
    if not toks:
        return ""
    s = toks[-1] if len(toks) <= 3 else toks[0]
    return fold(s).strip("'’")


def ids(text, raw=""):
    blob = text + " " + (raw or "")
    out = {}
    m = ZEN.search(blob)
    if m:
        out["zenodo"] = m.group(1)
    for m in DOI.finditer(blob):
        d = clean_doi(m.group(1))
        if not d.startswith("10.5281/zenodo"):
            out.setdefault("doi", d)
    m = ARX.search(blob) or ARX_BARE.search(blob)
    if m:
        out["arxiv"] = next(g for g in m.groups() if g)
    m = PAT.search(blob)
    if m:
        out["patent"] = "US" + m.group(1).replace(",", "")
    if re.search(r"wikipedia", blob, re.I) and not re.search(r"mirror|Kyushindo \(2007", text):
        u = re.search(r"wikipedia\.org/wiki/([^\s,;)]+)", text)
        q = re.search(r"[\"“]([^\"”]+)[\"”]", text)
        parts = [p.strip() for p in text.split(" | ")]
        if u:
            w_t = urllib.parse.unquote(html.unescape(u.group(1))).replace("_", " ").split("#")[0]
        elif len(parts) > 2 and parts[0].lower().startswith("wikipedia"):
            w_t = parts[2]
        elif q:
            w_t = q.group(1)
        else:
            m = re.match(r"^(?:Wikipedia contributors,\s*|Wikipedia,\s*)?([^,]+?),\s*(?:Wikipedia|https)", text)
            w_t = m.group(1) if m else ""
        w_t = re.sub(r"\s*(?:\(.*?\)|\[\d+\])\s*$", "", w_t)
        if w_t and len(w_t) < 80:
            out["wiki"] = fold(w_t).strip(" .,")
            out["wikititle"] = w_t.strip(" .,")
    return out


# ---------------------------------------------------------------- DICTO's own records
def own_records():
    """concept and version Zenodo ids -> (#number or book/dataset, title)."""
    rec = {}
    h = open(SITE, encoding="utf-8").read()
    parts = re.split(r'<span class="num">#(\d+)</span>', h)
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        t = re.sub(r"<[^>]+>", "", parts[i + 1].split("</span>")[0]).strip()
        t = re.sub(r"\s*DOI 10\.\S+$", "", html.unescape(t))
        m = re.search(r'class="doi-badge" href="https://doi.org/10\.5281/zenodo\.(\d+)"', parts[i + 1][:8000])
        if m and n not in [v[0] for v in rec.values()]:
            rec.setdefault(m.group(1), (f"#{n}", t))
    for root, _, files in os.walk(os.path.join(KR, "papers")):
        for f in files:
            if f.startswith("zenodo-state") and f.endswith(".json"):
                try:
                    s = json.load(open(os.path.join(root, f)))
                except Exception:
                    continue
                c, v = str(s.get("conceptrecid", "")), str(s.get("id", ""))
                if c in rec and v:
                    rec.setdefault(v, rec[c])
    return rec


def main():
    raw = json.load(open(os.path.join(DATA, "raw-references.json")))
    ov = json.load(open(os.path.join(DATA, "overrides.json"))) if os.path.exists(os.path.join(DATA, "overrides.json")) else {}
    own = own_records()
    own.update({k: tuple(v) for k, v in ov.get("own", {}).items()})
    alias = [(re.compile(a["pattern"], re.I), a["work"]) for a in ov.get("alias", [])]
    ignore = [re.compile(p, re.I) for p in ov.get("ignore", [])] + [re.compile(r"^\[C\]|This paper's own|^(?:Known|Searched|Not found|Checked|Prior art)\b")]

    works = {}          # key -> work
    index = {}          # identifier -> key

    def cite_label(r):
        return f"#{r['nums'][0]}" if r["nums"] else r["label"]

    def add(key, r, info):
        w = works.setdefault(key, {"key": key, "cites": [], "forms": [], "ids": {}, "surname": info.get("surname", ""),
                                   "year": info.get("year"), "title": info.get("title", ""), "kinds": []})
        lab = cite_label(r)
        if lab not in w["cites"]:
            w["cites"].append(lab)
        if r["text"] not in w["forms"]:
            w["forms"].append(r["text"])
        if r["kind"] not in w["kinds"]:
            w["kinds"].append(r["kind"])
        for k, v in info.get("ids", {}).items():
            w["ids"].setdefault(k, v)
            index.setdefault(f"{k}:{v}", key)
        if not w["title"] and info.get("title"):
            w["title"] = info["title"]
        if not w["year"] and info.get("year"):
            w["year"] = info["year"]

    def classify(r):
        t, rawh = re.sub(r"^\[[A-Z]\d?\]\s*", "", r["text"]), r.get("html", "")
        if any(p.search(t) for p in ignore):
            return None, None
        for p, wk in alias:
            if p.search(t):
                return wk, {"ids": {}}
        i = ids(t, rawh)
        if "zenodo" in i and (t.startswith("DICTO") or "DICTO" in t[:40] or i["zenodo"] in own or r["kind"] == "dataref"):
            z = i["zenodo"]
            if z in own:
                return f"own:{own[z][0]}", {"ids": {"zenodo": z}, "title": own[z][1]}
            m = re.search(r"#(\d+)", t)
            return (f"own:#{m.group(1)}" if m else f"own:zenodo.{z}"), {"ids": {"zenodo": z}, "title": title_of(t, rawh)}
        if re.match(r"^(?:Study|The study|study files)\b", t) or re.search(r"\bstudies/20\d\d-", t):
            return "own:study", {"ids": {}, "title": "DICTO's study folders, scripts and data"}
        if r["kind"] == "dataref" or t.startswith("DICTO"):
            m = re.search(r"#(\d+)", t)
            if m:
                return f"own:#{m.group(1)}", {"ids": {}, "title": title_of(t, rawh)}
            if t.startswith("DICTO"):
                if re.search(r"\bstud(?:y|ies)\b|commit|repositor|script|\.py\b", t):
                    return "own:study", {"ids": {}, "title": "DICTO's study folders, scripts and data"}
                return "own:" + fold(title_of(t, rawh) or t)[:60], {"ids": {}, "title": title_of(t, rawh)}
        y = YEAR.findall(t)
        info = {"ids": {k: v for k, v in i.items() if k != "zenodo"}, "surname": first_surname(t),
                "year": int(y[0]) if y else None, "title": title_of(t, rawh)}
        if " | " in t and len(t.split(" | ")) >= 2 and t.split(" | ")[1].strip().isdigit():
            info["year"] = int(t.split(" | ")[1])
        for k in ("doi", "arxiv", "patent", "wiki"):
            if k in info["ids"] and f"{k}:{info['ids'][k]}" in index:
                return index[f"{k}:{info['ids'][k]}"], info
        # author + year + title words
        best, score = None, 0
        for key, w in works.items():
            if key.startswith("own:") or w["surname"] != info["surname"] or not info["surname"]:
                continue
            if w["year"] and info["year"] and abs(w["year"] - info["year"]) > 1:
                continue
            s = sim(w["title"], info["title"])
            if s > score:
                best, score = key, s
        if best and score >= 0.5:
            return best, info
        for k in ("doi", "arxiv", "patent", "wiki"):
            if k in info["ids"]:
                return f"{k}:{info['ids'][k]}", info
        return f"ay:{info['surname']}:{info['year']}:{'-'.join(sorted(words(info['title']))[:4])}", info

    pending = []
    for r in raw:
        if r["kind"] == "checked":
            pending.append(r)
            continue
        key, info = classify(r)
        if key:
            add(key, r, info)

    # "Sources checked" items name works more loosely.  Pull out every identifier
    # (arXiv, DOI, US patent, Wikipedia article) and every "Author [and Author |
    # et al.] YEAR" mention; attach each to a known work where author + year agree,
    # else keep it as a "mention" for the library match and the fetch step.
    NAME = r"(?:(?:de |van |von |van der |Van der |Van |De |Du |Le |La |O')?[A-Z][a-zß-ÿā-ž'’\-]+)"
    MENTION = re.compile(r"(?:(?:[A-Z]\.\s?){1,3})?(" + NAME + r")(?:(?:,\s*|\s+and\s+|\s*&\s*|\s*[–-]\s*)(?:(?:[A-Z]\.\s?){1,3})?" + NAME + r")*(\s+et al\.?)?,?\s*\(?((?:1[5-9]|20)\d\d)\b")
    NOT_NAMES = {"October", "November", "September", "Table", "Figure", "Fig", "Version", "Section", "Chapter", "Web", "Library",
                 "Read", "Phys", "Rev", "Lett", "Acta", "Cryst", "Nature", "Science", "Bridges", "Studies", "Study", "Vol", "Proc",
                 "Since", "Note", "Search", "Reference", "Mathematics", "Notices", "Journal", "Chem", "Soc", "Math", "Inorg", "Solid",
                 "Condens", "Matter", "Sci", "Rep", "Appl", "Commun", "Mater", "Physica", "Theor", "Comput", "Ser", "No", "Part",
                 "IUCr", "ICGG", "PNAS", "AMS", "Wikipedia", "MathWorld", "Polytope", "Wiki", "Data", "Entropy", "Meeting",
                 "Mysterium", "Cosmographicum", "Deltahedron", "Scientific", "Queries", "Hits", "Pages", "Abstract", "Summary"}
    unresolved, mentions = [], 0
    for r in pending:
        t = r["text"]
        if any(p.search(t) for p in ignore):
            continue
        got = []
        for p, wk in alias:
            if p.search(t):
                got.append((wk, {"ids": {}}))
        low = t.lower()
        if "arxiv" in low:
            seg = t[low.find("arxiv"):]
            for a_ in dict.fromkeys(re.findall(r"(?<![\d.])(\d{4}\.\d{4,5}|(?:cond-mat|math|hep-th|gr-qc|quant-ph|math-ph)/\d{7})", seg)):
                got.append((index.get(f"arxiv:{a_}", f"arxiv:{a_}"), {"ids": {"arxiv": a_}}))
        for d in dict.fromkeys(clean_doi(x) for x in DOI.findall(t)):
            if not d.startswith("10.5281/zenodo"):
                got.append((index.get(f"doi:{d}", f"doi:{d}"), {"ids": {"doi": d}}))
        if re.search(r"\bUS (?:patents?|Pat)", t):
            for pn in re.findall(r"\b(\d{1,2},\d{3},\d{3})\b", t):
                pn = "US" + pn.replace(",", "")
                got.append((index.get(f"patent:{pn}", f"patent:{pn}"), {"ids": {"patent": pn}}))
        for m in re.finditer(r"Wikipedia[,:]?\s*((?:[\"“][^\"”]+[\"”](?:,\s*|\s+and\s+)?)+)", t):
            for q in re.findall(r"[\"“]([^\"”]+)[\"”]", m.group(1)):
                wt = fold(q).strip(" .,")
                got.append((index.get(f"wiki:{wt}", f"wiki:{wt}"), {"ids": {"wiki": wt, "wikititle": q.strip(" .,")}, "title": q, "surname": "wikipedia"}))
        m0 = re.match(r"^Wikipedia,\s*([^\"“(]+?)(?:\s*\(|\.|$)", t)
        if m0 and not got:
            for q in re.split(r",\s*|\s+and\s+", re.sub(r"\s*\[\d+\]", "", m0.group(1))):
                if 2 < len(q) < 60:
                    wt = fold(q).strip(" .,")
                    got.append((index.get(f"wiki:{wt}", f"wiki:{wt}"), {"ids": {"wiki": wt, "wikititle": q.strip(" .,")}, "title": q, "surname": "wikipedia"}))
        if not got:
            for m in MENTION.finditer(t):
                sn, yr = m.group(1), int(m.group(3))
                if sn.split()[-1] in NOT_NAMES or yr > 2026:
                    continue
                f = fold(sn.split()[-1])
                cands = [k for k, w in works.items() if w["surname"] == f and w["year"] and abs(w["year"] - yr) <= 0 and not k.startswith("own:")]
                if len(cands) == 1:
                    got.append((cands[0], {"ids": {}}))
                elif not cands:
                    detail = bool(re.search(r"\b\d+,\s*\d+\s*\(\d{4}\)|\d+\s*\(\d{4}\)\s*\d+|doi", t))
                    got.append((f"mention:{f}:{yr}", {"ids": {}, "surname": f, "year": yr, "title": "", "detail": detail}))
                    mentions += 1
                else:
                    got.append((f"mention:{f}:{yr}", {"ids": {}, "surname": f, "year": yr, "title": "", "ambiguous": cands}))
        if got:
            for key, info in got:
                add(key, r, info)
                if info.get("detail"):
                    works[key]["detail"] = True
        else:
            unresolved.append({"cite": cite_label(r), "src": r["src"], "text": t})

    # same first author and year, and the citations read alike: one work
    def body(w):
        return " ".join(w["forms"][:3])
    keys = [k for k in works if not k.startswith("own:") and works[k]["surname"]]
    for a in keys:
        for b in keys:
            if a >= b or a not in works or b not in works:
                continue
            wa, wb = works[a], works[b]
            if wa["surname"] != wb["surname"] or not wa["year"] or wa["year"] != wb["year"]:
                continue
            if sim(body(wa), body(wb)) < 0.6:
                continue
            ua = set(re.findall(r"https?://\S+?(?=[,;)\s]|$)", body(wa)))
            ub = set(re.findall(r"https?://\S+?(?=[,;)\s]|$)", body(wb)))
            if ua and ub and not (ua & ub):
                continue
            ida, idb = wa["ids"], wb["ids"]
            if any(k in ida and k in idb and ida[k] != idb[k] for k in ("doi", "arxiv", "patent")):
                continue
            keep, drop = (a, b) if len(wa["ids"]) >= len(wb["ids"]) else (b, a)
            wk, wd = works[keep], works.pop(drop)
            for f in ("cites", "forms", "kinds"):
                wk[f] += [x for x in wd[f] if x not in wk[f]]
            for k, v in wd["ids"].items():
                wk["ids"].setdefault(k, v)

    # works that share any identifier are one work
    def merge_into(keep, drop):
        wk, wd = works[keep], works.pop(drop)
        for f in ("cites", "forms", "kinds"):
            wk[f] += [x for x in wd[f] if x not in wk[f]]
        for k, v in wd["ids"].items():
            wk["ids"].setdefault(k, v)
        for f in ("surname", "year", "title"):
            if not wk.get(f) and wd.get(f):
                wk[f] = wd[f]
    changed = True
    while changed:
        changed = False
        seen_id = {}
        for key in list(works):
            if key not in works or key.startswith("own:"):
                continue
            for k, v in works[key]["ids"].items():
                if k == "zenodo":
                    continue
                other = seen_id.get((k, v.lower()))
                if other and other in works and other != key:
                    merge_into(other, key)
                    changed = True
                    break
                seen_id[(k, v.lower())] = key
            if changed:
                break

    # merges decided by hand
    for a, b in ov.get("merge", []):
        if a in works and b in works and a != b:
            wa, wb = works[a], works.pop(b)
            for f in ("cites", "forms", "kinds"):
                wa[f] += [x for x in wb[f] if x not in wa[f]]
            for k, v in wb["ids"].items():
                wa["ids"].setdefault(k, v)
    for key, fix in ov.get("canonical", {}).items():
        if key in works:
            works[key].update(fix)

    out = sorted(works.values(), key=lambda w: (w["key"].startswith("own:"), w["surname"] or "~", w["year"] or 0))
    for w in out:
        w["cites"].sort(key=lambda c: (not c.startswith("#"), int(c[1:]) if c[1:].isdigit() else 0, c))
        w["own"] = w["key"].startswith("own:")
    json.dump(out, open(os.path.join(DATA, "works.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(unresolved, open(os.path.join(DATA, "checked-unresolved.json"), "w"), ensure_ascii=False, indent=1)
    n_own = sum(w["own"] for w in out)
    print(f"{len(raw)} citations -> {len(out)} works ({n_own} DICTO's own, {len(out) - n_own} others); "
          f"{len(unresolved)} 'sources checked' items not matched to a work")


if __name__ == "__main__":
    main()
