import copy
from resources.connections import RabbitBaseConnection, MySQLBaseHandler, RedisBaseHandler, MongoBaseHandler
from resources.config_fetcher import parsing_config


class RabbitConnection(RabbitBaseConnection):

    def __init__(self):
        host = parsing_config.get_rabbitmq_min_args
        super().__init__(host)


class MySQLConnection(MySQLBaseHandler):

    def __init__(self):
        host, user, password, db_name = parsing_config.get_pymysql_args
        super().__init__(host, user, password, db_name)


class RedisConnection(RedisBaseHandler):

    HOST = parsing_config.get_redis_config['HOST']
    PORT = parsing_config.get_redis_config['PORT']
    DB = 3


class MongoConnection(MongoBaseHandler):

    DB_NAME = 'HTMLDumps'

    @staticmethod
    def _get_individual_hotels(crawled_data):
        insert_list = list()
        master_data_copy = copy.deepcopy(crawled_data)
        hotels = master_data_copy.pop('hotels')
        for hotel in hotels:
            insert_data = master_data_copy.copy()
            insert_data['hotel'] = hotel
            insert_list.append(insert_data)
        return insert_list

    def save_partial_parse(self, parsed_data, parse_type):
        collection = self.get_collection('CrawlResponseData')
        collection.insert(parsed_data)
        collection = self.get_collection('ParsedStatus')
        query = {
            'subRequestId': parsed_data['subRequestId'],
            'requestId': parsed_data['requestId'],
            'index': parsed_data['hotel']['index'],
            'status': parse_type
        }
        docs = collection.find(query)
        last_hotel = False
        if len(list(docs)) == 1:
            last_hotel = True
        collection.remove(query)

        query = {
            'subRequestId': parsed_data['subRequestId']
        }
        docs = collection.find(query)
        for doc in docs:
            return False
        if not last_hotel:
            return False
            raise Exception('Sub Request cannot be completed unless Last Hotel is Parsed')
        return True

    def save_successful_parse(self, parsed_data):
        collection = self.get_collection('CrawlResponseData')
        insert_list = self._get_individual_hotels(parsed_data)

        for insert_data in insert_list:
            collection.insert(insert_data)

    @classmethod
    def get_crawled_html(cls, query):
        collection = cls.get_collection('HTMLRepository')
        return collection.find(query)

    @classmethod
    def delete_parsed_data(cls, query):
        collection = cls.get_collection('CrawlResponseData')
        collection.remove(query)
        collection = cls.get_collection('ParsedStatus')
        collection.remove(query)

    @classmethod
    def mark_hotels_to_be_reparsed(cls, crawled_data):
        collection = cls.get_collection('ParsedStatus')

        for insert_data in crawled_data:
            doc = {
                'subRequestId': insert_data['subRequestId'],
                'requestId': insert_data['requestId'],
                'status': 'to_be_reparsed',
                'hotel_count': len(crawled_data),
                'index': insert_data['hotel']['index']
            }
            collection.insert(doc)


MongoConnection.set_mongo_url(parsing_config.get_mongodb_config['URL'])
