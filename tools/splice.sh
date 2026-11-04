#!/usr/bin/env bash
# Re-rend un passage [a,b] d'un épisode et le remplace dans la vidéo muette : splice.sh ep a b video.mp4
set -euo pipefail
ep=$1; a=$2; b=$3; v=$4; d=$(dirname "$v")
node "$(dirname "$0")/render.js" "$ep" - "$d/seg_$ep.mp4" --from "$a" --to "$b" --workers 4
ffmpeg -loglevel error -y -i "$v" -i "$d/seg_$ep.mp4" -filter_complex \
 "[0:v]trim=0:$a,setpts=PTS-STARTPTS[x];[1:v]setpts=PTS-STARTPTS[y];[0:v]trim=start=$b,setpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=1[o]" \
 -map "[o]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 "$d/tmp_$ep.mp4"
mv "$d/tmp_$ep.mp4" "$v"; rm -f "$d/seg_$ep.mp4"; echo "spliced $v $a-$b"
