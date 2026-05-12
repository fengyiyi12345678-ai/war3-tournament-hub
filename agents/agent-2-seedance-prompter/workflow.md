# Agent 2 工作流节点配置

## 节点表

| # | 节点 | 类型 | 输入 | 输出 |
| --- | --- | --- | --- | --- |
| Start | 开始 | 开始节点 | storyboard, default_duration, default_ratio, default_fps | — |
| A | 校验归一化 | 代码节点（Python） | storyboard | storyboard_norm |
| B | Seedance Prompt 生成 | LLM（文本，JSON 模式） | storyboard_norm | video_pack |
| End | 结束 | 结束节点 | video_pack | — |

## 节点 A · 校验归一化代码

```python
# Coze 代码节点（Python 3）
def main(args):
    sb = args["storyboard"]
    default_duration = args.get("default_duration", 3)

    assert len(sb["cells"]) == 9, "storyboard 必须包含 9 个 cell"

    role_order = [
        "opening_hook", "hero_visual", "scene_context",
        "macro_detail", "core_benefit", "usage_action",
        "emotional_reaction", "before_after", "call_to_action",
    ]
    cells_by_role = {c["role"]: c for c in sb["cells"]}
    cells = []
    for idx, role in enumerate(role_order, start=1):
        c = cells_by_role.get(role)
        if c is None:
            raise ValueError(f"缺少角色 {role}")
        # clamp 时长
        d = c.get("duration_sec", default_duration)
        c["duration_sec"] = max(2, min(5, int(d)))
        # 默认镜头参数
        c.setdefault("lens", "50mm")
        c.setdefault("lighting", "natural soft")
        c.setdefault("composition", "center")
        c["shot_id"] = f"{idx:02d}"
        c["position"] = [(idx - 1) // 3 + 1, (idx - 1) % 3 + 1]
        cells.append(c)

    sb["cells"] = cells
    return {"storyboard_norm": sb}
```

## 节点 B · LLM 配置

- **模型**：Doubao-1.5-pro 或 Doubao-Seed-1.6（文本）
- **温度**：0.4（求稳，不需要太发散）
- **响应格式**：JSON
- **System Prompt**：粘贴 [`system-prompt.md`](system-prompt.md)
- **User Prompt 模板**：

```
请把下面的 storyboard 转换为 9 段 Seedance 视频提示词包。

storyboard:
{{node_A.output.storyboard_norm}}

默认参数：
- duration: {{Start.default_duration}}
- ratio: {{Start.default_ratio}}
- fps: {{Start.default_fps}}

只输出 JSON，不要任何解释文字。
```

## 节点 End

- 输出字段：`video_pack`（数组，长度 9）
- 用户拿到后逐条复制到豆包 / 即梦 / 火山方舟 Seedance 控制台跑视频，或对接 Seedance API。

## 串联到父工作流

如果你用「父工作流」串联 Agent 1 → Agent 2：

```
父工作流.Start.image_url
  → 调用 Agent 1
    输出 grid_image_url, storyboard
  → 调用 Agent 2
    输入 storyboard
    输出 video_pack
父工作流.End:
  - grid_image_url
  - storyboard
  - video_pack
```

在 Coze 中：「工作流 → 添加节点 → 子工作流」依次选择 Agent 1、Agent 2 即可。
