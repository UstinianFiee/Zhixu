#!/bin/bash

echo "等待数据库就绪..."
MAX_RETRIES=60
RETRY_COUNT=0

while ! python -c "
import pymysql, os, sys
url = os.environ.get('DATABASE_URL', '')
# mysql+pymysql://user:pass@host:port/db
try:
    parts = url.replace('mysql+pymysql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    host_port = host_db[0].split(':')
    conn = pymysql.connect(
        host=host_port[0],
        port=int(host_port[1]) if len(host_port) > 1 else 3306,
        user=user_pass[0],
        password=user_pass[1],
        database=host_db[1] if len(host_db) > 1 else None,
        connect_timeout=5,
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f'  -> {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "数据库连接超时 ($MAX_RETRIES 次尝试)，退出"
        exit 1
    fi
    echo "数据库未就绪，等待中... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 3
done

echo "数据库连接成功，初始化数据..."
python -m app.seed

echo "启动服务..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8888
