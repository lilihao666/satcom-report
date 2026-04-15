#!/usr/bin/env python3
"""
卫星通信厂商产品图片抓取器 (标准库版本)
从厂商官网抓取产品图片
"""
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urljoin, urlparse

# 项目路径
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "satcom_data.json"
IMAGES_DIR = BASE_DIR / "images"

# 请求头模拟浏览器
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def load_data():
    """加载数据"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def download_image(url, save_path):
    """下载图片到本地"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                data = response.read()
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(data)
                print(f"  ✅ 下载成功: {save_path.name}")
                return True
    except Exception as e:
        print(f"  ❌ 下载失败: {str(e)[:50]}")
    return False

def fetch_webpage(url):
    """获取网页内容"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  ❌ 获取页面失败: {str(e)[:50]}")
    return None

def extract_images_from_html(html, base_url):
    """从HTML中提取图片URL (使用正则，不依赖bs4)"""
    images = []
    
    # 匹配 img 标签的 src 属性
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
    matches = re.findall(img_pattern, html, re.IGNORECASE)
    
    for src in matches:
        # 过滤掉 logo、icon 等小图标
        if any(x in src.lower() for x in ['logo', 'icon', 'bg.', 'banner', 'nav', 'footer']):
            continue
        
        full_url = urljoin(base_url, src)
        if full_url.startswith('http'):
            images.append(full_url)
    
    # 去重
    return list(dict.fromkeys(images))[:5]  # 最多5张

def get_company_folder_name(company_name):
    """生成公司文件夹名"""
    pinyin_map = {
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
        '航天金美': 'hangtianjinmei',
        '南京控维通信': 'ctrlsky'
    }
    return pinyin_map.get(company_name, company_name.lower().replace(' ', '_').replace('/', '_'))

def process_company(company, is_domestic=True):
    """处理单个厂商"""
    name = company['name']
    website = company.get('website', '')
    folder = get_company_folder_name(name)
    company_img_dir = IMAGES_DIR / folder
    
    print(f"\n📦 {name}")
    print(f"   官网: {website or '无'}")
    
    featured = company.get('featured_products', [])
    
    # 如果有官网，尝试抓取产品图片
    if website and not featured:
        print(f"   正在抓取...")
        html = fetch_webpage(website)
        if html:
            images = extract_images_from_html(html, website)
            if images:
                print(f"   找到 {len(images)} 张图片")
                new_products = []
                for i, img_url in enumerate(images, 1):
                    ext = Path(urlparse(img_url).path).suffix or '.jpg'
                    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                        ext = '.jpg'
                    
                    filename = f"product_{i}{ext}"
                    save_path = company_img_dir / filename
                    
                    if download_image(img_url, save_path):
                        new_products.append({
                            "name": f"产品 {i}",
                            "description": f"{name} 产品",
                            "image": f"images/{folder}/{filename}"
                        })
                
                if new_products:
                    company['featured_products'] = new_products
                    print(f"   ✅ 已添加 {len(new_products)} 个产品")
            else:
                print(f"   ⚠️ 未找到图片")
    elif featured:
        print(f"   已有 {len(featured)} 个产品")
    else:
        print(f"   ⚠️ 无官网，跳过")
    
    return company

def main():
    """主函数"""
    print("🛰️ 卫星通信产品图片抓取器")
    print("=" * 50)
    
    data = load_data()
    
    # 处理国内厂商
    print("\n🇨🇳 国内厂商")
    print("-" * 50)
    for i, company in enumerate(data['companies']['domestic']):
        data['companies']['domestic'][i] = process_company(company, True)
    
    # 处理国际厂商
    print("\n🌍 国际厂商")
    print("-" * 50)
    for i, company in enumerate(data['companies'].get('international', [])):
        data['companies']['international'][i] = process_company(company, False)
    
    # 保存更新后的数据
    save_data(data)
    print("\n" + "=" * 50)
    print("✅ 数据已更新")
    print(f"📁 图片目录: {IMAGES_DIR}")
    
    # 统计
    img_count = sum(1 for _ in IMAGES_DIR.rglob('*') if _.is_file())
    print(f"📊 已下载图片: {img_count} 张")

if __name__ == "__main__":
    main()
