#!/usr/bin/env python3
"""
URL-encode Chinese characters in search links to ensure cross-browser compatibility.
Also add rel="noopener noreferrer" for security.
"""

import re
from urllib.parse import quote

def encode_url(url):
    """URL-encode Chinese characters in the query string while preserving the base URL."""
    # Match pattern like https://www.baidu.com/s?wd=中文
    match = re.match(r'(https?://[^?]+\?)(.+)', url)
    if match:
        base = match.group(1)
        query = match.group(2)
        # Parse query parameters
        params = []
        for param in query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # URL encode the value
                encoded_value = quote(value, safe='')
                params.append(f'{key}={encoded_value}')
            else:
                params.append(param)
        return base + '&'.join(params)
    return url

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all baidu/google search links with Chinese characters and encode them
    link_pattern = r'href="(https://www\.(?:baidu|google)\.com/[^"]+)"'
    
    def fix_link(match):
        url = match.group(1)
        encoded = encode_url(url)
        # Also add rel attribute if not present
        return f'href="{encoded}" target="_blank" rel="noopener noreferrer"'
    
    # Only fix links that don't already have rel
    content = re.sub(r'href="(https://www\.(?:baidu|google)\.com/[^"]+)" target="_blank"', fix_link, content)
    
    # Count fixes
    count = len(re.findall(r'rel="noopener noreferrer"', content))
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {count} external links with URL encoding and security attributes")

if __name__ == '__main__':
    main()
