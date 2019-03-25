import pika
import json
import copy
import random
import requests
import datetime

from queues.executor import ScriptHandler
from queues.connections import MySQLConnection

from resources.logs import TimedRotatedLoggerBase

from scripts.core import services as core_services
from scripts.core import exceptions as core_exceptions


class QueueLogger(TimedRotatedLoggerBase):

    NAME = 'crawler_queue'
    INTERVAL = 2
    INTERVAL_TYPE = 'H'
    BACKUP_COUNT = 12
    LOG_PATH = 'logs'
    ALLOWED_LEVELS = {
        'INFO': 'info',
        'DEBUG': 'debug',
        'WARNING': 'warning',
        'ERROR': 'error',
    }

    @classmethod
    def _get_log_message(cls, message, r_id=None, sr_id=None, rd_id=None):
        msg_meta = list()
        if r_id:
            msg_meta.append('|R:')
            msg_meta.append(r_id)
        if sr_id:
            msg_meta.append('|SR:')
            msg_meta.append(sr_id)
        if rd_id:
            msg_meta.append('|RD:')
            msg_meta.append(rd_id)
        return "".join([str(m) for m in msg_meta]) + '| ' + message

    @classmethod
    def _make_log(cls, level, message, r_id=None, sr_id=None, rd_id=None):
        logger = cls.get_logger()
        log_writer = getattr(logger, cls.ALLOWED_LEVELS[level])
        log_writer(cls._get_log_message(message, r_id, sr_id, rd_id))

    @classmethod
    def info_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('INFO', message, r_id, sr_id, rd_id)

    @classmethod
    def debug_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('DEBUG', message, r_id, sr_id, rd_id)

    @classmethod
    def warning_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('WARNING', message, r_id, sr_id, rd_id)

    @classmethod
    def error_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('ERROR', message, r_id, sr_id, rd_id)


QueueLogger.set_logger()


class BaseCallback(object):

    LOGGER = QueueLogger
    MYSQL_CONN = MySQLConnection

    def __init__(self, channel, method, properties, body, redelivered=None):
        """
        :param channel:
        :param method:
        :param properties:
        :param body:
        """
        self.channel = channel
        self.method = method
        self.properties = properties
        self.redelivered = redelivered if redelivered is not None else self.method.redelivered
        self.body = body

        self._data = None
        self.processed_data = None

        self.request_id = None
        self.sub_request_id = None
        self.request_run_id = None

        self._error = None
        self._error_code = None
        self._error_message = None

    def _make_debug_log(self, message):
        print(message)
        self.LOGGER.debug_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    def _make_error_log(self, message):
        self._make_debug_log('[ERROR]' + message)
        self.LOGGER.error_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    def _make_info_log(self, message):
        self._make_error_log('[INFO]' + message)
        self.LOGGER.info_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    @property
    def _get_status(self):
        connection = self.MYSQL_CONN()
        cursor = connection.get_cursor
        cursor.execute("SELECT FK_StatusId FROM tbl_RequestRunDetail WHERE RequestRunId = %s" % self.request_run_id)
        status = cursor.fetchall()
        return status[0][0]

    @property
    def _paused(self):
        # return False
        return int(self._get_status) == 7

    @property
    def _stopped(self):
        # return False
        return int(self._get_status) == 6

    @property
    def _get_process_data(self):
        if self._data is not None:
            return self._data
        try:
            self._data = json.loads(self.body.decode('utf-8').replace("'", "\""))
        except Exception as e:
            self._data = eval(self.body.decode('utf-8'))
        return self._get_process_data

    def prep_process_data(self):
        process_data = self._get_process_data
        self.request_id = process_data['requestId']
        self.sub_request_id = process_data['subRequestId']
        self.request_run_id = process_data['requestRunId']

    def _execute_script(self):
        raise NotImplementedError

    def _set_error(self, error_code, error_message):
        # TODO: make checks for only allowed error_codes and corresponding _process_<error_code>_error functions
        self._error = True
        self._error_code = error_code
        self._error_message = error_message
        self._make_error_log("Setting Error Code:'%s' with Error Msg:'%s'" % (self._error_code, self._error_message))

    def _process_error(self):
        self._make_info_log("Processing Error Code:'%s' with Error Msg:'%s'" % (self._error_code, self._error_message))
        getattr(self, '_process_%s_error' % self._error_code)()

    def _process_paused(self):
        raise NotImplementedError

    def _process_stopped(self):
        raise NotImplementedError

    def _process_success(self):
        raise NotImplementedError

    def consume(self):
        self.prep_process_data()
        self._make_info_log("Method:%s" % self.method)
        self._make_info_log("Properties:%s" % self.properties)
        self._make_debug_log("Receiving Messages:%r" % self.body)
        self._make_info_log("Consumer Start Time:%s" % datetime.datetime.now())

        self.channel.basic_ack(delivery_tag=self.method.delivery_tag)

        if self._paused:
            self._process_paused()
        elif self._stopped:
            self._process_stopped()
        else:
            self._execute_script()

            if self._error:
                self._process_error()
            else:
                self._process_success()


