#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm.py - 三套文案生成方案统一接口

provider="claude"   → Anthropic Claude API（ANTHROPIC_API_KEY）
provider="deepseek" → DeepSeek API（DEEPSEEK_API_KEY）
provider="template" → 本地 JSON 模板填空，零依赖
"""
from __future__ import annotations
import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Optional

from prompts import SCRIPT_PROMPT, SYSTEM_PROMPT

TEMPLATES_DIR = Path(__file__).parent / "templates"


# ============================================================
# 1. Claude (Anthropic) provider
# ============================================================
def call_claude(user_prompt: str, api_key: str) -> str:
    """直连 Anthropic Messages API（不依赖 SDK，纯 urllib）。"""
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        data=json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": user_prompt}],
        }).encode("utf-8"),
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["content"][0]["text"]


# ============================================================
# 2. DeepSeek provider（OpenAI 兼容协议）
# ============================================================
def call_deepseek(user_prompt: str, api_key: str) -> str:
    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.8,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"},
        }).encode("utf-8"),
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


# ============================================================
# 3. Local template provider（零依赖兜底）
# ============================================================
def call_template(team_a: str, team_b: str, context: str = "") -> str:
    """从 templates/*.json 中挑一个最匹配的模板，机械填空。"""
    ctx_lower = context.lower()
    if any(k in ctx_lower for k in ["final", "决赛", "杯"]):
        tpl_name = "cup_final.json"
    elif any(k in ctx_lower for k in ["derby", "德比", "国家"]):
        tpl_name = "derby.json"
    else:
        tpl_name = "default.json"

    tpl_path = TEMPLATES_DIR / tpl_name
    tpl = json.loads(tpl_path.read_text(encoding="utf-8"))

    # 简单的 {team_a} / {team_b} / {context} 占位符替换
    def fill(obj):
        if isinstance(obj, str):
            return (obj.replace("{team_a}", team_a)
                       .replace("{team_b}", team_b)
                       .replace("{context}", context or "焦点对阵"))
        if isinstance(obj, list):
            return [fill(x) for x in obj]
        if isinstance(obj, dict):
            return {k: fill(v) for k, v in obj.items()}
        return obj

    return json.dumps(fill(tpl), ensure_ascii=False)


# ============================================================
# 统一入口
# ============================================================
def generate_script(team_a: str, team_b: str, context: str = "",
                    provider: str = "auto") -> dict:
    """
    返回一个 dict（已 parse 好 JSON），schema 见 prompts.SCRIPT_PROMPT。

    provider 自动选择规则：
      1. 显式指定 → 用指定的
      2. auto + 有 ANTHROPIC_API_KEY → claude
      3. auto + 有 DEEPSEEK_API_KEY  → deepseek
      4. 否则 → template
    """
    if provider == "auto":
        if os.getenv("ANTHROPIC_API_KEY"):
            provider = "claude"
        elif os.getenv("DEEPSEEK_API_KEY"):
            provider = "deepseek"
        else:
            provider = "template"

    print(f"[llm] using provider: {provider}")

    if provider == "claude":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        prompt = SCRIPT_PROMPT.format(team_a=team_a, team_b=team_b, context=context or "焦点对阵")
        raw = call_claude(prompt, key)
    elif provider == "deepseek":
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("DEEPSEEK_API_KEY not set")
        prompt = SCRIPT_PROMPT.format(team_a=team_a, team_b=team_b, context=context or "焦点对阵")
        raw = call_deepseek(prompt, key)
    elif provider == "template":
        raw = call_template(team_a, team_b, context)
    else:
        raise ValueError(f"unknown provider: {provider}")

    return _parse_json(raw)


def _parse_json(text: str) -> dict:
    """容错：LLM 有时会把 JSON 包在 ```json ... ``` 里。"""
    text = text.strip()
    # 去掉 markdown 代码块
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    return json.loads(text)


if __name__ == "__main__":
    # 简单自测
    import sys
    team_a = sys.argv[1] if len(sys.argv) > 1 else "拉齐奥"
    team_b = sys.argv[2] if len(sys.argv) > 2 else "国米"
    ctx = sys.argv[3] if len(sys.argv) > 3 else "意大利杯决赛"
    out = generate_script(team_a, team_b, ctx)
    print(json.dumps(out, ensure_ascii=False, indent=2))
