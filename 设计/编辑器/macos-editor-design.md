# macOS 编辑器界面设计文档

## 📋 设计规范参考

本文档遵循 `lucky实践` 中的 UI 绘制规范：
- 交互式 6 步选择流程
- 12 种标准配色方案
- 画布管理规范
- Pencil MCP 调用规范

---

## 1. 设计理念

### 1.1 Jef Raskin 的 Humane Interface 核心原则

#### "图形界面的命令行"
- **LEAP 模式**：通过键盘快捷键（如 `Cmd+Space`）快速跳转到任意位置
- **命令面板**：类似 VS Code 的 Command Palette，但更智能、更即时
- **即时反馈**：输入命令时实时预览结果，无需按回车确认
- **模糊匹配**：支持自然语言输入，例如输入 "save dark theme" 直接切换到暗黑模式并保存

#### 基于空间感的导航系统
- **无限画布**：文档不是线性的，而是在二维空间中展开
- **缩放导航**：
  - 缩小：看到整个项目结构（文件夹树、文件关系图）
  - 中等：当前文件的代码概览（minimap 增强版）
  - 放大：当前编辑区域
  - 超放大：查看某一行代码的细节、注释、历史版本
- **空间记忆**：文件在空间中的位置是固定的，用户通过位置记忆快速定位

### 1.2 科幻感设计元素
- **霓虹光效**：重点元素使用发光效果
- **深色主题为主**：深色背景 + 高对比度强调色
- **玻璃拟态**：半透明面板，显示背后内容的模糊轮廓
- **动态效果**：平滑的过渡动画，响应式微交互

---

## 2. 界面结构

### 2.1 整体布局

```
┌─────────────────────────────────────────────────────────────┐
│ [菜单栏] 文件  编辑  视图  导航  帮助                         │
├──────────┬────────────────────────────────────────┬─────────┤
│          │  [标签栏]  main.js  ┃  utils.js  [+]    │  🔍     │
│          ├────────────────────────────────────────┴─────────┤
│   空间   │                                                  │
│   导航   │              编  辑  区  域                      │
│   面板   │                                                  │
│   (可    │         ┌─────────────────────┐                  │
│   收缩)  │         │    代码编辑区       │                  │
│          │         │                     │                  │
│          │         │  function hello() { │                  │
│  ◀──▶    │         │    // 高亮行        │                  │
│          │         │  }                  │                  │
│          │         └─────────────────────┘                  │
│          │                                                  │
│          │  [命令行输入条] > git commit -m "feat:..."        │
├──────────┼──────────────────────────────────────────────────┤
│ 状态栏   │  行 42, 列 15  │  UTF-8  │  JavaScript  │  🌙    │
└──────────┴──────────────────────────────────────────────────┘
```

### 2.2 核心组件

#### A. 空间导航面板 (Space Navigator)
- **ZUI (Zoomable User Interface)**
- 类似 Google Maps 的缩放体验
- 不同缩放级别显示不同信息：
  - 10% - 项目结构图（文件夹、模块关系）
  - 30% - 文件列表 + 文件预览缩略图
  - 60% - 代码结构（函数、类）
  - 100% - 完整代码编辑
  - 200% - 聚焦模式（单行代码 + AI 建议）

#### B. 命令行融合输入条 (Command Fusion Bar)
- 位于编辑器底部
- 默认显示提示：`> 输入命令或搜索...`
- 支持三种模式自动切换：
  1. **命令模式**：以 `>` 开头，执行编辑器命令
  2. **搜索模式**：以 `/` 开头，全局搜索
  3. **AI 模式**：以 `@` 开头，询问 AI
- 实时预览结果在编辑器中高亮显示

#### C. 标签栏增强 (Spatial Tabs)
- 标签不仅是文件名，还显示：
  - 文件在 2D 空间中的位置缩略图
  - 修改状态指示器（发光点）
  - 关联文件的连接线
- 拖拽标签可重新排列空间布局

#### D. 全息上下文面板 (Holographic Context Panel)
- 右侧可滑出的面板
- 显示：
  - 当前函数的调用关系图
  - 变量定义和引用
  - Git 历史（时间轴形式）
  - AI 建议和注释
- 半透明玻璃效果，不遮挡代码

---

## 3. 配色方案

### 3.1 确认配色（暗黑金）

**已确认：暗黑金配色**

