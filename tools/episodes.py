#!/usr/bin/env python3
"""Découpe une chanson Suno en épisodes à partir du minutage des paroles.

Chaque ligne [Shout] = début d'un épisode. Sortie : un JSON par épisode avec
début/fin dans la chanson et les lignes de paroles (mots + temps) recalées à 0.
Usage : episodes.py alignment.json ep1,ep2,... outdir [song_duration]
"""
import json, sys, os

def lines_from(words):
    lines, cur = [], None
    for w in words:
        parts = w['word'].split('\n')
        for i, p in enumerate(parts):
            if i > 0 and cur is not None:
                if cur['text'].strip():
                    lines.append(cur)
                cur = None
            if cur is None:
                cur = {'text': '', 'words': [], 'tag': None}
            if p.strip():
                if p.strip().startswith('['):
                    cur['tag'] = p.strip().strip('[]')
                    continue
                cur['words'].append({'w': p, 't0': w['start_s'], 't1': w['end_s']})
            cur['text'] += p if not p.strip().startswith('[') else ''
    if cur and cur['text'].strip():
        lines.append(cur)
    # propagate section tags
    tag = None
    out = []
    for l in lines:
        if not l['words']:
            tag = l['tag'] or tag
            continue
        l['section'] = tag or l['tag']
        l['t0'] = l['words'][0]['t0']
        l['t1'] = l['words'][-1]['t1']
        l['text'] = l['text'].strip()
        out.append(l)
    return out

def main():
    al, eps, outdir = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], sys.argv[3]
    dur = float(sys.argv[4]) if len(sys.argv) > 4 else None
    d = json.load(open(al))
    words = d['words']
    # tag lines: a word containing "[Shout]" marks the start of a section
    sec = None
    tagged = []
    for w in words:
        if '[' in w['word']:
            for tok in w['word'].split('\n'):
                if tok.strip().startswith('['):
                    sec = tok.strip().strip('[]')
        tagged.append((sec, w))
    lines = []
    cur = None
    for sec, w in tagged:
        raw = w['word']
        segs = raw.split('\n')
        for i, s in enumerate(segs):
            if i > 0:
                if cur and cur['words']:
                    lines.append(cur)
                cur = None
            if s.strip().startswith('[') or not s.strip():
                continue
            if cur is None:
                cur = {'section': sec, 'words': []}
            cur['words'].append({'w': s, 't0': w['start_s'], 't1': w['end_s']})
    if cur and cur['words']:
        lines.append(cur)
    for l in lines:
        l['text'] = ''.join(x['w'] for x in l['words']).strip()
        l['t0'] = l['words'][0]['t0']; l['t1'] = l['words'][-1]['t1']
    # fix the first-line stretch bug: a word lasting > 3 s gets clamped
    for l in lines:
        for x in l['words']:
            if x['t1'] - x['t0'] > 3:
                x['t1'] = x['t0'] + 0.6
        l['t1'] = l['words'][-1]['t1']
    shouts = [i for i, l in enumerate(lines) if l['section'] == 'Shout']
    os.makedirs(outdir, exist_ok=True)
    for k, ep in enumerate(eps):
        a = shouts[k]
        b = shouts[k + 1] if k + 1 < len(shouts) else len(lines)
        start = 0.0 if k == 0 else lines[a]['t0'] - 0.15
        end = (lines[b]['t0'] - 0.15) if b < len(lines) else (dur or lines[-1]['t1'] + 2)
        eplines = []
        for l in lines[a:b]:
            eplines.append({
                'section': l['section'], 'text': l['text'],
                't0': round(l['t0'] - start, 3), 't1': round(l['t1'] - start, 3),
                'words': [{'w': x['w'], 't0': round(x['t0'] - start, 3), 't1': round(x['t1'] - start, 3)} for x in l['words']],
            })
        out = {'episode': ep, 'song_start': round(start, 3), 'song_end': round(end, 3),
               'duration': round(end - start, 3), 'shout': eplines[0]['text'], 'lines': eplines}
        json.dump(out, open(os.path.join(outdir, f'ep{ep:02d}.json'), 'w'), ensure_ascii=False, indent=1)
        print(f"ep{ep:02d} {start:7.2f}-{end:7.2f} ({end-start:5.1f}s) {out['shout']}")

if __name__ == '__main__':
    main()
