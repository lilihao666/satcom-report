#!/usr/bin/env python3
"""
Add more latest news items to the HTML.
"""

import re
from urllib.parse import quote

def make_news_item(title, date, source, content, impact="medium"):
    """Generate HTML for a news item."""
    encoded_title = quote(title)
    return f'''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-yellow-500">
            <div class="flex justify-between items-start">
                <h3 class="font-bold text-lg">{title}</h3>
                <div class="text-right">
                    <span class="text-sm text-gray-500">{date}</span>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded ml-2">{impact}影响</span>
                </div>
            </div>
            <p class="text-xs text-gray-500 mt-1">来源: {source}</p>
            <p class="text-sm text-gray-600 mt-2">{content}</p>
            <div class="flex flex-wrap gap-2 mt-2"></div>
            <div class="mt-2 text-xs text-gray-500">影响领域: </div>
            <div class="mt-2"><a href="https://www.bing.com/search?q={encoded_title}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline text-sm"><i class="fas fa-external-link-alt mr-1"></i>查看详情</a></div>
        </div>
'''

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # New news items to add
    new_items = [
        {
            "title": "马斯克大动作！SpaceX 600亿美元收购Cursor，AI+航天帝国加速成型",
            "date": "2026-04-22",
            "source": "36氪/国际电子商情",
            "content": "4月22日，马斯克旗下SpaceX与AI编程初创公司Cursor签下600亿美元收购协议。与此同时，SpaceX董事会为马斯克量身定制激励方案：若公司市值冲到6.6万亿美元并建成火星殖民地和太空数据中心，马斯克将额外获得6000万股股票。SpaceX计划6月启动IPO，目标估值1.75万亿美元，有望成为人类历史上规模最大的IPO。",
            "impact": "high"
        },
        {
            "title": "商业航天进入催化密集期：千帆、GW双轨并行，市场规模有望达3.5万亿",
            "date": "2026-04-22",
            "source": "新浪财经/赛迪智库",
            "content": "4月7日，千帆星座第七批组网卫星以一箭18星方式成功发射；GW星座第20组卫星也成功发射，中国星网累计发射超150颗。赛迪智库数据显示，2025年中国商业航天市场规模已达2.83万亿元，2026年有望攀升至3.5万亿元级别。十余家头部企业密集冲刺资本市场。",
            "impact": "high"
        },
        {
            "title": "SpaceX IPO文件曝光：星链2025年运营利润44亿美元，AI支出127亿",
            "date": "2026-04-21",
            "source": "每日经济新闻/财联社",
            "content": "SpaceX IPO文件显示，2025年底公司拥有约248亿美元现金，总资产920亿美元。星链卫星互联网服务2025年产生44.2亿美元营业利润，成为唯一盈利业务。但AI领域资本支出从2024年的56亿美元飙升至127亿美元，导致公司2025年整体亏损49.4亿美元。",
            "impact": "high"
        },
        {
            "title": "蓝色起源首次成功发射翻新'新格伦'火箭并完成海上回收",
            "date": "2026-04-19",
            "source": "华尔街见闻",
            "content": "4月19日，美国蓝色起源公司成功发射一枚翻新的'新格伦'重型运载火箭，并首次在海上回收火箭第一级箭体。这标志着重型复用火箭技术迈入新阶段，与SpaceX形成竞争态势。",
            "impact": "medium"
        },
        {
            "title": "千帆星座获巴西运营批准，成为拉美首个开放市场的中国星座",
            "date": "2026-03-01",
            "source": "泰伯网/中国无线电",
            "content": "巴西电信监管机构Anatel批准千帆星座自2026年起在巴西开展商业通信服务，巴西成为拉美首个向该星座开放市场的国家。千帆星座规划超1.5万颗卫星，2025年已入轨超90颗，聚焦亚太及新兴市场覆盖。",
            "impact": "medium"
        },
    ]
    
    # Find news section
    news_start = content.find('<section id="news">')
    news_end = content.find('id="back-to-top"')
    news_section = content[news_start:news_end]
    
    # Find the insertion point - after the existing <div class="space-y-4">
    insert_point = news_section.find('<div class="space-y-4">') + len('<div class="space-y-4">')
    
    # Generate new items HTML
    new_html = '\n'.join(make_news_item(**item) for item in new_items)
    
    # Insert after the opening <div class="space-y-4">
    new_news_section = news_section[:insert_point] + '\n' + new_html + '\n' + news_section[insert_point:]
    
    content = content[:news_start] + new_news_section + content[news_end:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added {len(new_items)} new news items")

if __name__ == '__main__':
    main()
