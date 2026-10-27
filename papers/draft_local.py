# Draft a paper with the local workhorse model on dicto-big-brother (run there). A DRAFT only: Claude checks every claim against the
# dossier and the studies before anything reaches DICTO. Usage: draft_local.py <paper folder> "<title>"
# Less invention (DICTO 2026-10-27, "modify DBB to hallucinate less"): reasoning on (with room for it), temperature 0.1, one outline
# section per call; then check_local.py lists every claim with the dossier line behind it.
import json, pathlib, sys, urllib.request
d = pathlib.Path(sys.argv[1]); title = sys.argv[2]; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
rules = (f'You draft ONE section of a mathematics paper by the artist DICTO and collaborators, titled "{title}". '
         'Use ONLY facts, numbers, names and DOIs found in the DOSSIER; copy numbers and formulas exactly as written there; never invent a result, '
         'value, phrase for an idea, or reference; where something is missing or marked pending write [CHECK: ...]. Measured is not proved: keep the '
         'dossier\'s own status words. "We" for joint work; ideas and names are DICTO\'s. Prior art: credit exactly as the dossier says; never claim '
         'novelty. Plain, serious, verifiable; no hype, no filler. Never label or describe the writing itself (banned: “in plain words”, “plain words”, “simply put”, “in short”, “on the other hand” as a lead-in); just write it. Markdown, starting with the section heading.')
def ask(system, user, max_tokens=8000):
    body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
                       'max_tokens': max_tokens, 'temperature': 0.1, 'chat_template_kwargs': {'reasoning_effort': 'medium'}}).encode()
    r = urllib.request.Request('http://127.0.0.1:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    return json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]['message']['content'].strip()
dossier = (d / 'dossier.json').read_text()
sections = [l.strip() for l in (d / 'outline.md').read_text().splitlines() if l.strip()]
out = [f'# {title}\n']
for s in sections:
    out.append(ask(rules, f'SECTION TO WRITE: {s}\n\nDOSSIER (JSON):\n{dossier}')); print('section done:', s[:60], flush=True)
(d / 'draft-local.md').write_text('\n\n'.join(out) + '\n'); print(d.name, 'draft-local.md written')
