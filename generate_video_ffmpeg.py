#!/usr/bin/env python3
"""
使用FFmpeg直接生成欧联杯决赛推荐视频 (内存优化版)
"""

import subprocess
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 视频参数
WIDTH, HEIGHT = 540, 960  # 更低分辨率
FPS = 20
OUTPUT_FILE = "/workspace/europa_league_final_video.mp4"

# 颜色
FREIBURG_RED = (138, 28, 47)
VILLA_CLARET = (102, 46, 66)
VILLA_BLUE = (47, 85, 151)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def draw_frame(scene_type, frame_offset, total_frames):
    """绘制单帧"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(40)
    font_medium = get_font(28)
    font_small = get_font(22)
    
    if scene_type == 0:  # 标题
        # 渐变背景
        for y in range(HEIGHT):
            r = int(FREIBURG_RED[0] * (1-y/HEIGHT) + VILLA_CLARET[0] * y/HEIGHT)
            g = int(FREIBURG_RED[1] * (1-y/HEIGHT) + VILLA_CLARET[1] * y/HEIGHT)
            b = int(FREIBURG_RED[2] * (1-y/HEIGHT) + VILLA_CLARET[2] * y/HEIGHT)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
        draw.text((WIDTH//2-100, 150), "🔥欧联杯决赛🔥", fill=GOLD, font=font_large)
        draw.text((WIDTH//2-80, 300), "弗赖堡", fill=WHITE, font=font_medium)
        draw.text((WIDTH//2-40, 380), "VS", fill=GOLD, font=font_medium)
        draw.text((WIDTH//2-100, 460), "阿斯顿维拉", fill=WHITE, font=font_medium)
        draw.text((WIDTH//2-70, 580), "今晚决战!", fill=GOLD, font=font_medium)
        draw.text((WIDTH//2-90, 700), "三倍推荐⬇️", fill=WHITE, font=font_small)
        
    elif scene_type == 1:  # 弗赖堡
        for y in range(HEIGHT):
            r = int(FREIBURG_RED[0] * (1-y/HEIGHT) + 60 * y/HEIGHT)
            g = int(20 * (1-y/HEIGHT) + 10 * y/HEIGHT)
            b = int(30 * (1-y/HEIGHT) + 20 * y/HEIGHT)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
        draw.text((30, 50), "⚽ 弗赖堡", fill=WHITE, font=font_medium)
        stats = ["德甲第6", "近5场:3胜1平1负", "核心:格里福", "主场强势"]
        for i, stat in enumerate(stats):
            if frame_offset > i * 20:
                draw.text((30, 120 + i*60), stat, fill=GOLD, font=font_small)
        if frame_offset > 80:
            progress = min((frame_offset-80)/40, 1) * 200
            draw.rectangle([30, 380, 30+progress, 400], fill=GOLD)
            draw.text((30, 350), "状态", fill=WHITE, font=font_small)
            
    elif scene_type == 2:  # 维拉
        for y in range(HEIGHT):
            r = int(VILLA_CLARET[0] * (1-y/HEIGHT) + VILLA_BLUE[0] * y/HEIGHT)
            g = int(VILLA_CLARET[1] * (1-y/HEIGHT) + VILLA_BLUE[1] * y/HEIGHT)
            b = int(VILLA_CLARET[2] * (1-y/HEIGHT) + VILLA_BLUE[2] * y/HEIGHT)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
        draw.text((30, 50), "🦁 阿斯顿维拉", fill=WHITE, font=font_medium)
        stats = ["英超第4", "近5场:4胜0平1负", "核心:沃特金斯", "埃梅里:欧战专家"]
        for i, stat in enumerate(stats):
            if frame_offset > i * 20:
                draw.text((30, 120 + i*60), stat, fill=GOLD, font=font_small)
        if frame_offset > 80:
            progress = min((frame_offset-80)/40, 1) * 200
            draw.rectangle([30, 380, 30+progress, 400], fill=GOLD)
            draw.text((30, 350), "状态", fill=WHITE, font=font_small)
            
    elif scene_type == 3:  # 推荐
        for y in range(HEIGHT):
            r = int(20 + 10 * y/HEIGHT)
            g = int(20 + 5 * y/HEIGHT)
            b = int(40 + 20 * y/HEIGHT)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
        draw.text((WIDTH//2-110, 40), "💎 三倍推荐 💎", fill=GOLD, font=font_medium)
        preds = [("进球数","2-3球"), ("胜负","维拉不败"), ("比分","1-2/2-2")]
        for i, (cat, val) in enumerate(preds):
            if frame_offset > i * 30:
                y_pos = 130 + i*80
                draw.rounded_rectangle([20, y_pos-15, WIDTH-20, y_pos+35], radius=10, 
                                      fill=(40, 40, 70), outline=GOLD, width=2)
                draw.text((30, y_pos), cat, fill=WHITE, font=font_small)
                draw.text((WIDTH//2, y_pos), val, fill=GOLD, font=font_small)
        if frame_offset > 100:
            draw.text((WIDTH//2-100, 500), "⚠️ 理性购彩", fill=WHITE, font=font_small)
            
    elif scene_type == 4:  # 结尾
        for y in range(HEIGHT):
            r = int(VILLA_BLUE[0] * (1-y/HEIGHT) + FREIBURG_RED[0] * y/HEIGHT)
            g = int(VILLA_BLUE[1] * (1-y/HEIGHT) + FREIBURG_RED[1] * y/HEIGHT)
            b = int(VILLA_BLUE[2] * (1-y/HEIGHT) + FREIBURG_RED[2] * y/HEIGHT)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
        draw.text((WIDTH//2-80, 150), "🤔 你看好谁?", fill=WHITE, font=font_medium)
        
        offset = int(10 * np.sin(frame_offset * 0.15))
        draw.rounded_rectangle([40, 250+offset, WIDTH-40, 310+offset], 
                              radius=15, fill=FREIBURG_RED, outline=WHITE, width=2)
        draw.text((WIDTH//2-60, 265+offset), "弗赖堡", fill=WHITE, font=font_small)
        
        offset2 = int(10 * np.sin(frame_offset * 0.15 + 3))
        draw.rounded_rectangle([40, 350+offset2, WIDTH-40, 410+offset2], 
                              radius=15, fill=VILLA_CLARET, outline=WHITE, width=2)
        draw.text((WIDTH//2-70, 365+offset2), "阿斯顿维拉", fill=WHITE, font=font_small)
        
        if frame_offset > 30:
            draw.text((WIDTH//2-100, 500), "👇 评论区预测", fill=GOLD, font=font_small)
            draw.text((WIDTH//2-100, 550), "❤️ 点赞+关注", fill=WHITE, font=font_small)
    
    return np.array(img)

def main():
    print("🎬 开始生成视频 (FFmpeg优化版)...")
    
    # 场景配置：(类型，帧数)
    scenes = [(0, 80), (1, 160), (2, 160), (3, 240), (4, 160)]
    total_frames = sum(frames for _, frames in scenes)
    
    temp_dir = tempfile.mkdtemp()
    print(f"临时目录：{temp_dir}")
    print(f"总帧数：{total_frames}")
    
    # 逐帧生成并立即写入文件
    frame_idx = 0
    for scene_type, num_frames in scenes:
        print(f"生成场景 {scene_type+1}/5...")
        for i in range(num_frames):
            img = draw_frame(scene_type, i, num_frames)
            frame_path = f"{temp_dir}/frame_{frame_idx:05d}.png"
            Image.fromarray(img).save(frame_path)
            frame_idx += 1
    
    print("使用FFmpeg编码视频...")
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-framerate', str(FPS),
        '-i', f'{temp_dir}/frame_%05d.png',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        '-vf', f'scale={WIDTH}:{HEIGHT}',
        OUTPUT_FILE
    ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    # 清理临时文件
    subprocess.run(['rm', '-rf', temp_dir])
    
    if result.returncode == 0:
        print(f"\n✅ 视频生成完成：{OUTPUT_FILE}")
        duration = total_frames / FPS
        print(f"📊 时长：{duration:.1f}秒")
        print(f"📐 分辨率：{WIDTH}x{HEIGHT}")
        print("\n💡 下一步:")
        print("1. 用剪映添加BGM和特效")
        print("2. 发布时加话题：#欧联杯 #足球推荐")
    else:
        print(f"❌ 失败：{result.stderr}")

if __name__ == "__main__":
    main()
