#!/bin/bash
# Database backup script — runs via crontab at 03:00 daily
# 0 3 * * * /home/linscio/scripts/backup_db.sh >> /home/linscio/logs/backup.log 2>&1

set -e

DATE=$(date +%Y%m%d)
BACKUP_DIR="/home/linscio/backups"
BACKUP_FILE="$BACKUP_DIR/mysql-$DATE.sql"

# 1. Dump database
mysqldump -u linscio -p"$DB_PASSWORD" linscio_db > "$BACKUP_FILE"

# 2. Compress
gzip "$BACKUP_FILE"

# 3. Upload to COS (using coscmd or Python SDK)
cd /home/linscio/api
source venv/bin/activate
python -c "
from app.services.cos import upload_backup
upload_backup('$BACKUP_FILE.gz', 'backups/mysql-$DATE.sql.gz')
print('Uploaded to COS: backups/mysql-$DATE.sql.gz')
"

# 4. Clean up local backups older than 30 days
find "$BACKUP_DIR" -name "mysql-*.sql.gz" -mtime +30 -delete

echo "[$DATE] Backup completed successfully"
