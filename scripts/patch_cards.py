#!/usr/bin/env python3
"""
修改报告生成脚本 - 添加分类标签显示
"""
import re
from pathlib import Path

SCRIPT_FILE = Path("/root/.openclaw/workspace/satcom-research-github/scripts/generate_report.py")

def read_script():
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_script(content):
    with open(SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    content = read_script()
    
    # 1. 修改国内厂商卡片 - 添加分类标签
    old_domestic_card = '''terminal_html.append(f\'\'\'
        <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative"  onclick="openModal(\'{escape_js(company["name"])}\', \'{escape_js(detail_content)}\')">
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
                    {\'\'\'.join(f\'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{p}</span>\' for p in company.get("products", [])[:3])}
                    {f\'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 3}</span>\' if len(company.get("products", [])) > 3 else \'\'\'}
                </div>
            </div>
        </div>
        \'\'\')'''
    
    new_domestic_card = '''# 分类标签颜色
        cat = company.get("category", "卫星物联网终端")
        cat_color = "purple" if "互联网" in cat else "orange"
        
        terminal_html.append(f\'\'\'
        <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative"  onclick="openModal(\'{escape_js(company["name"])}\', \'{escape_js(detail_content)}\')">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-bold">{company["name"]}</h3>
                    <span class="text-xs bg-{cat_color}-100 text-{cat_color}-700 px-2 py-0.5 rounded mt-1 inline-block">{cat}</span>
                </div>
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
                    {\'\'\'.join(f\'<span class="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{p}</span>\' for p in company.get("products", [])[:3])}
                    {f\'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 3}</span>\' if len(company.get("products", [])) > 3 else \'\'\'}
                </div>
            </div>
        </div>
        \'\'\')'''
    
    # 2. 修改国际厂商卡片
    old_intl_card = '''terminal_html.append(f\'\'\'         <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal(\'{escape_js(company["name"])}\', \'{escape_js(detail_content)}\')">
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
                    {\'\'\'.join(f\'<span class="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded">{p}</span>\' for p in company.get("products", [])[:2])}
                    {f\'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 2}</span>\' if len(company.get("products", [])) > 2 else \'\'\'}
                </div>
            </div>
        </div>
        \'\'\')'''
    
    new_intl_card = '''# 分类标签颜色
        cat = company.get("category", "卫星物联网终端")
        cat_color = "purple" if "互联网" in cat else "orange"
        
        terminal_html.append(f\'\'\'         <div class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition clickable-card relative" onclick="openModal(\'{escape_js(company["name"])}\', \'{escape_js(detail_content)}\')">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-bold">{company["name"]}</h3>
                    <span class="text-xs bg-{cat_color}-100 text-{cat_color}-700 px-2 py-0.5 rounded mt-1 inline-block">{cat}</span>
                </div>
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
                    {\'\'\'.join(f\'<span class="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded">{p}</span>\' for p in company.get("products", [])[:2])}
                    {f\'<span class="bg-gray-50 text-gray-400 text-xs px-2 py-0.5 rounded">+{len(company.get("products", [])) - 2}</span>\' if len(company.get("products", [])) > 2 else \'\'\'}
                </div>
            </div>
        </div>
        \'\'\')'''
    
    if old_domestic_card in content:
        content = content.replace(old_domestic_card, new_domestic_card)
        print("✓ 已更新国内厂商卡片")
    else:
        print("✗ 未找到国内厂商卡片代码")
    
    if old_intl_card in content:
        content = content.replace(old_intl_card, new_intl_card)
        print("✓ 已更新国际厂商卡片")
    else:
        print("✗ 未找到国际厂商卡片代码")
    
    write_script(content)
    print("\n✅ 脚本已更新")

if __name__ == "__main__":
    main()
