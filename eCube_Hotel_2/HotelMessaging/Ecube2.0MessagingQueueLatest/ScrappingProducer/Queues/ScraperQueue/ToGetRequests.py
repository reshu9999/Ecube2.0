from flask import Flask, jsonify, request
import schedule
from datetime import date, datetime, timedelta
from pdb import set_trace as st

import pymysql
from eCubeLog import logger

from config_fetcher import crawling_producer_config


def getRequest():
    # db = pymysql.connect(host="192.168.8.67",
    #                      user="tech",
    #                      passwd="eclerx#123",
    #                      db="eCube_Centralized_DB")

    # db = pymysql.connect(host="localhost",
    #                      user="tech",
    #                      passwd="eclerx#123",
    #                      db="eCube_Centralized_DB")

    # db = pymysql.connect(host="192.168.8.37",
    #                      user="tech",
    #                      passwd="eclerx#123",
    #                      db="eCube_Centralized_DB")

    # db = pymysql.connect(host="192.168.131.23",
    #                      user="tech",
    #                      passwd="Eclerx#123",
    #                      db="eCube_Centralized_DB")

    db = pymysql.connect(**crawling_producer_config.get_pymysql_kwargs)
    cur = db.cursor()
    # return cur
    print("running")
    logger.debug('Database Connection Established')
    # cur = getConnection()

    # domainName = request.args.get('domainName')
    # domainName = 'http://www.mouser.com'

    # query_string = "select b.Id, a.DomainId, HeaderName, HeaderValue from eCube.tbl_DomainMaster a, eCube.tbl_DomainHeaderMapping b WHERE a.Id = b.DomainId and a.DomainName = '{domainName}'".format(domainName=domainName)
    # try:
    if True:
        # cur.execute(query_string)
        cur.callproc('spGetRequestRunDetail')
        res = cur.fetchall()
        # print("aetos res")
        # print(res)
        for r in res:
            print(r)
            # print(r[0],r[1])
            print(r[0], r[1], r[-1])
            # SaveRequest(r[0], r[1], cur,db)
            SaveRequest(r[0], r[1], r[-1], cur, db)
            UpdateStatus(r[0], cur, db)

        # r = [dict((cur.description[i][0], value)
        #           for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
    # except Exception as e:
    #   logger.debug('Error Returned  by spGetRequestRunDetail Query', str(e))
    #   return True


# def SaveRequest(RequestRunId, RequestId,cur,db):
def SaveRequest(RequestRunId, RequestId, ReqModeId, cur, db):
    try:
        #     cur = getConnection()

        # cur.execute(query_string)
        args = [RequestId, RequestRunId, ReqModeId]
        # cur.callproc('spInsertRequestDetails',args)
        # res = cur.fetchall()

        # cur.callproc(procname='spInsertRequestDetails', args=args)

        # Code Change done for Hotel by Shrikant 04-06-2017 19:52 #

        if ReqModeId == 1:
            cur.callproc(procname='spInsertRequestDetails', args=args)
        if ReqModeId in (2, 3):
            args1 = [RequestId]
            print("args1 1")
            print(args1)
            cur.callproc('spGetPreCrawlDetails', args=args1)
            res = cur.fetchall()
            for i in res:
                if i[6] == 1:  # Based on Boardtype ID.
                    startDate = i[4]
                    endDate = i[5]
                    for n in range((endDate - startDate).days + 1):
                        thisdate = startDate + timedelta(n)
                        if thisdate.strftime('%A') in i[7]:
                            args2 = [i[1], RequestRunId, i[0], thisdate]
                            print('Arg2', args2)
                            if ReqModeId == 2:
                                cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                            elif ReqModeId == 3:
                                cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                    db.commit()
                elif i[6] == 2:
                    for advancedt in i[10].split(','):
                        thisdate = date.today() + timedelta(int(advancedt))
                        args2 = [i[1], RequestRunId, i[0], thisdate]
                        print('Arg2 1', args2)
                        if ReqModeId == 2:
                            cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                        elif ReqModeId == 3:
                            cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                    db.commit()
                elif i[6] == 3:
                    for advancedt in i[10].split(','):
                        thisdate = datetime.strptime(advancedt, '%m/%d/%Y').date()
                        args2 = [i[1], RequestRunId, i[0], thisdate]
                        print('Arg2 2', args2)
                        if ReqModeId == 2:
                            cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                        elif ReqModeId == 3:
                            cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                    db.commit()
                elif i[6] == 4:
                    for advancedt in i[10].split(','):
                        thisdate = date.today() + timedelta(int(advancedt) * 7)
                        args2 = [i[1], RequestRunId, i[0], thisdate]
                        print('Arg2 3', args2)
                        if ReqModeId == 2:
                            cur.callproc('spInsertHotelCrawlRequestDetails', args=args2)
                        elif ReqModeId == 3:
                            cur.callproc('spInsertHotelFlightCrawlRequestDetails', args=args2)
                    db.commit()

        # cur.execute('spInsertRequestDetails', args)
        # cur.fetchall()

        # cur.close()

        # r = [dict((cur.description[i][0], value)
        #           for i, value in enumerate(row)) for row in cur.fetchall()]
    except Exception as e:
        logger.debug('Error Returned  by spInsertRequestDetails Query', str(e))
        return jsonify({'StatusCode': 500, 'ResultData': e})
    # return jsonify({'StatusCode': 200,'ResultData' : r})


def UpdateStatus(RequestRunId, cur, db):
    print('updated')
    # domainName = request.args.get('domainName')
    # domainName = 'http://www.mouser.com'
    # conn = mysql.connect()
    # cur = mysql.connect().cursor()
    # query_string = "select b.Id, a.DomainId, HeaderName, HeaderValue from eCube.tbl_DomainMaster a, eCube.tbl_DomainHeaderMapping b WHERE a.Id = b.DomainId and a.DomainName = '{domainName}'".format(domainName=domainName)
    try:
        # cur.execute(query_string)
        args = [RequestRunId]
        # cur.callproc('spInsertRequestDetails',args)
        # res = cur.fetchall()
        cur.callproc('spUpdateRequestStatus', args)
        db.commit()

        # r = [dict((cur.description[i][0], value)
        #           for i, value in enumerate(row)) for row in cur.fetchall()]
    except Exception as e:
        logger.debug('Error Returned  by spUpdateRequestStatus Query', str(e))
        return jsonify({'StatusCode': 500, 'ResultData': e})
        # return jsonify({'StatusCode': 200,'ResultData' : r})


# getRequest()
'''
schedule.every(0.5).minutes.do(getRequest)
while True:
    logger.debug('To Get Request Request Service Started')
    schedule.run_pending()
'''
