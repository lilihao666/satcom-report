#!/usr/bin/env python3
"""
新增卫星运营商数据
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

def add_operators(data):
    """新增运营商板块"""
    
    operators_data = {
        "domestic": [
            {
                "name": "中国星网",
                "full_name": "中国卫星网络集团有限公司",
                "type": "国家队",
                "founded": "2021",
                "headquarters": "北京",
                "constellation": "国网/GW星座",
                "satellites_planned": 12992,
                "satellites_launched": 144,
                "services": ["宽带互联网", "物联网", "导航增强", "手机直连"],
                "business_model": "国家队主导，统筹国内低轨星座建设",
                "financing": "国资委全资",
                "valuation": "",
                "key_metrics": {
                    "星座规模": "12992颗（规划）",
                    "当前在轨": "144颗",
                    "目标市场": "国内+一带一路",
                    "服务能力": "2030年全球覆盖"
                },
                "partnerships": ["中国航天科技", "中国航天科工", "中科院", "中国电科"],
                "regulatory": "工信部频率许可，国防科工局发射许可",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=中国星网+卫星互联网",
                    "天眼查": "https://www.tianyancha.com/search?key=中国卫星网络集团"
                }
            },
            {
                "name": "垣信卫星",
                "full_name": "上海垣信卫星科技有限公司",
                "type": "商业航天",
                "founded": "2018",
                "headquarters": "上海",
                "constellation": "千帆星座(G60)",
                "satellites_planned": 15000,
                "satellites_launched": 108,
                "services": ["宽带通信", "物联网", "手机直连", "遥感数据"],
                "business_model": "G60星链计划，面向全球提供低轨宽带服务",
                "financing": "A轮+战略融资",
                "valuation": "超百亿人民币",
                "key_metrics": {
                    "星座规模": "15000颗（规划）",
                    "一期目标": "648颗（2025年）",
                    "二期目标": "15000颗（2027年）",
                    "制造能力": "年产300颗（G60基地）"
                },
                "partnerships": ["格思航天", "银河航天", "中科院小卫星工程部", "上海微小卫星工程中心"],
                "regulatory": "上海市政府支持，G60科创走廊重点项目",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=垣信卫星+千帆星座",
                    "天眼查": "https://www.tianyancha.com/search?key=垣信卫星"
                }
            },
            {
                "name": "时空道宇",
                "full_name": "浙江时空道宇科技有限公司",
                "type": "商业航天",
                "founded": "2018",
                "headquarters": "杭州",
                "constellation": "吉利未来出行星座",
                "satellites_planned": 5676,
                "satellites_launched": 64,
                "services": ["智能网联", "自动驾驶", "手机直连", "物联网"],
                "business_model": "吉利旗下，专注出行生态卫星服务",
                "financing": "吉利控股全资",
                "valuation": "",
                "key_metrics": {
                    "星座规模": "5676颗（规划）",
                    "一期完成": "72颗（2024年）",
                    "二期规划": "5604颗",
                    "覆盖范围": "一期覆盖中国及东南亚"
                },
                "partnerships": ["吉利集团", "极氪", "领克", "魅族", "中国电信"],
                "regulatory": "浙江省重点商业航天项目",
                "website": "https://www.geespace.com",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=时空道宇+吉利星座",
                    "天眼查": "https://www.tianyancha.com/search?key=时空道宇",
                    "官网": "https://www.geespace.com"
                }
            },
            {
                "name": "国电高科",
                "full_name": "北京国电高科科技有限公司",
                "type": "商业航天",
                "founded": "2015",
                "headquarters": "北京",
                "constellation": "天启星座",
                "satellites_planned": 38,
                "satellites_launched": 42,
                "services": ["卫星物联网", "数据采集", "应急通信"],
                "business_model": "国内首个商业物联网星座，专注窄带数据传输",
                "financing": "B+轮",
                "valuation": "数十亿人民币",
                "key_metrics": {
                    "星座规模": "38颗（完成部署）",
                    "实际发射": "42颗",
                    "覆盖范围": "全球",
                    "服务领域": "能源、环保、应急、物流"
                },
                "partnerships": ["中国航天科技", " elliptical时空（数据合作）"],
                "regulatory": "工信部卫星物联网频率许可",
                "website": "http://www.gddstech.com",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=国电高科+天启星座",
                    "天眼查": "https://www.tianyancha.com/search?key=国电高科"
                }
            },
            {
                "name": "椭圆时空",
                "full_name": "椭圆时空（深圳）科技有限公司",
                "type": "商业航天",
                "founded": "2016",
                "headquarters": "深圳",
                "constellation": "星池计划",
                "satellites_planned": 96,
                "satellites_launched": 6,
                "services": ["通导遥一体化", "物联网", "遥感数据"],
                "business_model": "通导遥融合星座，即时遥感服务",
                "financing": "B轮",
                "valuation": "",
                "key_metrics": {
                    "星座规模": "96颗（规划）",
                    "第一阶段": "12颗（通导遥一体化）",
                    "服务模式": "分钟级重访遥感"
                },
                "partnerships": ["国电高科（数据合作）", "清华大学", "哈工大"],
                "regulatory": "深圳市政府支持",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=椭圆时空+星池计划",
                    "天眼查": "https://www.tianyancha.com/search?key=椭圆时空"
                }
            },
            {
                "name": "银河航天",
                "full_name": "银河航天（北京）科技有限公司",
                "type": "商业航天",
                "founded": "2016",
                "headquarters": "北京",
                "constellation": "银河航天星座（规划中）",
                "satellites_planned": 1000,
                "satellites_launched": 12,
                "services": ["宽带通信", "卫星互联网", "手机直连"],
                "business_model": "对标Starlink，专注低轨宽带卫星",
                "financing": "C轮",
                "valuation": "超110亿人民币",
                "key_metrics": {
                    "验证星": "已发射多颗试验星",
                    "技术能力": "相控阵天线、星间链路",
                    "制造基地": "南通卫星超级工厂（年产300颗）"
                },
                "partnerships": ["南通市政府", "中国航天科技", "运营商合作"],
                "regulatory": "发改委核准，南通市重点招商项目",
                "website": "https://www.galaxypower.cn",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=银河航天+低轨星座",
                    "天眼查": "https://www.tianyancha.com/search?key=银河航天"
                }
            },
            {
                "name": "钧天航宇",
                "full_name": "北京钧天航宇科技有限公司",
                "type": "商业航天",
                "founded": "2020",
                "headquarters": "北京",
                "constellation": "钧天航宇星座",
                "satellites_planned": 72,
                "satellites_launched": 0,
                "services": ["宽带通信", "物联网", "导航增强"],
                "business_model": "高性价比平板卫星星座",
                "financing": "Pre-A轮",
                "valuation": "",
                "key_metrics": {
                    "星座规模": "72颗（一期）",
                    "技术特点": "平板卫星、一箭多星",
                    "目标市场": "行业应用、偏远地区"
                },
                "partnerships": ["航天发射服务商"],
                "regulatory": "规划中",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=钧天航宇+卫星",
                    "天眼查": "https://www.tianyancha.com/search?key=钧天航宇"
                }
            },
            {
                "name": "蓝凌星通",
                "full_name": "成都蓝凌星通科技有限公司",
                "type": "商业航天",
                "founded": "2020",
                "headquarters": "成都",
                "constellation": "蓝凌星座",
                "satellites_planned": 12,
                "satellites_launched": 0,
                "services": ["物联网", "数据采集", "行业应用"],
                "business_model": "区域性卫星物联网服务",
                "financing": "天使轮",
                "valuation": "",
                "key_metrics": {
                    "星座规模": "12颗（规划）",
                    "服务模式": "低轨物联网数据采集"
                },
                "partnerships": [],
                "regulatory": "规划中",
                "website": "",
                "detail_links": {
                    "百度搜索": "https://www.baidu.com/s?wd=蓝凌星通+卫星",
                    "天眼查": "https://www.tianyancha.com/search?key=蓝凌星通"
                }
            }
        ],
        "international": [
            {
                "name": "SpaceX Starlink",
                "full_name": "SpaceX / Starlink",
                "type": "商业航天",
                "founded": "2002 (SpaceX), 2015 (Starlink)",
                "headquarters": "美国加州霍桑",
                "constellation": "Starlink",
                "satellites_planned": 42000,
                "satellites_launched": 9500,
                "services": ["宽带互联网", "手机直连", "军事通信", "海事航空"],
                "business_model": "全球最大低轨星座，直接面向消费者销售终端和服务",
                "financing": "私有公司",
                "valuation": "SpaceX估值超1800亿美元",
                "revenue": "Starlink 2024年收入超66亿美元，已实现盈利",
                "key_metrics": {
                    "星座规模": "42000颗（规划）",
                    "当前在轨": "9500+颗",
                    "用户数量": "400万+（2024年）",
                    "覆盖范围": "全球100+国家",
                    "激光终端": "24000+个在轨"
                },
                "partnerships": ["T-Mobile（手机直连）", "Delta（航空）", "皇家加勒比（邮轮）", "美军"],
                "regulatory": "FCC许可，全球多国运营许可",
                "website": "https://www.starlink.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=SpaceX+Starlink",
                    "官网": "https://www.starlink.com"
                }
            },
            {
                "name": "Eutelsat OneWeb",
                "full_name": "Eutelsat Group (OneWeb)",
                "type": "商业航天",
                "founded": "2012 (OneWeb), 2023合并",
                "headquarters": "英国伦敦/法国巴黎",
                "constellation": "OneWeb",
                "satellites_planned": 648,
                "satellites_launched": 654,
                "services": ["企业宽带", "政府通信", "海事航空", "物联网"],
                "business_model": "B2B为主，专注政府和企业客户",
                "financing": "上市公司（Eutelsat）",
                "valuation": "合并后市值约30亿欧元",
                "revenue": "Eutelsat集团年营收约12亿欧元",
                "key_metrics": {
                    "星座规模": "648颗（完成一代）",
                    "实际发射": "654颗",
                    "服务能力": "二代计划3000颗（待定）",
                    "覆盖范围": "全球",
                    "客户类型": "政府、企业、海事、航空"
                },
                "partnerships": [" Hughes Network", "Kymeta", "Intellian", "多国政府"],
                "regulatory": "英国、法国、美国FCC、欧盟",
                "website": "https://www.oneweb.net",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Eutelsat+OneWeb",
                    "官网": "https://www.oneweb.net"
                }
            },
            {
                "name": "Amazon Kuiper",
                "full_name": "Amazon / Project Kuiper",
                "type": "互联网巨头",
                "founded": "2019",
                "headquarters": "美国华盛顿州西雅图",
                "constellation": "Project Kuiper",
                "satellites_planned": 3236,
                "satellites_launched": 200,
                "services": ["宽带互联网", "AWS云服务集成", "企业网络"],
                "business_model": "与AWS云服务深度集成，面向企业和消费者",
                "financing": "Amazon投资超100亿美元",
                "valuation": "Amazon子公司",
                "revenue": "尚未商用（计划2026年）",
                "key_metrics": {
                    "星座规模": "3236颗（规划）",
                    "当前发射": "200颗（测试+量产初期）",
                    "计划商用": "2026年开始",
                    "终端价格": "目标低于400美元",
                    "服务价格": "与Starlink竞争"
                },
                "partnerships": ["Verizon（5G回传）", "Vodafone", "AWS", "ULA/阿丽亚娜/蓝源（发射）"],
                "regulatory": "FCC许可，全球多国申请中",
                "website": "https://www.aboutamazon.com/what-we-do/devices-services/project-kuiper",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Amazon+Kuiper+satellite",
                    "官网": "https://www.aboutamazon.com/what-we-do/devices-services/project-kuiper"
                }
            },
            {
                "name": "Iridium",
                "full_name": "Iridium Communications Inc.",
                "type": "商业航天",
                "founded": "1991（一代）, 2017（二代NEXT完成）",
                "headquarters": "美国弗吉尼亚州",
                "constellation": "Iridium NEXT",
                "satellites_planned": 75,
                "satellites_launched": 75,
                "services": ["卫星电话", "物联网", "航空跟踪", "海事通信"],
                "business_model": "老牌卫星运营商，L波段语音和数据服务",
                "financing": "纳斯达克上市 (IRDM)",
                "valuation": "市值约60亿美元",
                "revenue": "年营收约7亿美元",
                "key_metrics": {
                    "星座规模": "75颗（66颗工作+9颗备用）",
                    "代际": "第二代Iridium NEXT（2017年完成）",
                    "服务寿命": "设计寿命15年",
                    "覆盖": "全球包括两极",
                    "合作伙伴": "200+行业合作伙伴"
                },
                "partnerships": ["Garmin", "Honeywell", "Thales", "SpaceX（发射服务）"],
                "regulatory": "FCC，全球多国运营许可",
                "website": "https://www.iridium.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Iridium+satellite+communications",
                    "官网": "https://www.iridium.com"
                }
            },
            {
                "name": "Telesat",
                "full_name": "Telesat Corporation",
                "type": "商业航天",
                "founded": "1969",
                "headquarters": "加拿大渥太华",
                "constellation": "Telesat Lightspeed",
                "satellites_planned": 198,
                "satellites_launched": 0,
                "services": ["企业宽带", "政府网络", "5G回传"],
                "business_model": "从GEO向LEO转型，专注高端企业客户",
                "financing": "多伦多/纳斯达克上市",
                "valuation": "市值约20亿加元",
                "revenue": "年营收约8亿加元（主要来自GEO业务）",
                "key_metrics": {
                    "星座规模": "198颗LEO（规划中）",
                    "状态": "尚未开始大规模部署",
                    "投资": "Lightspeed计划50亿加元",
                    "目标市场": "北美企业、政府"
                },
                "partnerships": ["MDA（卫星制造）", "SpaceX（发射）", "加拿大政府"],
                "regulatory": "加拿大、美国FCC、ITU",
                "website": "https://www.telesat.com/leo/",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Telesat+Lightspeed+LEO",
                    "官网": "https://www.telesat.com/leo/"
                }
            },
            {
                "name": "AST SpaceMobile",
                "full_name": "AST SpaceMobile, Inc.",
                "type": "商业航天",
                "founded": "2017",
                "headquarters": "美国德克萨斯州",
                "constellation": "BlueWalker",
                "satellites_planned": 168,
                "satellites_launched": 5,
                "services": ["手机直连卫星", "卫星宽带", "全球漫游"],
                "business_model": "与移动运营商合作，普通手机直连卫星",
                "financing": "纳斯达克上市 (ASTS)",
                "valuation": "市值波动较大（20-40亿美元）",
                "revenue": "尚未商用（计划2026年Q2美国商用）",
                "key_metrics": {
                    "星座规模": "168颗（规划）",
                    "卫星设计": "超大面积相控阵天线",
                    "合作运营商": "AT&T、Rakuten、Vodafone等",
                    "测试进展": "已完成手机直连语音通话测试"
                },
                "partnerships": ["AT&T（美国）", "Rakuten（日本）", "Vodafone（欧洲）", "Orange"],
                "regulatory": "FCC许可，多国频谱协商中",
                "website": "https://ast-science.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=AST+SpaceMobile+BlueWalker",
                    "官网": "https://ast-science.com"
                }
            },
            {
                "name": "Lynk Global",
                "full_name": "Lynk Global, Inc.",
                "type": "商业航天",
                "founded": "2017",
                "headquarters": "美国弗吉尼亚州",
                "constellation": "Lynk",
                "satellites_planned": 5000,
                "satellites_launched": 4,
                "services": ["手机直连短信", "应急通信", "物联网"],
                "business_model": "从短信起步，逐步实现语音和数据直连",
                "financing": "战略融资+政府合同",
                "valuation": "",
                "revenue": "早期阶段，政府合同收入",
                "key_metrics": {
                    "星座规模": "5000颗（长期规划）",
                    "当前阶段": "短信服务测试",
                    "服务方式": "无需改装现有手机",
                    "商业模式": "与移动运营商收入分成"
                },
                "partnerships": ["多个移动运营商（保密）", "美国国防部"],
                "regulatory": "FCC，频谱共享协议",
                "website": "https://www.lynk.world",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Lynk+Global+satellite+direct+to+phone",
                    "官网": "https://www.lynk.world"
                }
            },
            {
                "name": "Omnispace",
                "full_name": "Omnispace, LLC",
                "type": "商业航天",
                "founded": "2012",
                "headquarters": "美国弗吉尼亚州",
                "constellation": "Omnispace",
                "satellites_planned": 300,
                "satellites_launched": 2,
                "services": ["5G NTN", "物联网", "手机直连"],
                "business_model": "3GPP标准5G NTN卫星，与 terrestrial 5G融合",
                "financing": "战略融资",
                "valuation": "",
                "revenue": "早期阶段",
                "key_metrics": {
                    "星座规模": "300颗（规划）",
                    "技术标准": "3GPP 5G NTN",
                    "测试进展": "已完成5G语音通话测试"
                },
                "partnerships": ["NTT DoCoMo", "软银", "Marlin Capital"],
                "regulatory": "FCC，3GPP标准组织",
                "website": "https://omnispace.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Omnispace+5G+NTN+satellite",
                    "官网": "https://omnispace.com"
                }
            },
            {
                "name": "Globalstar",
                "full_name": "Globalstar, Inc.",
                "type": "商业航天",
                "founded": "1991",
                "headquarters": "美国路易斯安那州",
                "constellation": "Globalstar",
                "satellites_planned": 48,
                "satellites_launched": 48,
                "services": ["卫星电话", "物联网", "应急通信"],
                "business_model": "区域性LEO星座，与苹果合作提供紧急SOS服务",
                "financing": "纳斯达克上市 (GSAT)",
                "valuation": "市值约30亿美元",
                "revenue": "年营收约1.5亿美元",
                "key_metrics": {
                    "星座规模": "48颗LEO（二代）",
                    "特点": "无星间链路，依赖地面站",
                    "苹果合作": "iPhone卫星紧急SOS服务",
                    "服务区域": "北美、欧洲、澳大利亚"
                },
                "partnerships": ["Apple（iPhone卫星SOS）", "高通", "Nokia"],
                "regulatory": "FCC，多国运营许可",
                "website": "https://www.globalstar.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Globalstar+satellite+phone",
                    "官网": "https://www.globalstar.com"
                }
            },
            {
                "name": "Inmarsat/Viasat",
                "full_name": "Viasat, Inc. (收购Inmarsat)",
                "type": "商业航天",
                "founded": "1979 (Inmarsat), 2023收购",
                "headquarters": "英国伦敦/美国加州",
                "constellation": "Inmarsat GEO + Viasat",
                "satellites_planned": 5,
                "satellites_launched": 5,
                "services": ["海事通信", "航空宽带", "政府通信"],
                "business_model": "GEO卫星运营商，Inmarsat被Viasat收购",
                "financing": "Viasat纳斯达克上市 (VSAT)",
                "valuation": "收购价约74亿美元",
                "revenue": "Viasat年营收约40亿美元",
                "key_metrics": {
                    "星座类型": "GEO高轨卫星",
                    "Inmarsat历史": "40+年海事卫星经验",
                    "服务领域": "海事、航空、政府",
                    "合并": "2023年完成收购"
                },
                "partnerships": ["多家航空公司", "航运公司", "政府客户"],
                "regulatory": "英国、美国FCC、国际海事组织",
                "website": "https://www.viasat.com",
                "detail_links": {
                    "Google搜索": "https://www.google.com/search?q=Viasat+Inmarsat+satellite",
                    "官网": "https://www.viasat.com"
                }
            }
        ]
    }
    
    data["operators"] = operators_data
    print(f"✅ 新增运营商数据: 国内{len(operators_data['domestic'])}家, 国际{len(operators_data['international'])}家")
    return data

def main():
    print("📊 开始新增运营商数据...")
    data = load_data()
    data = add_operators(data)
    
    from datetime import datetime
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_data(data)
    print("✅ 运营商数据添加完成!")

if __name__ == "__main__":
    main()
