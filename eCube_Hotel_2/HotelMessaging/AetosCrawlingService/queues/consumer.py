import pika
from queues.core import NormalCallback
from queues.connections import MySQLConnection


class AetosConsumer(object):
    # @staticmethod
    def callback(ch, method, properties, body):
        NormalCallback(ch, method, properties, body).consume()

    def RabbitConnection(self):

        print('Dynamic Scrapping Consumer --- rabbitMQ Connection called')

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat_interval=0))
        # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    def GroupDBMaster(self):

        print('Dynamic Scrapping Consumer --- Group Master Called')

        Groupdb = MySQLConnection().connection

        group = Groupdb.cursor()
        group.execute("select * from tbl_Bli_GroupMaster")
        grouplist = []
        for row in group.fetchall():
            BusinessType = row[6]

            if "Retail" in BusinessType:

                GroupRowList = (row[1], row[2] or 0)
                grouplist.append(GroupRowList)

            elif "Hotel" in BusinessType:
                GroupRowList = (row[1], row[2] or 0)
                grouplist.append(GroupRowList)


        grouplist_dict = dict(grouplist)

        group.close()
        Groupdb.close()
        return grouplist_dict

    def Main(self):
        print("Dynamic Scrapping Producer --- Main function  Called")

        grouplistDict = self.GroupDBMaster()
        channel = self.RabbitConnection()

        print(grouplistDict)
        for key,value in grouplistDict.items():
            print("Sequence", key)
            for _ in range(int(value)):
                try:
                    channel.basic_consume(AetosConsumer.callback, queue=str(key), consumer_tag=None)
                except pika.exceptions.ChannelClosed:
                    print('Closed or no Queue ' + key)
                    print('Closed or no Queue ' + key)
                    channel = self.RabbitConnection()

        channel.start_consuming()
