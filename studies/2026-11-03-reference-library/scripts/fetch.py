#!/usr/bin/env python3
"""Step 4: find a legal free copy of every missing work, fetch it, file it.

  python3 -I scripts/fetch.py resolve     # metadata: arXiv API, OpenAlex (cached in data/cache/)
  python3 -I scripts/fetch.py plan        # decide copy or link for each missing work -> data/plan.json
  python3 -I scripts/fetch.py download N  # fetch the next N planned copies, one at a time, with pauses
  python3 -I scripts/fetch.py manifest    # write cited/MANIFEST.json and cited/dicto-own.json in the library

Legal sources only (library rules): arXiv; open-access copies that OpenAlex
lists with a repository or a CC/public-domain publisher licence; US patents
(Google Patents images); Wikipedia (CC BY-SA, printed by its own PDF service).
Everything else, and every copy over 40 MB, becomes a link entry.  No shadow
libraries.  Downloads stop if the study would pass 1.2 GB in total.
"""
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import xml.etree.ElementTree as ET

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalise import fold, sim, words  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
CACHE = os.path.join(DATA, "cache")
LIB = os.path.expanduser("~/Documents/kaleidohedra-references")
CITED = os.path.join(LIB, "cited")
UA = {"User-Agent": "DICTO-reference-library/1.0 (private study library; one request at a time)"}
PAUSE = 3.0
MAX_FILE = 60e6          # larger copies stay link entries
LOCAL_FILE = 20e6        # copies above this go to compute-host (DICTO 2026-11-03: the Pi's card is 87% full)
MAX_TOTAL = 500e6        # local total; past it every copy goes to compute-host
REMOTE = "compute-host"
REMOTE_DIR = "reference-library-incoming/cited"   # DICTO 2026-11-03: the library moves to compute-host
TODAY = time.strftime("%Y-%m-%d")

S = requests.Session()
S.headers.update(UA)


def cached(name, fn):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, hashlib.sha1(name.encode()).hexdigest()[:16] + ".json")
    if os.path.exists(p):
        return json.load(open(p))
    v = fn()
    json.dump({"query": name, "result": v}, open(p, "w"), ensure_ascii=False)
    time.sleep(1.0)
    return {"query": name, "result": v}


def get_json(url):
    try:
        r = S.get(url, timeout=40)
        if r.status_code == 404:
            return {"_status": 404}
        r.raise_for_status()
        return r.json()
    except Exception as e:  # network errors are recorded, not fatal
        return {"_error": str(e)[:200]}


def load():
    return json.load(open(os.path.join(DATA, "matched.json")))


def best_form(w):
    refs = [f for f in w["forms"] if not f.startswith(("arXiv ", "\"", "Wikipedia"))]
    good = [f for f in refs if re.match(r"^(?:[A-Z][\w.'’\- ]*?,|[A-Z]\. )", f) and len(f) < 400] or refs or w["forms"]
    return sorted(good, key=lambda f: (-min(len(f), 260), f))[0]


