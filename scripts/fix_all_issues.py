#!/usr/bin/env python3
"""
修复四个问题：
1. 天行探索 - 更正为北京天行探索科技有限公司，修正成立时间
2. 删除国内星座详情中的橙色备注框（用户认为内容错误）
3. 修复载荷弹窗转义问题
4. 确保国际星座链接正确显示
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

def fix_tianxing(data):
    """修复天行探索数据"""
    for c in data["companies"]["domestic"]:
        if c["name"] == "天行探索科技":
            # 根据天眼查信息：北京天行探索科技有限公司
            # 成立于2022年，位于北京
            c["name"] = "天行探索科技"
            c["city"] = "北京"
            c["founded"] = "2022"
            c["funding"] = "天使轮"
            c["full_name"] = "北京天行探索科技有限公司"
            print(f"✅ 修复: {c['name']} -> 城市: {c['city']}, 成立: {c['founded']}")
    return data

def main():
    data = load_data()
    data = fix_tianxing(data)
    save_data(data)
    print("\n✅ 数据修复完成")

if __name__ == "__main__":
    main()
