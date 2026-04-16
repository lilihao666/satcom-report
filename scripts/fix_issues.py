#!/usr/bin/env python3
"""
修复四个问题：
1. 星座卡片红色字体改为蓝色
2. 吉利未来星座改为物联网分类
3. 国际星座增加链接显示
4. 载荷弹窗转义修复
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

def fix_constellation_category(data):
    """修复吉利未来星座分类"""
    for c in data["constellations"]["domestic"]:
        if c["name"] == "吉利未来星座":
            c["category"] = "卫星物联网"
            print(f"✅ 修复: {c['name']} -> {c['category']}")
    return data

def main():
    data = load_data()
    data = fix_constellation_category(data)
    save_data(data)
    print("\n✅ 数据文件修复完成")

if __name__ == "__main__":
    main()
