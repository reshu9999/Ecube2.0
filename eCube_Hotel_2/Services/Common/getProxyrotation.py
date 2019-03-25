from datetime import timedelta
# import MySQLdb
import pymysql
# from Common.models import proxyuses
from datetime import datetime
import pandas as pd
import time
#import memcache
from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
#memcache_config = config_fetcher.get_memcache_config

db = pymysql.connect(host=mysql_config['HOST'],
                     user=mysql_config['USER'],
                     passwd=mysql_config['PASSWORD'],
                     db=mysql_config['DB'])

class getProxyrotation:
    dfLow = pd.DataFrame()
    dfMEDIUM = pd.DataFrame()
    dfHIGH = pd.DataFrame()
    #memc = memcache.Client(['%s:%s' % (memcache_config['HOST'], memcache_config['PORT'])])
    memc = ''

    def GetProxyData(self, domain, country,pos='',hittype=1):
        '''

        :param domain:
        :param country:
        :return:
        '''


        # self.memc.delete('topMediumcountry')
        # return None
        db = pymysql.connect(host=mysql_config['HOST'],
                             user=mysql_config['USER'],
                             passwd=mysql_config['PASSWORD'],
                             db=mysql_config['DB'])
                
        cur = db.cursor()
        cur.callproc('sp_Fetch_Proxydetails', [domain, country,pos,hittype])

        #df = pd.DataFrame(list(cur.fetchall()),
                              #columns=["Domain", "ProxyIP", "ProxyType", "Weights", "Country", "Status",
                                      # "ProxyUserName", "ProxyPassword","ProxyPort"])
        #df['successHits'] = 0
        #print(df)
        result = list(cur.fetchall())
        proxy_dict = {}
        if result:
            result = result[0]
            proxy_dict = {'IP': result[1],'port': result[8],'UserName': result[6],'Password': result[7]}

        cur.close()
        #result = obj.pickProxydetails(df,country,domain)
        print(result)            

        return proxy_dict

    def pickProxydetails(self, df,country,domain):
        ProxyServer = ''
        Username = ''
        Password = ''
        port=''
        LowCount = 0
        MediumCount = 0
        dftimezoneMEDIUMcount = 0
        dftimezoneLOWcount = 0
        HightCount = 0

        db = pymysql.connect(host=mysql_config['HOST'],
                             user=mysql_config['USER'],
                             passwd=mysql_config['PASSWORD'],
                             db=mysql_config['DB'])

        dfLow = pd.DataFrame(df.loc[df['ProxyType'] == 'LOW'])

        dfMEDIUM = pd.DataFrame(df.loc[df['ProxyType'] == 'MEDIUM'])

        dfHIGH = pd.DataFrame(df.loc[df['ProxyType'] == 'HIGH'])
        dfLow = dfLow.sort_values(by='Weights', ascending=False).sort_values(by='Weights', ascending=False)

        dfMEDIUM = dfMEDIUM.sort_values(by='Weights', ascending=False).sort_values(by='Weights',ascending=False)

        dfHIGH = dfHIGH.sort_values(by='Weights', ascending=False).sort_values(by='Weights', ascending=False)

        # data_items = dfLow.iterrows()
        data_items = list(dfLow.iterrows())
        last_proxy=False
        proxy_completed_rotation=False


        for i, data in enumerate(data_items):
            last_proxy = i == len(data_items) - 1


            proxy_completed_rotation = False
            index = data[0]
            row = data[1]

            successhits=row['successHits']
            Weights=row["Weights"]
            Proxystatus=row["Status"]
            print(Weights)


            proxy_completed_rotation = ((Weights - successhits) == 1)
            print(proxy_completed_rotation)
            if Weights<=successhits:

                continue
            else:

              successhits = successhits + 1
              print(successhits)
              row['successHits']=successhits
              ProxyServer = row['ProxyIP']
              Username = row['ProxyUserName']
              Password = row['ProxyPassword']
              port=row['ProxyPort']

              df.successHits[df[df.ProxyIP == ProxyServer].index] = successhits

              print("Memcached Before update", )
              self.memc.set('top5films', dict(df), 0)
              print("Memcache After update")
              break


        if last_proxy and proxy_completed_rotation:

            self.memc.delete('top5films')
        else:
            print('not last proxy')



        LowCount = len(dfLow[(dfLow['Status'] == 'UnBlocked')])
        print(LowCount)

        if LowCount == 0:

            print('Low Proxies completed')
            LowcountryProxyData = self.memc.get("Lowothercountry")
            if not LowcountryProxyData:
                print('ste1')
                cur = db.cursor()
                cur.callproc('sp_GetTimeZoneWiseProxy', [country, 1, domain])
                a = cur.fetchall()
                data = list(a)
                df = pd.DataFrame(data, columns=["Domain", "ProxyIP", "ProxyType", "Weights", "Country", "Status","ProxyUserName", "ProxyPassword", "ProxyPort"])
                df['successHits'] = 0
                cur.close()
                print(df)
                self.memc.set('Lowothercountry', dict(df), 0)
            else:
                # # print ("Load Data from memcached")
                df = pd.DataFrame((LowcountryProxyData))
                print('Memcache country')
                print(df)
            dftimezoneLOW = pd.DataFrame(df)
            dftimezoneLOW = dftimezoneLOW.sort_values(by='Weights', ascending=False).sort_values(by='Weights',ascending=False)
            data_items = list(dftimezoneLOW.iterrows())
            last_proxy = False
            proxy_completed_rotation = False
            for i, data in enumerate(data_items):
                last_proxy = i == len(data_items) - 1

                proxy_completed_rotation = False
                index = data[0]
                row = data[1]

                successhits=row['successHits']
                Weights=row["Weights"]
                Proxystatus=row["Status"]

                proxy_completed_rotation = ((Weights - successhits) == 1)
                if Weights<=successhits:

                    continue
                else:

                  successhits = successhits + 1

                  row['successHits']=successhits
                  ProxyServer = row['ProxyIP']
                  Username = row['ProxyUserName']
                  Password = row['ProxyPassword']
                  port=row['ProxyPort']

                  df.successHits[df[df.ProxyIP == ProxyServer].index] = successhits

                  print("Memcached Before update", )
                  self.memc.set('Lowothercountry', dict(df), 0)
                  print("Memcache After update")
                  break


            if last_proxy and proxy_completed_rotation:

                self.memc.delete('Lowothercountry')
            else:
                print('not last proxy')

            dftimezoneLOWcount = len(dftimezoneLOW[(dftimezoneLOW['Status'] == 'UnBlocked')])
        #
        if LowCount == 0 and dftimezoneLOWcount == 0:
            data_items = list(dfMEDIUM.iterrows())

            for i, data in enumerate(data_items):
                last_proxy = i == len(data_items) - 1
                print("last_proxy")
                print(last_proxy)
                proxy_completed_rotation = False
                index = data[0]
                row = data[1]
                print('loop no ' + str(i))
                successhits = row['successHits']
                Weights = row["Weights"]
                Proxystatus = row["Status"]
                print(Weights)
                print(successhits)
                print('IP')
                print(row['ProxyIP'])
                print(Weights)
                print(successhits)
                proxy_completed_rotation = ((Weights - successhits) == 1)
                if Weights <= successhits:
                    print('rotating proxy')
                    print('will continue ' + str(i))
                    continue
                else:
                    print('not rotating proxy')
                    successhits = successhits + 1

                    row['successHits'] = successhits
                    ProxyServer = row['ProxyIP']
                    Username = row['ProxyUserName']
                    Password = row['ProxyPassword']
                    port = row['ProxyPort']

                    df.successHits[df[df.ProxyIP == ProxyServer].index] = successhits

                    print("Memcached Before update", )
                    self.memc.set('top5films', dict(df), 0)
                    print("Memcache After update")
                    break

            print(last_proxy)
            print(proxy_completed_rotation)

            if last_proxy and proxy_completed_rotation:
                print('last proxy')
                self.memc.delete('top5films')
            else:
                print('not last proxy')

        MediumCount = len(dfMEDIUM[(dfMEDIUM['Status'] == 'UnBlocked')])
        # # #
        if MediumCount == 0 and LowCount == 0 and dftimezoneLOWcount == 0:
            print('Low Proxies completed')
            MediumcountryProxyData = self.memc.get("topMediumcountry")
            if not MediumcountryProxyData:
                print('ste1')
                cur = db.cursor()
                cur.callproc('sp_GetTimeZoneWiseProxy', [country, 2, domain])
                a = cur.fetchall()
                data = list(a)
                df = pd.DataFrame(data, columns=["Domain", "ProxyIP", "ProxyType", "Weights", "Country", "Status",
                                                 "ProxyUserName", "ProxyPassword", "ProxyPort"])
                df['successHits'] = 0
                cur.close()
                print(df)
                self.memc.set('topMediumcountry', dict(df), 0)
            else:
                # # print ("Load Data from memcached")
                df = pd.DataFrame((MediumcountryProxyData))
                print('Memcache country')
                print(df)
            dftimezoneMEDIUM = pd.DataFrame(df)
            dftimezoneMEDIUM = dftimezoneMEDIUM.sort_values(by='Weights', ascending=False).sort_values(by='Weights',
                                                                                                 ascending=False)
            data_items = list(dftimezoneMEDIUM.iterrows())
            last_proxy = False
            proxy_completed_rotation = False
            for i, data in enumerate(data_items):
                last_proxy = i == len(data_items) - 1

                proxy_completed_rotation = False
                index = data[0]
                row = data[1]

                successhits = row['successHits']
                Weights = row["Weights"]
                Proxystatus = row["Status"]

                proxy_completed_rotation = ((Weights - successhits) == 1)
                if Weights <= successhits:

                    continue
                else:

                    successhits = successhits + 1

                    row['successHits'] = successhits
                    ProxyServer = row['ProxyIP']
                    Username = row['ProxyUserName']
                    Password = row['ProxyPassword']
                    port = row['ProxyPort']

                    df.successHits[df[df.ProxyIP == ProxyServer].index] = successhits

                    print("Memcached Before update", )
                    self.memc.set('topMediumcountry', dict(df), 0)
                    print("Memcache After update")
                    break

            if last_proxy and proxy_completed_rotation:

                self.memc.delete('topMediumcountry')
            else:
                print('not last proxy')

            dftimezoneMEDIUMcount = len(dftimezoneMEDIUM[(dftimezoneMEDIUM['Status'] == 'UnBlocked')])
        # #
        if MediumCount == 0 and LowCount == 0 and dftimezoneLOWcount == 0 and dftimezoneMEDIUMcount == 0:
            data_items = list(dfHIGH.iterrows())

            for i, data in enumerate(data_items):
                last_proxy = i == len(data_items) - 1
                print("last_proxy")
                print(last_proxy)
                proxy_completed_rotation = False
                index = data[0]
                row = data[1]
                print('loop no ' + str(i))
                successhits = row['successHits']
                Weights = row["Weights"]
                Proxystatus = row["Status"]
                print(Weights)
                print(successhits)
                print('IP')
                print(row['ProxyIP'])
                print(Weights)
                print(successhits)
                proxy_completed_rotation = ((Weights - successhits) == 1)
                if Weights <= successhits:
                    print('rotating proxy')
                    print('will continue ' + str(i))
                    continue
                else:
                    print('not rotating proxy')
                    successhits = successhits + 1

                    row['successHits'] = successhits
                    ProxyServer = row['ProxyIP']
                    Username = row['ProxyUserName']
                    Password = row['ProxyPassword']
                    port = row['ProxyPort']

                    df.successHits[df[df.ProxyIP == ProxyServer].index] = successhits

                    print("Memcached Before update", )
                    self.memc.set('top5films', dict(df), 0)
                    print("Memcache After update")
                    break

            print(last_proxy)
            print(proxy_completed_rotation)

            if last_proxy and proxy_completed_rotation:
                print('last proxy')
                self.memc.delete('top5films')
            else:
                print('not last proxy')

        HightCount = len(dfHIGH[(dfHIGH['Status'] == 'UnBlocked')])

        k = ["IP", "UserName", "Password","port"]
        return dict(zip(k, [ProxyServer, Username, Password,port]))


#obj = getProxyrotation()
#obj.GetProxyData('it.farnell.com','Italy')
