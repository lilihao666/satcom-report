import re
import json

BASE = '/root/.openclaw/workspace/satcom-research-github'

def fix_payload_clickable(html):
    """给所有载荷卡片添加 clickable-card + onclick"""
    # 国内载荷 - 13家
    domestic = ['航天电子','上海瀚讯','星移联信','创智联恒','极光星通','蓝星光域','氦星光联','银河航天','京济通信','烽火通信','航天环宇','国博电子','铖昌科技']
    for name in domestic:
        old = f'<div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500">\n                <h4 class="font-bold text-lg">{name}</h4>'
        key = f"payload_{name}"
        new = f'<div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500 clickable-card relative" onclick="openModal(\'{key}\')">\n                <h4 class="font-bold text-lg">{name}</h4>'
        html = html.replace(old, new, 1)

    # 国际载荷
    intl = ['Mynaric','TESAT']
    for name in intl:
        old = f'<div class="bg-white rounded-lg shadow p-4 border-l-4 border-purple-500">\n                <h4 class="font-bold text-lg">{name}</h4>'
        key = f"payload_{name}"
        new = f'<div class="bg-white rounded-lg shadow p-4 border-l-4 border-purple-500 clickable-card relative" onclick="openModal(\'{key}\')">\n                <h4 class="font-bold text-lg">{name}</h4>'
        html = html.replace(old, new, 1)
    return html

def add_payload_modals(html):
    """在modalData中添加所有载荷厂商的详情"""
    modals = {}
    domestic_data = [
        ('航天电子', '10Gbps/15Gbps激光终端', '国家队龙头，国内唯一能量产星间激光终端并规模化在轨应用，GW星座市占约60%', '星载激光通信终端|ATP系统|光通信模块'),
        ('上海瀚讯', '5G NTN/量子加密星间链路', '千帆星座通信载荷独家供应商，"星-地-端"全链路布局，单套载荷价值约400万元', '卫星通信载荷|星载基站|信关站设备'),
        ('星移联信', 'IoT NTN/5G NR NTN', '国内首家专注卫星通信载荷系统设计的商业航天公司，2026年池州工厂投产，年产300台载荷，规划平天星座60+颗异构化卫星', '星载基站|星载路由|卫星物联网载荷'),
        ('创智联恒', '5G NTN/星上处理', '低轨卫星基带载荷国内市占率超75%，中国星网核心技术供应商，已实现全球首次5G NTN手机直连宽带视频通话', '星载基带载荷|星载路由|5G NTN载荷'),
        ('极光星通', '400Gbps激光通信', '首家完成400Gbps在轨测试，530km轨道实现5100km超远距建链，星网主力供应商', '星载激光通信终端|星间链路终端|高速光通信模块'),
        ('蓝星光域', 'Z4终端100Gbps/ATP系统', '第一家完成星载激光通信终端交付并在轨验证的中国商业航天公司，常熟基地年产千台', '星载激光通信终端|ATP系统|星间链路设备'),
        ('氦星光联', '高速激光通信终端', '目前在轨激光通信终端30余台，建成国内最大卫星激光通信终端产线，年产400台', '星载激光通信终端|激光通信模组|星间链路设备'),
        ('银河航天', '毫米波AiP瓦式多波束相控阵', '批量研制国内首批星载毫米波AiP瓦式多波束相控阵天线，已完成手机直连卫星在轨验证', '星载相控阵天线|多波束天线|通信载荷集成'),
        ('京济通信', '相控阵天线/射频组件', '参与了吉林一号星座、株洲星座、女娲星座等国内所有重大遥感卫星建设，完成国内首次双通道X频段4.2G速率星地通信试验', '星载相控阵天线|通信射频组件|星间链路设备'),
        ('烽火通信', '高速相干激光通信/光模块', '中国星网核心供应商，国内唯二可以制造激光通信终端光模块的企业，提供全栈式星间光通信解决方案', '高速相干激光通信终端|星载路由系统|光通信模块'),
        ('航天环宇', '有源相控阵天线', '参与鹊桥中继星关键部件研制，提供星载有源相控阵天线及射频组件', '星载相控阵天线|卫星通信天线|射频前端组件'),
        ('国博电子', 'T/R芯片/射频组件', '卫星载荷T/R组件核心供应商，为相控阵天线提供关键射频组件', '有源相控阵T/R完整组件|射频芯片|天线组件'),
        ('铖昌科技', '射频放大/LNA/幅相控制芯片', '相控阵芯片核心供应商，提供射频放大类芯片、低噪声放大器芯片、射频幅相控制芯片等', 'T/R芯片|射频放大器芯片|低噪声放大器|幅相控制芯片'),
    ]
    intl_data = [
        ('Mynaric', 'Condor MK3 100Gbps+', '欧洲星间激光通信领导者，合作SpaceX星链、欧洲IRIS²项目', '星载激光终端|地面光通信设备'),
        ('TESAT', 'LCT系列激光终端', '欧洲老牌激光通信厂商，为多个卫星项目提供激光通信终端', '星载激光通信终端|光学通信系统'),
    ]

    def make_modal(name, tech, desc, tags, is_intl=False):
        tag_html = ''.join([f'<span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">{t}</span>' for t in tags.split('|')])
        loc = '国际' if is_intl else '国内'
        return f'<div class="space-y-4"><div class="flex justify-between items-center"><span class="category-badge cat-internet">卫星载荷厂商</span><span class="text-xs text-gray-500">{loc}</span></div><div><p class="text-gray-600"><strong>核心技术:</strong> {tech}</p></div><div><p class="text-sm text-gray-500 mb-2">公司简介</p><p class="text-gray-700">{desc}</p></div><div><p class="font-semibold mb-2">主要产品:</p><div class="flex flex-wrap gap-2">{tag_html}</div></div><div><p class="font-semibold mb-2">🔍 详细调研:</p><div class="flex flex-wrap gap-2"><a href="https://www.baidu.com/s?wd={name}+卫星载荷" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>百度搜索</a><a href="https://www.tianyancha.com/search?key={name}" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>天眼查</a></div></div></div>'

    for name, tech, desc, tags in domestic_data:
        modals[f"payload_{name}"] = {"title": name, "content": make_modal(name, tech, desc, tags, False)}
    for name, tech, desc, tags in intl_data:
        modals[f"payload_{name}"] = {"title": name, "content": make_modal(name, tech, desc, tags, True)}

    # 屹信航天 modal
    modals["payload_屹信航天"] = {
        "title": "屹信航天",
        "content": '<div class="space-y-4"><div class="flex justify-between items-center"><span class="category-badge cat-internet">卫星载荷厂商</span><span class="text-xs text-gray-500">国内</span></div><div><p class="text-gray-600"><strong>核心技术:</strong> 微小卫星通信载荷/测控/数传</p></div><div><p class="text-sm text-gray-500 mb-2">公司简介</p><p class="text-gray-700">2018年成立，前军工卫星通信研究员孙谦创办。国内首家实现卫星物联网载荷大规模商业交付的企业，天启三号卫星物联网载荷供应商。2023年市占率63.6%，2024年85.7%。173+员工，交付500+台套，26颗卫星在2024年完成交付。国家级专精特新"小巨人"，IPO辅导中（2025年8月）。</p></div><div><p class="font-semibold mb-2">主要产品:</p><div class="flex flex-wrap gap-2"><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">卫星物联网载荷</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">测控应答机</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">星载图像压缩存储</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">高速数传</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">星载相控阵天线</span></div></div><div><p class="font-semibold mb-2">🔍 详细调研:</p><div class="flex flex-wrap gap-2"><a href="https://www.baidu.com/s?wd=屹信航天+卫星载荷" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>百度搜索</a><a href="https://www.tianyancha.com/search?key=屹信航天" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>天眼查</a></div></div></div>'
    }

    modal_json = json.dumps(modals, ensure_ascii=False, separators=(',', ':'))
    modal_json = modal_json[1:-1]  # strip outer braces

    # Insert before comp_SpaceX_Starlink in modalData
    html = html.replace('"comp_SpaceX_Starlink":', modal_json + ',"comp_SpaceX_Starlink":', 1)
    return html

