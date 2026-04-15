#!/usr/bin/env python3
"""
更新 generate_report.py，添加详情链接的展示
"""
import re

# 读取原文件
with open('/root/.openclaw/workspace/satcom-research-github/scripts/generate_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改国内厂商的 detail_content，添加详情链接
old_domestic_detail = '''        detail_content = f\'\'\'
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
                    {\'\'\'.join(f\'\'<span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">{p}</span>\'\' for p in company.get("products", []))}
                </div>
            </div>
            {f\'\'\'
            <div>
                <p class="font-semibold mb-3">代表产品:</p>
                <div class="grid grid-cols-1 gap-3">
                    {\'\'\'.join(f\'\'\'
                    <div class="flex gap-3 p-3 bg-gray-50 rounded-lg">
                        <img src="{fp.get("image", "")}" alt="{fp.get("name", "")}" class="w-20 h-20 object-cover rounded-lg">
                        <div>
                            <p class="font-semibold text-sm">{fp.get("name", "")}</p>
                            <p class="text-xs text-gray-600 mt-1">{fp.get("description", "")}</p>
                        </div>
                    </div>
                    \'\'\' for fp in company.get("featured_products", []))}
                </div>
            </div>
            \'\'\' if company.get("featured_products") else \'\'\'}
            {f\'<a href="{company["website"]}" target="_blank" class="inline-flex items-center text-blue-600 hover:text-blue-800 mt-2"><i class="fas fa-external-link-alt mr-1"></i> 访问官网</a>\' if company.get("website") else \'\'}
        </div>
        \'\'\'\n        
        terminal_html'''

new_domestic_detail = '''        # 构建详情链接HTML
        detail_links = company.get("detail_links", {})
        detail_links_html = ""
        if detail_links:
            links_items = []
            for link_name, link_url in detail_links.items():
                links_items.append(f\'<a href="{link_url}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full text-sm hover:bg-blue-100 transition mr-2 mb-2"><i class="fas fa-external-link-alt mr-1.5 text-xs"></i>{link_name}</a>\')
            detail_links_html = f\'\'<div class="mt-4 pt-4 border-t border-gray-200"><p class="text-sm font-semibold text-gray-700 mb-2">🔍 深入了解:</p><div class="flex flex-wrap">{"".join(links_items)}</div></div>\'\'
        
        detail_content = f\'\'\'
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
                    {\'\'\'.join(f\'\'<span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">{p}</span>\'\' for p in company.get("products", []))}
                </div>
            </div>
            {f\'\'\'
            <div>
                <p class="font-semibold mb-3">代表产品:</p>
                <div class="grid grid-cols-1 gap-3">
                    {\'\'\'.join(f\'\'\'
                    <div class="flex gap-3 p-3 bg-gray-50 rounded-lg">
                        <img src="{fp.get("image", "")}" alt="{fp.get("name", "")}" class="w-20 h-20 object-cover rounded-lg">
                        <div>
                            <p class="font-semibold text-sm">{fp.get("name", "")}</p>
                            <p class="text-xs text-gray-600 mt-1">{fp.get("description", "")}</p>
                        </div>
                    </div>
                    \'\'\' for fp in company.get("featured_products", []))}
                </div>
            </div>
            \'\'\' if company.get("featured_products") else \'\'\'}
            {detail_links_html}
        </div>
        \'\'\'\n        
        terminal_html'''

# 替换国内厂商的 detail_content
content = content.replace(old_domestic_detail, new_domestic_detail)

# 2. 修改国际厂商的 detail_content，添加详情链接
old_intl_detail = '''        detail_content = f\'\'\'
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
                    {\'\'\'.join(f\'\'<span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">{p}</span>\'\' for p in company.get("products", []))}
                </div>
            </div>
            {f\'<a href="{company["website"]}" target="_blank" class="inline-flex items-center text-blue-600 hover:text-blue-800 mt-2"><i class="fas fa-external-link-alt mr-1"></i> 访问官网</a>\' if company.get("website") else \'\'}
        </div>
        \'\'\'\n        
        terminal_html.append(f\'\'\'         <div'''

new_intl_detail = '''        # 构建国际厂商详情链接HTML
        detail_links_intl = company.get("detail_links", {})
        detail_links_intl_html = ""
        if detail_links_intl:
            links_items_intl = []
            for link_name, link_url in detail_links_intl.items():
                links_items_intl.append(f\'<a href="{link_url}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full text-sm hover:bg-blue-100 transition mr-2 mb-2"><i class="fas fa-external-link-alt mr-1.5 text-xs"></i>{link_name}</a>\')
            detail_links_intl_html = f\'\'<div class="mt-4 pt-4 border-t border-gray-200"><p class="text-sm font-semibold text-gray-700 mb-2">🔍 Learn More:</p><div class="flex flex-wrap">{"".join(links_items_intl)}</div></div>\'\'
        
        detail_content = f\'\'\'
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
                    {\'\'\'.join(f\'\'<span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">{p}</span>\'\' for p in company.get("products", []))}
                </div>
            </div>
            {detail_links_intl_html}
        </div>
        \'\'\'\n        
        terminal_html.append(f\'\'\'         <div'''

# 替换国际厂商的 detail_content
content = content.replace(old_intl_detail, new_intl_detail)

# 保存修改后的文件
with open('/root/.openclaw/workspace/satcom-research-github/scripts/generate_report.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ generate_report.py 已更新，添加了详情链接展示功能")
