#!/usr/bin/env python3
"""
修复问题：
1. 删除指定星座的备注（红字）
2. 修正北京天行探索成立时间为2025年
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

def remove_constellation_notes(data):
    """删除指定星座的备注"""
    target_constellations = ["国网/GW星座", "椭圆时空", "国科宇航星座"]
    for c in data["constellations"]["domestic"]:
        if c["name"] in target_constellations:
            old_note = c.get("note", "")
            c["note"] = ""  # 清空备注
            print(f"✅ 清空备注: {c['name']} (原: {old_note})")
    return data

def fix_tianxing(data):
    """修复天行探索成立时间为2025年"""
    for c in data["companies"]["domestic"]:
        if c["name"] == "天行探索科技":
            old_founded = c.get("founded", "")
            c["founded"] = "2025"
            print(f"✅ 修正: {c['name']} 成立时间 {old_founded} -> 2025")
    return data

def main():
    print("📊 开始修复数据...")
    data = load_data()
    data = remove_constellation_notes(data)
    data = fix_tianxing(data)
    save_data(data)
    print("\n✅ 所有修复完成")

if __name__ == "__main__":
    main()
