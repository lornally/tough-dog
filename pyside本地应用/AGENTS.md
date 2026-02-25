# uni5 AGENTS.md

> 节点编辑器统一版 uni5 - 开发知识库
> 版本: uni5 | 测试: 215/215 ✅ | 最后更新: 2026-02-24

---

## 核心原则（来自上级原则.md）

### 沟通原则
1. **第一原则**: 有啥疑问先沟通，不要闷头搞，沟通清楚再搞
2. **第二原则**: 确认的事项都要通过文档确认，不要直接对话问
3. **第三原则**: 确认的原则要更新到 agents.md 或添加为 skill，确认的需求要补充到需求文档，确认的 bug 要添加测试脚本/回归测试

### 沟通规范
- 尽量用文本沟通，而不是在 terminal 里面直接输出
- 修改要写修改申请，需求要写需求确认，测试也要形成文档
- 经验要及时总结到 agents.md 和其他相关文档
- 不要删除用户提出的问题，答复单独开文档
- 正面回答问题，不要回避问题

### 代码命名原则
1. **尽量简短**，中文或英文不重要，重要的是简短
2. **有大写字母就是不合法的**
3. **有非头部的下划线就是不合法的**（`_xx` 合法，`_xx_yy` 不合法）
4. **混合中英文是推荐的做法**，如 `is节点`, `快捷id`

### 版本规范
- 修改 bug: 升级小版本号（v1 → v1a）
- 新功能: 升级主版本号（v1 → v2）
- 既有 bug 修复又有新功能: 升级主版本号

### 测试驱动原则
1. 除非明确是生产版本，否则都是调试版本，保留各种状态 log 的测试代码
2. 用 `if 开调试:` 控制，而不是硬删除测试 log 代码
3. 尽量用 QTest 模拟测试，模拟操作行为，喷 log 看状态
4. 测试优先考虑的是**复现问题**，是为什么之前没有测试出来

---







## 测试体系




## 测试能力增强（关键教训）

### ❌ 之前的测试问题

| 问题           | 影响                                           | 案例                                               |
| -------------- | ---------------------------------------------- | -------------------------------------------------- |
| 直接调用方法   | 绕过事件系统，无法发现事件处理bug              | `node.mousePressEvent(event)` 没发现视图层命名错误 |
| 测试环境不一致 | 使用plain QApplication，没覆盖`应用`类特有方法 | 关闭窗口时报错（`close_window` vs `关窗`）         |
| 无源码检查     | 重构时遗漏调用点                               | `closeEvent`中方法名未同步                         |
| 无样式验证     | 无法发现样式不生效问题                         | 新栏样式不更新                                     |

### ✅ 测试改进方案

```python
# 1. 使用 QTest 模拟真实操作（而非直接调用）
# ❌ 错误
def test_click(self):
    node.mousePressEvent(event)  # 绕过视图层

# ✅ 正确
def test_click(self):
    QTest.mouseClick(viewport, button, modifier, pos)  # 走完整Qt事件

# 2. 源码静态检查（方法名验证）
def test_window_close(self):
    source = inspect.getsource(窗口.closeEvent)
    self.assertNotIn("close_window", source)  # 验证无英文方法名
    self.assertIn("关窗", source)              # 验证有中文方法名

# 3. 实际值验证（日志输出）
def test_tab_color(self):
    style = tab.styleSheet()
    # 解析并输出实际颜色值
    print(f"背景色: {bg_color}")  # 日志可见
    self.assertNotEqual(style1, style2)  # 验证确实不同

# 4. 跨窗口隔离测试
def test_multi_window(self):
    win1, win2 = 窗口(), 窗口()
    # 验证两个窗口的状态互不影响
```


## 调试黄金法则

### 遇到问题的标准流程

1. **能否稳定复现？**
2. **添加详细日志**（使用 `jdi()` 函数）
3. **对比正常/异常状态**（关键！）
4. **最小化复现**
5. **单点修复**（不瞎猜）
6. **验证并运行回归测试**

### 调试检查清单

```markdown
- [ ] 能否稳定复现？
- [ ] 添加详细日志
- [ ] 对比正常/异常状态
- [ ] 最小化复现
- [ ] 单点修复
- [ ] 验证并运行回归测试
```

---

## 历史教训

### 教训1：命名不一致导致运行时错误

**问题**：uni3 重构时，部分方法调用点未同步改为中文
```python
# win.py 中
self._app.close_window(self)  # ❌ 实际方法是 关窗()

# view.py 中
node.exit_edit_mode()         # ❌ 实际方法是 退编辑()
```

**解决**：
1. 添加源码检查测试
2. 使用 IDE 全局替换而非手动修改
3. 运行时捕获 AttributeError 并提示方法名错误

