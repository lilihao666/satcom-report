#!/usr/bin/env python3
"""
修复有问题的官网链接
"""
import json
from pathlib import Path

def load_data():
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = load_data()
    
    # 有问题的链接替换为百度搜索
    bad_websites = {
        # 国际星座
        "Omnispace": "https://www.google.com/search?q=Omnispace+satellite",
        
        # 国内终端厂商
        "磐钴智能": "https://www.baidu.com/s?wd=磐钴智能+卫星通信",
        "星联芯通": "https://www.baidu.com/s?wd=星联芯通+卫星通信",
        "国科宇航": "https://www.baidu.com/s?wd=国科宇航+卫星通信",
        "鹏鹄物宇": "https://www.baidu.com/s?wd=鹏鹄物宇+卫星通信",
        "环天智慧": "https://www.baidu.com/s?wd=环天智慧+卫星",
        
        # 国际终端
        "Hughes Network": "https://www.google.com/search?q=Hughes+Network+satellite",
        
        # 国内载荷厂商  
        "上海瀚讯": "https://www.baidu.com/s?wd=上海瀚讯+卫星通信",
        "极光星通": "https://www.baidu.com/s?wd=极光星通+激光通信",
        "银河航天": "https://www.baidu.com/s?wd=银河航天+卫星",
    }
    
    fix_count = 0
    
    # 修复国内终端厂商
    for c in data["companies"]["domestic"]:
        name = c["name"]
        if name in bad_websites:
            old_url = c.get("website", "")
            c["website"] = bad_websites[name]
            print(f"🔧 修复终端厂商: {name}")
            print(f"   旧: {old_url}")
            print(f"   新: {c['website']}")
            fix_count += 1
    
    # 修复国际终端厂商
    for c in data["companies"]["international"]:
        name = c["name"]
        if name in bad_websites:
            old_url = c.get("website", "")
            c["website"] = bad_websites[name]
            print(f"🔧 修复国际厂商: {name}")
            print(f"   旧: {old_url}")
            print(f"   新: {c['website']}")
            fix_count += 1
    
    # 修复国内载荷厂商
    for c in data["payloads"]["domestic"]:
        name = c["name"]
        if name in bad_websites:
            old_url = c.get("website", "")
            c["website"] = bad_websites[name]
            print(f"🔧 修复载荷厂商: {name}")
            print(f"   旧: {old_url}")
            print(f"   新: {c['website']}")
            fix_count += 1
    
    # 修复Omnispace
    for c in data["constellations"]["international"]:
        if c["name"] == "Omnispace":
            c["detail_links"]["官网"] = bad_websites["Omnispace"]
            print(f"🔧 修复星座: Omnispace")
            fix_count += 1
    
    save_data(data)
    print(f"\n✅ 共修复 {fix_count} 个问题链接")

if __name__ == "__main__":
    main()
