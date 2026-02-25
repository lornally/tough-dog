#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器设计稿生成器 - V2
改进：有机流动条纹 + 明显的水流特效
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

# 设置随机种子以获得可重复的结果
random.seed(42)

# 暗黑金配色方案
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

def draw_organic_curve(draw, start_y, amplitude, frequency, color, width, phase=0):
    """绘制有机流动曲线"""
    points = []
    for x in range(0, 1401, 5):
        # 使用正弦波组合创造有机感
        y = start_y + amplitude * math.sin(frequency * x / 100 + phase)
        y += amplitude * 0.3 * math.sin(frequency * 2.3 * x / 100 + phase * 1.5)
        y += amplitude * 0.15 * math.sin(frequency * 0.7 * x / 100 + phase * 0.5)
        points.append((x, y))
    
    if len(points) > 1:
        draw.line(points, fill=color, width=width)

def draw_flowing_stream(draw, y_base, intensity=1.0):
    """绘制流动的水流光带"""
    # 主光带
    for i in range(5):
        alpha = int(200 * intensity * (1 - i/10))
        color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
        
        points = []
        for x in range(220, 1120, 3):
            # 波浪形流动
            wave = 3 * math.sin((x - 220) / 30 + i * 0.5)
            y = y_base + wave + i * 0.5
            points.append((x, y))
        
        if len(points) > 1:
            draw.line(points, fill=color, width=2)
    
    # 亮金高光点
    for x in range(260, 1100, 80):
        glow_x = x + int(30 * math.sin(x / 100))
        for r in range(3, 0, -1):
            alpha = int(150 * intensity / r)
            color = (*hex_to_rgb(COLORS['accent_highlight'])[:3],)
            draw.ellipse(
                [(glow_x - r, y_base - 2 - r), (glow_x + r, y_base - 2 + r)],
                fill=color
            )

def draw_gem_glow(draw, cx, cy, radius, color_hex, intensity=0.1):
    """绘制宝石光泽（无模糊）"""
    color = hex_to_rgb(color_hex)
    for r in range(radius, 0, -2):
        alpha = int(255 * intensity * (radius - r) / radius)
        if alpha > 0:
            # 使用纯色渐变而非模糊
            glow_color = tuple(min(255, c + alpha) for c in color)
            draw.ellipse(
                [(cx - r, cy - r), (cx + r, cy + r)],
                outline=glow_color,
                width=1
            )

