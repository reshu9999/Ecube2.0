import json
from queues.connections import DBconnection, RabbitConnection
from queues.core import ReportHandler


class ReportConsumer(object):

    def callback(ch, method, properties, body):
        print(body)
        db = DBconnection()

        print("Receiving Messages -- %r" % body)
        data = body.decode('utf-8')

        consume_data = data.replace("'", "\"")
        consume_data = json.loads(consume_data)  # convert string to python dict

        requestRunId = consume_data['RID_RequestRunId']
        db.UpdateReportStatus(int(requestRunId), 'WIP')

        status = ReportHandler(consume_data).process_report()
        if status == 'Completed':
            db.UpdateReportStatus(int(requestRunId), status)

        db.clean_connections()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel = RabbitConnection.report_queue()  # calling Category Queue Connection class
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='Report')
    channel.start_consuming()