### 教训2：逻辑bug——提前返回

**问题**：`设当前栏()` 中的提前返回导致新栏样式不更新
```python
def 设当前栏(self, view):
    if self._栏 == view:  # ❌ 新栏创建时条件成立，提前返回
        return
    self._栏 = view
    for v in self._views:
        v.置栏样式(v == view)  # ❌ 这行没执行
```

**解决**：
1. 删除提前返回，确保样式始终更新
2. 添加边界条件测试（新栏创建后验证样式）

### 教训3：测试环境不一致

**问题**：测试使用 plain QApplication，实际使用 `应用` 类
```python
# 测试中
self.app = QApplication([])  # ❌ 不是 应用 类

# 实际运行
app = 应用([])  # 有 关窗() 等方法
```

**解决**：
1. 集成测试使用与生产环境相同的类
2. 添加源码级别的静态检查

---

## 代码规范


### 关键注释标记
```python
# 【uni3】uni3版本新增/修改
# 【v27c】v27c版本修复
# 【关键】关键逻辑说明
# 【教训】历史bug提醒
```

---

## 开发流程

### 1. 需求确认
- 所有需求必须通过 `需求.md` 确认
- 修改前创建 `修改申请_*.md` 文档

### 2. 测试驱动开发
```bash
# 新功能
1. 添加测试（先失败）
2. 实现功能（让测试通过）
3. 运行所有测试确保无回归

# Bug修复
1. 添加回归测试（复现bug）
2. 修复bug（让测试通过）
3. 运行所有测试
```

### 3. 文档更新
修改后必须更新：
- `AGENTS.md` - 项目知识库
- `README.md` - 使用说明
- `需求.md` - 需求答复
- `项目总结.md` - 历史记录

---




---

## 测试驱动开发教训（需求0224）

### 核心原则
1. **先写测试，再分析代码** - 不要猜测，用测试验证
2. **用Qt默认类做Demo** - 避免业务复杂度干扰
3. **分步骤验证** - 先分别测试，再组合
4. **坐标实时计算** - 每次点击前重新`mapFromScene()`
5. **通过log找问题** - 让测试跑起来，看log输出

### 本次关键发现
- 问题根源：`进编辑()`中`ensureVisible()`导致视图滚动，坐标失效
- 事件拦截猜测错误：实际事件分发正常，是坐标问题




# 节点编辑器统一版 - AGENTS.md


---



## 快速开始

### 环境要求

- Python 3.x
- PySide6 (`pip install pyside6`)






## 关键文档

| 文档           | 位置                       | 说明                               |
| -------------- | -------------------------- | ---------------------------------- |
| **开发知识库** | `uni5/AGENTS.md`           | 架构、命名规范、调试指南、教训总结 |
| **使用说明**   | `uni5/README.md`           | 快速开始、功能清单、快捷键         |
| **需求汇总**   | `uni5/需求汇总.md`         | 完整需求与设计文档                 |
| **项目历史**   | `uni5/项目历史.md`         | 版本历史记录                       |
| **问题总结**   | `uni5/汇报文档_uni5_v1.md` | 问题总结与避免机制                 |

---

## 核心教训（必读）

### 1. 测试必须用 QTest + offscreen

```python
# ❌ 错误 - 直接调用方法，绕过事件系统
def test_click(self):
    node.mousePressEvent(event)

# ✅ 正确 - QTest 模拟真实用户操作
def test_click(self):
    QTest.mouseClick(viewport, button, modifier, pos)

# ✅ 界面测试 - offscreen 平台 + 像素分析
def test_style(self):
    # QT_QPA_PLATFORM=offscreen
    pixmap = view.grab()
    img = pixmap.toImage()
    # 分析像素颜色
```

### 2. 简单优先原则

```python
# ❌ 错误 - 复杂自定义样式
self.setStyleSheet("""
    QScrollBar:vertical { ... }
    QScrollBar::handle { ... }
    QScrollBar::corner { ... }
    ... 20+ 行
""")

# ✅ 正确 - ppp/uni0 简单样式
self.setStyleSheet("QGraphicsView { background: transparent; border: none; }")
```

### 3. 防御代码审查

```python
# ❌ 错误 - 堆砌防御代码
for node in all_nodes:
    if node.hasFocus():
        node.clearFocus()
    if node.flags() != NoTextInteraction:
        node.setFlags(NoTextInteraction)
    if node.在编辑():
        node.退编辑()

# ✅ 正确 - 精简逻辑，依赖 Qt 自然机制
for node in self.取编辑中节点们():
    node.退编辑(to_normal=False)
```

### 4. 界面测试验证

