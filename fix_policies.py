#!/usr/bin/env python3
"""
1. Fix domestic policy links
2. Remove placeholder news item
3. Add more latest news items
"""

import re
from urllib.parse import quote

def add_policy_link(match):
    prefix = match.group(1)
    title_match = re.search(r'<h4[^>]*>([^<]+)</h4>', prefix)
    if title_match:
        title = title_match.group(1).strip()
        search_title = re.sub(r'[《》]', '', title)
        encoded = quote(search_title)
        link = f'<div class="mt-2"><a href="https://www.bing.com/search?q={encoded}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a></div>'
        return prefix + link
    return prefix + '<div class="mt-2"></div>'

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Domestic policy links
    domestic_start = content.find('国内政策')
    intl_start = content.find('国际政策', domestic_start)
    domestic_section = content[domestic_start:intl_start]
    
    domestic_pattern = r'(<div class="p-3 bg-gray-50 rounded-lg border-l-4 border-(?:red|blue|green)-400">.*?<p class="text-sm text-gray-600 mt-2">[^<]+</p>\s*)<div class="mt-2"></div>'
    new_domestic = re.sub(domestic_pattern, add_policy_link, domestic_section, flags=re.DOTALL)
    content = content[:domestic_start] + new_domestic + content[intl_start:]
    
    # Fix 2: Remove placeholder news item
    news_start = content.find('<section id="news">')
    news_end = content.find('id="back-to-top"')
    news_section = content[news_start:news_end]
    
    # Find first news item and remove it
    first_div = news_section.find('<div class="bg-white rounded-lg shadow p-4 border-l-4 border-yellow-500">')
    if first_div != -1:
        # Find where the first item ends - look for closing </div> followed by newline and next item
        next_item = news_section.find('<div class="bg-white rounded-lg shadow p-4 border-l-4 border-yellow-500">', first_div + 1)
        if next_item != -1:
            # Remove from first_div to just before next_item
            new_news = news_section[:first_div] + news_section[next_item:]
            content = content[:news_start] + new_news + content[news_end:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('Done: Fixed domestic policy links, removed placeholder news')

if __name__ == '__main__':
    main()
