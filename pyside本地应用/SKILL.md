# 测试构造技能

## 核心原则：测试代码正确性优先

当测试失败时，**先怀疑测试代码，再怀疑被测功能**。

---

## 错误案例分析：需求0225

### 现象
测试显示 "offscreen平台不支持focusOutEvent"，结论是错的。

### 真实原因
1. 使用`setFocus()`直接设置焦点（不会触发focus事件）
2. 坐标缓存导致第二次点击没点到目标
3. 只监控focus事件，不知道鼠标事件是否正常触发


## 测试代码正确性检查清单

### 1. 触发方式是否正确

```python
# ❌ 错误：直接调用API不会触发事件链
a.setFocus()          # 不会触发focusInEvent
a.setSelected(True)   # 不会触发selectionChanged

# ✅ 正确：模拟用户操作触发完整事件链
QTest.mouseClick(view.viewport(), Qt.LeftButton, pos=pos)  # 触发mousePress/Release/focus
```

### 2. 坐标是否实时计算

```python
# ❌ 错误：缓存坐标可能在视图滚动后失效
a_vp = view.mapFromScene(a.scenePos())  # 缓存
QTest.mouseClick(..., pos=a_vp)  # A被选中后视图可能滚动
QTest.mouseClick(..., pos=b_vp)  # ❌ 坐标已失效

# ✅ 正确：每次点击前重新计算
QTest.mouseClick(..., pos=view.mapFromScene(a.scenePos()))
QTest.mouseClick(..., pos=view.mapFromScene(b.scenePos()))
```

### 3. 监控是否足够全面

```python
# ❌ 错误：只监控目标事件
class TestItem(QGraphicsTextItem):
    def focusInEvent(self, event):
        print('focusInEvent')

# ✅ 正确：同时监控触发事件和中间状态
class TestItem(QGraphicsTextItem):
    def mousePressEvent(self, event):
        print(f'mousePress: itemAt={self.scene().views()[0].itemAt(event.pos())}')
        super().mousePressEvent(event)
        
    def focusInEvent(self, event):
        print('focusInEvent')
        super().focusInEvent(event)
        
    def focusOutEvent(self, event):
        print('focusOutEvent')
        super().focusOutEvent(event)
```

### 4. 是否过早下结论

| 过早结论 | 正确做法 |
|---------|---------|
| "offscreen平台不支持focus事件" | "测试代码可能有bug，检查触发方式和坐标" |
| "Qt有bug" | "我的测试代码可能有bug" |
| "功能不能实现" | "先检查测试代码3遍" |

---

## 多平台验证

当怀疑是平台限制时：

```bash
# 1. 先用GUI平台验证基本功能
QT_QPA_PLATFORM=cocoa python3 test.py

# 2. 再用offscreen验证
QT_QPA_PLATFORM=offscreen python3 test.py

# 3. 对比差异，定位平台相关问题
```

---

## 一句话教训

> **"不是功能不能实现，是你的测试代码写得不对。"**

下次再说"xxx不能实现"之前，先：
1. 检查触发方式是否正确（模拟用户操作 vs 直接API调用）
2. 检查坐标/状态是否实时计算
3. 检查是否监控了足够的事件来定位问题
