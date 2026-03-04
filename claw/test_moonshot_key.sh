#!/bin/bash
# Moonshot API Key 测试脚本

API_KEY="sk-4uQa7r74VIeFwHAg7mKZKjDnHMmUJ0pBdsmM23yy4sO2yYkM"

echo "========================================"
echo "🌙 Moonshot API 密钥测试"
echo "========================================"
echo ""

# 测试 1: 获取模型列表
echo "📋 测试 1: 获取可用模型列表..."
response1=$(curl -s -w "\n%{http_code}" https://api.moonshot.cn/v1/models \
  -H "Authorization: Bearer ${API_KEY}")

http_code1=$(echo "$response1" | tail -n1)
body1=$(echo "$response1" | sed '$d')

echo "HTTP 状态码: $http_code1"
if [ "$http_code1" = "200" ]; then
    echo "✅ 模型列表获取成功"
    echo "可用模型:"
    echo "$body1" | grep -o '"id":"[^"]*"' | head -5
else
    echo "❌ 模型列表获取失败"
    echo "响应: $body1"
fi

echo ""
echo "----------------------------------------"
echo ""

# 测试 2: 简单聊天请求
echo "💬 测试 2: 发送聊天请求..."
response2=$(curl -s -w "\n%{http_code}" https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2-5",
    "messages": [{"role": "user", "content": "你好，请用一句话介绍自己"}],
    "max_tokens": 100,
    "temperature": 0.3
  }')

http_code2=$(echo "$response2" | tail -n1)
body2=$(echo "$response2" | sed '$d')

echo "HTTP 状态码: $http_code2"
if [ "$http_code2" = "200" ]; then
    echo "✅ 聊天请求成功"
    echo ""
    echo "🤖 AI 回复:"
    echo "$body2" | grep -o '"content":"[^"]*"' | head -1 | sed 's/"content":"//;s/"$//'
else
    echo "❌ 聊天请求失败"
    echo "响应: $body2"
fi

echo ""
echo "========================================"
echo "📊 测试结果总结"
echo "========================================"

if [ "$http_code1" = "200" ] && [ "$http_code2" = "200" ]; then
    echo "✅ 所有测试通过！API 密钥有效。"
    exit 0
else
    echo "❌ 测试失败！API 密钥可能无效或未生效。"
    echo ""
    echo "可能的原因:"
    echo "  1. 密钥尚未生效（新密钥可能需要几分钟）"
    echo "  2. 密钥已被删除或过期"
    echo "  3. 账号需要充值或验证"
    echo ""
    echo "建议:"
    echo "  - 访问 https://platform.moonshot.cn/ 检查密钥状态"
    echo "  - 重新生成一个新的 API 密钥"
    exit 1
fi
