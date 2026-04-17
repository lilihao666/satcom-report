#!/bin/bash
cd /root/.openclaw/workspace/satcom-research-github

# 生成免费版
python3 scripts/generate_report_v4.py

# 生成付费版
python3 scripts/generate_premium.py

# 提交到GitHub
git add -A
git commit -m "🛰️ 数据更新：国星宇航发射情况+AROGOS去重

- 国星宇航：已发射12颗卫星（星算计划01组，2025年5月14日发射）
- AROGOS：删除重复条目，保留一个规划中状态
- 同步更新免费版和付费版"
git push origin main

echo "✅ 报告已更新并推送"
