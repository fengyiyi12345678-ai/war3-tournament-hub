#!/usr/bin/env bash
# config.sh - 视频生成参数 + 素材源
# 改这一份就够，main 脚本会引用

# ============ 输出参数 ============
export WIDTH=1080
export HEIGHT=1920
export FPS=30
export OUTPUT="lazio_inter_30s.mp4"

# ============ 工作目录 ============
export ASSETS_DIR="./assets"
export CLIPS_DIR="./clips"
export FINAL_DIR="./out"

# ============ YouTube 素材源 ============
# 注释里写的是被截取段在原片中的大致起始秒，可按需调整
declare -gA YT_SOURCES=(
    [inter_celebration]="https://www.youtube.com/watch?v=vgHwOfIB6Qk"   # Inter 3-0 Lazio 集锦
    [dazn_highlights]="https://www.youtube.com/watch?v=4iRpY1KXfOY"     # DAZN Tris Inter 集锦
    [history_2000]="https://www.youtube.com/watch?v=f4UvzFrClsY"        # 2000 决赛全场
    [stadium_aerial]="https://www.youtube.com/watch?v=w7Ar_QoWPvU"      # 罗马奥林匹克航拍
)

# ============ 中文字体（自动检测） ============
detect_font() {
    local candidates=(
        "/System/Library/Fonts/PingFang.ttc"
        "/System/Library/Fonts/STHeiti Medium.ttc"
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
        "C:/Windows/Fonts/msyh.ttc"
    )
    for f in "${candidates[@]}"; do
        if [[ -f "$f" ]]; then
            echo "$f"
            return 0
        fi
    done
    echo ""
}
export FONT="${FONT:-$(detect_font)}"

# ============ 30s 时间线 ============
# 格式: 段号|时长秒|来源类型|来源标识|起始秒|主标题|副标题|背景色
# 类型: yt=YouTube 截取 | card=纯色文字卡片 | mix=YouTube 加滤镜
export TIMELINE=(
    "1|2.5|yt|inter_celebration|6|国米已锁意甲冠军|账面碾压一切|#000000"
    "2|3.5|yt|dazn_highlights|10|3 天前 同球场|0-3 暴击拉齐奥|#001A4D"
    "3|4.0|card||0|🚨 国米锋线塌一半|图拉姆 ❌ 恰球王 ❌ 小埃斯 ❌|#1A0000"
    "4|3.0|card||0|🦅 拉齐奥反扑|队长扎卡尼伤愈回归|#009EE0"
    "5|4.0|mix|history_2000|120|26 年前 · 2000 年|拉齐奥 2-1 干翻国米|sepia"
    "6|5.0|yt|stadium_aerial|10|罗马奥林匹克|今晚 · 决战之夜|#0F2027"
    "7|5.0|card||0|🎯 预测|拉齐奥拖加时 / 1-2 / 1-1|#0F0F14"
    "8|3.0|card||0|你押谁？|扣 1 国米 · 扣 2 拉齐奥|#E63946"
)
