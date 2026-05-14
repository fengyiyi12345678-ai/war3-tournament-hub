#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
youtube.py - 用 yt-dlp 按关键词搜索 + 下载视频。
搜索失败时返回 None，让上层退化成文字卡片。
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional


def search_first(query: str) -> Optional[str]:
    """对单个关键词执行 ytsearch1，返回第一个视频的 URL；失败返回 None。"""
    try:
        import yt_dlp
    except ImportError:
        print("[youtube] yt-dlp 未安装")
        return None

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "skip_download": True,
        "socket_timeout": 20,
        "default_search": "ytsearch",
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)
        entries = (result or {}).get("entries") or []
        if not entries:
            return None
        first = entries[0]
        return first.get("url") or first.get("webpage_url") or \
               f"https://www.youtube.com/watch?v={first.get('id')}"
    except Exception as e:
        print(f"[youtube] 搜索失败 [{query}]: {e}")
        return None


def resolve_sources(yt_search: dict) -> dict:
    """
    输入: {"hero_a": "Real Madrid celebration goals", ...}
    输出: {"hero_a": "https://www.youtube.com/watch?v=xxx", ...}
    搜不到的 key 会被跳过（上层渲染时会退化成卡片）
    """
    sources = {}
    for key, query in yt_search.items():
        print(f"[youtube] 搜索 [{key}] {query}")
        url = search_first(query)
        if url:
            sources[key] = url
            print(f"           → {url}")
        else:
            print(f"           → 未找到，会退化成文字卡片")
    return sources


def download(url: str, target: Path) -> bool:
    """下载视频到指定路径。"""
    try:
        import yt_dlp
    except ImportError:
        return False

    if target.exists() and target.stat().st_size > 0:
        print(f"[youtube] ✅ 已存在: {target.name}")
        return True

    target.parent.mkdir(parents=True, exist_ok=True)
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
        return target.exists() and target.stat().st_size > 0
    except Exception as e:
        print(f"[youtube] 下载失败: {e}")
        return False


def download_all(sources: dict, assets_dir: Path) -> dict:
    """批量下载 sources 里的所有 URL，返回成功下载的子集。"""
    ok = {}
    for key, url in sources.items():
        target = assets_dir / f"{key}.mp4"
        if download(url, target):
            ok[key] = url
    return ok


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "Real Madrid celebration goal"
    url = search_first(query)
    print(f"\nResult: {url}")
