#!/usr/bin/env python3
"""
验证所有官网链接，找出有问题的
"""
import json
import requests
from pathlib import Path

def load_data():
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def check_url(url, name, context):
    """检查URL是否可访问"""
    if not url or url == "#":
        return False, "空链接"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            return True, f"OK ({response.status_code})"
        elif response.status_code in [301, 302, 307, 308]:
            return True, f"重定向 ({response.status_code})"
        else:
            return False, f"错误 ({response.status_code})"
    except requests.exceptions.Timeout:
        return False, "超时"
    except requests.exceptions.ConnectionError:
        return False, "连接错误"
    except Exception as e:
        return False, str(e)[:30]

def main():
    data = load_data()
    
    print("🔍 验证官网链接...\n")
    
    # 验证国际星座
    print("📡 国际星座:")
    for c in data["constellations"]["international"]:
        name = c["name"]
        links = c.get("detail_links", {})
        if "官网" in links:
            url = links["官网"]
            ok, status = check_url(url, name, "星座")
            status_icon = "✅" if ok else "❌"
            print(f"  {status_icon} {name}: {url} -> {status}")
    
    # 验证国内厂商
    print("\n🏭 国内终端厂商:")
    for c in data["companies"]["domestic"]:
        name = c["name"]
        url = c.get("website", "")
        if url:
            ok, status = check_url(url, name, "终端")
            status_icon = "✅" if ok else "❌"
            print(f"  {status_icon} {name}: {url} -> {status}")
        else:
            print(f"  ⚠️  {name}: 无官网")
    
    # 验证国际厂商
    print("\n🌍 国际终端厂商:")
    for c in data["companies"]["international"]:
        name = c["name"]
        url = c.get("website", "")
        links = c.get("detail_links", {})
        
        if url:
            ok, status = check_url(url, name, "国际终端")
            status_icon = "✅" if ok else "❌"
            print(f"  {status_icon} {name}: {url} -> {status}")
        elif "官网" in links:
            url = links["官网"]
            ok, status = check_url(url, name, "国际终端")
            status_icon = "✅" if ok else "❌"
            print(f"  {status_icon} {name}: {url} -> {status}")
        else:
            print(f"  ⚠️  {name}: 无官网")
    
    # 验证载荷厂商
    print("\n🛰️ 国内载荷厂商:")
    for c in data["payloads"]["domestic"]:
        name = c["name"]
        url = c.get("website", "")
        if url:
            ok, status = check_url(url, name, "载荷")
            status_icon = "✅" if ok else "❌"
            print(f"  {status_icon} {name}: {url} -> {status}")
        else:
            print(f"  ⚠️  {name}: 无官网")

if __name__ == "__main__":
    main()
