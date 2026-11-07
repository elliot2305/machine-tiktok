#!/usr/bin/env python3
"""Cherche de vraies photos libres sur Wikimedia Commons pour un clip (sans IA) : fetch_photos.py <dossier>
Lit brief.json (commons_queries ou image_queries), écrit img1..3.jpg + credits.json. Ne touche pas aux img* déjà là."""
import json, os, sys, glob, re, urllib.request, urllib.parse
d = sys.argv[1]; b = json.load(open(f'{d}/brief.json'))
if len(glob.glob(f'{d}/img*.*')) >= 3: sys.exit(print('photos déjà là'))
for f in glob.glob(f'{d}/img*.*'): os.remove(f)
UA = {'User-Agent': 'machine-tiktok-bot/1.0 (GitHub Actions)'}
def get(url): return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
qs = b.get('commons_queries') or [re.sub(r'\(.*?\)', '', q).strip() for q in b.get('image_queries', [])]
credits, seen, n = [], set(), 0
want = 3
qs = qs + [' '.join(q.split()[:2]) for q in qs] + [q.split()[-1] for q in qs]
for q in qs:
    if n >= want: break
    got = 0
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'generator': 'search',
          'gsrnamespace': 6, 'gsrsearch': f'{q} filetype:bitmap', 'gsrlimit': 15, 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 1400})
    try: pages = sorted(json.loads(get(api)).get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    except Exception as e: print('erreur', q, e); continue
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
        lic = md.get('LicenseShortName', {}).get('value', '')
        if p['title'] in seen or ii.get('height', 0) < 700 or not re.search(r'CC|Public domain|PD', lic, re.I): continue
        n += 1; seen.add(p['title'])
        open(f'{d}/img{n}.jpg', 'wb').write(get(ii['thumburl']))
        artist = re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', '')).strip()
        credits.append({'file': f'img{n}.jpg', 'query': q, 'title': p['title'], 'author': artist, 'license': lic, 'page': ii.get('descriptionurl')})
        print('OK', q, '->', p['title'], lic); got += 1
        if got >= 2 or n >= want: break
json.dump(credits, open(f'{d}/credits.json', 'w'), ensure_ascii=False, indent=1)
print(n, 'photos')