def add_yixin_card(html):
    """在国内载荷厂商最后添加屹信航天"""
    card = '''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500 clickable-card relative" onclick="openModal('payload_屹信航天')">
                <h4 class="font-bold text-lg">屹信航天</h4>
                <p class="text-sm text-gray-500">微小卫星通信载荷/测控/数传</p>
                <p class="text-sm text-gray-600 mt-2">天启三号物联网载荷供应商，国内商业卫星载荷市占率85%+，173+员工，500+台套交付</p>
                <div class="flex flex-wrap gap-1 mt-2"><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">卫星物联网载荷</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">测控应答机</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">高速数传</span><span class="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">星载相控阵天线</span></div>
            </div>
'''
    marker = '<h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center"><span class="category-badge cat-internet mr-2">国际载荷厂商</span></h3>'
    html = html.replace(marker, card + marker, 1)
    return html

def add_pingtian(html):
    """添加平天星座到星座层和modalData"""
    # Add modal
    pingtian_modal = {
        "const_平天星座": {
            "title": "平天星座",
            "content": '<div class="space-y-4">\n            <div class="flex justify-between items-center"><span class="category-badge cat-internet">卫星互联网</span><span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">规划中</span></div>\n            <div><p class="text-gray-600"><strong>运营方:</strong> 星移联信</p><p class="text-gray-600"><strong>规划数量:</strong> 60+ 颗</p><p class="text-gray-600"><strong>已发射:</strong> 0 颗</p></div>\n            <div class="bg-gray-50 p-3 rounded-lg"><p class="font-semibold text-gray-700 mb-2"><i class="fas fa-satellite mr-1"></i> 星间链路</p><p class="text-sm text-gray-600">规划中，异构化卫星编队</p></div>\n            <div><p class="font-semibold mb-2">🔍 了解更多:</p><div class="flex flex-wrap gap-2"><a href="https://www.baidu.com/s?wd=平天星座+星移联信" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>搜索</a><a href="https://www.baidu.com/s?wd=平天星座+发射" target="_blank" class="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-sm hover:bg-blue-100 transition"><i class="fas fa-external-link-alt mr-1.5"></i>发射动态</a></div></div>\n            <div><p class="font-semibold mb-2">应用场景:</p><div class="flex flex-wrap gap-2"><span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">卫星互联网</span><span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">物联网</span><span class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">遥感</span></div></div>\n            <div class="mt-4"><p class="text-sm text-gray-500 mb-2">部署进度: 0.0%</p><div class="w-full bg-gray-200 rounded-full h-3"><div class="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full" style="width: 0.0%"></div></div></div>\n        </div>'
        }
    }
    modal_json = json.dumps(pingtian_modal, ensure_ascii=False, separators=(',', ':'))
    modal_json = modal_json[1:-1]
    html = html.replace('"const_蓝凌星通":', modal_json + ',"const_蓝凌星通":', 1)

    # Add card before 蓝凌星通
    card = '''<div class="bg-white rounded-lg shadow p-4 border-l-4 border-green-500 clickable-card relative" onclick="openModal('const_平天星座')">
                        <div class="flex justify-between items-center mb-2">
                            <h4 class="font-bold text-lg">平天星座</h4>
                            <span class="category-badge cat-internet">规划中</span>
                        </div>
                        <p class="text-sm text-gray-600">星移联信 | 60+颗 | 已发射0</p>
                        <p class="text-sm text-gray-500 mt-2">异构化卫星编队，卫星互联网星座</p>
                    </div>
'''
    marker = '<div class="bg-white rounded-lg shadow p-4 border-l-4 border-green-500 clickable-card relative" onclick="openModal(\'const_蓝凌星通\')">'
    html = html.replace(marker, card + marker, 1)
    return html