# ------------------------------------------------------------------ resolve
def resolve():
    works = load()
    miss = [w for w in works if not w["own"]]
    # arXiv: one batched call per 50 ids
    ax = sorted({w["ids"]["arxiv"] for w in miss if "arxiv" in w["ids"]})
    meta = {}
    for i in range(0, len(ax), 50):
        chunk = ax[i:i + 50]
        res = cached("arxiv:" + ",".join(chunk), lambda: S.get("https://export.arxiv.org/api/query", params={"id_list": ",".join(chunk), "max_results": 60}, timeout=60).text)
        root = ET.fromstring(res["result"])
        ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
        for e in root.findall("a:entry", ns):
            aid = e.find("a:id", ns).text.rsplit("/abs/", 1)[-1]
            aid = re.sub(r"v\d+$", "", aid)
            t = e.find("a:title", ns)
            if t is None or "Error" in (t.text or ""):
                continue
            lic = e.find("x:license", ns)
            meta[aid] = {"title": " ".join(t.text.split()), "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
                         "year": int(e.find("a:published", ns).text[:4]), "doi": (e.find("x:doi", ns).text if e.find("x:doi", ns) is not None else None),
                         "journal": (e.find("x:journal_ref", ns).text if e.find("x:journal_ref", ns) is not None else None),
                         "license": lic.text if lic is not None else None}
        print(f"arXiv metadata {min(i + 50, len(ax))}/{len(ax)}", flush=True)
    json.dump(meta, open(os.path.join(DATA, "arxiv-meta.json"), "w"), ensure_ascii=False, indent=1)
    # OpenAlex: every cited DOI (check it), and missing works with a usable title
    oa = {}
    todo = [w for w in miss if "doi" in w["ids"]] + [w for w in miss if w["status"] == "missing" and "doi" not in w["ids"]
                                                    and not ({"arxiv", "patent", "wiki"} & set(w["ids"])) and not w["key"].startswith("mention:")]
    for n, w in enumerate(todo):
        if "doi" in w["ids"]:
            q = "https://api.openalex.org/works/doi:" + urllib.parse.quote(w["ids"]["doi"])
            r = cached(q, lambda: get_json(q))["result"]
            oa[w["key"]] = {"how": "doi", "work": slim(r)}
        else:
            t = title_guess(w)
            if len(words(t)) < 3:
                continue
            flt = f"publication_year:{w['year'] - 1}-{w['year'] + 1}" if w.get("year") else None
            q = "https://api.openalex.org/works?per-page=5&search=" + urllib.parse.quote(t) + (f"&filter={flt}" if flt else "")
            r = cached(q, lambda: get_json(q))["result"]
            cands = [slim(x) for x in (r.get("results") or [])]
            ok = [c for c in cands if sim(c["title"], t) >= 0.7 and (not w["surname"] or any(w["surname"] in fold(a) for a in c["authors"]))]
            oa[w["key"]] = {"how": "search", "query": t, "work": ok[0] if ok else None}
        if n % 20 == 0:
            print(f"OpenAlex {n}/{len(todo)}", flush=True)
    json.dump(oa, open(os.path.join(DATA, "openalex.json"), "w"), ensure_ascii=False, indent=1)
    print("resolved:", len(meta), "arXiv,", sum(1 for v in oa.values() if v.get("work") and not v["work"].get("missing")), "OpenAlex")


def title_guess(w):
    f = best_form(w)
    m = re.search(r"[\"“]([^\"”]{8,})[\"”]", f)
    if m:
        return m.group(1)
    t = w.get("title") or ""
    return t if len(words(t)) >= 3 else ""