class Callback(BaseCallback):

    def _process_empty_hotels_error(self):
        core_services.MongoHandler().save_pnf(self.processed_data, self._error_message)
        pnf_update_query = "UPDATE tbl_HotelCrawlRequestDetail SET StatusId = 8 WHERE HotelCrawlRequestDetailId = %s AND StatusId = 11"
        conn = MySQLConnection()
        cur = conn.get_cursor
        cur.execute(pnf_update_query % self.processed_data['subRequestId'])
        conn.connection.commit()
        conn.clean_connections()

    def _process_proxy_service_dead_error(self):
        self._process_empty_hotels_error()

    def _process_script_timeout_error(self):
        self._make_error_log("Script Timeout")
        connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel2 = connection2.channel()
        channel2.queue_declare("Recrawl")
        channel2.basic_publish(exchange='', routing_key='Recrawl', body=json.dumps(self.processed_data))
        connection2.close()

    def _process_success(self):
        self._make_info_log("GREAT SUCCESS with '%s' Hotels" % len(self.processed_data['hotels']))
        core_services.MongoHandler().save_successful_crawl(self.processed_data)
        core_services.MongoHandler().mark_hotels_to_be_parsed(self.processed_data)
        processed_data = copy.deepcopy(self.processed_data)
        hotels = processed_data.pop('hotels')

        connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel2 = connection2.channel()
        channel2.queue_declare("Parser")

        for hotel in hotels:
            parser_data = copy.deepcopy(processed_data)
            parser_data['hotel'] = hotel
            # channel2.basic_publish(exchange='', routing_key='Parser', body=json.dumps(self.processed_data))

            channel2.basic_publish(exchange='', routing_key='Parser', body=json.dumps(parser_data))
        connection2.close()

    @property
    def _get_processed_data(self):
        raise NotImplementedError

    def _execute_script(self):
        # self.processed_data = self._get_processed_data
        try:
            self._make_info_log("Executing Script")
            self.processed_data = self._get_processed_data
        except core_exceptions.ScriptPNF as e:
            self._set_error('empty_hotels', 'hotel cannot be parsed')
            self.processed_data = self._get_process_data.copy()
        except core_exceptions.ScriptTimeout as e:
            self._set_error('script_timeout', 'website blocked access')
            self.processed_data = self._get_process_data.copy()
        except core_exceptions.ProxyServiceNotWorking as e:
            self._set_error('proxy_service_dead', str(e))
            self.processed_data = self._get_process_data.copy()

        crawled_hotel_count = len(self.processed_data.get('hotels', list()))
        self._make_info_log("Hotels Found:%s" % str(crawled_hotel_count))
        if not crawled_hotel_count and not self._error:
            self._set_error('empty_hotels', 'no hotels found')

    def _process_paused(self):
        self._make_info_log("Paused Request Bypassed")

    def _process_stopped(self):
        self._make_info_log("Stopped Request Bypassed")


class NormalCallback(Callback):

    @property
    def _get_processed_data(self):
        return ScriptHandler(self._get_process_data).execute_crawl(False)


class ScriptTimeoutCallback(Callback):

    @property
    def _get_processed_data(self):
        return ScriptHandler(self._get_process_data).execute_crawl(True)