| 项目 | 色值 | 用途 |
|------|------|------|
| 主背景 | #0F172A | 深空黑背景 |
| 强调色 | #CA8A04 | 暗黑金 |
| 次级强调 | #B45309 | 深金 |
| 高光 | #F59E0B | 亮金 |
| 文字主色 | #E8F0FF | 主文本 |
| 文字次色 | #94A3B8 | 次要文本 |

### 3.2 最终配色方案（已确认）

```css
/* 暗黑金配色方案 - 全屏清晰，无模糊 */
--bg-primary: #0F172A;        /* 深空黑 - 主背景 */
--bg-secondary: #1E293B;      /* 次级背景 */
--bg-tertiary: #334155;       /* 面板背景 */

--accent-primary: #CA8A04;    /* 暗黑金 - 主要强调 */
--accent-secondary: #B45309;  /* 深金 - 次要强调 */
--accent-highlight: #F59E0B;  /* 亮金 - 高光 */
--accent-error: #EF4444;      /* 错误红 */
--accent-success: #22C55E;    /* 成功绿 */

--text-primary: #E8F0FF;      /* 主文本 */
--text-secondary: #94A3B8;    /* 次要文本 */
--text-muted: #64748B;        /* 弱化文本 */

/* 水流特效光带 */
--stream-glow: linear-gradient(
  90deg,
  transparent 0%,
  rgba(202, 138, 4, 0.3) 50%,
  transparent 100%
);

/* 宝石光泽条纹 */
--gem-stripe: repeating-linear-gradient(
  45deg,
  transparent,
  transparent 10px,
  rgba(245, 158, 11, 0.05) 10px,
  rgba(245, 158, 11, 0.05) 11px
);
```

### 3.3 语义化颜色

```css
/* 代码高亮 */
--syntax-keyword: #FF79C6;    /* 关键字 - 粉 */
--syntax-function: #00D9FF;   /* 函数 - 青 */
--syntax-string: #F1FA8C;     /* 字符串 - 黄 */
--syntax-comment: #6272A4;    /* 注释 - 灰蓝 */
--syntax-variable: #E8F0FF;   /* 变量 - 白 */

/* 发光效果 */
--glow-accent: 0 0 20px rgba(0, 217, 255, 0.5);
--glow-error: 0 0 20px rgba(255, 0, 110, 0.5);
--glow-success: 0 0 20px rgba(6, 255, 165, 0.5);
--glow-gold: 0 0 20px rgba(202, 138, 4, 0.5);
```

---

## 4. 设计方案选择（已确认）

| 编号 | 方案 | 特点 | 状态 |
|------|------|------|------|
| 1 | 标准macOS | 浅色模式、系统原生风格 | - |
| 2 | **暗黑模式** | 深色主题、OLED优化、水流特效、宝石光泽 | **✅ 已选** |
| 3 | 玻璃拟态 | 半透明效果、背景模糊 | ❌ **禁用** |

**确认选择：方案 2 - 暗黑模式（暗黑金配色）**

### 4.1 视觉特效（已确认）

#### ✅ 允许特效

**1. 水流光带效果**
```css
/* 水平流光 */
.stream-effect {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(202, 138, 4, 0.4) 50%,
    transparent 100%
  );
  animation: flow 3s ease-in-out infinite;
}

@keyframes flow {
  0%, 100% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
}
```

**2. 丝状/细条纹宝石光泽**
```css
/* 45度角细条纹 */
.gem-stripe {
  background: repeating-linear-gradient(
    45deg,
    #0F172A 0px,
    #0F172A 8px,
    rgba(202, 138, 4, 0.08) 8px,
    rgba(202, 138, 4, 0.08) 9px
  );
}

/* 垂直细条纹 */
.gem-vertical {
  background: repeating-linear-gradient(
    90deg,
    #0F172A 0px,
    #0F172A 20px,
    rgba(245, 158, 11, 0.05) 20px,
    rgba(245, 158, 11, 0.05) 21px
  );
}
```

**3. 金边发光效果（清晰锐利）**
```css
/* 清晰的金色边框，无模糊 */
.gold-border {
  border: 1px solid #CA8A04;
  box-shadow: 
    0 0 0 1px #B45309,
    0 0 0 2px #0F172A;
}

/* 当前行金边高亮 */
.current-line {
  border-left: 3px solid #CA8A04;
  background: rgba(202, 138, 4, 0.08);
}
```

