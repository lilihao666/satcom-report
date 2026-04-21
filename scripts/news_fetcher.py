#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Satellite Communication News Fetcher
Fetches latest satellite communication news from multiple public sources.
Supports RSS feeds, API endpoints, and manual news injection.
"""

import json
import os
import sys
import re
import argparse
from datetime import datetime, timedelta
from urllib.parse import urljoin

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests not installed. Limited functionality.")

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

# Configuration
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'satcom_data.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'update.log')

# News sources (RSS feeds and APIs)
RSS_SOURCES = [
    {
        "name": "未来天玑",
        "url": "https://www.futurephecda.com/feed",
        "keyword_filter": ["卫星", "星座", "航天", "SpaceX", "星链", "千帆", "天启", "物联网", "通信"]
    },
    {
        "name": "泰伯网",
        "url": "https://www.taibo.cn/feed",
        "keyword_filter": ["卫星", "星座", "航天", "通信", "物联网"]
    },
]

# Fallback: scrape from known news pages
SCRAPE_SOURCES = [
    {
        "name": "未来天玑-卫星通信",
        "url": "https://www.futurephecda.com/news?tags=%E5%8D%AB%E6%98%9F%E9%80%9A%E4%BF%A1",
        "pattern": r'<article[^>]*>.*?<h[23][^>]*>(.*?)</h[23]>.*?<a[^>]*href="([^"]*)".*?<time[^>]*>(.*?)</time>.*?</article>',
        "date_format": "%Y-%m-%d"
    }
]

# Simulated news templates for when no network is available
SIMULATED_NEWS = [
    {
        "date": "2026-04-21",
        "title": "卫星通信行业动态更新",
        "summary": "自动更新系统运行中，请关注实际发射和行业动态。",
        "source": "自动更新系统",
        "link": "",
        "category": "行业动态"
    }
]


def log_message(msg):
    """Write log message to file and stdout"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
    except:
        pass


def fetch_rss_feed(source):
    """Fetch news from RSS feed"""
    if not HAS_REQUESTS:
        return []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(source['url'], headers=headers, timeout=15)
        response.raise_for_status()
        
        if HAS_FEEDPARSER:
            feed = feedparser.parse(response.text)
            news_items = []
            for entry in feed.entries[:10]:
                title = entry.get('title', '')
                # Check keyword filter
                if source.get('keyword_filter'):
                    if not any(kw in title for kw in source['keyword_filter']):
                        continue
                
                news_items.append({
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "title": title,
                    "summary": entry.get('summary', '')[:200],
                    "source": source['name'],
                    "link": entry.get('link', ''),
                    "category": "行业动态"
                })
            return news_items
        else:
            # Basic XML parsing fallback
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.text)
            news_items = []
            # Try common RSS formats
            for item in root.iter('item'):
                title = item.findtext('title', '')
                if source.get('keyword_filter'):
                    if not any(kw in title for kw in source['keyword_filter']):
                        continue
                news_items.append({
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "title": title,
                    "summary": item.findtext('description', '')[:200],
                    "source": source['name'],
                    "link": item.findtext('link', ''),
                    "category": "行业动态"
                })
            return news_items[:10]
    except Exception as e:
        log_message(f"RSS fetch failed for {source['name']}: {e}")
        return []


def fetch_all_news():
    """Fetch news from all configured sources"""
    all_news = []
    
    # Try RSS sources
    for source in RSS_SOURCES:
        news = fetch_rss_feed(source)
        if news:
            all_news.extend(news)
            log_message(f"Fetched {len(news)} items from {source['name']}")
    
    return all_news


def inject_manual_news(manual_file):
    """Inject manually provided news from a JSON file"""
    try:
        with open(manual_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Failed to load manual news: {e}")
        return []


def update_data_file(new_news_items):
    """Update the satcom_data.json with new news"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        log_message(f"Failed to load data file: {e}")
        return False
    
    current_news = data.get('news', [])
    existing_titles = {n.get('title', '') for n in current_news}
    
    added = 0
    for item in new_news_items:
        if item.get('title') and item['title'] not in existing_titles:
            current_news.insert(0, item)
            existing_titles.add(item['title'])
            added += 1
    
    # Sort by date descending
    current_news.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Keep max 30 items
    data['news'] = current_news[:30]
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        log_message(f"Updated data file. Added {added} new items. Total news: {len(data['news'])}")
        return True
    except Exception as e:
        log_message(f"Failed to write data file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Satellite Communication News Fetcher')
    parser.add_argument('--manual-news', help='Path to JSON file with manually collected news')
    parser.add_argument('--force-simulated', action='store_true', help='Use simulated news if no sources available')
    parser.add_argument('--update-date-only', action='store_true', help='Only update the last_updated date')
    args = parser.parse_args()

    log_message("=" * 50)
    log_message("News fetcher started")

    if args.update_date_only:
        log_message("Update date only mode")
        update_data_file([])
        sys.exit(0)

    all_news = []

    # 1. Try manual news injection first (most reliable)
    if args.manual_news:
        manual_news = inject_manual_news(args.manual_news)
        if manual_news:
            all_news.extend(manual_news)
            log_message(f"Injected {len(manual_news)} manual news items")

    # 2. Try fetching from RSS sources
    if HAS_REQUESTS:
        fetched_news = fetch_all_news()
        if fetched_news:
            all_news.extend(fetched_news)
    else:
        log_message("requests library not available, skipping RSS fetch")

    # 3. Fallback to simulated news if nothing else worked
    if not all_news and args.force_simulated:
        log_message("Using simulated news as fallback")
        all_news = SIMULATED_NEWS

    if all_news:
        update_data_file(all_news)
    else:
        log_message("No news items fetched. Updating date only.")
        update_data_file([])

    log_message("News fetcher completed")


if __name__ == '__main__':
    main()
