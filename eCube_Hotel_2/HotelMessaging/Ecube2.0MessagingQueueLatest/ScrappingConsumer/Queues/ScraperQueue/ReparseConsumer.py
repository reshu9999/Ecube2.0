import pika
import json

from Queues.ScraperQueue.executor import ScriptHandler
from Queues.ScraperQueue import DynamicCommonConnection
from Queues.ScraperQueue.core import services as core_services
from Queues.ScraperQueue.ScriptExecutor import ScriptsExecution
from Queues.ScraperQueue.core import exceptions as core_exceptions


class ReparseConsumer(object):

    @classmethod
    def get_channel(cls):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    def callback(ch, method, properties, body):

        # print("Method Name --------------", method)
        # print("Properties Name ----------", properties)

        '''
        :param ch:   connection channel
        :param method:  method name
        :param properties: priority Properties
        :param body:  message
        :return:
        '''


        # print("Receiving Messages ------------ %r" % body)
        # print("Consumer running Time", datetime.datetime.now())

        try:
            data = body.decode('utf-8')
            consume_data = data.replace("'", "\"")
            consume_data = json.loads(consume_data)  # convert string to python dict

        except Exception as e:
            data = body.decode('utf-8')
            consume_data = eval(data)

        print('queue message for SR:%s' % consume_data['subRequestId'])
        '''
        if consume_data['GroupName'] =='Hotelbeds':
            try:
                scexec=ScriptHandler(consume_data)
                data=scexec.execute_crawl()
            except Exception as e:
                print("Script Executer return error", str(e))
        '''

        # from pdb import set_trace; set_trace()
        if "Retail" in consume_data['BusinessType']:
            try:
                scexec = ScriptsExecution(consume_data)
                data = scexec.run()
                print(" Received as a response", data)
            except Exception as e:
                    print("Retail Script Executer return error", str(e))
                    #logger.error("Script Executer return error", str(e))

        elif "Hotel" in consume_data['BusinessType']:
            error = None
            error_code = ''
            # sub_req_id = consume_data['subRequestId']
            ch.basic_ack(delivery_tag=method.delivery_tag)
            try:
                crawled_data = ScriptHandler(consume_data).execute_crawl(True)
            except core_exceptions.ScriptPNF:
                error = True
                error_code = 'script_timeout'
                crawled_data = consume_data.copy()

            crawled_hotel_count = len(crawled_data.get('hotels', list()))
            if not crawled_hotel_count and not error_code == 'script_timeout':
                error = True
                error_code = 'empty_hotels'
            print("\n\n\ncrawled hotels, error")
            print(crawled_hotel_count, bool(error), error_code)

            if error and error_code == 'empty_hotels':
                print('\n\n\nEmpty Hotels')
                core_services.MongoHandler().save_pnf(crawled_data, error)
                pnf_update_query = "UPDATE tbl_HotelCrawlRequestDetail SET StatusId = 8 WHERE HotelCrawlRequestDetailId = %s AND StatusId = 11"
                conn = DynamicCommonConnection.MySQLConnection()
                cur = conn.cursor()
                cur.execute(pnf_update_query % crawled_data['subRequestId'])
                conn.commit()
                cur.close()
                conn.close()
            elif error and error_code == 'script_timeout':
                print('\n\n\nScript Timeout')
                connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel2 = connection2.channel()
                channel2.queue_declare("Reparse")
                channel2.basic_publish(exchange='', routing_key='Reparse', body=json.dumps(crawled_data))
                connection2.close()
            else:
                print('\n\n\nGREAT SUCCESS')
                core_services.MongoHandler().save_successful_crawl(crawled_data)
                connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                channel2 = connection2.channel()
                channel2.queue_declare("Parser")
                channel2.basic_publish(exchange='', routing_key='Parser', body=json.dumps(crawled_data))
                connection2.close()

    def Main(self):
        try:
            print('running main')
            channel = self.get_channel()
            try:
                channel.basic_consume(ReparseConsumer.callback, queue=str('Reparse'), consumer_tag=None)
            except pika.exceptions.ChannelClosed:
                channel = self.get_channel()
            channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            ReparseConsumer().Main()
