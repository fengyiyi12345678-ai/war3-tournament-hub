# Coze（扣子）工作流配置教程

本文档分步教你在 [扣子 coze.cn](https://www.coze.cn/) 上把两个 Agent 搭建起来。Dify 同理，只是节点名称略不同（已在每步标注 Dify 对照）。

---

## Agent 1：九宫格电商电影模板生成器

### Step 0 · 新建工作流

- 「工作流」→「创建工作流」→ 名称：`产品九宫格电影模板`
- 描述：上传产品图，生成 3×3 电商分镜九宫格

### Step 1 · 配置开始节点

| 字段 | 类型 | 是否必填 | 备注 |
| --- | --- | --- | --- |
| `image_url` | String / File | 是 | 用户上传的产品图（建议白底） |
| `style_anchor` | String | 否（默认「高端电影感」） | 全局风格关键词 |
| `language` | String | 否（默认 `zh`） | 输出语言 |

### Step 2 · 节点 A：产品要素识别（视觉 LLM）

- 节点类型：**LLM** → 模型选 **Doubao-1.5-vision-pro**（Dify：`gpt-4o` 或 `qwen-vl-max`）
- 输入：`image_url` 作为 `image` 参数
- 系统提示词：粘贴 [`agents/agent-1-grid-template/system-prompt.md`](../agents/agent-1-grid-template/system-prompt.md) 中的 **「Section A · 视觉解析 system prompt」**
- 输出格式：**JSON 模式**，结构如下

```json
{
  "category": "string",
  "color": "string",
  "material": "string",
  "target_audience": "string",
  "style": "string",
  "key_visual": "string"
}
```

- 把这个输出保存为变量 `product_meta`

### Step 3 · 节点 B：分镜脚本生成（文本 LLM）

- 节点类型：**LLM** → 模型 **Doubao-1.5-pro-32k** 或 **Doubao-Seed-1.6**
- 输入变量：`product_meta`、`style_anchor`、`language`
- 系统提示词：粘贴 [`agents/agent-1-grid-template/system-prompt.md`](../agents/agent-1-grid-template/system-prompt.md) 中的 **「Section B · 9 镜分镜 system prompt」**
- 输出格式：**JSON 模式**，结构遵循 [`output-schema.json`](../agents/agent-1-grid-template/output-schema.json)
- 输出保存为 `storyboard`

### Step 4 · 节点 C：9 张参考图并行生成（图像生成 + 循环）

- 节点类型：**循环 / Loop** → 数组 = `storyboard.cells`
- 循环体内：
  1. **图像生成节点**（Coze 内置「图像生成」→ 选 Seedream 3.0；Dify：替换为 SD 节点）
  2. 入参：
     - `prompt`：`item.image_prompt`
     - `reference_image`：开始节点的 `image_url`
     - `mode`：`i2i`
     - `strength`：`0.7`
     - `aspect_ratio`：`1:1`（拼图需要等比）
     - `seed`：`-1`（让 9 张有差异）
  3. 输出 `item.image_url` 写回当前 cell

> 如果 Coze 版本不支持 i2i 的循环节点，用「批处理图像生成」插件，或拆 9 个并行节点（推荐前者）。

### Step 5 · 节点 D：3×3 拼接 + 角标

- 节点类型：**代码节点**（Python 3）。Coze 也有现成「图片拼接」插件可用。
- 代码逻辑：下载 9 张图，用 PIL 拼成 3×3，在每张子图左上角叠加 `shot_id + role` 文字标签
- 参考代码：见 [`agents/agent-1-grid-template/workflow.md`](../agents/agent-1-grid-template/workflow.md) 末尾「拼图代码片段」

### Step 6 · 结束节点

- 输出 2 个字段：
  - `grid_image_url`：Step 5 拼好的图
  - `storyboard`：Step 3 的 JSON（透传，给 Agent 2 用）

### Step 7 · 测试

- 试一张白底香水瓶图，检查：
  - [ ] 9 个 cell 的 `role` 是否对应固定的 9 个分工
  - [ ] 9 张参考图风格是否一致（看是否需要调大 `global_style_anchor` 权重）
  - [ ] 角标是否清晰可读

---

## Agent 2：Seedance 提示词智能体

### Step 0 · 新建工作流

- 名称：`Seedance 提示词生成器`

### Step 1 · 开始节点

| 字段 | 类型 | 备注 |
| --- | --- | --- |
| `storyboard` | Object（JSON） | 直接复用 Agent 1 的输出 |
| `default_duration` | Number | 默认 3 |
| `default_ratio` | String | 默认 `16:9` |
| `default_fps` | Number | 默认 24 |

### Step 2 · 节点 A：归一化（代码节点）

- 校验 `storyboard.cells.length === 9`
- 对每个 cell：
  - `duration_sec` clamp 到 `[2, 5]`
  - 缺省 `lens` → `50mm`
  - 缺省 `lighting` → `natural soft`

### Step 3 · 节点 B：Seedance Prompt 批量生成

- 节点类型：**LLM**（文本即可，无需视觉）
- 模型：Doubao-1.5-pro 或同档
- 系统提示词：粘贴 [`agents/agent-2-seedance-prompter/system-prompt.md`](../agents/agent-2-seedance-prompter/system-prompt.md)
- 输入：整个 `storyboard`（带 9 个 cell）+ Agent 1 的 `product_meta`
- 输出格式：**JSON 模式**

```json
{
  "video_pack": [
    {
      "shot_id": "01",
      "seedance_prompt": "...约 50–80 字...",
      "duration": 2,
      "ratio": "16:9",
      "fps": 24,
      "motion_strength": "medium",
      "negative_prompt": "low quality, jitter, watermark"
    }
  ]
}
```

### Step 4 · 结束节点

- 输出 `video_pack`（数组，9 项）
- 用户直接复制每条 `seedance_prompt` 到豆包 / 即梦 / 火山方舟 Seedance 工作台即可生成视频

---

## 串联模式（推荐）：父工作流

新建一个父工作流 `电商一键开拍`：

```
[开始：image_url]
  │
  ▼
[子工作流 · Agent 1] → grid_image_url, storyboard
  │
  ▼
[子工作流 · Agent 2] → video_pack
  │
  ▼
[结束节点 · 同时输出]
  - grid_image_url
  - storyboard
  - video_pack
```

这样用户上传一张图后只点一次按钮，就能拿到「九宫格预览图 + 9 段 Seedance Prompt」两件套。

---

## 常见踩坑

| 问题 | 原因 | 解决 |
| --- | --- | --- |
| 9 张图风格漂移 | LLM 在每格里换了风格词 | 强制 `global_style_anchor` 写在每个 `image_prompt` 开头 |
| 产品长得不像 | i2i strength 太低 | 提到 0.7–0.8 |
| JSON 解析失败 | 模型自由发挥 | 必开 JSON 模式 / 函数调用 |
| Seedance 拒绝 prompt | 含敏感词 | 在 Agent 2 system prompt 里加合规过滤约束 |
| 拼图字幕乱码 | PIL 没装中文字体 | 在代码节点加载 `NotoSansSC-Regular.otf` |
