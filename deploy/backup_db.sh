#!/bin/bash
# Database backup script — runs via crontab at 03:00 daily
# 0 3 * * * /www/wwwroot/linscio-portal/deploy/backup_db.sh >> /www/wwwroot/linscio-release/logs/backup.log 2>&1

set -euo pipefail

DATE=$(date +%Y%m%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
BACKUP_DIR="/www/wwwroot/linscio-release/backups"
BACKUP_FILE="$BACKUP_DIR/mysql-$DATE.sql"
BACKUP_GZ="$BACKUP_FILE.gz"
COS_KEY="backups/mysql-$DATE.sql.gz"
API_DIR="/www/wwwroot/linscio-portal/api"

mkdir -p "$BACKUP_DIR"

send_result() {
    local success=$1
    local error_msg="${2:-}"
    cd "$API_DIR"
    source venv/bin/activate
    python -c "
import asyncio
from app.services.email import send_backup_result
asyncio.run(send_backup_result(
    success=$success,
    filename='$COS_KEY',
    timestamp='$TIMESTAMP',
    error_message='$error_msg',
))
"
}

# 1. Dump database
if ! mysqldump -u linscio -p"$DB_PASSWORD" linscio_db > "$BACKUP_FILE"; then
    send_result "False" "mysqldump failed"
    exit 1
fi

# 2. Compress
gzip "$BACKUP_FILE"

# 3. Upload to COS
cd "$API_DIR"
source venv/bin/activate
if ! python -c "
from app.services.cos import upload_backup
upload_backup('$BACKUP_GZ', '$COS_KEY')
print('Uploaded to COS: $COS_KEY')
"; then
    send_result "False" "COS upload failed"
    exit 1
fi

# 4. Clean up local backups older than 30 days
find "$BACKUP_DIR" -name "mysql-*.sql.gz" -mtime +30 -delete

# 5. Send success notification
send_result "True"

echo "[$DATE] Backup completed successfully"
