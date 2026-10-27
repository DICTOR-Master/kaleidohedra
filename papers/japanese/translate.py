# Japanese title + abstract drafts (DICTO 2026-10-27), local workhorse model on dicto-big-brother. A DRAFT: Claude checks every one
# (numbers, formulas, DOIs, DICTO's names) before DICTO sees it; nothing goes public from here. Usage: translate.py <id> [<id> ...]
import json, pathlib, sys, urllib.request
here = pathlib.Path(__file__).parent; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
R = {str(r['id']): r for r in json.load(open(here / 'records.json'))}
SYS = ('You translate the title and abstract of a published geometry paper by the Japanese artist DICTO into natural, accurate academic '
       'Japanese (である調), for Japanese readers. Rules: keep every number, fraction, formula, symbol (φ, √, λ), paper number (#57) and DOI '
       'exactly; keep DICTO\'s own names of shapes, pieces and worlds in their original Latin spelling (e.g. Icosaxes, Lotus Jewel Axes, '
       'Chucky, Fang, DICTO Jewel), optionally followed once by a short Japanese gloss in parentheses; use the standard Japanese terms for '
       'classical solids and notions (正二十面体, 正十二面体, 菱形十二面体, 最密充填, 空間充填, ボロノイ図 etc.); translate meaning, not word '
       'order; never add, drop or soften a claim; never describe the writing itself (no 「平易に言えば」, 「簡単に言うと」 or similar). '
       'Drop any label such as "In short." from the abstract. Output JSON only: {"title_ja": "...", "abstract_ja": "..."}')
def ask(user):
    body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': SYS}, {'role': 'user', 'content': user}],
                       'temperature': 0.1, 'max_tokens': 20000, 'chat_template_kwargs': {'reasoning_effort': 'low'}}).encode()
    r = urllib.request.Request('http://127.0.0.1:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    return json.load(urllib.request.urlopen(r, timeout=3600))['choices'][0]['message']['content'].strip()
out = here / 'drafts'; out.mkdir(exist_ok=True)
for rid in sys.argv[1:]:
    r = R[rid]; t = ask(f"TITLE: {r['title']}\n\nABSTRACT:\n{r['description']}")
    if '{' not in t: print(rid, 'NO JSON:', t[:300], flush=True); continue
    t = t[t.index('{'):t.rindex('}') + 1]; j = json.loads(t); j.update(id=r['id'], title=r['title'])
    json.dump(j, open(out / f'{rid}.json', 'w'), ensure_ascii=False, indent=1); print(rid, j['title_ja'], flush=True)
