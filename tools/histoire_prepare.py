#!/usr/bin/env python3
"""Histoire vraie folle en chanson, étape 1 (GitHub Actions, clé API) : trouve une histoire vraie dingue mais PAS tragique,
vérifie chaque fait (2 sources min.), écrit paroles + prompt Suno + cartes + recherche photos. Sortie : data/histoire/<slug>/brief.json"""
import json, os, re, sys, datetime, urllib.request
MODEL = os.environ.get('ACTU_MODEL', 'claude-sonnet-5-5')
today = datetime.date.today().isoformat()
deja = sorted(os.listdir('data/histoire')) if os.path.isdir('data/histoire') else []
PROMPT = f"""Tu prépares un clip TikTok « Histoire vraie en chanson » (public français, 65-80 s).
1. Cherche sur le web UNE histoire vraie complètement folle mais PAS tragique : arnaque géniale, évasion absurde, coïncidence dingue,
   pari fou, braquage raté ridicule... INTERDIT : morts, enfants victimes, violences, maladie, drame. Les gens doivent rire et dire « c'est pas possible ».
   Une histoire connue en France ou facile à comprendre sans contexte. Déjà faites (à éviter) : {', '.join(deja) or 'aucune'}.
2. Vérifie chaque fait (date, lieu, chiffre, nom) avec AU MOINS 2 sources reconnues différentes (presse, Wikipédia + un média...). Un fait non confirmé par 2 sources = tu ne l'utilises pas. Zéro invention.
3. Écris une chanson drôle et ultra-accrocheuse en français familier qui RACONTE l'histoire dans l'ordre (début, embrouille, retournement final), style pop urbaine / afropop / rap mélodique.
   Courte : 1 hook crié + 2 couplets de 4 lignes + 1 refrain répété 2 fois, et c'est tout (la chanson doit faire ~75 s).
   La 1re ligne est la phrase choc criée (préfixe [Shout]), compréhensible sans contexte, qui donne envie de savoir la suite (ex. « Il a vendu la tour Eiffel... deux fois ! »).
   Balises Suno [Shout] [Verse] [Chorus] autorisées.
Réponds UNIQUEMENT par un JSON (pas de texte autour) :
{{"slug":"motcle-court","title":"TITRE COURT EN MAJ (max 28 car.)","part":"HISTOIRE VRAIE","kicker":"HISTOIRE VRAIE","summary":"2 phrases",
"facts":[{{"fact":"...","sources":["url1","url2"]}}],"sources":["Média 1","Média 2"],
"lyrics":"paroles complètes avec balises","suno_style":"style musical en anglais, max 200 car.",
"cards":[{{"at":0,"big":"PHRASE CHOC (max 40 car.)","size":130}},{{"at":0.3,"big":"DATE OU CHIFFRE CLÉ","sub":"court contexte"}},{{"at":0.6,"big":"LE RETOURNEMENT","color":"#ffd60a"}},{{"at":0.88,"type":"camps","big":"T'AURAIS FAIT QUOI ?","a":"CHOIX 1","b":"CHOIX 2"}}],
"commons_queries":["3 recherches courtes en anglais pour trouver de VRAIES photos libres sur Wikimedia Commons (lieu, objet, époque de l'histoire, pas de visage d'anonyme)"]}}
« at » = position dans le clip entre 0 et 1. La 1re carte (at 0) affiche la phrase choc en gros dès la 1re seconde."""
body = {"model": MODEL, "max_tokens": 8000, "messages": [{"role": "user", "content": PROMPT}],
        "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 12}]}
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
d = f'data/histoire/{slug}'; os.makedirs(d, exist_ok=True)
json.dump(brief, open(f'{d}/brief.json', 'w'), ensure_ascii=False, indent=1)
print(d); print(json.dumps(r.get('usage', {})))