def add_more_news(html):
    """在最新动态区域添加5条新闻"""
    # Find the pattern: </div> </section> before <!-- 技术趋势 -->
    new_items = '''                <div class="border-l-4 border-green-500 pl-4 py-2">
                    <p class="text-sm font-semibold text-gray-800">2025年4月：屹信航天启动IPO辅导</p>
                    <p class="text-xs text-gray-500">南京屹信航天（现江苏屹信航天）正式开启IPO上市辅导，2023-2024年商业卫星载荷市占率从63.6%跃升至85.7%，173人团队交付500+台套</p>
                </div>
                <div class="border-l-4 border-blue-500 pl-4 py-2">
                    <p class="text-sm font-semibold text-gray-800">2025年4月：星移联信池州工厂投产</p>
                    <p class="text-xs text-gray-500">星移联信池州载荷工厂正式投产，年产300台卫星通信载荷，平天星座规划60+颗异构化卫星</p>
                </div>
                <div class="border-l-4 border-purple-500 pl-4 py-2">
                    <p class="text-sm font-semibold text-gray-800">2025年4月：千帆星座新增54颗卫星</p>
                    <p class="text-xs text-gray-500">垣信卫星千帆星座完成新一轮批量发射，在轨卫星数量增至126颗，二期G60星座部署加速</p>
                </div>
                <div class="border-l-4 border-orange-500 pl-4 py-2">
                    <p class="text-sm font-semibold text-gray-800">2025年4月：SpaceX星链突破7200颗</p>
                    <p class="text-xs text-gray-500">Starlink在轨运营卫星超7200颗，激光星间链路终端超24000个，手机直连服务覆盖进一步扩大</p>
                </div>
                <div class="border-l-4 border-red-500 pl-4 py-2">
                    <p class="text-sm font-semibold text-gray-800">2025年4月：国星宇航"星算计划"发射6颗</p>
                    <p class="text-xs text-gray-500">国星宇航成功发射6颗太空计算卫星，星算计划在轨卫星达27颗，全球首次实现星载AI推理集群</p>
                </div>
'''
    # The news section is inside <section id="news"> and ends before <!-- 技术趋势 -->
    # We need to insert before the closing </div> of the news grid
    # Pattern: the last news item ends, then </div> then </section>
    # Replace the closing </div></section> before 技术趋势
    old = '            </div>\n        </section>\n        <!-- 技术趋势 -->'
    new = new_items + '            </div>\n        </section>\n        <!-- 技术趋势 -->'
    html = html.replace(old, new, 1)
    return html

def process_file(path):
    print(f"Processing {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original_len = len(html)

    html = fix_payload_clickable(html)
    html = add_payload_modals(html)
    html = add_yixin_card(html)
    html = add_pingtian(html)
    html = add_more_news(html)

    new_len = len(html)
    print(f"  Size: {original_len} -> {new_len} (+{new_len-original_len})")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Verify clickable cards count
    clickable_count = html.count('clickable-card')
    print(f"  clickable-card count: {clickable_count}")

    return new_len - original_len

# Process both files
free_delta = process_file(f'{BASE}/index.html')
premium_delta = process_file(f'{BASE}/premium/index.html')

print(f"\nDone. Free: +{free_delta}, Premium: +{premium_delta}")
