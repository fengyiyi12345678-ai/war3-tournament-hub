# Agent 1 工作流节点配置

> 参考 [`docs/coze-setup.md`](../../docs/coze-setup.md) 完整教程。本文件是节点级速查表 + 拼图代码片段。

## 节点表

| # | 节点 | 类型 | 模型 / 插件 | 输入 | 输出 |
| --- | --- | --- | --- | --- | --- |
| Start | 开始 | 开始节点 | — | image_url, style_anchor, language | — |
| A | 产品要素识别 | LLM | Doubao-1.5-vision-pro | image_url | product_meta (JSON) |
| B | 9 镜分镜生成 | LLM | Doubao-1.5-pro-32k | product_meta, style_anchor | storyboard (JSON) |
| C | 9 张参考图 | 循环 + 图像生成 | Seedream 3.0 i2i | storyboard.cells[i].image_prompt + image_url | cells[i].image_url |
| D | 3×3 拼图 + 角标 | 代码节点 (Python) | PIL | cells[].image_url, storyboard | grid_image_url |
| End | 结束 | 结束节点 | — | grid_image_url, storyboard | — |

## 节点 C 的循环配置

- **循环类型**：`数组循环`
- **数组变量**：`{{node_B.output.cells}}`
- **循环体**：单个「图像生成」节点
  - `prompt` ← `{{item.image_prompt}}`
  - `reference_image` ← `{{Start.output.image_url}}`
  - `mode` = `i2i`
  - `strength` = `0.7`
  - `aspect_ratio` = `1:1`
  - `seed` = `{{item.shot_id_as_int}}` 或 `-1`
- **循环输出**：将生成图 URL 回填到 `item.image_url`

## 节点 D · 拼图代码片段（Python，可直接粘到 Coze 代码节点）

```python
# Coze 代码节点（Python 3）
# 输入参数：cells (list of dict, 含 shot_id/role/image_url)，grid_size = 1024
# 依赖：requests, Pillow（Coze 内置）

import io
import requests
from PIL import Image, ImageDraw, ImageFont

def main(args):
    cells = args["cells"]
    grid_size = args.get("grid_size", 1024)
    cell_size = grid_size // 3
    canvas = Image.new("RGB", (grid_size, grid_size), (20, 20, 20))

    # 按 shot_id 01..09 排序
    cells = sorted(cells, key=lambda c: c["shot_id"])

    try:
        font = ImageFont.truetype("/usr/share/fonts/NotoSansSC-Bold.otf", 26)
    except OSError:
        font = ImageFont.load_default()

    for cell in cells:
        row, col = cell["position"]  # 1-based
        x = (col - 1) * cell_size
        y = (row - 1) * cell_size

        # 下载并裁剪到正方形
        resp = requests.get(cell["image_url"], timeout=30)
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w - side) // 2, (h - side) // 2,
                        (w + side) // 2, (h + side) // 2))
        img = img.resize((cell_size, cell_size), Image.LANCZOS)
        canvas.paste(img, (x, y))

        # 左上角角标：shot_id + role
        draw = ImageDraw.Draw(canvas)
        label = f"{cell['shot_id']} · {cell['role']}"
        # 半透明黑底
        text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
        draw.rectangle(
            [x + 8, y + 8, x + 8 + text_w + 16, y + 8 + text_h + 10],
            fill=(0, 0, 0, 180),
        )
        draw.text((x + 16, y + 13), label, fill=(255, 255, 255), font=font)

        # 右下角字幕
        if cell.get("subtitle"):
            sub = cell["subtitle"]
            sub_w, sub_h = draw.textbbox((0, 0), sub, font=font)[2:]
            draw.rectangle(
                [x + cell_size - sub_w - 24, y + cell_size - sub_h - 18,
                 x + cell_size - 8, y + cell_size - 8],
                fill=(0, 0, 0, 180),
            )
            draw.text(
                (x + cell_size - sub_w - 16, y + cell_size - sub_h - 13),
                sub,
                fill=(255, 255, 255),
                font=font,
            )

    # 上传到 Coze 临时图床或对象存储，返回 URL
    buf = io.BytesIO()
    canvas.save(buf, format="PNG", optimize=True)
    grid_image_url = upload_to_coze_oss(buf.getvalue(), "grid.png")  # Coze 内置 SDK
    return {"grid_image_url": grid_image_url}
```

> `upload_to_coze_oss` 在 Coze 代码节点中通过 `coze.tools.upload_image()` 调用；Dify 用 `tool.invoke("uploader", ...)`。
