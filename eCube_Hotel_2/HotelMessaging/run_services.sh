#!/usr/bin/env bash
#source /home/tech/crawling_services/bin/activate


cd AetosCrawlingService
nohup python start_request_scheduler.py >/dev/null 2>&1 &
nohup python start_producer.py >/dev/null 2>&1 &

nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &

nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &

nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &

nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &

nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &

nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &
nohup python start_recrawl.py >/dev/null 2>&1 &


cd ../AetosParsingService
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_producer.py >/dev/null 2>&1 &
nohup python start_reparse.py >/dev/null 2>&1 &


cd ../AetosReportingService
nohup python start_watcher.py >/dev/null 2>&1 &
nohup python start_producer.py >/dev/null 2>&1 &
nohup python start_consumer.py >/dev/null 2>&1 &
nohup python start_hotel_addition.py >/dev/null 2>&1 &
