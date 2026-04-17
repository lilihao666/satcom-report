#!/usr/bin/env python3
"""
生成100个付费版访问密码
"""
import random
import string

def generate_password(length=10):
    """生成随机密码：字母+数字，避免易混淆字符"""
    # 排除易混淆字符：0, O, 1, I, l
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'
    return ''.join(random.choice(chars) for _ in range(length))

# 生成100个唯一密码
passwords = set()
while len(passwords) < 100:
    passwords.add(generate_password(10))

passwords = sorted(list(passwords))

# 输出格式
print("# 卫星通信调研报告 - 付费版访问密码列表")
print(f"# 生成时间: 2026-04-17")
print(f"# 有效期: 30天")
print(f"# 总计: {len(passwords)} 个密码\n")

print("| 序号 | 访问密码 | 状态 |")
print("|------|----------|------|")

for i, pwd in enumerate(passwords, 1):
    print(f"| {i:3d} | `{pwd}` | 未使用 |")

print("\n## 使用说明")
print("1. 用户付款后，从列表中分配一个密码")
print("2. 在 `premium/index.html` 的 `PASSWORDS` 配置中添加新密码")
print("3. 更新状态为'已分配'，记录分配时间和用户信息")
