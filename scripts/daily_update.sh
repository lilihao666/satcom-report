#!/bin/bash
# 卫星通信调研报告每日自动更新
# 配置：0 8 * * * /root/.openclaw/workspace/satcom-research-github/scripts/daily_update.sh

cd /root/.openclaw/workspace/satcom-research-github

LOG_FILE="logs/update_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "=== 卫星通信报告自动更新 $(date) ===" | tee -a "$LOG_FILE"

# 更新数据日期
sed -i "s/\"last_updated\": \"[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\"/\"last_updated\": \"$(date +%Y-%m-%d)\"/" data/satcom_data.json

# 重新生成报告
echo "[1/2] 生成免费版报告..." | tee -a "$LOG_FILE"
python3 scripts/generate_report_v4.py 2>&1 | tee -a "$LOG_FILE"

echo "[2/2] 生成付费版报告..." | tee -a "$LOG_FILE"
python3 scripts/generate_premium.py 2>&1 | tee -a "$LOG_FILE"

echo "✅ 更新完成: $(date)" | tee -a "$LOG_FILE"

# Git提交
git add -A
git commit -m "📊 自动更新 $(date +%Y-%m-%d)" || true
git push origin main 2>&1 | tee -a "$LOG_FILE"
