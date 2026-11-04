#!/usr/bin/env bash
# Recadre la vidéo muette (temps chanson) sur la coupe officielle du MP3 et colle le son.
# finalize.sh <ep> <silent.mp4> <ep.mp3> <out.mp4>
set -euo pipefail
ep=$((10#$1)); v=$2; a=$3; o=$4
case $ep in
  1) f="[0:v]trim=start=1.13,setpts=PTS-STARTPTS[v]";;
  2) f="[0:v]trim=0:4.4,setpts=PTS-STARTPTS[a];[0:v]trim=start=13.98,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1[v]";;
  3) f="[0:v]trim=start=0.57,setpts=PTS-STARTPTS[v]";;
  *) echo "coupe inconnue pour ép $ep (voir outils/decoupe_episodes_S1.py)"; exit 1;;
esac
ffmpeg -loglevel error -y -i "$v" -i "$a" -filter_complex "$f" -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$o"
echo "OK $o"
