#!/usr/bin/env bash
# download.sh - 自动下载所有 YouTube 素材
set -e
cd "$(dirname "$0")"
source ./config.sh

mkdir -p "$ASSETS_DIR"

if ! command -v yt-dlp >/dev/null 2>&1; then
    echo "❌ 未检测到 yt-dlp"
    echo "   macOS:  brew install yt-dlp"
    echo "   Linux:  pip install -U yt-dlp"
    echo "   Win:    pip install -U yt-dlp"
    exit 1
fi

echo "🎬 开始下载 YouTube 素材到 $ASSETS_DIR/"
echo ""

for key in "${!YT_SOURCES[@]}"; do
    url="${YT_SOURCES[$key]}"
    target="$ASSETS_DIR/${key}.mp4"
    if [[ -f "$target" ]]; then
        echo "✅ 已存在: $key.mp4 (跳过)"
        continue
    fi
    echo "⬇️  下载 [$key] $url"
    yt-dlp \
        -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]" \
        --merge-output-format mp4 \
        -o "$target" \
        "$url" || {
            echo "⚠️  下载失败: $key  (建议手动下载到 $target)"
            continue
        }
    echo ""
done

echo ""
echo "📦 下载完成。已就绪素材："
ls -lh "$ASSETS_DIR"/*.mp4 2>/dev/null || echo "(目录为空)"
