# Referee attack on the series paper by the local workhorse on dicto-big-brother. Claude judges every point before anything changes.
import json, pathlib, re, html, urllib.request
d = pathlib.Path(__file__).parent; key = (pathlib.Path.home() / '.config/dicto/llama-key').read_text().strip()
txt = html.unescape(re.sub(r'<[^>]+>', ' ', (d / 'paper.src.html').read_text())); txt = re.sub(r'\s+', ' ', txt)
rules = ('You are a hard, fair referee. Attack this short paper. Check EVERY factual sentence against the DOSSIER of the published papers it retells '
         '(the origin paragraph about DICTO is his own account: check only that it is clear and not overclaimed). List numbered points, most serious first. '
         'For each: the exact quote, the problem (wrong / unsupported by the dossier / overclaim / unclear to a lay reader / clumsy), and a concrete fix. '
         'Also flag any sentence a non-mathematician would not follow, and any physics overclaim. Do not invent facts. Be concise.')
user = 'PAPER:\n' + txt + '\n\nDOSSIER (JSON):\n' + (d / 'dossier.json').read_text()
body = json.dumps({'model': 'workhorse', 'messages': [{'role': 'system', 'content': rules}, {'role': 'user', 'content': user}],
                   'max_tokens': 8000, 'temperature': 0.2, 'chat_template_kwargs': {'enable_thinking': False}}).encode()
r = urllib.request.Request('http://dicto-big-brother.local:8081/v1/chat/completions', data=body,
                           headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
(d / 'referee-v3-120b.md').write_text(json.load(urllib.request.urlopen(r, timeout=5400))['choices'][0]['message']['content'].strip() + '\n')
print('referee-v3-120b.md written')
