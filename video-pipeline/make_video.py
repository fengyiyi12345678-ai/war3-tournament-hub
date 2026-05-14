#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_video.py - 跨平台视频生成器（Windows/macOS/Linux 都能跑）
依赖: yt-dlp (pip install yt-dlp) + ffmpeg (在 PATH 中)
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# ============ 输出参数 ============
WIDTH, HEIGHT, FPS = 1080, 1920, 30
OUTPUT_NAME = "lazio_inter_30s.mp4"

# ============ 目录 ============
HERE = Path(__file__).parent.resolve()
ASSETS = HERE / "assets"
CLIPS = HERE / "clips"
OUT = HERE / "out"
SRT_FILE = HERE / "subtitles.srt"

# ============ 素材源 ============
YT_SOURCES = {
    "inter_celebration": "https://www.youtube.com/watch?v=vgHwOfIB6Qk",
    # 把意大利地区屏蔽的 DAZN 官方版换成可全球访问的替代源
    "dazn_highlights":   "https://www.youtube.com/watch?v=H3SXkgNRhMU",
    "history_2000":      "https://www.youtube.com/watch?v=f4UvzFrClsY",
    "stadium_aerial":    "https://www.youtube.com/watch?v=w7Ar_QoWPvU",
}

# ============ 30 秒时间线 ============
# (idx, duration, type, source_key, start_sec, title, subtitle, extra)
TIMELINE = [
    (1, 2.5, "yt",   "inter_celebration", 6,   "国米已锁意甲冠军",   "账面碾压一切",           "#000000"),
    (2, 3.5, "yt",   "dazn_highlights",   10,  "3 天前 同球场",      "0-3 暴击拉齐奥",         "#001A4D"),
    (3, 4.0, "card", None,                0,   "🚨 国米锋线塌一半",  "图拉姆 X 恰球王 X 小埃斯", "#1A0000"),
    (4, 3.0, "card", None,                0,   "🦅 拉齐奥反扑",      "队长扎卡尼伤愈回归",     "#009EE0"),
    (5, 4.0, "mix",  "history_2000",      120, "26 年前 · 2000 年",  "拉齐奥 2-1 干翻国米",    "sepia"),
    (6, 5.0, "yt",   "stadium_aerial",    10,  "罗马奥林匹克",       "今晚 · 决战之夜",        "#0F2027"),
    (7, 5.0, "card", None,                0,   "🎯 预测",            "拉齐奥拖加时 / 1-2 / 1-1","#0F0F14"),
    (8, 3.0, "card", None,                0,   "你押谁？",           "扣 1 国米 · 扣 2 拉齐奥","#E63946"),
]

# ============ 字体检测 ============
def find_font():
    candidates = [
        # Windows
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        # Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None

FONT = find_font()

# ============ FFmpeg 路径转义 ============
def ff_path(p: Path) -> str:
    s = str(p)
    if sys.platform == "win32":
        s = s.replace("\\", "/").replace(":", r"\:")
    return s

def font_escape(p: str) -> str:
    s = p
    if sys.platform == "win32":
        s = s.replace("\\", "/").replace(":", r"\:")
    return s

def text_escape(s: str) -> str:
    # ffmpeg drawtext 的转义：单引号 / 冒号 / 反斜杠
    return s.replace("\\", "\\\\").replace(":", r"\:").replace("'", r"\'")

# ============ 工具检查 ============
def check_tools():
    print("🔍 检查环境……")
    if not shutil.which("ffmpeg"):
        print("❌ 未找到 ffmpeg。请装好 ffmpeg 后重试。")
        sys.exit(1)
    print("✅ ffmpeg")
    if FONT:
        print(f"✅ 中文字体: {FONT}")
    else:
        print("⚠️  未找到中文字体，文字将退化为英文。")

# ============ 下载 YouTube 素材 ============
def download_assets():
    ASSETS.mkdir(exist_ok=True)
    try:
        import yt_dlp
    except ImportError:
        print("❌ 缺少 yt-dlp，正在自动安装……")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        import yt_dlp

    for key, url in YT_SOURCES.items():
        target = ASSETS / f"{key}.mp4"
        if target.exists() and target.stat().st_size > 0:
            print(f"✅ 已存在: {key}.mp4")
            continue
        print(f"⬇️  下载 [{key}] {url}")
        opts = {
            "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
            "merge_output_format": "mp4",
            "outtmpl": str(target),
            "quiet": False,
            "no_warnings": True,
            "socket_timeout": 20,
            "retries": 2,
            "fragment_retries": 2,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"⚠️  下载失败 [{key}]: {e}")
            print(f"   你也可以手动下载并保存为: {target}")

# ============ 渲染单个 YT 片段 ============
def make_yt_clip(idx, dur, src_key, start, title, sub, extra):
    src = ASSETS / f"{src_key}.mp4"
    out = CLIPS / f"clip{idx:02d}.mp4"
    if not src.exists():
        print(f"⚠️  缺素材 {src.name} → 用占位卡片替代")
        return make_card(idx, dur, title, sub, "#1A1A1A")

    vf = f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},fps={FPS},setsar=1,format=yuv420p"
    if extra == "sepia":
        vf += ",colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,noise=alls=12:allf=t"

    if FONT and title:
        font_p = font_escape(FONT)
        vf += f",drawbox=x=0:y=h-360:w=w:h=360:color=black@0.6:t=fill"
        vf += f",drawtext=fontfile='{font_p}':text='{text_escape(title)}':fontsize=64:fontcolor=#FFD700:x=(w-text_w)/2:y=h-280:borderw=3:bordercolor=black"
        vf += f",drawtext=fontfile='{font_p}':text='{text_escape(sub)}':fontsize=42:fontcolor=white:x=(w-text_w)/2:y=h-180:borderw=2:bordercolor=black"

    print(f"🎞  [{idx}] 截取 {src_key} +{start}s/{dur}s")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", str(start), "-i", str(src),
        "-t", str(dur), "-vf", vf, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        str(out)
    ]
    subprocess.run(cmd, check=True)

