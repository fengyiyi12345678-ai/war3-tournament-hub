#!/usr/bin/env bash
# run.sh - 一键全流程（下载 + 生成）
set -e
cd "$(dirname "$0")"

echo "═══════════════════════════════════════"
echo "  🦅 拉齐奥 vs 国米 抖音视频生成 Pipeline"
echo "═══════════════════════════════════════"
echo ""

chmod +x ./download.sh ./make_video.sh

# Step 1
bash ./download.sh

echo ""
echo "═══════════════════════════════════════"
echo ""

# Step 2
bash ./make_video.sh

echo ""
echo "═══════════════════════════════════════"
echo "  🎉 全部完成！"
echo "═══════════════════════════════════════"
