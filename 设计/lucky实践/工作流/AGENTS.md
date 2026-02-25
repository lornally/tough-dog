# APP UI 绘制系统配置

本文档说明如何在Kimi Code CLI中集成APP UI绘制能力，通过Pencil MCP在画布上绘制移动端界面。

## ⚠️ 重要：交互式选择流程

**绘制UI时必须遵循以下流程：**

```
用户: 帮我画一个APP登录界面

Kimi:
1. 【列出Skills】展示所有可用的设计系统
2. 【等待选择】让用户选择平台/Skill
3. 【列出配色】询问颜色偏好（见下文配色方案选择）
4. 【列出方案】展示该Skill的多个设计方案
5. 【等待选择】让用户选择具体方案
6. 【确认】汇总选择，等待用户确认
7. 【检查画布】使用find_empty_space_on_canvas检查空白位置
8. 【执行】只有确认后才开始绘制
```

**不要**在没有用户明确选择的情况下直接开始绘制！

## ⚠️ 画布管理规范

**每次绘制前必须执行：**

```javascript
// 1. 检查画布上的现有内容
snapshot_layout({maxDepth: 1})

// 2. 查找空白位置
find_empty_space_on_canvas({
  width: 400,    // 根据平台调整
  height: 900,   // 根据平台调整
  padding: 50,
  direction: "right"  // 或 "bottom"
})

// 3. 将新界面放置在空白位置，避免重叠
// 如果返回 {x: 443, y: 0}，则设置 screen.x = 443
```

**禁止**：直接将新界面绘制在 (0,0)，这会导致与已有界面重叠！

## 📊 图表绘制规范（更新）

### 默认方案：Pencil基础形状（可编辑）

**优先使用Pencil基础形状绘制图表**，保证可编辑性：

```javascript
// 饼图示例：用圆形+扇形路径
pieChart=I(container, {
  type: "frame",
  width: 120,
  height: 120,
  fill: "#FFC107", // 主色
  cornerRadius: 60 // 圆形
})

// 图例用矩形+文字
legend=I(container, {
  type: "frame",
  layout: "horizontal",
  gap: 8
})

I(legend, {
  type: "frame",
  width: 12,
  height: 12,
  fill: "#FFC107" // 色块
})

I(legend, {
  type: "text",
  content: "现金 35%",
  fontFamily: "Roboto",
  fontSize: 12
})
```

### 备选方案：AntV图表图片（专业美观）

**当用户明确要求专业美观效果时**，可使用AntV生成图表图片：

```
1. 询问用户："需要生成专业图表图片吗？（默认使用可编辑简化版）"
2. 用户确认后，使用AntV MCP生成
3. 明确告知："此图表为图片生成，不可编辑"
```

### 安装路径
```
skills/antv-mcp-server/
```

### 支持的图表类型（26种）
- **饼图/环形图** - 部分与整体关系
- **柱状图** - 类别对比
- **折线图** - 趋势展示
- **雷达图** - 多维数据
- 等等...

### 方案对比

| 场景 | 推荐方案 | 说明 |
|------|---------|------|
| **默认情况** | Pencil基础形状 | 可编辑，便于修改 |
| 专业美观 | AntV图表图片 | 效果好但不可编辑 |
| 用户要求编辑 | Pencil基础形状 | 唯一可编辑方案 |

### 重要提示
- **默认可编辑**：优先保证用户能修改调整
- **图片作为备选**：仅在用户要求专业效果时使用
- **明确告知限制**：使用图片前必须说明不可编辑

## ⚠️ 配色方案选择（新增）

**必须在选择设计方案前，询问用户颜色偏好：**

```
🎨 选择配色方案：

1. 【科技蓝】#007AFF / #0A84FF
   适用：通用APP、科技产品
   
2. 【财富金】#FFC107 / #F59E0B
   适用：金融、财富管理、高端服务
   
3. 【健康绿】#34C759 / #30D158
   适用：健康、运动、环保
   
4. 【热情红】#FF3B30 / #FF453A
   适用：电商、促销、社交
   
5. 【神秘紫】#AF52DE / #BF5AF2
   适用：创意、娱乐、艺术
   
6. 【自定义】用户提供具体色值

请选择一个（输入数字1-6）：
```

## ⚠️ 状态栏规范

**iOS状态栏必须包含：**
- 时间（9:41或当前时间）
- 信号图标（可选）
- WiFi图标（可选）
- 电池图标（可选）

**Android状态栏必须包含：**
- 时间
- 符合Material Design的系统图标

**禁止**：只显示简单的时间文本！

