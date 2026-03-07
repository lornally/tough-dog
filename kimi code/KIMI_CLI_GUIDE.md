# Kimi Code CLI 使用指南

> 本文档按使用场景分类，方便快速查找。

---

## 一、交互模式（默认，最常用）

### 1.1 基础对话
```sh
# 进入交互式会话
kimi

# 指定工作目录（默认是当前目录）
kimi -w /path/to/project

# 添加额外的目录到工作区
kimi --add-dir /path/to/another/dir
```

**适用场景**：日常开发、代码审查、问题排查。

### 1.2 继续会话
```sh
# 继续上一次的会话
kimi -C

# 或者
kimi --continue

# 指定会话 ID 恢复特定会话
kimi -S <session_id>
```

**适用场景**：之前的对话没处理完，下次接着聊。

### 1.3 思考模式
```sh
# 强制开启思考模式（让 Kimi 更仔细地分析问题）
kimi --thinking

# 关闭思考模式（更快响应）
kimi --no-thinking
```

**适用场景**：复杂问题用 `--thinking`，简单问题用 `--no-thinking` 提速。

---

## 二、非交互模式（脚本/自动化）

### 2.1 单次执行（Print 模式）
```sh
# 直接执行命令并退出（不需要确认）
kimi --print -p "分析 main.py 的代码质量"

# 处理文件内容
kimi --print -p "优化这段代码" < main.py

# 管道输入
cat README.md | kimi --print -p "总结这个文档"
```

**适用场景**：脚本集成、批量处理、CI/CD 流程。

### 2.2 静默模式
```sh
# 只输出最终结果，不显示中间过程
kimi --quiet -p "提取 package.json 中的依赖列表"

# 等价于
kimi --print --output-format text --final-message-only -p "..."
```

**适用场景**：只需要结果，不想看思考过程的自动化任务。

### 2.3 自动确认模式
```sh
# 自动批准所有操作（等同于输入 y）
kimi --yolo -p "重构当前目录的所有 Python 文件"

# 或者
kimi -y -p "删除所有临时文件"
```

⚠️ **警告**：使用 `--yolo` 前确保你理解 Kimi 会执行什么操作。

**适用场景**：信任 Kimi 的操作，不想每次都按 `y` 确认。

---

## 三、TUI 界面模式

### 3.1 启动 TUI
```sh
# 启动 Toad TUI 界面
kimi term
```

**界面特点**：
- 类似传统终端 UI，支持键盘导航
- 会话历史可视化
- 文件树浏览

**适用场景**：喜欢用键盘操作、习惯 TUI 界面的用户。

---

## 四、Web 界面模式

### 4.1 启动 Web UI
```sh
# 启动 Web 界面并自动打开浏览器
kimi web

# 指定端口
kimi web --port 8080

# 允许局域网访问（其他设备可访问）
kimi web --network

# 指定 IP 地址
kimi web --host 192.168.1.100

# 禁用自动打开浏览器
kimi web --no-open
```

**适用场景**：
- 在浏览器中使用 Kimi
- 需要局域网内多台设备访问
- 喜欢图形界面

---

## 五、MCP 服务器管理

### 5.1 查看 MCP 配置
```sh
# 列出所有 MCP 服务器
kimi mcp list

# 测试 MCP 连接
kimi mcp test <server_name>
```

### 5.2 添加 MCP 服务器
```sh
# 添加 STDIO 类型 MCP
kimi mcp add <name> --command <command> --args <args>

# 示例：添加一个本地 MCP 服务器
kimi mcp add my-server --command node --args /path/to/server.js
```

### 5.3 删除 MCP 服务器
```sh
kimi mcp remove <server_name>
```

### 5.4 OAuth 授权
```sh
# 授权需要登录的 MCP
kimi mcp auth <server_name>

# 重置授权
kimi mcp reset-auth <server_name>
```

**适用场景**：
- 管理外部工具集成（如 Pencil、数据库工具等）
- 排查 MCP 连接问题

---

## 六、服务器模式（高级）

### 6.1 ACP 服务器
```sh
# 启动 ACP 服务器（供其他客户端接入）
kimi acp

# 其他客户端（如 VS Code）可以连接到这个服务器
```

**适用场景**：
- VS Code Kimi 扩展使用
- 第三方工具集成

### 6.2 Wire 服务器（实验性）
```sh
# 启动 Wire 服务器
kimi --wire
```

---

## 七、配置文件管理

### 7.1 使用自定义配置
```sh
# 指定配置文件
kimi --config-file /path/to/config.toml

# 直接传入配置 JSON
kimi --config '{"model": "kimi-k2"}'
```

### 7.2 配置文件位置
- 主配置：`~/.kimi/config.toml`（或 `.json`）
- MCP 配置：`~/.kimi/mcp.json`
- CLI 配置：`~/.config/kimi-cli/config.json`

---

## 八、模型和参数设置

### 8.1 指定模型
```sh
# 使用特定模型
kimi -m kimi-k2

# 或者
kimi --model kimi-k2
```

### 8.2 调整执行参数
```sh
# 限制每轮最大步数
kimi --max-steps-per-turn 50

# 限制重试次数
kimi --max-retries-per-step 3

# Ralph 模式迭代次数（-1 为无限制）
kimi --max-ralph-iterations 10
```

---

## 九、实用组合案例

### 案例 1：批量代码审查
```sh
#!/bin/bash
for dir in */; do
    echo "审查 $dir..."
    kimi --quiet -p "审查 $dir 的代码质量并给出建议" -w "$dir" >> review_report.txt
done
```

### 案例 2：生成项目文档
```sh
# 读取整个项目，生成 README
kimi --yolo --print -p "根据代码生成完整的 README.md 文档" > README.md
```

### 案例 3：自动化重构
```sh
# 自动重构并提交
cd my-project
kimi --yolo -p "重构所有不符合 PEP8 的 Python 文件"
git add -A
git commit -m "refactor: auto-fix by kimi"
```

### 案例 4：多目录分析
```sh
# 同时分析前端和后端代码
kimi -w ./frontend --add-dir ./backend -p "分析前后端接口是否一致"
```

### 案例 5：CI/CD 集成
```sh
# 在 CI 中检查代码
kimi --quiet --print -p "检查是否有潜在的安全问题" || exit 1
```

---

## 十、故障排查

### 10.1 调试模式
```sh
# 开启详细日志
kimi --debug

# 开启冗余输出
kimi --verbose
```

### 10.2 查看版本信息
```sh
kimi --version
kimi info
```

### 10.3 常见错误排查
```sh
# 运行诊断脚本（如果已创建）
./kimi-doctor.sh

# 查看日志
cat ~/.kimi/logs/kimi.log
```

---

## 快速参考表

| 命令 | 作用 |
|------|------|
| `kimi` | 启动交互会话 |
| `kimi -C` | 继续上次的会话 |
| `kimi --print -p "..."` | 非交互执行 |
| `kimi --quiet -p "..."` | 静默执行 |
| `kimi --yolo -p "..."` | 自动确认执行 |
| `kimi term` | TUI 界面 |
| `kimi web` | Web 界面 |
| `kimi mcp list` | 查看 MCP 配置 |
| `kimi acp` | ACP 服务器 |
| `kimi -w <dir>` | 指定工作目录 |
| `kimi --thinking` | 开启思考模式 |
| `kimi --model <model>` | 指定模型 |
