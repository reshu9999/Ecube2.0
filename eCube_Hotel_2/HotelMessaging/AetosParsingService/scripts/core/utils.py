# from resources.db_connectors import MongoHandler, MySQLBaseHandler
# from resources.config_coordinator import config_fetcher
#
# MongoHandler.set_mongo_url()
#
#
# class MySQLHandler(MySQLBaseHandler):
#     def __init__(self):
#         host = config_fetcher.get_mysql_config['HOST']
#         user = config_fetcher.get_mysql_config['USER']
#         password = config_fetcher.get_mysql_config['PASSWORD']
#         db_name = config_fetcher.get_mysql_config['DB']
#         super().__init__(host, user, password, db_name)
#
#
# def save_parsed_data(mongo_data):
#     mongo_data['_id'] = int(MongoHandler.CONN.system_js.getNextSequence("Crawl"))
#     MongoHandler.get_db('CrawlResponse').insert(mongo_data)
#     return mongo_data
#
#
# def get_field_mapping(request_id):
#     db_handler = MySQLHandler()
#     try:
#         cursor, response = db_handler.fetch_from_procedure('GetCrawlDataMapper', [int(request_id)])
#         result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in response]
#     except Exception as e:
#         return None
#     finally:
#         db_handler.clean_connections()
#
#     return result
