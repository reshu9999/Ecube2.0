# Core Imports
from eCube_UI_2.core.resources.db_connectors import MySQLBaseHandler

# Django Imports
from django.conf import settings


class UserManagementDB(MySQLBaseHandler):

    def __init__(self, user_id):
        self.user_id = user_id
        print("self.user_id")
        print(self.user_id)
        host = settings.DATABASES['default']['HOST']
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        db_name = settings.DATABASES['default']['NAME']
        super().__init__(host, user, password, db_name)

    def get_role_users(self):
        print("get_role_users")
        cursor = self._cursor()
        args = [self.user_id]
        cursor.callproc(procname="GetRoleWiseUsers", args=args)
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_users_menu(self):
        cursor = self._cursor()
        args = [self.user_id]
        cursor.callproc(procname="GetUserMenus", args=args)
        records = cursor.fetchall()
        cursor.close()
        return records
    
  
    def GetCompetitorsByDomains(self):
        cursor = self._cursor()
        cursor.callproc(procname="GetCompetitorsByDomains")
        records = cursor.fetchall()
        cursor.close()
        return records  