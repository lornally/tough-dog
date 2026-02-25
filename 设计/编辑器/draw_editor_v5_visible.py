#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器 - V5 可见性优化版
纤细但不失可见度，有设计感的随机线条
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

random.seed(123)

COLORS = {
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'bg_tertiary': '#334155',
    'accent_primary': '#CA8A04',
    'accent_secondary': '#B45309',
    'accent_highlight': '#F59E0B',
    'text_primary': '#E8F0FF',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    'traffic_red': '#FF5F57',
    'traffic_yellow': '#FFBD2E',
    'traffic_green': '#28CA42',
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class VisibleEditor:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        self.img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_primary']))
        self.draw = ImageDraw.Draw(self.img)
        
        try:
            self.font_large = ImageFont.truetype("/System/Library/Fonts/SFProDisplay-Regular.otf", 16)
            self.font_medium = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 13)
            self.font_small = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 11)
            self.font_code = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_code = ImageFont.load_default()
    
    def draw_visible_organic_lines(self):
        """绘制可见的有机线条 - 纤细但有设计感"""
        
        # ===== 1. 主要流动曲线（细但可见）=====
        for i in range(15):
            # 随机起点
            x = random.randint(-100, self.width + 100)
            y = random.randint(100, self.height - 100)
            
            points = [(x, y)]
            num_segments = random.randint(5, 12)
            
            for _ in range(num_segments):
                # 随机角度和距离
                angle = random.uniform(-math.pi/2, math.pi/2) + random.choice([0, math.pi])
                dist = random.randint(80, 200)
                
                # 控制点创造曲线
                mid_x = x + int(dist * math.cos(angle) / 2) + random.randint(-30, 30)
                mid_y = y + int(dist * math.sin(angle) / 2) + random.randint(-30, 30)
                end_x = x + int(dist * math.cos(angle))
                end_y = y + int(dist * math.sin(angle))
                
                # 贝塞尔曲线点
                for t in [0.2, 0.4, 0.6, 0.8, 1.0]:
                    px = int((1-t)**2 * x + 2*(1-t)*t * mid_x + t**2 * end_x)
                    py = int((1-t)**2 * y + 2*(1-t)*t * mid_y + t**2 * end_y)
                    points.append((px, py))
                
                x, y = end_x, end_y
            
            # 绘制主线条 - 纤细可见
            if len(points) > 1:
                width = random.choice([1, 1, 2])  # 主要是1px，偶尔2px
                alpha = random.uniform(0.15, 0.35)  # 可见但不抢镜
                
                color_choice = random.choice([
                    COLORS['accent_primary'],
                    COLORS['accent_secondary'],
                    COLORS['accent_highlight']
                ])
                base_rgb = hex_to_rgb(color_choice)
                color = tuple(int(c * alpha + hex_to_rgb(COLORS['bg_primary'])[i] * (1-alpha)) 
                             for i, c in enumerate(base_rgb))
                
                self.draw.line(points, fill=color, width=width)
                
                # 添加"小瘤子"节点 - 随机膨胀
                for j in range(1, len(points)-1, random.randint(2, 4)):
                    if random.random() < 0.5:
                        px, py = points[j]
                        size = random.randint(2, 5)
                        node_alpha = alpha * 1.3
                        node_color = tuple(int(c * node_alpha + hex_to_rgb(COLORS['bg_primary'])[i] * (1-node_alpha))
                                          for i, c in enumerate(base_rgb))
                        self.draw.ellipse([(px-size, py-size), (px+size, py+size)], fill=node_color)
        
        # ===== 2. 树枝状分叉（细线）=====
        def draw_branch(x, y, angle, length, depth):
            if depth > 4 or length < 20:
                return
            
            end_x = x + int(length * math.cos(angle))
            end_y = y + int(length * math.sin(angle))
            
            # 弯曲
            mid_x = (x + end_x) // 2 + random.randint(-15, 15)
            mid_y = (y + end_y) // 2 + random.randint(-15, 15)
            
            # 绘制
            width = max(1, 2 - depth // 2)
            alpha = 0.2 - depth * 0.03
            base_rgb = hex_to_rgb(COLORS['accent_primary'])
            color = tuple(int(c * alpha + hex_to_rgb(COLORS['bg_primary'])[i] * (1-alpha))
                         for i, c in enumerate(base_rgb))
            
            self.draw.line([(x, y), (mid_x, mid_y), (end_x, end_y)], fill=color, width=width)
            
            # 分叉
            if random.random() < 0.7:
                draw_branch(end_x, end_y, angle + random.uniform(0.4, 0.9), 
                           length * random.uniform(0.5, 0.75), depth + 1)
            if random.random() < 0.5:
                draw_branch(end_x, end_y, angle - random.uniform(0.4, 0.9), 
                           length * random.uniform(0.4, 0.65), depth + 1)
        
        # 生成树枝
        for _ in range(8):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(100, 180)
            draw_branch(x, y, angle, length, 0)
        
        # ===== 3. 极细的金丝（点缀）=====
        for i in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            points = [(x, y)]
            
            for _ in range(random.randint(20, 50)):
                x += random.randint(-5, 5)
                y += random.randint(-3, 3)
                x = max(0, min(self.width, x))
                y = max(0, min(self.height, y))
                if random.random() < 0.3:
                    points.append((x, y))
            
            if len(points) > 1:
                alpha = random.uniform(0.2, 0.4)
                base_rgb = hex_to_rgb(COLORS['accent_highlight'])
                color = tuple(int(c * alpha + hex_to_rgb(COLORS['bg_primary'])[i] * (1-alpha))
                             for i, c in enumerate(base_rgb))
                self.draw.line(points, fill=color, width=1)
    
    def draw_ui(self):
        """绘制UI"""
        # 标题栏
        self.draw.rectangle([(0, 0), (self.width, 38)], fill=hex_to_rgb(COLORS['bg_secondary']))
        for x, c in [(20, COLORS['traffic_red']), (40, COLORS['traffic_yellow']), (60, COLORS['traffic_green'])]:
            self.draw.ellipse([(x-6, 13), (x+6, 25)], fill=hex_to_rgb(c))
        self.draw.text((650, 10), "Golden Editor", font=self.font_medium, fill=hex_to_rgb(COLORS['text_secondary']))
        
        # 左侧面板
        left_w = 220
        self.draw.rectangle([(0, 38), (left_w, self.height-20)], fill=hex_to_rgb(COLORS['bg_secondary']))
        self.draw.text((15, 53), "EXPLORER", font=self.font_small, fill=hex_to_rgb(COLORS['text_muted']))
        
        files = [("  🟨  main.js", True), ("  📄  utils.js", False), ("  📄  config.js", False)]
        y = 83
        for name, active in files:
            if active:
                self.draw.rectangle([(0, y-3), (left_w, y+22)], fill=hex_to_rgb(COLORS['bg_tertiary']))
                self.draw.line([(0, y-3), (0, y+22)], fill=hex_to_rgb(COLORS['accent_primary']), width=3)
            self.draw.text((15, y), name, font=self.font_medium, 
                          fill=hex_to_rgb(COLORS['text_primary'] if active else COLORS['text_secondary']))
            y += 28
        
        # 标签栏
        self.draw.rectangle([(left_w, 38), (self.width-280, 74)], fill=hex_to_rgb(COLORS['bg_primary']))
        self.draw.rectangle([(left_w+10, 43), (left_w+120, 74)], fill=hex_to_rgb(COLORS['bg_secondary']))
        self.draw.line([(left_w+10, 43), (left_w+120, 43)], fill=hex_to_rgb(COLORS['accent_primary']), width=3)
        self.draw.text((left_w+22, 50), "main.js", font=self.font_medium, fill=hex_to_rgb(COLORS['text_primary']))
        
        # 编辑区
        editor_h = self.height - 140
        self.draw.rectangle([(left_w, 74), (self.width-280, 74+editor_h)], fill=hex_to_rgb(COLORS['bg_primary']))
        
        # 代码
        lines = [
            ("1", "import { useState } from 'react';", '#F59E0B'),
            ("2", "", COLORS['text_secondary']),
            ("3", "function App() {", '#F59E0B'),
            ("4", "  const [count, setCount] = useState(0);", COLORS['text_primary'], True),
            ("5", "", COLORS['text_secondary']),
            ("6", "  return (", COLORS['text_secondary']),
            ("7", "    <div className='app'>", COLORS['text_secondary']),
        ]
        
        y = 94
        for num, code, color, *rest in lines:
            is_current = rest[0] if rest else False
            if is_current:
                self.draw.rectangle([(left_w, y-3), (self.width-280, y+24)], fill=hex_to_rgb('#1E293B'))
                self.draw.line([(left_w, y-3), (left_w, y+24)], fill=hex_to_rgb(COLORS['accent_primary']), width=4)
            
            self.draw.text((left_w+45, y), num, font=self.font_small,
                          fill=hex_to_rgb(COLORS['accent_primary'] if is_current else COLORS['text_muted']))
            self.draw.text((left_w+75, y), code, font=self.font_code, fill=hex_to_rgb(color))
            y += 26
        
        # 右侧面板
        right_x = self.width - 280
        self.draw.rectangle([(right_x, 74), (self.width, 74+editor_h)], fill=hex_to_rgb(COLORS['bg_secondary']))
        self.draw.line([(right_x, 74), (right_x, 74+editor_h)], fill=hex_to_rgb(COLORS['accent_primary']), width=2)
        self.draw.text((right_x+15, 89), "CONTEXT", font=self.font_small, fill=hex_to_rgb(COLORS['text_muted']))
        
        # AI卡片
        self.draw.rectangle([(right_x+10, 119), (self.width-10, 194)], 
                           fill=hex_to_rgb(COLORS['bg_tertiary']),
                           outline=hex_to_rgb(COLORS['accent_primary']), width=1)
        self.draw.text((right_x+20, 134), "🤖 AI Assistant", font=self.font_medium, fill=hex_to_rgb(COLORS['accent_primary']))
        
        # 命令栏 + 明显水流
        bar_y = self.height - 66
        self.draw.rectangle([(left_w, bar_y), (self.width-280, bar_y+46)], fill=hex_to_rgb(COLORS['bg_secondary']))
        
        # 水流特效
        for i in range(15):
            x = left_w + 40 + i * 55
            y = bar_y + 3
            for r in range(5, 0, -1):
                alpha = 0.6 / r
                base_rgb = hex_to_rgb(COLORS['accent_highlight'])
                color = tuple(int(c * alpha + hex_to_rgb(COLORS['bg_secondary'])[i] * (1-alpha))
                             for i, c in enumerate(base_rgb))
                self.draw.ellipse([(x-r, y-r), (x+3+r, y+r)], fill=color)
        
        self.draw.text((left_w+15, bar_y+12), ">", font=self.font_large, fill=hex_to_rgb(COLORS['accent_primary']))
        self.draw.text((left_w+35, bar_y+14), 'git commit -m "feat: add counter"', 
                      font=self.font_medium, fill=hex_to_rgb(COLORS['text_primary']))
        
        # 状态栏
        self.draw.rectangle([(0, self.height-20), (self.width, self.height)], fill=hex_to_rgb(COLORS['accent_primary']))
        items = ["Ln 4, Col 15", "UTF-8", "JavaScript", "🌙 暗黑", "⎋ LEAP"]
        x = 15
        for item in items:
            self.draw.text((x, self.height-16), item, font=self.font_small, fill=hex_to_rgb('#0F172A'))
            bbox = self.draw.textbbox((0, 0), item, font=self.font_small)
            x += (bbox[2]-bbox[0]) + 25
    
    def render(self):
        self.draw_visible_organic_lines()
        self.draw_ui()
        return self.img
    
    def save(self, filename="macos_editor_v5_visible.png"):
        self.img.save(filename)
        print(f"✅ 已保存: {filename}")

if __name__ == "__main__":
    editor = VisibleEditor()
    editor.render()
    editor.save()
