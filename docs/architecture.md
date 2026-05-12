# 架构与数据流

## 一、设计原则

1. **单输入 / 双输出**：只要一张产品图 → 拿到「图文九宫格 + Seedance prompt 包」
2. **可单独使用，也可串联**：Agent 1、Agent 2 是两个独立工作流，可以独立运行，也可以串成一个父工作流（推荐）
3. **结构化中间件**：两 Agent 之间用 `storyboard.json` 这个 schema 通信，平台无关
4. **9 格分工固定**：每一格的「角色」固定（开篇 / 主视觉 / 细节微距 / …），保证产出的稳定性

## 二、九宫格的「九格分工」

之所以是 3×3 而不是任意数量，是因为电商短片有一套**经典 9 镜头节奏**，我把它固化进 prompt 里：

| 位置 | 镜头编号 | 角色 | 默认时长 | 默认运镜 |
| --- | --- | --- | --- | --- |
| (1,1) 左上 | 01 开场 | 悬念吸睛 · 产品入场 | 2s | 推镜 / push-in |
| (1,2) 中上 | 02 主视觉 | 产品全貌 · 品牌定调 | 3s | 环绕 / orbit |
| (1,3) 右上 | 03 场景植入 | 使用场景氛围 | 3s | 跟随 / follow |
| (2,1) 左中 | 04 细节微距 | 材质 / 工艺 / 卖点 1 | 2s | 微距推进 / macro push |
| (2,2) 正中 | 05 核心卖点 | 卖点 2 + 利益点字幕位 | 3s | 静帧 + 字幕动效 |
| (2,3) 右中 | 06 动作演示 | 产品被使用的瞬间 | 3s | 手持跟拍 / handheld |
| (3,1) 左下 | 07 情绪共鸣 | 用户表情 / 反应 | 2s | 半身中景 / medium |
| (3,2) 中下 | 08 对比反差 | Before/After 或对比镜 | 2s | 切换 / cut |
| (3,3) 右下 | 09 收尾召唤 | Logo + 行动召唤 | 3s | 拉镜 / pull-out |

总时长 ≈ 23 秒，正好对应抖音 / 视频号黄金 25s 区间。

## 三、Agent 1 内部节点图

```
[开始节点 · image_url 输入]
        │
        ▼
[节点 A · 豆包视觉]
   输入：image_url
   输出：product_meta {category, color, material,
                       target_audience, style, key_visual}
        │
        ▼
[节点 B · 豆包文本（结构化输出）]
   输入：product_meta + 9 镜头分工模板
   输出：storyboard.json （9 个 cell，每 cell 含
         shot_id, role, duration, camera, lighting,
         composition, mood, action, image_prompt, subtitle）
        │
        ├─► 并行循环 9 次 ◄─┐
        ▼                  │
[节点 C · Seedream 3.0 i2i]  │（按 cell.image_prompt + 原图 i2i）
   输入：reference_image, prompt, strength=0.7
   输出：cell_image_url       │
        │                  │
        └──────┬───────────┘
               ▼
[节点 D · 图像拼接（3×3 + 角标）]
   输入：9 张 cell_image_url + storyboard.json
   输出：grid.png (1080×1080 或 1024×1024)
        │
        ▼
[结束节点 · 同时输出]
   - grid.png   （图文九宫格）
   - storyboard.json （结构化分镜数据，给 Agent 2 用）
```

## 四、Agent 2 内部节点图

```
[开始节点 · storyboard.json 输入]
        │
        ▼
[节点 A · 校验与归一化]
   - 字段缺省补全
   - 时长 clamp 到 [2s, 5s]
   - 分辨率默认 1080p / 24fps
        │
        ▼
[节点 B · 豆包文本（按 Seedance 提示词规范逐格扩写）]
   输入：每个 cell + 全局风格锚 + 产品锚
   输出：9 段 seedance_prompt（中文，约 50–80 汉字）
         + 推荐参数：duration, ratio, fps, motion_strength
        │
        ▼
[结束节点 · seedance_pack.json]
```

## 五、数据契约 storyboard.json

详见 [`agents/agent-1-grid-template/output-schema.json`](../agents/agent-1-grid-template/output-schema.json)。
核心字段（每个 cell）：

```json
{
  "shot_id": "01",
  "role": "opening_hook",
  "position": [1, 1],
  "duration_sec": 2,
  "camera": "push-in slow",
  "lens": "50mm",
  "lighting": "soft rim light",
  "composition": "center close-up",
  "mood": "mysterious",
  "action": "fragrance bottle emerges from mist",
  "image_prompt": "...用于 Seedream 的 prompt...",
  "subtitle": "为你而来"
}
```

## 六、关键工程细节

1. **i2i 参考强度**：Seedream 的 `strength` 建议 0.65–0.75，太低会丢失产品识别度，太高会缺少创意
2. **风格锚定**：在 Agent 1 节点 B 的 system prompt 里，强制要求 9 格共享同一个 `global_style_anchor`（如「电影感冷色调 / 高端杂志风 / 赛博朋克」），避免 9 张图风格漂移
3. **产品锚定**：每个 cell 的 `image_prompt` 都必须以 `{product_meta.category} {product_meta.color} {product_meta.key_visual}` 开头，保证产品一致性
4. **失败兜底**：图像节点失败时，用占位灰图 + 文案补位，不阻断整体流程
5. **Token 预算**：分镜 JSON 输出建议用「JSON 模式」或函数调用，避免模型自由发挥导致解析失败
