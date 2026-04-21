#!/usr/bin/env python3
"""
报告生成器 - 从JSON数据生成完整HTML报告（修复引号转义问题）
"""
import json
import base64
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
        
        .clickable-card {
            cursor: pointer;
            transition: all 0.2s;
        }
        .clickable-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
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
                    <a href="#payload" class="tab-inactive hover:text-blue-600 py-5 transition">载荷层</a>
                    <a href="#operator" class="tab-inactive hover:text-blue-600 py-5 transition">运营商</a>
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
        
        <!-- 执行摘要 -->
        {{summary}}
        
        <!-- 卫星星座 -->
        {{constellations}}
        
        <!-- 终端设备 -->
        {{terminals}}
        
        <!-- 卫星载荷 -->
        {{payloads}}
        
        <!-- 卫星运营商 -->
        {{operators}}
        
        <!-- 商业模式 -->
        {{commercial}}
        
        <!-- 政策法规 -->
        {{policy}}
        
        <!-- 技术趋势 -->
        {{tech_trends}}
        
        <!-- 最新动态 -->
        {{news}}
        
    </main>

    <!-- 回到顶部按钮 -->
    <button id="back-to-top" onclick="scrollToTop()" class="hidden no-print">
        <i class="fas fa-arrow-up"></i>
    </button>

    <!-- 详情弹窗 -->
    <div id="detail-modal" class="modal-overlay no-print" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header relative">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                <h3 id="modal-title" class="text-xl font-bold"></h3>
            </div>
            <div id="modal-body" class="modal-body"></div>
        </div>
    </div>

    <!-- 详情数据存储 -->
    <script>
        // 详情弹窗数据
        const modalData = {{modal_data_json}};
        
        // 回到顶部
        const backToTopBtn = document.getElementById('back-to-top');
        window.onscroll = function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                backToTopBtn.classList.remove('hidden');
            } else {
                backToTopBtn.classList.add('hidden');
            }
        };
        function scrollToTop() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        
        // 弹窗控制
        function openModal(id) {
            const data = modalData[id];
            if (!data) return;
            document.getElementById('modal-title').textContent = data.title;
            document.getElementById('modal-body').innerHTML = data.content;
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
</html>
'''

def generate_summary(data):
    """生成执行摘要"""
    return f'''
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
                <div class="text-3xl font-bold">10,861</div>
                <div class="text-sm opacity-80">全球在轨卫星</div>
            </div>
            <div class="bg-white/10 rounded-lg p-4">
                <div class="text-3xl font-bold">{len(data.get("news", []))}</div>
                <div class="text-sm opacity-80">近期动态</div>
            </div>
        </div>
    </div>
    '''

def generate_constellations(data):
    """生成星座对比部分"""
    html = []
    modal_data = {}
    html.append('<section id="constellation"><h2 class="text-2xl font-bold mb-4">🌐 卫星星座对比</h2>')
    
    # 国内星座 - 卫星互联网
    html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">卫星互联网</span>国内星座</h3>')
    html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">')
    for const in data['constellations']['domestic']:
        if const.get('category') == '卫星互联网':
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
    html.append('</div>')
    
    # 国内星座 - 卫星物联网
    html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-iot mr-2">卫星物联网</span>国内星座</h3>')
    html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">')
    for const in data['constellations']['domestic']:
        if const.get('category') == '卫星物联网':
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
    html.append('</div>')
    
    # 高轨卫星
    if 'geo_domestic' in data['constellations']:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-mixed mr-2">高轨卫星</span>国内星座</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">')
        for const in data['constellations']['geo_domestic']:
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    # 国际星座 - 按分类展示
    # 卫星互联网
    intl_internet = [c for c in data['constellations']['international'] if c.get('category') == '卫星互联网']
    if intl_internet:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">卫星互联网</span>国际星座</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for const in intl_internet:
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    # 卫星物联网
    intl_iot = [c for c in data['constellations']['international'] if c.get('category') == '卫星物联网']
    if intl_iot:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-iot mr-2">卫星物联网</span>国际星座</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for const in intl_iot:
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    # 国际高轨卫星
    if 'geo_international' in data['constellations'] and data['constellations']['geo_international']:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-mixed mr-2">高轨卫星</span>国际星座</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for const in data['constellations']['geo_international']:
            card_html, modal_id, modal_content = generate_constellation_card(const)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    html.append('</section>')
    return '\n'.join(html), modal_data

def generate_constellation_card(const):
    """生成星座卡片，返回卡片HTML、modal ID和modal内容"""
    category = const.get('category', '卫星互联网')
    cat_class = 'cat-internet' if '互联网' in category else 'cat-iot'
    progress = (const.get('launched', 0) / max(const.get('planned', 1), 1)) * 100
    modal_id = f"const_{const['name'].replace(' ', '_').replace('/', '_')}"
    
    # 构建详情弹窗内容
    inter_satellite = const.get('inter_satellite_link', {})
    if inter_satellite.get('enabled'):
        bandwidth_line = f'<p class="text-sm text-blue-700"><strong>带宽:</strong> {inter_satellite.get("bandwidth")}</p>' if inter_satellite.get('bandwidth') else ''
        note_line = f'<p class="text-xs text-blue-600 mt-1"><i class="fas fa-info-circle mr-1"></i> {inter_satellite.get("note")}</p>' if inter_satellite.get('note') else ''
        isl_html = f'<div class="bg-blue-50 p-3 rounded-lg"><p class="font-semibold text-blue-800 mb-2"><i class="fas fa-satellite mr-1"></i> 星间链路</p><p class="text-sm text-blue-700"><strong>状态:</strong> ✅ 支持</p><p class="text-sm text-blue-700"><strong>技术:</strong> {inter_satellite.get("tech", "未知")}</p>{bandwidth_line}{note_line}</div>'
    else:
        isl_html = f'<div class="bg-gray-50 p-3 rounded-lg"><p class="font-semibold text-gray-700 mb-2"><i class="fas fa-satellite mr-1"></i> 星间链路</p><p class="text-sm text-gray-600">{inter_satellite.get("note", "无星间链路")}</p></div>'
    
    # 构建链接
    links = []
    if 'detail_links' in const:
        for k, v in const['detail_links'].items():
            links.append(f'<a href="{v}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>{k}</a>')
    links_html = '<div class="flex flex-wrap gap-2">' + ''.join(links) + '</div>'
    
    # 场景标签
    use_cases = const.get('use_cases', [])
    use_cases_html = '<div class="flex flex-wrap gap-2">' + ''.join([f'<span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">{uc}</span>' for uc in use_cases]) + '</div>'
    
    modal_content = {
        'title': const['name'],
        'content': f'''<div class="space-y-4">
            <div class="flex justify-between items-center"><span class="category-badge {cat_class}">{category}</span><span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">{const.get("stage", "规划中")}</span></div>
            <div><p class="text-gray-600"><strong>运营方:</strong> {const.get("operator", "未知")}</p><p class="text-gray-600"><strong>规划数量:</strong> {const.get("planned", 0):,} 颗</p><p class="text-gray-600"><strong>已发射:</strong> {const.get("launched", 0)} 颗</p></div>
            {isl_html}
            <div><p class="font-semibold mb-2">🔍 了解更多:</p>{links_html}</div>
            <div><p class="font-semibold mb-2">应用场景:</p>{use_cases_html}</div>
            <div class="mt-4"><p class="text-sm text-gray-500 mb-2">部署进度: {progress:.1f}%</p><div class="w-full bg-gray-200 rounded-full h-3"><div class="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full" style="width: {min(progress, 100)}%"></div></div></div>
        </div>'''
    }
    
    card = f'''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500 clickable-card relative" onclick="openModal('{modal_id}')">
        <div class="flex justify-between items-start">
            <div>
                <h3 class="font-bold text-lg">{const['name']}</h3>
                <span class="category-badge {cat_class} mt-1">{category}</span>
            </div>
            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">{const.get('stage', '规划中')}</span>
        </div>
        <p class="text-gray-600 text-sm mt-2">{const.get('operator', '未知')}</p>
        <div class="mt-3">
            <div class="flex justify-between text-sm mb-1">
                <span>在轨: {const.get('launched', 0)}颗</span>
                <span class="text-gray-500">规划: {const.get('planned', 0):,}颗</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full" style="width: {min(progress, 100)}%"></div>
            </div>
        </div>
        {'<p class="text-xs text-gray-500 mt-2">' + const.get('note', '') + '</p>' if const.get('note') else ''}
    </div>'''
    
    return card, modal_id, modal_content

def generate_terminals(data):
    """生成终端设备部分"""
    html = []
    modal_data = {}
    html.append('<section id="terminal"><h2 class="text-2xl font-bold mb-4">📱 终端设备厂商</h2>')
    
    # 国内厂商 - 按类别分组
    domestic = data['companies']['domestic']
    
    # 卫星物联网终端
    iot_companies = [c for c in domestic if c.get('category') == '卫星物联网终端']
    if iot_companies:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-iot mr-2">卫星物联网终端</span>国内厂商</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for company in iot_companies:
            card_html, modal_id, modal_content = generate_terminal_card(company)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    # 卫星互联网终端
    internet_companies = [c for c in domestic if c.get('category') == '卫星互联网终端']
    if internet_companies:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">卫星互联网终端</span>国内厂商</h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for company in internet_companies:
            card_html, modal_id, modal_content = generate_terminal_card(company)
            html.append(card_html)
            modal_data[modal_id] = modal_content
        html.append('</div>')
    
    # 国际厂商
    html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700">国际厂商</h3>')
    html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">')
    for company in data['companies']['international']:
        card_html, modal_id, modal_content = generate_terminal_card(company, is_international=True)
        html.append(card_html)
        modal_data[modal_id] = modal_content
    html.append('</div>')
    
    html.append('</section>')
    return '\n'.join(html), modal_data

def generate_terminal_card(company, is_international=False):
    """生成终端厂商卡片"""
    category = company.get('category', '卫星物联网终端')
    cat_class = 'cat-iot' if '物联网' in category else 'cat-internet'
    location = company.get('region' if is_international else 'city', '未知')
    modal_id = f"comp_{company['name'].replace(' ', '_').replace('/', '_')}"
    
    # 构建链接
    links = []
    if 'detail_links' in company:
        for k, v in company['detail_links'].items():
            icon = 'fa-external-link-alt' if 'http' in v else 'fa-search'
            links.append(f'<a href="{v}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas {icon} mr-1.5"></i>{k}</a>')
    links_html = '<div class="flex flex-wrap gap-2">' + ''.join(links) + '</div>'
    
    # 产品标签
    products = company.get('products', [])
    products_html = '<div class="flex flex-wrap gap-2">' + ''.join([f'<span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">{p}</span>' for p in products[:3]]) + '</div>'
    
    # 产品图片展示
    featured_products = company.get('featured_products', [])
    featured_html = ''
    if featured_products:
        fp_items = []
        for fp in featured_products[:4]:
            img = fp.get('image', '')
            if img and not img.startswith('https://via.placeholder'):
                fp_items.append(f'<div class="text-center"><img src="{img}" class="w-full h-20 object-cover rounded mb-1" loading="lazy"><p class="text-xs font-medium">{fp["name"]}</p></div>')
            else:
                fp_items.append(f'<div class="bg-gray-50 p-2 rounded text-center"><p class="font-medium text-sm">{fp["name"]}</p><p class="text-xs text-gray-500">{fp.get("description", "")[:25]}...</p></div>')
        if fp_items:
            featured_html = '<div><p class="font-semibold mb-2">🎁 典型产品:</p><div class="grid grid-cols-2 gap-2">' + ''.join(fp_items) + '</div></div>'
    
    modal_content = {
        'title': company['name'],
        'content': f'''<div class="space-y-4">
            <div class="flex justify-between items-center"><span class="category-badge {cat_class}">{category}</span><span class="text-xs text-gray-500">{location}</span></div>
            <div class="grid grid-cols-2 gap-4">
                <div><p class="text-sm text-gray-500">成立时间</p><p class="font-medium">{company.get("founded", "未知")}</p></div>
                <div><p class="text-sm text-gray-500">融资阶段</p><p class="font-medium"><span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">{company.get("funding", "未知")}</span></p></div>
                <div><p class="text-sm text-gray-500">核心技术</p><p class="font-medium">{company.get("tech", "未知")}</p></div>
            </div>
            <div><p class="text-sm text-gray-500 mb-2">主营业务</p><p class="text-gray-700">{company.get("focus", "未知")}</p></div>
            <div><p class="text-sm text-gray-500 mb-2">公司简介</p><p class="text-gray-700">{company.get("description", "暂无描述")}</p></div>
            <div><p class="font-semibold mb-2">主要产品:</p>{products_html}</div>
            {featured_html}
            <div><p class="font-semibold mb-2">🔍 详细调研:</p>{links_html}</div>
        </div>'''
    }
    
    card = f'''<div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal('{modal_id}')">
        <div class="flex justify-between items-start mb-2">
            <div>
                <h3 class="font-bold text-lg">{company['name']}</h3>
                <span class="category-badge {cat_class} mt-1">{category}</span>
            </div>
            <span class="text-xs text-gray-500">{location}</span>
        </div>
        <p class="text-sm text-gray-600 mb-2"><strong>聚焦:</strong> {company.get('focus', '未知')}</p>
        <p class="text-sm text-gray-600 mb-3"><strong>技术:</strong> {company.get('tech', '未知')}</p>
        <div class="flex flex-wrap gap-2 mt-3">
            {''.join([f'<span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">{p}</span>' for p in products[:4]])}
        </div>
    </div>'''
    
    return card, modal_id, modal_content

def generate_payloads(data):
    """生成载荷层部分 - 使用实际数据"""
    payloads = data.get('payloads', {})
    html = ['<section id="payload"><h2 class="text-2xl font-bold mb-4">🔧 卫星载荷层</h2>']
    
    # 国内载荷厂商
    domestic_payloads = payloads.get('domestic', [])
    if domestic_payloads:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">国内载荷厂商</span></h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for p in domestic_payloads:
            name = p.get('name', '未知')
            tech = p.get('tech', '')
            products = p.get('products', [])
            desc = p.get('description', '')
            
            products_html = ''
            if products:
                products_html = '<div class="flex flex-wrap gap-1 mt-2">' + ''.join([f'<span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">{pr}</span>' for pr in products]) + '</div>'
            
            html.append(f'''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500">
                <h4 class="font-bold text-lg">{name}</h4>
                <p class="text-sm text-gray-500">{tech}</p>
                <p class="text-sm text-gray-600 mt-2">{desc}</p>
                {products_html}
            </div>''')
        html.append('</div>')
    
    # 国际载荷厂商
    intl_payloads = payloads.get('international', [])
    if intl_payloads:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">国际载荷厂商</span></h3>')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">')
        for p in intl_payloads:
            name = p.get('name', '未知')
            tech = p.get('tech', '')
            products = p.get('products', [])
            desc = p.get('description', '')
            
            products_html = ''
            if products:
                products_html = '<div class="flex flex-wrap gap-1 mt-2">' + ''.join([f'<span class="bg-purple-50 text-purple-700 px-2 py-0.5 rounded text-xs">{pr}</span>' for pr in products]) + '</div>'
            
            html.append(f'''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-purple-500">
                <h4 class="font-bold text-lg">{name}</h4>
                <p class="text-sm text-gray-500">{tech}</p>
                <p class="text-sm text-gray-600 mt-2">{desc}</p>
                {products_html}
            </div>''')
        html.append('</div>')
    
    # 载荷技术路线
    tech_roadmap = payloads.get('tech_roadmap', [])
    if tech_roadmap:
        html.append('<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-mixed mr-2">技术路线</span></h3>')
        html.append('<div class="bg-white rounded-lg shadow p-4">')
        html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-4">')
        for tr in tech_roadmap:
            stage = tr.get('stage', '')
            tech = tr.get('tech', '')
            status = tr.get('status', '')
            timeline = tr.get('timeline', '')
            key_players = tr.get('key_players', [])
            players_html = ''.join([f'<span class="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-xs mr-1">{kp}</span>' for kp in key_players])
            html.append(f'''<div class="border-l-4 border-green-500 pl-4">
                <h4 class="font-semibold text-green-700">{stage}</h4>
                <p class="text-sm text-gray-600 mt-1"><strong>技术:</strong> {tech}</p>
                <p class="text-sm text-gray-600"><strong>状态:</strong> {status} | <strong>时间:</strong> {timeline}</p>
                <div class="mt-2">{players_html}</div>
            </div>''')
        html.append('</div>')
        html.append('</div>')
    
    # 兜底：如果没有数据，显示静态内容
    if not domestic_payloads and not intl_payloads:
        html.append('''<div class="bg-white rounded-lg shadow p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="border-l-4 border-blue-500 pl-4">
                    <h3 class="font-bold text-lg mb-2">通信载荷</h3>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>• 相控阵天线</li>
                        <li>• 抛物面天线</li>
                        <li>• 平板天线</li>
                        <li>• 激光通信终端</li>
                    </ul>
                </div>
                <div class="border-l-4 border-green-500 pl-4">
                    <h3 class="font-bold text-lg mb-2">导航载荷</h3>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>• 原子钟</li>
                        <li>• 导航信号生成</li>
                        <li>• 星间链路设备</li>
                    </ul>
                </div>
                <div class="border-l-4 border-purple-500 pl-4">
                    <h3 class="font-bold text-lg mb-2">遥感载荷</h3>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>• 光学相机</li>
                        <li>• SAR雷达</li>
                        <li>• 红外探测器</li>
                    </ul>
                </div>
            </div>
        </div>''')
    
    html.append('</section>')
    return '\n'.join(html)

def generate_operators(data):
    """生成运营商部分"""
    return '''<section id="operator"><h2 class="text-2xl font-bold mb-4">📡 卫星运营商</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white rounded-lg shadow p-4">
            <h3 class="font-bold text-lg mb-3 text-blue-600">国内运营商</h3>
            <div class="space-y-3">
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">中国星网</span><span class="text-sm text-gray-500">GW星座运营</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">垣信卫星</span><span class="text-sm text-gray-500">千帆星座运营</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">国电高科</span><span class="text-sm text-gray-500">天启星座运营</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">时空道宇</span><span class="text-sm text-gray-500">吉利未来星座</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">中国卫通</span><span class="text-sm text-gray-500">中星系列</span></div>
            </div>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
            <h3 class="font-bold text-lg mb-3 text-purple-600">国际运营商</h3>
            <div class="space-y-3">
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">SpaceX Starlink</span><span class="text-sm text-gray-500">全球最大星座</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">Eutelsat OneWeb</span><span class="text-sm text-gray-500">企业宽带服务</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">Amazon Kuiper</span><span class="text-sm text-gray-500">部署中</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">Iridium</span><span class="text-sm text-gray-500">卫星电话/物联网</span></div>
                <div class="flex justify-between items-center p-2 bg-gray-50 rounded"><span class="font-medium">Intelsat/SES</span><span class="text-sm text-gray-500">GEO卫星运营</span></div>
            </div>
        </div>
    </div></section>'''

def generate_commercial(data):
    """生成商业模式部分"""
    html = ['<section id="commercial"><h2 class="text-2xl font-bold mb-4">💼 商业模式与定价</h2>']
    
    html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">')
    
    # 国内商业模式
    html.append('<div class="bg-white rounded-lg shadow p-4"><h3 class="font-bold text-lg mb-3">国内商业模式</h3><div class="space-y-3">')
    for model in data['business_models']['domestic']:
        html.append(f'''<div class="p-3 bg-gray-50 rounded-lg">
            <h4 class="font-semibold text-blue-700">{model['model']}</h4>
            <p class="text-sm text-gray-600 mt-1">{model['description']}</p>
            <p class="text-xs text-gray-500 mt-2">玩家: {', '.join(model['players'])}</p>
        </div>''')
    html.append('</div></div>')
    
    # 国际商业模式
    html.append('<div class="bg-white rounded-lg shadow p-4"><h3 class="font-bold text-lg mb-3">国际商业模式</h3><div class="space-y-3">')
    for model in data['business_models']['international']:
        html.append(f'''<div class="p-3 bg-gray-50 rounded-lg">
            <h4 class="font-semibold text-purple-700">{model['model']}</h4>
            <p class="text-sm text-gray-600 mt-1">{model['description']}</p>
            <p class="text-xs text-gray-500 mt-2">玩家: {', '.join(model['players'])}</p>
        </div>''')
    html.append('</div></div>')
    
    html.append('</div>')
    
    # 价格对比
    html.append('<div class="bg-white rounded-lg shadow overflow-hidden"><h3 class="font-bold text-lg p-4 border-b">价格对比</h3>')
    html.append('<div class="overflow-x-auto"><table class="w-full text-sm"><thead class="bg-gray-50"><tr><th class="p-3 text-left">服务</th><th class="p-3 text-right">终端价格</th><th class="p-3 text-right">月费</th><th class="p-3 text-left">速率</th></tr></thead><tbody>')
    for price in data['business_models']['price_comparison']['broadband']:
        terminal = price.get('terminal_usd', price.get('terminal_cny', '-'))
        monthly = price.get('monthly_usd', price.get('monthly_cny', '-'))
        currency = '$' if 'terminal_usd' in price else '¥'
        html.append(f'''<tr class="border-t"><td class="p-3 font-medium">{price['service']}</td>
            <td class="p-3 text-right">{currency}{terminal}</td>
            <td class="p-3 text-right">{currency}{monthly}</td>
            <td class="p-3">{price['speed']}</td></tr>''')
    html.append('</tbody></table></div></div>')
    
    html.append('</section>')
    return '\n'.join(html)

def generate_policy(data):
    """生成政策法规部分"""
    html = ['<section id="policy"><h2 class="text-2xl font-bold mb-4">⚖️ 政策法规</h2>']
    
    html.append('<div class="grid grid-cols-1 md:grid-cols-2 gap-6">')
    
    # 国内政策
    html.append('<div class="bg-white rounded-lg shadow p-4"><h3 class="font-bold text-lg mb-3 text-blue-600">国内政策</h3><div class="space-y-3">')
    for policy in data['policy']['china']:
        impact_color = 'red' if policy.get('impact') == 'high' else 'yellow'
        link_html = f'<a href="{policy.get("url", "#")}" target="_blank" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a>' if policy.get('url') else ''
        html.append(f'''<div class="p-3 bg-gray-50 rounded-lg border-l-4 border-{impact_color}-400">
            <div class="flex justify-between items-start">
                <h4 class="font-semibold">{policy['title']}</h4>
                <span class="text-xs text-gray-500">{policy.get('date', '未知')}</span>
            </div>
            <p class="text-xs text-gray-500 mt-1">{policy.get('department', '未知')}</p>
            <p class="text-sm text-gray-600 mt-2">{policy['summary']}</p>
            <div class="mt-2">{link_html}</div>
        </div>''')
    html.append('</div></div>')
    
    # 国际政策
    html.append('<div class="bg-white rounded-lg shadow p-4"><h3 class="font-bold text-lg mb-3 text-purple-600">国际政策</h3><div class="space-y-3">')
    for policy in data['policy']['international']:
        impact_color = 'red' if policy.get('impact') == 'high' else 'yellow'
        link_html = f'<a href="{policy.get("url", "#")}" target="_blank" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a>' if policy.get('url') else ''
        html.append(f'''<div class="p-3 bg-gray-50 rounded-lg border-l-4 border-{impact_color}-400">
            <div class="flex justify-between items-start">
                <h4 class="font-semibold">{policy['title']}</h4>
                <span class="text-xs text-gray-500">{policy.get('date', '未知')}</span>
            </div>
            <p class="text-xs text-gray-500 mt-1">{policy.get('country', '未知')}</p>
            <p class="text-sm text-gray-600 mt-2">{policy['summary']}</p>
            <div class="mt-2">{link_html}</div>
        </div>''')
    html.append('</div></div>')
    
    html.append('</div></section>')
    return '\n'.join(html)

def generate_tech_trends(data):
    """生成技术趋势部分"""
    html = ['<section id="tech"><h2 class="text-2xl font-bold mb-4">🔬 技术趋势</h2><div class="grid grid-cols-1 md:grid-cols-2 gap-4">']
    
    for trend in data['tech_trends']:
        status_color = {
            '商业化初期': 'yellow',
            '部署中': 'blue',
            '成本下降中': 'green',
            '早期应用': 'purple'
        }.get(trend.get('status', ''), 'gray')
        
        link_html = f'<a href="{trend.get("url", "#")}" target="_blank" class="text-blue-600 hover:underline text-sm mt-2 inline-block"><i class="fas fa-external-link-alt mr-1"></i>了解更多</a>' if trend.get('url') else ''
        
        html.append(f'''<div class="bg-white rounded-lg shadow p-4 clickable-card" onclick="window.open('{trend.get('url', '#')}', '_blank')">
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-bold text-lg">{trend['trend']}</h3>
                <span class="text-xs bg-{status_color}-100 text-{status_color}-800 px-2 py-1 rounded">{trend.get('status', '未知')}</span>
            </div>
            <p class="text-sm text-gray-600 mb-2">{trend['description']}</p>
            <div class="flex justify-between text-xs text-gray-500 mb-2">
                <span>时间线: {trend.get('timeline', '未知')}</span>
            </div>
            <p class="text-xs text-gray-500">领军: {', '.join(trend.get('leaders', []))}</p>
            {link_html}
        </div>''')
    
    html.append('</div></section>')
    return '\n'.join(html)

def generate_news(data):
    """生成最新动态部分"""
    html = ['<section id="news"><h2 class="text-2xl font-bold mb-4">📰 最新动态</h2><div class="space-y-4">']
    
    for item in data.get('news', [])[:10]:
        impact_color = 'red' if item.get('impact_analysis', {}).get('level') == 'high' else 'yellow'
        sectors = ', '.join(item.get('impact_analysis', {}).get('sectors', []))
        tags_html = ' '.join([f'<span class="bg-gray-100 text-gray-600 px-2 py-0.5 rounded text-xs">{t}</span>' for t in item.get('tags', [])])
        
        link_html = f'<a href="{item.get("url", "#")}" target="_blank" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看原文</a>' if item.get('url') else ''
        
        html.append(f'''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-{impact_color}-500">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{item['title']}</h3>
                <div class="text-right">
                    <span class="text-sm text-gray-500">{item.get('date', '未知')}</span>
                    <span class="text-xs bg-{impact_color}-100 text-{impact_color}-800 px-2 py-0.5 rounded ml-2">{item.get('impact_analysis', {}).get('level', 'medium')}影响</span>
                </div>
            </div>
            <p class="text-xs text-gray-500 mt-1">来源: {item.get('source', '未知')}</p>
            <p class="text-sm text-gray-600 mt-2">{item.get('summary', '暂无摘要')}</p>
            <div class="flex flex-wrap gap-2 mt-2">{tags_html}</div>
            <div class="mt-2 text-xs text-gray-500">影响领域: {sectors}</div>
            <div class="mt-2">{link_html}</div>
        </div>''')
    
    html.append('</div></section>')
    return '\n'.join(html)

def main():
    """主函数"""
    # 读取数据
    data_file = Path('/root/.openclaw/workspace/satcom-research-github/data/satcom_data.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = data.get('last_updated', datetime.now().strftime('%Y-%m-%d'))
    
    # 收集所有模态框数据
    all_modal_data = {}
    
    # 生成各部分
    constellations_html, constellations_modals = generate_constellations(data)
    all_modal_data.update(constellations_modals)
    
    terminals_html, terminals_modals = generate_terminals(data)
    all_modal_data.update(terminals_modals)
    
    # 生成模态框数据脚本
    modal_data_json = json.dumps(all_modal_data, ensure_ascii=False)
    
    # 替换模板
    report = TEMPLATE.replace('{{date}}', today)
    report = report.replace('{{summary}}', generate_summary(data))
    report = report.replace('{{constellations}}', constellations_html)
    report = report.replace('{{terminals}}', terminals_html)
    report = report.replace('{{payloads}}', generate_payloads(data))
    report = report.replace('{{operators}}', generate_operators(data))
    report = report.replace('{{commercial}}', generate_commercial(data))
    report = report.replace('{{policy}}', generate_policy(data))
    report = report.replace('{{tech_trends}}', generate_tech_trends(data))
    report = report.replace('{{news}}', generate_news(data))
    report = report.replace('{{modal_data_json}}', modal_data_json)
    
    # 保存报告
    output_file = Path('/root/.openclaw/workspace/satcom-research-github/index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已生成: {output_file}")
    print(f"📅 报告日期: {today}")
    print(f"📊 国内终端厂商: {len(data['companies']['domestic'])}家")
    print(f"🌍 国际终端厂商: {len(data['companies']['international'])}家")
    print(f"🛰️ 国内星座: {len(data['constellations']['domestic'])}个")
    print(f"🛰️ 国际星座: {len(data['constellations']['international'])}个")
    print(f"💬 模态框数据: {len(all_modal_data)}个")

if __name__ == '__main__':
    main()
