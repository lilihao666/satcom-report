#!/bin/bash
# 启动报告预览服务器

cd /root/.openclaw/workspace/satcom-research/reports

# 找到最新的报告目录
LATEST=$(ls -t | head -1)

if [ -z "$LATEST" ]; then
    echo "没有可用的报告，请先运行生成脚本: python3 scripts/generate_report.py full"
    exit 1
fi

echo "🚀 启动报告预览服务器..."
echo "📄 最新报告: $LATEST"
echo "🌐 访问地址: http://localhost:8080/report.html"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

cd "$LATEST"
python3 -m http.server 8080
