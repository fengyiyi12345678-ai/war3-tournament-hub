# Agent 1 · 九宫格电商电影模板生成器

## 一句话
上传一张产品图，输出一张 3×3 图文混合九宫格（9 张 AI 参考图 + 9 段分镜文案）+ 结构化 `storyboard.json`。

## 文件清单

| 文件 | 用途 |
| --- | --- |
| `system-prompt.md` | 两段 system prompt（Section A 视觉解析、Section B 9 镜分镜） |
| `image-prompt-template.md` | Seedream i2i 的 9 格 prompt 模板 |
| `workflow.md` | Coze 工作流节点配置 + 拼图 Python 代码 |
| `output-schema.json` | storyboard.json 的 JSON Schema |

## 输入

```json
{
  "image_url": "https://.../product.png",
  "style_anchor": "高端电影感, 冷色调, Vogue 杂志风",
  "language": "zh"
}
```

## 输出

```json
{
  "grid_image_url": "https://.../grid_3x3.png",
  "storyboard": { /* 见 output-schema.json */ }
}
```
