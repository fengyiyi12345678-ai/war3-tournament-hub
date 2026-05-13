#!/usr/bin/env bash
# make_video.sh - 一键生成 30 秒抖音竖屏视频
set -e
cd "$(dirname "$0")"
source ./config.sh

# ============ 0. 环境检查 ============
echo "🔍 检查环境……"
command -v ffmpeg >/dev/null 2>&1 || { echo "❌ 未检测到 ffmpeg"; echo "   macOS: brew install ffmpeg"; echo "   Linux: apt install ffmpeg"; exit 1; }
[[ -z "$FONT" ]] && { echo "⚠️  未找到中文字体，文字卡片将退化为英文。"; FONT_OPT=""; } || { echo "✅ 字体: $FONT"; FONT_OPT="fontfile=$FONT:"; }

mkdir -p "$CLIPS_DIR" "$FINAL_DIR"
rm -f "$CLIPS_DIR"/*.mp4

# ============ 1. 通用滤镜：竖屏化 ============
SCALE_VF="scale=${WIDTH}:${HEIGHT}:force_original_aspect_ratio=increase,crop=${WIDTH}:${HEIGHT},fps=${FPS},setsar=1,format=yuv420p"

make_yt_clip() {
    local idx=$1 dur=$2 src=$3 start=$4 title=$5 sub=$6 extra=$7
    local in="$ASSETS_DIR/${src}.mp4"
    local out="$CLIPS_DIR/clip$(printf %02d $idx).mp4"

    if [[ ! -f "$in" ]]; then
        echo "⚠️  缺素材 $in → 用占位卡片替代"
        make_card_clip "$idx" "$dur" "$title" "$sub" "#1A1A1A"
        return
    fi

    local vf="$SCALE_VF"
    [[ "$extra" == "sepia" ]] && vf="$SCALE_VF,colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,noise=alls=12:allf=t"

    # 文字叠加（标题+副标题）
    if [[ -n "$FONT" && -n "$title" ]]; then
        vf="$vf,drawbox=x=0:y=h-360:w=w:h=360:color=black@0.6:t=fill"
        vf="$vf,drawtext=${FONT_OPT}text='${title}':fontsize=64:fontcolor=#FFD700:x=(w-text_w)/2:y=h-280:borderw=3:bordercolor=black"
        vf="$vf,drawtext=${FONT_OPT}text='${sub}':fontsize=42:fontcolor=white:x=(w-text_w)/2:y=h-180:borderw=2:bordercolor=black"
    fi

    echo "🎞  [片段 $idx] 截取 ${src} ${start}s+${dur}s"
    ffmpeg -y -ss "$start" -i "$in" -t "$dur" -vf "$vf" -an -c:v libx264 -preset fast -crf 20 "$out" 2>/dev/null
}

make_card_clip() {
    local idx=$1 dur=$2 title=$3 sub=$4 bg=$5
    local out="$CLIPS_DIR/clip$(printf %02d $idx).mp4"
    # 把 #RRGGBB 转成 0xRRGGBB
    bg_hex="${bg/#\#/0x}"

    local vf="format=yuv420p"
    if [[ -n "$FONT" ]]; then
        vf="${vf},drawtext=${FONT_OPT}text='${title}':fontsize=92:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100:borderw=4:bordercolor=black"
        vf="${vf},drawtext=${FONT_OPT}text='${sub}':fontsize=46:fontcolor=#FFD700:x=(w-text_w)/2:y=(h-text_h)/2+60:borderw=3:bordercolor=black"
    fi

    echo "🃏 [片段 $idx] 文字卡片  $title"
    ffmpeg -y -f lavfi -i "color=c=${bg_hex}:s=${WIDTH}x${HEIGHT}:d=${dur}:r=${FPS}" \
        -vf "$vf" -c:v libx264 -preset fast -crf 20 "$out" 2>/dev/null
}

# ============ 2. 渲染所有片段 ============
echo ""
echo "🎬 渲染 8 个片段……"
for line in "${TIMELINE[@]}"; do
    IFS='|' read -r idx dur type src start title sub extra <<<"$line"
    case "$type" in
        yt|mix)  make_yt_clip "$idx" "$dur" "$src" "$start" "$title" "$sub" "$extra" ;;
        card)    make_card_clip "$idx" "$dur" "$title" "$sub" "$extra" ;;
    esac
done

# ============ 3. 拼接 ============
echo ""
echo "🔗 拼接片段……"
LIST="$CLIPS_DIR/list.txt"
ls "$CLIPS_DIR"/clip*.mp4 | sort | sed "s/.*/file '&'/" > "$LIST"
ffmpeg -y -f concat -safe 0 -i "$LIST" -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -r "$FPS" "$FINAL_DIR/merged.mp4" 2>/dev/null

# ============ 4. 烧录字幕 ============
echo "📝 烧录字幕……"
SUB_STYLE="FontSize=40,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,MarginV=240,Alignment=2"
[[ -n "$FONT" ]] && SUB_STYLE="FontName=$(basename "${FONT%.*}"),${SUB_STYLE}"

ffmpeg -y -i "$FINAL_DIR/merged.mp4" \
    -vf "subtitles=./subtitles.srt:force_style='${SUB_STYLE}'" \
    -c:v libx264 -preset fast -crf 18 "$FINAL_DIR/subbed.mp4" 2>/dev/null

# ============ 5. 加 BGM（可选） ============
if [[ -f "./bgm.mp3" ]]; then
    echo "🎵 混入 BGM……"
    ffmpeg -y -i "$FINAL_DIR/subbed.mp4" -i "./bgm.mp3" \
        -filter_complex "[1:a]volume=0.4,afade=t=in:st=0:d=0.5,afade=t=out:st=29:d=1[a]" \
        -map 0:v -map "[a]" -shortest -c:v copy -c:a aac -b:a 192k "$FINAL_DIR/$OUTPUT" 2>/dev/null
else
    echo "⚠️  未找到 ./bgm.mp3 → 输出无配乐版本"
    cp "$FINAL_DIR/subbed.mp4" "$FINAL_DIR/$OUTPUT"
fi

# ============ 6. 清理 ============
rm -f "$FINAL_DIR/merged.mp4" "$FINAL_DIR/subbed.mp4"

echo ""
echo "✅ 完成！"
echo "📁 输出: $FINAL_DIR/$OUTPUT"
echo "📐 尺寸: ${WIDTH}x${HEIGHT} @ ${FPS}fps · 时长 30s"
echo ""
echo "👉 直接拖进抖音 / 小红书上传即可"
