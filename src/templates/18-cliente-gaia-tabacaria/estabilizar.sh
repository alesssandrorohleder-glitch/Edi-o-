#!/bin/bash
# Uso: ./estabilizar.sh <pasta_com_os_.mov_originais>
# Estabiliza (vidstab 2 passes), aplica grade leve e gera _frames_src/C####.mp4 em 1080x1920 60fps (horizontais ficam 1920x1080).
SRC="$1"; OUT="$(dirname "$0")/_frames_src"; mkdir -p "$OUT"
for f in "$SRC"/*C41*.m*; do n=$(basename "$f" | sed 's/.*\(C41[0-9]*\)\..*/\1/'); [ -f "$OUT/$n.mp4" ] && continue
  ffmpeg -loglevel error -y -i "$f" -vf vidstabdetect=shakiness=6:accuracy=15:result="/tmp/$n.trf" -f null - &&
  ffmpeg -loglevel error -y -i "$f" -vf "vidstabtransform=input=/tmp/$n.trf:smoothing=30:zoom=4:optzoom=0:interpol=bicubic,unsharp=5:5:0.35,eq=contrast=1.05:saturation=1.05:gamma=0.98" -an -c:v libx264 -crf 17 -preset fast -pix_fmt yuv420p "$OUT/$n.mp4" && echo "$n ok"
done
