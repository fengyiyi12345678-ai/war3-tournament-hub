#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py - 输入一对球队 → 自动产出整支 30 秒视频

用法:
  # 自动选 provider（有哪个 key 用哪个，都没有就用模板）
  python generator/generate.py "皇马" "巴萨" "西甲国家德比"

  # 显式指定
  python generator/generate.py "皇马" "巴萨" "西甲" --provider claude
  python generator/generate.py "皇马" "巴萨" --provider template

环境变量:
  ANTHROPIC_API_KEY  → 用 Claude
  DEEPSEEK_API_KEY   → 用 DeepSeek
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# 让本目录可导入
HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from llm import generate_script
from youtube import resolve_sources

# 项目布局
ROOT = HERE.parent
PIPELINE_DIR = ROOT / "video-pipeline"
ASSETS_DIR = PIPELINE_DIR / "assets"
CONFIG_PATH = PIPELINE_DIR / "config.json"
SRT_PATH = PIPELINE_DIR / "subtitles.srt"


def write_srt(subtitles: list) -> None:
    """把 [{start, end, text}] 转成 SRT 文件。"""
    lines = []
    for i, s in enumerate(subtitles, 1):
        lines.append(str(i))
        lines.append(f"{_t(s['start'])} --> {_t(s['end'])}")
        lines.append(s["text"])
        lines.append("")
    SRT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[srt] wrote {SRT_PATH} ({len(subtitles)} cues)")


def _t(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def write_config(script: dict, yt_urls: dict) -> Path:
    """把 LLM 产出的 script + 解析后的 yt_urls 合成 make_video.py 期望的 config.json。"""
    meta = script["meta"]
    config = {
        "meta": meta,
        "video": {
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "output": meta.get("output_filename", "match_30s.mp4"),
        },
        "yt_sources": yt_urls,
        "timeline": script["timeline"],
    }
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[config] wrote {CONFIG_PATH}")
    return CONFIG_PATH


def run_pipeline(config_path: Path) -> Path:
    """调用现有的 make_video.py 渲染视频。"""
    print("\n" + "=" * 60)
    print("Starting video render pipeline...")
    print("=" * 60)
    cmd = [sys.executable, str(PIPELINE_DIR / "make_video.py"), str(config_path)]
    result = subprocess.run(cmd, cwd=str(PIPELINE_DIR))
    if result.returncode != 0:
        raise RuntimeError(f"make_video.py exited with {result.returncode}")
    out_dir = PIPELINE_DIR / "out"
    # 找最新输出文件
    mp4s = sorted(out_dir.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    return mp4s[0] if mp4s else (out_dir / "video.mp4")


def main():
    ap = argparse.ArgumentParser(description="自动生成足球短视频")
    ap.add_argument("team_a", help="主队")
    ap.add_argument("team_b", help="客队")
    ap.add_argument("context", nargs="?", default="", help="背景信息 (选填)")
    ap.add_argument("--provider", default="auto",
                    choices=["auto", "claude", "deepseek", "template"],
                    help="文案生成方式")
    ap.add_argument("--skip-render", action="store_true",
                    help="只生成配置不渲染（用于调试）")
    args = ap.parse_args()

    print("=" * 60)
    print(f"🎬 {args.team_a}  VS  {args.team_b}")
    if args.context:
        print(f"   背景: {args.context}")
    print("=" * 60)
    print()

    # 1. 文案
    print("📝 Step 1/3: generating script...")
    script = generate_script(args.team_a, args.team_b, args.context, provider=args.provider)
    print(f"[meta] 标题: {script['meta']['title']}")
    print(f"[meta] 文件名: {script['meta'].get('output_filename', 'match_30s.mp4')}")

    # 2. YouTube 搜索素材
    print("\n🔍 Step 2/3: searching YouTube for clips...")
    yt_urls = resolve_sources(script["yt_search"])

    # 3. 写 config + SRT
    write_srt(script["subtitles"])
    config_path = write_config(script, yt_urls)

    if args.skip_render:
        print("\n[done] config + srt written. Run make_video.py manually to render.")
        return

    # 4. 渲染
    print("\n🎞  Step 3/3: rendering video...")
    out_path = run_pipeline(config_path)

    print()
    print("=" * 60)
    print(f"✅ 全部完成！")
    print(f"📁 视频: {out_path}")
    print(f"📋 抖音文案 (复制粘贴):")
    print("-" * 60)
    print(script["meta"]["caption"])
    print("-" * 60)
    print(f"🏷  标签: {' '.join(script['meta']['hashtags'])}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[interrupted]")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        sys.exit(1)