正确示例：
```javascript
// iOS标准状态栏
statusBar=I(screen, {
  type: "frame",
  width: "fill_container",
  height: 44,
  padding: [0, 24],
  layout: "horizontal",
  justifyContent: "space_between",
  alignItems: "center"
})

// 左侧时间
I(statusBar, {
  type: "text",
  content: "9:41",
  fontFamily: "SF Pro",
  fontSize: 15,
  fontWeight: "600",
  fill: "#000000"
})

// 右侧系统图标区域
systemIcons=I(statusBar, {
  type: "frame",
  layout: "horizontal",
  gap: 4,
  alignItems: "center"
})

I(systemIcons, {
  type: "icon_font",
  iconFontFamily: "lucide",
  iconFontName: "signal",
  width: 16,
  height: 16,
  fill: "#000000"
})

I(systemIcons, {
  type: "icon_font",
  iconFontFamily: "lucide",
  iconFontName: "wifi",
  width: 16,
  height: 16,
  fill: "#000000"
})

I(systemIcons, {
  type: "icon_font",
  iconFontFamily: "lucide",
  iconFontName: "battery-full",
  width: 20,
  height: 20,
  fill: "#000000"
})
```

## 系统架构

```
[Kimi Code CLI]
├── Skill: pencil-ui-orchestrator (协调器)
│   └── 必须让用户选择Skill和方案后才绘制
├── Skill: platform-design-skills (第三方)
│   ├── ios-design-guidelines (多种方案)
│   ├── android-design-guidelines (多种方案)
│   └── ...
├── Skill: ui-ux-pro-max (已有)
│   └── 自动生成多个设计方案供选择
└── MCP: pencil
    └── 画布绘制
```

## 已集成的Skills

### 1. pencil-ui-orchestrator (协调器)
**路径**: `~/.config/agents/skills/pencil-ui-orchestrator/`

**核心职责**: 协调选择流程，必须：
1. 列出所有可用的设计系统Skills
2. 让用户选择平台和Skill
3. **询问颜色偏好（新增）**
4. 列出该Skill的多个设计方案
5. 让用户选择具体方案
6. **检查画布空白位置（新增）**
7. 确认后才开始绘制

### 2. platform-design-skills (第三方GitHub)
**路径**: `./skills/platform-design-skills/`
**来源**: https://github.com/ehmo/platform-design-skills

包含300+设计规则，每个平台有多个设计方案：

| 平台 | 可用方案 |
|------|----------|
| **iOS** | 标准浅色、暗黑模式、玻璃拟态 |
| **Android** | Material You、标准Material 3、暗黑主题 |
| **iPadOS** | 标准、多窗口、Stage Manager |
| **Web** | 响应式、可访问性优先、移动端优先 |

### 3. ui-ux-pro-max (已有)
**路径**: `./skills/ui-ux-pro-max/`

自动生成多个设计方案：
- 67种UI风格
- 96种配色方案
- 57种字体组合

## 正确的使用流程

### 步骤1: 用户发出请求
```
用户: 帮我画一个APP登录界面
```

### 步骤2: 列出可用的Skills
```
📱 可用的UI设计系统：

1. 【iOS】Apple Human Interface Guidelines
   适用: iPhone原生应用
   
2. 【Android】Material Design 3
   适用: Android原生应用

3. 【iPadOS】Apple HIG for iPad
   适用: iPad专用应用

4. 【Web】WCAG 2.2 + 响应式设计
   适用: Web应用

5. 【UI UX Pro Max】Web/Mobile设计系统
   适用: Web应用、跨平台应用
   
请选择一个（输入数字1-5）：
```

### 步骤3: 用户选择Skill
```
用户: 1
```

### 步骤4: 询问配色方案（新增）
```
您选择了【iOS】Apple Human Interface Guidelines。

🎨 选择配色方案：

1. 【科技蓝】#007AFF / #0A84FF
2. 【财富金】#FFC107 / #F59E0B
3. 【健康绿】#34C759 / #30D158
4. 【热情红】#FF3B30 / #FF453A
5. 【神秘紫】#AF52DE / #BF5AF2

请选择一个（输入数字1-5）：
```

### 步骤5: 列出该Skill的方案
```
您选择了【财富金】配色方案。

📋 可用设计方案：

1. 【标准iOS】浅色模式、系统默认颜色
2. 【暗黑模式】深色主题、OLED优化
3. 【玻璃拟态】半透明效果、现代感

请选择一个方案（输入数字）：
```

### 步骤6: 用户选择方案
```
用户: 2
```

### 步骤7: 选择页面类型
```
您选择了【暗黑模式】方案。

📄 选择页面类型：
1. 登录/注册
2. 首页/仪表盘
3. 列表/浏览
...

请选择一个：
```

### 步骤8: 检查画布空白位置（新增）
```
用户: 1

🎯 您的选择：
- 平台: iOS
- 设计系统: Apple HIG
- 配色: 财富金
- 方案: 暗黑模式
- 页面: 登录页

正在检查画布...
✅ 发现空白位置: x=443, y=0

确认开始绘制？(y/n)
```

