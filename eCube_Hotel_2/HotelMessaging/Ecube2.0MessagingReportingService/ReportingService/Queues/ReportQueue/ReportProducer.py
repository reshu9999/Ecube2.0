# from Queues.ProducerQueueScripts.DBConnection import DBconnection
# from Queues.ProducerQueueScripts.RabbitConnections import Rabbit_connection
from DBConnection import DBconnection
from RabbitConnections import Rabbit_connection
import pika
import threading
import schedule
# class ReportProducer:

def ReportQueue():

        cur = DBconnection.GetInQueRequest("")  # Calling Database connections
        channel = Rabbit_connection.ReportQueueConnection("")  # Calling Producer and Queue Connections

        if cur:
            for row in cur.fetchall():
                row_list = [("ReportRunId", row[0] or ""),
                            ("RID_RequestId", row[1] or ""),
                            ("ReportName", row[2] or ""),
                            ("RID_RequestRunId", row[3] or "")
                            ]
                print(row_list)
                data_row_dict = dict(row_list)
                channel.basic_publish(exchange='',
                                      routing_key='Report',
                                      body=str(data_row_dict),
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,
                                      ))
        cur.close()
        return True


schedule.every(0.5).minutes.do(ReportQueue)
while True:
    schedule.run_pending()


# if __name__ == '__main__':
#     pro = ReportProducer()
#     t1 = threading.Thread(target=pro.ReportQueue, args=[])
#     t1.start()


