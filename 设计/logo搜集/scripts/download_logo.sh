#!/bin/bash
# Logo 下载脚本
# 支持从多个源获取 Logo

COMPANY_NAME="$1"
SYMBOL="$2"
OUTPUT_DIR="$3"

if [ -z "$COMPANY_NAME" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "用法: $0 <公司名称> [股票代码] <输出目录>"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 标准化公司名称 (用于 URL)
COMPANY_ENCODED=$(echo "$COMPANY_NAME" | sed 's/ /+/g; s/,//g; s/\.//g' | tr '[:upper:]' '[:lower:]')
COMPANY_CLEAN=$(echo "$COMPANY_NAME" | sed 's/, Inc\.//g; s/ Inc\.//g; s/ Corporation//g; s/ Corp\.//g; s/ Company//g; s/ Co\.//g' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

echo "正在获取: $COMPANY_NAME"

# 1. 尝试 worldvectorlogo.com
LOGO_URL="https://worldvectorlogo.com/download/${COMPANY_CLEAN}.svg"
echo "  尝试: $LOGO_URL"

# 检查是否已存在
if [ -f "$OUTPUT_DIR/${COMPANY_CLEAN}.svg" ]; then
    echo "  ✓ 已存在"
    exit 0
fi

# 使用 curl 下载 (静默模式)
curl -sL -o "$OUTPUT_DIR/${COMPANY_CLEAN}.svg" "$LOGO_URL" --max-time 10

# 检查是否下载成功 (文件大小 > 1KB 且包含 SVG 标签)
if [ -s "$OUTPUT_DIR/${COMPANY_CLEAN}.svg" ]; then
    if grep -q "<svg" "$OUTPUT_DIR/${COMPANY_CLEAN}.svg" 2>/dev/null; then
        echo "  ✓ 成功从 worldvectorlogo.com 下载"
        exit 0
    else
        # 下载的内容不是有效的 SVG，删除
        rm "$OUTPUT_DIR/${COMPANY_CLEAN}.svg"
    fi
fi

# 2. 尝试 Clearbit Logo API
echo "  尝试 Clearbit Logo API"
curl -sL -o "$OUTPUT_DIR/${COMPANY_CLEAN}_clearbit.png" "https://logo.clearbit.com/${COMPANY_CLEAN}.com" --max-time 10 2>/dev/null

if [ -s "$OUTPUT_DIR/${COMPANY_CLEAN}_clearbit.png" ]; then
    # 检查是否是有效的图片 (文件大小 > 100 字节)
    FILE_SIZE=$(stat -f%z "$OUTPUT_DIR/${COMPANY_CLEAN}_clearbit.png" 2>/dev/null || stat -c%s "$OUTPUT_DIR/${COMPANY_CLEAN}_clearbit.png" 2>/dev/null || echo 0)
    if [ "$FILE_SIZE" -gt 100 ]; then
        echo "  ✓ 成功从 Clearbit 下载 PNG"
        exit 0
    else
        rm "$OUTPUT_DIR/${COMPANY_CLEAN}_clearbit.png"
    fi
fi

echo "  ✗ 未找到 Logo"
