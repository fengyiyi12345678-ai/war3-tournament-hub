#!/usr/bin/env python3
"""
生成欧联杯决赛弗赖堡 vs 阿斯顿维拉抖音推荐视频
由于无法使用真实比赛画面，将生成动态图形动画视频
"""

import moviepy
from moviepy import ImageSequenceClip, ColorClip, CompositeVideoClip, TextClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# 视频参数
WIDTH, HEIGHT = 720, 1280  # 抖音竖屏比例 (降低分辨率)
FPS = 24  # 降低帧数
DURATION = 45  # 总时长约45秒

# 颜色定义
FREIBURG_RED = (138, 28, 47)  # 弗赖堡红色
VILLA_CLARET = (102, 46, 66)  # 维拉栗色
VILLA_BLUE = (47, 85, 151)   # 维拉蓝色
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)

def create_background(color1, color2, frame_num, total_frames):
    """创建渐变背景"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    
    # 动态渐变效果
    ratio = frame_num / total_frames
    for y in range(HEIGHT):
        progress = y / HEIGHT
        r = int(color1[0] * (1 - progress) + color2[0] * progress)
        g = int(color1[1] * (1 - progress) + color2[1] * progress)
        b = int(color1[2] * (1 - progress) + color2[2] * progress)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    return img

def add_text_overlay(img, text, position, font_size=60, color=WHITE, bold=False):
    """添加文字覆盖层"""
    draw = ImageDraw.Draw(img)
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # 文字阴影效果
    shadow_offset = 3
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), text, fill=BLACK, font=font)
    draw.text(position, text, fill=color, font=font)
    
    return img

def create_title_card(frame_num):
    """创建标题卡片（0-5秒）"""
    bg = create_background(FREIBURG_RED, VILLA_CLARET, frame_num, 150)
    draw = ImageDraw.Draw(bg)
    
    # 添加足球图案元素
    center_x, center_y = WIDTH // 2, HEIGHT // 2 - 100
    
    # 主标题
    title_text = "🔥欧联杯决赛🔥"
    add_text_overlay(bg, title_text, (WIDTH//2 - 280, 200), font_size=80, color=GOLD)
    
    # 对阵信息
    team1_text = "弗赖堡"
    team2_text = "阿斯顿维拉"
    add_text_overlay(bg, team1_text, (WIDTH//2 - 150, 500), font_size=70, color=WHITE)
    add_text_overlay(bg, "VS", (WIDTH//2 - 50, 600), font_size=60, color=GOLD)
    add_text_overlay(bg, team2_text, (WIDTH//2 - 200, 700), font_size=70, color=WHITE)
    
    # 时间信息
    time_text = "今晚决战！"
    add_text_overlay(bg, time_text, (WIDTH//2 - 120, 850), font_size=50, color=GOLD)
    
    # 底部提示
    tip_text = "三倍推荐方案⬇️"
    add_text_overlay(bg, tip_text, (WIDTH//2 - 150, 1100), font_size=45, color=WHITE)
    
    return bg

def create_team_analysis(team_name, colors, stats, start_frame, duration):
    """创建球队分析卡片"""
    frames = []
    for i in range(duration):
        frame_num = start_frame + i
        bg = create_background(colors[0], colors[1], i, duration)
        draw = ImageDraw.Draw(bg)
        
        # 球队名称
        add_text_overlay(bg, f"⚽ {team_name}", (50, 100), font_size=60, color=WHITE)
        
        # 统计数据
        y_pos = 250
        for stat in stats:
            label, value = stat
            add_text_overlay(bg, f"{label}:", (50, y_pos), font_size=40, color=WHITE)
            add_text_overlay(bg, value, (350, y_pos), font_size=40, color=GOLD)
            y_pos += 80
        
        # 进度条动画
        if i > 10:
            progress = min((i - 10) / 30, 1.0)
            bar_width = int(800 * progress)
            draw.rectangle([50, 600, 50 + bar_width, 630], fill=GOLD)
            add_text_overlay(bg, "近期状态", (50, 550), font_size=40, color=WHITE)
        
        frames.append(np.array(bg))
    
    return frames

def create_prediction_card(start_frame, duration):
    """创建推荐方案卡片"""
    frames = []
    for i in range(duration):
        frame_num = start_frame + i
        bg = create_background((20, 20, 40), (40, 20, 60), i, duration)
        draw = ImageDraw.Draw(bg)
        
        # 标题
        add_text_overlay(bg, "💎 三倍推荐方案 💎", (WIDTH//2 - 320, 100), font_size=55, color=GOLD)
        
        # 推荐内容
        predictions = [
            ("1️⃣ 进球数", "2-3球", "稳健"),
            ("2️⃣ 胜负", "维拉不败", "中等"),
            ("3️⃣ 比分", "1-2 / 2-2", "博高赔")
        ]
        
        y_pos = 250
        for pred in predictions:
            category, prediction, confidence = pred
            
            # 根据动画显示不同行
            if i > (predictions.index(pred) * 15):
                box_y = y_pos - 20
                draw.rounded_rectangle([50, box_y, WIDTH-50, y_pos+50], radius=15, 
                                      fill=(50, 50, 80, 180), outline=GOLD, width=3)
                add_text_overlay(bg, category, (80, y_pos), font_size=40, color=WHITE)
                add_text_overlay(bg, prediction, (400, y_pos), font_size=40, color=GOLD)
                add_text_overlay(bg, f"[{confidence}]", (800, y_pos), font_size=35, color=WHITE)
            
            y_pos += 100
        
        # 底部提醒
        if i > 50:
            add_text_overlay(bg, "⚠️ 理性购彩 量力而行", (WIDTH//2 - 280, 1400), 
                           font_size=35, color=WHITE)
        
        frames.append(np.array(bg))
        
    return frames

def create_ending_card(start_frame, duration):
    """创建结尾互动卡片"""
    frames = []
    for i in range(duration):
        bg = create_background(VILLA_BLUE, FREIBURG_RED, i, duration)
        draw = ImageDraw.Draw(bg)
        
        # 互动问题
        add_text_overlay(bg, "🤔 你看好谁？", (WIDTH//2 - 180, 400), font_size=60, color=WHITE)
        
        # 选项
        option1_y = 600 + int(20 * np.sin(i * 0.2))  # 轻微动画
        option2_y = 800 + int(20 * np.sin(i * 0.2 + 3))
        
        draw.rounded_rectangle([100, option1_y-30, WIDTH-100, option1_y+70], 
                              radius=20, fill=FREIBURG_RED, outline=WHITE, width=3)
        add_text_overlay(bg, "⚪ 弗赖堡", (WIDTH//2 - 150, option1_y), font_size=50, color=WHITE)
        
        draw.rounded_rectangle([100, option2_y-30, WIDTH-100, option2_y+70], 
                              radius=20, fill=VILLA_CLARET, outline=WHITE, width=3)
        add_text_overlay(bg, "🦁 阿斯顿维拉", (WIDTH//2 - 200, option2_y), font_size=50, color=WHITE)
        
        # CTA
        if i > 20:
            add_text_overlay(bg, "👇 评论区留下你的预测", (WIDTH//2 - 300, 1200), 
                           font_size=45, color=GOLD)
            add_text_overlay(bg, "❤️ 点赞 + ➕ 关注 获取更多推荐", (WIDTH//2 - 350, 1350), 
                           font_size=40, color=WHITE)
        
        frames.append(np.array(bg))
    
    return frames

def main():
    print("🎬 开始生成欧联杯决赛推荐视频...")
    
    all_frames = []
    
    # 1. 标题卡片 (4秒)
    print("生成标题卡片...")
    for i in range(96):  # 4秒 * 24fps
        all_frames.append(create_title_card(i))
    
    # 2. 弗赖堡分析 (8秒)
    print("生成弗赖堡分析...")
    freiburg_stats = [
        ("德甲排名", "第6名"),
        ("近5场", "3胜1平1负"),
        ("进攻核心", "格里福"),
        ("主场优势", "强势")
    ]
    freiburg_frames = create_team_analysis("弗赖堡", [FREIBURG_RED, (80, 20, 30)], 
                                           freiburg_stats, 96, 192)  # 8秒
    all_frames.extend(freiburg_frames)
    
    # 3. 维拉分析 (8秒)
    print("生成阿斯顿维拉分析...")
    villa_stats = [
        ("英超排名", "第4名"),
        ("近5场", "4胜0平1负"),
        ("进攻核心", "沃特金斯"),
        ("埃梅里战术", "欧战专家")
    ]
    villa_frames = create_team_analysis("阿斯顿维拉", [VILLA_CLARET, VILLA_BLUE], 
                                        villa_stats, 288, 192)  # 8秒
    all_frames.extend(villa_frames)
    
    # 4. 推荐方案 (12秒)
    print("生成推荐方案...")
    prediction_frames = create_prediction_card(480, 288)  # 12秒
    all_frames.extend(prediction_frames)
    
    # 5. 结尾互动 (8秒)
    print("生成结尾互动...")
    ending_frames = create_ending_card(768, 192)  # 8秒
    all_frames.extend(ending_frames)
    
    # 转换为视频
    print(f"合成视频中... (共{len(all_frames)}帧)")
    clip = ImageSequenceClip(all_frames, fps=FPS)
    
    # 输出视频
    output_file = "/workspace/europa_league_final_video.mp4"
    print("正在编码视频，请稍候...")
    clip.write_videofile(output_file, fps=FPS, codec='libx264', 
                        audio_codec='aac', temp_audiofile='temp-audio.m4a', 
                        remove_temp=True, verbose=False, logger=None)
    
    print(f"\n✅ 视频生成完成：{output_file}")
    print(f"📊 视频时长：{len(all_frames)/FPS:.1f}秒")
    print(f"📐 分辨率：{WIDTH}x{HEIGHT} (抖音竖屏)")
    print("\n💡 提示：")
    print("1. 可使用剪映等软件添加热门BGM")
    print("2. 建议添加动态贴纸和特效增强视觉冲击")
    print("3. 发布时添加话题：#欧联杯 #足球推荐 #弗赖堡vs维拉")

if __name__ == "__main__":
    main()
