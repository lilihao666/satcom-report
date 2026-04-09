#!/bin/bash
# ============================================================================
# 🛰️ 卫星通信调研报告 - 一键部署脚本
# 功能: 自动创建GitHub仓库、推送代码、配置Netlify部署
# ============================================================================

set -e  # 遇到错误立即退出

echo "=========================================="
echo "🚀 卫星通信调研报告 - 一键部署"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/root/.openclaw/workspace/satcom-research-github"
cd "$PROJECT_DIR"

echo -e "${BLUE}📁 项目路径: $PROJECT_DIR${NC}"
echo ""

# ============================================================================
# 步骤 1: 检查并登录 GitHub
# ============================================================================
echo -e "${YELLOW}步骤 1/5: 检查 GitHub 登录状态${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ 未安装 GitHub CLI，请先安装${NC}"
    exit 1
fi

if gh auth status &> /dev/null; then
    echo -e "${GREEN}✅ 已登录 GitHub${NC}"
    gh auth status
else
    echo -e "${YELLOW}⚠️  未登录 GitHub，开始登录流程...${NC}"
    echo ""
    echo "请按提示完成浏览器授权："
    echo "1. 选择 GitHub.com"
    echo "2. 选择 HTTPS"
    echo "3. 选择 Login with a web browser"
    echo "4. 复制代码到浏览器完成授权"
    echo ""
    gh auth login
fi

echo ""

# ============================================================================
# 步骤 2: 获取 GitHub 用户名
# ============================================================================
echo -e "${YELLOW}步骤 2/5: 获取 GitHub 信息${NC}"

GITHUB_USER=$(gh api user -q '.login' 2>/dev/null || echo "")
if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}❌ 无法获取 GitHub 用户名，请检查登录状态${NC}"
    exit 1
fi

echo -e "${GREEN}✅ GitHub 用户名: $GITHUB_USER${NC}"
echo ""

# ============================================================================
# 步骤 3: 创建 GitHub 仓库
# ============================================================================
echo -e "${YELLOW}步骤 3/5: 创建 GitHub 仓库${NC}"

REPO_NAME="satcom-report"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME"

# 检查仓库是否已存在
if gh repo view "$GITHUB_USER/$REPO_NAME" &> /dev/null; then
    echo -e "${YELLOW}⚠️  仓库 $REPO_NAME 已存在${NC}"
    read -p "是否删除并重新创建? (y/N): " confirm
    if [[ $confirm == [yY] ]]; then
        echo "正在删除旧仓库..."
        gh repo delete "$GITHUB_USER/$REPO_NAME" --yes
        echo -e "${GREEN}✅ 旧仓库已删除${NC}"
    else
        echo -e "${BLUE}将使用现有仓库${NC}"
    fi
fi

# 创建新仓库
if ! gh repo view "$GITHUB_USER/$REPO_NAME" &> /dev/null; then
    echo "正在创建仓库 $REPO_NAME..."
    gh repo create "$REPO_NAME" --public --description="卫星通信产业调研报告 - 自动每日更新" --source=. --remote=origin --push
    echo -e "${GREEN}✅ 仓库创建成功${NC}"
else
    # 推送到现有仓库
    echo "推送到现有仓库..."
    git remote remove origin 2>/dev/null || true
    git remote add origin "$REPO_URL"
    git branch -M main 2>/dev/null || git branch -M master main
    git push -u origin main --force
    echo -e "${GREEN}✅ 代码已推送${NC}"
fi

echo ""
echo -e "${BLUE}🌐 仓库地址: $REPO_URL${NC}"
echo ""

# ============================================================================
# 步骤 4: 配置 GitHub Actions 密钥（可选）
# ============================================================================
echo -e "${YELLOW}步骤 4/5: 配置 GitHub Actions${NC}"

