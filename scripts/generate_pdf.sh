#!/bin/bash
# 备用PDF生成脚本 - 使用 pandoc + wkhtmltopdf

REPORT_DIR="$1"
if [ -z "$REPORT_DIR" ]; then
    # 使用最新报告
    REPORT_DIR="/root/.openclaw/workspace/satcom-research/reports/$(ls -t /root/.openclaw/workspace/satcom-research/reports/ | head -1)"
fi

HTML_FILE="$REPORT_DIR/report.html"
PDF_FILE="$REPORT_DIR/report.pdf"

echo "正在生成PDF: $PDF_FILE"

# 方法1: 使用 wkhtmltopdf (如果有)
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf --enable-local-file-access --page-size A4 "$HTML_FILE" "$PDF_FILE"
    echo "✅ PDF已生成 (wkhtmltopdf)"
    exit 0
fi

# 方法2: 使用 pandoc 转换为LaTeX再编译
if command -v pandoc &> /dev/null; then
    # 提取文本内容转换为Markdown再转PDF
    echo "使用 pandoc 生成PDF..."
    pandoc "$HTML_FILE" -o "$PDF_FILE" --pdf-engine=xelatex 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ PDF已生成 (pandoc)"
        exit 0
    fi
fi

# 方法3: 提示用户使用浏览器
# 创建一个简单的打印页面
cat > "$REPORT_DIR/print.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>打印报告</title>
    <style>
        body { font-family: 'Noto Sans SC', sans-serif; padding: 40px; }
        .print-btn { 
            position: fixed; top: 20px; right: 20px; 
            padding: 12px 24px; background: #3b82f6; color: white;
            border: none; border-radius: 8px; cursor: pointer;
        }
        @media print { .print-btn { display: none; } }
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ 打印为PDF</button>
    <iframe src="report.html" style="width:100%; height:95vh; border:none;"></iframe>
</body>
</html>
EOF

echo "⚠️ 自动PDF生成需要安装额外工具"
echo "已创建打印页面: $REPORT_DIR/print.html"
echo ""
echo "使用以下任一方法导出PDF:"
echo "1. 打开 print.html 点击打印按钮"
echo "2. 安装 wkhtmltopdf: apt install wkhtmltopdf"
echo "3. 安装 pandoc: apt install pandoc texlive-xetex"
