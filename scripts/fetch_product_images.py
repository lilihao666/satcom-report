#!/usr/bin/env python3
"""
卫星通信厂商产品图片抓取器
从厂商官网抓取产品图片
"""
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("需要安装依赖: pip install beautifulsoup4")
    exit(1)

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
                print(f"✅ 下载成功: {save_path.name}")
                return True
    except Exception as e:
        print(f"❌ 下载失败: {url} - {e}")
    return False

def fetch_webpage(url):
    """获取网页内容"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"❌ 获取页面失败: {url} - {e}")
    return None

def extract_product_images(html, base_url, company_name):
    """从产品页面提取图片"""
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    
    # 1. 查找产品相关的图片
    # 常见的产品图片选择器
    selectors = [
        'img[src*="product"]', 'img[src*="Product"]', 
        '.product img', '.product-item img',
        '.solution img', '.device img',
        'img[src*="device"]', 'img[src*="terminal"]',
        'img[src*="module"]', 'img[src*="chip"]'
    ]
    
    for selector in selectors:
        for img in soup.select(selector):
            src = img.get('src') or img.get('data-src')
            if src:
                full_url = urljoin(base_url, src)
                alt = img.get('alt', '')
                images.append({
                    'url': full_url,
                    'alt': alt,
                    'type': 'product'
                })
    
    # 2. 查找所有图片，过滤出可能的产品的
    if not images:
        all_imgs = soup.find_all('img')
        for img in all_imgs:
            src = img.get('src') or img.get('data-src')
            if src and not any(x in src.lower() for x in ['logo', 'icon', 'banner', 'bg', 'background']):
                full_url = urljoin(base_url, src)
                if full_url.startswith('http'):
                    images.append({
                        'url': full_url,
                        'alt': img.get('alt', ''),
                        'type': 'general'
                    })
    
    # 去重
    seen = set()
    unique = []
    for img in images:
        if img['url'] not in seen:
            seen.add(img['url'])
            unique.append(img)
    
    return unique[:3]  # 最多返回3张

def get_company_folder_name(company_name):
    """生成公司文件夹名"""
    # 拼音映射
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
        '航天金美': 'hangtianjinmei'
    }
    return pinyin_map.get(company_name, company_name.lower().replace(' ', '_'))

def process_company(company, is_domestic=True):
    """处理单个厂商"""
    name = company['name']
    website = company.get('website', '')
    folder = get_company_folder_name(name)
    company_img_dir = IMAGES_DIR / folder
    
    print(f"\n📦 处理: {name}")
    print(f"   官网: {website or '无'}")
    
    # 检查是否已有 featured_products
    featured = company.get('featured_products', [])
    
    # 如果有官网，尝试抓取产品图片
    if website and not featured:
        print(f"   正在抓取产品图片...")
        html = fetch_webpage(website)
        if html:
            images = extract_product_images(html, website, name)
            if images:
                print(f"   找到 {len(images)} 张图片")
                new_products = []
                for i, img_info in enumerate(images, 1):
                    ext = Path(urlparse(img_info['url']).path).suffix or '.jpg'
                    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                        ext = '.jpg'
                    
                    filename = f"product_{i}{ext}"
                    save_path = company_img_dir / filename
                    
                    if download_image(img_info['url'], save_path):
                        new_products.append({
                            "name": img_info['alt'] or f"产品 {i}",
                            "description": f"{name} 产品",
                            "image": f"images/{folder}/{filename}"
                        })
                
                if new_products:
                    company['featured_products'] = new_products
                    print(f"   ✅ 已添加 {len(new_products)} 个产品")
            else:
                print(f"   ⚠️ 未找到产品图片")
    
    # 如果已有 featured_products 但图片是 placeholder，尝试更新
    elif featured:
        print(f"   已有 {len(featured)} 个产品")
        for i, product in enumerate(featured):
            img_url = product.get('image', '')
            if 'placeholder' in img_url or not img_url.startswith('images/'):
                if website:
                    print(f"   尝试抓取产品 {i+1} 的真实图片...")
                    # 简化处理：先用占位图逻辑
                    pass
    
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

if __name__ == "__main__":
    main()
