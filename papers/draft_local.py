# Draft a paper with the local workhorse model on dicto-big-brother (run there). A DRAFT only: Claude checks every claim against the
# dossier and the studies before anything reaches DICTO. Usage: draft_local.py <paper folder> "<title>"
import json, pathlib, sys, urllib.request
d = pathlib.Path(sys.argv[1]); title = sys.argv[2]; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
rules = (f'You draft a mathematics paper by the artist DICTO and collaborators. Title: "{title}". Follow the OUTLINE section by section. '
         'Use ONLY facts, numbers, names and DOIs in the DOSSIER; never invent a result, value or reference; where something is missing or marked '
         'pending write [CHECK: ...]. Lead with the main theorem stated plainly, then a 2-3 sentence plain-words opening per section. "We" for joint '
         'work; ideas and names are DICTO\'s ("DICTO\'s idea", "named by DICTO"). Cite earlier papers by # number and DICTO DOI. Prior art: credit '
         'exactly as the dossier says; never claim novelty, only "not found in the sources searched". Plain, serious, verifiable; no hype. '
         'Markdown with $...$ maths.')
user = 'OUTLINE:\n' + (d / 'outline.md').read_text() + '\n\nDOSSIER (JSON):\n' + (d / 'dossier.json').read_text()
body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': rules}, {'role': 'user', 'content': user}],
                   'max_tokens': 12000, 'temperature': 0.3, 'chat_template_kwargs': {'enable_thinking': False}}).encode()
r = urllib.request.Request('http://127.0.0.1:8081/v1/chat/completions', data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
(d / 'draft-local.md').write_text(json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]['message']['content'].strip() + '\n')
print(d.name, 'draft-local.md written')
