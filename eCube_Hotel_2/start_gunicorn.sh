#!/usr/bin/env bash
cd
cd /var/www/
source ui_env/bin/activate
cd eCube_Hotel_2/Services/

echo "Starting HTMLProcess"
nohup gunicorn HTMLProcess.HTMLProcessService:app --bind=0.0.0.0:8001 --timeout=1200 >/dev/null 2>&1 &

cd mongo_api
echo "Starting Mongo API"
nohup gunicorn routes:app --bind=0.0.0.0:8002 --timeout=1200 >/dev/null 2>&1 &

cd ../proxy_service
echo "Starting Proxy Service"
# nohup gunicorn routes:app --bind=0.0.0.0:8003 --timeout=1200 >/dev/null 2>&1 &

cd ../mail_lib
echo "Starting Mail Service"
nohup gunicorn routes:app --bind=0.0.0.0:8004 --timeout=1200 >/dev/null 2>&1 &

cd ../cache_page
echo "Starting Cache Page"
nohup gunicorn routes:app --bind=0.0.0.0:8005 --timeout=1200 >/dev/null 2>&1 &

echo "All gunicorn services running successfully"

