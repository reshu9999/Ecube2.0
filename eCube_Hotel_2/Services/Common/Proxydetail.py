from datetime import timedelta
# import MySQLdb
import pymysql
# from Common.models import proxyuses
from datetime import datetime
import pandas as pd
import time
import memcache

from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
memcache_config = config_fetcher.get_memcache_config

class Proxydetail:


    def SaveProxyDetails(self, domain, proxyserver, proxyport, proxycountry, proxyregion, Proxystatus):
        memc = memcache.Client(['%s:%s' % (memcache_config['HOST'], memcache_config['PORT'])])

        db = pymysql.connect(host=mysql_config['HOST'],
                             user=mysql_config['USER'],
                             passwd=mysql_config['PASSWORD'],
                             db=mysql_config['DB'])

        result1 = 0
        cur = db.cursor()
        cur.callproc('sp_Add_ProxyMaster',
                     [domain, proxyserver, proxyport, proxycountry, proxyregion, Proxystatus, result1])
        cur.execute("Select @_sp_Add_ProxyMaster_7")
        result = cur.fetchone()
        cur.close()
        db.commit()
        memc.delete('top5films')
        memc.delete('Lowothercountry')
        memc.delete('topMediumcountry')