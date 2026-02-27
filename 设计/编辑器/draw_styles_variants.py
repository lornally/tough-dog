#!/usr/bin/env python3
"""
各种新风格变体 - 裂缝、哥窑、神经网络、藤蔓等
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
}

class StyleVariants:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        
        try:
            self.font_medium = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 13)
            self.font_small = ImageFont.truetype("/System/Library/Fonts/SFProText-Regular.otf", 11)
        except:
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
    
    # ===== 风格1: 裂缝风格 =====
    def draw_crack_style(self, draw):
        """裂缝风格 - 像干涸的土地或破碎的玻璃"""
        random.seed(100)
        
        # 主裂缝
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            points = [(x, y)]
            angle = random.uniform(0, 2 * math.pi)
            
            for _ in range(random.randint(5, 15)):
                step = random.randint(20, 50)
                angle += random.uniform(-0.5, 0.5)
                x += int(step * math.cos(angle))
                y += int(step * math.sin(angle))
                
                # 裂缝的锯齿感
                x += random.randint(-5, 5)
                y += random.randint(-5, 5)
                
                x = max(-50, min(self.width + 50, x))
                y = max(-50, min(self.height + 50, y))
                points.append((x, y))
                
                # 分叉裂缝
                if random.random() < 0.3:
                    branch_angle = angle + random.uniform(-1.0, 1.0)
                    branch_x = x
                    branch_y = y
                    branch_points = [(branch_x, branch_y)]
                    
                    for _ in range(random.randint(3, 8)):
                        step = random.randint(10, 25)
                        branch_angle += random.uniform(-0.3, 0.3)
                        branch_x += int(step * math.cos(branch_angle))
                        branch_y += int(step * math.sin(branch_angle))
                        branch_points.append((branch_x, branch_y))
                    
                    if len(branch_points) > 1:
                        brightness = random.uniform(0.5, 0.8)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                        draw.line(branch_points, fill=color, width=1)
            
            if len(points) > 1:
                # 主裂缝较亮
                brightness = random.uniform(0.6, 0.9)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=2)
                
                # 裂缝交点的高光
                for i in range(2, len(points) - 2, 3):
                    px, py = points[i]
                    size = random.randint(2, 4)
                    node_color = tuple(int(c * 0.9) for c in hex_to_rgb(COLORS['accent_highlight']))
                    draw.ellipse([(px-size, py-size), (px+size, py+size)], fill=node_color)
    
    # ===== 风格2: 哥窑瓷器 =====
    def draw_geyao_style(self, draw):
        """哥窑风格 - 金丝铁线，开片纹理"""
        random.seed(200)
        
        # 纵向主线（铁线 - 深色）
        for i in range(8):
            x = random.randint(0, self.width)
            points = [(x, 0)]
            
            for y in range(0, self.height, 20):
                x += random.randint(-10, 10)
                points.append((x, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.3, 0.5)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_secondary']))
                draw.line(points, fill=color, width=2)
        
        # 横向主线（金丝 - 亮色）
        for i in range(10):
            y = random.randint(0, self.height)
            points = [(0, y)]
            
            for x in range(0, self.width, 25):
                y += random.randint(-8, 8)
                points.append((x, y))
            
            if len(points) > 1:
                brightness = random.uniform(0.5, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                draw.line(points, fill=color, width=1)
        
        # 细碎开片
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(30, 80)
            
            end_x = x + int(length * math.cos(angle))
            end_y = y + int(length * math.sin(angle))
            
            brightness = random.uniform(0.4, 0.7)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
            draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
    
    # ===== 风格3: 神经网络 =====
    def draw_neural_style(self, draw):
        """神经网络风格 - 节点和连接"""
        random.seed(300)
        
        nodes = []
        # 生成节点
        for _ in range(80):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 5)
            nodes.append((x, y, size))
            
            # 绘制节点
            brightness = random.uniform(0.5, 0.9)
            color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
            draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=color)
        
        # 绘制连接
        for i, (x1, y1, s1) in enumerate(nodes):
            # 连接到最近的3-5个节点
            distances = []
            for j, (x2, y2, s2) in enumerate(nodes):
                if i != j:
                    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                    if dist < 200:  # 只连接近距离的
                        distances.append((dist, j, x2, y2))
            
            distances.sort()
            for dist, j, x2, y2 in distances[:random.randint(2, 4)]:
                # 连接线
                alpha = max(0.1, 1 - dist / 200)
                brightness = alpha * random.uniform(0.3, 0.6)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    
    # ===== 风格4: 藤蔓缠绕 =====
    def draw_vine_style(self, draw):
        """藤蔓风格 - 螺旋缠绕，有机生长"""
        random.seed(400)
        
        for _ in range(15):
            # 起点
            start_x = random.randint(0, self.width)
            start_y = self.height if random.random() < 0.5 else 0
            
            points = [(start_x, start_y)]
            x, y = start_x, start_y
            
            # 螺旋向上/向下生长
            angle = -math.pi / 2 if start_y == self.height else math.pi / 2
            spiral_radius = random.randint(20, 50)
            
            for i in range(random.randint(30, 60)):
                # 螺旋运动
                angle += 0.15
                spiral_x = x + int(spiral_radius * math.cos(angle))
                spiral_y = y + int(spiral_radius * 0.3 * math.sin(angle))
                
                # 向上/向下生长
                if start_y == self.height:
                    y -= random.randint(10, 20)
                else:
                    y += random.randint(10, 20)
                
                x = spiral_x
                x = max(-50, min(self.width + 50, x))
                y = max(-50, min(self.height + 50, y))
                
                points.append((x, y))
                
                # 随机叶子（小瘤子）
                if random.random() < 0.3:
                    leaf_x = x + random.randint(-15, 15)
                    leaf_y = y + random.randint(-15, 15)
                    size = random.randint(3, 6)
                    brightness = random.uniform(0.6, 0.9)
                    color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                    draw.ellipse([(leaf_x-size, leaf_y-size), (leaf_x+size, leaf_y+size)], fill=color)
            
            if len(points) > 1:
                brightness = random.uniform(0.5, 0.8)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_primary']))
                for j in range(len(points) - 1):
                    width = random.choice([1, 1, 2])
                    draw.line([points[j], points[j+1]], fill=color, width=width)
    
    # ===== 风格5: 闪电/能量 =====
    def draw_lightning_style(self, draw):
        """闪电风格 - 锯齿状能量线"""
        random.seed(500)
        
        for _ in range(25):
            x1 = random.randint(0, self.width)
            y1 = 0
            x2 = random.randint(0, self.width)
            y2 = self.height
            
            # 生成锯齿路径
            points = [(x1, y1)]
            x, y = x1, y1
            
            segments = random.randint(5, 12)
            for i in range(segments):
                progress = (i + 1) / segments
                target_x = x1 + (x2 - x1) * progress
                target_y = y1 + (y2 - y1) * progress
                
                # 锯齿偏移
                offset = random.randint(-40, 40)
                x = int(target_x + offset)
                y = int(target_y)
                
                points.append((x, y))
            
            points.append((x2, y2))
            
            if len(points) > 1:
                # 主闪电
                brightness = random.uniform(0.6, 1.0)
                color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_bright']))
                for j in range(len(points) - 1):
                    draw.line([points[j], points[j+1]], fill=color, width=2)
                
                # 分支闪电
                for j in range(1, len(points) - 1):
                    if random.random() < 0.4:
                        px, py = points[j]
                        branch_x = px + random.randint(-30, 30)
                        branch_y = py + random.randint(20, 50)
                        brightness = random.uniform(0.4, 0.7)
                        color = tuple(int(c * brightness) for c in hex_to_rgb(COLORS['accent_highlight']))
                        draw.line([(px, py), (branch_x, branch_y)], fill=color, width=1)
    
    def create_base_image(self):
        """创建基础图片"""
        img = Image.new('RGB', (self.width, self.height), hex_to_rgb(COLORS['bg_primary']))
        return img, ImageDraw.Draw(img)
    
    def generate_all(self):
        """生成所有风格"""
        styles = [
            ("style1_crack", self.draw_crack_style),
            ("style2_geyao", self.draw_geyao_style),
            ("style3_neural", self.draw_neural_style),
            ("style4_vine", self.draw_vine_style),
            ("style5_lightning", self.draw_lightning_style),
        ]
        
        for name, draw_fn in styles:
            img, draw = self.create_base_image()
            draw_fn(draw)
            
            filename = f"macos_editor_{name}.png"
            img.save(filename)
            print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    variants = StyleVariants()
    variants.generate_all()
