#!/usr/bin/env python3
"""
报告生成器 - 从JSON数据生成HTML报告
"""
import json
from datetime import datetime
from pathlib import Path

TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>卫星通信产业调研报告 | {{date}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        body {{ font-family: 'Noto Sans SC', sans-serif; }}
        .tab-active {{ border-bottom: 3px solid #3b82f6; color: #3b82f6; }}
        .tab-inactive {{ border-bottom: 3px solid transparent; color: #6b7280; }}
        @media print {{ .no-print {{ display: none !important; }} }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-satellite text-blue-600 text-2xl"></i>
                    <div>
                        <h1 class="text-xl font-bold text-gray-900">卫星通信产业调研报告</h1>
                        <p class="text-xs text-gray-500">数据更新：{{date}}</p>
                    </div>
                </div>
                <button onclick="window.print()" class="no-print bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">
                    <i class="fas fa-file-pdf mr-2"></i>导出PDF
                </button>
            </div>
        </div>
    </header>
    
    <nav class="bg-white border-b border-gray-200 no-print">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex space-x-8 overflow-x-auto">
                <a href="#constellation" class="tab-active py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-globe mr-2"></i>星座层
                </a>
                <a href="#terminal" class="tab-inactive py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-mobile-alt mr-2"></i>终端层
                </a>
                <a href="#commercial" class="tab-inactive py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-chart-line mr-2"></i>商业层
                </a>
                <a href="#policy" class="tab-inactive py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-balance-scale mr-2"></i>政策层
                </a>
                <a href="#tech" class="tab-inactive py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-microchip mr-2"></i>技术趋势
                </a>
                <a href="#news" class="tab-inactive py-4 px-1 text-sm font-medium whitespace-nowrap">
                    <i class="fas fa-newspaper mr-2"></i>最新动态
                </a>
            </div>
        </div>
    </nav>
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
        {{content}}
    </main>
    
    <footer class="bg-gray-800 text-white py-8 mt-12">
        <div class="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
            <p>本报告由 GitHub Actions 自动生成 | 数据更新时间：{{date}}</p>
        </div>
    </footer>
</body>
</html>'''

def load_data():
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_content(data):
    """生成报告内容"""
    content = []
    
    # 执行摘要
    content.append(f'''
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-6">
        <h2 class="text-2xl font-bold mb-4">📊 执行摘要</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data["companies"]["domestic"])}</div>
                <div class="text-sm opacity-80">国内终端厂商</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data["constellations"]["domestic"])}</div>
                <div class="text-sm opacity-80">国内星座计划</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{sum(c.get("launched", 0) for c in data["constellations"]["domestic"])}</div>
                <div class="text-sm opacity-80">在轨卫星数量</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data.get("news", []))}</div>
                <div class="text-sm opacity-80">近期动态</div>
            </div>
        </div>
    </div>
    ''')
    
    # 星座层
    constellation_html = ['<section id="constellation"><h2 class="text-2xl font-bold mb-4">🌐 卫星星座对比</h2>']
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4">')
    
    for c in data["constellations"]["domestic"]:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{c["name"]}</h3>
                <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            <div class="mt-3">
                <div class="flex justify-between text-sm mb-1">
                    <span>在轨: {c["launched"]}颗</span>
                    <span>规划: {c["planned"]}颗</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" style="width: {min(progress, 100)}%"></div>
                </div>
            </div>
        </div>
        ''')
    
    constellation_html.append('</div></section>')
    content.append("".join(constellation_html))
    
    # 终端层
    terminal_html = ['<section id="terminal"><h2 class="text-2xl font-bold mb-4">📱 终端设备厂商</h2>']
    terminal_html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">')
    
    for company in data["companies"]["domestic"]:
        terminal_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition">
            <div class="flex justify-between items-start">
                <h3 class="font-bold">{company["name"]}</h3>
                <span class="text-xs text-gray-500">{company.get("city", "")}</span>
            </div>
            <div class="mt-2 text-sm space-y-1">
                <p><span class="text-gray-500">聚焦:</span> {company["focus"]}</p>
                <p><span class="text-gray-500">技术:</span> {company["tech"]}</p>
                <p><span class="text-gray-500">融资:</span> <span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">{company.get("funding", "-")}</span></p>
            </div>
            <div class="mt-3">
                <span class="text-xs text-gray-500">产品:</span>
                <div class="flex flex-wrap gap-1 mt-1">
                    {''.join(f'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{p}</span>' for p in company.get("products", []))}
                </div>
            </div>
        </div>
        ''')
    
    terminal_html.append('</div></section>')
    content.append("".join(terminal_html))
    
    # 技术趋势
    tech_html = ['<section id="tech"><h2 class="text-2xl font-bold mb-4">🔬 技术趋势</h2>']
    tech_html.append('<div class="space-y-4">')
    
    for trend in data["tech_trends"]:
        status_colors = {
            "商业化初期": "green",
            "成本下降中": "blue",
            "部署中": "purple",
            "技术验证": "yellow",
            "早期应用": "orange"
        }
        color = status_colors.get(trend["status"], "gray")
        tech_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-bold text-lg">{trend["trend"]}</h3>
                    <p class="text-gray-600 text-sm mt-1">{trend["description"]}</p>
                </div>
                <span class="bg-{color}-100 text-{color}-800 text-xs px-3 py-1 rounded-full">{trend["status"]}</span>
            </div>
            <div class="mt-3 flex flex-wrap gap-2">
                {''.join(f'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{l}</span>' for l in trend.get("leaders", []))}
            </div>
        </div>
        ''')
    
    tech_html.append('</div></section>')
    content.append("".join(tech_html))
    
    # 最新动态
    if data.get("news"):
        news_html = ['<section id="news"><h2 class="text-2xl font-bold mb-4">📰 最新动态</h2>']
        news_html.append('<div class="space-y-4">')
        
        for news in data["news"][:10]:  # 只显示最近10条
            impact = news.get("impact_analysis", {}).get("level", "low")
            impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
            color = impact_colors.get(impact, "gray")
            
            news_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                <div class="flex justify-between items-start">
                    <h3 class="font-bold">{news["title"]}</h3>
                    <span class="text-xs text-gray-500">{news["date"]}</span>
                </div>
                <p class="text-gray-600 text-sm mt-2">{news["summary"]}</p>
                <div class="mt-2 flex justify-between items-center text-xs">
                    <span class="text-gray-500">来源: {news["source"]}</span>
                    <div class="flex gap-1">
                        {''.join(f'<span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded">{t}</span>' for t in news.get("tags", []))}
                    </div>
                </div>
            </div>
            ''')
        
        news_html.append('</div></section>')
        content.append("".join(news_html))
    
    return "\n".join(content)

def generate():
    data = load_data()
    content = generate_content(data)
    
    html = TEMPLATE.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    html = html.replace("{{content}}", content)
    
    output_file = Path(__file__).parent.parent / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 报告已生成: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        generate()
    else:
        generate()
