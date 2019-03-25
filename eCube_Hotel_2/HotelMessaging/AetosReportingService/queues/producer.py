import pika

from queues.connections import DBconnection, RabbitConnection


def ReportQueue():
    db = DBconnection()
    cur = db.GetInQueRequest  # Calling Database connections
    channel = RabbitConnection.report_queue()  # Calling Producer and Queue Connections

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
    db.clean_connections()
    return True


main_i = 1000


def TestingReportQueue():
    channel = RabbitConnection.report_queue()  # Calling Producer and Queue Connections
    for row in range(1, 100):
        row_list = [
            ("ReportRunId", "%s" % (main_i + row * 1000)),
            ("RID_RequestId", "%s" % (main_i + row * 100)),
            ("ReportName", "Aetos_Main_I_%s" % (main_i + row)),
            ("RID_RequestRunId", "%s" % (main_i + row * 10000))
        ]
        print(row_list)
        data_row_dict = dict(row_list)
        channel.basic_publish(exchange='', routing_key='Report', body=str(data_row_dict),
                              properties=pika.BasicProperties(delivery_mode=2,))

    return True


def AetosReportQueue():
    channel = RabbitConnection.report_queue()
    data_row_dict = {
        'ReportRunId': '6155',
        'RID_RequestId': '6155',
        'ReportName': 'aetos_report',
        'RID_RequestRunId': '186826',
    }
    channel.basic_publish(exchange='', routing_key='Report', body=str(data_row_dict),
                              properties=pika.BasicProperties(delivery_mode=2,))

    return True
