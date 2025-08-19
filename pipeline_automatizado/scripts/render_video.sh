#!/bin/bash
# Renderizador de video - Pipeline CO-RA
# Compone video vertical con gráficos, subtítulos y música

set -e

# Parámetros
SUBJECT=${1:-"sueldos_morelos"}
BROLL=${2:-"content/$SUBJECT/broll/clip1.mp4"}
CHART="content/$SUBJECT/out/chart_salarios.png"
MUSIC=${3:-"content/$SUBJECT/music/track.mp3"}
SRT="content/$SUBJECT/out/subs.srt"
OUT="content/$SUBJECT/out/video_final.mp4"

echo "🎬 Renderizando video: $SUBJECT"
echo "📊 Gráfico: $CHART"
echo "🎵 Música: $MUSIC"
echo "📝 Subtítulos: $SRT"

# Verificar archivos requeridos
for file in "$BROLL" "$CHART" "$MUSIC" "$SRT"; do
    if [[ ! -f "$file" ]]; then
        echo "❌ Error: Archivo no encontrado: $file"
        exit 1
    fi
done

# Crear directorio de salida
mkdir -p "$(dirname "$OUT")"

# Renderizar con FFmpeg
ffmpeg -y \
    -i "$BROLL" \
    -i "$MUSIC" \
    -loop 1 -t 15 -i "$CHART" \
    -filter_complex "
        [0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p[v0];
        [2:v]scale=900:-1[chart];
        [v0][chart]overlay=90:200[v1];
        [v1]subtitles='$SRT':force_style='FontSize=32,PrimaryColour=&H00FFFFFF&,BackColour=&HAA000000&,BorderStyle=3,Outline=2'[v_final]
    " \
    -map "[v_final]" -map 1:a \
    -c:v libx264 -preset medium -crf 20 \
    -c:a aac -b:a 128k \
    -shortest \
    -movflags +faststart \
    "$OUT"

echo "✅ Video generado: $OUT"

# Generar miniatura
THUMB="content/$SUBJECT/out/thumbnail.jpg"
ffmpeg -y -i "$OUT" -ss 00:00:03 -vframes 1 -q:v 2 "$THUMB"
echo "🖼️  Miniatura: $THUMB"

# Información del video
echo "📊 Información del video:"
ffprobe -v quiet -print_format json -show_format -show_streams "$OUT" | jq -r '
    "Duración: " + (.format.duration | tonumber | floor | tostring) + "s",
    "Resolución: " + .streams[0].width + "x" + .streams[0].height,
    "Tamaño: " + ((.format.size | tonumber) / 1024 / 1024 | floor | tostring) + "MB"
'