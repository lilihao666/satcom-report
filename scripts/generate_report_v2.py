#!/usr/bin/env python3
"""
卫星通信调研报告生成器 v2.0
集成实时新闻，支持多维度数据展示
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 配置
WORKSPACE_DIR = Path("/root/.openclaw/workspace/satcom-research")
REPORTS_DIR = WORKSPACE_DIR / "reports"
DATA_DIR = WORKSPACE_DIR / "data"
TEMPLATES_DIR = WORKSPACE_DIR / "templates"

def ensure_dirs():
    """确保目录结构存在"""
    for dir_path in [REPORTS_DIR, DATA_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

def load_full_data() -> Dict:
    """加载完整数据"""
    data_file = DATA_DIR / "data_full.json"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_news_cache() -> List[Dict]:
    """加载新闻缓存"""
    news_file = DATA_DIR / "news_cache.json"
    if news_file.exists():
        with open(news_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("news", [])
    return []

def generate_enhanced_html(data: Dict, news: List[Dict]) -> str:
    """生成增强版HTML报告"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 生成星座层HTML
    constellation_html = generate_constellation_section(data)
    
    # 生成终端层HTML
    terminal_html = generate_terminal_section(data)
    
    # 生成商业层HTML
    commercial_html = generate_commercial_section(data)
    
    # 生成政策层HTML
    policy_html = generate_policy_section(data)
    
    # 生成技术趋势HTML
    tech_html = generate_tech_section(data)
    
    # 生成新闻动态HTML
    news_html = generate_news_section(news)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>卫星通信产业调研报告 | {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        body {{ font-family: 'Noto Sans SC', sans-serif; }}
        .tab-active {{ border-bottom: 3px solid #3b82f6; color: #3b82f6; background: linear-gradient(to bottom, transparent 95%, rgba(59,130,246,0.1) 100%); }}
        .tab-inactive {{ border-bottom: 3px solid transparent; color: #6b7280; }}
        .tab-inactive:hover {{ color: #374151; border-bottom-color: #d1d5db; }}
        .company-card {{ transition: all 0.3s ease; }}
        .company-card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .news-high {{ border-left: 4px solid #ef4444; }}
        .news-medium {{ border-left: 4px solid #f59e0b; }}
        .news-low {{ border-left: 4px solid #10b981; }}
        @media print {{
            .no-print {{ display: none !important; }}
            .page-break {{ page-break-before: always; }}
            body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .tab-content {{ display: block !important; }}
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-satellite text-blue-600 text-2xl"></i>
                    <div>
                        <h1 class="text-xl font-bold text-gray-900">卫星通信产业调研报告</h1>
                        <p class="text-xs text-gray-500">Satellite Communications Industry Research</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-500">
                        <i class="far fa-calendar-alt mr-1"></i>
                        数据更新：<span id="update-date">{today}</span>
                    </span>
                    <button onclick="exportPDF()" class="no-print bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
                        <i class="fas fa-file-pdf mr-2"></i>导出PDF
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Executive Summary -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h2 class="text-2xl font-bold mb-4">📊 执行摘要</h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div class="text-3xl font-bold">{len(data.get('companies', {}).get('domestic', []))}</div>
                    <div class="text-sm opacity-80">国内终端厂商</div>
                </div>
                <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div class="text-3xl font-bold">{len(data.get('constellations', {}).get('domestic', []))}</div>
                    <div class="text-sm opacity-80">国内星座计划</div>
                </div>
                <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div class="text-3xl font-bold">{sum(c.get('launched', 0) for c in data.get('constellations', {}).get('domestic', []))}</div>
                    <div class="text-sm opacity-80">在轨卫星数量</div>
                </div>
                <div class="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div class="text-3xl font-bold">{len(news)}</div>
                    <div class="text-sm opacity-80">近期动态</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <nav class="bg-white border-b border-gray-200 no-print">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex space-x-8">
                <button onclick="switchTab('constellation')" id="tab-constellation" class="tab-active py-4 px-1 text-sm font-medium">
                    <i class="fas fa-globe mr-2"></i>星座层
                </button>
                <button onclick="switchTab('terminal')" id="tab-terminal" class="tab-inactive py-4 px-1 text-sm font-medium">
                    <i class="fas fa-mobile-alt mr-2"></i>终端层
                </button>
                <button onclick="switchTab('commercial')" id="tab-commercial" class="tab-inactive py-4 px-1 text-sm font-medium">
                    <i class="fas fa-chart-line mr-2"></i>商业层
                </button>
                <button onclick="switchTab('policy')" id="tab-policy" class="tab-inactive py-4 px-1 text-sm font-medium">
                    <i class="fas fa-balance-scale mr-2"></i>政策层
                </button>
                <button onclick="switchTab('tech')" id="tab-tech" class="tab-inactive py-4 px-1 text-sm font-medium">
                    <i class="fas fa-microchip mr-2"></i>技术趋势
                </button>
                <button onclick="switchTab('news')" id="tab-news" class="tab-inactive py-4 px-1 text-sm font-medium">
                    <i class="fas fa-newspaper mr-2"></i>最新动态
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {constellation_html}
        {terminal_html}
        {commercial_html}
        {policy_html}
        {tech_html}
        {news_html}
    </main>

    <script>
        function switchTab(tabName) {{
            document.querySelectorAll('[id^="tab-"]').forEach(tab => {{
                tab.classList.remove('tab-active');
                tab.classList.add('tab-inactive');
            }});
            document.getElementById('tab-' + tabName).classList.remove('tab-inactive');
            document.getElementById('tab-' + tabName).classList.add('tab-active');
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.add('hidden');
            }});
            document.getElementById('content-' + tabName).classList.remove('hidden');
        }}

        function exportPDF() {{
            window.print();
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            switchTab('constellation');
        }});
    </script>
</body>
</html>"""
    
    return html

def generate_constellation_section(data: Dict) -> str:
    """生成星座层HTML"""
    domestic = data.get("constellations", {}).get("domestic", [])
    international = data.get("constellations", {}).get("international", [])
    
    html = """
    <div id="content-constellation" class="tab-content">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">🌐 卫星星座对比</h2>
            <p class="text-gray-600">国内外主要低轨卫星星座部署进度对比</p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Domestic -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-100">
                    <h3 class="text-lg font-bold text-gray-900">🇨🇳 国内星座</h3>
                </div>
                <div class="p-6 space-y-4">
    """
    
    for c in domestic:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
        html += f"""
                    <div class="border rounded-lg p-4">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <h4 class="font-bold text-gray-900">{c.get('name')}</h4>
                                <p class="text-sm text-gray-500">{c.get('operator')}</p>
                            </div>
                            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">{c.get('stage')}</span>
                        </div>
                        <div class="flex justify-between text-sm mb-2">
                            <span class="text-gray-600">在轨: {c.get('launched')}颗</span>
                            <span class="text-gray-600">规划: {c.get('planned')}颗</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-blue-600 h-2 rounded-full" style="width: {min(progress, 100)}%"></div>
                        </div>
                        <div class="mt-3 flex flex-wrap gap-1">
                            {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{tag}</span>' for tag in c.get('use_cases', [])])}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <!-- International -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-100">
                    <h3 class="text-lg font-bold text-gray-900">🌍 国际星座</h3>
                </div>
                <div class="p-6 space-y-4">
    """
    
    for c in international:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100 if c.get("planned", 0) > 0 else 0
        html += f"""
                    <div class="border rounded-lg p-4">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <h4 class="font-bold text-gray-900">{c.get('name')}</h4>
                                <p class="text-sm text-gray-500">{c.get('operator')}</p>
                            </div>
                            <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">{c.get('stage')}</span>
                        </div>
                        <div class="flex justify-between text-sm mb-2">
                            <span class="text-gray-600">在轨: {c.get('launched', 'N/A')}颗</span>
                            <span class="text-gray-600">规划: {c.get('planned', 'N/A')}颗</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="bg-green-600 h-2 rounded-full" style="width: {min(progress, 100)}%"></div>
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def generate_terminal_section(data: Dict) -> str:
    """生成终端层HTML"""
    domestic = data.get("companies", {}).get("domestic", [])
    international = data.get("companies", {}).get("international", [])
    
    html = """
    <div id="content-terminal" class="tab-content hidden">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">📱 终端设备厂商</h2>
            <p class="text-gray-600">国内外卫星通信终端设备制造商对比分析</p>
        </div>
        
        <div class="mb-4">
            <h3 class="text-lg font-bold text-gray-900 mb-4">🇨🇳 国内厂商 ({len(domestic)}家)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    """
    
    for company in domestic:
        html += f"""
                <div class="company-card bg-white rounded-lg shadow-sm border border-gray-200 p-5">
                    <div class="flex justify-between items-start mb-3">
                        <h4 class="font-bold text-gray-900">{company.get('name')}</h4>
                        <span class="text-xs text-gray-500">{company.get('city', '-')}</span>
                    </div>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-500">业务聚焦:</span>
                            <span class="text-gray-900">{company.get('focus')}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-500">技术体制:</span>
                            <span class="text-gray-900">{company.get('tech')}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-500">成立时间:</span>
                            <span class="text-gray-900">{company.get('founded', '-')}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-500">融资阶段:</span>
                            <span class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded">{company.get('funding', '-')}</span>
                        </div>
                    </div>
                    <div class="mt-3 pt-3 border-t border-gray-100">
                        <span class="text-xs text-gray-500">主要产品:</span>
                        <div class="flex flex-wrap gap-1 mt-1">
                            {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{p}</span>' for p in company.get('products', [])])}
                        </div>
                    </div>
                </div>
        """
    
    html += f"""
            </div>
        </div>
        
        <div class="mt-8">
            <h3 class="text-lg font-bold text-gray-900 mb-4">🌍 国际厂商 ({len(international)}家)</h3>
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">公司</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">地区</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">用户/规模</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">终端价格</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">服务费</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
    """
    
    for company in international:
        html += f"""
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{company.get('name')}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-gray-500">{company.get('region')}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-gray-500">{company.get('subscribers', 'N/A')}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-gray-500">{company.get('terminal_price', 'N/A')}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-gray-500">{company.get('service_price', 'N/A')}</td>
                        </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    
    return html

def generate_commercial_section(data: Dict) -> str:
    """生成商业层HTML"""
    models = data.get("business_models", {})
    
    html = """
    <div id="content-commercial" class="tab-content hidden">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">📈 商业模式与定价</h2>
            <p class="text-gray-600">卫星通信行业商业模式分析及价格对比</p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">🇨🇳 国内商业模式</h3>
                <div class="space-y-4">
    """
    
    for model in models.get("domestic", []):
        html += f"""
                    <div class="border-l-4 border-blue-500 pl-4 py-2">
                        <h4 class="font-bold text-gray-900">{model.get('model')}</h4>
                        <p class="text-sm text-gray-600 mt-1">{model.get('description')}</p>
                        <div class="mt-2 flex flex-wrap gap-2">
                            {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{p}</span>' for p in model.get('players', [])])}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">🌍 国际商业模式</h3>
                <div class="space-y-4">
    """
    
    for model in models.get("international", []):
        html += f"""
                    <div class="border-l-4 border-green-500 pl-4 py-2">
                        <h4 class="font-bold text-gray-900">{model.get('model')}</h4>
                        <p class="text-sm text-gray-600 mt-1">{model.get('description')}</p>
                        <div class="mt-2 flex flex-wrap gap-2">
                            {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{p}</span>' for p in model.get('players', [])])}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-4">💰 价格对比</h3>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">服务</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">终端价格</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">月费</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">速率/规格</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
    """
    
    for item in models.get("price_comparison", {}).get("broadband", []):
        html += f"""
                        <tr>
                            <td class="px-6 py-4 font-medium text-gray-900">{item.get('service')}</td>
                            <td class="px-6 py-4 text-gray-500">${item.get('terminal_usd') if 'terminal_usd' in item else '¥' + str(item.get('terminal_cny', 'N/A'))}</td>
                            <td class="px-6 py-4 text-gray-500">${item.get('monthly_usd') if 'monthly_usd' in item else '¥' + str(item.get('monthly_cny', 'N/A'))}</td>
                            <td class="px-6 py-4 text-gray-500">{item.get('speed')}</td>
                        </tr>
        """
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    
    return html

def generate_policy_section(data: Dict) -> str:
    """生成政策层HTML"""
    policy = data.get("policy", {})
    
    html = """
    <div id="content-policy" class="tab-content hidden">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">⚖️ 政策法规动态</h2>
            <p class="text-gray-600">国内外卫星通信相关政策法规及许可要求</p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-100">
                    <h3 class="text-lg font-bold text-gray-900">🇨🇳 国内政策</h3>
                </div>
                <div class="p-6 space-y-4">
    """
    
    for item in policy.get("china", []):
        impact_color = "red" if item.get("impact") == "high" else "yellow"
        html += f"""
                    <div class="border-l-4 border-{impact_color}-500 pl-4 py-2 bg-{impact_color}-50 rounded-r">
                        <div class="flex justify-between items-start">
                            <h4 class="font-bold text-gray-900">{item.get('title')}</h4>
                            <span class="text-xs text-gray-500">{item.get('date')}</span>
                        </div>
                        <p class="text-sm text-gray-600 mt-1">{item.get('content')}</p>
                        <span class="text-xs text-gray-500">发布: {item.get('issuer')}</span>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-sm border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-100">
                    <h3 class="text-lg font-bold text-gray-900">🌍 国际政策</h3>
                </div>
                <div class="p-6 space-y-4">
    """
    
    for item in policy.get("international", []):
        impact_color = "red" if item.get("impact") == "high" else "yellow"
        html += f"""
                    <div class="border-l-4 border-{impact_color}-500 pl-4 py-2 bg-{impact_color}-50 rounded-r">
                        <div class="flex justify-between items-start">
                            <h4 class="font-bold text-gray-900">{item.get('title')}</h4>
                            <span class="text-xs text-gray-500">{item.get('date')}</span>
                        </div>
                        <p class="text-sm text-gray-600 mt-1">{item.get('content')}</p>
                        <span class="text-xs text-gray-500">发布: {item.get('issuer')}</span>
                    </div>
        """
    
    html += """
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-4">📋 许可要求对比</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    """
    
    licensing = policy.get("licensing", {})
    for country, info in licensing.items():
        flag = "🇨🇳" if country == "china" else "🇺🇸"
        name = "中国" if country == "china" else "美国"
        html += f"""
                <div class="border rounded-lg p-4">
                    <h4 class="font-bold text-gray-900 mb-3">{flag} {name}</h4>
                    <div class="space-y-2">
                        <div class="text-sm">
                            <span class="text-gray-500">主管部门:</span>
                            <span class="text-gray-900 ml-2">{info.get('authority')}</span>
                        </div>
                        <div class="text-sm">
                            <span class="text-gray-500">审批周期:</span>
                            <span class="text-gray-900 ml-2">{info.get('timeline')}</span>
                        </div>
                        <div class="text-sm">
                            <span class="text-gray-500">许可类型:</span>
                            <div class="flex flex-wrap gap-1 mt-1">
                                {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{r}</span>' for r in info.get('requirements', [])])}
                            </div>
                        </div>
                    </div>
                </div>
        """
    
    html += """
            </div>
        </div>
    </div>
    """
    
    return html

def generate_tech_section(data: Dict) -> str:
    """生成技术趋势HTML"""
    trends = data.get("tech_trends", [])
    
    html = """
    <div id="content-tech" class="tab-content hidden">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">🔬 技术趋势</h2>
            <p class="text-gray-600">卫星通信领域关键技术发展趋势与路线图</p>
        </div>
        
        <div class="space-y-4">
    """
    
    for trend in trends:
        status_colors = {
            "商业化初期": "green",
            "成本下降中": "blue",
            "部署中": "purple",
            "技术验证": "yellow",
            "早期应用": "orange"
        }
        color = status_colors.get(trend.get("status"), "gray")
        
        html += f"""
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h3 class="text-lg font-bold text-gray-900">{trend.get('trend')}</h3>
                        <p class="text-gray-600 mt-1">{trend.get('description')}</p>
                    </div>
                    <span class="px-3 py-1 bg-{color}-100 text-{color}-800 text-sm rounded-full">{trend.get('status')}</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-100">
                    <div>
                        <span class="text-xs text-gray-500 uppercase">领先企业</span>
                        <div class="flex flex-wrap gap-1 mt-1">
                            {''.join([f'<span class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{l}</span>' for l in trend.get('leaders', [])])}
                        </div>
                    </div>
                    <div>
                        <span class="text-xs text-gray-500 uppercase">时间线</span>
                        <p class="text-sm text-gray-900 mt-1">{trend.get('timeline')}</p>
                    </div>
                </div>
            </div>
    """
    
    html += """
        </div>
    </div>
    """
    
    return html

def generate_news_section(news: List[Dict]) -> str:
    """生成新闻动态HTML"""
    html = f"""
    <div id="content-news" class="tab-content hidden">
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">📰 最新动态</h2>
            <p class="text-gray-600">卫星通信行业最新新闻与动态 ({len(news)}条)</p>
        </div>
        
        <div class="space-y-4">
    """
    
    for item in news:
        impact = item.get("impact_analysis", {}).get("level", "low")
        impact_class = f"news-{impact}"
        impact_label = {"high": "🔴 高影响", "medium": "🟡 中影响", "low": "🟢 低影响"}.get(impact, "")
        
        html += f"""
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 {impact_class}">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-lg font-bold text-gray-900">{item.get('title')}</h3>
                    <span class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">{impact_label}</span>
                </div>
                <p class="text-gray-600 mb-3">{item.get('summary')}</p>
                <div class="flex justify-between items-center text-sm">
                    <div class="flex items-center gap-4">
                        <span class="text-gray-500"><i class="far fa-calendar mr-1"></i>{item.get('date')}</span>
                        <span class="text-gray-500">来源: {item.get('source')}</span>
                    </div>
                    <div class="flex gap-1">
                        {''.join([f'<span class="px-2 py-0.5 bg-blue-50 text-blue-600 text-xs rounded">{tag}</span>' for tag in item.get('tags', [])])}
                    </div>
                </div>
            </div>
    """
    
    html += """
        </div>
    </div>
    """
    
    return html

def generate_report():
    """生成完整的增强版报告"""
    ensure_dirs()
    
    today = datetime.now().strftime("%Y-%m-%d")
    report_dir = REPORTS_DIR / today
    report_dir.mkdir(exist_ok=True)
    
    # 加载数据
    data = load_full_data()
    news = load_news_cache()
    
    # 生成HTML
    html = generate_enhanced_html(data, news)
    
    # 保存HTML
    html_path = report_dir / "report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ HTML报告已生成: {html_path}")
    
    # 生成PDF
    pdf_path = report_dir / "report.pdf"
    try:
        subprocess.run([
            "wkhtmltopdf",
            "--enable-local-file-access",
            "--page-size", "A4",
            str(html_path), str(pdf_path)
        ], check=True, timeout=120)
        print(f"✅ PDF报告已生成: {pdf_path}")
    except Exception as e:
        print(f"⚠️ PDF生成失败: {e}")
    
    return html_path, pdf_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "generate":
            generate_report()
    else:
        # 更新新闻并生成报告
        print("🔄 更新新闻数据...")
        subprocess.run(["python3", str(WORKSPACE_DIR / "scripts/news_fetcher.py"), "update"])
        print("\n🔄 生成报告...")
        generate_report()
