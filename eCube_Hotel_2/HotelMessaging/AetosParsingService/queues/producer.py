from queues.connections import MySQLConnection
from queues.core import RequestReparse, SubRequestReparse


class ReparseProducer(object):

    MYSQL_CONN = MySQLConnection

    @property
    def _get_reparse_requests(self):
        connection = self.MYSQL_CONN()
        requests = connection.fetch_from_query("SELECT FK_RequestId, RequestRunId FROM tbl_RequestRunDetail WHERE FK_StatusId=10;")
        connection.clean_connections()
        return requests

    @property
    def _get_reparse_sub_requests(self):
        connection = self.MYSQL_CONN()
        sub_requests = connection.fetch_from_query("SELECT HotelCrawlRequestDetailId, RequestId, RequestRunId FROM tbl_HotelCrawlRequestDetail WHERE StatusId=10;")
        connection.clean_connections()
        return sub_requests

    def Main(self):
        for request in self._get_reparse_requests:
            request_id = request[0]
            request_reparse = RequestReparse(request_id)
            print('Reparse Request ID "%s"' % request_id)
            request_reparse.update_status()
            request_reparse.clean_parsed_data()
            request_reparse.push_to_reparse_queue()

        for sub_request in self._get_reparse_sub_requests:
            sub_request_id = sub_request[0]
            sub_request_reparse = SubRequestReparse(sub_request_id)
            print('Reparse Sub Request ID "%s"' % sub_request_id)
            sub_request_reparse.update_status()
            sub_request_reparse.clean_parsed_data()
            sub_request_reparse.push_to_reparse_queue()
