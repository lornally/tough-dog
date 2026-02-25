#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器 - V7 最终版
高可见度 + 纤细线条 + 有机设计感
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

random.seed(789)

COLORS = {
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'bg_tertiary': '#334155',
    'accent_primary': '#CA8A04',
    'accent_secondary': '#B45309',
    'accent_highlight': '#F59E0B',
    'accent_bright': '#FCD34D',
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

class FinalEditor:
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
    
    def draw_final_lines(self):
        """绘制最终版高可见度纤细线条"""
        
        # ===== 1. 主曲线 - 高可见度金色 =====
        for i in range(25):
            start_x = random.randint(-100, self.width + 100)
            start_y = random.randint(0, self.height)
            
            points = [(start_x, start_y)]
            x, y = start_x, start_y
            
            for _ in range(random.randint(40, 80)):
                angle = random.uniform(0, 2 * math.pi)
                step = random.randint(20, 40)
                
                x += int(step * math.cos(angle))
                y += int(step * math.sin(angle))
                x += int(15 * math.sin(y / 30))
                y += int(15 * math.cos(x / 30))
                
                x = max(-150, min(self.width + 150, x))
                y = max(-150, min(self.height + 150, y))
                points.append((x, y))
            
            if len(points) > 3:
                width = random.choice([1, 1, 2])
                # 50-80%亮度，非常可见
                brightness = random.uniform(0.5, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                
                for j in range(len(points) - 1):
                    w = width if random.random() < 0.7 else width + 1
                    self.draw.line([points[j], points[j+1]], fill=color, width=w)
                
                # 明显的小瘤子
                for j in range(3, len(points) - 3, random.randint(2, 5)):
                    if random.random() < 0.7:
                        px, py = points[j]
                        size = random.randint(3, 6)
                        node_color = tuple(int(c * 0.9) for c in hex_to_rgb(COLORS['accent_highlight']))
                        self.draw.ellipse([(px-size, py-size), (px+size, py+size)], fill=node_color)
        
        # ===== 2. 细密树枝 =====
        def draw_branch(x, y, angle, length, depth):
            if depth > 4 or length < 12:
                return
            
            ctrl_x = x + int(length * math.cos(angle) * 0.5) + random.randint(-25, 25)
            ctrl_y = y + int(length * math.sin(angle) * 0.5) + random.randint(-25, 25)
            end_x = x + int(length * math.cos(angle))
            end_y = y + int(length * math.sin(angle))
            
            points = []
            for t in [i/15 for i in range(16)]:
                px = int((1-t)**2 * x + 2*(1-t)*t * ctrl_x + t**2 * end_x)
                py = int((1-t)**2 * y + 2*(1-t)*t * ctrl_y + t**2 * end_y)
                points.append((px, py))
            
            width = max(1, 2 - depth // 2)
            brightness = 0.5 - depth * 0.08
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
            
            for j in range(len(points) - 1):
                self.draw.line([points[j], points[j+1]], fill=color, width=width)
            
            num = random.choice([1, 2, 2, 3])
            for _ in range(num):
                new_angle = angle + random.uniform(-1.2, 1.2)
                new_length = length * random.uniform(0.45, 0.75)
                draw_branch(end_x, end_y, new_angle, new_length, depth + 1)
        
        for _ in range(12):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(60, 120)
            draw_branch(x, y, angle, length, 0)
        
        # ===== 3. 亮金丝 =====
        for i in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            points = [(x, y)]
            
            for _ in range(random.randint(40, 100)):
                x += random.randint(-5, 5)
                y += random.randint(-4, 4)
                x = max(0, min(self.width, x))
                y = max(0, min(self.height, y))
                if random.random() < 0.2:
                    points.append((x, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.4, 0.7)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                self.draw.line(points, fill=color, width=1)
        
        # ===== 4. 对角装饰线 =====
        for i in range(20):
            x1 = random.randint(-100, self.width + 100)
            y1 = random.choice([0, self.height])
            x2 = x1 + random.randint(-300, 300)
            y2 = self.height if y1 == 0 else 0
            
            brightness = random.uniform(0.2, 0.4)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
            self.draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    
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
        
        self.draw.rectangle([(right_x+10, 119), (self.width-10, 194)], 
                           fill=hex_to_rgb(COLORS['bg_tertiary']),
                           outline=hex_to_rgb(COLORS['accent_primary']), width=1)
        self.draw.text((right_x+20, 134), "🤖 AI Assistant", font=self.font_medium, fill=hex_to_rgb(COLORS['accent_primary']))
        
        # 命令栏 + 明显水流
        bar_y = self.height - 66
        self.draw.rectangle([(left_w, bar_y), (self.width-280, bar_y+46)], fill=hex_to_rgb(COLORS['bg_secondary']))
        
        for i in range(25):
            x = left_w + 25 + i * 35
            y = bar_y + 3
            for r in range(7, 0, -1):
                alpha = 0.8 / r
                base_rgb = hex_to_rgb(COLORS['accent_highlight'])
                color = tuple(int(c * alpha + hex_to_rgb(COLORS['bg_secondary'])[i] * (1-alpha))
                             for i, c in enumerate(base_rgb))
                self.draw.ellipse([(x-r, y-r), (x+5+r, y+r)], fill=color)
        
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
        self.draw_final_lines()
        self.draw_ui()
        return self.img
    
    def save(self, filename="macos_editor_v7_final.png"):
        self.img.save(filename)
        print(f"✅ 已保存: {filename}")

if __name__ == "__main__":
    editor = FinalEditor()
    editor.render()
    editor.save()
