# 测试驱动开发技能 - 从需求0224总结

## 核心原则

### 1. 先写测试，再分析代码
- **不要**先看代码猜测问题
- **要**先写测试验证行为
- 测试比代码分析更可靠

### 2. 用Qt默认类做Demo
- 测试时继承Qt默认类（如QGraphicsTextItem）
- 只打印log，不执行实际业务逻辑
- 避免引入业务复杂度干扰测试

```python
class TestTextItem(QGraphicsTextItem):
    def mousePressEvent(self, event):
        print(f'[mousePressEvent] text="{self.toPlainText()}"')
        print(f'  isSelected={self.isSelected()}, hasFocus={self.hasFocus()}')
        # 不调用super，不执行实际代码
```

### 3. 分步骤验证
不要一次性测试复杂流程，先分别验证：
1. 单击A是否正常
2. 单击B是否正常
3. 双击A是否正常
4. 最后再组合测试

### 4. 事件坐标要实时计算
**错误做法：**
```python
a_vp = view.mapFromScene(a.scenePos())  # 缓存坐标
# ... 执行某些操作（可能导致视图滚动）
QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=a_vp)  # 使用过期坐标
```

**正确做法：**
```python
# 每次点击前重新计算坐标
click_pos = view.mapFromScene(target.scenePos())
QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=click_pos)
```

### 5. 通过测试和log找问题
- 不要直接看代码猜测
- 先让测试跑起来，看log输出
- 根据log确定问题范围，再分析代码

## 常见陷阱

### 陷阱1: 视图滚动导致坐标失效
当节点进入编辑态时，如果调用了`ensureVisible()`，视图会滚动，之前计算的视口坐标会失效。

**解决方案:**
- 每次点击前重新计算`mapFromScene()`
- 或者禁用`ensureVisible()`进行测试

### 陷阱2: 事件拦截误判
以为是事件拦截问题，实际是坐标问题。

**验证方法:**
- 在`mousePressEvent`中打印`self.toPlainText()`
- 确认实际接收者是谁

### 陷阱3: QApplication单例限制
不能多次创建QApplication。

**解决方案:**
```python
app = QApplication.instance() or QApplication([])
```

## 测试脚本模板

```python
#!/usr/bin/env python3
"""测试脚本模板"""
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PySide6.QtCore import Qt, QPoint
from PySide6.QtTest import QTest


class TestItem(QGraphicsTextItem):
    """只打印log的测试用Item"""
    
    def __init__(self, text):
        super().__init__(text)
        self.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsTextItem.GraphicsItemFlag.ItemIsFocusable, True)
    
    def _print_state(self, event_name):
        print(f'  [{event_name}] text="{self.toPlainText()}"')
        print(f'    isSelected={self.isSelected()}, hasFocus={self.hasFocus()}')
    
    def mousePressEvent(self, event):
        self._print_state('mousePressEvent')
        # 不调用super，不执行实际代码
    
    def focusInEvent(self, event):
        self._print_state('focusInEvent')
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        self._print_state('focusOutEvent')
        super().focusOutEvent(event)


def run_test():
    app = QApplication.instance() or QApplication([])
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    view.resize(800, 600)
    
    # 创建测试item
    a = TestItem('AAAAAA')
    b = TestItem('BBBBBB')
    a.setPos(100, 100)
    b.setPos(300, 100)
    scene.addItem(a)
    scene.addItem(b)
    
    # 每次点击前重新计算坐标
    click_a = lambda: QTest.mouseClick(
        view.viewport(), Qt.LeftButton, 
        pos=view.mapFromScene(a.scenePos())
    )
    click_b = lambda: QTest.mouseClick(
        view.viewport(), Qt.LeftButton,
        pos=view.mapFromScene(b.scenePos())
    )
    
    # 执行测试
    print('=== 单击A ===')
    click_a()
    
    print('\n=== 单击B ===')
    click_b()
    
    # 验证结果
    success = b.isSelected() and not a.isSelected()
    print(f'\n{"✅ PASS" if success else "❌ FAIL"}')


if __name__ == '__main__':
    run_test()
```

## 调试流程

1. **写测试** - 用最简单的Qt类重现问题
2. **加log** - 在事件处理函数中打印状态
3. **跑测试** - 看log输出，确认实际行为
4. **找问题** - 根据log定位问题
5. **修代码** - 修改后再跑测试验证
6. **更新测试** - 把测试加入回归测试套件

## 测试代码正确性检查（需求0225教训）

### 黄金法则：先怀疑测试代码，再怀疑被测功能

当测试失败时，按以下顺序排查：

1. **触发方式是否正确**
   ```python
   # ❌ 错误：直接调用API不会触发事件
   a.setFocus()  # 不会触发focusInEvent
   
   # ✅ 正确：模拟用户操作
   QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=pos)  # 触发完整事件链
   ```

2. **坐标是否实时计算**
   ```python
   # ❌ 错误：缓存坐标可能在视图滚动后失效
   a_vp = view.mapFromScene(a.scenePos())  # 缓存
   QTest.mouseClick(..., pos=a_vp)  # A被选中后视图可能滚动
   QTest.mouseClick(..., pos=b_vp)  # ❌ 坐标已失效！
   
   # ✅ 正确：每次点击前重新计算
   QTest.mouseClick(..., pos=view.mapFromScene(a.scenePos()))
   QTest.mouseClick(..., pos=view.mapFromScene(b.scenePos()))
   ```

3. **监控是否足够全面**
   ```python
   # ❌ 错误：只监控目标事件
   def focusInEvent(self, event): ...
   
   # ✅ 正确：同时监控触发事件和中间状态
   def mousePressEvent(self, event):
       print(f'[{self.name}] mousePress hasFocus={self.hasFocus()}')
       print(f'  itemAt={self.scene().views()[0].itemAt(pos)}')  # 确认点到了谁
       super().mousePressEvent(event)
   
   def focusInEvent(self, event):
       print(f'[{self.name}] focusInEvent')
   ```

4. **是否过早下结论**
   - ❌ "offscreen平台不支持focus事件"
   - ✅ "测试代码可能有bug，让我检查触发方式和坐标计算"

### 多平台验证

当怀疑是平台限制时：
```bash
# 1. 先用GUI平台验证基本功能
QT_QPA_PLATFORM=cocoa python3 test.py

# 2. 再用offscreen验证
QT_QPA_PLATFORM=offscreen python3 test.py

# 3. 对比差异，定位平台相关问题
```

## 经验教训

| 错误做法             | 正确做法                            |
| -------------------- | ----------------------------------- |
| 直接看代码猜测问题   | 先写测试验证行为                    |
| 用业务类（Node）测试 | 用Qt默认类（QGraphicsTextItem）测试 |
| 缓存视口坐标         | 每次点击前重新计算坐标              |
| 一次性测试复杂流程   | 分步骤分别测试                      |
| 直接调用函数测试     | 用QTest模拟真实点击                 |
| 测试失败就分析功能   | 先检查测试代码是否正确              |
| 单点监控             | 多点监控（mouse + focus + itemAt）  |
| 过早下结论           | 多平台验证后再下结论                |
