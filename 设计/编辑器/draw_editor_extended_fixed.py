#!/usr/bin/env python3
"""
延展风格修复版 - 确保纹理可见，同时避开主要文字区域
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

COLORS = {
    'bg_primary': '#0F172A',
    'accent_primary': '#CA8A04',
    'accent_secondary': '#B45309',
    'accent_highlight': '#F59E0B',
    'accent_bright': '#FCD34D',
}

class FixedExtendedStyles:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        # 只避开最核心的文字区域（代码编辑区）
        self.core_text_zone = (280, 100, 840, 750)  # 代码区
    
    def is_in_core_zone(self, x, y):
        """检查是否在核心文字区域"""
        zx, zy, zw, zh = self.core_text_zone
        return zx <= x <= zx + zw and zy <= y <= zy + zh
    
    def create_base(self):
        img = Image.new('RGB', (self.width, self.height), hex_to_rgb(COLORS['bg_primary']))
        return img, ImageDraw.Draw(img)
    
    # ===== 风格2: 螺旋星系 =====
    def draw_galaxy(self, draw):
        random.seed(1200)
        centers = [(200, 200), (1100, 300), (600, 700)]
        
        for cx, cy in centers:
            for arm in range(4):
                offset = arm * (2 * math.pi / 4)
                points = []
                
                for i in range(80):
                    angle = offset + i * 0.08
                    radius = 20 + i * 4
                    
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    
                    # 核心区域降低密度
                    if self.is_in_core_zone(x, y) and random.random() < 0.7:
                        continue
                    
                    points.append((x, y))
                    
                    if random.random() < 0.15:
                        size = random.randint(1, 3)
                        brightness = random.uniform(0.5, 0.9)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                        draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
                
                if len(points) > 1:
                    brightness = random.uniform(0.3, 0.6)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格3: 水波纹 =====
    def draw_ripple(self, draw):
        random.seed(1300)
        centers = [(150, 150), (500, 400), (1200, 200), (300, 700), (1100, 600)]
        
        for cx, cy in centers:
            for radius in range(30, 250, 20):
                points = []
                for angle in [i * 0.05 for i in range(126)]:
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    
                    x += int(8 * math.sin(angle * 5))
                    y += int(8 * math.cos(angle * 5))
                    
                    if not self.is_in_core_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 5:
                    alpha = max(0.3, 1 - radius / 250)
                    brightness = 0.5 * alpha
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                    
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格4: 羽毛 =====
    def draw_feather(self, draw):
        random.seed(1400)
        
        for _ in range(60):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_core_zone(x, y):
                continue
            
            length = random.randint(60, 120)
            angle = random.uniform(0, 2 * math.pi)
            
            main_points = [(x, y)]
            cx, cy = x, y
            
            for i in range(length // 4):
                cx += int(4 * math.cos(angle))
                cy += int(4 * math.sin(angle))
                angle += random.uniform(-0.08, 0.08)
                main_points.append((cx, cy))
            
            if len(main_points) > 3:
                brightness = random.uniform(0.4, 0.7)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                draw.line(main_points, fill=color, width=1)
                
                for j in range(0, len(main_points), 2):
                    mx, my = main_points[j]
                    branch_angle = angle + random.uniform(-1.2, 1.2)
                    bl = random.randint(8, 18)
                    
                    bx = mx + int(bl * math.cos(branch_angle))
                    by = my + int(bl * math.sin(branch_angle))
                    
                    if not self.is_in_core_zone(bx, by):
                        brightness = random.uniform(0.25, 0.5)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                        draw.line([(mx, my), (bx, by)], fill=color, width=1)
    
    # ===== 风格5: 蛛网 =====
    def draw_spiderweb(self, draw):
        random.seed(1500)
        centers = [(250, 250), (1000, 400), (600, 700)]
        
        for cx, cy in centers:
            for i in range(10):
                angle = (2 * math.pi / 10) * i
                length = 180
                
                points = [(cx, cy)]
                for r in range(0, length, 15):
                    x = cx + int(r * math.cos(angle))
                    y = cy + int(r * math.sin(angle))
                    if not self.is_in_core_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 1:
                    brightness = random.uniform(0.35, 0.6)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                    draw.line(points, fill=color, width=1)
            
            for radius in range(30, 200, 35):
                points = []
                for angle in [i * 0.03 for i in range(210)]:
                    x = cx + int(radius * math.cos(angle))
                    y = cy + int(radius * math.sin(angle))
                    y += int(12 * math.sin(angle * 3))
                    
                    if not self.is_in_core_zone(x, y):
                        points.append((x, y))
                
                if len(points) > 5:
                    brightness = random.uniform(0.25, 0.5)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                    for j in range(len(points) - 1):
                        draw.line([points[j], points[j+1]], fill=color, width=1)
    
    # ===== 风格6: 电路板 =====
    def draw_circuit(self, draw):
        random.seed(1600)
        
        for _ in range(40):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_core_zone(x, y):
                continue
            
            if random.random() < 0.5:
                end_x = min(x + random.randint(80, 200), self.width)
                if not self.is_in_core_zone(end_x, y):
                    brightness = random.uniform(0.45, 0.75)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    draw.line([(x, y), (end_x, y)], fill=color, width=2)
                    
                    for px in range(x, end_x, 25):
                        if not self.is_in_core_zone(px, y) and random.random() < 0.4:
                            draw.ellipse([(px-2, y-2), (px+2, y+2)], 
                                        fill=hex_to_rgb(COLORS['accent_highlight']))
            else:
                end_y = min(y + random.randint(80, 200), self.height)
                if not self.is_in_core_zone(x, end_y):
                    brightness = random.uniform(0.45, 0.75)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    draw.line([(x, y), (x, end_y)], fill=color, width=2)
        
        for _ in range(40):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            if not self.is_in_core_zone(x, y):
                size = random.randint(3, 6)
                brightness = random.uniform(0.6, 0.9)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
    
    # ===== 风格7: 水晶 =====
    def draw_crystal(self, draw):
        random.seed(1700)
        
        for _ in range(40):
            cx = random.randint(0, self.width)
            cy = random.randint(0, self.height)
            
            if self.is_in_core_zone(cx, cy):
                continue
            
            sides = random.choice([3, 4, 5, 6])
            radius = random.randint(25, 60)
            
            points = []
            for i in range(sides):
                angle = (2 * math.pi / sides) * i + random.uniform(-0.15, 0.15)
                x = cx + int(radius * math.cos(angle))
                y = cy + int(radius * math.sin(angle))
                points.append((x, y))
            
            points.append(points[0])
            
            brightness = random.uniform(0.35, 0.65)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
            draw.line(points, fill=color, width=1)
            
            for i in range(sides):
                for j in range(i+2, sides):
                    if abs(i - j) > 1 and not (i == 0 and j == sides - 1):
                        draw.line([points[i], points[j]], fill=color, width=1)
    
    # ===== 风格8: 熔岩 =====
    def draw_magma(self, draw):
        random.seed(1800)
        
        for _ in range(20):
            points = []
            x = random.randint(0, self.width)
            y = 0
            
            for _ in range(random.randint(25, 50)):
                x += random.randint(-25, 25)
                y += random.randint(12, 22)
                
                if y > self.height:
                    break
                
                if not self.is_in_core_zone(x, y):
                    points.append((x, y))
            
            if len(points) > 3:
                for offset in range(-2, 3):
                    offset_points = [(px + offset, py) for px, py in points]
                    brightness = 0.9 - abs(offset) * 0.25
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    for j in range(len(offset_points) - 1):
                        draw.line([offset_points[j], offset_points[j+1]], fill=color, width=1)
    
    # ===== 风格9: 星轨 =====
    def draw_star_trails(self, draw):
        random.seed(1900)
        center_x, center_y = self.width // 2, self.height // 2
        
        for i in range(150):
            angle = random.uniform(0, 2 * math.pi)
            start_r = random.randint(150, 650)
            end_r = start_r - random.randint(30, 80)
            
            sx = center_x + int(start_r * math.cos(angle))
            sy = center_y + int(start_r * math.sin(angle))
            ex = center_x + int(end_r * math.cos(angle + 0.12))
            ey = center_y + int(end_r * math.sin(angle + 0.12))
            
            if not self.is_in_core_zone(sx, sy) and not self.is_in_core_zone(ex, ey):
                brightness = random.uniform(0.35, 0.75)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                draw.line([(sx, sy), (ex, ey)], fill=color, width=1)
                
                if random.random() < 0.25:
                    draw.ellipse([(sx-2, sy-2), (sx+2, sy+2)], 
                                fill=hex_to_rgb(COLORS['accent_bright']))
    
    # ===== 风格10: 蒲公英 =====
    def draw_dandelion(self, draw):
        random.seed(2000)
        
        for _ in range(80):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            if self.is_in_core_zone(x, y):
                continue
            
            size = random.randint(2, 4)
            brightness = random.uniform(0.6, 0.9)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
            draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
            
            for _ in range(random.randint(6, 12)):
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(25, 55)
                ex = x + int(length * math.cos(angle))
                ey = y + int(length * math.sin(angle))
                
                if not self.is_in_core_zone(ex, ey):
                    brightness = random.uniform(0.25, 0.5)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                    draw.line([(x, y), (ex, ey)], fill=color, width=1)
    
    def generate_all(self):
        styles = [
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
            
            filename = f"macos_editor_{name}_fixed.png"
            img.save(filename)
            print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    styles = FixedExtendedStyles()
    styles.generate_all()
