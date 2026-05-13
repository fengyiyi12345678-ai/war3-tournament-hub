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

_FFMPEG_PATH = (
    "github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
    "ffmpeg-master-latest-win64-gpl.zip"
)
# 多个 GitHub 加速镜像，按顺序尝试
FFMPEG_URLS_WIN = [
    f"https://{_FFMPEG_PATH}",
    f"https://ghproxy.com/https://{_FFMPEG_PATH}",
    f"https://gh-proxy.com/https://{_FFMPEG_PATH}",
    f"https://mirror.ghproxy.com/https://{_FFMPEG_PATH}",
]


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

    def progress(blocks, bs, total):
        pct = min(100, blocks * bs * 100 // max(total, 1))
        bar = "#" * (pct // 2)
        sys.stdout.write(f"\r        [{bar:<50}] {pct}%")
        sys.stdout.flush()

    downloaded = False
    for url in FFMPEG_URLS_WIN:
        host = url.split("/")[2]
        print(f"[ffmpeg] trying mirror: {host}")
        try:
            urllib.request.urlretrieve(url, zip_path, progress)
            print()
            downloaded = True
            break
        except Exception as e:
            print(f"\n[ffmpeg] {host} failed: {e}")
            if zip_path.exists():
                zip_path.unlink()
            continue

    if not downloaded:
        print("[ffmpeg] ERROR: all mirrors failed.")
        print("        Manual fix: download ffmpeg from one of:")
        for url in FFMPEG_URLS_WIN:
            print(f"          {url}")
        print(f"        Then extract so that ffmpeg.exe lives at:")
        print(f"          {FFMPEG_DIR}/bin/ffmpeg.exe")
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
    """确保 yt-dlp 可用（自动 fallback 多个 pip 镜像）"""
    try:
        import yt_dlp  # noqa: F401
        print("[yt-dlp] already installed")
        return
    except ImportError:
        pass

    # 多个镜像源，按顺序尝试
    mirrors = [
        ("default",  None),  # pypi.org
        ("Tsinghua", "https://pypi.tuna.tsinghua.edu.cn/simple"),
        ("Aliyun",   "https://mirrors.aliyun.com/pypi/simple/"),
        ("Huawei",   "https://mirrors.huaweicloud.com/repository/pypi/simple/"),
        ("USTC",     "https://pypi.mirrors.ustc.edu.cn/simple/"),
    ]

    for name, url in mirrors:
        print(f"[yt-dlp] trying pip source: {name}")
        cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "yt-dlp"]
        if url:
            # 国内镜像还要把镜像域名加入信任主机
            host = url.split("/")[2]
            cmd += ["-i", url, "--trusted-host", host]
        try:
            subprocess.check_call(cmd)
            print(f"[yt-dlp] installed via {name}")
            return
        except subprocess.CalledProcessError:
            print(f"[yt-dlp] {name} failed, trying next...")
            continue

    print("[yt-dlp] ERROR: all pip mirrors failed.")
    print("        Try manually in cmd:")
    print("        py -3 -m pip install -U yt-dlp -i https://pypi.tuna.tsinghua.edu.cn/simple")
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
