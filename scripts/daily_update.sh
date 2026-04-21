#!/bin/bash
# Daily Update Script - Fixed Version
# This script updates satellite communication research data and generates reports
# Runs at 8:00 AM daily via cron

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_DIR/data"
LOGS_DIR="$PROJECT_DIR/logs"
TEMPLATES_DIR="$PROJECT_DIR/templates"
REPORTS_DIR="$PROJECT_DIR/reports"

# Create necessary directories
mkdir -p "$LOGS_DIR"
mkdir -p "$REPORTS_DIR"

echo "=================================="
echo "Daily Update Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================="

# Step 1: Update last_updated date in data file
echo "[1/4] Updating data timestamp..."
cd "$PROJECT_DIR"
python3 -c "
import json
from datetime import datetime
with open('data/satcom_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
with open('data/satcom_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'Updated timestamp: {data[\"last_updated\"]}')
"

# Step 2: Fetch news (if requests library is available)
echo "[2/4] Fetching latest news..."
if python3 -c "import requests" 2>/dev/null; then
    python3 "$SCRIPT_DIR/news_fetcher.py" --force-simulated || true
else
    echo "Warning: requests library not installed. Skipping news fetch."
    echo "Install with: pip install requests feedparser"
    python3 "$SCRIPT_DIR/news_fetcher.py" --update-date-only
fi

# Step 3: Generate free report
echo "[3/4] Generating free report..."
python3 "$SCRIPT_DIR/generate_report_v4.py" generate

# Step 4: Generate premium report
echo "[4/4] Generating premium report..."
python3 "$SCRIPT_DIR/generate_premium.py" generate

# Step 5: Git operations (if git is available and configured)
echo "[5/5] Syncing with GitHub..."
cd "$PROJECT_DIR"

if [ -d .git ]; then
    git add -A || true
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        echo "No changes to commit"
    else
        git commit -m "Daily update: $(date '+%Y-%m-%d')" || true
        
        # Try to push (may fail if no remote configured)
        git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "Note: Git push skipped (no remote or auth issues)"
    fi
else
    echo "Warning: Not a git repository. Skipping git operations."
    echo "To enable auto-sync, initialize git: cd $PROJECT_DIR && git init && git remote add origin <your-repo-url>"
fi

echo "=================================="
echo "Daily Update Completed: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=================================="
echo ""
echo "Report URLs:"
echo "  Free:    https://lilicoder.github.io/satcom-research/"
echo "  Premium: https://lilicoder.github.io/satcom-research/premium.html"
echo ""
