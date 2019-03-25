import logging 
from logging.handlers import TimedRotatingFileHandler
import os


logger=logging.getLogger('ServicesLog')
logging.captureWarnings(True)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler=TimedRotatingFileHandler(filename=os.path.join('logs','ServiceLogs.txt'),when='H',interval=1)
handler.setFormatter(formatter)
logger.addHandler(handler)
