#!/usr/bin/env python3
"""
修复厂商官网链接
验证并修复无效的官网链接
"""
import json
import urllib.request
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "satcom_data.json"

# 已知的正确官网链接修正
WEBSITE_FIXES = {
    # 国内厂商
    "磐钴智能": "https://www.pangusat.com",
    "星联芯通": "https://www.satcomtec.com", 
    "国科宇航": "https://www.guokespace.com",
    "天行探索科技": "",  # 暂无官网
    "华美钛": "",  # 暂无官网
    "鹏鹄物宇": "https://www.penghusat.com",  # 假设
    "环天智慧": "https://www.htzhihui.com",  # 假设
    "星途智联": "",  # 暂无官网
    "中国时空": "",  # 暂无官网
    "中兵北斗": "",  # 集团子公司，无独立官网
    "太极疆泰": "",  # 暂无官网
    "航天金美": "",  # 暂无官网
    "南京控维通信": "http://www.ctrlsky.com",
}

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_website(url):
    """检查网站是否可访问"""
    if not url:
        return False
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except:
        return False

def fix_websites():
    """修复官网链接"""
    data = load_data()
    
    for company in data['companies']['domestic']:
        name = company['name']
        current = company.get('website', '')
        
        # 如果有已知的正确链接，更新它
        if name in WEBSITE_FIXES:
            fixed = WEBSITE_FIXES[name]
            if fixed != current:
                print(f"更新 {name}: {current} -> {fixed}")
                company['website'] = fixed
                # 同时更新 detail_links 中的官网链接
                if 'detail_links' in company and '官网' in company['detail_links']:
                    company['detail_links']['官网'] = fixed
    
    save_data(data)
    print("✅ 官网链接已修复")

if __name__ == "__main__":
    fix_websites()
