#!/usr/bin/env python3
"""Actu en chanson, étape 3 : brief.json + alignment.json (minutage Suno) + durée du MP3 -> clip.json pour scene/actu.html.
Usage : actu_build.py data/actu/<slug> <durée_s>"""
import json, sys, glob, os, re
d, dur = sys.argv[1], float(sys.argv[2])
b = json.load(open(f'{d}/brief.json')); al = json.load(open(f'{d}/alignment.json'))
lines, cur = [], []
for w in al['words']:
    raw = w['word']; parts = raw.split('\n')
    for i, p in enumerate(parts):
        if i > 0 and cur: lines.append(cur); cur = []
        p = re.sub(r'\[[^\]]*\]', '', p)
        if not p.strip(): continue
        if cur and not p.startswith(' ') and i == 0: cur[-1]['w'] += p.strip()
        else: cur.append({'w': p.strip(), 't0': round(w['start_s'], 2), 't1': round(w['end_s'], 2)})
if cur: lines.append(cur)
# Intro sans voix : on la coupe pour que la phrase choc tombe à ~0,4 s (hook dans la 1re seconde).
skip = round(lines[0][0]['t0'] - 0.4, 2) if lines and lines[0][0]['t0'] > 1.5 else 0
for l in lines:
    for x in l: x['t0'] = round(x['t0'] - skip, 2); x['t1'] = round(x['t1'] - skip, 2)
dur -= skip
# Coupe : si la chanson dépasse 82 s, on s'arrête à la fin de la dernière ligne finie entre 60 et 80 s.
full = dur
if dur > 82:
    ends = [l[-1]['t1'] for l in lines if 60 <= l[-1]['t1'] <= 80]
    dur = round((max(ends) if ends else 78) + 1.2, 2)
    lines = [l for l in lines if l[0]['t0'] < dur - 0.5]
if dur > 3 + max((l[-1]['t1'] for l in lines), default=0): dur = round(max(l[-1]['t1'] for l in lines) + 3, 2)  # pas de longue outro
L = [{'t0': l[0]['t0'], 't1': l[-1]['t1'] + 0.3, 'words': [{'w': x['w'], 't0': x['t0']} for x in l]} for l in lines if l]
cs = sorted(b.get('cards', []), key=lambda c: c.get('at', 0)); cards = []
for i, c in enumerate(cs):
    c = dict(c); t0 = c.pop('at', 0) * dur; t1 = cs[i + 1]['at'] * dur if i + 1 < len(cs) else 99
    cards.append({'t0': round(t0, 2), 't1': round(t1, 2), **c})
imgs = sorted(glob.glob(f'{d}/img*.*')) or sorted(glob.glob('data/actu/test/el_*.png'))
kick = b.get('kicker', 'FLASH INFO')
clip = {'title': b['title'], 'kicker': kick, 'fx': kick == 'FLASH INFO', 'ia': not glob.glob(f'{d}/img*.*'), 'part': b.get('part', 'ACTU'), 'duration': dur, 'sources': b.get('sources', []),
        'images': imgs, 'cards': cards, 'lines': L}
json.dump(clip, open(f'{d}/clip.json', 'w'), ensure_ascii=False)
open(f'{d}/cut.txt', 'w').write(str(dur)); open(f'{d}/skip.txt', 'w').write(str(skip))
print(f'{d}/clip.json', len(L), 'lignes', len(imgs), 'images', f'coupe {dur}s / {full}s')