#### ❌ 禁止特效

```css
/* 禁止使用任何模糊效果 */
.glass-effect {
  /* ❌ backdrop-filter: blur(20px); */
  /* ❌ filter: blur(10px); */
  /* ❌ opacity: 0.5; 导致模糊感 */
}
```

---

## 5. 交互设计

### 5.1 键盘导航 (LEAP 系统)

| 快捷键 | 功能 |
|--------|------|
| `Cmd+Space` | 打开 LEAP 跳转（类似 Spotlight） |
| `Cmd+Shift+Space` | 打开命令面板 |
| `Cmd+Up/Down` | 缩放导航（放大/缩小视图） |
| `Cmd+Drag` | 平移画布 |
| `Cmd+1~9` | 快速跳转到预定义的空间位置 |
| `Option+Hover` | 预览定义（悬停显示） |
| `Cmd+K, Cmd+S` | 保存当前空间位置为书签 |

### 5.2 空间导航手势

| 操作 | 功能 |
|------|------|
| 双指缩放 | 缩放视图级别 |
| 双指滑动 | 平移画布 |
| 双击 | 智能放大（根据内容自动选择级别） |
| 长按 | 显示上下文菜单（全息面板） |
| 画圈手势 | 圈选代码块，触发 AI 操作 |

### 5.3 命令行融合输入条交互

```
用户输入: > theme dark

┌────────────────────────────────────────────────────┐
│ > theme dark                                        │
├────────────────────────────────────────────────────┤
│ ⚡ 切换到暗黑主题                                    │
│ ⚡ 保存主题为默认                                    │
│ 🔍 搜索 "dark" 相关命令...                          │
└────────────────────────────────────────────────────┘
         ↑ 实时预览，上下键选择，回车执行
```

---

## 6. 视觉设计细节

### 6.1 暗黑金面板（清晰锐利）
```css
/* 无模糊，全屏清晰 */
.dark-panel {
  background: #1E293B;
  border: 1px solid #334155;
  /* 宝石光泽背景 */
  background-image: repeating-linear-gradient(
    45deg,
    transparent 0px,
    transparent 8px,
    rgba(202, 138, 4, 0.05) 8px,
    rgba(202, 138, 4, 0.05) 9px
  );
}
```

### 6.2 金边边框效果
```css
/* 清晰的金色边框 */
.gold-border {
  border: 1px solid #CA8A04;
  /* 双重边框制造立体感 */
  box-shadow: 
    inset 0 0 0 1px rgba(202, 138, 4, 0.3);
}

/* 激活状态 */
.gold-border-active {
  border: 2px solid #CA8A04;
  background: rgba(202, 138, 4, 0.1);
}
```

### 6.3 当前行高亮（金边）
```css
.current-line {
  border-left: 3px solid #CA8A04;
  background: rgba(202, 138, 4, 0.08);
  /* 水流光带 */
  background-image: linear-gradient(
    90deg,
    transparent 0%,
    rgba(202, 138, 4, 0.1) 50%,
    transparent 100%
  );
}
```

### 6.4 光标设计（金色脉冲）
```css
.cursor {
  width: 2px;
  background: #CA8A04;
  /* 清晰的脉冲效果 */
  animation: gold-pulse 1.5s ease-in-out infinite;
}

@keyframes gold-pulse {
  0%, 100% { 
    opacity: 1;
    background: #CA8A04;
  }
  50% { 
    opacity: 0.6;
    background: #F59E0B;
  }
}
```

### 6.5 水流特效（底部命令栏）
```css
.command-bar {
  background: #0F172A;
  border-top: 1px solid #334155;
  position: relative;
  overflow: hidden;
}

/* 水流光带动画 */
.command-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    #CA8A04 50%,
    transparent 100%
  );
  animation: stream-flow 4s ease-in-out infinite;
}

@keyframes stream-flow {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}
```

---

## 7. 排版规范（关键！）

根据 `lucky实践` 的排版问题解决经验：

### 7.1 禁止直接使用 lineHeight
❌ 错误：
```javascript
I(text, {
  type: "text",
  content: "Hello",
  lineHeight: 1.5  // 会导致高度计算错误
})
```

✅ 正确：
```javascript
// 使用固定高度容器包裹
textContainer = I(parent, {
  type: "frame",
  height: 24  // 固定高度
})

I(textContainer, {
  type: "text",
  content: "Hello"
})
```

