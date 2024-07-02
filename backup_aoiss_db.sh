#!/bin/bash
cur_time=$(date +%Y%m%d_%H_%M_%S)
mkdir -p /var/AOI-ST/sdd/aoiss_local_db_backup
/usr/pgsql-10/bin/pg_dump "host=127.0.0.1 port=5432 user=postgres password=1234qwer\!\@\#\$QWER dbname=aoiss" -f /var/AOI-ST/sdd/aoiss_local_db_backup/aoiss_backup_$cur_time.dmp
tar zcPf "/var/AOI-ST/sdd/aoiss_local_db_backup/aoiss-backup.$cur_time.tar.gz" /var/AOI-ST/sdd/aoiss_local_db_backup/*.dmp
rm -rf /var/AOI-ST/sdd/aoiss_local_db_backup/aoiss_backup*.dmp
find /var/AOI-ST/sdd/aoiss_local_db_backup/ -mtime +16 -name "aoiss-backup*" -exec rm -rf {} \;
echo "backup finished"