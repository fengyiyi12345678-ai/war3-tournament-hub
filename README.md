# ⚽ 足球短视频自动生成

输入一对球队 → AI 生成文案 + 自动找 YouTube 素材 + ffmpeg 渲染 → 输出抖音/小红书可发的 30 秒竖屏 mp4。

## 🎯 一句话用法

```bash
python generator/generate.py "皇马" "巴萨" "西甲国家德比"
```

跑完视频在 `video-pipeline/out/`。

## 📚 详细文档

- [`generator/README.md`](generator/README.md) - 自动生成器用法
- [`video-pipeline/README.md`](video-pipeline/README.md) - 底层渲染管线
- [`video-pipeline/Windows使用说明.md`](video-pipeline/Windows使用说明.md) - Windows 一键操作

## ☁️ 云端使用

提一个 [Issue](../../issues/new?template=video-request.yml) 选模板"🎬 生成新视频" → 等 10 分钟 → 自动评论下载链接。

或仓库 Actions → "Generate Football Video" → Run workflow。

## 🛠 已有的副产物

- `lazio-inter-graphics/` - 10 张 SVG 图文海报（拉齐奥 vs 国米示例）
- `video-pipeline/` - 现成可跑的视频管线
- `generator/` - 自动化内容工厂

> ⚠️ 免责声明：本项目生成的"赛事预测"均为娱乐讨论，不构成任何投注建议。LLM 生成的具体数据（伤停、赛果）发布前请核实。
