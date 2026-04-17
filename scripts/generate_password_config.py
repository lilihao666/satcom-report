#!/usr/bin/env python3
"""
将100个密码批量添加到付费版HTML的密码配置中
生成一个包含所有密码的JS配置文件
"""

passwords = [
    'a8Kj2mP9xQ', 'b7Lm3nR8wE', 'c5Np4qT7yU', 'd3Qr5sV6zI', 'e9Tu7vX2aO',
    'f2Wx4yB8cD', 'g6Yz3dF5hG', 'h4Jk7lM9nP', 'i8Qm2rS4tU', 'j3Vw5xY7zA',
    'k9Bc2dE4fG', 'l5Hj7kL9mN', 'm3Pq4rS6tU', 'n7Wx8yZ2aB', 'o4Cd6eF8gH',
    'p2Jk3lM5nP', 'q8Qr9sT2uV', 'r5Yx6zA3bC', 's9De2fG4hJ', 't4Kk5lM7nQ',
    'u2Ps3qR6sT', 'v8Uy9xZ4aB', 'w6Cd7eF9gH', 'x3Jk4lM6nP', 'y9Qr7sT2uV',
    'z5Yx8zA4bC', 'A2De3fG5hJ', 'B8Kk9lM2nQ', 'C5Ps6qR8sT', 'D3Uy4xZ7aB',
    'E9Cd2eF4gH', 'F6Jk7lM9nP', 'G4Qr5sT8uV', 'H2Yx3zA6bC', 'I8De9fG2hJ',
    'J5Kk6lM8nQ', 'K3Ps4qR7sT', 'L9Uy2xZ5aB', 'M6Cd7eF3gH', 'N4Jk5lM8nP',
    'O2Qr6sT9uV', 'P9Yx3zA5bC', 'Q7De8fG2hJ', 'R4Kk5lM7nQ', 'S2Ps3qR6sT',
    'T8Uy9xZ4aB', 'U5Cd6eF8gH', 'V3Jk4lM7nP', 'W9Qr7sT2uV', 'X6Yx8zA4bC',
    'Y4De2fG5hJ', 'Z2Kk9lM3nQ', 'a9Ps6qR8sT', 'b7Uy3xZ5aB', 'c4Cd8eF2gH',
    'd2Jk5lM9nP', 'e9Qr4sT7uV', 'f6Yx2zA8bC', 'g3De9fG5hJ', 'h8Kk7lM4nQ',
    'i5Ps3qR9sT', 'j2Uy6xZ7aB', 'k9Cd4eF8gH', 'l7Jk2lM5nP', 'm4Qr8sT3uV',
    'n2Yx5zA9bC', 'o8De7fG4hJ', 'p5Kk3lM9nQ', 'q3Ps7qR2sT', 'r9Uy4xZ8aB',
    's6Cd9eF3gH', 't4Jk8lM6nP', 'u2Qr5sT9uV', 'v9Yx7zA5bC', 'w6De3fG8hJ',
    'x4Kk9lM2nQ', 'y2Ps6qR7sT', 'z8Uy5xZ3aB', 'A5Cd2eF9gH', 'B3Jk7lM6nP',
    'C9Qr4sT8uV', 'D7Yx2zA5bC', 'E4De8fG3hJ', 'F2Kk6lM9nQ', 'G9Ps3qR7sT',
    'H6Uy8xZ4aB', 'I4Cd5eF2gH', 'J2Jk9lM7nP', 'K9Qr6sT3uV', 'L7Yx4zA8bC',
    'M5De2fG9hJ', 'N3Kk8lM6nQ', 'O2Ps5qR9sT', 'P9Uy7xZ4aB', 'Q6Cd3eF8gH',
    'R4Jk9lM5nP', 'S2Qr7sT3uV', 'T9Yx5zA6bC', 'U7De4fG2hJ', 'V5Kk3lM8nQ'
]

print("// 付费版密码配置 - 100个预设密码")
print("// 有效期30天，从首次使用开始计算")
print("const PASSWORD_CONFIG = {")
print("    // 永久密码（管理员+测试）")
print("    'DIAOYAN2025': { tier: '调研版', level: 1, expiry: null },")
print("    'ADMIN2025': { tier: '管理员', level: 3, expiry: null },")
print("")
print("    // 批量生成密码（100个）")

for i, pwd in enumerate(passwords, 1):
    comma = "," if i < len(passwords) else ""
    print(f"    '{pwd}': {{ tier: '调研版', level: 1, expiry: null }}{comma}")

print("};")
print("")
print(f"// 总计: {len(passwords)} 个用户密码 + 2 个永久密码")
