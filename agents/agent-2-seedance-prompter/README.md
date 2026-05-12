# Agent 2 · Seedance 提示词智能体

## 一句话
吃下 Agent 1 的 `storyboard.json`，吐出 9 段标准 Seedance 视频 prompt + 推荐参数。

## 输入

```json
{
  "storyboard": { /* Agent 1 的完整输出 */ },
  "default_duration": 3,
  "default_ratio": "16:9",
  "default_fps": 24
}
```

## 输出

```json
{
  "video_pack": [
    {
      "shot_id": "01",
      "seedance_prompt": "...50-80 字 Seedance 视频 prompt...",
      "duration": 2,
      "ratio": "16:9",
      "fps": 24,
      "motion_strength": "medium",
      "negative_prompt": "低质量, 模糊, 抖动, 水印"
    }
    // ... 共 9 条
  ]
}
```

## 文件清单

| 文件 | 用途 |
| --- | --- |
| `system-prompt.md` | LLM 节点系统提示词 |
| `seedance-prompt-template.md` | 单格 Seedance prompt 模板与变量映射 |
| `workflow.md` | 工作流节点配置 |