class RequestScheduler(object):

    MYSQL_CONNECTION = MySQLConnection

    def __init__(self, cutoff_time=None):
        self.cutoff_time = cutoff_time or datetime.datetime.now()

    @property
    def _get_schedule_data(self):
        mysql_connection = self.MYSQL_CONNECTION()
        cur = mysql_connection.get_cursor
        cur.execute(
            """
            SELECT ScheduleDatesId, SD_RequestId, scheduleDate, scheduleTime, Status
            FROM tbl_ScheduleDate SD
            WHERE date_format(scheduleDate, '%Y-%m-%d') = curdate() AND scheduleTime < curtime() AND Status='Pending'
            """
        )
        res = cur.fetchall()
        mysql_connection.clean_connections()
        return res

    def make_request_run_details(self):
        mysql_connection = self.MYSQL_CONNECTION()
        for row in self._get_schedule_data:
            schedule_id = str(row[0])
            request_id = str(row[1])
            print("row[0], row[1], row[2], row[3], row[4]")
            print(row[0], row[1], row[2], row[3], row[4])
            # if str(self.cutoff_time.time().strftime("%H:%M")) == t[0:5]:
            req_run_cursor = mysql_connection.get_cursor
            req_run_cursor.callproc('sp_SaveRequestRunDetail', [int(request_id), 2, schedule_id])
            mysql_connection.connection.commit()
            cur = mysql_connection.get_cursor
            cur.execute(
                """
                select RequestId ,RequestName, CreatedBy, UserName,EmailID from tbl_RequestMaster as r 
                inner join tbl_UserMaster  as u  on r.CreatedBy = u.UserId where  RequestId = """+request_id+""" ; 
                """
            )
            sp_res = cur.fetchall()
            cur.close()

            body = '''
            
                
                <style type="text/css">
                p.MsoNormal, li.MsoNormal, div.MsoNormal  {
                    margin: 0in;
                margin:bottom:.0001pt;
                font:size:11.0pt;
                font:family:"Verdana", "sans:serif";
                }
                a:link, span.MsoHyperlink  {
                mso:style:priority:99;
                color:blue;
                text:decoration:underline;
                }
                a:visited, span.MsoHyperlinkFollowed  {
                mso:style:priority:99;
                color:purple;
                text:decoration:underline;
                }
                span.EmailStyle17  {
                mso:style:type:personal;
                font:family:"Verdana", "sans:serif";
                color:windowtext;
                }
                span.EmailStyle18  {
                mso:style:type:personal:reply;
                font:family:"Verdana", "sans:serif";
                color:#1F497D;
                }
                .MsoChpDefault  {
                mso:style:type:export:only;
                font:size:10.0pt;
                }
                @page Section1  {
                    size: 8.5in 11.0in;
                margin:1.0in 1.0in 1.0in 1.0in;
                }
                div.Section1  {
                    page: Section1;
                }
                table  {
                border:collapse:collapse;
                width :800px;
                
                }
                table, td, th  {
                border:1px solid black;
                
                }
                
                </style>
                
                <div style="font-family: verdana; font-size:12px; line-height: 18px;"> 
                <p style="font-family: verdana; ">    Dear User,   <br><br>  Following request has been initiated  </p> 
                    
                    <br>
                    <table width="60%" border="0" cellspacing="0" cellpadding="10" style="border-collapse: collapse; border:1px solid #999; font-size: 12px; text-align: left;">
                <tbody>
                    <tr>
            <th style="background:#365f91; color: #fff; text-align: left;"> Request Id  </th>
                    <th style="background:#365f91; color: #fff; text-align: left;"> Request Name </th>
                    <th style="background:#365f91; color: #fff; text-align: left;"> User Name </th>
                    </tr>
                    <tr>
                    <td> '''+str(sp_res[0][0])+'''  </td>
                    <td> '''+str(sp_res[0][1])+'''  </td>
                    <td> '''+str(sp_res[0][3])+'''   </td>
                    </tr>
                </tbody>
                </table>
                
                <br>
                        <p>          Regards,<br>
                        PricingTech<br>
                        <br><br>
                        This message including attachment(s) is intended only for the personal and confidential use of the recipient(s) named above.This communication is for          informational purposes only.Email transmission cannot be guaranteed to be secure or error:free. All information is subject to change without notice.          If you are not the intended recipient of this message you are hereby notified that any review,dissemination,distribution or copying of this message          is strictly prohibited. If you are not the intended recipient,         please contact:<a href="mailto:helpdesk@eclerx.com" style="color: #0000ff;">helpdesk@eclerx.com</a></p>
                        
                
                <p>  <font size="2pt" color="black" family="Tahoma"><strong> eClerx :An ISO/IEC 27001:2005 Certified Organization</strong></font>  </p>
                </div>
            '''

            dict1 = {"cc": "PricingTech@eclerx.com", "to": sp_res[0][4], "bcc": "PricingTech@eclerx.com", "body": body,
                     "subject": "eCube 2.0 - Request ("+str(sp_res[0][1])+") Initiated   ", "has_attachments": False}
            mail_args = json.dumps(dict1)
            requests.post('http://192.168.8.20/mail/api/v1/send_email/', data=mail_args)
        mysql_connection.clean_connections()


