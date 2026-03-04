#!/bin/bash
# CPA 一键部署脚本（Linux/Mac）

echo "=========================================="
echo "  CPA 反代一键部署脚本"
echo "=========================================="
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 未安装 Git，请先安装"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安装 Python 3，请先安装"
    exit 1
fi

# 创建配置文件
if [ ! -f "config.json" ]; then
    echo "📝 创建配置文件..."
    cp config.example.json config.json
    echo "✅ 已创建 config.json，请编辑填写你的配置"
    echo ""
    echo "需要填写："
    echo "  - cpa_url: 你的 Render 服务地址"
    echo "  - cpa_password: 你设置的密码"
    echo ""
    read -p "按回车继续..."
fi

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install requests

# 上传 Token
echo ""
echo "📤 开始上传 Token..."
python3 upload_tokens.py

# 配置保活
echo ""
read -p "是否配置 UptimeRobot 自动唤醒? (y/n): " setup_uptime

if [ "$setup_uptime" = "y" ]; then
    python3 setup_uptimerobot.py
fi

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "你的 API 地址："
python3 -c "import json; print(json.load(open('config.json'))['cpa_url'])"
echo ""
echo "使用示例："
echo "  python3 example_usage.py"
