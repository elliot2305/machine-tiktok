#!/usr/bin/env python3
"""Actu en chanson, étape 1 (GitHub Actions, clé API) : choisit le sujet le plus chaud du jour en France,
vérifie les faits (2 sources min.), écrit paroles + prompt Suno + cartes. Sortie : data/actu/<slug>/brief.json"""
import json, os, re, sys, datetime, urllib.request
MODEL = os.environ.get('ACTU_MODEL', 'claude-sonnet-5-5')
today = datetime.date.today().isoformat()
PROMPT = f"""On est le {today}. Tu prépares un clip TikTok « Actu en chanson » (France, 60-75 s).
1. Cherche sur le web LE sujet d'actu le plus brûlant du jour en France (grand public, pas un drame avec victimes).
2. Vérifie chaque chiffre/fait avec AU MOINS 2 sources de médias reconnus différents. Zéro fake news : un fait non confirmé par 2 sources = tu ne l'utilises pas.
3. Écris une chanson drôle et accrocheuse en français familier (style rap mélodique / afropop / pop urbaine), 3 couplets courts + refrain.
   La 1re ligne est un hook crié (préfixe [Shout]) compréhensible sans contexte. Balises Suno [Verse] [Chorus] [Shout] autorisées.
Réponds UNIQUEMENT par un JSON (pas de texte autour) :
{{"slug":"{today}-motcle","title":"TITRE COURT EN MAJ (max 28 car.)","part":"ACTU","summary":"2 phrases",
"facts":[{{"fact":"...","sources":["url1","url2"]}}],"sources":["Média 1","Média 2"],
"lyrics":"paroles complètes avec balises","suno_style":"style musical en anglais, max 200 car.",
"cards":[{{"at":0.05,"big":"CHIFFRE CLÉ","sub":"selon ..."}},{{"at":0.35,"big":"...","sub":"..."}},{{"at":0.65,"big":"QUESTION ?","color":"#ffd60a"}},{{"at":0.9,"type":"camps","big":"ET TOI ?"}}],
"image_queries":["3 idées de photos libres de droits à chercher"]}}
« at » = position dans le clip entre 0 et 1."""
body = {"model": MODEL, "max_tokens": 8000, "messages": [{"role": "user", "content": PROMPT}],
        "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]}
req = urllib.request.Request('https://api.anthropic.com/v1/messages', json.dumps(body).encode(),
      {'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
r = json.load(urllib.request.urlopen(req, timeout=600))
text = ''.join(b.get('text', '') for b in r['content'] if b['type'] == 'text')
m = re.search(r'\{.*\}', text, re.S)
if not m: sys.exit('Pas de JSON dans la réponse :\n' + text)
brief = json.loads(m.group(0))
bad = [f['fact'] for f in brief.get('facts', []) if len(set(f.get('sources', []))) < 2]
if bad: sys.exit('Faits sans 2 sources, refusé : ' + json.dumps(bad, ensure_ascii=False))
slug = re.sub(r'[^a-z0-9-]', '', brief.get('slug', today).lower()) or today
d = f'data/actu/{slug}'; os.makedirs(d, exist_ok=True)
json.dump(brief, open(f'{d}/brief.json', 'w'), ensure_ascii=False, indent=1)
print(d); print(json.dumps(r.get('usage', {})))
