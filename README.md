# Machine TikTok – Patate Story

Rendu des épisodes (vidéo 1080x1920, 30 i/s) :

1. `python3 tools/episodes.py data/alignment/songN.json ep,ep,ep,ep data/episodes` : découpe la chanson Suno aux lignes `[Shout]` (minutage des paroles).
2. `node tools/render.js <ep> - out/epNN_silent.mp4` : scène 3D `scene/patate.html` + mise en scène `scene/episodes/epNN.js`, capturée image par image.
3. `tools/mux.sh out/epNN_silent.mp4 epNN.mp3 out/epNN.mp4` : colle le son.

Règles (bible S1) : ragot crié affiché dès 0 s, « Partie N/30 », 60-79 s, « À suivre » figé à la fin.

Coupes audio officielles (outils/decoupe_episodes_S1.py du zip sources) : la vidéo muette est rendue en temps « chanson »,
puis recadrée sur les segments du MP3 (ex. ép 1 : 1,13 s → fin ; ép 2 : 0-4,4 s + 13,98 s → fin ; ép 3 : 0,57 s → fin).

## Actu en chanson (GitHub Actions)

1. **actu-prepare** (clé API) : modifier `.github/actu-trigger` → sujet du jour, faits vérifiés (2 sources), paroles, prompt Suno → `data/actu/<slug>/brief.json`.
2. **Suno** (seule étape hors Actions, connecteur Suno dans Claude) : générer avec `lyrics` + `suno_style`, télécharger, minutage → déposer `song.mp3` + `alignment.json` dans le dossier (+ `img1..3` facultatives).
3. **render-actu** : se lance tout seul à l'arrivée du `song.mp3` → MP4 en artefact `actu-mp4`.
