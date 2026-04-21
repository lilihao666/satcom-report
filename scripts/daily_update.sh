#!/bin/bash
# 本地每日更新脚本
# 每天早上8点运行

set -e

cd /root/.openclaw/workspace/satcom-research-github

LOG_FILE="logs/daily_update_$(date +%Y%m%d).log"
mkdir -p logs

echo "========================================" >> "$LOG_FILE"
echo "Daily Update: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# 1. 拉取最新代码
echo "[1/5] Pulling latest code..." >> "$LOG_FILE"
git pull origin main >> "$LOG_FILE" 2>&1 || true

# 2. 运行新闻抓取
echo "[2/5] Fetching latest news..." >> "$LOG_FILE"
python3 scripts/news_fetcher.py >> "$LOG_FILE" 2>&1

# 3. 生成免费版报告
echo "[3/5] Generating free report..." >> "$LOG_FILE"
python3 scripts/generate_report_v4.py generate >> "$LOG_FILE" 2>&1

# 4. 生成付费版报告
echo "[4/5] Generating premium report..." >> "$LOG_FILE"
python3 scripts/generate_premium.py generate >> "$LOG_FILE" 2>&1

# 5. 更新日期戳
echo "[5/5] Updating timestamp..." >> "$LOG_FILE"
DATE=$(date +%Y-%m-%d)
python3 -c "
import json
with open('data/satcom_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['last_updated'] = '$DATE'
with open('data/satcom_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('Updated last_updated to', '$DATE')
" >> "$LOG_FILE" 2>&1

# 6. 提交并推送
echo "[6/6] Committing and pushing..." >> "$LOG_FILE"
git add -A
git diff --cached --quiet || git commit -m "Auto update: $DATE - refresh news and reports"
git push origin main >> "$LOG_FILE" 2>&1

echo "Update completed at $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
