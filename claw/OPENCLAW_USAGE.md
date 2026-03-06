# OpenClaw 使用文档

## 简介

OpenClaw 是一个自托管的 AI Agent 网关，连接你的聊天应用（WhatsApp、Telegram、Discord、iMessage 等）与 AI 编程助手。

---

## 安装状态

| 组件 | 版本 | 状态 |
|------|------|------|
| OpenClaw CLI | v2026.3.2 | ✅ 已安装 |
| Gateway | - | ✅ 运行中 |
| AI 模型 | Kimi K2.5 | ✅ 已连接 |
| API 端点 | api.moonshot.cn | ✅ 中国版 |

---

## 快速开始

### 1. 启动 Gateway

Gateway 是 OpenClaw 的核心服务，必须运行才能使用 AI 功能。

```bash
# 方式一：前台运行（查看日志）
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
openclaw gateway run --force

# 方式二：后台运行
openclaw gateway run --force > /tmp/openclaw.log 2>&1 &
```

### 2. 验证运行状态

```bash
# 检查健康状态
openclaw health

# 查看详细状态
openclaw status
```

### 3. 与 AI 对话

```bash
# 发送消息
openclaw agent --agent main --message "你好"

# 示例：让 AI 写代码
openclaw agent --agent main --message "用 Python 写一个计算斐波那契数列的函数"
```

---

## 常用命令

### 基础命令

| 命令 | 说明 |
|------|------|
| `openclaw health` | 检查 Gateway 健康状态 |
| `openclaw status` | 查看 Gateway 运行状态 |
| `openclaw dashboard` | 打开 Web 控制面板 |
| `openclaw --version` | 查看版本 |

### Agent 命令

| 命令 | 说明 |
|------|------|
| `openclaw agent --agent main --message "内容"` | 发送消息给 AI |
| `openclaw agent --agent main --message "内容" --session-id xxx` | 保持上下文对话 |

### 配置命令

| 命令 | 说明 |
|------|------|
| `openclaw config file` | 查看配置文件路径 |
| `openclaw config validate` | 验证配置是否正确 |
| `openclaw config get agents.defaults` | 查看默认配置 |
| `openclaw doctor` | 诊断和修复问题 |
| `openclaw doctor --fix` | 自动修复问题 |

### 模型命令

| 命令 | 说明 |
|------|------|
| `openclaw models list` | 列出内置模型 |
| `openclaw models list --all` | 列出所有可用模型 |
| `openclaw models status` | 查看模型配置状态 |

---

## 配置文件

配置文件位置：`~/.openclaw/openclaw.json`

### 当前配置（Kimi K2.5）

```json
{
  "agents": {
    "defaults": {
      "model": { 
        "primary": "moonshot/kimi-k2.5" 
      },
      "workspace": "/Users/mmm/.openclaw/workspace"
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.cn/v1",
        "apiKey": "sk-4uQa7r74VIeFwHAg7mKZKjDnHMmUJ0pBdsmM23yy4sO2yYkM",
        "api": "openai-completions",
        "models": [{
          "id": "kimi-k2.5",
          "name": "Kimi K2.5",
          "contextWindow": 256000,
          "maxTokens": 8192
        }]
      }
    }
  }
}
```

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `agents.defaults.model.primary` | 默认使用的 AI 模型 |
| `agents.defaults.workspace` | Agent 工作目录 |
| `models.providers` | 模型提供商配置 |
| `models.providers.moonshot.baseUrl` | Moonshot API 地址（中国版用 `api.moonshot.cn`）|
| `models.providers.moonshot.apiKey` | API 密钥 |

---

## Web 控制面板

启动 Gateway 后，可以通过浏览器访问控制面板：

- **地址**: http://127.0.0.1:18789/
- **功能**: 查看会话、发送消息、管理配置

```bash
# 打开控制面板
openclaw dashboard
```

---

## 实用技巧

### 1. 创建启动脚本

创建文件 `~/start-openclaw.sh`：

```bash
#!/bin/bash
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"

# 检查是否已在运行
if pgrep -f "openclaw-gateway" > /dev/null; then
    echo "OpenClaw 已在运行"
    openclaw health
    exit 0
fi

# 启动 Gateway
openclaw gateway run --force > /tmp/openclaw.log 2>&1 &
sleep 3

# 检查状态
if openclaw health > /dev/null 2>&1; then
    echo "✅ OpenClaw 启动成功"
    echo "Dashboard: http://127.0.0.1:18789/"
else
    echo "❌ 启动失败，查看日志: tail -f /tmp/openclaw.log"
fi
```

赋予执行权限：
```bash
chmod +x ~/start-openclaw.sh
```

### 2. 查看日志

```bash
# Gateway 日志
tail -f /tmp/openclaw.log

# 或者
tail -f /tmp/openclaw/openclaw-*.log
```

### 3. 停止 Gateway

```bash
# 查找并停止
pkill -f "openclaw-gateway"

# 或者使用 openclaw 命令
openclaw gateway stop
```

### 4. 切换模型

如需切换到其他模型（如 OpenRouter）：

```bash
# 设置模型
openclaw config set agents.defaults.model "openrouter/anthropic/claude-sonnet-4"

# 重启 Gateway
pkill -f "openclaw"
openclaw gateway run --force &
```

---

## 故障排除

### 问题 1：401 认证失败

**原因**: API 密钥无效或配置错误

**解决**:
```bash
# 检查密钥
openclaw models status

# 验证配置
openclaw config validate
```

### 问题 2：Gateway 无法启动

**原因**: 端口被占用

**解决**:
```bash
# 强制释放端口
openclaw gateway run --force

# 或者使用其他端口
openclaw gateway run --port 18800
```

### 问题 3：模型未找到

**原因**: 模型名称错误

**解决**:
```bash
# 查看可用模型
openclaw models list --all | grep moonshot
```

---

## 参考链接

- **官方文档**: https://docs.openclaw.ai/
- **模型提供商**: https://docs.openclaw.ai/concepts/model-providers
- **GitHub**: https://github.com/openclaw/openclaw

---

## 快捷键

| 操作 | 命令 |
|------|------|
| 启动 | `openclaw gateway run --force` |
| 停止 | `pkill -f "openclaw-gateway"` |
| 对话 | `openclaw agent --agent main --message "内容"` |
| 面板 | `openclaw dashboard` |
| 诊断 | `openclaw doctor` |

---

*文档生成时间: 2026-03-06*
*OpenClaw 版本: v2026.3.2*
*配置模型: Moonshot Kimi K2.5*
