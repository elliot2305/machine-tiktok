#!/usr/bin/env bash
# Colle le MP3 d'un épisode sur la vidéo muette : mux.sh video_muette.mp4 episode.mp3 sortie.mp4
set -euo pipefail
v=$1; a=$2; o=$3
vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
ffmpeg -loglevel error -y -i "$v" -i "$a" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k \
  -af "apad,atrim=0:${vd},afade=t=out:st=$(echo "$vd - 0.5" | bc):d=0.5" -movflags +faststart "$o"
echo "OK $o ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$o") s)"
