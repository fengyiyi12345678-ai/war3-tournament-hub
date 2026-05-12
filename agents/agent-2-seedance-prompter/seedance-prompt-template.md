# Seedance Prompt 单格模板

## 通用拼装公式（人工兜底）

```
{{product_anchor}}，{{scene_from_image_prompt}}，{{action_with_motion_verb}}，{{camera_phrase}}，{{global_style_anchor}}，4K，{{fps}}fps。
```

## 变量映射

| 模板变量 | 来源 | 处理 |
| --- | --- | --- |
| `product_anchor` | storyboard.product_anchor | 整段照抄 |
| `scene_from_image_prompt` | cell.image_prompt | 抽取「场景 + 光照 + 构图」相关短句，10–20 字 |
| `action_with_motion_verb` | cell.action | 在动作前/后加「缓缓 / 渐渐 / 流动 / 旋转 / 推进 / 浮动」等运动动词 |
| `camera_phrase` | cell.camera + cell.lens + cell.composition | 合并成 8–15 字（如「50mm 中心特写慢推」） |
| `global_style_anchor` | storyboard.global_style_anchor | 整段照抄 |
| `fps` | 见 system prompt 的参数推断规则 | 24 或 30 |

## 9 个 role 对应的「Seedance 风味」加成词（可选）

| role | 推荐加成词 |
| --- | --- |
| opening_hook | 神秘、悬浮、雾气、缓缓浮现 |
| hero_visual | 旋转、对称、纯净背景、聚光 |
| scene_context | 真实场景、自然光、生活气 |
| macro_detail | 微距、纹理、质感、光影流动 |
| core_benefit | 静帧、字幕动效空间、聚焦 |
| usage_action | 手部特写、动作连贯、自然流畅 |
| emotional_reaction | 表情特写、眼神光、暖色情绪 |
| before_after | 分屏、过渡、对比反差 |
| call_to_action | 拉远、留白、品牌位、收尾感 |

## 一段完整示例

输入 cell：
```json
{
  "shot_id": "04",
  "role": "macro_detail",
  "duration_sec": 2,
  "camera": "macro push 微距推进",
  "lens": "85mm macro",
  "lighting": "hard side light 硬侧光",
  "composition": "extreme close-up 极特写",
  "mood": "delicate 细腻",
  "action": "镜头逼近瓶身金色花纹纹理",
  "image_prompt": "电影感, 冷色调, 柔光, 高对比, 杂志风。一瓶琥珀金色玻璃香水瓶，瓶身浮雕金色花纹，黑色丝绒背景，硬侧光勾勒花纹立体感，85mm 微距极特写。",
  "subtitle": "工艺之美"
}
```

对应 Seedance prompt：
```
一瓶琥珀金色玻璃香水瓶，瓶身浮雕金色花纹，黑色丝绒背景上，金色花纹在硬侧光下纹理逐渐清晰，镜头以 85mm 微距缓缓推进至瓶身花纹处，电影感、冷色调、柔光、高对比、杂志风、4K、30fps。
```

参数：`duration=2, ratio=16:9, fps=30, motion_strength=medium`
