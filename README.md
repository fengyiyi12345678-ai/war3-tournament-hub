# 产品九宫格 × Seedance 智能体套件

一套**零代码**的 Coze（扣子）/ Dify 智能体配置方案：

- 📸 **Agent 1 · 九宫格电商电影模板生成器**：上传一张产品图 → 输出一张 3×3 图文混合九宫格分镜板（9 张 AI 参考图 + 9 段分镜文案）
- 🎬 **Agent 2 · Seedance 提示词智能体**：把 Agent 1 的九宫格作为输入 → 输出 9 段标准 Seedance 视频提示词（直接粘进豆包 / 即梦 / 火山方舟跑视频）

> 设计目标：**电商商家上传一张白底产品图，10 分钟内拿到一支完整的「9 镜头电商短片」拍摄脚本和 9 段 Seedance prompt**，不写一行代码。

---

## 整体数据流

```
[用户上传产品图]
        │
        ▼
┌──────────────────────────────────────────┐
│  Agent 1  九宫格电商电影模板生成器        │
│  ┌────────────────────────────────────┐  │
│  │ 1. 豆包视觉  → 产品要素提取         │  │
│  │ 2. 豆包文本  → 9 镜分镜 JSON       │  │
│  │ 3. Seedream → 9 张参考图（i2i）   │  │
│  │ 4. 图像合成节点 → 3×3 拼图 + 角标  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
        │
        ▼  storyboard.json + grid.png
┌──────────────────────────────────────────┐
│  Agent 2  Seedance 提示词智能体           │
│  ┌────────────────────────────────────┐  │
│  │ 1. 解析 storyboard.json            │  │
│  │ 2. 按 Seedance Prompt 规范逐格生成  │  │
│  │ 3. 校验时长/运镜/分辨率 token       │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
        │
        ▼
[9 段 Seedance Prompt + 推荐参数]
```

---

## 推荐模型组合（国内可用，与 Seedance 同生态）

| 环节 | 模型 | 平台 |
| --- | --- | --- |
| 产品图理解 | **Doubao-1.5-vision-pro** | Coze 内置 |
| 分镜文案生成 | **Doubao-1.5-pro-32k** 或 **Doubao-Seed-1.6** | Coze 内置 |
| 9 格参考图生成 | **Seedream 3.0**（即梦图像，i2i 模式，参考强度 0.6–0.8） | Coze 插件 |
| 拼图合成 | Coze 自带「图像拼接」插件（或 Python 代码节点） | Coze 内置 |
| 视频提示词输出 | 文本模型 + 结构化输出 | Coze 内置 |
| 最终视频生成 | **Seedance 1.0 Pro / Lite**（由用户自行粘贴使用） | 豆包 / 火山方舟 |

> 也兼容 Dify、FastGPT 等平台，只需把对应节点替换为同类模型即可。

---

## 仓库结构

```
.
├── README.md                              # 本文档
├── docs/
│   ├── architecture.md                    # 架构与数据流详解
│   ├── coze-setup.md                      # Coze 工作流配置分步教程
│   └── seedance-prompt-guide.md           # Seedance 提示词撰写规范
├── agents/
│   ├── agent-1-grid-template/
│   │   ├── README.md                      # Agent 1 使用说明
│   │   ├── system-prompt.md               # 主系统提示词
│   │   ├── image-prompt-template.md       # 9 格图像生成提示词模板
│   │   ├── workflow.md                    # Coze 工作流节点配置
│   │   └── output-schema.json             # storyboard.json 输出 Schema
│   └── agent-2-seedance-prompter/
│       ├── README.md                      # Agent 2 使用说明
│       ├── system-prompt.md               # 主系统提示词
│       ├── seedance-prompt-template.md    # Seedance Prompt 单格模板
│       └── workflow.md                    # Coze 工作流节点配置
└── examples/
    ├── example-input.md                   # 示例输入（一款香水）
    └── example-output.json                # 完整示例输出
```

---

## 快速开始

1. 打开 [Coze 扣子](https://www.coze.cn/) 或 Dify
2. 新建工作流 → 按 [`docs/coze-setup.md`](docs/coze-setup.md) 中的步骤搭建 Agent 1
3. 复制 [`agents/agent-1-grid-template/system-prompt.md`](agents/agent-1-grid-template/system-prompt.md) 到 LLM 节点
4. 复制 [`agents/agent-1-grid-template/image-prompt-template.md`](agents/agent-1-grid-template/image-prompt-template.md) 到图像生成节点
5. 重复同样步骤搭建 Agent 2
6. 把 Agent 1 的输出作为 Agent 2 的输入（也可在 Coze 里串成一条工作流）

完整范例见 [`examples/`](examples/)。
