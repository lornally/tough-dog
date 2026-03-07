#!/bin/bash
# Kimi Code CLI 健康检查脚本
# 用于诊断配置问题，避免手动排查

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo "=========================================="
echo "Kimi Code CLI 健康检查"
echo "=========================================="
echo ""

# 检查 Kimi 配置目录
KIMI_DIR="$HOME/.kimi"
KIMI_CONFIG="$KIMI_DIR/config.json"
KIMI_MCP="$KIMI_DIR/mcp.json"

echo "📁 检查 Kimi 配置目录..."
if [ -d "$KIMI_DIR" ]; then
    echo -e "${GREEN}✓${NC} 配置目录存在: $KIMI_DIR"
else
    echo -e "${YELLOW}⚠${NC} 配置目录不存在: $KIMI_DIR"
    ((WARNINGS++))
fi
echo ""

# 检查 mcp.json
echo "🔧 检查 MCP 配置..."
if [ -f "$KIMI_MCP" ]; then
    echo -e "${GREEN}✓${NC} MCP 配置文件存在: $KIMI_MCP"
    echo ""
    
    # 检查 JSON 格式
    if python3 -c "import json; json.load(open('$KIMI_MCP'))" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} JSON 格式正确"
    else
        echo -e "${RED}✗${NC} JSON 格式错误！请检查文件语法"
        ((ERRORS++))
    fi
    
    # 提取并检查每个 MCP 服务器路径
    echo ""
    echo "  检查 MCP 服务器路径..."
    
    # 获取所有命令路径
    MCP_COMMANDS=$(python3 -c "
import json
try:
    with open('$KIMI_MCP') as f:
        config = json.load(f)
    servers = config.get('mcpServers', {})
    for name, server in servers.items():
        cmd = server.get('command', '')
        args = server.get('args', [])
        # 如果是 node 或 python 运行某个脚本，检查第一个参数
        if cmd in ['node', 'python', 'python3'] and args:
            print(f'{name}|{args[0]}')
        else:
            print(f'{name}|{cmd}')
except Exception as e:
    pass
" 2>/dev/null)
    
    if [ -n "$MCP_COMMANDS" ]; then
        echo "$MCP_COMMANDS" | while IFS='|' read -r name path; do
            if [ -n "$path" ]; then
                if [ -f "$path" ]; then
                    echo -e "    ${GREEN}✓${NC} $name: $path"
                elif [ -d "$path" ]; then
                    echo -e "    ${GREEN}✓${NC} $name: $path (目录存在)"
                else
                    echo -e "    ${RED}✗${NC} $name: 路径不存在！"
                    echo "      路径: $path"
                    ((ERRORS++))
                fi
            fi
        done
    fi
    
    # 检查 VS Code 扩展路径（常见问题）
    echo ""
    echo "  检查 VS Code 扩展路径..."
    VSCODE_EXT_PATHS=$(grep -oE '/Users/[^"]+/.vscode/extensions/[^"]+' "$KIMI_MCP" 2>/dev/null || true)
    
    if [ -n "$VSCODE_EXT_PATHS" ]; then
        echo "$VSCODE_EXT_PATHS" | while read -r path; do
            # 清理路径（去掉可能的尾随字符）
            path=$(echo "$path" | sed 's/[",]*$//')
            
            # 提取扩展 ID 和版本
            EXT_PATTERN=$(echo "$path" | grep -oE '[^/]+\.[\w-]+-[0-9]+\.[0-9]+\.[0-9]+' || true)
            
            if [ -n "$EXT_PATTERN" ]; then
                EXT_NAME=$(echo "$EXT_PATTERN" | sed 's/-[0-9]\+\.[0-9]\+\.[0-9]\+$//')
                EXT_VERSION=$(echo "$EXT_PATTERN" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+$')
                
                # 检查该扩展是否存在（任何版本）
                EXT_BASE="$HOME/.vscode/extensions/${EXT_NAME}-"
                if ls "${EXT_BASE}"* 1>/dev/null 2>&1; then
                    INSTALLED=$(ls -d "${EXT_BASE}"* 2>/dev/null | head -1)
                    if [ "$INSTALLED" != "$path" ]; then
                        echo -e "    ${YELLOW}⚠${NC} 扩展版本不匹配！"
                        echo "      配置: $path"
                        echo "      实际: $INSTALLED"
                        echo -e "      ${YELLOW}建议: 更新 mcp.json 中的路径${NC}"
                        ((WARNINGS++))
                    fi
                else
                    echo -e "    ${RED}✗${NC} 扩展未安装: $EXT_NAME"
                    ((ERRORS++))
                fi
            fi
        done
    else
        echo "    未检测到 VS Code 扩展路径"
    fi
else
    echo -e "${YELLOW}⚠${NC} MCP 配置文件不存在: $KIMI_MCP"
    echo "   (这通常不是问题，只是没有配置 MCP 服务器)"
    ((WARNINGS++))
fi
echo ""

# 检查 Kimi CLI 配置
echo "⚙️  检查 Kimi CLI 配置..."
KIMI_CLI_CONFIG="$HOME/.config/kimi-cli/config.json"
if [ -f "$KIMI_CLI_CONFIG" ]; then
    if [ -s "$KIMI_CLI_CONFIG" ]; then
        echo -e "${GREEN}✓${NC} CLI 配置文件存在且有内容"
    else
        echo -e "${YELLOW}⚠${NC} CLI 配置文件存在但为空"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} CLI 配置文件不存在: $KIMI_CLI_CONFIG"
    ((WARNINGS++))
fi
echo ""

# 检查日志目录
echo "📝 检查日志..."
KIMI_LOG="$HOME/.kimi/logs/kimi.log"
if [ -f "$KIMI_LOG" ]; then
    echo -e "${GREEN}✓${NC} 日志文件存在"
    # 检查最近是否有错误
    RECENT_ERRORS=$(tail -100 "$KIMI_LOG" 2>/dev/null | grep -i "error\|failed\|exception" | tail -5 || true)
    if [ -n "$RECENT_ERRORS" ]; then
        echo ""
        echo -e "  ${YELLOW}最近的错误日志:${NC}"
        echo "$RECENT_ERRORS" | while read -r line; do
            echo "    $line"
        done
    fi
else
    echo -e "${YELLOW}⚠${NC} 日志文件不存在"
fi
echo ""

# 检查 Kimi CLI 是否可运行
echo "🚀 检查 Kimi CLI..."
if command -v kimi &>/dev/null; then
    echo -e "${GREEN}✓${NC} Kimi CLI 已安装"
    KIMI_VERSION=$(kimi --version 2>/dev/null || echo "unknown")
    echo "   版本: $KIMI_VERSION"
else
    echo -e "${RED}✗${NC} Kimi CLI 未找到"
    ((ERRORS++))
fi
echo ""

# 总结
echo "=========================================="
echo "检查结果"
echo "=========================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ 一切正常！${NC}"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ 发现 $WARNINGS 个警告，但可以继续运行${NC}"
else
    echo -e "${RED}✗ 发现 $ERRORS 个错误，$WARNINGS 个警告${NC}"
    echo ""
    echo "建议修复步骤:"
    echo "1. 如果 MCP 服务器路径不存在，请更新 ~/.kimi/mcp.json"
    echo "2. 如果 VS Code 扩展版本不匹配，请修改配置中的路径"
    echo "3. 如果不确定，可以删除 ~/.kimi/mcp.json 重新配置"
fi
echo ""

exit $ERRORS
