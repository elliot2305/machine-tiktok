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
L = [{'t0': l[0]['t0'], 't1': l[-1]['t1'] + 0.3, 'words': [{'w': x['w'], 't0': x['t0']} for x in l]} for l in lines if l]
cs = sorted(b.get('cards', []), key=lambda c: c.get('at', 0)); cards = []
for i, c in enumerate(cs):
    c = dict(c); t0 = c.pop('at', 0) * dur; t1 = cs[i + 1]['at'] * dur if i + 1 < len(cs) else 99
    cards.append({'t0': round(t0, 2), 't1': round(t1, 2), **c})
imgs = sorted(glob.glob(f'{d}/img*.*')) or sorted(glob.glob('data/actu/test/el_*.png'))
clip = {'title': b['title'], 'part': b.get('part', 'ACTU'), 'duration': dur, 'sources': b.get('sources', []),
        'images': imgs, 'cards': cards, 'lines': L}
json.dump(clip, open(f'{d}/clip.json', 'w'), ensure_ascii=False)
print(f'{d}/clip.json', len(L), 'lignes', len(imgs), 'images')
