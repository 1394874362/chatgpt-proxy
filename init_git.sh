#!/bin/bash
# 初始化 Git 仓库并推送到 GitHub

echo "=========================================="
echo "  Git 仓库初始化脚本"
echo "=========================================="
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 未安装 Git，请先安装"
    exit 1
fi

# 初始化仓库
echo "📦 初始化 Git 仓库..."
git init

# 添加文件
echo "📝 添加文件..."
git add .

# 提交
echo "💾 创建初始提交..."
git commit -m "Initial commit: CPA deployment files"

# 获取 GitHub 仓库地址
echo ""
echo "请在 GitHub 创建一个新仓库，然后输入仓库地址"
echo "例如: https://github.com/你的用户名/chatgpt-proxy.git"
echo ""
read -p "GitHub 仓库地址: " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ 未输入仓库地址"
    exit 1
fi

# 添加远程仓库
echo ""
echo "🔗 添加远程仓库..."
git remote add origin "$repo_url"

# 推送
echo "📤 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "  完成！"
echo "=========================================="
echo ""
echo "仓库地址: $repo_url"
echo ""
echo "下一步："
echo "1. 访问 https://render.com"
echo "2. 点击 'New +' → 'Web Service'"
echo "3. 连接你的 GitHub 仓库"
echo "4. Render 会自动部署"
