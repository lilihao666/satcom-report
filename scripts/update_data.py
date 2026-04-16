#!/usr/bin/env python3
"""
更新卫星通信调研数据
1. 校准星座数据
2. 为国际星座添加完整链接
3. 新增载荷板块
"""

import json
from pathlib import Path

def load_data():
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    data_file = Path(__file__).parent.parent / "data" / "satcom_data.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_constellations(data):
    """更新星座数据"""
    # 更新国内星座数据 - 校准数量
    domestic_updates = {
        "国网/GW星座": {"launched": 144},  # 更新为最新
        "千帆星座": {"launched": 108},
        "吉利未来星座": {"launched": 64},
        "天启星座": {"launched": 42},
    }
    
    for c in data["constellations"]["domestic"]:
        if c["name"] in domestic_updates:
            c.update(domestic_updates[c["name"]])
    
    # 更新国际星座数据 - 校准数量并添加链接
    for c in data["constellations"]["international"]:
        name = c["name"]
        
        # 更新卫星数量
        if name == "Starlink":
            c["launched"] = 9500
            c["inter_satellite_link"]["bandwidth"] = "200Gbps+"
            c["inter_satellite_link"]["note"] = "超24000个激光终端在轨"
        elif name == "OneWeb":
            c["launched"] = 654
        elif name == "Kuiper":
            c["launched"] = 200
        
        # 添加/更新链接
        if "detail_links" not in c:
            c["detail_links"] = {}
        
        # 搜索链接
        search_name = name.replace(" ", "+")
        c["detail_links"]["搜索"] = f"https://www.google.com/search?q={search_name}+satellite+constellation"
        
        # 官网链接
        website_map = {
            "Starlink": "https://www.starlink.com",
            "OneWeb": "https://www.oneweb.net",
            "Kuiper": "https://www.aboutamazon.com/what-we-do/devices-services/project-kuiper",
            "Iridium NEXT": "https://iridium.com",
            "Telesat Lightspeed": "https://www.telesat.com/leo/",
            "AST SpaceMobile": "https://ast-science.com",
            "Lynk": "https://www.lynk.world",
            "Omnispace": "https://omnispace.com",
            "Globalstar": "https://www.globalstar.com",
            "Inmarsat": "https://www.viasat.com",
            "AROGOS星座": "https://www.dlr.de",
        }
        if name in website_map:
            c["detail_links"]["官网"] = website_map[name]
    
    return data