### 7.2 精确计算总高度
```
总高度 = paddingTop + 内容高度 + gap + paddingBottom
```

### 7.3 卡片布局示例
```javascript
// 卡片容器
card = I(container, {
  type: "frame",
  layout: "vertical",
  padding: 16,
  gap: 12
})

// 标题区域（固定高度）
titleContainer = I(card, {
  type: "frame",
  height: 28
})
I(titleContainer, {
  type: "text",
  content: "标题",
  fontSize: 16,
  fontWeight: "600"
})

// 内容区域
contentContainer = I(card, {
  type: "frame",
  height: 80  // 确保足够空间
})
```

---

## 8. 使用 Pencil MCP 绘制流程

### Step 1: 平台确认 ✅
- 平台：macOS
- 设计系统：macOS Human Interface Guidelines + 科幻增强

### Step 2: 配色方案选择（已确认）
**确认：暗黑金配色**
- 主背景：深空黑 #0F172A
- 强调色：暗黑金 #CA8A04
- 高光：亮金 #F59E0B

### Step 3: 设计方案选择（已确认）
**确认：方案 2 - 暗黑模式**
- ✅ 水流特效
- ✅ 丝状/细条纹宝石光泽
- ✅ 金边发光效果
- ❌ 无玻璃模糊
- ❌ 无背景模糊
- ✅ 全屏清晰

### Step 4: 页面类型确认
- 页面类型：代码编辑器主界面
- 包含组件：
  - ✅ 标题栏（红绿灯按钮）
  - ✅ 空间导航面板（左侧，可收缩）
  - ✅ 标签栏
  - ✅ 代码编辑区（中央）
  - ✅ 命令行输入条（底部）
  - ✅ 状态栏
  - ✅ 全息上下文面板（右侧，可滑出）

### Step 5: 检查画布空白位置
绘制前必须执行：
```javascript
// 1. 检查画布状态
snapshot_layout({maxDepth: 1})

// 2. 查找空白位置
find_empty_space_on_canvas({
  width: 1280,    // macOS 窗口宽度
  height: 832,    // macOS 窗口高度
  padding: 50,
  direction: "right"
})
```

### Step 6: 确认并开始绘制
汇总选择（已确认）：
| 项目 | 选择 |
|------|------|
| 平台 | macOS |
| 配色 | **暗黑金** #0F172A / #CA8A04 |
| 方案 | **暗黑模式** + 水流特效 + 宝石光泽 |
| 禁忌 | 无模糊效果、无玻璃拟态 |
| 要求 | 全屏清晰 |
| 页面 | 代码编辑器主界面 |
| 位置 | 待检查画布后确定 |

---

## 9. 组件层次结构（Pencil 绘制用）

```
Window (1280x832)
├── TitleBar (高度: 28)
│   ├── Traffic Lights (红黄绿按钮) - 左上角
│   └── Window Title - 居中
├── MainContainer
│   ├── LeftPanel - 空间导航 (宽度: 200, 可收缩)
│   │   ├── ZoomControls (缩放控制)
│   │   └── SpaceMap (空间地图)
│   ├── CenterArea
│   │   ├── TabBar (高度: 38)
│   │   │   ├── Tab (文件名 + 关闭按钮)
│   │   │   └── AddButton (+)
│   │   ├── EditorArea
│   │   │   ├── LineNumbers (行号区)
│   │   │   └── CodeContent (代码内容)
│   │   └── CommandBar (高度: 36)
│   │       ├── Prompt (>)
│   │       └── Input
│   └── RightPanel - 上下文面板 (宽度: 280, 可滑出)
│       ├── AI Suggestions
│       └── Context Info
└── StatusBar (高度: 24)
    ├── Position (行, 列)
    ├── Encoding (UTF-8)
    ├── Language (JavaScript)
    └── ThemeToggle (🌙)
```

---

## 10. 特色功能

### 10.1 全息代码地图 (Holographic Minimap)
- 右侧的代码地图不是简单的缩略图
- 而是带有深度感的 3D 可视化
- 当前编辑区域发光高亮
- 悬停显示函数/类名称

### 10.2 时空穿梭 (Time Travel)
- 命令：`> timeline`
- 底部弹出时间轴，显示代码的历史变更
- 左右滑动查看不同版本
- 点击时间点可对比差异

