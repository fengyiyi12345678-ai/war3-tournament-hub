#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap.py - 自动准备运行环境
1. 检查/安装 yt-dlp
2. 检查/下载 portable ffmpeg (Windows)
3. 调用 make_video.py 生成视频
"""
import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
TOOLS = HERE / "tools"
FFMPEG_DIR = TOOLS / "ffmpeg"

FFMPEG_URL_WIN = (
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
    "ffmpeg-master-latest-win64-gpl.zip"
)


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def add_to_path(p: Path):
    os.environ["PATH"] = str(p) + os.pathsep + os.environ.get("PATH", "")


def ensure_ffmpeg():
    """如果系统没 ffmpeg，下载 portable 版到 tools/ffmpeg/"""
    if have("ffmpeg"):
        print("[ffmpeg] system installation found")
        return

    # 检查是否已经下载过 portable（包含上次失败残留的 ffmpeg-master-* 目录）
    if TOOLS.exists():
        for candidate_dir in [FFMPEG_DIR] + list(TOOLS.glob("ffmpeg*")):
            if not candidate_dir.is_dir():
                continue
            bins = list(candidate_dir.glob("**/bin/ffmpeg.exe")) + list(
                candidate_dir.glob("**/bin/ffmpeg")
            )
            if bins:
                bin_dir = bins[0].parent
                add_to_path(bin_dir)
                print(f"[ffmpeg] portable found at: {bin_dir}")
                return

    if sys.platform != "win32":
        print("[ffmpeg] ERROR: ffmpeg not in PATH. Install via your package manager:")
        print("        macOS:  brew install ffmpeg")
        print("        Linux:  sudo apt install ffmpeg")
        sys.exit(1)

    # Windows: 下载 portable 版
    print(f"[ffmpeg] not found, downloading portable build (~100MB)...")
    print(f"        from: {FFMPEG_URL_WIN}")
    TOOLS.mkdir(exist_ok=True)
    zip_path = TOOLS / "ffmpeg.zip"

    # 清理旧的失败残留
    if FFMPEG_DIR.exists():
        shutil.rmtree(FFMPEG_DIR, ignore_errors=True)
    for stale in TOOLS.glob("ffmpeg-master-*"):
        if stale.is_dir():
            shutil.rmtree(stale, ignore_errors=True)
    if zip_path.exists():
        zip_path.unlink()

    try:
        # 带进度条下载
        def progress(blocks, bs, total):
            pct = min(100, blocks * bs * 100 // max(total, 1))
            bar = "#" * (pct // 2)
            sys.stdout.write(f"\r        [{bar:<50}] {pct}%")
            sys.stdout.flush()

        urllib.request.urlretrieve(FFMPEG_URL_WIN, zip_path, progress)
        print()
    except Exception as e:
        print(f"\n[ffmpeg] download failed: {e}")
        print("        Manual fix: download ffmpeg yourself and put ffmpeg.exe in PATH.")
        sys.exit(1)

    print("[ffmpeg] extracting...")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(TOOLS)
    zip_path.unlink()

    # 找到解压后的目录，重命名为 tools/ffmpeg
    extracted = [
        p for p in TOOLS.iterdir()
        if p.is_dir() and p.name.startswith("ffmpeg-")
    ]
    if not extracted:
        print("[ffmpeg] extraction failed: no ffmpeg-* directory found")
        sys.exit(1)
    extracted[0].rename(FFMPEG_DIR)

    bin_dir = FFMPEG_DIR / "bin"
    if not (bin_dir / "ffmpeg.exe").exists():
        print(f"[ffmpeg] expected ffmpeg.exe in {bin_dir} but not found")
        sys.exit(1)
    add_to_path(bin_dir)
    print(f"[ffmpeg] ready: {bin_dir / 'ffmpeg.exe'}")


def ensure_yt_dlp():
    """确保 yt-dlp 可用"""
    try:
        import yt_dlp  # noqa: F401
        print("[yt-dlp] already installed")
        return
    except ImportError:
        pass

    print("[yt-dlp] installing via pip...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "yt-dlp"]
        )
        print("[yt-dlp] installed")
    except subprocess.CalledProcessError as e:
        print(f"[yt-dlp] pip install failed: {e}")
        print("        Manual fix:  python -m pip install -U yt-dlp")
        sys.exit(1)


def run_pipeline():
    print()
    print("=" * 50)
    print("Starting video pipeline...")
    print("=" * 50)
    script = HERE / "make_video.py"
    if not script.exists():
        print(f"ERROR: make_video.py not found at {script}")
        sys.exit(1)
    # 用当前 env (含更新过的 PATH) 调用
    result = subprocess.run([sys.executable, str(script)], env=os.environ.copy())
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    print()
    print("[bootstrap] preparing environment...")
    ensure_yt_dlp()
    ensure_ffmpeg()
    run_pipeline()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[bootstrap] cancelled by user")
        sys.exit(130)
