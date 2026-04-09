#!/usr/bin/env python3
"""
卫星通信行业新闻抓取器
每天自动抓取最新行业动态
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("需要安装依赖: pip install requests beautifulsoup4")
    exit(1)

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "satcom_data.json"

def load_data():
    """加载现有数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    """保存数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_news():
    """抓取新闻（使用搜索API模拟）"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 这里可以接入真实的搜索API
    # 目前使用模拟数据展示结构
    mock_news = [
        {
            "title": f"千帆星座新一轮组网卫星成功发射 ({today})",
            "summary": "垣信卫星成功发射18颗千帆星座卫星，组网进度持续推进。",
            "date": today,
            "source": "新华社",
            "tags": ["千帆星座", "发射"],
            "impact_analysis": {"level": "high", "areas": ["星座部署"]},
            "url": "https://example.com/news1"
        },
        {
            "title": f"某卫星通信终端厂商获得新一轮融资 ({today})",
            "summary": "国内某卫星物联网终端企业完成亿元级B轮融资。",
            "date": today,
            "source": "36氪",
            "tags": ["融资", "物联网"],
            "impact_analysis": {"level": "medium", "areas": ["资本市场"]},
            "url": "https://example.com/news2"
        }
    ]
    
    return mock_news

def update_news():
    """更新新闻数据"""
    data = load_data()
    new_news = fetch_news()
    
    # 合并新闻（去重）
    existing_titles = {n["title"] for n in data.get("news", [])}
    for news in new_news:
        if news["title"] not in existing_titles:
            data.setdefault("news", []).insert(0, news)
    
    # 只保留最近30天的新闻
    data["news"] = data["news"][:30]
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_data(data)
    print(f"✅ 新闻更新完成，共 {len(data['news'])} 条")

if __name__ == "__main__":
    update_news()