```python
# ✅ 滚动条白线测试
def test_corner_no_white_pixel(self):
    pixmap = view.grab()
    img = pixmap.toImage()
    
    white_count = 0
    for x in range(w-20, w):
        for y in range(h-20, h):
            color = img.pixelColor(x, y)
            if color.red() > 200 and color.green() > 200 and color.blue() > 200:
                white_count += 1
    
    white_ratio = white_count / 400
    self.assertLess(white_ratio, 0.05)  # 白线比例 < 5%
```

---


## 调试黄金法则

1. **先打log，再分析** - 不要猜测
2. **对比状态，找差异** - 正常 vs 异常
3. **单点修复，不瞎猜** - 基于证据
4. **保留调试代码** - 调试阶段保留所有日志开关
5. **先怀疑测试代码** - 测试失败时，先检查测试代码是否正确，再怀疑被测功能（需求0225教训）

---

## 问题避免机制

1. **简单优先原则** - 首先尝试与 ppp/uni0 保持一致的方案
2. **offscreen 自动化测试** - 所有界面样式问题必须通过 offscreen 测试
3. **防御代码审查** - 定期审查"防御性"逻辑，问自己："这是解决根本问题，还是掩盖问题？"
4. **版本冻结与回退** - 每个版本都有明确基线，能够快速回退

---

## 文档维护原则

- 确认的原则 → AGENTS.md / skill
- 确认的需求 → 需求汇总.md
- 确认的版本 → 项目历史.md
- 确认的bug → 测试脚本/回归测试

---

## 测试驱动开发 - 从需求0224总结

### 核心教训

| #   | 教训                 | 说明                                                     |
| --- | -------------------- | -------------------------------------------------------- |
| 1   | 先写测试，再分析代码 | 不要先看代码猜测问题，要先写测试验证行为                 |
| 2   | 用Qt默认类做Demo     | 测试时继承QGraphicsTextItem，只打印log，不引入业务复杂度 |
| 3   | 分步骤验证           | 先分别测试单击、双击，再组合测试                         |
| 4   | 坐标要实时计算       | 每次点击前重新调用`mapFromScene()`，不能缓存             |
| 5   | 通过log找问题        | 让测试跑起来，看log输出，再分析代码                      |

### 关键Bug案例

**问题1**: 双击A后单击B，B无法被选中
**原因**: `进编辑()`中调用`ensureVisible()`导致视图滚动，之前缓存的B视口坐标失效
**解决**: 每次点击前重新计算`view.mapFromScene(item.scenePos())`

**问题2**: 误以为"offscreen平台不支持focusOutEvent"（需求0225）
**原因**: 
1. 使用`setFocus()`直接设置焦点（不会触发focus事件）
2. 坐标缓存导致第二次点击没点到目标
**解决**: 
1. 使用`QTest.mouseClick()`模拟真实点击
2. 每次点击前重新计算坐标
3. 同时监控mousePress/mouseRelease/focusIn/focusOut多个事件
**教训**: 测试失败时先检查测试代码，不要过早下结论

### 测试脚本规范

```python
# 正确做法 - 每次点击前重新计算坐标
click_pos = view.mapFromScene(target.scenePos())
QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=click_pos)

# 错误做法 - 缓存坐标可能导致失效
click_pos = view.mapFromScene(target.scenePos())  # 缓存
... # 某些操作导致视图滚动
QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=click_pos)  # 坐标已失效
```

### 测试代码正确性检查清单

当测试失败时，按以下顺序排查：

1. **触发方式是否正确**
   ```python
   # ❌ 直接调用API不会触发事件
   a.setFocus()  # 不会触发focusInEvent
   
   # ✅ 模拟用户操作
   QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=pos)
   ```

2. **坐标是否实时计算**
   ```python
   # ❌ 缓存坐标可能失效
   a_vp = view.mapFromScene(a.scenePos())  # 缓存
   QTest.mouseClick(..., pos=a_vp)  # A被选中后视图滚动
   QTest.mouseClick(..., pos=b_vp)  # ❌ 坐标已失效
   
   # ✅ 每次点击前重新计算
   QTest.mouseClick(..., pos=view.mapFromScene(a.scenePos()))
   QTest.mouseClick(..., pos=view.mapFromScene(b.scenePos()))
   ```

3. **监控是否足够全面**
   ```python
   # ❌ 只监控目标事件
   def focusInEvent(self, event): ...
   
   # ✅ 同时监控触发事件和中间状态
   def mousePressEvent(self, event):
       print(f'[{self.name}] mousePress')
       print(f'  itemAt={view.itemAt(pos)}')  # 确认点到了谁
   ```

4. **是否过早下结论**
   - ❌ "offscreen平台不支持focus事件"
   - ✅ "测试代码可能有bug，让我检查触发方式和坐标"



### skill文档
SKILL.md
TESTING_SKILL.md