# ============ 渲染文字卡片 ============
def make_card(idx, dur, title, sub, bg):
    out = CLIPS / f"clip{idx:02d}.mp4"
    bg_hex = bg.replace("#", "0x")
    vf = "format=yuv420p"
    if FONT:
        font_p = font_escape(FONT)
        vf += f",drawtext=fontfile='{font_p}':text='{text_escape(title)}':fontsize=92:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100:borderw=4:bordercolor=black"
        vf += f",drawtext=fontfile='{font_p}':text='{text_escape(sub)}':fontsize=46:fontcolor=#FFD700:x=(w-text_w)/2:y=(h-text_h)/2+60:borderw=3:bordercolor=black"
    print(f"🃏 [{idx}] 文字卡片: {title}")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi",
        "-i", f"color=c={bg_hex}:s={WIDTH}x{HEIGHT}:d={dur}:r={FPS}",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        str(out)
    ]
    subprocess.run(cmd, check=True)

# ============ 拼接 + 烧字幕 + 加 BGM ============
def finalize():
    OUT.mkdir(exist_ok=True)
    # 拼接
    print("🔗 拼接所有片段……")
    list_file = CLIPS / "list.txt"
    files = sorted(CLIPS.glob("clip*.mp4"))
    list_file.write_text("\n".join(f"file '{f.name}'" for f in files), encoding="utf-8")

    merged = OUT / "_merged.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(merged)
    ], check=True, cwd=str(CLIPS))

    # 烧录字幕
    if SRT_FILE.exists():
        print("📝 烧录中文字幕……")
        subbed = OUT / "_subbed.mp4"
        srt_path = ff_path(SRT_FILE)
        style = "FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,MarginV=240,Alignment=2"
        if FONT:
            font_name = Path(FONT).stem
            style = f"FontName={font_name},{style}"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(merged),
            "-vf", f"subtitles='{srt_path}':force_style='{style}'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(subbed)
        ], check=True)
        merged.unlink()
        merged = subbed

    # 加 BGM
    bgm = HERE / "bgm.mp3"
    final = OUT / OUTPUT_NAME
    if bgm.exists():
        print("🎵 混入 BGM……")
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(merged), "-i", str(bgm),
            "-filter_complex", "[1:a]volume=0.4,afade=t=in:st=0:d=0.5,afade=t=out:st=29:d=1[a]",
            "-map", "0:v", "-map", "[a]", "-shortest",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            str(final)
        ], check=True)
    else:
        print("⚠️  未找到 bgm.mp3 → 输出无配乐版本")
        shutil.copy(merged, final)

    # 清理
    if merged.exists() and merged != final:
        merged.unlink()
    return final

# ============ 主流程 ============
def main():
    print("═" * 50)
    print("  🦅 拉齐奥 vs 国米 抖音视频生成 Pipeline")
    print("═" * 50)
    print()

    check_tools()
    print()

    print("📥 第 1 步: 下载素材")
    print("-" * 50)
    download_assets()
    print()

    print("🎬 第 2 步: 渲染 8 个片段")
    print("-" * 50)
    CLIPS.mkdir(exist_ok=True)
    for f in CLIPS.glob("clip*.mp4"):
        f.unlink()
    for entry in TIMELINE:
        idx, dur, typ, src, start, title, sub, extra = entry
        if typ in ("yt", "mix"):
            make_yt_clip(idx, dur, src, start, title, sub, extra)
        else:
            make_card(idx, dur, title, sub, extra)
    print()

    print("🎞  第 3 步: 拼接 + 字幕 + 配乐")
    print("-" * 50)
    final = finalize()
    print()

    print("═" * 50)
    print(f"  ✅ 完成！文件: {final}")
    print(f"  📐 {WIDTH}x{HEIGHT} @ {FPS}fps · 30s")
    print("═" * 50)
    return final

if __name__ == "__main__":
    try:
        out = main()
        # Windows: 自动打开输出文件夹
        if sys.platform == "win32":
            os.startfile(str(out.parent))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(out.parent)])
        else:
            subprocess.run(["xdg-open", str(out.parent)], check=False)
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        sys.exit(1)