class DarkGoldEditorV2:
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
    
    def draw_organic_stripes(self):
        """绘制有机流动的背景条纹"""
        # 使用多层不同频率的正弦波组合
        
        # 大范围的流动条纹
        for i in range(8):
            y_base = 100 + i * 100
            amplitude = 20 + i * 3
            frequency = 0.5 + i * 0.1
            phase = i * 0.8
            alpha = int(30 - i * 3)
            color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
            draw_organic_curve(self.draw, y_base, amplitude, frequency, color, 25, phase)
        
        # 中等频率的流动条纹
        for i in range(6):
            y_base = 150 + i * 130
            amplitude = 15 + i * 2
            frequency = 0.8 + i * 0.15
            phase = i * 1.2 + 2
            color = (*hex_to_rgb(COLORS['accent_secondary'])[:3],)
            draw_organic_curve(self.draw, y_base, amplitude, frequency, color, 15, phase)
        
        # 细密的流动条纹
        for i in range(10):
            y_base = 80 + i * 85
            amplitude = 8 + i * 1.5
            frequency = 1.2 + i * 0.2
            phase = i * 0.6 + 1
            color = (*hex_to_rgb(COLORS['accent_highlight'])[:3],)
            draw_organic_curve(self.draw, y_base, amplitude, frequency, color, 5, phase)
        
        # 垂直方向的流动感
        for i in range(5):
            x_base = 200 + i * 250
            points = []
            for y in range(0, 900, 5):
                wave = 30 * math.sin(y / 80 + i * 1.5)
                x = x_base + wave
                points.append((x, y))
            if len(points) > 1:
                color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
                self.draw.line(points, fill=color, width=40)
    
    def draw_title_bar(self):
        """绘制标题栏（含红绿灯按钮）"""
        title_height = 38
        
        # 标题栏背景
        self.draw.rectangle(
            [(0, 0), (self.width, title_height)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 有机纹理覆盖
        for i in range(3):
            y = 10 + i * 12
            amplitude = 5
            frequency = 1.5
            phase = i * 2
            color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
            draw_organic_curve(self.draw, y, amplitude, frequency, color, 15, phase)
        
        # 红绿灯按钮
        button_y = 19
        button_radius = 6
        buttons = [
            (20, COLORS['traffic_red']),
            (40, COLORS['traffic_yellow']),
            (60, COLORS['traffic_green'])
        ]
        
        for x, color in buttons:
            # 按钮外圈
            self.draw.ellipse(
                [(x - button_radius - 1, button_y - button_radius - 1),
                 (x + button_radius + 1, button_y + button_radius + 1)],
                fill=hex_to_rgb(COLORS['bg_primary'])
            )
            # 按钮主体
            self.draw.ellipse(
                [(x - button_radius, button_y - button_radius),
                 (x + button_radius, button_y + button_radius)],
                fill=hex_to_rgb(color)
            )
            # 宝石光泽效果
            draw_gem_glow(self.draw, x, button_y, button_radius + 3, color, 0.15)
        
        # 窗口标题
        title = "Golden Editor"
        bbox = self.draw.textbbox((0, 0), title, font=self.font_medium)
        title_w = bbox[2] - bbox[0]
        self.draw.text(
            ((self.width - title_w) // 2, 10),
            title,
            font=self.font_medium,
            fill=hex_to_rgb(COLORS['text_secondary'])
        )
    
    def draw_left_panel(self):
        """绘制左侧空间导航面板"""
        panel_width = 220
        panel_x = 0
        panel_y = 38
        panel_h = self.height - 38 - 20
        
        # 面板背景
        self.draw.rectangle(
            [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 有机流动纹理
        for i in range(5):
            y_base = 60 + i * 150
            amplitude = 25
            frequency = 0.6 + i * 0.1
            phase = i * 1.5
            width = 220
            
            points = []
            for x in range(0, 221, 3):
                y = y_base + amplitude * math.sin(frequency * x / 30 + phase)
                y += amplitude * 0.4 * math.sin(frequency * 2.1 * x / 30 + phase * 1.3)
                points.append((x, y))
            
            if len(points) > 1:
                color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
                self.draw.line(points, fill=color, width=30)
        
        # 垂直流动条纹
        for i in range(3):
            x_base = 30 + i * 70
            points = []
            for y in range(38, panel_h + 38, 5):
                wave = 20 * math.sin((y - 38) / 60 + i * 2)
                x = x_base + wave
                points.append((x, y))
            if len(points) > 1:
                color = (*hex_to_rgb(COLORS['accent_highlight'])[:3],)
                self.draw.line(points, fill=color, width=25)
        
        # 面板标题
        self.draw.text(
            (15, panel_y + 15),
            "EXPLORER",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_muted'])
        )
        
        # 文件树
        files = [
            ("📁  src", 0),
            ("  🟨  main.js", 1, True),
            ("  📄  utils.js", 1, False),
            ("  📄  config.js", 1, False),
            ("📁  tests", 0, False),
            ("  📄  test.js", 1, False),
            ("📄  README.md", 0, False),
        ]
        
        y = panel_y + 45
        for item in files:
            filename = item[0]
            level = item[1]
            is_active = item[2] if len(item) > 2 else False
            
            x = 15 + level * 15
            
            if is_active:
                # 选中项高亮
                self.draw.rectangle(
                    [(0, y - 3), (panel_width, y + 22)],
                    fill=hex_to_rgb(COLORS['bg_tertiary'])
                )
                # 金边高亮
                self.draw.line(
                    [(0, y - 3), (0, y + 22)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=3
                )
                # 宝石光泽
                draw_gem_glow(self.draw, 20, y + 10, 15, COLORS['accent_primary'], 0.2)
                text_color = COLORS['text_primary']
            else:
                text_color = COLORS['text_secondary']
            
            self.draw.text((x, y), filename, font=self.font_medium, fill=hex_to_rgb(text_color))
            y += 28
        
        return panel_width
    
    def draw_tab_bar(self, left_w):
        """绘制标签栏"""
        tab_y = 38
        tab_h = 36
        
        # 标签栏背景
        self.draw.rectangle(
            [(left_w, tab_y), (self.width - 280, tab_y + tab_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 有机纹理
        for i in range(2):
            y = tab_y + 10 + i * 10
            amplitude = 4
            frequency = 2
            phase = i * 3
            color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
            points = [(x, y + amplitude * math.sin(frequency * x / 100 + phase)) 
                     for x in range(left_w, self.width - 280, 5)]
            if len(points) > 1:
                self.draw.line(points, fill=color, width=8)
        
        # 标签
        tabs = [
            ("main.js", True),
            ("utils.js", False),
            ("config.js", False),
        ]
        
        x = left_w + 10
        for tab_name, is_active in tabs:
            tab_w = 110
            
            if is_active:
                # 选中标签背景
                self.draw.rectangle(
                    [(x, tab_y + 5), (x + tab_w, tab_y + tab_h)],
                    fill=hex_to_rgb(COLORS['bg_secondary'])
                )
                # 顶部金边
                self.draw.line(
                    [(x, tab_y + 5), (x + tab_w, tab_y + 5)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=3
                )
                # 宝石光泽
                draw_gem_glow(self.draw, x + tab_w//2, tab_y + 5, tab_w//2, COLORS['accent_primary'], 0.15)
                text_color = COLORS['text_primary']
            else:
                text_color = COLORS['text_secondary']
            
            # 标签文字
            self.draw.text((x + 12, tab_y + 12), tab_name, font=self.font_medium, fill=hex_to_rgb(text_color))
            
            # 关闭按钮
            self.draw.text((x + tab_w - 20, tab_y + 10), "×", font=self.font_medium, fill=hex_to_rgb(COLORS['text_muted']))
            
            x += tab_w + 5
        
        # 添加按钮
        self.draw.text((x + 5, tab_y + 8), "+", font=self.font_large, fill=hex_to_rgb(COLORS['text_secondary']))
    
    def draw_editor_area(self, left_w):
        """绘制代码编辑区"""
        editor_y = 74
        editor_h = self.height - editor_y - 66
        right_panel_w = 280
        
        # 编辑区背景
        self.draw.rectangle(
            [(left_w, editor_y), (self.width - right_panel_w, editor_y + editor_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 有机背景纹理
        for i in range(4):
            y_base = editor_y + 100 + i * 150
            amplitude = 30
            frequency = 0.4 + i * 0.1
            phase = i * 2
            color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
            points = [(x, y_base + amplitude * math.sin(frequency * (x - left_w) / 100 + phase)) 
                     for x in range(left_w, self.width - right_panel_w, 5)]
            if len(points) > 1:
                self.draw.line(points, fill=color, width=60)
        
        # 行号区
        line_num_w = 60
        self.draw.rectangle(
            [(left_w, editor_y), (left_w + line_num_w, editor_y + editor_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 代码内容
        code_lines = [
            ("1", "import { useState } from 'react';", False),
            ("2", "", False),
            ("3", "function App() {", False),
            ("4", "  const [count, setCount] = useState(0);", True),
            ("5", "", False),
            ("6", "  return (", False),
            ("7", "    <div className=\"app\">", False),
            ("8", "      <h1>Hello World</h1>", False),
            ("9", "      <p>Count: {count}</p>", False),
            ("10", "      <button onClick={() => setCount(c + 1)}>", False),
            ("11", "        Increment", False),
            ("12", "      </button>", False),
            ("13", "    </div>", False),
            ("14", "  );", False),
            ("15", "}", False),
            ("16", "", False),
            ("17", "export default App;", False),
        ]
        
        y = editor_y + 20
        for line_num, code, is_current in code_lines:
            # 当前行金边高亮
            if is_current:
                self.draw.rectangle(
                    [(left_w, y - 3), (self.width - right_panel_w, y + 24)],
                    fill=hex_to_rgb('#1E293B')
                )
                # 左金边
                self.draw.line(
                    [(left_w, y - 3), (left_w, y + 24)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=4
                )
                # 水流光带效果
                for offset in range(0, 600, 150):
                    for r in range(3, 0, -1):
                        alpha = int(100 / r)
                        color = tuple(min(255, c + alpha) for c in hex_to_rgb(COLORS['accent_primary']))
                        self.draw.ellipse(
                            [(left_w + 300 + offset - r, y + 8 - r), 
                             (left_w + 300 + offset + 20 + r, y + 8 + r)],
                            outline=color,
                            width=1
                        )
                # 宝石光泽
                draw_gem_glow(self.draw, left_w + 100, y + 10, 50, COLORS['accent_primary'], 0.1)
            
            # 行号
            self.draw.text(
                (left_w + 45, y),
                line_num,
                font=self.font_small,
                fill=hex_to_rgb(COLORS['accent_primary'] if is_current else COLORS['text_muted'])
            )
            
            # 代码
            code_x = left_w + 75
            if code.startswith("import"):
                parts = code.split('{')
                self.draw.text((code_x, y), parts[0], font=self.font_code, fill=hex_to_rgb('#F59E0B'))
                if len(parts) > 1:
                    self.draw.text((code_x + 60, y), '{' + parts[1], font=self.font_code, fill=hex_to_rgb(COLORS['text_secondary']))
            elif code.startswith("function"):
                self.draw.text((code_x, y), "function", font=self.font_code, fill=hex_to_rgb('#F59E0B'))
                self.draw.text((code_x + 75, y), " App() {", font=self.font_code, fill=hex_to_rgb(COLORS['text_primary']))
            elif is_current:
                self.draw.text((code_x, y), code, font=self.font_code, fill=hex_to_rgb(COLORS['text_primary']))
            else:
                self.draw.text((code_x, y), code, font=self.font_code, fill=hex_to_rgb(COLORS['text_secondary']))
            
            y += 26
    
    def draw_right_panel(self):
        """绘制右侧面板"""
        panel_w = 280
        panel_x = self.width - panel_w
        panel_y = 74
        panel_h = self.height - panel_y - 66
        
        # 面板背景
        self.draw.rectangle(
            [(panel_x, panel_y), (self.width, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 有机流动纹理
        for i in range(4):
            x_base = panel_x + 30 + i * 60
            points = []
            for y in range(panel_y, panel_y + panel_h, 5):
                wave = 25 * math.sin((y - panel_y) / 50 + i * 1.8)
                x = x_base + wave
                points.append((x, y))
            if len(points) > 1:
                color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
                self.draw.line(points, fill=color, width=35)
        
        # 左金边
        self.draw.line(
            [(panel_x, panel_y), (panel_x, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['accent_primary']),
            width=2
        )
        
        # 面板标题
        self.draw.text(
            (panel_x + 15, panel_y + 15),
            "CONTEXT",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_muted'])
        )
        
        # AI 建议区域
        y = panel_y + 45
        self.draw.rectangle(
            [(panel_x + 10, y), (self.width - 10, y + 120)],
            fill=hex_to_rgb(COLORS['bg_tertiary']),
            outline=hex_to_rgb(COLORS['accent_primary']),
            width=1
        )
        
        # AI 图标
        self.draw.text(
            (panel_x + 20, y + 15),
            "🤖 AI Assistant",
            font=self.font_medium,
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        self.draw.text(
            (panel_x + 20, y + 45),
            "useState is a React Hook\nthat lets you add state to\nfunctional components.",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_secondary'])
        )
        
        # 装饰性流动线条
        for i in range(3):
            y_line = y + 140 + i * 80
            points = []
            for x in range(panel_x + 10, self.width - 10, 5):
                wave = 10 * math.sin((x - panel_x) / 40 + i)
                points.append((x, y_line + wave))
            if len(points) > 1:
                color = (*hex_to_rgb(COLORS['accent_highlight'])[:3],)
                self.draw.line(points, fill=color, width=2)
    
    def draw_command_bar(self, left_w):
        """绘制底部命令栏（含明显的水流特效）"""
        bar_y = self.height - 66
        bar_h = 46
        right_panel_w = 280
        
        # 命令栏背景
        self.draw.rectangle(
            [(left_w, bar_y), (self.width - right_panel_w, bar_y + bar_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 顶部边框
        self.draw.line(
            [(left_w, bar_y), (self.width - right_panel_w, bar_y)],
            fill=hex_to_rgb(COLORS['bg_tertiary']),
            width=1
        )
        
        # 明显的水流光带效果
        draw_flowing_stream(self.draw, bar_y + 2, 1.0)
        
        # 额外的流动光点
        for i in range(8):
            x = 300 + i * 100 + int(20 * math.sin(i * 1.5))
            for r in range(4, 0, -1):
                alpha = int(200 / r)
                color = tuple(min(255, c + alpha) for c in hex_to_rgb(COLORS['accent_highlight']))
                self.draw.ellipse(
                    [(x - r, bar_y + 3 - r), (x + r, bar_y + 3 + r)],
                    fill=color
                )
        
        # 命令提示符
        self.draw.text(
            (left_w + 15, bar_y + 12),
            ">",
            font=self.font_large,
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        # 输入文本
        self.draw.text(
            (left_w + 35, bar_y + 14),
            "git commit -m \"feat: add counter\"",
            font=self.font_medium,
            fill=hex_to_rgb(COLORS['text_primary'])
        )
        
        # 光标（闪烁效果用静态表示）
        cursor_x = left_w + 320
        self.draw.rectangle(
            [(cursor_x, bar_y + 14), (cursor_x + 2, bar_y + 32)],
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        # 光标宝石光泽
        draw_gem_glow(self.draw, cursor_x + 1, bar_y + 23, 5, COLORS['accent_primary'], 0.3)
    
    def draw_status_bar(self):
        """绘制状态栏"""
        bar_y = self.height - 20
        bar_h = 20
        
        # 状态栏背景
        self.draw.rectangle(
            [(0, bar_y), (self.width, bar_y + bar_h)],
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        # 有机底部纹理
        for i in range(3):
            y = bar_y - 5 + i * 5
            amplitude = 3
            frequency = 3
            phase = i * 4
            color = (*hex_to_rgb('#0F172A')[:3],)
            points = [(x, y + amplitude * math.sin(frequency * x / 100 + phase)) 
                     for x in range(0, self.width, 5)]
            if len(points) > 1:
                self.draw.line(points, fill=color, width=3)
        
        # 状态信息
        status_items = [
            "Ln 4, Col 15",
            "UTF-8",
            "JavaScript",
            "🌙 暗黑",
            "⎋ LEAP"
        ]
        
        x = 15
        for item in status_items:
            bbox = self.draw.textbbox((0, 0), item, font=self.font_small)
            text_w = bbox[2] - bbox[0]
            self.draw.text((x, bar_y + 4), item, font=self.font_small, fill=hex_to_rgb('#0F172A'))
            x += text_w + 25
    
    def render(self):
        """绘制完整编辑器"""
        # 1. 有机背景条纹
        self.draw_organic_stripes()
        
        # 2. 标题栏
        self.draw_title_bar()
        
        # 3. 左侧面板
        left_w = self.draw_left_panel()
        
        # 4. 标签栏
        self.draw_tab_bar(left_w)
        
        # 5. 编辑区
        self.draw_editor_area(left_w)
        
        # 6. 右侧面板
        self.draw_right_panel()
        
        # 7. 命令栏
        self.draw_command_bar(left_w)
        
        # 8. 状态栏
        self.draw_status_bar()
        
        return self.img
    
    def save(self, filename="macos_editor_dark_gold_v2.png"):
        """保存图片"""
        self.img.save(filename)
        print(f"✅ 设计稿 V2 已保存: {filename}")
        return filename

if __name__ == "__main__":
    editor = DarkGoldEditorV2()
    editor.render()
    editor.save()
