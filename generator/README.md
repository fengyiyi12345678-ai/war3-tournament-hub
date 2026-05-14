# 🤖 自动足球短视频生成器

输入一对球队 → 自动产文案 + 自动找素材 + 自动渲染出 30 秒抖音视频。

---

## 🚀 用法

### 本地跑

```bash
# 自动选 provider（按可用 API key）
python generator/generate.py "皇马" "巴萨" "西甲国家德比"

# 强制用本地模板（不需要 API key，零依赖）
python generator/generate.py "皇马" "巴萨" --provider template

# 用 Claude API
ANTHROPIC_API_KEY=sk-ant-xxx \
  python generator/generate.py "皇马" "巴萨" "国家德比" --provider claude

# 用 DeepSeek API
DEEPSEEK_API_KEY=sk-xxx \
  python generator/generate.py "皇马" "巴萨" "国家德比" --provider deepseek
```

跑完之后视频在 `video-pipeline/out/`。

### 云端跑（GitHub Actions）

1. 仓库 → **Issues** → **New issue** → 选 "🎬 生成新视频"
2. 填表单提交
3. 等 10-15 分钟
4. issue 里会自动留言带下载链接

或者：仓库 → **Actions** → **Generate Football Video** → **Run workflow** → 填参数

---

## 📋 三种文案生成方式对比

| 方式 | API Key | 文案质量 | 成本 |
|---|---|---|---|
| `claude` | `ANTHROPIC_API_KEY` | ⭐⭐⭐⭐⭐ 最自然 | ~¥0.1 / 视频 |
| `deepseek` | `DEEPSEEK_API_KEY` | ⭐⭐⭐⭐ 不错 | ~¥0.01 / 视频 |
| `template` | 不需要 | ⭐⭐⭐ 工整 | 免费 |

### 配置 API Key

#### 本地（环境变量）
```bash
export ANTHROPIC_API_KEY=sk-ant-xxx
export DEEPSEEK_API_KEY=sk-xxx
```

#### GitHub Actions（Secret）
仓库 → Settings → Secrets and variables → Actions → New secret：
- `ANTHROPIC_API_KEY` = `sk-ant-...`
- `DEEPSEEK_API_KEY` = `sk-...`

---

## 🏗 项目结构

```
generator/
├── generate.py            ← 入口，组合 LLM + YouTube + 渲染
├── llm.py                 ← 三套 provider 抽象
├── youtube.py             ← yt-dlp 搜索 + 下载
├── prompts.py             ← LLM 提示词
├── templates/             ← 本地模板（无 API 模式用）
│   ├── default.json
│   ├── derby.json
│   └── cup_final.json
└── README.md
```

跑完会写两个文件给现有 pipeline 用：
- `video-pipeline/config.json` —— make_video.py 的动态配置
- `video-pipeline/subtitles.srt` —— 烧录的中文字幕

---

## 🎬 工作流程

```
1. LLM 拿到对阵 → 生成完整 JSON 脚本 (8 段时间线 + 字幕)
2. yt-dlp 按 "Real Madrid celebration" 类关键词搜 YouTube → 拿到 URL
3. 写 config.json + subtitles.srt
4. 调用现有的 make_video.py 走老流程
5. 输出 mp4
```

---

## 💡 自定义

### 改提示词风格

编辑 `prompts.py` 里的 `SYSTEM_PROMPT` / `SCRIPT_PROMPT`。

### 加新的本地模板

在 `templates/` 下加 JSON，文件名约定：
- `default.json` —— 兜底
- `derby.json` —— 包含 "德比/derby/国家" 关键词时选用
- `cup_final.json` —— 包含 "杯/决赛/final" 时选用

往里面填 `{team_a}` `{team_b}` `{context}` 占位符即可。

### 改视频时间线模板

`prompts.py` 里规定了 8 段的角色（钩子/数据/反转…），改这里就能改整体节奏。

---

## ⚠️ 限制

- **YouTube 访问**：本地跑需要能连 YouTube（国内要梯子）。GitHub Actions 默认可以连。
- **地区屏蔽**：少量视频会被 YouTube 地区屏蔽，会自动退化成文字卡片。
- **LLM 准确性**：生成的伤停/赛果数据 LLM 可能编，**发布前自己核实关键事实**。
- **不构成投注建议**：所有"预测"都是娱乐内容。
