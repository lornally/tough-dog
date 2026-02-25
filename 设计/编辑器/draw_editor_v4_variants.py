#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器 - V4 多版本变体
尝试各种纤细、不规律、随机的线条风格
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

# 暗黑金配色
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

def blend_color(color1, color2, alpha):
    return tuple(int(c1 * (1 - alpha) + c2 * alpha) for c1, c2 in zip(color1, color2))

class EditorVariant:
    def __init__(self, width=1400, height=900, seed=42):
        self.width = width
        self.height = height
        random.seed(seed)
        
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
    
    def create_base(self):
        """创建基础画布"""
        img = Image.new('RGB', (self.width, self.height), hex_to_rgb(COLORS['bg_primary']))
        return img, ImageDraw.Draw(img)
    
    # ========== 变体 1: 纤细随机蛇形线 ==========
    def draw_snake_lines(self, draw, intensity=0.08):
        """蛇形线 - 蜿蜒曲折，有膨胀节点"""
        for i in range(25):
            # 随机起点
            x = random.randint(0, self.width)
            y = random.randint(50, self.height - 50)
            
            points = [(x, y)]
            segments = random.randint(8, 15)
            
            for _ in range(segments):
                # 随机方向和距离
                angle = random.uniform(0, 2 * math.pi)
                dist = random.randint(30, 80)
                x += int(dist * math.cos(angle))
                y += int(dist * math.sin(angle))
                x = max(0, min(self.width, x))
                y = max(0, min(self.height, y))
                points.append((x, y))
            
            # 绘制主线
            if len(points) > 1:
                width = random.choice([1, 1, 2, 2, 3])  # 大部分很细，偶尔稍粗
                color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    intensity
                )
                draw.line(points, fill=color, width=width)
                
                # 添加"小瘤子"节点
                for j in range(1, len(points) - 1):
                    if random.random() < 0.4:  # 40%概率有节点
                        px, py = points[j]
                        node_size = random.randint(2, 5)
                        node_color = blend_color(
                            hex_to_rgb(COLORS['bg_primary']),
                            hex_to_rgb(COLORS['accent_highlight']),
                            intensity * 1.5
                        )
                        draw.ellipse(
                            [(px - node_size, py - node_size), 
                             (px + node_size, py + node_size)],
                            fill=node_color
                        )
    
    # ========== 变体 2: 树枝状分叉线 ==========
    def draw_branch_lines(self, draw, intensity=0.06):
        """树枝状 - 分叉结构"""
        def draw_branch(x, y, angle, length, depth, max_depth):
            if depth > max_depth or length < 5:
                return
            
            # 计算终点，带随机弯曲
            end_x = x + int(length * math.cos(angle))
            end_y = y + int(length * math.sin(angle))
            
            # 添加弯曲点
            mid_x = (x + end_x) // 2 + random.randint(-10, 10)
            mid_y = (y + end_y) // 2 + random.randint(-10, 10)
            
            # 绘制线段
            width = max(1, 3 - depth)  # 越细分越细
            color = blend_color(
                hex_to_rgb(COLORS['bg_primary']),
                hex_to_rgb(COLORS['accent_primary']),
                intensity * (1 - depth / max_depth * 0.5)
            )
            draw.line([(x, y), (mid_x, mid_y), (end_x, end_y)], fill=color, width=width)
            
            # 递归分叉
            if random.random() < 0.7:  # 70%概率分叉
                new_angle1 = angle + random.uniform(0.3, 0.8)
                new_length1 = length * random.uniform(0.5, 0.8)
                draw_branch(end_x, end_y, new_angle1, new_length1, depth + 1, max_depth)
            
            if random.random() < 0.5:  # 50%概率第二分叉
                new_angle2 = angle - random.uniform(0.3, 0.8)
                new_length2 = length * random.uniform(0.4, 0.7)
                draw_branch(end_x, end_y, new_angle2, new_length2, depth + 1, max_depth)
        
        # 生成多个树枝
        for _ in range(12):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(60, 120)
            draw_branch(x, y, angle, length, 0, random.randint(3, 5))
    
    # ========== 变体 3: 明亮细线条 ==========
    def draw_bright_thin_lines(self, draw, intensity=0.15):
        """明亮的极细线条"""
        for i in range(40):
            # 随机曲线
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            points = []
            segment_length = random.randint(100, 300)
            
            for j in range(segment_length):
                # 布朗运动式随机 walk
                x += random.randint(-3, 3)
                y += random.randint(-2, 2)
                x = max(0, min(self.width, x))
                y = max(0, min(self.height, y))
                
                if j % 3 == 0:  # 每3个点采样一个
                    points.append((x, y))
            
            if len(points) > 1:
                width = 1  # 始终保持1像素细线
                # 更明亮的颜色
                color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_highlight']),
                    intensity * random.uniform(0.5, 1.0)
                )
                draw.line(points, fill=color, width=width)
    
    # ========== 变体 4: 有机流动细线 ==========
    def draw_organic_flow(self, draw, intensity=0.07):
        """有机流动 - 类藤蔓"""
        for i in range(30):
            # 起点
            start_x = random.randint(0, self.width)
            start_y = random.randint(0, self.height)
            
            x, y = start_x, start_y
            points = [(x, y)]
            
            # 控制点生成有机曲线
            for _ in range(random.randint(5, 12)):
                # 使用噪声般的随机
                dx = random.randint(-60, 60)
                dy = random.randint(-40, 40)
                
                # 贝塞尔曲线中间点
                mid_x = x + dx // 2 + random.randint(-15, 15)
                mid_y = y + dy // 2 + random.randint(-15, 15)
                
                # 细分曲线
                for t in [0.2, 0.4, 0.6, 0.8]:
                    px = int((1-t)**2 * x + 2*(1-t)*t * mid_x + t**2 * (x + dx))
                    py = int((1-t)**2 * y + 2*(1-t)*t * mid_y + t**2 * (y + dy))
                    points.append((px, py))
                
                x += dx
                y += dy
            
            if len(points) > 1:
                # 线宽变化 - 有粗有细
                base_width = random.choice([1, 1, 1, 2])
                color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_secondary']),
                    intensity
                )
                
                # 分段绘制，每段不同粗细
                for j in range(len(points) - 1):
                    w = base_width if random.random() < 0.7 else base_width + 1
                    draw.line([points[j], points[j+1]], fill=color, width=w)
                
                # 随机添加膨胀节点（小瘤子）
                for j in range(1, len(points) - 1, random.randint(2, 5)):
                    if random.random() < 0.3:
                        px, py = points[j]
                        size = random.randint(2, 4)
                        draw.ellipse(
                            [(px-size, py-size), (px+size, py+size)],
                            fill=color
                        )
    
    # ========== 变体 5: 综合混合 ==========
    def draw_mixed_style(self, draw):
        """混合多种风格"""
        # 30% 蛇形线
        self.draw_snake_lines(draw, intensity=0.05)
        # 30% 树枝
        self.draw_branch_lines(draw, intensity=0.04)
        # 20% 明亮细线
        self.draw_bright_thin_lines(draw, intensity=0.08)
        # 20% 有机流动
        self.draw_organic_flow(draw, intensity=0.05)
    
    # ========== 公共绘制方法 ==========
    def draw_ui(self, draw):
        """绘制UI元素"""
        # 标题栏
        self._draw_title_bar(draw)
        # 左侧面板
        left_w = self._draw_left_panel(draw)
        # 标签栏
        self._draw_tab_bar(draw, left_w)
        # 编辑区
        self._draw_editor_area(draw, left_w)
        # 右侧面板
        self._draw_right_panel(draw)
        # 命令栏
        self._draw_command_bar(draw, left_w)
        # 状态栏
        self._draw_status_bar(draw)
    
    def _draw_title_bar(self, draw):
        title_height = 38
        draw.rectangle([(0, 0), (self.width, title_height)], 
                      fill=hex_to_rgb(COLORS['bg_secondary']))
        
        # 红绿灯按钮
        for x, color in [(20, COLORS['traffic_red']), (40, COLORS['traffic_yellow']), (60, COLORS['traffic_green'])]:
            draw.ellipse([(x-6, 13), (x+6, 25)], fill=hex_to_rgb(color))
        
        draw.text((650, 10), "Golden Editor", font=self.font_medium, 
                 fill=hex_to_rgb(COLORS['text_secondary']))
    
    def _draw_left_panel(self, draw):
        panel_w, panel_y, panel_h = 220, 38, self.height - 58
        draw.rectangle([(0, panel_y), (panel_w, panel_y + panel_h)],
                      fill=hex_to_rgb(COLORS['bg_secondary']))
        
        draw.text((15, panel_y + 15), "EXPLORER", font=self.font_small,
                 fill=hex_to_rgb(COLORS['text_muted']))
        
        files = [("📁  src", 0), ("  🟨  main.js", 1, True), ("  📄  utils.js", 1), 
                ("  📄  config.js", 1), ("📁  tests", 0), ("  📄  test.js", 1), ("📄  README.md", 0)]
        
        y = panel_y + 45
        for item in files:
            filename, level = item[0], item[1]
            is_active = item[2] if len(item) > 2 else False
            x = 15 + level * 15
            
            if is_active:
                draw.rectangle([(0, y-3), (panel_w, y+22)], fill=hex_to_rgb(COLORS['bg_tertiary']))
                draw.line([(0, y-3), (0, y+22)], fill=hex_to_rgb(COLORS['accent_primary']), width=3)
                color = COLORS['text_primary']
            else:
                color = COLORS['text_secondary']
            
            draw.text((x, y), filename, font=self.font_medium, fill=hex_to_rgb(color))
            y += 28
        
        return panel_w
    
    def _draw_tab_bar(self, draw, left_w):
        tab_y, tab_h = 38, 36
        draw.rectangle([(left_w, tab_y), (self.width - 280, tab_y + tab_h)],
                      fill=hex_to_rgb(COLORS['bg_primary']))
        
        tabs = [("main.js", True), ("utils.js", False), ("config.js", False)]
        x = left_w + 10
        for name, active in tabs:
            if active:
                draw.rectangle([(x, tab_y+5), (x+110, tab_y+tab_h)], 
                             fill=hex_to_rgb(COLORS['bg_secondary']))
                draw.line([(x, tab_y+5), (x+110, tab_y+5)], 
                         fill=hex_to_rgb(COLORS['accent_primary']), width=3)
                color = COLORS['text_primary']
            else:
                color = COLORS['text_secondary']
            
            draw.text((x+12, tab_y+12), name, font=self.font_medium, fill=hex_to_rgb(color))
            draw.text((x+90, tab_y+10), "×", font=self.font_medium, fill=hex_to_rgb(COLORS['text_muted']))
            x += 115
    
    def _draw_editor_area(self, draw, left_w):
        editor_y, editor_h = 74, self.height - 140
        right_w = 280
        
        draw.rectangle([(left_w, editor_y), (self.width - right_w, editor_y + editor_h)],
                      fill=hex_to_rgb(COLORS['bg_primary']))
        
        # 行号区
        draw.rectangle([(left_w, editor_y), (left_w + 60, editor_y + editor_h)],
                      fill=hex_to_rgb(COLORS['bg_primary']))
        
        # 代码
        lines = [
            ("1", "import { useState } from 'react';", False),
            ("2", "", False),
            ("3", "function App() {", False),
            ("4", "  const [count, setCount] = useState(0);", True),
            ("5", "", False),
            ("6", "  return (", False),
            ("7", "    <div className='app'>", False),
            ("8", "      <h1>Hello World</h1>", False),
            ("9", "      <p>Count: {count}</p>", False),
            ("10", "    </div>", False),
            ("11", "  );", False),
            ("12", "}", False),
            ("13", "", False),
            ("14", "export default App;", False),
        ]
        
        y = editor_y + 20
        for num, code, current in lines:
            if current:
                draw.rectangle([(left_w, y-3), (self.width - right_w, y+24)],
                             fill=hex_to_rgb('#1E293B'))
                draw.line([(left_w, y-3), (left_w, y+24)],
                         fill=hex_to_rgb(COLORS['accent_primary']), width=4)
            
            draw.text((left_w + 45, y), num, font=self.font_small,
                     fill=hex_to_rgb(COLORS['accent_primary'] if current else COLORS['text_muted']))
            
            color = '#F59E0B' if code.startswith(('import', 'function')) else (COLORS['text_primary'] if current else COLORS['text_secondary'])
            draw.text((left_w + 75, y), code, font=self.font_code, fill=hex_to_rgb(color))
            y += 26
    
    def _draw_right_panel(self, draw):
        panel_x, panel_y = self.width - 280, 74
        panel_h = self.height - 140
        
        draw.rectangle([(panel_x, panel_y), (self.width, panel_y + panel_h)],
                      fill=hex_to_rgb(COLORS['bg_secondary']))
        draw.line([(panel_x, panel_y), (panel_x, panel_y + panel_h)],
                 fill=hex_to_rgb(COLORS['accent_primary']), width=2)
        
        draw.text((panel_x + 15, panel_y + 15), "CONTEXT", font=self.font_small,
                 fill=hex_to_rgb(COLORS['text_muted']))
        
        # AI卡片
        draw.rectangle([(panel_x + 10, panel_y + 45), (self.width - 10, panel_y + 120)],
                      fill=hex_to_rgb(COLORS['bg_tertiary']),
                      outline=hex_to_rgb(COLORS['accent_primary']), width=1)
        draw.text((panel_x + 20, panel_y + 60), "🤖 AI Assistant", font=self.font_medium,
                 fill=hex_to_rgb(COLORS['accent_primary']))
    
    def _draw_command_bar(self, draw, left_w):
        bar_y = self.height - 66
        right_w = 280
        
        draw.rectangle([(left_w, bar_y), (self.width - right_w, bar_y + 46)],
                      fill=hex_to_rgb(COLORS['bg_secondary']))
        draw.line([(left_w, bar_y), (self.width - right_w, bar_y)],
                 fill=hex_to_rgb(COLORS['bg_tertiary']), width=1)
        
        # 水流特效
        for i in range(10):
            x = left_w + 50 + i * 80
            y = bar_y + 3
            for r in range(4, 0, -1):
                color = blend_color(hex_to_rgb(COLORS['bg_secondary']),
                                  hex_to_rgb(COLORS['accent_highlight']), 0.5/r)
                draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color)
        
        draw.text((left_w + 15, bar_y + 12), ">", font=self.font_large,
                 fill=hex_to_rgb(COLORS['accent_primary']))
        draw.text((left_w + 35, bar_y + 14), 'git commit -m "feat: add counter"',
                 font=self.font_medium, fill=hex_to_rgb(COLORS['text_primary']))
    
    def _draw_status_bar(self, draw):
        bar_y = self.height - 20
        draw.rectangle([(0, bar_y), (self.width, bar_y + 20)],
                      fill=hex_to_rgb(COLORS['accent_primary']))
        
        items = ["Ln 4, Col 15", "UTF-8", "JavaScript", "🌙 暗黑", "⎋ LEAP"]
        x = 15
        for item in items:
            draw.text((x, bar_y + 4), item, font=self.font_small, fill=hex_to_rgb('#0F172A'))
            bbox = draw.textbbox((0, 0), item, font=self.font_small)
            x += (bbox[2] - bbox[0]) + 25
    
    # ========== 生成各版本 ==========
    def generate_all(self):
        """生成所有变体"""
        variants = [
            ("variant1_snake", self.draw_snake_lines, 0.08),
            ("variant2_branch", self.draw_branch_lines, 0.06),
            ("variant3_bright", self.draw_bright_thin_lines, 0.15),
            ("variant4_organic", self.draw_organic_flow, 0.07),
            ("variant5_mixed", self.draw_mixed_style, None),
        ]
        
        for name, draw_fn, intensity in variants:
            img, draw = self.create_base()
            
            # 绘制背景线条
            if intensity:
                draw_fn(draw, intensity)
            else:
                draw_fn(draw)
            
            # 绘制UI
            self.draw_ui(draw)
            
            # 保存
            filename = f"macos_editor_{name}.png"
            img.save(filename)
            print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    editor = EditorVariant(seed=42)
    editor.generate_all()