# 检查是否需要配置新闻API密钥
echo "是否需要配置新闻搜索API? (用于自动抓取最新动态)"
echo "可选: NewsAPI (https://newsapi.org) 或 其他搜索API"
read -p "输入API密钥 (或留空跳过): " NEWS_API_KEY

if [ -n "$NEWS_API_KEY" ]; then
    echo "正在配置 Secrets..."
    gh secret set NEWS_API_KEY -b"$NEWS_API_KEY" -R "$GITHUB_USER/$REPO_NAME"
    echo -e "${GREEN}✅ API密钥已配置${NC}"
else
    echo -e "${BLUE}跳过API配置，使用默认模拟数据${NC}"
fi

echo ""

# ============================================================================
# 步骤 5: 部署到 Netlify
# ============================================================================
echo -e "${YELLOW}步骤 5/5: 部署到 Netlify${NC}"
echo ""

echo "选择部署方式:"
echo "1) 使用 Netlify CLI (命令行自动部署)"
echo "2) 手动在 Netlify 网站配置 (推荐，更简单)"
read -p "请选择 (1/2): " deploy_choice

if [ "$deploy_choice" == "1" ]; then
    # 使用 Netlify CLI
    if ! command -v netlify &> /dev/null; then
        echo "安装 Netlify CLI..."
        npm install -g netlify-cli
    fi
    
    echo "正在登录 Netlify..."
    netlify login
    
    echo "初始化 Netlify 站点..."
    netlify init --manual --gitRemoteOrigin="$REPO_URL"
    
    echo "部署站点..."
    netlify deploy --prod
    
    echo -e "${GREEN}✅ Netlify 部署完成${NC}"
    
else
    # 手动配置说明
    echo ""
    echo "=========================================="
    echo -e "${GREEN}请按以下步骤手动配置 Netlify:${NC}"
    echo "=========================================="
    echo ""
    echo "1. 访问: https://app.netlify.com/"
    echo "2. 点击 'Add new site' → 'Import an existing project'"
    echo "3. 选择 'GitHub' 并授权"
    echo "4. 搜索并选择仓库: ${BLUE}$GITHUB_USER/$REPO_NAME${NC}"
    echo "5. 构建设置:"
    echo "   - Build command: (留空，我们已预构建)"
    echo "   - Publish directory: ${BLUE}.${NC}"
    echo "6. 点击 'Deploy site'"
    echo ""
    echo "部署完成后，你会得到一个类似以下的链接:"
    echo -e "   ${GREEN}https://satcom-report-xxx.netlify.app${NC}"
    echo ""
    echo "=========================================="
    
    # 保存配置信息到文件
    cat > "$PROJECT_DIR/DEPLOY_INFO.txt" << EOF
部署信息
========
GitHub 仓库: $REPO_URL
部署方式: Netlify

手动部署步骤:
1. 访问 https://app.netlify.com/
2. Add new site → Import from GitHub
3. 选择仓库: $GITHUB_USER/$REPO_NAME
4. Build command: (留空)
5. Publish directory: .
6. Deploy

自动更新:
- 每天早上8点 (UTC 00:00) 自动抓取新闻
- 每次推送代码自动重新部署
EOF
    
    echo -e "${BLUE}部署说明已保存到: DEPLOY_INFO.txt${NC}"
fi

# ============================================================================
# 完成
# ============================================================================
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 部署完成!${NC}"
echo "=========================================="
echo ""
echo -e "📊 GitHub 仓库: ${BLUE}$REPO_URL${NC}"
echo ""
echo "⚙️  自动更新设置:"
echo "   - 每天早上8点自动抓取最新新闻"
echo "   - GitHub Actions 运行日志: $REPO_URL/actions"
echo ""
echo "📖 使用说明:"
echo "   1. 手动触发更新: 访问 Actions → Daily Update → Run workflow"
echo "   2. 修改数据: 编辑 data/satcom_data.json"
echo "   3. 查看报告: index.html"
echo ""
echo "=========================================="
