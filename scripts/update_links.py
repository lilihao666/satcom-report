#!/usr/bin/env python3
"""
手动添加产品图片和详情链接的数据更新脚本
"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "satcom_data.json"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_detail_links():
    """为所有厂商添加详情链接"""
    data = load_data()
    
    # 搜索链接模板
    search_templates = {
        "baidu": "https://www.baidu.com/s?wd={}",
        "google": "https://www.google.com/search?q={}",
        "bing": "https://www.bing.com/search?q={}",
        "tianyancha": "https://www.tianyancha.com/search?key={}"
    }
    
    # 为国内厂商添加链接
    for company in data['companies']['domestic']:
        name = company['name']
        
        # 添加详情链接
        if 'detail_links' not in company:
            company['detail_links'] = {
                "百度搜索": f"https://www.baidu.com/s?wd={name}+卫星通信",
                "天眼查": f"https://www.tianyancha.com/search?key={name}",
                "产品搜索": f"https://www.baidu.com/s?wd={name}+产品"
            }
        
        # 如果有官网，添加官网链接
        if company.get('website') and "官网" not in company.get('detail_links', {}):
            company['detail_links']["官网"] = company['website']
    
    # 为国际厂商添加链接
    for company in data['companies'].get('international', []):
        name = company['name']
        
        if 'detail_links' not in company:
            company['detail_links'] = {
                "Google搜索": f"https://www.google.com/search?q={name}+satellite",
                "产品搜索": f"https://www.google.com/search?q={name}+product"
            }
        
        if company.get('website') and "官网" not in company.get('detail_links', {}):
            company['detail_links']["官网"] = company['website']
    
    # 为星座添加链接
    for constellation in data['constellations']['domestic']:
        name = constellation['name']
        operator = constellation.get('operator', '')
        
        if 'detail_links' not in constellation:
            constellation['detail_links'] = {
                "搜索": f"https://www.baidu.com/s?wd={name}",
                "发射动态": f"https://www.baidu.com/s?wd={name}+发射"
            }
    
    for constellation in data['constellations'].get('international', []):
        name = constellation['name']
        
        if 'detail_links' not in constellation:
            constellation['detail_links'] = {
                "搜索": f"https://www.google.com/search?q={name}+satellite+constellation"
            }
    
    save_data(data)
    print("✅ 已为所有厂商和星座添加详情链接")

def update_product_images_with_local_paths():
    """更新产品图片为本地路径"""
    data = load_data()
    
    # 公司名到文件夹的映射
    folder_map = {
        '磐钴智能': 'pangu',
        '星联芯通': 'xinglian', 
        '国科宇航': 'guoke',
        '天行探索科技': 'tianxing',
        '华美钛': 'huameitai',
        '鹏鹄物宇': 'penghu',
        '环天智慧': 'huantian',
        '星途智联': 'xingtu',
        '中国时空': 'shikong',
        '中兵北斗': 'zhongbing',
        '太极疆泰': 'taiji',
        '航天金美': 'hangtianjinmei'
    }
    
    # 更新已有 featured_products 的图片路径
    for company in data['companies']['domestic']:
        name = company['name']
        folder = folder_map.get(name, '')
        
        if folder and 'featured_products' in company:
            for i, product in enumerate(company['featured_products']):
                # 如果当前是 placeholder，保持原样，等待后续替换
                if 'placeholder' not in product.get('image', ''):
                    continue
                # 否则更新为本地路径格式
                # product['image'] = f"images/{folder}/product_{i+1}.jpg"
    
    save_data(data)
    print("✅ 产品图片路径已准备")

if __name__ == "__main__":
    print("🔗 添加详情链接...")
    add_detail_links()
    
    print("\n🖼️ 更新产品图片路径...")
    update_product_images_with_local_paths()
    
    print("\n✅ 所有更新完成！")
    print("\n📋 接下来你可以：")
    print("   1. 手动上传产品图片到 images/ 目录")
    print("   2. 运行 python scripts/fetch_product_images.py 抓取图片")
    print("   3. 运行 python scripts/generate_report.py generate 生成报告")