### 10.3 AI 副驾驶面板
- 命令：`@ 解释这段代码`
- 右侧滑出半透明面板
- AI 的解释以对话气泡形式显示
- 支持代码示例的交互式编辑

### 10.4 专注模式 (Focus Mode)
- 命令：`> focus`
- 隐藏所有 UI 元素，只保留代码
- 当前行居中显示，其他行淡化
- 背景显示微妙的空间网格

---

## 11. 示意图

### 11.1 整体界面草图

```
┌────🟡🟠🟢─── Golden Editor ───────────────────────────────┐
│  丝状宝石光泽背景                                         │
│  ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱ │
│  ┌───────┐  ┌──────────────────────────────────┬───────┐ │
│  │◀▶     │  │  main.js  ┃  utils.js  [+]  🔍   │  ◇    │ │
│  │ ╱╱╱╱╱ │  ├──────────────────────────────────┴───────┤ │
│  │  📁   │  │                                         │ │
│  │  📄   │  │    ┌─────────────────────────────┐      │ │
│  │  📄   │  │    │  function hello() {         │      │ │
│  │  📄 ╱ │  │    │    console.log("Hello");  ◀───🟨   │ │
│  │  📄   │  │    │  }                          │      │ │
│  │       │  │    │                             │      │ │
│  │ ╱╱╱╱╱ │  │    │  // 更多代码...              │      │ │
│  │       │  │    └─────────────────────────────┘      │ │
│  │       │  │                                         │ │
│  │       │  │  > git commit ─────────────── 🌊       │ │
│  └───────┘  └─────────────────────────────────────────┘ │
│                                                           │
│  行 42, 列 15  │  UTF-8  │  JavaScript  │  🟨  暗黑  │  ⎋  │
└───────────────────────────────────────────────────────────┘

图例:
🟡🟠🟢 = macOS 红绿灯按钮
◀▶    = 空间导航面板收缩按钮
🟨    = 金边高亮（当前行）
◇     = 上下文面板开关
🌊    = 水流光带效果
⎋     = LEAP 按钮
╱╱╱   = 丝状宝石光泽纹理
```

### 11.2 缩放级别示意

```
[10% 视图 - 项目鸟瞰图]
┌─────────────────────────────────────────┐
│  📦 src/                                │
│    ├── 📄 main.js ────────┐             │
│    ├── 📄 utils.js        │ 连接线显示  │
│    └── 📄 config.js ◄─────┘  文件关系   │
│  📦 tests/                              │
└─────────────────────────────────────────┘

[60% 视图 - 代码结构]
┌─────────────────────────────────────────┐
│  function init() {                      │
│  ┌─────────────────────────────────┐    │
│  │  function setup() {             │    │
│  │    // ...                       │    │
│  │  }                              │    │
│  │  ┌───────────────────────────┐  │    │
│  │  │  class Processor {        │  │    │
│  │  │    process() { }          │  │    │
│  │  │  }                        │  │    │
│  │  └───────────────────────────┘  │    │
│  └─────────────────────────────────┘    │
│  function cleanup() {                   │
└─────────────────────────────────────────┘
```

---

## 12. 总结

这个 macOS 编辑器设计的核心创新点：

1. **空间导航系统**：打破传统的文件树结构，让用户在二维空间中直观地浏览和定位代码
2. **命令行融合**：底部的智能输入条将命令行效率与图形界面直观性结合
3. **科幻视觉风格**：深色主题 + 霓虹光效 + 玻璃拟态，营造未来感
4. **即时反馈**：所有操作都有视觉反馈，AI 助手随时待命

这是一个旨在降低编程入门门槛，同时提升专业开发者效率的编辑器设计。

---

## 13. 绘制检查清单

根据 `lucky实践` 的 AGENTS.md 规范，绘制前确认：

- [ ] Step 1: 平台已确认 (macOS)
- [ ] Step 2: 配色已选择 (自定义科幻)
- [ ] Step 3: 方案已选择 (玻璃拟态)
- [ ] Step 4: 页面类型已确认 (编辑器主界面)
- [ ] Step 5: 画布空白位置已检查
- [ ] Step 6: 用户已确认 (y/n)

**排版注意**：
- [ ] 不使用 lineHeight
- [ ] 使用固定高度容器
- [ ] 精确计算总高度
