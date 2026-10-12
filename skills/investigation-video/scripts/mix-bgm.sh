#!/bin/zsh
# 旁白 + 闪避配乐 混音，视频流不重编码
set -e
FF=${FFMPEG:-ffmpeg}
BGM=${BGM:-assets/bgm.mp3}   # 自备配乐，仓库不附带
NAR=renderer/public/narration.wav
VID=renders/full-silent-b.mp4
OUT=renders/mix-pre-loudnorm.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$NAR")
$FF -nostdin -y -v error \
 -i "$VID" -i "$NAR" \
 -stream_loop -1 -t "$DUR" -ss 0 -to 97 -i "$BGM" \
 -filter_complex "[2:a]volume=0.22,aresample=48000,afade=t=in:st=0:d=1.5,afade=t=out:st=$(echo "$DUR-3.5"|bc):d=3.5[bg];\
[1:a]asplit=2[nar][key];\
[bg][key]sidechaincompress=threshold=0.008:ratio=6:attack=20:release=350[duck];\
[duck]asplit=2[duckA][duckB];\
[nar][duckA]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95[mix]" \
 -map 0:v -map "[mix]" -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT" \
 -map "[duckB]" -c:a pcm_s16le renders/duck-bgm.wav
echo "MIX_DONE $OUT"
