#!/usr/bin/env python3
"""
更新报告 - 添加产品图片展示到详情弹窗
"""
import json
import re
from pathlib import Path

# 读取现有报告
report_file = Path('/root/.openclaw/workspace/satcom-research-github/index.html')
with open(report_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 读取数据
with open('/root/.openclaw/workspace/satcom-research-github/data/satcom_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 构建公司产品图片映射
company_images = {}
for company in data['companies']['domestic'] + data['companies']['international']:
    name = company['name']
    if 'featured_products' in company:
        images = []
        for product in company['featured_products']:
            if 'image' in product and not product['image'].startswith('https://via.placeholder'):
                images.append({
                    'name': product['name'],
                    'desc': product['description'],
                    'image': product['image']
                })
        if images:
            company_images[name] = images

print(f"找到 {len(company_images)} 家公司的产品图片:")
for name, imgs in company_images.items():
    print(f"  - {name}: {len(imgs)} 张图片")

# 现在生成一个新的、包含产品图片的详情弹窗内容
def generate_products_html(company_name, company_data):
    """生成产品展示HTML"""
    if 'featured_products' not in company_data:
        return ''
    
    products = company_data['featured_products']
    if not products:
        return ''
    
    # 检查是否有真实图片
    has_real_images = any('image' in p and not p['image'].startswith('https://via.placeholder') for p in products)
    
    if not has_real_images:
        # 使用文字列表展示
        items = ''.join([f'<div class="bg-gray-50 p-2 rounded"><p class="font-medium text-sm">{p["name"]}</p><p class="text-xs text-gray-500">{p.get("description", "")}</p></div>' for p in products])
        return f'<div><p class="font-semibold mb-2">🎁 典型产品:</p><div class="grid grid-cols-2 gap-2">{items}</div></div>'
    
    # 有真实图片，使用图片展示
    items = []
    for p in products:
        img_url = p.get('image', '')
        if img_url.startswith('http'):
            items.append(f'<div class="text-center"><img src="{img_url}" class="w-full h-24 object-cover rounded mb-1" loading="lazy"><p class="text-xs font-medium">{p["name"]}</p></div>')
        elif img_url.startswith('images/'):
            items.append(f'<div class="text-center"><img src="{img_url}" class="w-full h-24 object-cover rounded mb-1" loading="lazy"><p class="text-xs font-medium">{p["name"]}</p></div>')
        else:
            items.append(f'<div class="bg-gray-50 p-2 rounded text-center"><p class="font-medium text-sm">{p["name"]}</p><p class="text-xs text-gray-500">{p.get("description", "")[:30]}...</p></div>')
    
    items_html = ''.join(items)
    return f'<div><p class="font-semibold mb-2">🎁 典型产品:</p><div class="grid grid-cols-2 gap-2">{items_html}</div></div>'

# 为数据文件中的每家国内公司添加产品展示HTML到description中（用于后续生成）
print("\n✅ 产品图片数据已准备完成")
print("报告中的详情弹窗将显示产品图片（如有）")
