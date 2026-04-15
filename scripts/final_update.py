#!/usr/bin/env python3
"""
更新卫星通信数据 - 添加蓝凌星通、南京控维通信、分类字段
"""
import json
from pathlib import Path

DATA_FILE = Path("/root/.openclaw/workspace/satcom-research-github/data/satcom_data.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def classify_constellation(use_cases):
    """根据use_cases分类星座"""
    internet_keywords = ["宽带互联网", "宽带", "手机直连", "互联网", "宽带通信", "D2D", "企业宽带", "云服务", "全球通信", "5G-IoT"]
    iot_keywords = ["物联网", "数据采集", "遥感", "行业应用", "应急通信", "导航", "定位", "语音数据"]
    
    for use in use_cases:
        for keyword in internet_keywords:
            if keyword in use:
                return "卫星互联网"
    return "卫星物联网"

def classify_company(focus):
    """根据focus分类终端厂商"""
    iot_keywords = ["物联网", "模组", "芯片", "窄带", "IoT", "数据采集", "LoRa"]
    internet_keywords = ["互联网", "宽带", "相控阵", "VSAT", "动中通", "平板天线", "卫星通信终端", "终端设备"]
    
    focus_lower = focus.lower()
    for keyword in iot_keywords:
        if keyword in focus_lower:
            return "卫星物联网终端"
    for keyword in internet_keywords:
        if keyword in focus_lower:
            return "卫星互联网终端"
    return "卫星物联网终端"  # 默认分类

def main():
    data = load_data()
    
    # 1. 为国内星座添加分类
    print("为国内星座添加分类...")
    for c in data['constellations']['domestic']:
        c['category'] = classify_constellation(c.get('use_cases', []))
        print(f"  {c['name']}: {c['category']}")
    
    # 2. 为国际星座添加分类
    print("\n为国际星座添加分类...")
    for c in data['constellations']['international']:
        c['category'] = classify_constellation(c.get('use_cases', []))
        print(f"  {c['name']}: {c['category']}")
    
    # 3. 为国内GEO星座添加分类
    print("\n为GEO星座添加分类...")
    for c in data['constellations'].get('geo_domestic', []):
        c['category'] = "卫星互联网"  # GEO主要用于宽带
        print(f"  {c['name']}: {c['category']}")
    for c in data['constellations'].get('geo_international', []):
        c['category'] = "卫星互联网"
        print(f"  {c['name']}: {c['category']}")
    
    # 4. 为国内终端厂商添加分类
    print("\n为国内终端厂商添加分类...")
    for c in data['companies']['domestic']:
        c['category'] = classify_company(c.get('focus', ''))
        print(f"  {c['name']}: {c['category']}")
    
    # 5. 为国际终端厂商添加分类
    print("\n为国际终端厂商添加分类...")
    for c in data['companies']['international']:
        c['category'] = classify_company(c.get('focus', ''))
        print(f"  {c['name']}: {c['category']}")
    
    # 6. 添加蓝凌星通星座
    print("\n添加蓝凌星通星座...")
    lanling = {
        "name": "蓝凌星通",
        "operator": "蓝凌星通",
        "planned": 12,
        "launched": 0,
        "stage": "规划中",
        "use_cases": ["物联网", "数据采集", "行业应用"],
        "category": "卫星物联网",
        "inter_satellite_link": {"enabled": False, "tech": "无", "note": "规划中"},
        "detail_links": {
            "搜索": "https://www.baidu.com/s?wd=蓝凌星通",
            "发射动态": "https://www.baidu.com/s?wd=蓝凌星通+发射"
        }
    }
    # 检查是否已存在
    exists = any(c['name'] == '蓝凌星通' for c in data['constellations']['domestic'])
    if not exists:
        data['constellations']['domestic'].append(lanling)
        print("  ✓ 已添加蓝凌星通")
    else:
        print("  蓝凌星通已存在，跳过")
    
    # 7. 添加南京控维通信
    print("\n添加南京控维通信...")
    kongwei = {
        "name": "南京控维通信",
        "city": "南京",
        "focus": "卫星互联网终端",
        "tech": "VSAT/卫星通信",
        "category": "卫星互联网终端",
        "founded": "2018",
        "funding": "B轮",
        "products": ["VSAT终端", "卫星调制解调器", "动中通"],
        "description": "卫星通信VSAT终端和系统集成解决方案提供商",
        "website": "http://www.ctrlsky.com",
        "detail_links": {
            "百度搜索": "https://www.baidu.com/s?wd=南京控维通信",
            "天眼查": "https://www.tianyancha.com/search?key=南京控维通信",
            "产品搜索": "https://www.baidu.com/s?wd=南京控维通信+产品",
            "官网": "http://www.ctrlsky.com"
        }
    }
    # 检查是否已存在
    exists = any(c['name'] == '南京控维通信' for c in data['companies']['domestic'])
    if not exists:
        data['companies']['domestic'].append(kongwei)
        print("  ✓ 已添加南京控维通信")
    else:
        print("  南京控维通信已存在，跳过")
    
    # 8. 为新闻添加URL字段
    print("\n为新闻添加URL...")
    news_urls = {
        "SpaceX官方": "https://www.spacex.com",
        "华为官方": "https://www.huawei.com",
        "时空道宇": "https://www.geespace.com",
        "FCC": "https://www.fcc.gov",
        "浙江日报": "https://www.zjnews.cn",
        "AST SpaceMobile": "https://www.ast-science.com",
        "中国航天报": "https://www.spacechina.com",
        "欧盟委员会": "https://commission.europa.eu",
        "中国星网": "https://www.chinasatnet.com",
        "SoftBank": "https://group.softbank",
        "界面新闻/新浪财经": "https://www.jiemian.com",
        "C114通信网": "https://www.c114.com.cn",
        "财新网": "https://www.caixin.com",
        "财经报纸": "",
        "国际电信联盟": "https://www.itu.int",
        "北京日报": "https://www.bjd.com.cn",
        "极光星通": "https://www.jiguangxingtong.com",
        "证券时报": "https://www.stcn.com",
        "C114年终盘点": "https://www.c114.com.cn",
        "国电高科": "https://www.guodiankeji.com"
    }
    
    for news in data.get('news', []):
        source = news.get('source', '')
        if source in news_urls and not news.get('url'):
            news['url'] = news_urls[source]
    print("  ✓ 已为新闻添加URL")
    
    # 9. 修复官网链接
    print("\n修复官网链接...")
    website_fixes = {
        "磐钴智能": "https://www.pangusat.com",
        "星联芯通": "https://www.satcomtec.com",
        "国科宇航": "https://www.guokespace.com",
        "南京控维通信": "http://www.ctrlsky.com"
    }
    for company in data['companies']['domestic']:
        name = company['name']
        if name in website_fixes:
            company['website'] = website_fixes[name]
            if 'detail_links' in company:
                company['detail_links']['官网'] = website_fixes[name]
            print(f"  ✓ 修复 {name} 官网链接")
    
    # 保存数据
    save_data(data)
    print("\n✅ 所有更新已完成！")
    
    # 统计
    print("\n📊 数据统计:")
    print(f"  国内星座: {len(data['constellations']['domestic'])} 个")
    print(f"  国际星座: {len(data['constellations']['international'])} 个")
    print(f"  国内厂商: {len(data['companies']['domestic'])} 个")
    print(f"  国际厂商: {len(data['companies']['international'])} 个")
    print(f"  最新动态: {len(data.get('news', []))} 条")

if __name__ == "__main__":
    main()
