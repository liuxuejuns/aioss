#!/bin/bash
cur_time=$(date +%Y%m%d_%H_%M_%S)
mkdir -p /aoiss/media/sdd/aoiss_local_db_backup
pg_dump "host=127.0.0.1 port=5432 user=postgres password=1234qwer\!\@\#\$QWER dbname=aoiss" | gzip -c > /aoiss/media/sdd/aoiss_local_db_backup/aoiss-backup_$cur_time.gz
find /aoiss/media/sdd/aoiss_local_db_backup/ -mtime +16 -name "aoiss-backup*" -exec rm -rf {} \;
echo "backup finished"