def slim(r):
    if not r or r.get("_status") == 404:
        return {"missing": True}
    if r.get("_error"):
        return {"error": r["_error"]}
    locs = []
    for l in (r.get("locations") or []):
        src = l.get("source") or {}
        locs.append({"pdf": l.get("pdf_url"), "landing": l.get("landing_page_url"), "license": l.get("license"),
                     "version": l.get("version"), "is_oa": l.get("is_oa"), "type": src.get("type"), "host": src.get("display_name")})
    return {"id": r.get("id"), "doi": (r.get("doi") or "").replace("https://doi.org/", ""), "title": r.get("title") or "",
            "year": r.get("publication_year"), "authors": [a["author"]["display_name"] for a in r.get("authorships", []) if a.get("author")],
            "venue": ((r.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "oa_status": (r.get("open_access") or {}).get("oa_status"), "locations": locs}


# ------------------------------------------------------------------ plan
def short(s, n=6):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    ws = [w for w in re.findall(r"[A-Za-z0-9]+", s)][:n]
    return "-".join(w[:1].upper() + w[1:] for w in ws)


def fname(authors, year, title):
    a = authors if isinstance(authors, list) else re.split(r",\s*|\s+and\s+", authors or "")
    sn = [short(x.split()[-1], 1) for x in a if x.strip()][:3] or ["Anon"]
    return f"{'-'.join(sn)}-{year or 'nd'}-{short(title)}"


def plan():
    works = load()
    ax = json.load(open(os.path.join(DATA, "arxiv-meta.json")))
    oa = json.load(open(os.path.join(DATA, "openalex.json")))
    out, flags = [], []
    manual = json.load(open(os.path.join(DATA, "manual-copies.json")))
    for w in works:
        if w["own"]:
            continue
        o = (oa.get(w["key"]) or {}).get("work") or {}
        # citation checks (all cited works, held ones too): does the identifier lead to the work as cited?
        form = " ".join(f for f in w["forms"] if len(f) < 600)
        if "doi" in w["ids"] and o.get("missing"):
            flags.append({"key": w["key"], "cites": w["cites"], "issue": f"DOI {w['ids']['doi']} not found in OpenAlex", "form": best_form(w)})
        elif "doi" in w["ids"] and o.get("title") and w["kinds"] != ["checked"] and sim(o["title"], form) < 0.5:
            flags.append({"key": w["key"], "cites": w["cites"], "issue": f"DOI {w['ids']['doi']} resolves to \"{o['title']}\" ({o.get('year')})", "form": best_form(w)})
        elif "doi" in w["ids"] and o.get("year") and w.get("year") and w["kinds"] != ["checked"] and abs(o["year"] - w["year"]) > 1 and not re.search(r"repr|ed\.|edition|transl", form):
            flags.append({"key": w["key"], "cites": w["cites"], "issue": f"cited year {w['year']}, DOI record year {o['year']}", "form": best_form(w)})
        if "arxiv" in w["ids"]:
            m = ax.get(w["ids"]["arxiv"])
            if not m:
                flags.append({"key": w["key"], "cites": w["cites"], "issue": f"arXiv {w['ids']['arxiv']} not found", "form": best_form(w)})
            elif w["kinds"] != ["checked"] and sim(m["title"], form) < 0.5:
                flags.append({"key": w["key"], "cites": w["cites"], "issue": f"arXiv {w['ids']['arxiv']} is \"{m['title']}\"", "form": best_form(w)})
        if w["status"] != "missing" or w["key"].startswith("mention:"):
            continue
        e = {"key": w["key"], "cites": w["cites"], "citation": best_form(w), "kinds": w["kinds"]}
        if "arxiv" in w["ids"] and w["ids"]["arxiv"] in ax:
            m = ax[w["ids"]["arxiv"]]
            e.update(authors=", ".join(m["authors"][:6]) + (" et al." if len(m["authors"]) > 6 else ""), year=m["year"], title=m["title"],
                     venue="arXiv:" + w["ids"]["arxiv"] + (f"; {m['journal']}" if m.get("journal") else ""),
                     url=f"https://arxiv.org/abs/{w['ids']['arxiv']}", pdf=f"https://arxiv.org/pdf/{w['ids']['arxiv']}",
                     licence="arXiv preprint (author copy, free to read)" + (f"; {m['license'].rsplit('/licenses/', 1)[-1]}" if m.get("license") else ""),
                     action="download", file=fname(m["authors"], m["year"], m["title"]) + ".pdf")
        elif "patent" in w["ids"]:
            pn = w["ids"]["patent"]
            e.update(authors=w["surname"].title(), year=w.get("year"), title=w.get("title") or pn, venue=f"US Patent {pn[2:]}",
                     url=f"https://patents.google.com/patent/{pn}", pdf="patent:" + pn, licence="US patent (public domain)",
                     action="download", file=f"{w['surname'].title() or 'Patent'}-{w.get('year') or 'nd'}-{pn}.pdf")
        elif "wiki" in w["ids"]:
            t = w["ids"].get("wikititle") or w["ids"]["wiki"]
            t = t[:1].upper() + t[1:]
            page = urllib.parse.quote(t.replace(" ", "_"))
            e.update(authors="Wikipedia contributors", year=2026, title=t, venue="Wikipedia", url=f"https://en.wikipedia.org/wiki/{page}",
                     pdf=f"https://en.wikipedia.org/api/rest_v1/page/pdf/{page}", licence="CC BY-SA 4.0 (Wikipedia), printed " + TODAY,
                     action="download", file=f"Wikipedia-2026-{short(t, 8)}.pdf")
        else:
            e.update(authors=", ".join(o.get("authors", [])[:6]) if o.get("authors") else first_authors(e["citation"]), year=o.get("year") or w.get("year"),
                     title=o.get("title") or title_guess(w) or w.get("title") or "", venue=o.get("venue") or "")
            doi = w["ids"].get("doi") or o.get("doi")
            url = f"https://doi.org/{doi}" if doi else (re.search(r"https?://[^\s,;)]+", e["citation"]) or [None])[0]
            if not url:
                m = re.search(r"\b((?:www\.)?[a-z0-9.-]+\.(?:com|org|net|ch|de|edu|jp)/[^\s,;)]*)", e["citation"])
                url = "https://" + m.group(1).rstrip(".") if m else None
            e["url"] = url.rstrip(".") if url else url
            legal = None
            for l in o.get("locations", []) if not o.get("missing") else []:
                if not l.get("pdf"):
                    continue
                lic = (l.get("license") or "")
                if l.get("type") == "repository" and l.get("version") in ("publishedVersion", "acceptedVersion", "submittedVersion"):
                    legal = (l, f"{l.get('host') or 'repository'} copy ({l.get('version')}){', ' + lic if lic else ''}")
                    break
                if lic.startswith(("cc-", "public-domain", "pd")):
                    legal = legal or (l, f"open access ({lic}) at {l.get('host') or 'publisher'}")
            if legal:
                e.update(pdf=legal[0]["pdf"], licence=legal[1], action="download",
                         file=fname(o.get("authors") or e["authors"], e["year"], e["title"]) + ".pdf")
            else:
                yr = e["year"] or 0
                e.update(action="link", licence=("link only: public domain by age; no verified free scan fetched" if yr and int(yr) < 1929
                                                 else "link only: in copyright, no legal free copy found" if url and "doi.org" in (url or "")
                                                 else "link only: free web page" if url else "link only: no online copy identified"))
        if w["key"] in manual:
            mc = manual[w["key"]]
            e.update(action="download", pdf=mc["pdf"], url=mc.get("url", e.get("url")), licence=mc["licence"], file=mc["file"])
        out.append(e)
    json.dump(out, open(os.path.join(DATA, "plan.json"), "w"), ensure_ascii=False, indent=1)
    json.dump(flags, open(os.path.join(DATA, "citation-flags.json"), "w"), ensure_ascii=False, indent=1)
    c = {}
    for e in out:
        c[e["action"]] = c.get(e["action"], 0) + 1
    print("plan:", c, "| citation flags:", len(flags))


def first_authors(c):
    m = re.match(r"^(.*?)(?:,\s*[\"“]|,\s*(?=[A-Z][a-z]+ [a-z])|\s\()", c)
    return (m.group(1) if m else c.split(",")[0])[:120]


# ------------------------------------------------------------------ download
def used_bytes():
    if not os.path.isdir(CITED):
        return 0
    return sum(os.path.getsize(os.path.join(CITED, f)) for f in os.listdir(CITED) if not f.endswith(".json"))


def patent_pdf(pn):
    """PDF link and bibliographic data from the Google Patents page."""
    r = S.get(f"https://patents.google.com/patent/{pn}/en", timeout=40)
    m = re.search(r"https://patentimages\.storage\.googleapis\.com/[^\"]+?\.pdf", r.text)
    if not m:
        time.sleep(PAUSE)
        r = S.get(f"https://patents.google.com/patent/{pn}A/en", timeout=40)
        m = re.search(r"https://patentimages\.storage\.googleapis\.com/[^\"]+?\.pdf", r.text)
    time.sleep(PAUSE)
    meta = {}
    t = re.search(r'<meta name="DC\.title" content="([^"]*)"', r.text)
    who = re.findall(r'<meta name="DC\.contributor" content="([^"]*)" scheme="inventor"', r.text) or re.findall(r'<meta name="DC\.contributor" content="([^"]*)"', r.text)[:1]
    dates = re.findall(r'<meta name="DC\.date" content="(\d{4})', r.text)
    if t:
        meta["title"] = " ".join(t.group(1).split())
    if who:
        meta["authors"] = ", ".join(who)
    if dates:
        meta["year"] = int(dates[-1])
    return (m.group(0) if m else None), meta


def download(n):
    os.makedirs(CITED, exist_ok=True)
    plan_ = json.load(open(os.path.join(DATA, "plan.json")))
    logp = os.path.join(DATA, "downloads.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    done = 0
    for e in plan_:
        if e["action"] != "download" or e["key"] in log:
            continue
        if done >= n:
            break
        url = e["pdf"]
        try:
            pmeta = {}
            if url.startswith("patent:"):
                url, pmeta = patent_pdf(url.split(":", 1)[1])
                if not url:
                    raise RuntimeError("no patent PDF link")
                if pmeta.get("authors"):
                    pn = e["pdf"].split(":", 1)[1]
                    e["file"] = f"{short(pmeta['authors'].split(',')[0].split()[-1], 1)}-{pmeta.get('year', 'nd')}-{pn}.pdf"
            h = S.head(url, timeout=40, allow_redirects=True)
            size = int(h.headers.get("Content-Length") or 0)
            if size > MAX_FILE:
                raise RuntimeError(f"too large ({size / 1e6:.0f} MB)")
            r = S.get(url, timeout=120, stream=True)
            r.raise_for_status()
            body = b""
            for chunk in r.iter_content(1 << 16):
                body += chunk
                if len(body) > MAX_FILE:
                    raise RuntimeError("too large (stream)")
            if not body.startswith(b"%PDF"):
                raise RuntimeError(f"not a PDF ({r.headers.get('Content-Type')})")
            path = os.path.join(CITED, e["file"])
            open(path, "wb").write(body)
            remote = None
            if len(body) > LOCAL_FILE or used_bytes() > MAX_TOTAL:
                import subprocess
                subprocess.run(["ssh", REMOTE, f"mkdir -p ~/{REMOTE_DIR}"], check=True)
                subprocess.run(["rsync", "-a", path, f"{REMOTE}:{REMOTE_DIR}/"], check=True)
                os.remove(path)
                remote = f"{REMOTE}:~/{REMOTE_DIR}/{e['file']}"
            log[e["key"]] = {"remote": remote} if remote else {}
            log[e["key"]].update({"ok": True, "file": e["file"], "source_url": url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "accessed": TODAY, **({"meta": pmeta} if pmeta else {})})
            print(f"  ok   {len(body) / 1e6:5.1f} MB  {e['file']}", flush=True)
        except Exception as ex:
            log[e["key"]] = {"ok": False, "error": str(ex)[:160], "tried": url}
            print(f"  FAIL {e['key'][:40]}: {str(ex)[:100]}", flush=True)
        json.dump(log, open(logp, "w"), ensure_ascii=False, indent=1)
        done += 1
        time.sleep(PAUSE)
    left = sum(1 for e in plan_ if e["action"] == "download" and e["key"] not in log)
    print(f"batch done: {done}; still to fetch: {left}; cited/ holds {used_bytes() / 1e6:.0f} MB")


# ------------------------------------------------------------------ manifest
def manifest():
    plan_ = json.load(open(os.path.join(DATA, "plan.json")))
    log = json.load(open(os.path.join(DATA, "downloads.json"))) if os.path.exists(os.path.join(DATA, "downloads.json")) else {}
    entries = []
    for e in plan_:
        d = log.get(e["key"], {})
        ok = d.get("ok")
        if ok and d.get("remote"):
            e = dict(e, licence=e["licence"] + "; copy waiting on compute-host: " + d["remote"].split(":", 1)[1])
        status = e["licence"] if ok else (e["licence"] if e["action"] == "link" else f"link only: copy not fetched ({d.get('error', 'not tried')})")
        if not ok and e["action"] == "download" and e.get("licence", "").startswith(("arXiv", "US patent", "CC BY-SA")):
            status = f"link only: free copy at the link (fetch failed: {d.get('error', 'not tried')})"
        e = dict(e, **(d.get("meta") or {}))
        entries.append({
            "file": d.get("file") if ok else None,   # remote copies: path as if in place (library moving to compute-host)
            "authors": e.get("authors") or "", "year": e.get("year"), "title": e.get("title") or e["citation"][:120],
            "venue": e.get("venue") or "", "doi_or_url": e.get("url"), "source_url": d.get("source_url") if ok else None, **({"copy_on": d["remote"]} if d.get("remote") else {}),
            "licence_or_status": status, "citation": e["citation"],
            "why_it_matters": "Cited in DICTO's " + ", ".join(e["cites"]) + ("" if e["kinds"] != ["checked"] else " (named in a prior-art check)") + ".",
            "related_findings": [c for c in e["cites"] if c.startswith("#")], "cited_by": e["cites"],
            "accessed": d.get("accessed", TODAY), **({"bytes": d["bytes"], "sha256": d["sha256"]} if ok else {}),
        })
    entries.sort(key=lambda x: (fold(x["authors"] or "~"), str(x["year"])))
    json.dump({"note": "Works cited in DICTO's papers (#1-#88) and books that the library did not yet have (2026-11-03, study "
               "k-research/studies/2026-11-03-reference-library). Legal copies only: arXiv, open-access repository or CC copies, "
               "US patents, Wikipedia (CC BY-SA). Everything else is a link entry.", "entries": entries},
              open(os.path.join(CITED, "MANIFEST.json"), "w"), ensure_ascii=False, indent=1)
    own = [w for w in load() if w["own"] and w["key"] not in ("own:study",)]
    rows = []
    for w in own:
        z = w["ids"].get("zenodo")
        rows.append({"key": w["key"], "label": w["key"][4:] if w["key"].startswith("own:#") else "", "title": w.get("title") or best_form(w)[:120],
                     "doi": f"10.5281/zenodo.{z}" if z else None, "citation": best_form(w), "cited_by": w["cites"]})
    rows.sort(key=lambda r: (not r["label"], int(r["label"][1:]) if r["label"][1:].isdigit() else 0, r["title"]))
    json.dump({"note": "DICTO's own papers, books and data set as cited in his other papers: Zenodo DICTO DOIs, listed, not copied.", "entries": rows},
              open(os.path.join(CITED, "dicto-own.json"), "w"), ensure_ascii=False, indent=1)
    print(f"cited/MANIFEST.json: {len(entries)} entries ({sum(1 for x in entries if x['file'])} with a copy); dicto-own.json: {len(rows)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "resolve":
        resolve()
    elif cmd == "plan":
        plan()
    elif cmd == "download":
        download(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    elif cmd == "manifest":
        manifest()
    else:
        print(__doc__)
