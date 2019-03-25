#!/usr/bin/python
from resources.connections import RabbitBaseConnection, MySQLBaseHandler
from resources.config_fetcher import crawling_config


class RabbitConnection(RabbitBaseConnection):

    def __init__(self):
        host = crawling_config.get_rabbitmq_min_args
        super().__init__(host)


class MySQLConnection(MySQLBaseHandler):

    def __init__(self):
        host, user, password, db_name = crawling_config.get_pymysql_args
        super().__init__(host, user, password, db_name)

    @property
    def group_bli_ids(self):
        group = self.get_cursor
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

        self.clean_connections()
        return dict(grouplist)

