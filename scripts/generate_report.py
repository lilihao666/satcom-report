#!/usr/bin/env python3
"""
报告生成器 - 从JSON数据生成完整HTML报告（支持分类显示）
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
            transition: all 0.2s;
        }
        .clickable-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* 分类标签 */
        .category-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }
        .cat-internet { background: #dbeafe; color: #1e40af; }
        .cat-iot { background: #dcfce7; color: #166534; }
        .cat-mixed { background: #fef3c7; color: #92400e; }
    </style>
</head>
<body class="bg-gray-100">
    <!-- 导航栏 -->
    <nav class="bg-white shadow-sm sticky top-0 z-50 no-print">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <i class="fas fa-satellite text-blue-600 text-2xl mr-2"></i>
                    <span class="font-bold text-xl">卫星通信产业调研报告</span>
                </div>
                <div class="hidden md:flex space-x-6 text-sm font-medium">
                    <a href="#constellation" class="tab-inactive hover:text-blue-600 py-5 transition">星座层</a>
                    <a href="#terminal" class="tab-inactive hover:text-blue-600 py-5 transition">终端层</a>
                    <a href="#commercial" class="tab-inactive hover:text-blue-600 py-5 transition">商业层</a>
                    <a href="#policy" class="tab-inactive hover:text-blue-600 py-5 transition">政策层</a>
                    <a href="#tech" class="tab-inactive hover:text-blue-600 py-5 transition">技术趋势</a>
                    <a href="#news" class="tab-inactive hover:text-blue-600 py-5 transition">最新动态</a>
                </div>
                <div class="flex items-center space-x-3">
                    <button onclick="window.print()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition flex items-center text-sm no-print">
                        <i class="fas fa-file-pdf mr-2"></i>导出PDF
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- 主内容 -->
    <main class="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {{content}}
    </main>

    <!-- 页脚 -->
    <footer class="bg-gray-800 text-gray-400 py-6 mt-12 no-print">
        <div class="max-w-7xl mx-auto px-4 text-center text-sm">
            <p>卫星通信产业调研报告 | 数据更新时间: {{date}}</p>
            <p class="mt-1">本报告由 GitHub Actions 自动更新生成</p>
        </div>
    </footer>

    <!-- 详情弹窗 -->
    <div id="detail-modal" class="modal-overlay" onclick="closeModal(event)">
        <div class="modal-content relative">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div class="modal-header" id="modal-header">
                <h3 class="text-xl font-bold">详情</h3>
            </div>
            <div class="modal-body" id="modal-body">
            </div>
        </div>
    </div>

    <!-- 回到顶部按钮 -->
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
    """转义JavaScript字符串"""
    if not s:
        return ""
    s = ' '.join(s.split())
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '&quot;')

def get_category_class(category):
    """获取分类样式类"""
    if '互联网' in category:
        return 'cat-internet'
    elif '物联网' in category:
        return 'cat-iot'
    return 'cat-mixed'

def generate_company_detail(company, is_domestic=True):
    """生成厂商详情内容"""
    detail_links_html = ""
    if company.get('detail_links'):
        links_items = []
        for link_name, link_url in company['detail_links'].items():
            color = 'blue' if is_domestic else 'green'
            links_items.append(f'<a href="{link_url}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-{color}-50 text-{color}-600 rounded-lg text-sm hover:bg-{color}-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>{link_name}</a>')
        detail_links_html = f'''
        <div>
            <p class="font-semibold mb-2">🔍 {"详细调研" if is_domestic else "More Info"}:</p>
            <div class="flex flex-wrap gap-2">
                {''.join(links_items)}
            </div>
        </div>
        '''
    
    # 分类标签
    category = company.get('category', '综合终端')
    cat_class = get_category_class(category)
    
    if is_domestic:
        return f'''
        <div class="space-y-4">
            <div class="flex justify-between items-center">
                <span class="category-badge {cat_class}">{category}</span>
                <span class="text-xs text-gray-500">{company.get("city", "")}</span>
            </div>
            <div class="grid grid-cols-2 gap-4">
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
            {detail_links_html}
            {f'''
            <div>
                <p class="font-semibold mb-3">代表产品:</p>
                <div class="grid grid-cols-1 gap-3">
                    {''.join(f'''
                    <div class="flex gap-3 p-3 bg-gray-50 rounded-lg">
                        <img src="{fp.get("image", "")}" alt="{fp.get("name", "")}" class="w-20 h-20 object-cover rounded-lg" onerror="this.style.display='none'">
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
    else:
        return f'''
        <div class="space-y-4">
            <div class="flex justify-between items-center">
                <span class="category-badge {cat_class}">{category}</span>
                <span class="text-xs text-gray-500">{company.get("region", "")}</span>
            </div>
            <div class="grid grid-cols-2 gap-4">
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
            {detail_links_html}
            {f'<a href="{company["website"]}" target="_blank" class="inline-flex items-center text-blue-600 hover:text-blue-800 mt-2"><i class="fas fa-external-link-alt mr-1"></i> Website</a>' if company.get("website") else ''}
        </div>
        '''

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
    
    # 星座层
    constellation_html = ['<section id="constellation"><h2 class="text-2xl font-bold mb-4">🌐 卫星星座对比</h2>']
    
    # 按分类分组显示国内星座
    domestic_by_category = {}
    for c in data["constellations"]["domestic"]:
        cat = c.get("category", "综合应用")
        domestic_by_category.setdefault(cat, []).append(c)
    
    for category, constellations in domestic_by_category.items():
        cat_class = get_category_class(category)
        constellation_html.append(f'''
        <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="category-badge {cat_class} mr-2">{category}</span>
            国内星座
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        ''')
        
        for c in constellations:
            progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
            note = c.get("note", "")
            note_html = f'<p class="text-xs text-orange-600 mt-1">{note}</p>' if note else ""
            
            # 详情内容
            isl = c.get("inter_satellite_link", {})
            isl_html = ""
            if isl:
                isl_status = "✅ 支持" if isl.get("enabled") else "❌ 不支持"
                isl_tech = isl.get("tech", "-")
                isl_bw = isl.get("bandwidth", "-")
                isl_note = isl.get("note", "")
                isl_html = f'''
                <div class="bg-blue-50 p-3 rounded-lg">
                    <p class="font-semibold text-blue-800 mb-2"><i class="fas fa-satellite mr-1"></i> 星间链路</p>
                    <p class="text-sm text-blue-700"><strong>状态:</strong> {isl_status}</p>
                    <p class="text-sm text-blue-700"><strong>技术:</strong> {isl_tech}</p>
                    {f'<p class="text-sm text-blue-700"><strong>带宽:</strong> {isl_bw}</p>' if isl.get("bandwidth") != "-" else ''}
                    {f'<p class="text-xs text-blue-600 mt-1"><i class="fas fa-info-circle mr-1"></i> {isl_note}</p>' if isl_note else ''}
                </div>
                '''
            
            # 详情链接
            detail_links_html = ""
            if c.get('detail_links'):
                links_items = []
                for link_name, link_url in c['detail_links'].items():
                    links_items.append(f'<a href="{link_url}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-sm hover:bg-red-100 transition"><i class="fas fa-search mr-1.5"></i>{link_name}</a>')
                detail_links_html = f'''
                <div>
                    <p class="font-semibold mb-2">🔍 了解更多:</p>
                    <div class="flex flex-wrap gap-2">
                        {''.join(links_items)}
                    </div>
                </div>
                '''
            
            detail_content = f'''
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <span class="category-badge {cat_class}">{category}</span>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">{c["stage"]}</span>
                </div>
                <div>
                    <p class="text-gray-600"><strong>运营方:</strong> {c["operator"]}</p>
                    <p class="text-gray-600"><strong>规划数量:</strong> {c["planned"]:,} 颗</p>
                    <p class="text-gray-600"><strong>已发射:</strong> {c["launched"]} 颗</p>
                </div>
                {isl_html}
                {detail_links_html}
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
                    <div>
                        <h3 class="font-bold text-lg">{c["name"]}</h3>
                        <span class="category-badge {cat_class} mt-1">{category}</span>
                    </div>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">{c["stage"]}</span>
                </div>
                <p class="text-gray-600 text-sm mt-2">{c["operator"]}</p>
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
    
    # 国际星座（简化显示）
    constellation_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>国际星座</h3>')
    constellation_html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4">')
    for c in data["constellations"]["international"]:
        progress = (c.get("launched", 0) / c.get("planned", 1)) * 100
        constellation_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 border-l-4 border-green-500">
            <div class="flex justify-between items-start">
                <h3 class="font-bold">{c["name"]}</h3>
                <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">{c["stage"]}</span>
            </div>
            <p class="text-gray-600 text-sm">{c["operator"]}</p>
            <div class="mt-2 text-sm">
                <span>{c["launched"]:,}颗 / {c["planned"]:,}颗</span>
                <span class="text-gray-400 ml-2">({progress:.1f}%)</span>
            </div>
        </div>
        ''')
    constellation_html.append('</div>')
    
    constellation_html.append('</section>')
    content.append("".join(constellation_html))
    
    # 终端层 - 按分类分组
    terminal_html = ['<section id="terminal"><h2 class="text-2xl font-bold mb-4">📱 终端设备厂商</h2>']
    
    # 国内厂商按分类分组
    domestic_by_cat = {}
    for c in data["companies"]["domestic"]:
        cat = c.get("category", "综合终端")
        domestic_by_cat.setdefault(cat, []).append(c)
    
    for category, companies in domestic_by_cat.items():
        cat_class = get_category_class(category)
        terminal_html.append(f'''
        <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="category-badge {cat_class} mr-2">{category}</span>
            国内厂商
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        ''')
        
        for company in companies:
            detail_content = generate_company_detail(company, True)
            cat_badge = f'<span class="category-badge {cat_class}">{category}</span>'
            
            terminal_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal('{escape_js(company["name"])}', '{escape_js(detail_content)}')">
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="font-bold">{company["name"]}</h3>
                        {cat_badge}
                    </div>
                    <span class="text-xs text-gray-500">{company.get("city", "")}</span>
                </div>
                <div class="mt-2 text-sm space-y-1">
                    <p><span class="text-gray-500">聚焦:</span> {company["focus"]}</p>
                    <p><span class="text-gray-500">技术:</span> {company["tech"]}</p>
                </div>
                <div class="mt-3">
                    <span class="text-xs text-gray-500">产品:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                        {''.join(f'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{p}</span>' for p in company.get("products", [])[:3])}
                    </div>
                </div>
                <div class="mt-3 pt-2 border-t border-gray-100 text-center">
                    <span class="text-xs text-blue-500"><i class="fas fa-hand-pointer mr-1"></i>点击查看详情</span>
                </div>
            </div>
            ''')
        
        terminal_html.append('</div>')
    
    # 国际厂商
    terminal_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国际厂商</h3>')
    terminal_html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">')
    for company in data["companies"]["international"]:
        detail_content = generate_company_detail(company, False)
        terminal_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal('{escape_js(company["name"])}', '{escape_js(detail_content)}')">
            <div class="flex justify-between items-start">
                <h3 class="font-bold">{company["name"]}</h3>
                <span class="text-xs text-gray-500">{company.get("region", "")}</span>
            </div>
            <div class="mt-2 text-sm space-y-1">
                <p><span class="text-gray-500">聚焦:</span> {company["focus"]}</p>
            </div>
            <div class="mt-3 pt-2 border-t border-gray-100 text-center">
                <span class="text-xs text-blue-500"><i class="fas fa-hand-pointer mr-1"></i>点击查看详情</span>
            </div>
        </div>
        ''')
    terminal_html.append('</div></section>')
    content.append("".join(terminal_html))
    
    # 商业层、政策层、技术趋势、最新动态
    # ... (省略，与之前相同)
    
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
        commercial_html.append('</section>')
        content.append("".join(commercial_html))
    
    # 政策层
    if "policy" in data:
        policy_html = ['<section id="policy"><h2 class="text-2xl font-bold mb-4">📜 政策法规</h2>']
        
        # 国内政策
        policy_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国内政策</h3>')
        policy_html.append('<div class="space-y-3 mb-6">')
        for policy in data["policy"].get("china", []):
            impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
            color = impact_colors.get(policy.get("impact", "low"), "gray")
            url = policy.get("url", "#")
            policy_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                <div class="flex justify-between items-start">
                    <h4 class="font-bold">{policy["title"]}</h4>
                    <span class="text-xs text-gray-500">{policy["date"]} · {policy["issuer"]}</span>
                </div>
                <p class="text-gray-600 text-sm mt-2">{policy["content"]}</p>
                <div class="mt-2 text-right">
                    <a href="{url}" target="_blank" class="text-xs text-blue-600 hover:underline">
                        <i class="fas fa-external-link-alt mr-1"></i>查看详情
                    </a>
                </div>
            </div>
            ''')
        policy_html.append('</div>')
        
        # 国际政策
        if data["policy"].get("international"):
            policy_html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国际政策</h3>')
            policy_html.append('<div class="space-y-3 mb-6">')
            for policy in data["policy"].get("international", []):
                impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
                color = impact_colors.get(policy.get("impact", "low"), "gray")
                url = policy.get("url", "#")
                policy_html.append(f'''
                <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold">{policy["title"]}</h4>
                        <span class="text-xs text-gray-500">{policy["date"]} · {policy["issuer"]}</span>
                    </div>
                    <p class="text-gray-600 text-sm mt-2">{policy["content"]}</p>
                    <div class="mt-2 text-right">
                        <a href="{url}" target="_blank" class="text-xs text-blue-600 hover:underline">
                            <i class="fas fa-external-link-alt mr-1"></i>查看详情
                        </a>
                    </div>
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
        url = trend.get("url", "#")
        tech_html.append(f'''
        <div class="bg-white rounded-lg shadow p-4">
            <div class="flex justify-between items-start">
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <h3 class="font-bold text-lg">{trend["trend"]}</h3>
                        <span class="bg-{color}-100 text-{color}-800 text-xs px-3 py-1 rounded-full">{trend["status"]}</span>
                    </div>
                    <p class="text-gray-600 text-sm mt-1">{trend["description"]}</p>
                    <div class="mt-2 flex justify-between items-center">
                        <span class="text-xs text-gray-500">主要推动者: {', '.join(trend.get("leaders", []))}</span>
                        <a href="{url}" target="_blank" class="text-xs text-blue-600 hover:underline">
                            <i class="fas fa-external-link-alt mr-1"></i>了解更多
                        </a>
                    </div>
                </div>
            </div>
        </div>
        ''')
    tech_html.append('</div></section>')
    content.append("".join(tech_html))
    
    # 最新动态 - 带链接
    news_html = ['<section id="news"><h2 class="text-2xl font-bold mb-4">📰 最新动态</h2>']
    if data.get("news"):
        news_html.append('<div class="space-y-4">')
        for news in data["news"][:10]:
            impact = news.get("impact_analysis", {}).get("level", "low")
            impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
            color = impact_colors.get(impact, "gray")
            url = news.get("url", "#")
            
            news_html.append(f'''
            <div class="bg-white rounded-lg shadow p-4 border-l-4 border-{color}-500">
                <div class="flex justify-between items-start">
                    <h3 class="font-bold">{news["title"]}</h3>
                    <span class="text-xs text-gray-500">{news["date"]}</span>
                </div>
                <p class="text-gray-600 text-sm mt-2">{news["summary"]}</p>
                <div class="mt-2 flex justify-between items-center text-xs">
                    <a href="{url}" target="_blank" class="text-blue-600 hover:underline">
                        <i class="fas fa-external-link-alt mr-1"></i>来源: {news["source"]}
                    </a>
                    <div class="flex gap-1">
                        {''.join(f'<span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded">{t}</span>' for t in news.get("tags", []))}
                    </div>
                </div>
            </div>
            ''')
        news_html.append('</div>')
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
