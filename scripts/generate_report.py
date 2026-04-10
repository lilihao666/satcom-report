#!/usr/bin/env python3
"""
报告生成器 - 从JSON数据生成完整HTML报告（支持点击查看详情）
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
        body { font-family: 'Noto Sans SC', sans-serif; }
        .tab-active { border-bottom: 3px solid #3b82f6; color: #3b82f6; }
        .tab-inactive { border-bottom: 3px solid transparent; color: #6b7280; }
        @media print { .no-print { display: none !important; } }
        
        /* 回到顶部按钮 */
        #back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            transition: all 0.3s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        #back-to-top:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
        }
        #back-to-top.hidden {
            opacity: 0;
            visibility: hidden;
        }
        
        /* 详情弹窗 */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }
        .modal-content {
            background: white;
            border-radius: 16px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            padding: 0;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }
        .modal-overlay.active .modal-content {
            transform: scale(1);
        }
        .modal-header {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 20px 24px;
            border-radius: 16px 16px 0 0;
        }
        .modal-body {
            padding: 24px;
        }
        .modal-close {
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            transition: background 0.2s;
        }
        .modal-close:hover {
            background: rgba(255,255,255,0.3);
        }
        
        /* 可点击卡片 */
        .clickable-card {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .clickable-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }
        .clickable-card::after {
            content: "点击查看详情";
            position: absolute;
            bottom: 8px;
            right: 8px;
            font-size: 10px;
            color: #3b82f6;
            opacity: 0;
            transition: opacity 0.2s;
        }
        .clickable-card:hover::after {
            opacity: 1;
        }
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
    
    <!-- 详情弹窗 -->
    <div id="detail-modal" class="modal-overlay no-print" onclick="closeModal(event)">
        <div class="modal-content relative" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div id="modal-header" class="modal-header"></div>
            <div id="modal-body" class="modal-body"></div>
        </div>
    </div>
    
    <button id="back-to-top" class="no-print hidden" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="回到顶部">
        <i class="fas fa-arrow-up"></i>
    </button>
    
    <script>
        // 回到顶部按钮
        const backToTopBtn = document.getElementById('back-to-top');
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.remove('hidden');
            } else {
                backToTopBtn.classList.add('hidden');
            }
        });
        
        // Tab切换
        document.querySelectorAll('nav a').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('nav a').forEach(t => {
                    t.classList.remove('tab-active');
                    t.classList.add('tab-inactive');
                });
                this.classList.remove('tab-inactive');
                this.classList.add('tab-active');
            });
        });
        
        // 弹窗控制
        function openModal(title, content) {
            document.getElementById('modal-header').innerHTML = `<h3 class="text-xl font-bold">${title}</h3>`;
            document.getElementById('modal-body').innerHTML = content;
            document.getElementById('detail-modal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeModal(event) {
            if (!event || event.target.id === 'detail-modal') {
                document.getElementById('detail-modal').classList.remove('active');
                document.body.style.overflow = '';
            }
        }
        
        // ESC键关闭弹窗
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeModal();
        });
    </script>
</body>
</html>'''

def load_data():
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def escape_js(s):
    """转义JavaScript字符串，用于HTML属性"""
    if not s:
        return ""
    # 移除换行符和多余空格，使内容适合单行HTML属性
    s = ' '.join(s.split())
    # 使用HTML实体&quot;代替\"，避免与HTML属性引号冲突
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '&quot;')

def generate_content(data):
    """生成报告内容"""
    content = []
    
    # 执行摘要
    total_domestic_launched = sum(c.get("launched", 0) for c in data["constellations"]["domestic"])
    total_intl_launched = sum(c.get("launched", 0) for c in data["constellations"]["international"])
    
    content.append(f'''
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-6">
        <h2 class="text-2xl font-bold mb-4">📊 执行摘要</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data["companies"]["domestic"])}+{len(data["companies"]["international"])}</div>
                <div class="text-sm opacity-80">终端厂商</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data["constellations"]["domestic"])}+{len(data["constellations"]["international"])}</div>
                <div class="text-sm opacity-80">星座计划</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{total_domestic_launched + total_intl_launched:,}</div>
                <div class="text-sm opacity-80">全球在轨卫星</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data.get("news", []))}</div>
                <div class="text-sm opacity-80">近期动态</div>
            </div>
        </div>
    </div>
    ''')
    
    # 星座层 - 国内
    constellation_html = ['<section id="constellation"><h2 class="text-2xl font-bold mb-4">🌐 卫星星座对比</h2>']
    
    # 国内星座
    constellation_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-red-500 rounded-full mr-2"></span>国内星座</h3>')
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">')
    
    for c in data["constellations"]["domestic"]:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
        note = c.get("note", "")
        note_html = f'<p class="text-xs text-orange-600 mt-1">{note}</p>' if note else ""
        
        # 详情内容
        detail_content = f'''
        <div class="space-y-4">
            <div>
                <p class="text-gray-600"><strong>运营方:</strong> {c["operator"]}</p>
                <p class="text-gray-600"><strong>规划数量:</strong> {c["planned"]:,} 颗</p>
                <p class="text-gray-600"><strong>已发射:</strong> {c["launched"]} 颗</p>
                <p class="text-gray-600"><strong>当前阶段:</strong> <span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">{c["stage"]}</span></p>
            </div>
            <div>
                <p class="font-semibold mb-2">应用场景:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">{uc}</span>' for uc in c.get("use_cases", []))}
                </div>
            </div>
            {f'<div class="bg-orange-50 p-3 rounded-lg"><p class="text-sm text-orange-700"><i class="fas fa-info-circle mr-1"></i> {note}</p></div>' if note else ''}
            <div class="mt-4">
                <p class="text-sm text-gray-500 mb-2">部署进度: {progress:.1f}%</p>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full" style="width: {min(progress, 100)}%"></div>
                </div>
            </div>
        </div>
        '''
        
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500 clickable-card relative" onclick="openModal('{escape_js(c["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{c["name"]}</h3>
                <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            {note_html}
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
    
    constellation_html.append('</div>')
    
    # 国际星座
    constellation_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>国际星座</h3>')
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4">')
    
    for c in data["constellations"]["international"]:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
        note = c.get("note", "")
        note_html = f'<p class="text-xs text-orange-600 mt-1">{note}</p>' if note else ""
        
        detail_content = f'''
        <div class="space-y-4">
            <div>
                <p class="text-gray-600"><strong>运营方:</strong> {c["operator"]}</p>
                <p class="text-gray-600"><strong>规划数量:</strong> {c["planned"]:,} 颗</p>
                <p class="text-gray-600"><strong>已发射:</strong> {c["launched"]:,} 颗</p>
                <p class="text-gray-600"><strong>当前阶段:</strong> <span class="bg-green-100 text-green-800 px-2 py-0.5 rounded">{c["stage"]}</span></p>
            </div>
            <div>
                <p class="font-semibold mb-2">应用场景:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">{uc}</span>' for uc in c.get("use_cases", []))}
                </div>
            </div>
            {f'<div class="bg-orange-50 p-3 rounded-lg"><p class="text-sm text-orange-700"><i class="fas fa-info-circle mr-1"></i> {note}</p></div>' if note else ''}
            <div class="mt-4">
                <p class="text-sm text-gray-500 mb-2">部署进度: {progress:.1f}%</p>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full" style="width: {min(progress, 100)}%"></div>
                </div>
            </div>
        </div>
        '''
        
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-green-500 clickable-card relative" onclick="openModal('{escape_js(c["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{c["name"]}</h3>
                <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            {note_html}
            <div class="mt-3">
                <div class="flex justify-between text-sm mb-1">
                    <span>在轨: {c["launched"]:,}颗</span>
                    <span>规划: {c["planned"]:,}颗</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" style="width: {min(progress, 100)}%"></div>
                </div>
            </div>
        </div>
        ''')
    
    constellation_html.append('</div></section>')
    
    # 高轨GEO星座 - 国内
    constellation_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center mt-8"><span class="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>国内高轨GEO星座</h3>')
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">')
    
    for c in data["constellations"].get("geo_domestic", []):
        note = c.get("note", "")
        note_html = f'<p class="text-xs text-purple-600 mt-1">{note}</p>' if note else ""
        
        detail_content = f'''
        <div class="space-y-4">
            <div>
                <p class="text-gray-600"><strong>运营方:</strong> {c["operator"]}</p>
                <p class="text-gray-600"><strong>卫星数量:</strong> {c["launched"]} 颗</p>
                <p class="text-gray-600"><strong>轨道类型:</strong> <span class="bg-purple-100 text-purple-800 px-2 py-0.5 rounded">GEO地球静止轨道</span></p>
            </div>
            <div>
                <p class="font-semibold mb-2">应用场景:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">{uc}</span>' for uc in c.get("use_cases", []))}
                </div>
            </div>
            {f'<div class="bg-purple-50 p-3 rounded-lg"><p class="text-sm text-purple-700"><i class="fas fa-info-circle mr-1"></i> {note}</p></div>' if note else ''}
        </div>
        '''
        
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-purple-500 clickable-card relative" onclick="openModal('{escape_js(c["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{c["name"]}</h3>
                <span class="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            {note_html}
            <div class="mt-3">
                <span class="text-sm text-gray-500">{c["launched"]}颗GEO卫星在轨</span>
            </div>
        </div>
        ''')
    
    constellation_html.append('</div>')
    
    # 高轨GEO星座 - 国际
    constellation_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>国际高轨GEO星座</h3>')
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">')
    
    for c in data["constellations"].get("geo_international", []):
        note = c.get("note", "")
        note_html = f'<p class="text-xs text-indigo-600 mt-1">{note}</p>' if note else ""
        
        detail_content = f'''
        <div class="space-y-4">
            <div>
                <p class="text-gray-600"><strong>运营方:</strong> {c["operator"]}</p>
                <p class="text-gray-600"><strong>卫星数量:</strong> {c["launched"]:,} 颗</p>
                <p class="text-gray-600"><strong>轨道类型:</strong> <span class="bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded">{c.get("orbit", "GEO")}</span></p>
            </div>
            <div>
                <p class="font-semibold mb-2">应用场景:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">{uc}</span>' for uc in c.get("use_cases", []))}
                </div>
            </div>
            {f'<div class="bg-indigo-50 p-3 rounded-lg"><p class="text-sm text-indigo-700"><i class="fas fa-info-circle mr-1"></i> {note}</p></div>' if note else ''}
        </div>
        '''
        
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-indigo-500 clickable-card relative" onclick="openModal('{escape_js(c["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{c["name"]}</h3>
                <span class="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            {note_html}
            <div class="mt-3">
                <span class="text-sm text-gray-500">{c["launched"]:,}颗卫星在轨</span>
            </div>
        </div>
        ''')
    
    constellation_html.append('</div>')
    
    content.append("".join(constellation_html))
    
    # 终端层 - 国内厂商
    terminal_html = ['<section id="terminal"><h2 class="text-2xl font-bold mb-4">📱 终端设备厂商</h2>']
    
    terminal_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-red-500 rounded-full mr-2"></span>国内厂商</h3>')
    terminal_html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
    
    for company in data["companies"]["domestic"]:
        detail_content = f'''
        <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-sm text-gray-500">总部</p>
                    <p class="font-medium">{company.get("city", "-")}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">成立时间</p>
                    <p class="font-medium">{company.get("founded", "-")}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">融资阶段</p>
                    <p class="font-medium"><span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">{company.get("funding", "-")}</span></p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">核心技术</p>
                    <p class="font-medium">{company.get("tech", "-")}</p>
                </div>
            </div>
            <div>
                <p class="text-sm text-gray-500 mb-2">主营业务</p>
                <p class="text-gray-700">{company.get("focus", "-")}</p>
            </div>
            <div>
                <p class="text-sm text-gray-500 mb-2">公司简介</p>
                <p class="text-gray-700">{company.get("description", "暂无简介")}</p>
            </div>
            <div>
                <p class="font-semibold mb-2">主要产品:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">{p}</span>' for p in company.get("products", []))}
                </div>
            </div>
            {f'''
            <div>
                <p class="font-semibold mb-3">代表产品:</p>
                <div class="grid grid-cols-1 gap-3">
                    {''.join(f'''
                    <div class="flex gap-3 p-3 bg-gray-50 rounded-lg">
                        <img src="{fp.get("image", "")}" alt="{fp.get("name", "")}" class="w-20 h-20 object-cover rounded-lg">
                        <div>
                            <p class="font-semibold text-sm">{fp.get("name", "")}</p>
                            <p class="text-xs text-gray-600 mt-1">{fp.get("description", "")}</p>
                        </div>
                    </div>
                    ''' for fp in company.get("featured_products", []))}
                </div>
            </div>
            ''' if company.get("featured_products") else ''}
            {f'<a href="{company["website"]}" target="_blank" class="inline-flex items-center text-blue-600 hover:text-blue-800 mt-2"><i class="fas fa-external-link-alt mr-1"></i> 访问官网</a>' if company.get("website") else ''}
        </div>
        '''
        
        terminal_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative"  onclick="openModal('{escape_js(company["name"])}', '{escape_js(detail_content)}')">
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
                    {''.join(f'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{p}</span>' for p in company.get("products", [])[:3])}
                    {f'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 3}</span>' if len(company.get("products", [])) > 3 else ''}
                </div>
            </div>
        </div>
        ''')
    
    terminal_html.append('</div>')
    
    # 国际厂商
    terminal_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>国际厂商</h3>')
    terminal_html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">')
    
    for company in data["companies"]["international"]:
        detail_content = f'''
        <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-sm text-gray-500">国家/地区</p>
                    <p class="font-medium">{company.get("region", "-")}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">成立时间</p>
                    <p class="font-medium">{company.get("founded", "-")}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">主要客户</p>
                    <p class="font-medium">{company.get("customers", "-")}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">核心技术</p>
                    <p class="font-medium">{company.get("tech", "-")}</p>
                </div>
            </div>
            <div>
                <p class="text-sm text-gray-500 mb-2">主营业务</p>
                <p class="text-gray-700">{company.get("focus", "-")}</p>
            </div>
            <div>
                <p class="text-sm text-gray-500 mb-2">公司简介</p>
                <p class="text-gray-700">{company.get("description", "暂无简介")}</p>
            </div>
            <div>
                <p class="font-semibold mb-2">主要产品:</p>
                <div class="flex flex-wrap gap-2">
                    {''.join(f'<span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">{p}</span>' for p in company.get("products", []))}
                </div>
            </div>
            {f'<a href="{company["website"]}" target="_blank" class="inline-flex items-center text-blue-600 hover:text-blue-800 mt-2"><i class="fas fa-external-link-alt mr-1"></i> 访问官网</a>' if company.get("website") else ''}
        </div>
        '''
        
        terminal_html.append(f'''         <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal('{escape_js(company["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold">{company["name"]}</h3>
                <span class="text-xs text-gray-500">{company.get("region", "")}</span>
            </div>
            <div class="mt-2 text-sm space-y-1">
                <p><span class="text-gray-500">聚焦:</span> {company["focus"]}</p>
                <p><span class="text-gray-500">技术:</span> {company["tech"]}</p>
                <p><span class="text-gray-500">客户:</span> <span class="text-xs">{company.get("customers", "-")}</span></p>
            </div>
            <div class="mt-3">
                <span class="text-xs text-gray-500">产品:</span>
                <div class="flex flex-wrap gap-1 mt-1">
                    {''.join(f'<span class="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded">{p}</span>' for p in company.get("products", [])[:2])}
                    {f'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 2}</span>' if len(company.get("products", [])) > 2 else ''}
                </div>
            </div>
        </div>
        ''')
    
    terminal_html.append('</div></section>')
    content.append("".join(terminal_html))
    
    # 商业层、政策层、技术趋势、最新动态保持原有逻辑
    # ... (省略重复代码，保留原有功能)
    
    # 商业层
    if "business_models" in data:
        commercial_html = ['<section id="commercial"><h2 class="text-2xl font-bold mb-4">💰 商业模式</h2>']
        
        commercial_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国内商业模式</h3>')
        commercial_html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">')
        for model in data["business_models"].get("domestic", []):
            commercial_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 border-l-4 border-green-500">
                <h4 class="font-bold text-lg">{model["model"]}</h4>
                <p class="text-gray-600 text-sm mt-2">{model["description"]}</p>
                <div class="mt-3">
                    <span class="text-xs text-gray-500">主要玩家:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                        {''.join(f'<span class="bg-green-50 text-green-700 text-xs px-2 py-0.5 rounded">{p}</span>' for p in model.get("players", []))}
                    </div>
                </div>
            </div>
            ''')
        commercial_html.append('</div>')
        
        if "price_comparison" in data["business_models"]:
            commercial_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">价格对比</h3>')
            commercial_html.append('<div class="bg-white rounded-lg shadow overflow-hidden">')
            commercial_html.append('''
            <table class="min-w-full text-sm">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-4 py-2 text-left">服务</th>
                        <th class="px-4 py-2 text-left">终端价格</th>
                        <th class="px-4 py-2 text-left">月费</th>
                        <th class="px-4 py-2 text-left">速率</th>
                    </tr>
                </thead>
                <tbody>
            ''')
            for item in data["business_models"]["price_comparison"].get("broadband", []):
                terminal = f"${item['terminal_usd']}" if 'terminal_usd' in item else f"¥{item.get('terminal_cny', '-')}"
                monthly = f"${item['monthly_usd']}/月" if 'monthly_usd' in item else f"¥{item.get('monthly_cny', '-')}/月"
                commercial_html.append(f'''
                <tr class="border-t">
                    <td class="px-4 py-2">{item["service"]}</td>
                    <td class="px-4 py-2">{terminal}</td>
                    <td class="px-4 py-2">{monthly}</td>
                    <td class="px-4 py-2">{item["speed"]}</td>
                </tr>
                ''')
            commercial_html.append('</tbody></table></div>')
        
        commercial_html.append('</section>')
        content.append("".join(commercial_html))
    
    # 政策层
    if "policy" in data:
        policy_html = ['<section id="policy"><h2 class="text-2xl font-bold mb-4">📜 政策法规</h2>']
        
        policy_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国内政策</h3>')
        policy_html.append('<div class="space-y-3 mb-6">')
        for policy in data["policy"].get("china", []):
            impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
            color = impact_colors.get(policy.get("impact", "low"), "gray")
            policy_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                <div class="flex justify-between items-start">
                    <h4 class="font-bold">{policy["title"]}</h4>
                    <span class="text-xs text-gray-500">{policy["date"]} · {policy["issuer"]}</span>
                </div>
                <p class="text-gray-600 text-sm mt-2">{policy["content"]}</p>
            </div>
            ''')
        policy_html.append('</div>')
        
        if data["policy"].get("international"):
            policy_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国际政策</h3>')
            policy_html.append('<div class="space-y-3">')
            for policy in data["policy"]["international"]:
                impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
                color = impact_colors.get(policy.get("impact", "low"), "gray")
                policy_html.append(f'''
                <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold">{policy["title"]}</h4>
                        <span class="text-xs text-gray-500">{policy["date"]} · {policy["issuer"]}</span>
                    </div>
                    <p class="text-gray-600 text-sm mt-2">{policy["content"]}</p>
                </div>
                ''')
            policy_html.append('</div>')
        
        policy_html.append('</section>')
        content.append("".join(policy_html))
    
    # 技术趋势
    tech_html = ['<section id="tech"><h2 class="text-2xl font-bold mb-4">🔬 技术趋势</h2>']
    tech_html.append('<div class="space-y-4">')
    
    for trend in data.get("tech_trends", []):
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
    news_html = ['<section id="news"><h2 class="text-2xl font-bold mb-4">📰 最新动态</h2>']
    if data.get("news"):
        news_html.append('<div class="space-y-4">')
        for news in data["news"][:10]:
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
        news_html.append('</div>')
    else:
        news_html.append('''
        <div class="bg-gray-100 rounded-lg p-8 text-center">
            <i class="fas fa-newspaper text-gray-400 text-4xl mb-3"></i>
            <p class="text-gray-500">暂无最新动态数据</p>
            <p class="text-xs text-gray-400 mt-2">动态数据将由 GitHub Actions 每日自动抓取更新</p>
        </div>
        ''')
    news_html.append('</section>')
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
    generate()
