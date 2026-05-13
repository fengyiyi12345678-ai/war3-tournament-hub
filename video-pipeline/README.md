# 🎬 拉齐奥 vs 国米 抖音视频生成 Pipeline

**全自动**从 YouTube 下载素材 → 截取 → 加字幕 → 加 BGM → 输出 30 秒竖屏 mp4。

## 📋 你需要装的工具

```bash
# macOS
brew install yt-dlp ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install ffmpeg
pip install -U yt-dlp

# Windows (WSL 推荐)
sudo apt install ffmpeg
pip install -U yt-dlp
```

中文字体（**必须**，否则文字会丢失）：
- macOS / Windows：自带就有 ✓
- Linux：`sudo apt install fonts-noto-cjk` 或 `sudo apt install fonts-wqy-microhei`

## 🚀 一键运行

```bash
chmod +x run.sh
./run.sh
```

完成后视频在 `out/lazio_inter_30s.mp4`，直接拖进抖音 / 小红书上传即可。

## 🎵 加 BGM（可选）

把任意 mp3 重命名为 `bgm.mp3` 放在这个目录下，再跑 `./make_video.sh` 就会自动混音。

推荐：
- 抖音曲库搜「足球解说 Phonk」
- 或下载 [Pixabay 免费 BGM](https://pixabay.com/music/search/sports/)

## 📁 目录结构

```
video-pipeline/
├── run.sh              # 一键全流程入口
├── download.sh         # 从 YouTube 下载素材
├── make_video.sh       # FFmpeg 渲染管线
├── config.sh           # 改参数 / 时间线 / 素材源
├── subtitles.srt       # 中文字幕
├── README.md
├── bgm.mp3             # ← 你自己放（可选）
├── assets/             # 自动生成：下载的原始素材
├── clips/              # 自动生成：渲染好的片段
└── out/
    └── lazio_inter_30s.mp4   # 最终输出
```

## 🎛 自定义

改 `config.sh` 中的 `TIMELINE` 数组，每行格式：
```
段号 | 时长秒 | 类型 | 来源key | 起始秒 | 主标题 | 副标题 | 背景色/滤镜
```
- `yt`：从 YouTube 素材截取（叠加文字）
- `card`：纯色文字卡片（无视频）
- `mix`：从 YouTube 截取 + 加滤镜（如 `sepia` 复古）

## 🔧 分步运行

```bash
./download.sh      # 仅下载素材
./make_video.sh    # 仅渲染（前提：素材已就绪）
```

## ⚠️ 故障排查

| 问题 | 解决 |
|---|---|
| `yt-dlp` 报错 403 / 频率限制 | 等 10 分钟再试，或挂代理 |
| 字幕乱码 / 不显示 | 装中文字体后重跑（见上方） |
| 视频卡顿 / 黑屏 | 检查 `assets/*.mp4` 是否下载完整 |
| 没声音 | 放一个 `bgm.mp3` 进来再跑 |

## 📌 素材来源（YouTube）

| key | 用途 | URL |
|---|---|---|
| inter_celebration | 国米庆祝集锦 | https://www.youtube.com/watch?v=vgHwOfIB6Qk |
| dazn_highlights | 3-0 DAZN 集锦 | https://www.youtube.com/watch?v=4iRpY1KXfOY |
| history_2000 | 2000 决赛全场 | https://www.youtube.com/watch?v=f4UvzFrClsY |
| stadium_aerial | 罗马奥林匹克航拍 | https://www.youtube.com/watch?v=w7Ar_QoWPvU |

## ⚖️ 版权提示

下载的 YouTube 素材仅供**个人学习/二次创作**使用。
发布前请遵守平台规则：
- 单段引用 ≤ 8 秒
- 加上自己的解说字幕 / 二创处理
- 注明素材来源

> **本项目不构成任何投注建议，赛事预测内容仅供娱乐讨论。**