### 步骤9: 确认并开始绘制
```
用户: y

AI: 开始执行绘制...
- 放置位置: (443, 0)
- 绘制状态栏（标准样式）
- 绘制内容区域...
```

## 测试记录

### 2024-02-09 测试 #1 - 财富管理APP登录界面

**问题发现**: 在测试中没有遵循交互式选择流程
- ❌ 没有列出Skills让用户选择
- ❌ 没有列出多个设计方案让用户选择
- ❌ 直接开始执行绘制

**正确做法**:
- ✅ 应该先列出所有5个Skill选项
- ✅ 用户选择后，列出该平台的所有设计方案
- ✅ 用户选择方案后，才开始绘制

**修复措施**:
已更新 `pencil-ui-orchestrator/SKILL.md`

---

### 2024-02-09 测试 #2 - Android资产管理界面

**问题发现 #1**: 画布重叠
- ❌ 新界面直接绘制在 (0,0)，与已有iOS界面重叠
- ❌ 没有使用 `find_empty_space_on_canvas` 检查空白位置

**正确做法**:
```javascript
// 检查空白位置
find_empty_space_on_canvas({
  width: 400,
  height: 900,
  direction: "right"
})
// 返回: {x: 443, y: 0}

// 放置新界面到空白位置
screen.x = 443
```

**问题发现 #2**: 缺少配色方案选择
- ❌ 直接使用了金色配色，没有询问用户偏好
- ❌ 应该提供6种标准配色供用户选择

**正确做法**:
- ✅ 在选择设计方案前，询问配色偏好
- ✅ 提供：科技蓝、财富金、健康绿、热情红、神秘紫、自定义

**问题发现 #3**: 状态栏样式不规范
- ❌ 只显示了简单的时间文本
- ❌ 缺少信号、WiFi、电池等系统图标

**正确做法**:
- ✅ iOS状态栏：时间(9:41) + 信号 + WiFi + 电池
- ✅ Android状态栏：时间 + 系统图标
- ✅ 使用水平布局，左右分布

**修复措施**:
1. 已移动Android界面到空白位置 (443, 0)
2. 已更新AGENTS.md，添加配色方案选择规范
3. 已更新AGENTS.md，添加状态栏规范
4. 已更新AGENTS.md，添加画布管理规范

## Pencil MCP 调用流程

### 1. 检查画布状态
```javascript
snapshot_layout({maxDepth: 1})
```

### 2. 查找空白位置
```javascript
find_empty_space_on_canvas({
  width: 400,
  height: 900,
  padding: 50,
  direction: "right"
})
```

### 3. 创建新画布或放置到空白位置
```javascript
// 设置新界面的位置
screen=I(document, {
  type: "frame",
  x: 443,  // 使用空白位置的x
  y: 0,
  ...
})
```

### 4. 生成并执行绘制操作
```javascript
batch_design({
  filePath: "...",
  operations: `
    screen=I(document, {type: "frame", name: "Screen", x: 443, ...})
    // ... 更多组件
  `
})
```

### 5. 验证结果
```javascript
get_screenshot({
  filePath: "...",
  nodeId: "screen-id"
})
```

## 支持的页面类型

| 页面类型 | 描述 |
|----------|------|
| 登录/注册 | Logo、输入框、按钮、社交登录 |
| 首页/仪表盘 | 导航、卡片、数据展示 |
| 列表/浏览 | 搜索、列表项、筛选 |
| 详情页 | 图片、内容、操作按钮 |
| 个人中心 | 头像、菜单、统计 |
| 设置页 | 开关、选项、分组 |

## 设计系统命令参考

### 读取Skill规范
```bash
cat skills/platform-design-skills/skills/ios/SKILL.md
cat skills/platform-design-skills/skills/android/SKILL.md
```

### 生成ui-ux-pro-max设计系统
```bash
python3 skills/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py "<query>" --design-system
```

## 注意事项

1. **必须交互式选择** - 不要假设用户选择，必须明确列出选项
2. **等待用户输入** - 每个选择步骤都要等待用户确认
3. **确认后再绘制** - 汇总所有选择，用户确认y后才执行
4. **检查画布位置** - 使用find_empty_space_on_canvas避免重叠
5. **询问配色方案** - 在选择设计方案前询问颜色偏好
6. **标准状态栏** - iOS/Android都需要完整的系统图标
7. **记录选择** - 在对话中记录用户的选择便于回溯

## 扩展计划

- [ ] 添加更多第三方Skills
- [ ] 创建设计系统模板库
- [ ] 支持导入自定义设计系统
- [ ] 添加设计版本管理
