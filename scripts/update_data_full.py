#!/usr/bin/env python3
"""
更新卫星通信数据
添加新厂商、星座，增加分类字段
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

def add_blue_ling_constellation(data):
    """添加蓝凌星通星座"""
    blue_ling = {
        "name": "蓝凌星通",
        "operator": "蓝凌星通",
        "planned": 12,
        "launched": 0,
        "stage": "规划中",
        "use_cases": ["物联网", "数据采集", "行业应用"],
        "category": "卫星物联网",
        "inter_satellite_link": {
            "enabled": False,
            "tech": "无",
            "note": "规划中"
        },
        "detail_links": {
            "搜索": "https://www.baidu.com/s?wd=蓝凌星通",
            "发射动态": "https://www.baidu.com/s?wd=蓝凌星通+发射"
        }
    }
    
    # 检查是否已存在
    exists = any(c['name'] == '蓝凌星通' for c in data['constellations']['domestic'])
    if not exists:
        data['constellations']['domestic'].append(blue_ling)
        print("✅ 已添加蓝凌星通星座")
    else:
        print("ℹ️ 蓝凌星通星座已存在")

def add_nanjing_ctrlway(data):
    """添加南京控维通信"""
    ctrlway = {
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
            "百度搜索": "https://www.baidu.com/s?wd=南京控维通信+卫星通信",
            "天眼查": "https://www.tianyancha.com/search?key=南京控维通信",
            "产品搜索": "https://www.baidu.com/s?wd=南京控维通信+产品",
            "官网": "http://www.ctrlsky.com"
        }
    }
    
    exists = any(c['name'] == '南京控维通信' for c in data['companies']['domestic'])
    if not exists:
        data['companies']['domestic'].append(ctrlway)
        print("✅ 已添加南京控维通信")
    else:
        print("ℹ️ 南京控维通信已存在")

def classify_constellations(data):
    """为星座添加分类"""
    for c in data['constellations']['domestic']:
        if 'category' not in c:
            use_cases = [uc.lower() for uc in c.get('use_cases', [])]
            # 判断是否卫星互联网
            internet_keywords = ['宽带', '互联网', '宽带互联网', '手机直连', '宽带通信']
            iot_keywords = ['物联网', '数据采集', '遥感', '导航', '应急通信']
            
            is_internet = any(kw in uc for kw in internet_keywords for uc in use_cases)
            is_iot = any(kw in uc for kw in iot_keywords for uc in use_cases)
            
            if is_internet:
                c['category'] = '卫星互联网'
            elif is_iot:
                c['category'] = '卫星物联网'
            else:
                c['category'] = '综合应用'
    
    for c in data['constellations'].get('international', []):
        if 'category' not in c:
            use_cases = [uc.lower() for uc in c.get('use_cases', [])]
            internet_keywords = ['broadband', 'internet', 'mobile', 'phone']
            iot_keywords = ['iot', 'm2m', 'narrowband', 'machine']
            
            is_internet = any(kw in uc.lower() for kw in internet_keywords for uc in use_cases)
            is_iot = any(kw in uc.lower() for kw in iot_keywords for uc in use_cases)
            
            if is_internet:
                c['category'] = '卫星互联网'
            elif is_iot:
                c['category'] = '卫星物联网'
            else:
                c['category'] = '综合应用'
    
    print("✅ 星座分类完成")

def classify_companies(data):
    """为终端厂商添加分类"""
    for c in data['companies']['domestic']:
        if 'category' not in c:
            focus = c.get('focus', '').lower()
            iot_keywords = ['物联网', '模组', '窄带', 'lora', 'iot']
            internet_keywords = ['互联网', '宽带', '相控阵', 'vsat', '动中通']
            
            is_iot = any(kw in focus for kw in iot_keywords)
            is_internet = any(kw in focus for kw in internet_keywords)
            
            if is_iot:
                c['category'] = '卫星物联网终端'
            elif is_internet:
                c['category'] = '卫星互联网终端'
            else:
                c['category'] = '综合终端'
    
    for c in data['companies'].get('international', []):
        if 'category' not in c:
            focus = c.get('focus', '').lower()
            iot_keywords = ['iot', 'm2m', 'modem', 'module']
            internet_keywords = ['broadband', 'vsat', 'terminal', 'antenna']
            
            is_iot = any(kw in focus for kw in iot_keywords)
            is_internet = any(kw in focus for kw in internet_keywords)
            
            if is_iot:
                c['category'] = '卫星物联网终端'
            elif is_internet:
                c['category'] = '卫星互联网终端'
            else:
                c['category'] = '综合终端'
    
    print("✅ 终端厂商分类完成")

def add_news_urls(data):
    """为新闻添加来源链接"""
    source_urls = {
        "SpaceX官方": "https://www.spacex.com",
        "华为官方": "https://www.huawei.com",
        "时空道宇": "https://www.geespace.com",
        "FCC": "https://www.fcc.gov",
        "浙江日报": "http://www.zjnews.cn",
        "AST SpaceMobile": "https://www.ast-science.com",
        "中国航天报": "http://www.spacechina.com",
        "欧盟委员会": "https://ec.europa.eu",
        "中国星网": "http://www.chinasatnet.com",
        "SoftBank": "https://www.softbank.jp",
        "界面新闻/新浪财经": "https://www.jiemian.com",
        "C114通信网": "https://www.c114.com.cn",
        "财新网": "https://www.caixin.com",
        "财经报纸": "https://www.caijing.com.cn",
        "国际电信联盟": "https://www.itu.int",
        "北京日报": "https://www.bjd.com.cn",
        "极光星通": "http://www.jlxt.com",
        "证券时报": "http://www.stcn.com",
        "国电高科": "http://www.chinasatcom.com",
    }
    
    for news in data.get('news', []):
        if 'url' not in news:
            source = news.get('source', '')
            if source in source_urls:
                news['url'] = source_urls[source]
            else:
                # 使用搜索链接
                title = news.get('title', '')
                news['url'] = f"https://www.baidu.com/s?wd={title[:30]}"
    
    print("✅ 新闻来源链接已添加")

def main():
    print("🛰️ 更新卫星通信数据")
    print("=" * 50)
    
    data = load_data()
    
    add_blue_ling_constellation(data)
    add_nanjing_ctrlway(data)
    classify_constellations(data)
    classify_companies(data)
    add_news_urls(data)
    
    save_data(data)
    print("\n" + "=" * 50)
    print("✅ 所有更新已完成！")

if __name__ == "__main__":
    main()
