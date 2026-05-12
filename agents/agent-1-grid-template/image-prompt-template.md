# 九格 Seedream i2i 提示词模板

> 由 Agent 1 Section B 自动生成 9 个 `image_prompt`，每个都会塞进 Seedream / 即梦图像生成节点。本文件提供「**人工 fallback 模板**」——当 LLM 输出不稳定时，可以用这套模板做兜底拼装。

## 通用模板（变量用 `{{}}` 标记）

```
{{global_style_anchor}}。{{product_anchor}}，{{scene}}，{{action}}，{{camera}}，{{lens}}，{{lighting}}，{{composition}}，{{mood}}。
```

## 9 格场景词推荐表

| shot_id | role | scene 推荐 | action 推荐 | camera | lighting |
| --- | --- | --- | --- | --- | --- |
| 01 | opening_hook | 深色雾气背景 | 产品从雾气中浮现 | push-in 推镜 | soft rim light 柔边光 |
| 02 | hero_visual | 极简灰色无缝背景 | 产品 360° 缓慢自转 | orbit 环绕 | studio softbox 双柔光箱 |
| 03 | scene_context | 真实使用场景（如梳妆台/咖啡桌/办公桌） | 产品自然摆放在场景中 | follow 跟随 | natural window light 自然窗光 |
| 04 | macro_detail | 黑色丝绒背景 | 镜头逼近材质纹理 | macro push 微距推进 | hard side light 硬侧光 |
| 05 | core_benefit | 大字幕版位灰底 | 产品居中静帧，左侧留字幕位 | locked-off 静帧 | flat soft light 平柔光 |
| 06 | usage_action | 真实使用环境（厨房/浴室/户外） | 一双手 / 人物正在使用产品 | handheld follow 手持跟拍 | natural daylight 自然日光 |
| 07 | emotional_reaction | 暖光室内特写 | 用户使用后表情愉悦 / 惊喜 | medium 半身中景 | warm key light 暖主光 |
| 08 | before_after | 分屏 / 上下对比构图 | 左前 vs 右后 | split-screen cut 分屏切 | dual lighting 双调光 |
| 09 | call_to_action | 黑色极简背景 + Logo 位 | 镜头缓缓拉远，留出 logo 区 | pull-out 拉镜 | spotlight 聚光 |

## 强烈建议保留的负向提示词（即梦/Seedream）

```
低质量, 模糊, 多余手指, 畸形, 水印, logo 错乱, 文字错位, 失真, 噪点, 过曝, 欠曝
```

## 参数

- `mode`: `i2i`
- `reference_image`: 用户上传的产品图
- `strength` / `denoise`: **0.7**（关键，决定产品识别度 vs 创意度的平衡）
- `aspect_ratio`: `1:1`（用于 3×3 拼图）
- `seed`: 9 张图建议传不同 seed，避免重复构图
