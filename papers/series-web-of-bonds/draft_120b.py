# Draft the series paper with the local workhorse on dicto-big-brother. A DRAFT only: Claude checks every claim against the dossier and the published papers.
import json, pathlib, urllib.request
d = pathlib.Path(__file__).parent; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
rules = ('You draft a mathematics paper by the artist DICTO and collaborators. Title: "From the Octet to Every Stacking: the Web of Bonds". '
         'Follow the OUTLINE section by section. Use ONLY facts, numbers, names and DOIs in the DOSSIER; never invent a result, value or reference; '
         'where something is missing write [CHECK: ...]. Lead with the main theorem stated plainly, then a 2-3 sentence plain-words opening per section. '
         '"We" for joint work; ideas and names are DICTO\'s ("DICTO\'s idea", "named by DICTO"). Cite each earlier paper by its # number and DICTO DOI. '
         'Plain, serious, verifiable style; no hype. Output Markdown with $...$ maths.')
user = 'OUTLINE:\n' + (d / 'outline.md').read_text() + '\n\nDOSSIER (JSON):\n' + (d / 'dossier.json').read_text()
body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': rules}, {'role': 'user', 'content': user}],
                   'max_tokens': 14000, 'temperature': 0.3, 'chat_template_kwargs': {'enable_thinking': False}}).encode()
r = urllib.request.Request('http://dicto-big-brother.local:8081/v1/chat/completions', data=body,
                           headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
(d / 'draft-120b.md').write_text(json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]['message']['content'].strip() + '\n')
print('draft-120b.md written')
