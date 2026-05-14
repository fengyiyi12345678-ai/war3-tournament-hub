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
# 国内常卡 github.com 原始链接，先试加速镜像，最后才回退到原站
FFMPEG_URLS_WIN = [
    f"https://ghfast.top/https://{_FFMPEG_PATH}",
    f"https://ghproxy.com/https://{_FFMPEG_PATH}",
    f"https://mirror.ghproxy.com/https://{_FFMPEG_PATH}",
    f"https://gh-proxy.com/https://{_FFMPEG_PATH}",
    f"https://hub.gitmirror.com/https://{_FFMPEG_PATH}",
    f"https://{_FFMPEG_PATH}",
]

# 单次连接 / 单块读取超时（秒）。超时立即跳下一个镜像。
DOWNLOAD_TIMEOUT = 15


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def add_to_path(p: Path):
    os.environ["PATH"] = str(p) + os.pathsep + os.environ.get("PATH", "")


def disable_proxy():
    """清掉所有代理设置，避免连一个已经挂掉的代理。"""
    proxy_vars = [
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy",
    ]
    cleared = []
    for k in proxy_vars:
        if k in os.environ:
            cleared.append(f"{k}={os.environ[k]}")
            del os.environ[k]
    if cleared:
        print(f"[net] cleared dead proxy env: {', '.join(cleared)}")
    # urllib 在 Windows 上还会读注册表里的代理设置，这里强制无代理
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    urllib.request.install_opener(opener)
    # 让子进程也读不到代理
    os.environ["no_proxy"] = "*"
    os.environ["NO_PROXY"] = "*"


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

    def stream_download(url, dest):
        """带超时的流式下载——一旦 15 秒内没拿到数据就抛错，避免卡死。"""
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            got = 0
            last_pct = -1
            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(64 * 1024)  # 64KB
                    if not chunk:
                        break
                    f.write(chunk)
                    got += len(chunk)
                    if total > 0:
                        pct = min(100, got * 100 // total)
                        if pct != last_pct:
                            bar = "#" * (pct // 2)
                            mb = got / 1024 / 1024
                            sys.stdout.write(f"\r        [{bar:<50}] {pct:3d}% ({mb:.1f}MB)")
                            sys.stdout.flush()
                            last_pct = pct

    downloaded = False
    for url in FFMPEG_URLS_WIN:
        host = url.split("/")[2]
        print(f"[ffmpeg] trying mirror: {host} (timeout {DOWNLOAD_TIMEOUT}s)")
        try:
            stream_download(url, zip_path)
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
        # --proxy "" 强制 pip 不走任何代理，再加上短 timeout 跳过卡死的请求
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--upgrade", "yt-dlp",
            "--proxy", "",
            "--timeout", "20",
            "--retries", "1",
        ]
        if url:
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
    disable_proxy()
    ensure_yt_dlp()
    ensure_ffmpeg()
    run_pipeline()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[bootstrap] cancelled by user")
        sys.exit(130)
