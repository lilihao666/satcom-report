#!/usr/bin/env python3
"""添加国外LoRa卫星星座数据"""
import json

# 读取数据文件
with open('/root/.openclaw/workspace/satcom-research-github/data/satcom_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 国外LoRa卫星星座
intl_lora_constellations = [
    {
        "name": "Eutelsat IoT",
        "operator": "Eutelsat",
        "planned": 30,
        "launched": 0,
        "stage": "规划中",
        "use_cases": ["物联网", "资产管理", "供应链追踪"],
        "note": "S波段卫星物联网星座，计划2026年开始部署",
        "inter_satellite_link": {
            "enabled": False,
            "tech": "无",
            "note": "无星间链路设计"
        },
        "detail_links": {
            "搜索": "https://www.google.com/search?q=Eutelsat+IoT+satellite",
            "官网": "https://www.eutelsat.com"
        },
        "category": "卫星物联网"
    },
    {
        "name": "Swarm (SpaceBEE)",
        "operator": "SpaceX/Swarm",
        "planned": 150,
        "launched": 150,
        "stage": "运营中",
        "use_cases": ["物联网", "农业监测", "环境监测"],
        "note": "已被SpaceX收购，提供全球物联网连接服务",
        "inter_satellite_link": {
            "enabled": False,
            "tech": "无",
            "note": "依赖地面站"
        },
        "detail_links": {
            "搜索": "https://www.google.com/search?q=Swarm+SpaceBEE+satellite+IoT",
            "官网": "https://swarm.space"
        },
        "category": "卫星物联网"
    },
    {
        "name": "Kepler",
        "operator": "Kepler Communications",
        "planned": 140,
        "launched": 21,
        "stage": "部署中",
        "use_cases": ["物联网", "宽带数据", "极地通信"],
        "note": "加拿大公司，专注极地和高纬度地区通信",
        "inter_satellite_link": {
            "enabled": False,
            "tech": "无",
            "note": "依赖地面站"
        },
        "detail_links": {
            "搜索": "https://www.google.com/search?q=Kepler+Communications+satellite",
            "官网": "https://kepler.space"
        },
        "category": "卫星物联网"
    },
    {
        "name": "Myriota",
        "operator": "Myriota",
        "planned": 50,
        "launched": 12,
        "stage": "部署中",
        "use_cases": ["物联网", "农业", "水资源监测"],
        "note": "澳大利亚公司，专注低功耗物联网",
        "inter_satellite_link": {
            "enabled": False,
            "tech": "无",
            "note": "无星间链路设计"
        },
        "detail_links": {
            "搜索": "https://www.google.com/search?q=Myriota+satellite+IoT",
            "官网": "https://myriota.com"
        },
        "category": "卫星物联网"
    }
]

# 添加到国际星座列表
for const in intl_lora_constellations:
    exists = any(c['name'] == const['name'] for c in data['constellations']['international'])
    if not exists:
        data['constellations']['international'].append(const)
        print(f"✓ 添加: {const['name']}")
    else:
        print(f"- 已存在: {const['name']}")

# 更新last_updated
data['last_updated'] = "2026-04-17"

# 保存文件
with open('/root/.openclaw/workspace/satcom-research-github/data/satcom_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 国外LoRa卫星星座添加完成!")
print(f"当前国际星座数量: {len(data['constellations']['international'])}")
