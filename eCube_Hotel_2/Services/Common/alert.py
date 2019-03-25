from pymongo import MongoClient
import pymysql
from Common.alertSupport import csvEngine
from Common.config_coordinator import config_fetcher
import datetime
from collections import OrderedDict
from bson.codec_options import CodecOptions
from bson.son import SON

MONGODB_CONFIG = config_fetcher.get_mongodb_config
MYSQL_CONFIG = config_fetcher.get_mysql_config

class Alert:
    def getMongoDbConnection(self):
        # client = MongoClient('mongodb://localhost:27017/')
        client = MongoClient(MONGODB_CONFIG['CRAWLED']['URL'])
        db = client.HTMLDumps
        return db

    def getDBConnection(self):
        try:
            # db = pymysql.connect(host="localhost",user="root",passwd="tech",db="eCube_Centralized_DB",autocommit=True)
            db = pymysql.connect(host=MYSQL_CONFIG['HOST'],user=MYSQL_CONFIG['USER'],passwd=MYSQL_CONFIG['PASSWORD'],db=MYSQL_CONFIG['DB'],autocommit=True)
            cur = db.cursor()
        except pymysql.DatabaseError as d:
            print(d.args[0])
        return cur
    
    def getdata(self, RequestId, RequestRunId):
        cur = self.getDBConnection()
        cur.execute(
            "Select al.FK_RequestId,al.Type,al.amountOrUnit,al.Conversions,al.Attributes from alert al join tbl_RequestMaster rm on al.FK_RequestId= rm.RequestId where al.FK_RequestId = %s",
            RequestId)
        row_count = cur.rowcount
        if row_count > 0:
            for row in cur.fetchall():
                alert_Type = row[1]
                amountOrUnit = row[2]
                conversions = row[3]
                attributes = row[4]
                records = self.getMongoData(RequestId, RequestRunId)
                if alert_Type == "PriceChange":
                    priceReports = self.downloadPriceType(amountOrUnit, conversions, attributes, records, RequestRunId)
                elif alert_Type == "StockChange":
                    stockReports = self.downloadStockType(amountOrUnit, conversions, attributes, records, RequestRunId)
        cur.close()        

    def getMongoData(self, reqid, reqRunId):
        db = self.getMongoDbConnection()
        opts = CodecOptions(document_class=SON)
        collection_son = db.CrawlResponse.with_options(codec_options=opts)
        finalRecordList = []
        records = collection_son.find({
            '$and': [{
                'RequestId': reqid
            }, {
                'RequestRunId': {
                    '$in': reqRunId
                }
            }]
        }, {
            "_id": 0,
            "RequestRunId": 1,
            "DomainName": 1,
            "rsCompetitorId": 1,
            "SubRequestId": 1,
            "rsMarketId": 1,
            'Was_price': 1,
            'inDateAdded': 1,
            'comStockQty_1': 1,
            'comBreak_1': 1,
            'comBreak_10': 1,
            'comBreak_2': 1,
            'comBreak_3': 1,
            'comBreak_4': 1,
            'comBreak_5': 1,
            'comBreak_6': 1,
            'comBreak_7': 1,
            'comBreak_8': 1,
            'comBreak_9': 1,
            'comOrderCode': 1,
            'comPrice_1': 1,
            'comPrice_10': 1,
            'comPrice_2': 1,
            'comPrice_3': 1,
            'comPrice_4': 1,
            'comPrice_5': 1,
            'comPrice_6': 1,
            'comPrice_7': 1,
            'comPrice_8': 1,
            'comPrice_9': 1,
            'comProductURL': 1,
            'manName': 1,
            'manPartDesc': 1,
            'manPartId': 1
        })

        for val in records:
            finalRecordList.append(val)

        return finalRecordList

    priceMapper = OrderedDict()
    priceMapper['rsCompetitorId'] = 'Competitor'
    priceMapper['rsMarketId'] = 'Market'
    priceMapper['comProductURL'] = 'Input SKUs'
    priceMapper['comOrderCode'] = 'Order Code'
    priceMapper['manName'] = 'MPN'
    priceMapper['manPartId'] = 'Brand'
    priceMapper['manPartDesc'] = 'Product Description'
    priceMapper['Old Price Date'] = 'Old Price Date'
    priceMapper['inDateAdded'] = 'Changed Noticed'
    priceMapper['Position1'] = 'Position1'
    priceMapper['Position2'] = 'Position2'
    priceMapper['Position3'] = 'Position3'
    priceMapper['Position4'] = 'Position4'
    priceMapper['Position5'] = 'Position5'
    priceMapper['Position6'] = 'Position6'
    priceMapper['Position7'] = 'Position7'
    priceMapper['Position8'] = 'Position8'
    priceMapper['Position9'] = 'Position9'
    priceMapper['Position10'] = 'Position10'
    priceMapper['Ref. No.'] = 'Ref. No.'

    stockMapper = OrderedDict()
    stockMapper['rsCompetitorId'] = 'Competitor'
    stockMapper['rsMarketId'] = 'Market'
    stockMapper['comProductURL'] = 'Input SKUs'
    stockMapper['comOrderCode'] = 'Order Code'
    stockMapper['manName'] = 'MPN'
    stockMapper['manPartId'] = 'Brand'
    stockMapper['manPartDesc'] = 'Product Description'
    stockMapper['Previuos stock Date'] = 'Previuos stock Date'
    stockMapper['inDateAdded'] = 'Changed Noticed'
    stockMapper['comStockQty_1'] = 'New stock quantity'
    stockMapper['Stock difference'] = 'Stock difference'
    stockMapper['Flag'] = 'Flag'

    def _csv_Price_fomation(self, data_rows, attributes):
        new_data_rows = []
        for data_row in data_rows:
            extra_data = OrderedDict([(self.priceMapper[header], '') for header in self.priceMapper])
            mongo_data = OrderedDict({self.priceMapper[header]: value for header, value in data_row.items() if
                                      header in self.priceMapper})
            mongo_data["Ref. No."] = attributes
            extra_data.update(mongo_data)
            new_data_rows.append(extra_data)
        return new_data_rows

    def _csv_Stock_fomation(self, data_rows, attributes):
        new_data_rows = []
        for data_row in data_rows:
            extra_data = OrderedDict([(self.stockMapper[header], '') for header in self.stockMapper])
            mongo_data = OrderedDict({self.stockMapper[header]: value for header, value in data_row.items() if
                                      header in self.stockMapper})
            mongo_data["Flag"] = attributes
            extra_data.update(mongo_data)
            new_data_rows.append(extra_data)
        return new_data_rows

    def downloadPriceType(self, amountOrUnit, conversions, attributes, records, RequestRunId):
        finalVal = []
        positions_arr = ['Position1', 'Position2', 'Position3', 'Position4', 'Position5', 'Position6', 'Position7',
                         'Position8', 'Position9', 'Position10']
        preVal = [rec for rec in records if rec['RequestRunId'] == RequestRunId[0]]
        currentVal = [rec for rec in records if rec['RequestRunId'] == RequestRunId[1]]

        for c in currentVal:
            for k in positions_arr:
                c[k] = " | "
            for p in preVal:
                if p['comProductURL'] == c['comProductURL']:
                    k_prices = [k for k in p.keys() if k != 'comProductURL' and k.startswith('comPrice')]
                    k_breaks = [k for k in p.keys() if k != 'comProductURL' and k.startswith('comBreak')]
                    u = []
                    for idx, ele in enumerate(k_prices):
                        if not str(p[ele]) == "" and not str(c[ele]) == "":
                            p[ele] = str(p[ele]).replace(",", "", str(p[ele]).count(",") - 1).replace(",", ".").strip()
                            c[ele] = str(c[ele]).replace(",", "", str(c[ele]).count(",") - 1).replace(",", ".").strip()
                            try:
                                if attributes == "Cheaper" and conversions == "$":
                                    if float(p[ele]) - float(c[ele]) >= float(amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                elif attributes == "Cheaper" and conversions == "%":
                                    if (float(p[ele]) - float(c[ele])) / float(p[ele]) * 100 >= float(amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                elif attributes == "Costlier" and conversions == "$":
                                    if float(c[ele]) - float(p[ele]) >= float(amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                elif attributes == "Costlier" and conversions == "%":
                                    if (float(c[ele]) - float(p[ele])) / float(p[ele]) * 100 >= float(amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                elif attributes == "Change" and conversions == "$":
                                    if abs(float(p[ele]) - float(c[ele])) >= float(amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                elif attributes == "Change" and conversions == "%":
                                    if abs((float(p[ele]) - float(c[ele])) / float(p[ele])) * 100 >= float(
                                            amountOrUnit):
                                        self._get_price_positions(c, finalVal, k_breaks, k_prices, p, positions_arr)
                                        break
                                else:
                                    u.append(ele)
                            except Exception as e:
                                u.append(ele)

        csvObj = csvEngine()
        csvData = self._csv_Price_fomation(finalVal, attributes)
        priceReport = csvObj.CreateCSVReport(csvData,
                                             filename="Alert_Price_" + attributes + datetime.datetime.now().strftime(
                                                 "%Y-%m-%d_%H:%M") + ".csv")
        return "price report downloaded succefully"

    def _get_price_positions(self, c, finalVal, k_breaks, k_prices, p, positions_arr):
        for idy, eley in enumerate(k_prices):
            p[eley] = str(p[eley]).replace(",", "", str(p[eley]).count(",") - 1).replace(",", ".").strip()
            c[eley] = str(c[eley]).replace(",", "", str(c[eley]).count(",") - 1).replace(",", ".").strip()

            key_break = k_breaks[idy]
            key_pos = positions_arr[idy]
            curval_break = str(c[key_break])
            preval_break = str(p[key_break])
            position_str = " | "

            if curval_break == '' and preval_break != '':
                position_str = "0|0"
            elif (curval_break != '' and preval_break == '') \
                    or (p[eley] == '' and c[eley] != ''):
                position_str = '+' + curval_break + position_str
                if p[eley] != c[eley]:
                    position_str = position_str + c[eley]
            else:
                if curval_break != preval_break:
                    position_str = curval_break + position_str
                if p[eley] != c[eley]:
                    position_str = position_str + c[eley]
            c[key_pos] = position_str

        c['Old Price Date'] = p['inDateAdded']
        finalVal.append(c)

    def downloadStockType(self, amountOrUnit, conversions, attributes, records,
                          RequestRunId):
        preVal = [rec for rec in records if rec['RequestRunId'] == RequestRunId[0]]
        currentVal = [rec for rec in records if rec['RequestRunId'] == RequestRunId[1]]
        finalStockVal = []

        for c in currentVal:
            for p in preVal:
                if p['comProductURL'] == c['comProductURL']:
                    u = []
                    try:
                        if attributes == "Higher":
                            if float(c['comStockQty_1']) - float(p['comStockQty_1']) >= float(amountOrUnit):
                                c['Previuos stock Date'] = p['inDateAdded']
                                c['Stock difference'] = float(c['comStockQty_1']) - float(p['comStockQty_1'])
                                finalStockVal.append(c)
                                break
                        elif attributes == "Lower":
                            if float(p['comStockQty_1']) - float(c['comStockQty_1']) >= float(amountOrUnit):
                                c['Previuos stock Date'] = p['inDateAdded']
                                c['Stock difference'] = float(c['comStockQty_1']) - float(p['comStockQty_1'])
                                finalStockVal.append(c)
                                break
                        elif attributes == "Change":
                            if abs(float(p['comStockQty_1']) - float(c['comStockQty_1'])) >= float(amountOrUnit):
                                c['Previuos stock Date'] = p['inDateAdded']
                                c['Stock difference'] = float(c['comStockQty_1']) - float(p['comStockQty_1'])
                                finalStockVal.append(c)
                                break
                    except Exception as e:
                        print(e)
                        # u.append()

            csvObj = csvEngine()
            csvData = self._csv_Stock_fomation(finalStockVal, attributes)
            stockReport = csvObj.CreateCSVReport(csvData,
                                                 filename="Alert_Stock_" + attributes + datetime.datetime.now().strftime(
                                                     "%Y-%m-%d_%H:%M") + ".csv")
        return "stock report downloaded succefully"


# al = Alert()
# k = al.getdata(29, [59084, 59087])
