#!/bin/bash
# 卫星通信调研报告每日自动更新脚本
# 建议添加到crontab: 0 8 * * * /root/.openclaw/workspace/satcom-research/scripts/daily_update.sh

cd /root/.openclaw/workspace/satcom-research

# 记录日志
LOG_FILE="logs/update_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "=== 卫星通信报告自动更新 $(date) ===" | tee -a "$LOG_FILE"

# 激活Python环境（如果有的话）
# source /path/to/venv/bin/activate

# 执行完整更新
echo "[1/3] 更新数据..." | tee -a "$LOG_FILE"
python3 scripts/generate_report.py update 2>&1 | tee -a "$LOG_FILE"

echo "[2/3] 生成报告..." | tee -a "$LOG_FILE"
python3 scripts/generate_report.py generate 2>&1 | tee -a "$LOG_FILE"

echo "[3/3] 清理旧报告（保留最近30天）..." | tee -a "$LOG_FILE"
find reports -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true

echo "✅ 更新完成: $(date)" | tee -a "$LOG_FILE"

# 可选：发送通知
# python3 scripts/send_notification.py "报告已更新"
