# Machine TikTok – Patate Story

Rendu des épisodes (vidéo 1080x1920, 30 i/s) :

1. `python3 tools/episodes.py data/alignment/songN.json ep,ep,ep,ep data/episodes` : découpe la chanson Suno aux lignes `[Shout]` (minutage des paroles).
2. `node tools/render.js <ep> - out/epNN_silent.mp4` : scène 3D `scene/patate.html` + mise en scène `scene/episodes/epNN.js`, capturée image par image.
3. `tools/mux.sh out/epNN_silent.mp4 epNN.mp3 out/epNN.mp4` : colle le son.

Règles (bible S1) : ragot crié affiché dès 0 s, « Partie N/30 », 60-79 s, « À suivre » figé à la fin.
