#!/usr/bin/env python3
"""
暗黑金风格 macOS 编辑器设计稿生成器
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 暗黑金配色方案
COLORS = {
    'bg_primary': '#0F172A',      # 深空黑
    'bg_secondary': '#1E293B',    # 次级背景
    'bg_tertiary': '#334155',     # 面板背景
    'accent_primary': '#CA8A04',  # 暗黑金
    'accent_secondary': '#B45309', # 深金
    'accent_highlight': '#F59E0B', # 亮金
    'text_primary': '#E8F0FF',    # 主文本
    'text_secondary': '#94A3B8',  # 次要文本
    'text_muted': '#64748B',      # 弱化文本
    'traffic_red': '#FF5F57',     # 关闭按钮
    'traffic_yellow': '#FFBD2E',  # 最小化按钮
    'traffic_green': '#28CA42',   # 全屏按钮
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class DarkGoldEditor:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        self.img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_primary']))
        self.draw = ImageDraw.Draw(self.img)
        
        # 尝试加载字体
        try:
            self.font_large = ImageFont.truetype("/System/Library/Fonts/SFProDisplay-Regular.otf", 16)
            self.font_medium = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 13)
            self.font_small = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 11)
            self.font_code = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        except:
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_code = ImageFont.load_default()
    
    def draw_gem_pattern(self, x, y, w, h):
        """绘制丝状宝石光泽纹理"""
        spacing = 20
        for i in range(0, w + h, spacing):
            alpha = 15
            color = (*hex_to_rgb(COLORS['accent_primary'])[:3], alpha)
            # 45度角线条
            self.draw.line([
                (x + i, y),
                (x + i - h, y + h)
            ], fill=color[:3], width=1)
    
    def draw_title_bar(self):
        """绘制标题栏（含红绿灯按钮）"""
        title_height = 38
        
        # 标题栏背景
        self.draw.rectangle(
            [(0, 0), (self.width, title_height)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 绘制宝石光泽纹理
        self.draw_gem_pattern(0, 0, self.width, title_height)
        
        # 红绿灯按钮
        button_y = 13
        button_radius = 6
        buttons = [
            (20, COLORS['traffic_red']),
            (40, COLORS['traffic_yellow']),
            (60, COLORS['traffic_green'])
        ]
        
        for x, color in buttons:
            # 按钮外圈（深色边框）
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
        panel_h = self.height - 38 - 24  # 减去标题栏和状态栏
        
        # 面板背景
        self.draw.rectangle(
            [(panel_x, panel_y), (panel_x + panel_width, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 宝石光泽纹理
        self.draw_gem_pattern(panel_x, panel_y, panel_width, panel_h)
        
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
            ("  📄  main.js", 1),
            ("  📄  utils.js", 1),
            ("  📄  config.js", 1),
            ("📁  tests", 0),
            ("  📄  test.js", 1),
            ("📄  README.md", 0),
        ]
        
        y = panel_y + 45
        for filename, level in files:
            x = 15 + level * 15
            # 选中项高亮（main.js）
            if "main.js" in filename:
                self.draw.rectangle(
                    [(0, y - 3), (panel_width, y + 20)],
                    fill=hex_to_rgb(COLORS['bg_tertiary'])
                )
                # 金边高亮
                self.draw.line(
                    [(0, y - 3), (0, y + 20)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=2
                )
                text_color = COLORS['text_primary']
            else:
                text_color = COLORS['text_secondary']
            
            self.draw.text((x, y), filename, font=self.font_medium, fill=hex_to_rgb(text_color))
            y += 26
        
        return panel_width
    
    def draw_tab_bar(self, left_w):
        """绘制标签栏"""
        tab_y = 38
        tab_h = 36
        
        # 标签栏背景
        self.draw.rectangle(
            [(left_w, tab_y), (self.width, tab_y + tab_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 标签
        tabs = [
            ("main.js", True),   # 当前选中
            ("utils.js", False),
            ("config.js", False),
        ]
        
        x = left_w + 10
        for tab_name, is_active in tabs:
            tab_w = 100
            
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
                    width=2
                )
                text_color = COLORS['text_primary']
            else:
                text_color = COLORS['text_secondary']
            
            # 标签文字
            self.draw.text((x + 10, tab_y + 10), tab_name, font=self.font_medium, fill=hex_to_rgb(text_color))
            
            # 关闭按钮
            self.draw.text((x + tab_w - 18, tab_y + 9), "×", font=self.font_medium, fill=hex_to_rgb(COLORS['text_muted']))
            
            x += tab_w + 5
        
        # 添加按钮
        self.draw.text((x + 5, tab_y + 8), "+", font=self.font_large, fill=hex_to_rgb(COLORS['text_secondary']))
    
    def draw_editor_area(self, left_w):
        """绘制代码编辑区"""
        editor_y = 74  # 38 + 36
        editor_h = self.height - editor_y - 70  # 减去命令栏和状态栏
        
        # 编辑区背景
        self.draw.rectangle(
            [(left_w, editor_y), (self.width, editor_y + editor_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 行号区
        line_num_w = 50
        self.draw.rectangle(
            [(left_w, editor_y), (left_w + line_num_w, editor_y + editor_h)],
            fill=hex_to_rgb(COLORS['bg_primary'])
        )
        
        # 代码内容
        code_lines = [
            ("1", "import { useState } from 'react';", False),
            ("2", "", False),
            ("3", "function App() {", False),
            ("4", "  const [count, setCount] = useState(0);", True),  # 当前行
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
        
        y = editor_y + 15
        for line_num, code, is_current in code_lines:
            # 当前行金边高亮
            if is_current:
                self.draw.rectangle(
                    [(left_w, y - 2), (self.width - 280, y + 20)],
                    fill=hex_to_rgb('#1E293B')
                )
                # 左金边
                self.draw.line(
                    [(left_w, y - 2), (left_w, y + 20)],
                    fill=hex_to_rgb(COLORS['accent_primary']),
                    width=3
                )
                # 水流光带效果
                for i in range(0, self.width - 280 - left_w - 100, 200):
                    self.draw.line(
                        [(left_w + i, y + 9), (left_w + i + 50, y + 9)],
                        fill=hex_to_rgb(COLORS['accent_primary']),
                        width=1
                    )
            
            # 行号
            self.draw.text(
                (left_w + 35 - len(line_num) * 4, y),
                line_num,
                font=self.font_small,
                fill=hex_to_rgb(COLORS['text_muted'])
            )
            
            # 代码
            code_x = left_w + 65
            if code.startswith("import"):
                self.draw.text((code_x, y), "import", font=self.font_code, fill=hex_to_rgb('#F59E0B'))
                self.draw.text((code_x + 50, y), " { useState } from 'react';", font=self.font_code, fill=hex_to_rgb(COLORS['text_secondary']))
            elif code.startswith("function"):
                self.draw.text((code_x, y), "function", font=self.font_code, fill=hex_to_rgb('#F59E0B'))
                self.draw.text((code_x + 60, y), " App() {", font=self.font_code, fill=hex_to_rgb(COLORS['text_primary']))
            elif is_current:
                self.draw.text((code_x, y), code, font=self.font_code, fill=hex_to_rgb(COLORS['text_primary']))
            else:
                self.draw.text((code_x, y), code, font=self.font_code, fill=hex_to_rgb(COLORS['text_secondary']))
            
            y += 22
    
    def draw_right_panel(self):
        """绘制右侧面板"""
        panel_w = 280
        panel_x = self.width - panel_w
        panel_y = 74
        panel_h = self.height - panel_y - 70
        
        # 面板背景
        self.draw.rectangle(
            [(panel_x, panel_y), (self.width, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 宝石光泽
        self.draw_gem_pattern(panel_x, panel_y, panel_w, panel_h)
        
        # 左金边
        self.draw.line(
            [(panel_x, panel_y), (panel_x, panel_y + panel_h)],
            fill=hex_to_rgb(COLORS['accent_primary']),
            width=1
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
            [(panel_x + 10, y), (self.width - 10, y + 80)],
            fill=hex_to_rgb(COLORS['bg_tertiary'])
        )
        
        # AI 图标
        self.draw.text(
            (panel_x + 20, y + 10),
            "🤖 AI Assistant",
            font=self.font_medium,
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
        
        self.draw.text(
            (panel_x + 20, y + 35),
            "useState is a React Hook\nthat lets you add state\nto functional components.",
            font=self.font_small,
            fill=hex_to_rgb(COLORS['text_secondary'])
        )
    
    def draw_command_bar(self, left_w):
        """绘制底部命令栏（含水流特效）"""
        bar_y = self.height - 70
        bar_h = 46
        
        # 命令栏背景
        self.draw.rectangle(
            [(left_w, bar_y), (self.width - 280, bar_y + bar_h)],
            fill=hex_to_rgb(COLORS['bg_secondary'])
        )
        
        # 顶部边框
        self.draw.line(
            [(left_w, bar_y), (self.width - 280, bar_y)],
            fill=hex_to_rgb(COLORS['bg_tertiary']),
            width=1
        )
        
        # 水流光带效果
        stream_y = bar_y + 1
        for i in range(0, self.width - 280 - left_w, 300):
            # 光带
            gradient_w = 100
            for j in range(gradient_w):
                alpha = int(200 * (1 - abs(j - gradient_w/2) / (gradient_w/2)))
                color = (*hex_to_rgb(COLORS['accent_primary'])[:3],)
                if j % 2 == 0:
                    self.draw.point((left_w + i + j, stream_y), fill=color)
        
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
        cursor_x = left_w + 280
        self.draw.rectangle(
            [(cursor_x, bar_y + 14), (cursor_x + 2, bar_y + 30)],
            fill=hex_to_rgb(COLORS['accent_primary'])
        )
    
    def draw_status_bar(self):
        """绘制状态栏"""
        bar_y = self.height - 24
        bar_h = 24
        
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
            "◐ 暗黑",
            "⎋ LEAP"
        ]
        
        x = 15
        for item in status_items:
            # 背景色文字用深色
            self.draw.text((x, bar_y + 4), item, font=self.font_small, fill=(15, 23, 42))
            bbox = self.draw.textbbox((x, bar_y + 4), item, font=self.font_small)
            x += (bbox[2] - bbox[0]) + 30
    
    def render(self):
        """绘制完整编辑器"""
        # 1. 标题栏
        self.draw_title_bar()
        
        # 2. 左侧面板
        left_w = self.draw_left_panel()
        
        # 3. 标签栏
        self.draw_tab_bar(left_w)
        
        # 4. 编辑区
        self.draw_editor_area(left_w)
        
        # 5. 右侧面板
        self.draw_right_panel()
        
        # 6. 命令栏
        self.draw_command_bar(left_w)
        
        # 7. 状态栏
        self.draw_status_bar()
        
        return self.img
    
    def save(self, filename="macos_editor_dark_gold.png"):
        """保存图片"""
        self.img.save(filename)
        print(f"✅ 设计稿已保存: {filename}")
        return filename

if __name__ == "__main__":
    editor = DarkGoldEditor()
    editor.render()
    editor.save()
