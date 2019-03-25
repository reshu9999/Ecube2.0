import schedule

from queues.producer import ReportQueue, TestingReportQueue, AetosReportQueue


schedule.every(0.5).minutes.do(ReportQueue)
# schedule.every(0.5).minutes.do(TestingReportQueue)
while True:
    schedule.run_pending()

# ReportQueue()
# TestingReportQueue()
# AetosReportQueue()
