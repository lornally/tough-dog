#!/usr/bin/env python3
"""
延展更多炸裂风格 - 同时确保文字清晰可读
在文字区域降低纹理密度，使用半透明遮罩
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

COLORS = {
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'accent_primary': '#CA8A04',
    'accent_secondary': '#B45309',
    'accent_highlight': '#F59E0B',
    'accent_bright': '#FCD34D',
    'text_primary': '#E8F0FF',
}

class ExtendedStyles:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        # 文字区域定义 (x, y, w, h) - 这些区域纹理要稀疏
        self.text_zones = [
            (0, 0, 220, 900),      # 左侧 Explorer
            (220, 38, 900, 36),    # 标签栏
            (220, 74, 60, 760),    # 行号区
            (280, 74, 840, 760),   # 代码编辑区
            (1120, 74, 280, 760),  # 右侧 Context
            (220, 834, 900, 46),   # 命令栏
            (0, 880, 1400, 20),    # 状态栏
        ]
    
    def is_in_text_zone(self, x, y):
        """检查点是否在文字区域内"""
        for zx, zy, zw, zh in self.text_zones:
            if zx <= x <= zx + zw and zy <= y <= zy + zh:
                return True
        return False
    
    def create_base(self):
        img = Image.new('RGB', (self.width, self.height), hex_to_rgb(COLORS['bg_primary']))
        return img, ImageDraw.Draw(img)
    
    # ===== 风格11: 放射状/爆炸 =====
    def draw_explosion(self, draw):
        random.seed(1100)
        centers = [(300, 300), (1000, 200), (700, 600), (200, 700), (1200, 700)]
        
        for cx, cy in centers:
            for i in range(40):
                angle = (2 * math.pi / 40) * i + random.uniform(-0.1, 0.1)
                length = random.randint(100, 400)
                
                # 如果朝向文字区域，缩短长度
                end_x = cx + int(length * math.cos(angle))
                end_y = cy + int(length * math.sin(angle))
                
                if self.is_in_text_zone(end_x, end_y):
                    length = int(length * 0.3)
                    end_x = cx + int(length * math.cos(angle))
                    end_y = cy + int(length * math.sin(angle))
                
                # 锯齿状射线
                points = [(cx, cy)]
                segments = random.randint(3, 6)
                for j in range(segments):
                    t = (j + 1) / segments
                    px = cx + int(t * (end_x - cx)) + random.randint(-10, 10)
                    py = cy + int(t * (end_y - cy)) + random.randint(-10, 10)
                    points.append((px, py))
                
                brightness = random.uniform(0.4, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=random.choice([1, 1, 2]))
                
                # 端点发光
                if random.random() < 0.3:
                    draw.ellipse([(end_x-3, end_y-3), (end_x+3, end_y+3)], 
                                fill=hex_to_rgb(COLORS['accent_highlight']))
    
    # ===== 风格12: 螺旋星系 =====
    def draw_galaxy(self, draw):
        random.seed(1200)
        centers = [(400, 400), (1000, 500)]
        
        for cx, cy in centers:
            # 螺旋臂
            for arm in range(3):
                offset = arm * (2 * math.pi / 3)
                points = []
                
                for i in range(100):
                    angle = offset + i * 0.1
                    radius = 20 + i * 3
                    
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    
                    # 避开文字区
                    if self.is_in_text_zone(x, y):
                        continue
                    
                    points.append((x, y))
                    
                    # 星点
                    if random.random() < 0.2:
                        size = random.randint(1, 3)
                        brightness = random.uniform(0.5, 0.9)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                        draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
                
                if len(points) > 1:
                    brightness = random.uniform(0.3, 0.6)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格13: 水波纹/涟漪 =====
    def draw_ripple(self, draw):
        random.seed(1300)
        centers = [(200, 200), (600, 400), (1000, 300), (400, 700), (1100, 600)]
        
        for cx, cy in centers:
            for radius in range(30, 300, 25):
                points = []
                for angle in [i * 0.1 for i in range(63)]:
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    
                    # 波纹变形
                    x += int(10 * math.sin(angle * 5))
                    y += int(10 * math.cos(angle * 5))
                    
                    if not self.is_in_text_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 5:
                    alpha = max(0.2, 1 - radius / 300)
                    brightness = 0.5 * alpha
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                    
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格14: 羽毛/毛发 =====
    def draw_feather(self, draw):
        random.seed(1400)
        
        for _ in range(80):
            # 起点
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_text_zone(x, y):
                continue
            
            length = random.randint(50, 150)
            angle = random.uniform(0, 2 * math.pi)
            
            # 主茎
            main_points = [(x, y)]
            cx, cy = x, y
            
            for i in range(length // 5):
                cx += int(5 * math.cos(angle))
                cy += int(5 * math.sin(angle))
                angle += random.uniform(-0.1, 0.1)
                main_points.append((cx, cy))
            
            if len(main_points) > 3:
                brightness = random.uniform(0.4, 0.7)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                draw.line(main_points, fill=color, width=1)
                
                # 毛细分支
                for j in range(0, len(main_points), 3):
                    mx, my = main_points[j]
                    branch_angle = angle + random.uniform(-1.5, 1.5)
                    bl = random.randint(10, 25)
                    
                    bx = mx + int(bl * math.cos(branch_angle))
                    by = my + int(bl * math.sin(branch_angle))
                    
                    if not self.is_in_text_zone(bx, by):
                        brightness = random.uniform(0.3, 0.5)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                        draw.line([(mx, my), (bx, by)], fill=color, width=1)
    
    # ===== 风格15: 蛛网 =====
    def draw_spiderweb(self, draw):
        random.seed(1500)
        centers = [(300, 300), (1000, 400), (600, 700)]
        
        for cx, cy in centers:
            # 放射线
            for i in range(12):
                angle = (2 * math.pi / 12) * i
                length = 200
                
                points = [(cx, cy)]
                for r in range(0, length, 20):
                    x = cx + int(r * math.cos(angle))
                    y = cy + int(r * math.sin(angle))
                    if not self.is_in_text_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 1:
                    brightness = random.uniform(0.3, 0.6)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                    draw.line(points, fill=color, width=1)
            
            # 同心圆（变形）
            for radius in range(40, 220, 40):
                points = []
                for angle in [i * 0.05 for i in range(126)]:
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    
                    # 蛛网下垂变形
                    y += int(20 * math.sin(angle * 3))
                    
                    if not self.is_in_text_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 5:
                    brightness = random.uniform(0.25, 0.5)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格16: 电路板 =====
    def draw_circuit(self, draw):
        random.seed(1600)
        
        # 主干线
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_text_zone(x, y):
                continue
            
            # 水平或垂直
            if random.random() < 0.5:
                # 水平
                end_x = min(x + random.randint(100, 300), self.width)
                if not self.is_in_text_zone(end_x, y):
                    brightness = random.uniform(0.4, 0.7)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    draw.line([(x, y), (end_x, y)], fill=color, width=2)
                    
                    # 焊点
                    for px in range(x, end_x, 30):
                        if not self.is_in_text_zone(px, y) and random.random() < 0.5:
                            draw.ellipse([(px-2, y-2), (px+2, y+2)], 
                                        fill=hex_to_rgb(COLORS['accent_highlight']))
            else:
                # 垂直
                end_y = min(y + random.randint(100, 300), self.height)
                if not self.is_in_text_zone(x, end_y):
                    brightness = random.uniform(0.4, 0.7)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    draw.line([(x, y), (x, end_y)], fill=color, width=2)
        
        # 连接点
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            if not self.is_in_text_zone(x, y):
                size = random.randint(3, 6)
                brightness = random.uniform(0.6, 0.9)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
    
    # ===== 风格17: 水晶/棱镜 =====
    def draw_crystal(self, draw):
        random.seed(1700)
        
        for _ in range(25):
            # 多边形中心
            cx = random.randint(0, self.width)
            cy = random.randint(0, self.height)
            
            if self.is_in_text_zone(cx, cy):
                continue
            
            sides = random.choice([3, 4, 5, 6])
            radius = random.randint(30, 80)
            
            points = []
            for i in range(sides):
                angle = (2 * math.pi / sides) * i + random.uniform(-0.2, 0.2)
                x = cx + int(radius * math.cos(angle))
                y = cy + int(radius * math.sin(angle))
                points.append((x, y))
            
            points.append(points[0])  # 闭合
            
            brightness = random.uniform(0.3, 0.6)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
            draw.line(points, fill=color, width=1)
            
            # 内部对角线
            for i in range(sides):
                for j in range(i+2, sides):
                    if abs(i - j) > 1 and not (i == 0 and j == sides - 1):
                        if not self.is_in_text_zone(points[i][0], points[i][1]):
                            draw.line([points[i], points[j]], fill=color, width=1)
    
    # ===== 风格18: 熔岩流动 =====
    def draw_magma(self, draw):
        random.seed(1800)
        
        for _ in range(15):
            points = []
            x = random.randint(0, self.width)
            y = 0
            
            for _ in range(random.randint(20, 40)):
                x += random.randint(-20, 20)
                y += random.randint(10, 25)
                
                if y > self.height:
                    break
                
                if not self.is_in_text_zone(x, y):
                    points.append((x, y))
            
            if len(points) > 3:
                # 多层线条模拟流动
                for offset in range(-2, 3):
                    offset_points = [(px + offset, py) for px, py in points]
                    brightness = 0.8 - abs(offset) * 0.2
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    for j in range(len(offset_points) - 1):
                        draw.line([offset_points[j], offset_points[j+1]], fill=color, width=1)
    
    # ===== 风格19: 星轨 =====
    def draw_star_trails(self, draw):
        random.seed(1900)
        center_x, center_y = self.width // 2, self.height // 2
        
        for i in range(100):
            angle = random.uniform(0, 2 * math.pi)
            start_r = random.randint(100, 600)
            end_r = start_r - random.randint(20, 50)
            
            sx = center_x + int(start_r * math.cos(angle))
            sy = center_y + int(start_r * math.sin(angle))
            ex = center_x + int(end_r * math.cos(angle + 0.1))
            ey = center_y + int(end_r * math.sin(angle + 0.1))
            
            if not self.is_in_text_zone(sx, sy) and not self.is_in_text_zone(ex, ey):
                brightness = random.uniform(0.4, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                draw.line([(sx, sy), (ex, ey)], fill=color, width=1)
                
                # 星点
                if random.random() < 0.3:
                    draw.ellipse([(sx-2, sy-2), (sx+2, sy+2)], 
                                fill=hex_to_rgb(COLORS['accent_bright']))
    
    # ===== 风格20: 蒲公英种子 =====
    def draw_dandelion(self, draw):
        random.seed(2000)
        seeds = []
        
        # 种子头部
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_text_zone(x, y):
                continue
            
            seeds.append((x, y))
            
            # 种子
            size = random.randint(2, 4)
            brightness = random.uniform(0.6, 0.9)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
            draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
            
            # 绒毛
            for _ in range(random.randint(5, 10)):
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(20, 50)
                ex = x + int(length * math.cos(angle))
                ey = y + int(length * math.sin(angle))
                
                if not self.is_in_text_zone(ex, ey):
                    brightness = random.uniform(0.2, 0.5)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                    draw.line([(x, y), (ex, ey)], fill=color, width=1)
    
    def generate_all(self):
        styles = [
            ("extended1_explosion", self.draw_explosion),
            ("extended2_galaxy", self.draw_galaxy),
            ("extended3_ripple", self.draw_ripple),
            ("extended4_feather", self.draw_feather),
            ("extended5_spiderweb", self.draw_spiderweb),
            ("extended6_circuit", self.draw_circuit),
            ("extended7_crystal", self.draw_crystal),
            ("extended8_magma", self.draw_magma),
            ("extended9_startrails", self.draw_star_trails),
            ("extended10_dandelion", self.draw_dandelion),
        ]
        
        for name, draw_fn in styles:
            img, draw = self.create_base()
            draw_fn(draw)
            
            filename = f"macos_editor_{name}.png"
            img.save(filename)
            print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    styles = ExtendedStyles()
    styles.generate_all()
