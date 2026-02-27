#!/usr/bin/env python3
"""
混合风格 - 两种风格的融合
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

class HybridStyles:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
    
    def create_base(self):
        img = Image.new('RGB', (self.width, self.height), hex_to_rgb(COLORS['bg_primary']))
        return img, ImageDraw.Draw(img)
    
    # ===== 混合1: 裂缝 + 有机 =====
    def draw_crack_organic(self, draw):
        random.seed(300)
        
        # 主裂缝
        for _ in range(8):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            points = [(x, y)]
            angle = random.uniform(0, 2 * math.pi)
            
            for _ in range(random.randint(5, 12)):
                step = random.randint(30, 60)
                angle += random.uniform(-0.4, 0.4)
                x += int(step * math.cos(angle))
                y += int(step * math.sin(angle))
                x += random.randint(-8, 8)
                points.append((x, y))
                
                # 有机弯曲分支
                if random.random() < 0.4:
                    branch_points = [(x, y)]
                    bx, by = x, y
                    b_angle = angle + random.uniform(-1.0, 1.0)
                    for _ in range(random.randint(3, 6)):
                        step = random.randint(15, 30)
                        b_angle += random.uniform(-0.3, 0.3)
                        bx += int(step * math.cos(b_angle))
                        by += int(step * math.sin(b_angle))
                        branch_points.append((bx, by))
                    
                    if len(branch_points) > 1:
                        brightness = random.uniform(0.4, 0.7)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                        draw.line(branch_points, fill=color, width=1)
            
            if len(points) > 1:
                brightness = random.uniform(0.5, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=2)
    
    # ===== 混合2: 哥窑 + 藤蔓 =====
    def draw_geyao_vine(self, draw):
        random.seed(400)
        
        # 纵向哥窑线带藤蔓弯曲
        for i in range(6):
            x = 200 + i * 200
            points = [(x, 0)]
            
            for y in range(0, self.height, 30):
                wave = 40 * math.sin(y / 80 + i)
                points.append((x + wave, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.3, 0.5)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                draw.line(points, fill=color, width=2)
                
                # 藤蔓叶子
                for j in range(5, len(points) - 5, 8):
                    px, py = points[j]
                    if random.random() < 0.6:
                        size = random.randint(3, 6)
                        leaf_color = tuple(int(c * 0.8) for c in hex_to_rgb(COLORS['accent_highlight']))
                        draw.ellipse([(px-size, py-size), (px+size, py+size)], fill=leaf_color)
        
        # 横向金丝
        for i in range(5):
            y = 150 + i * 150
            points = [(0, y)]
            
            for x in range(0, self.width, 25):
                wave = 20 * math.sin(x / 60 + i)
                points.append((x, y + wave))
            
            if len(points) > 1:
                brightness = random.uniform(0.4, 0.7)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=1)
    
    # ===== 混合3: 神经网络 + 闪电 =====
    def draw_neural_lightning(self, draw):
        random.seed(500)
        
        # 节点
        nodes = []
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            nodes.append((x, y))
            
            size = random.randint(2, 4)
            brightness = random.uniform(0.6, 0.9)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
            draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
        
        # 闪电式连接
        for i, (x1, y1) in enumerate(nodes):
            nearby = []
            for j, (x2, y2) in enumerate(nodes):
                if i != j:
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    if dist < 180:
                        nearby.append((dist, j, x2, y2))
            
            nearby.sort()
            for dist, j, x2, y2 in nearby[:random.randint(1, 3)]:
                # 锯齿状连线
                mid_x = (x1 + x2) // 2 + random.randint(-30, 30)
                mid_y = (y1 + y2) // 2 + random.randint(-30, 30)
                
                brightness = max(0.15, 1 - dist / 180) * random.uniform(0.3, 0.6)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                draw.line([(x1, y1), (mid_x, mid_y), (x2, y2)], fill=color, width=1)
    
    # ===== 混合4: 有机流动 + 金丝 =====
    def draw_organic_gold(self, draw):
        random.seed(600)
        
        # 有机主线
        for _ in range(12):
            points = []
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            angle = random.uniform(0, 2 * math.pi)
            for _ in range(random.randint(20, 40)):
                step = random.randint(15, 35)
                angle += random.uniform(-0.3, 0.3)
                x += int(step * math.cos(angle))
                y += int(step * math.sin(angle))
                x += int(10 * math.sin(y / 25))
                points.append((x, y))
            
            if len(points) > 1:
                # 主线
                brightness = random.uniform(0.3, 0.6)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                for j in range(len(points) - 1):
                    draw.line([points[j], points[j+1]], fill=color, width=2)
                
                # 金丝细线跟随
                for offset in [-5, 5]:
                    gold_points = []
                    for px, py in points:
                        gold_points.append((px + offset, py + offset))
                    
                    brightness = random.uniform(0.5, 0.8)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                    draw.line(gold_points, fill=color, width=1)
    
    # ===== 混合5: 裂缝 + 哥窑 =====
    def draw_crack_geyao(self, draw):
        random.seed(700)
        
        # 纵向裂缝（铁线风格）
        for i in range(8):
            x = 150 + i * 160
            points = [(x, 0)]
            
            for y in range(0, self.height, 40):
                x += random.randint(-15, 15)
                points.append((x, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.35, 0.55)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                draw.line(points, fill=color, width=2)
        
        # 横向金丝（带裂缝锯齿）
        for i in range(6):
            y = 120 + i * 130
            x = 0
            points = [(x, y)]
            
            while x < self.width:
                step = random.randint(40, 80)
                x += step
                y += random.randint(-20, 20)
                points.append((x, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.5, 0.75)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=1)
        
        # 细碎开片
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(20, 50)
            
            end_x = x + int(length * math.cos(angle))
            end_y = y + int(length * math.sin(angle))
            
            brightness = random.uniform(0.3, 0.6)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
            draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
    
    def generate_all(self):
        styles = [
            ("hybrid1_crack_organic", self.draw_crack_organic),
            ("hybrid2_geyao_vine", self.draw_geyao_vine),
            ("hybrid3_neural_lightning", self.draw_neural_lightning),
            ("hybrid4_organic_gold", self.draw_organic_gold),
            ("hybrid5_crack_geyao", self.draw_crack_geyao),
        ]
        
        for name, draw_fn in styles:
            img, draw = self.create_base()
            draw_fn(draw)
            
            filename = f"macos_editor_{name}.png"
            img.save(filename)
            print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    from PIL import Image, ImageDraw, ImageFont
    hybrid = HybridStyles()
    hybrid.generate_all()
