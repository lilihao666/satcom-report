#!/bin/bash
# 一键上传代码到 GitHub

echo "🚀 准备上传代码到 GitHub..."
echo ""

cd /root/.openclaw/workspace/satcom-research-github

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 提交最新更改..."
    git add .
    git commit -m "更新部署配置"
fi

# 确保分支名正确
git branch -M main

echo ""
echo "=========================================="
echo "📤 开始推送到 GitHub..."
echo "仓库: https://github.com/lilihao666/satcom-report"
echo "=========================================="
echo ""

# 尝试推送
git push -u origin main

echo ""
if [ $? -eq 0 ]; then
    echo "✅ 上传成功！"
    echo ""
    echo "🔗 访问你的仓库:"
    echo "   https://github.com/lilihao666/satcom-report"
else
    echo "❌ 上传失败"
    echo ""
    echo "可能需要输入 GitHub 凭据:"
    echo "  Username: lilihao666"
    echo "  Password: 你的 Personal Access Token"
    echo ""
    echo "获取 Token: https://github.com/settings/tokens/new"
    echo "（勾选 repo 权限）"
fi