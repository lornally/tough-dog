#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器设计稿生成器 - V3
改进：细腻的有机流动条纹 + 明显的水流特效
"""

from PIL import Image, ImageDraw, ImageFont
import math

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

def blend_color(color1, color2, alpha):
    """混合两种颜色"""
    return tuple(int(c1 * (1 - alpha) + c2 * alpha) for c1, c2 in zip(color1, color2))

class DarkGoldEditorV3:
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
    
    def draw_subtle_organic_stripes(self):
        """绘制细腻的有机流动条纹 - 不遮挡内容"""
        
        # 大范围的极淡流动背景（在最底层）
        for i in range(5):
            y_base = 150 + i * 180
            amplitude = 40
            frequency = 0.3
            phase = i * 1.2
            
            points = []
            for x in range(0, self.width, 10):
                y = y_base + amplitude * math.sin(frequency * x / 100 + phase)
                y += amplitude * 0.5 * math.sin(frequency * 1.7 * x / 100 + phase * 0.8)
                points.append((x, y))
            
            if len(points) > 1:
                # 极淡的金色，几乎不可见但营造氛围
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    0.03
                )
                self.draw.line(points, fill=stripe_color, width=80)
        
        # 中等频率的细条纹
        for i in range(8):
            y_base = 80 + i * 110
            amplitude = 25
            frequency = 0.5
            phase = i * 0.9
            
            points = []
            for x in range(0, self.width, 5):
                y = y_base + amplitude * math.sin(frequency * x / 80 + phase)
                y += amplitude * 0.3 * math.sin(frequency * 2.1 * x / 80 + phase * 1.1)
                points.append((x, y))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_secondary']),
                    0.05
                )
                self.draw.line(points, fill=stripe_color, width=30)
        
        # 细密的金丝线（装饰性）
        for i in range(12):
            y_base = 50 + i * 75
            amplitude = 15
            frequency = 0.8
            phase = i * 0.6
            
            points = []
            for x in range(0, self.width, 3):
                y = y_base + amplitude * math.sin(frequency * x / 60 + phase)
                points.append((x, y))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_highlight']),
                    0.06
                )
                self.draw.line(points, fill=stripe_color, width=3)
    
    def draw_title_bar(self):
        """绘制标题栏"""
        title_height = 38
        
        # 标题栏背景
        self.draw.rectangle(
            [(0, 0), (self.width, title_height)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 标题栏有机纹理（细腻）
        for i in range(3):
            y = 15 + i * 8
            points = []
            for x in range(0, self.width, 5):
                wave = 3 * math.sin(x / 80 + i * 2)
                points.append((x, y + wave))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    0.08
                )
                self.draw.line(points, fill=stripe_color, width=12)
        
        # 红绿灯按钮
        button_y = 19
        button_radius = 6
        buttons = [
            (20, COLORS['traffic_red']),
            (40, COLORS['traffic_yellow']),
            (60, COLORS['traffic_green'])
        ]
        
        for x, color in buttons:
            self.draw.ellipse(
                [(x - button_radius - 1, button_y - button_radius - 1),
                 (x + button_radius + 1, button_y + button_radius + 1)],
                fill=hex_to_rgb(COLORS['bg_primary'])
            )
            self.draw.ellipse(
                [(x - button_radius, button_y - button_radius),
                 (x + button_radius, button_y + button_radius)],
                fill=hex_to_rgb(color)
            )
        
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
        """绘制左侧面板"""
        panel_width = 220
        panel_x = 0
        panel_y = 38
        panel_h = self.height - 38 - 20
        
        # 面板背景
        self.draw.rectangle(
            [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 面板有机纹理（细腻流动）
        for i in range(4):
            x_base = 20 + i * 50
            points = []
            for y in range(panel_y, panel_y + panel_h, 5):
                wave = 30 * math.sin((y - panel_y) / 70 + i * 1.5)
                points.append((x_base + wave, y))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    0.05
                )
                self.draw.line(points, fill=stripe_color, width=40)
        
        # 水平流动线条
        for i in range(5):
            y_base = panel_y + 100 + i * 150
            points = []
            for x in range(0, panel_width, 3):
                wave = 20 * math.sin(x / 40 + i)
                points.append((x, y_base + wave))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_highlight']),
                    0.04
                )
                self.draw.line(points, fill=stripe_color, width=20)
        
        # 面板标题
        self.draw.text(
            (15, panel_y + 15),
            "EXPLORER",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_muted'])
        )
        
        # 文件树
        files = [
            ("📁  src", 0, False),
            ("  🟨  main.js", 1, True),
            ("  📄  utils.js", 1, False),
            ("  📄  config.js", 1, False),
            ("📁  tests", 0, False),
            ("  📄  test.js", 1, False),
            ("📄  README.md", 0, False),
        ]
        
        y = panel_y + 45
        for filename, level, is_active in files:
            x = 15 + level * 15
            
            if is_active:
                # 选中项高亮
                self.draw.rectangle(
                    [(0, y - 3), (panel_width, y + 22)],
                    fill=hex_to_rgb(COLORS['bg_tertiary'])
                )
                # 金边
                self.draw.line(
                    [(0, y - 3), (0, y + 22)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=3
                )
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
        right_w = 280
        
        # 标签栏背景
        self.draw.rectangle(
            [(left_w, tab_y), (self.width - right_w, tab_y + tab_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
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
                # 选中标签
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
                text_color = COLORS['text_primary']
            else:
                text_color = COLORS['text_secondary']
            
            self.draw.text((x + 12, tab_y + 12), tab_name, font=self.font_medium, fill=hex_to_rgb(text_color))
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
        
        # 编辑区有机纹理（极淡）
        for i in range(3):
            y_base = editor_y + 150 + i * 200
            points = []
            for x in range(left_w, self.width - right_panel_w, 10):
                wave = 40 * math.sin((x - left_w) / 120 + i * 1.5)
                points.append((x, y_base + wave))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_primary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    0.02
                )
                self.draw.line(points, fill=stripe_color, width=100)
        
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
            if is_current:
                # 当前行高亮
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
                # 水流光点效果
                for offset in [200, 400, 600]:
                    for r in range(3, 0, -1):
                        color = blend_color(
                            hex_to_rgb(COLORS['bg_tertiary']),
                            hex_to_rgb(COLORS['accent_primary']),
                            0.3 / r
                        )
                        self.draw.ellipse(
                            [(left_w + offset - r, y + 8 - r), 
                             (left_w + offset + 15 + r, y + 8 + r)],
                            outline=color,
                            width=1
                        )
            
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
                self.draw.text((code_x, y), "import", font=self.font_code, fill=hex_to_rgb('#F59E0B'))
                self.draw.text((code_x + 60, y), " { useState } from 'react';", font=self.font_code, fill=hex_to_rgb(COLORS['text_secondary']))
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
        
        # 面板有机纹理
        for i in range(3):
            x_base = panel_x + 40 + i * 80
            points = []
            for y in range(panel_y, panel_y + panel_h, 5):
                wave = 30 * math.sin((y - panel_y) / 60 + i * 2)
                points.append((x_base + wave, y))
            
            if len(points) > 1:
                stripe_color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    0.04
                )
                self.draw.line(points, fill=stripe_color, width=50)
        
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
        
        # AI 卡片
        y = panel_y + 45
        self.draw.rectangle(
            [(panel_x + 10, y), (self.width - 10, y + 120)],
            fill=hex_to_rgb(COLORS['bg_tertiary']),
            outline=hex_to_rgb(COLORS['accent_primary']),
            width=1
        )
        
        self.draw.text(
            (panel_x + 20, y + 15),
            "🤖 AI Assistant",
            font=self.font_medium,
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        self.draw.text(
            (panel_x + 20, y + 45),
            "useState is a React Hook that lets\nyou add state to functional components.",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_secondary'])
        )
    
    def draw_command_bar(self, left_w):
        """绘制命令栏 + 明显的水流特效"""
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
        
        # ===== 明显的水流光带效果 =====
        
        # 1. 主光带（波浪形）
        for i in range(3):
            points = []
            for x in range(left_w, self.width - right_panel_w, 2):
                # 波浪 + 流动感
                wave = 4 * math.sin((x - left_w) / 25 + i * 0.5)
                y = bar_y + 3 + wave + i * 0.5
                points.append((x, y))
            
            if len(points) > 1:
                # 渐变色带效果
                alpha = 0.6 - i * 0.15
                color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_primary']),
                    alpha
                )
                self.draw.line(points, fill=color, width=3)
        
        # 2. 流动的高光点
        for i in range(12):
            x = left_w + 50 + i * 70
            # 正弦波位置
            wave_y = 3 * math.sin((x - left_w) / 25)
            
            # 多层光点制造发光效果
            for r in range(5, 0, -1):
                alpha = 0.5 / r
                color = blend_color(
                    hex_to_rgb(COLORS['bg_secondary']),
                    hex_to_rgb(COLORS['accent_highlight']),
                    alpha
                )
                self.draw.ellipse(
                    [(x - r, bar_y + 3 + wave_y - r), 
                     (x + 3 + r, bar_y + 3 + wave_y + r)],
                    fill=color
                )
        
        # 3. 亮金细线
        points = []
        for x in range(left_w, self.width - right_panel_w, 3):
            wave = 2 * math.sin((x - left_w) / 40)
            points.append((x, bar_y + 3 + wave))
        
        if len(points) > 1:
            self.draw.line(points, fill=hex_to_rgb(COLORS['accent_highlight']), width=1)
        
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
        
        # 光标
        cursor_x = left_w + 320
        self.draw.rectangle(
            [(cursor_x, bar_y + 14), (cursor_x + 2, bar_y + 32)],
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
    
    def draw_status_bar(self):
        """绘制状态栏"""
        bar_y = self.height - 20
        bar_h = 20
        
        # 状态栏背景
        self.draw.rectangle(
            [(0, bar_y), (self.width, bar_y + bar_h)],
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
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
        self.draw_subtle_organic_stripes()
        
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
    
    def save(self, filename="macos_editor_dark_gold_v3.png"):
        """保存图片"""
        self.img.save(filename)
        print(f"✅ 设计稿 V3 已保存: {filename}")
        return filename

if __name__ == "__main__":
    editor = DarkGoldEditorV3()
    editor.render()
    editor.save()
