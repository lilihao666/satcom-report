#!/usr/bin/env python3
"""
Fix three issues in the satcom research HTML:
1. Latest news - add "view details" search links
2. International policy - add external links
3. Payload vendors - add clickable modal functionality
"""

import re
import html

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ========== FIX 1: International Policy Links ==========
    # Find international policy section and add links
    policy_section_marker = '<h3 class="font-bold text-lg mb-3 text-purple-600">国际政策</h3>'
    if policy_section_marker in content:
        parts = content.split(policy_section_marker)
        before = parts[0]
        after = policy_section_marker + parts[1]
        
        # Replace empty <div class="mt-2"></div> in international policy with search links
        # Pattern: find policy items and add links
        intl_policy_pattern = r'(<div class="p-3 bg-gray-50 rounded-lg border-l-4 border-(?:yellow|red)-400">\s*<div class="flex justify-between items-start">\s*<h4 class="font-semibold">([^<]+)</h4>\s*<span class="text-xs text-gray-500">([^<]+)</span>\s*</div>\s*<p class="text-xs text-gray-500 mt-1">([^<]+)</p>\s*<p class="text-sm text-gray-600 mt-2">([^<]+)</p>\s*)<div class="mt-2"></div>'
        
        def add_policy_link(match):
            prefix = match.group(1)
            title = match.group(2).strip()
            # Create search link
            search_query = html.escape(title)
            link = f'<div class="mt-2"><a href="https://www.baidu.com/s?wd={search_query}" target="_blank" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a></div>'
            return prefix + link
        
        after = re.sub(intl_policy_pattern, add_policy_link, after, flags=re.DOTALL)
        content = before + after
    
    # ========== FIX 2: Latest News - Add View Details Links ==========
    # Find news section and add search links to each item
    news_section_start = '<section id="news">'
    news_section_end = '</section>'
    
    news_start_idx = content.find(news_section_start)
    if news_start_idx != -1:
        news_end_idx = content.find(news_section_end, news_start_idx + len(news_section_start))
        news_section = content[news_start_idx:news_end_idx + len(news_section_end)]
        
        # Replace empty divs at end of news items with search links
        news_item_pattern = r'(<div class="bg-white rounded-lg shadow p-4 border-l-4 border-yellow-500">.*?<p class="text-xs text-gray-500 mt-1">([^<]+)</p>.*?<p class="text-sm text-gray-600 mt-2">([^<]+)</p>\s*<div class="flex flex-wrap gap-2 mt-2"></div>\s*<div class="mt-2 text-xs text-gray-500">影响领域:[^<]*</div>\s*)<div class="mt-2"></div>'
        
        def add_news_link(match):
            prefix = match.group(1)
            source = match.group(2).strip()
            # Extract title from the h3 tag in prefix
            title_match = re.search(r'<h3 class="font-bold text-lg">([^<]+)</h3>', prefix)
            if title_match:
                title = title_match.group(1).strip()
                search_query = html.escape(title)
                link = f'<div class="mt-2"><a href="https://www.baidu.com/s?wd={search_query}" target="_blank" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a></div>'
                return prefix + link
            return prefix + '<div class="mt-2"></div>'
        
        new_news_section = re.sub(news_item_pattern, add_news_link, news_section, flags=re.DOTALL)
        content = content[:news_start_idx] + new_news_section + content[news_end_idx + len(news_section_end):]
    
    # ========== FIX 3: Payload Vendors - Add clickable modal ==========
    # We need to:
    # a) Add clickable-card class and onclick to payload vendor cards
    # b) Add modal data for each vendor
    
    # Find payload section
    payload_start_marker = '<section id="payload">'
    payload_end_marker = '<section id="operator">'
    
    payload_start_idx = content.find(payload_start_marker)
    payload_end_idx = content.find(payload_end_marker)
    
    if payload_start_idx != -1 and payload_end_idx != -1:
        payload_section = content[payload_start_idx:payload_end_idx]
        
        # Find payload vendor cards (h4 tags within the domestic/international sections)
        # Pattern for vendor cards
        vendor_pattern = r'(<div class="bg-white rounded-lg shadow p-4 border-l-4 border-(?:blue|purple)-500">)\s*(<h4 class="font-bold text-lg">([^<]+)</h4>)'
        
        vendor_keys = []
        def make_clickable(match):
            div_start = match.group(1)
            h4_tag = match.group(2)
            name = match.group(3).strip()
            # Create safe key
            key = 'payload_' + re.sub(r'[^\w]', '_', name)
            vendor_keys.append((key, name))
            return f'{div_start[:-1]} clickable-card relative" onclick="openModal(\'{key}\')">\n                {h4_tag}'
        
        new_payload = re.sub(vendor_pattern, make_clickable, payload_section)
        content = content[:payload_start_idx] + new_payload + content[payload_end_idx:]
        
        # Add modal data for payload vendors
        if vendor_keys:
            # Find modalData object
            modal_data_match = re.search(r'(const modalData = \{)(.*?)(\};\s*\n\s*function openModal)', content, re.DOTALL)
            if modal_data_match:
                prefix = modal_data_match.group(1)
                existing_data = modal_data_match.group(2)
                suffix = modal_data_match.group(3)
                
                # Build payload modal entries
                payload_entries = []
                for key, name in vendor_keys:
                    entry = f'"{key}": {{"title": "{name}", "content": "<div class=\\"space-y-4\\"><div class=\\"flex justify-between items-center\\"><span class=\\"category-badge cat-internet\\">卫星载荷厂商</span></div><div><p class=\\"text-gray-600\\"><strong>厂商:</strong> {name}</p></div><div><p class=\\"font-semibold mb-2\\">🔍 详细调研:</p><div class=\\"flex flex-wrap gap-2\\"><a href=\\"https://www.baidu.com/s?wd={html.escape(name)}+卫星载荷\\" target=\\"_blank\\" class=\\"inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition\\"><i class=\\"fas fa-external-link-alt mr-1.5\\"></i>百度搜索</a><a href=\\"https://www.tianyancha.com/search?key={html.escape(name)}\\" target=\\"_blank\\" class=\\"inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition\\"><i class=\\"fas fa-external-link-alt mr-1.5\\"></i>天眼查</a></div></div></div>"}}'
                    payload_entries.append(entry)
                
                # Insert before the closing of modalData
                new_modal_data = prefix + existing_data + ',' + ','.join(payload_entries) + suffix
                content = content[:modal_data_match.start()] + new_modal_data + content[modal_data_match.end():]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: Added {len(vendor_keys)} payload vendor modals")
    print("Fixes applied: international policy links, latest news links, payload vendor clickables")

if __name__ == '__main__':
    main()
