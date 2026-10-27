#!/bin/bash
set -euo pipefail

asset_root="$(cd "$(dirname "$0")/.." && pwd)"
starter="$asset_root/premiere-foundation-starter/media"
ai_dir="$asset_root/ai-demo"
tmp_dir="$(mktemp -d /private/tmp/acp-pr-media.XXXXXX)"
trap 'rm -rf "$tmp_dir"' EXIT

make_voice() {
  local text="$1"
  local seconds="$2"
  local output="$3"
  local aiff="$tmp_dir/voice-$RANDOM.aiff"
  say -v Meijia -r 165 -o "$aiff" "$text"
  ffmpeg -hide_banner -loglevel error -y -i "$aiff" \
    -af "apad=pad_dur=${seconds},atrim=duration=${seconds}" \
    -ar 48000 -ac 2 "$output"
}

make_still_video() {
  local image="$1"
  local audio="$2"
  local seconds="$3"
  local frames="$4"
  local output="$5"
  ffmpeg -hide_banner -loglevel error -y -i "$image" -i "$audio" \
    -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.00035,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames}:s=1920x1080:fps=25,format=yuv420p[v];[1:a]apad=pad_dur=${seconds},atrim=duration=${seconds}[a]" \
    -map '[v]' -map '[a]' -t "$seconds" -r 25 -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 160k -movflags +faststart "$output"
}

make_voice "第一段是海邊燈塔。請注意畫面右側主體與完整地平線。" 12 "$tmp_dir/foundation-01.wav"
make_voice "第二段是城市通勤。請注意道路方向與畫面中的移動線索。" 10 "$tmp_dir/foundation-02.wav"
make_voice "第三段是社區工作坊。請注意人物活動與前景空間。" 14 "$tmp_dir/foundation-03.wav"

make_still_video "$starter/still-01-lighthouse.png" "$tmp_dir/foundation-01.wav" 12 300 "$starter/clip-01-lighthouse.mp4"
make_still_video "$starter/still-02-city.png" "$tmp_dir/foundation-02.wav" 10 250 "$starter/clip-02-city.mp4"
make_still_video "$starter/still-03-workshop.png" "$tmp_dir/foundation-03.wav" 14 350 "$starter/clip-03-workshop.mp4"

audio_list="$tmp_dir/audio-list.txt"
: > "$audio_list"
while IFS='|' read -r number start end text; do
  [ -n "$number" ] || continue
  aiff="$tmp_dir/ai-${number}.aiff"
  wav="$tmp_dir/ai-${number}.wav"
  say -v Meijia -r 165 -o "$aiff" "$text"
  ffmpeg -hide_banner -loglevel error -y -i "$aiff" \
    -af "adelay=500:all=1,apad=pad_dur=10,atrim=duration=10" \
    -ar 48000 -ac 2 "$wav"
  printf "file '%s'\n" "$wav" >> "$audio_list"
done < "$ai_dir/ai-short-video-demo-script-v1.txt"

ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$audio_list" -c:a pcm_s16le "$tmp_dir/ai-demo.wav"

make_still_video "$starter/still-03-workshop.png" "$tmp_dir/ai-demo.wav" 40 1000 "$tmp_dir/visual-01.mp4"
make_still_video "$starter/still-02-city.png" "$tmp_dir/ai-demo.wav" 40 1000 "$tmp_dir/visual-02-with-audio.mp4"
make_still_video "$starter/still-01-lighthouse.png" "$tmp_dir/ai-demo.wav" 40 1000 "$tmp_dir/visual-03-with-audio.mp4"

video_list="$tmp_dir/video-list.txt"
printf "file '%s'\nfile '%s'\nfile '%s'\n" \
  "$tmp_dir/visual-01.mp4" "$tmp_dir/visual-02-with-audio.mp4" "$tmp_dir/visual-03-with-audio.mp4" > "$video_list"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$video_list" -an -c:v copy "$tmp_dir/ai-visual.mp4"
ffmpeg -hide_banner -loglevel error -y -i "$tmp_dir/ai-visual.mp4" -i "$tmp_dir/ai-demo.wav" \
  -map 0:v -map 1:a -t 120 -c:v copy -c:a aac -b:a 160k -movflags +faststart "$ai_dir/ai-short-video-demo-01.mp4"

ffmpeg -hide_banner -loglevel error -y -i "$tmp_dir/ai-demo.wav" -t 20 -c:a pcm_s16le "$starter/audio-01-voice.wav"

for spec in "01|0.5" "02|80.5" "03|110.5"; do
  IFS='|' read -r number start <<< "$spec"
  ffmpeg -hide_banner -loglevel error -y -ss "$start" -t 8.3 -i "$ai_dir/ai-short-video-demo-01.mp4" \
    -vf "scale=-2:1920,crop=1080:1920,format=yuv420p" -r 25 \
    -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 160k "$tmp_dir/mini-${number}.mp4"
done

mini_list="$tmp_dir/mini-list.txt"
printf "file '%s'\nfile '%s'\nfile '%s'\n" \
  "$tmp_dir/mini-01.mp4" "$tmp_dir/mini-02.mp4" "$tmp_dir/mini-03.mp4" > "$mini_list"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i "$mini_list" \
  -c copy -movflags +faststart "$ai_dir/ai-mini-cut-reference.mp4"

printf '媒體素材由本專案自行生成，供課堂剪輯練習使用。\n' > "$starter/title-text-v1.txt"

echo "Generated foundation clips, narration, 120-second AI demo, and 24.9-second vertical reference cut."