def add_payload_section(data):
    """新增载荷板块数据"""
    
    payload_data = {
        "domestic": [
            {
                "name": "航天电子",
                "city": "武汉",
                "category": "激光通信终端",
                "focus": "星间激光通信载荷",
                "tech": "10Gbps/15Gbps激光终端",
                "products": [
                    "星载激光通信终端",
                    "ATP系统",
                    "光通信模块"
                ],
                "description": "国家队龙头，国内唯一能量产星间激光终端并规模化在轨应用，GW星座市占约60%",
                "founded": "1998",
                "funding": "上市公司",
                "capacity": "年产能500台套",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=航天电子+激光通信",
                    "天眼查": "https://www.tianyancha.com/search?key=航天电子"
                }
            },
            {
                "name": "上海瀚讯",
                "city": "上海",
                "category": "通信载荷",
                "focus": "低轨卫星通信载荷",
                "tech": "5G NTN/量子加密星间链路",
                "products": [
                    "卫星通信载荷",
                    "星载基站",
                    "信关站设备"
                ],
                "description": "千帆星座通信载荷独家供应商，'星-地-端'全链路布局，单套载荷价值约400万元",
                "founded": "2006",
                "funding": "上市公司",
                "capacity": "已锁定数十亿级订单",
                "website": "http://www.sh-hyhx.com",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=上海瀚讯+卫星载荷",
                    "天眼查": "https://www.tianyancha.com/search?key=上海瀚讯"
                }
            },
            {
                "name": "星移联信",
                "city": "池州",
                "category": "通信载荷",
                "focus": "卫星通信载荷系统",
                "tech": "IoT NTN/5G NR NTN",
                "products": [
                    "星载基站",
                    "星载路由",
                    "卫星物联网载荷"
                ],
                "description": "国内首家专注卫星通信载荷系统设计的商业航天公司，2026年池州工厂投产，年产300台载荷",
                "founded": "2020",
                "funding": "战略融资",
                "capacity": "年产300台载荷",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=星移联信+卫星通信载荷",
                    "天眼查": "https://www.tianyancha.com/search?key=星移联信"
                }
            },
            {
                "name": "创智联恒",
                "city": "成都",
                "category": "通信载荷",
                "focus": "低轨卫星基带载荷",
                "tech": "5G NTN/星上处理",
                "products": [
                    "星载基带载荷",
                    "星载路由",
                    "5G NTN载荷"
                ],
                "description": "低轨卫星基带载荷国内市占率超75%，中国星网核心技术供应商，已实现全球首次5G NTN手机直连宽带视频通话",
                "founded": "2018",
                "funding": "B轮",
                "capacity": "交付排至2027年",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=创智联恒+卫星载荷",
                    "天眼查": "https://www.tianyancha.com/search?key=创智联恒"
                }
            },
            {
                "name": "极光星通",
                "city": "北京",
                "category": "激光通信终端",
                "focus": "星间激光通信",
                "tech": "400Gbps激光通信",
                "products": [
                    "星载激光通信终端",
                    "星间链路终端",
                    "高速光通信模块"
                ],
                "description": "首家完成400Gbps在轨测试，530km轨道实现5100km超远距建链，星网主力供应商",
                "founded": "2020",
                "funding": "战略融资",
                "capacity": "2025订单超10亿元",
                "website": "http://www.auroracomm.cn",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=极光星通+激光通信",
                    "天眼查": "https://www.tianyancha.com/search?key=极光星通"
                }
            },
            {
                "name": "蓝星光域",
                "city": "常熟",
                "category": "激光通信终端",
                "focus": "星间激光通信终端",
                "tech": "Z4终端100Gbps/ATP系统",
                "products": [
                    "星载激光通信终端",
                    "ATP系统",
                    "星间链路设备"
                ],
                "description": "第一家完成星载激光通信终端交付并在轨验证的中国商业航天公司，常熟基地年产千台",
                "founded": "2021",
                "funding": "A轮",
                "capacity": "年产1000台，理论5000台",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=蓝星光域+激光通信",
                    "天眼查": "https://www.tianyancha.com/search?key=蓝星光域"
                }
            },
            {
                "name": "氦星光联",
                "city": "无锡",
                "category": "激光通信终端",
                "focus": "星间激光通信",
                "tech": "高速激光通信终端",
                "products": [
                    "星载激光通信终端",
                    "激光通信模组",
                    "星间链路设备"
                ],
                "description": "目前在轨激光通信终端30余台，建成国内最大卫星激光通信终端产线，年产400台",
                "founded": "2021",
                "funding": "A轮",
                "capacity": "年产400台",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=氦星光联+激光通信",
                    "天眼查": "https://www.tianyancha.com/search?key=氦星光联"
                }
            },
            {
                "name": "银河航天",
                "city": "北京",
                "category": "相控阵天线",
                "focus": "星载相控阵天线",
                "tech": "毫米波AiP瓦式多波束相控阵",
                "products": [
                    "星载相控阵天线",
                    "多波束天线",
                    "通信载荷集成"
                ],
                "description": "批量研制国内首批星载毫米波AiP瓦式多波束相控阵天线，已完成手机直连卫星在轨验证",
                "founded": "2016",
                "funding": "C轮",
                "capacity": "",
                "website": "https://www.galaxypower.cn",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=银河航天+相控阵",
                    "官网": "https://www.galaxypower.cn"
                }
            },
            {
                "name": "京济通信",
                "city": "北京",
                "category": "相控阵天线",
                "focus": "星载通信载荷",
                "tech": "相控阵天线/射频组件",
                "products": [
                    "星载相控阵天线",
                    "通信射频组件",
                    "星间链路设备"
                ],
                "description": "参与了吉林一号星座、株洲星座、女娲星座等国内所有重大遥感卫星建设，完成国内首次双通道X频段4.2G速率星地通信试验",
                "founded": "2015",
                "funding": "B轮",
                "capacity": "",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=京济通信+卫星载荷",
                    "天眼查": "https://www.tianyancha.com/search?key=京济通信"
                }
            },
            {
                "name": "烽火通信",
                "city": "武汉",
                "category": "激光通信终端",
                "focus": "星间光通信解决方案",
                "tech": "高速相干激光通信/光模块",
                "products": [
                    "高速相干激光通信终端",
                    "星载路由系统",
                    "光通信模块"
                ],
                "description": "中国星网核心供应商，国内唯二可以制造激光通信终端光模块的企业，提供全栈式星间光通信解决方案",
                "founded": "1999",
                "funding": "上市公司",
                "capacity": "",
                "website": "https://www.fiberhome.com",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=烽火通信+激光通信",
                    "官网": "https://www.fiberhome.com"
                }
            },
            {
                "name": "航天环宇",
                "city": "长沙",
                "category": "相控阵天线",
                "focus": "星载通信天线",
                "tech": "有源相控阵天线",
                "products": [
                    "星载相控阵天线",
                    "卫星通信天线",
                    "射频前端组件"
                ],
                "description": "参与鹊桥中继星关键部件研制，提供星载有源相控阵天线及射频组件",
                "founded": "2000",
                "funding": "上市公司",
                "capacity": "",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=航天环宇+卫星天线",
                    "天眼查": "https://www.tianyancha.com/search?key=航天环宇"
                }
            },
            {
                "name": "国博电子",
                "city": "南京",
                "category": "T/R组件",
                "focus": "有源相控阵T/R组件",
                "tech": "T/R芯片/射频组件",
                "products": [
                    "有源相控阵T/R完整组件",
                    "射频芯片",
                    "天线组件"
                ],
                "description": "卫星载荷T/R组件核心供应商，为相控阵天线提供关键射频组件",
                "founded": "2000",
                "funding": "上市公司",
                "capacity": "",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=国博电子+T/R组件",
                    "天眼查": "https://www.tianyancha.com/search?key=国博电子"
                }
            },
            {
                "name": "铖昌科技",
                "city": "杭州",
                "category": "T/R芯片",
                "focus": "相控阵T/R芯片",
                "tech": "射频放大/LNA/幅相控制芯片",
                "products": [
                    "T/R芯片",
                    "射频放大器芯片",
                    "低噪声放大器",
                    "幅相控制芯片"
                ],
                "description": "相控阵芯片核心供应商，提供射频放大类芯片、低噪声放大器芯片、射频幅相控制芯片等",
                "founded": "2010",
                "funding": "上市公司",
                "capacity": "",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=铖昌科技+相控阵芯片",
                    "天眼查": "https://www.tianyancha.com/search?key=铖昌科技"
                }
            }
        ],
        "international": [
            {
                "name": "Mynaric",
                "region": "德国",
                "category": "激光通信终端",
                "focus": "星间激光通信",
                "tech": "Condor MK3 100Gbps+",
                "products": [
                    "星载激光终端",
                    "地面光通信设备"
                ],
                "description": "欧洲星间激光通信领导者，合作SpaceX星链、欧洲IRIS²项目",
                "website": "https://www.mynaric.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Mynaric+laser+communication",
                    "官网": "https://www.mynaric.com"
                }
            },
            {
                "name": "TESAT",
                "region": "德国",
                "category": "激光通信终端",
                "focus": "星间激光通信",
                "tech": "LCT系列激光终端",
                "products": [
                    "星载激光通信终端",
                    "光学通信系统"
                ],
                "description": "欧洲老牌激光通信厂商，为多个卫星项目提供激光通信终端",
                "website": "https://www.tesat.de",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=TESAT+satellite+laser",
                    "官网": "https://www.tesat.de"
                }
            }
        ],
        "tech_roadmap": [
            {
                "stage": "星载激光通信",
                "tech": "10Gbps-400Gbps激光链路",
                "status": "商业化部署",
                "timeline": "2024-2030",
                "key_players": ["航天电子", "极光星通", "蓝星光域", "氦星光联"]
            },
            {
                "stage": "相控阵天线",
                "tech": "毫米波AiP/瓦片式多波束",
                "status": "批量应用",
                "timeline": "2023-2028",
                "key_players": ["银河航天", "京济通信", "航天环宇"]
            },
            {
                "stage": "5G NTN载荷",
                "tech": "3GPP标准星载基站",
                "status": "商业化初期",
                "timeline": "2024-2027",
                "key_players": ["上海瀚讯", "星移联信", "创智联恒"]
            },
            {
                "stage": "星上处理",
                "tech": "星载路由/星上交换",
                "status": "部署中",
                "timeline": "2024-2028",
                "key_players": ["烽火通信", "创智联恒", "航天电子"]
            }
        ]
    }
    
    data["payloads"] = payload_data
    return data

def main():
    print("📊 开始更新卫星通信数据...")
    
    data = load_data()
    
    # 1. 更新星座数据
    print("🔄 校准星座数据并添加国际星座链接...")
    data = update_constellations(data)
    
    # 2. 新增载荷板块
    print("🔄 新增载荷板块数据...")
    data = add_payload_section(data)
    
    # 更新最后更新时间
    from datetime import datetime
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    # 保存
    save_data(data)
    print("✅ 数据更新完成!")
    print(f"   - 国内星座: {len(data['constellations']['domestic'])} 个")
    print(f"   - 国际星座: {len(data['constellations']['international'])} 个")
    print(f"   - 国内载荷厂商: {len(data['payloads']['domestic'])} 家")
    print(f"   - 国际载荷厂商: {len(data['payloads']['international'])} 家")
    print(f"   - 载荷技术路线: {len(data['payloads']['tech_roadmap'])} 条")

if __name__ == "__main__":
    main()