class DataKey(object):

    def __init__(self, key, value, return_func):
        self._key = key
        self._val = value
        self._func = getattr(self, 'get_' + return_func)

    @staticmethod
    def get_int(value):
        return int(value)

    @staticmethod
    def get_float(value):
        return float(value)

    @staticmethod
    def get_string(value):
        return str(value)

    @staticmethod
    def get_first_object(value):
        if not isinstance(value, list):
            value = [value]
        return value[0]

    @staticmethod
    def get_empty_string(value):
        return str(value) if value else ''

    @staticmethod
    def get_random_int(value):
        return str(random.randint(1 * int(value), 10 * int(value) - 1))

    @staticmethod
    def get_None(value):
        return value if bool(value) else None

    @property
    def get_value(self):
        return self._func(self._val)

    def update_sample(self, sample):
        sample_deep_dict = sample
        if '.' in self._key:
            keys = self._key.split('.')
            for key in keys[:-1]:
                sample_deep_dict = sample_deep_dict[key]
            sample_deep_dict[keys[-1]] = self.get_value
        else:
            sample_deep_dict[self._key] = self.get_value
        return sample


class ScriptDataMaker(object):
    SAMPLE = {
        "requestId": "1",
        "subRequestId": "1",
        "requestRunId": "1",
        "domainName": "https://www.travelrepublic.co.uk",
        "ParserScript": "ParserTravelRepublicPython",
        "ScraperScript": "ScrapperTravelRepublicPython",
        "country": "India",
        "DomainName": "Travel",
        "PointOfSale": "",
        "call_func": "crawl_hotels",
        "RequestInputs": {
            "city": "Mumbai",
            "children": 0,
            "adults": 2,
            "room": "",
            "board": "",
            "checkIn": str(datetime.datetime.now()).split(' ')[0],
            "nights": 3,
            "days": 7,
            "hotelName": "",
            "starRating": "",
            "webSiteHotelId": "",
            "pos": "United Kingdom",
            "competitorId": 5,
            "crawlMode": ""
        }
    }
    DATA_DICT = {
        'HRS': {
            'inputs': [
                DataKey('requestId', 10000, 'random_int'),
                DataKey('subRequestId', 100000000, 'random_int'),
                DataKey('requestRunId', 1000000, 'random_int'),

                DataKey('domainName', 'https://www.hrs.com/web3/', 'string'),
                DataKey('ParserScript', 'ParserHRSPython', 'string'),
                DataKey('ScraperScript', 'ScrapperHRSPython', 'string'),
                DataKey('country', 'GERMANY', 'string'),
                DataKey('DomainName', 'HRS', 'string'),
                DataKey('RequestInputs.city', 'BERLIN', 'string'),
                DataKey('RequestInputs.children', 0, 'int'),
                DataKey('RequestInputs.adults', 2, 'int'),
            ]
        },
        'Starwood': {
            'inputs': [
                DataKey('requestId', 10000, 'random_int'),
                DataKey('subRequestId', 100000000, 'random_int'),
                DataKey('requestRunId', 1000000, 'random_int'),

                DataKey('domainName', 'http://www.starwood.com', 'string'),
                DataKey('ParserScript', 'ParserStarwoodPython', 'string'),
                DataKey('ScraperScript', 'ScrapperStarwoodPython', 'string'),
                DataKey('country', 'France', 'string'),
                DataKey('DomainName', 'Starwood', 'string'),
                DataKey('RequestInputs.city', 'Paris', 'string'),
                DataKey('RequestInputs.children', 0, 'int'),
                DataKey('RequestInputs.adults', 2, 'int'),
            ]
        },
        'Travel': {
            'inputs': [
                DataKey('requestId', 10000, 'random_int'),
                DataKey('subRequestId', 100000000, 'random_int'),
                DataKey('requestRunId', 1000000, 'random_int'),

                DataKey('domainName', 'https://www.travelrepublic.co.uk', 'string'),
                DataKey('ParserScript', 'ParserTravelRepublicPython', 'string'),
                DataKey('ScraperScript', 'ScrapperTravelRepublicPython', 'string'),
                DataKey('country', 'India', 'string'),
                DataKey('DomainName', 'Travel', 'string'),
                DataKey('RequestInputs.city', 'Mumbai', 'string'),
                DataKey('RequestInputs.children', 0, 'int'),
                DataKey('RequestInputs.adults', 2, 'int'),
            ]
        }
    }
    ALLOWED_KEYS = ['domainName', 'ParserScript', 'ScraperScript', 'country', 'DomainName', 'RequestInputs.city',
                    'RequestInputs.children', 'RequestInputs.adults']

    def __init__(self, script_tag):
        self._tag = script_tag

    @property
    def _data_keys(self):
        return self.DATA_DICT[self._tag]['inputs'] if self.DATA_DICT else list()

    @property
    def script_data(self):
        script_data = copy.deepcopy(self.SAMPLE)

        for data_key in self._data_keys:
            data_key.update_sample(script_data)

        return script_data
