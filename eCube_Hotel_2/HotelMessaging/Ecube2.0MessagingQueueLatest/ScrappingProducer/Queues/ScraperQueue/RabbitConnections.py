import pika
class Rabbit_connection:



    def CrawlerQueueConnection(self):
        credentials = pika.PlainCredentials('guest', 'guest')

        parameters = pika.ConnectionParameters('localhost',
                                               5672,
                                               '/',
                                               credentials)


        # credentials = pika.PlainCredentials('tech', 'eclerx@ecube2')
        #
        # parameters = pika.ConnectionParameters('192.168.8.6',
        #                                        5672,
        #                                        '/',
        #                                        credentials)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue='Crawler', durable=True)
        print(channel)
        return channel


    def ParserQueueConnection(self):

        credentials = pika.PlainCredentials('tech', 'eclerx@ecube2')

        parameters = pika.ConnectionParameters('192.168.8.6',
                                               5672,
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)

        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.8.6'))

        channel = connection.channel()
        channel.queue_declare(queue='Parser', durable=True)
        return channel

    def ReportQueueConnection(self):
        credentials = pika.PlainCredentials('tech', 'eclerx@ecube2')

        parameters = pika.ConnectionParameters('192.168.8.6',
                                               5672,
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='Report', durable=True)
        return channel



    # def CategoryQueue(self):
    #     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    #     channel = connection.channel()
    #
    #     channel.queue_declare(queue='rahul', durable=True)
    #     print(' [*] Waiting for messages. To exit press CTRL+C')
    #     return channel


