#!/bin/bash
# ============================================================================
# 🛰️ 卫星通信调研报告 - 部署方案 B (Token 方式)
# 无需浏览器交互，使用 GitHub Personal Access Token
# ============================================================================

set -e

echo "=========================================="
echo "🚀 卫星通信报告部署 - Token 方式"
echo "=========================================="
echo ""

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/root/.openclaw/workspace/satcom-research-github"
cd "$PROJECT_DIR"

echo -e "${YELLOW}这种方式需要你先创建 GitHub Token${NC}"
echo ""
echo "获取 Token 步骤:"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限（完整仓库访问）"
echo "4. 点击 Generate token"
echo "5. 复制生成的 token（只显示一次！）"
echo ""

# 获取 Token
read -s -p "粘贴你的 GitHub Token: " GITHUB_TOKEN
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Token 不能为空"
    exit 1
fi

# 验证 Token
echo "🔍 验证 Token..."
GITHUB_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -o '"login": "[^"]*"' | cut -d'"' -f4)

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Token 无效"
    exit 1
fi

echo -e "${GREEN}✅ Token 有效，用户: $GITHUB_USER${NC}"

# 创建仓库
echo ""
echo "📦 创建 GitHub 仓库..."

REPO_NAME="satcom-report"
REPO_EXISTS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$GITHUB_USER/$REPO_NAME" | grep -o '"id":' || echo "")

if [ -n "$REPO_EXISTS" ]; then
    echo -e "${YELLOW}⚠️  仓库已存在，将使用现有仓库${NC}"
else
    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"name\":\"$REPO_NAME\",\"description\":\"卫星通信产业调研报告\",\"private\":false}" \
        https://api.github.com/user/repos
    echo -e "${GREEN}✅ 仓库创建成功${NC}"
fi

# 配置 Git
echo ""
echo "⚙️  配置 Git..."
git config user.name "GitHub Actions"
git config user.email "actions@github.com"

# 设置远程仓库
echo ""
echo "🔗 设置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"

# 推送代码
echo ""
echo "📤 推送代码..."
git branch -M main 2>/dev/null || true
git push -u origin main --force

echo -e "${GREEN}✅ 代码已推送到 GitHub${NC}"

# 显示结果
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 部署完成！${NC}"
echo "=========================================="
echo ""
echo -e "📊 GitHub 仓库: ${BLUE}https://github.com/$GITHUB_USER/$REPO_NAME${NC}"
echo ""
echo "下一步 - 连接 Netlify:"
echo "1. 访问 https://app.netlify.com/"
echo "2. Add new site → Import from GitHub"
echo "3. 选择 $GITHUB_USER/$REPO_NAME"
echo "4. Build command: (留空)"
echo "5. Publish directory: ."
echo "6. Deploy"
echo ""
echo "Token 已用于推送，建议从 Git 配置中移除:"
echo "  git remote set-url origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo ""
echo "=========================================="
