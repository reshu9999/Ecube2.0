import logging 
from logging.handlers import TimedRotatingFileHandler
import os

logger=logging.getLogger('CrawlLog')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler=TimedRotatingFileHandler(filename=os.path.join('CrawlLogs','Crawlogs.txt'),when='H',interval=1,backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)
