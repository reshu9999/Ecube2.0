import pika

from queues.core import ScriptTimeoutCallback


class AetosScriptTimeoutConsumer(object):
    @classmethod
    def get_channel(cls):
        # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat_interval=0))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    # @staticmethod
    def callback(ch, method, properties, body):
        ScriptTimeoutCallback(ch, method, properties, body).consume()

    def Main(self):
        print('running main')
        channel = self.get_channel()
        try:
            channel.basic_consume(AetosScriptTimeoutConsumer.callback, queue=str('Recrawl'), consumer_tag=None)
        except pika.exceptions.ChannelClosed:
            channel = self.get_channel()
        channel.start_consuming()
