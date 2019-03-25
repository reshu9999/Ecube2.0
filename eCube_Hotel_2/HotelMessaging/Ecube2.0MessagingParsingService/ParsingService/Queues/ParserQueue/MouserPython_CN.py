
import urllib3, ssl
from bs4 import BeautifulSoup
import re, string
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
rcConnectionError = '-6'
rcManualTermination = '-5'
rcFormatError = '-4'
rcSiteError = '-3'
rcNotFound = '-2'
rcLoginFailure = '-1'
rcGeneralFailure = '0'
rcOK = '1'
rcPartcodeSearch = 'p'
rcKeywordSearch = 'k'
rcContainSearch = 'c'

class MouserPython_CN:
    def __init__(self,htmlElements):
        try:
                htmlElem = BeautifulSoup(htmlElements['htmlElement'], "html.parser")
                self.html_Element = htmlElem
        except:
            htmlElem = BeautifulSoup(htmlElements, "html.parser")
            self.html_Element = htmlElem

    def Category(self):
            divCategory = self.html_Element.find("div", {"id": "pdpBreadcrumb"})
            if divCategory is not None:
                category = divCategory.findAll('a')
                if len(category) != 0:
                    categories = "|".join(str(cat.text.encode('utf-8').strip()) for cat in category)
                    categories = categories.replace("All Products|", '')
                    categories = categories.replace("Alle Produkte|", '')
                    categories = categories.replace("|See an Error?", '')
                else:
                    categories = ''

            else:
                categories = ''
            print ('Categories: ' + categories)
            return categories


    def ManPartDesc(self):
        result = self.html_Element.find("span", {"id": "spnDescription"})
        if result is not None:
            Mandesc = result.text.strip()
        else:
            Mandesc = ''
        print ('Mandesc: ' + Mandesc)
        return Mandesc



    def OrderCode(self):
        result = self.html_Element.find("div", {"id": "divMouserPartNum"})
        if result is not None:
            orderCode = result.text.strip()
        else:
            orderCode = ''
        print ('orderCode: ' + orderCode)
        return orderCode



    def ManPartId(self):
        # parse Manufacturer Part Number
        # result = self.html_Element.find("div", {"id": "divManufacturerPartNum"})
        result = self.html_Element.find("span", {"id": "spnManufacturerPartNumber"})
        if result is not None:
            manPartNum = result.text.strip()
        else:
            manPartNum = ''
        print ('ManPartId: ' + manPartNum)
        return manPartNum

    def Ean(self):
        return ''


    def ImgUrl(self):
        divImgUrl = self.html_Element.find("div", {"id": "image_container"})
        if divImgUrl is not None:
            img = divImgUrl.find('img')
            if img is not None:
                result = img['src']
                src = 'https://www.mouser.com/' + result[2:]
            else:
                src = ''
        else:
            src = ''
        print ('ImgUrl: ' + src)
        return src

    def Price(self):
        quantities = ''
        prices = ''
        BreakResult = self.html_Element.find("div", {"class": "div-table pdp-pricing-table"})
        if BreakResult is not None:
            breakList = BreakResult.findAll("div", {"class": "div-table-row"})
            if len(breakList) > 0:
                for p in breakList:

                    breakValue = filter(lambda x: x in '.0123456789',
                                        p.find("div", {"class": "row"}).find("a").text)
                    if breakValue is not None:
                        breakValue = filter(lambda x: x in '.0123456789',
                                            p.find("div", {"class": "row"}).find("a").text)
                        # priceValue = filter(lambda x: x in '.0123456789', p.find("div", {"class": "row"}).find("div", {
                        #     "class": "col-xs-4 text-right"}).find("span").text)
                        priceValue = p.find("div", {"class": "row"}).find("div", {
                            "class": "col-xs-4 text-right"}).find("span")
                        if priceValue is not None:
                            priceValue = p.find("div", {"class": "row"}).find("div", {
                                "class": "col-xs-4 text-right"}).find("span").text
                            priceValue = re.sub('[^0-9.]', '', priceValue)

                            if quantities == '':
                                listQty = ','.join(i for i in breakValue)
                                # listpricevalue = ','.join(str(i) for i in priceValue)
                                quantities = listQty
                                prices = priceValue
                            else:
                                listQty = ','.join(i for i in quantities)
                                listbValue = ','.join(str(i) for i in breakValue)
                                quantities = listQty + "->" + listbValue

                                # listprice = ','.join(i for i in prices)
                                # listpriceValue = ','.join(str(i) for i in priceValue)

                                prices = prices + "->" + priceValue
            # print ('quantities: ' + quantities)
            print('prices: ' + prices)
            return prices



    def ManPackQty(self):
        quantities = ''
        prices = ''
        BreakResult = self.html_Element.find("div", {"class": "div-table pdp-pricing-table"})
        if BreakResult is not None:
            breakList = BreakResult.findAll("div", {"class": "div-table-row"})
            if len(breakList) > 0:
                for p in breakList:

                    breakValue = filter(lambda x: x in '.0123456789',
                                        p.find("div", {"class": "row"}).find("a").text)
                    if breakValue is not None:
                        breakValue = filter(lambda x: x in '.0123456789',
                                            p.find("div", {"class": "row"}).find("a").text)
                        # priceValue = filter(lambda x: x in '.0123456789', p.find("div", {"class": "row"}).find("div", {
                        #     "class": "col-xs-4 text-right"}).find("span").text)
                        priceValue = p.find("div", {"class": "row"}).find("div", {
                            "class": "col-xs-4 text-right"}).find("span")
                        if priceValue is not None:
                            priceValue = p.find("div", {"class": "row"}).find("div", {
                                "class": "col-xs-4 text-right"}).find("span").text
                            priceValue = re.sub('[^0-9.]', '', priceValue)

                            if quantities == '':
                                listQty = ','.join(i for i in breakValue)
                                # listpricevalue = ','.join(str(i) for i in priceValue)
                                quantities = listQty
                                prices = priceValue
                            else:
                                listQty = ','.join(i for i in quantities)
                                listbValue = ','.join(str(i) for i in breakValue)
                                quantities = listQty + "->" + listbValue

                                # listprice = ','.join(i for i in prices)
                                # listpriceValue = ','.join(str(i) for i in priceValue)

                                prices = prices + "->" + priceValue
        print('ManPackQty: ' + quantities)
        return quantities



    def UOM(self):
        return ''

    def TechnicalDataSheet(self):
        result = self.html_Element.find("a", {"id": "pdp-datasheet_0"})
        if result is not None:
            dsURL = result['href']
        else:
            dsURL = ''
        print ('TechnicalDataSheet: ' + dsURL)
        return dsURL

    def Specification(self):
        list = self.html_Element.find("div", {"class": "div-table specs-table"})
        try:
            if list is not None:
                list1 = list.findAll("div", {"class": "div-table-row"})
                Strspec = "|".join(str(row.text.strip().replace('\n', ' ').replace('\r', '')) for row in list1)
                Strspec = re.sub("\s\s+", " ", Strspec)
                return Strspec

            else:
                Strspec = ''
        except Exception as e:
            print(e)
        print("Specification:" + Strspec)
        return Strspec



    def ManName(self):
        result = self.html_Element.find("span", {"itemprop": "name"})
        if result is not None:
            manName = result.text.strip()
        else:
            manName = ''
        print ('manName: ' + manName)
        return manName


    def ComStockloc(self):
        htmlElem=self.html_Element
        divStock = htmlElem.find("div", {"class": "pdp-product-availability"})
        if divStock is not None:
            result1 = divStock.find("div", {"class": "col-xs-8"})
            if result1 is not None:
                result2 = result1.find("div")
                print(result2.text.strip())
                result = result2.text.strip()

                stock1 = ''
                stock2 = ''
                result = re.split(" ", result)
                if (len(result) > 0):
                    stock1 = result[0]
                    stock1 = str.replace(stock1, ",", "")
                    if (stock1.isdigit()):
                        stockMessage = result[1:]
                        for i in range(len(stockMessage)):
                            stock2 = stock2 + ' ' + stockMessage[i]
                    else:
                        stock1 = ''
                        for i in range(len(result)):
                            stock2 = stock2 + ' ' + result[i]
                        stock2 = stock2.strip()
                else:
                    stock1 = ''
                    stock2 = ''
            else:
                stock1 = ''
                stock2 = ''
                # stockQty = ''
        else:
            stock1 = ''
            stock2 = ''
        print("ComStockloc: "+stock1)
        return stock1


    def Warranty(self):
        return ''

    def ColourVariant(self):
        return ''

    def ProductName(self):
        Productnm=''
        result = self.html_Element.find("div", {"id": "pdpProdInfo"})
        if result is not None:
            result2 = result.find("h4", {"class": "panel-title"})
            if result2 is not None:
                Productnm = result2.text.strip()
        print("ProductName: " + Productnm)
        return Productnm

    def discount(self):
        return ''

    def deliveryOptions(self):
        return ''

    def SellerDetails(self):
        return ''

    def Rating(self):
        return ''

    def Brand(self):
        return ''

    def NumberInStock(self):
        return ''

    def Minimum_multiples_breaks(self):
        return ''

    def ItemID(self):
        return ''

    def ListPrice(self):
        return ''

    def PromoPrice(self):
        return ''

    def Currency(self):
        result1 = self.html_Element.find("select", {"id": "SelectedCurrencyId"})
        if result1 is not None:
            result = result1.find("option", {"selected": "selected"})
            if result is not None:
                strCurrency = result.text.strip()
            else:
                strCurrency = ''
        else:
            strCurrency = ''
        print("Currency: " + strCurrency)
        return strCurrency

    def WarrantyType(self):
        return ''

    def Lifecycle(self):
        lifecycle = ''
        result = self.html_Element.find("div", {"id": "product-desc"})
        if result is not None:
            pattern = re.compile(r"Lifecycle:")
            chkData = result.find(text=pattern)
            print(chkData)
            if chkData is not None:
                result = result.find(text=pattern).parent.parent.parent
                if result is not None:
                    span = result.find("div", {"class": "col-xs-8"})
                    if span is not None:
                        lifecycle = span.text.strip()
            else:
                pattern = re.compile(r"寿命周期:")
                chkData = result.find(text=pattern)
                print(chkData)
                if chkData is not None:
                    result = result.find(text=pattern).parent.parent.parent
                    if result is not None:
                        span = result.find("div", {"class": "col-xs-8"})
                        if span is not None:
                            lifecycle = span.text.strip()

        print ('lifecycle: ' + lifecycle)
        return lifecycle

    def Onorder(self):
        OnOrder = ''
        divOnOrder = self.html_Element.find("div", {"class": "pdp-product-availability"})
        if divOnOrder is not None:
            result = divOnOrder.findAll('div', {"class": "row"})
            print(len(result))
            if result is not None:

                if len(result) == 1:

                    result = result[0].text.strip().find('div', {"class": "col-xs-8"})
                elif len(result) == 2:
                    result = result[1].text.strip().find('div', {"class": "col-xs-8"})
                # OnOrder = result.text.strip()

            else:
                OnOrder = ''
        else:
            OnOrder = ''

        return OnOrder

    def FLT(self):
        FLT = ''
        divFLT = self.html_Element.find("div", {"class": "pdp-product-availability"})
        if divFLT is not None:
            result = divFLT.findAll('div', {"class": "row"})
            if result is not None:
                # result1 = result[2].find(('div'), {"class": "col-xs-8"})
                # result3 = result[2].find('label', {"for": "FactoryLeadTime"})
                # if result3 is not None:
                #     FLT = result3.text.strip()
                # else:
                #     FLT = result[2].find('div').text.strip()
                # result1 = result[2].find(('div'), {"class": "col-xs-8"})
                # result3 = result[2].find('label', {"for": "FactoryLeadTime"})
                for div in result:
                    # result1 = div.find(('div'), {"class": "col-xs-8"})
                    result3 = div.find('label', {"for": "FactoryLeadTime"})
                    if result3 is not None:
                        #     FLT = result3.text.strip()
                        if (div.text.find(':') != -1):
                            FLT = div.text.split(':')[1].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        else:
                            FLT = ''
                        # else:
                        #     FLT = result[2].find('div').text.strip()

        print ('FLT: ' + FLT)
        return FLT

    def MinimumQty(self):
         divQuantity = self.html_Element.find("div", {"class": "pdp-buy-button"})
         if divQuantity is not None:
             result = divQuantity.findAll("div", {"class": "row"})
             if result is not None:
                 result = result[0].find('div', {"class": "col-xs-8"})
                 if result is not None:
                     result = result.find("div").text.strip().split(":")
                     print(result)
                     # minQty = re.sub('[^0-9.]', '', result[1])
                     # print(result[0])
                     # print(minQty)
                     # mulQty = re.sub('[^0-9.]', '', result[2])
                     # print(result[2])
                 #quantity = [int(s) for s in result if s.isdigit()]
                 #print(quantity[:])
                 if (len(result) >= 2):
                     minQty = re.sub('[^0-9.]', '', result[1])

                     mulQty = re.sub('[^0-9.]', '', result[2])
                 else:
                     minQty = ''
                     mulQty = ''
             else:
                 minQty = ''
                 mulQty = ''
         else:
             minQty = ''
             mulQty = ''
         print ('minQty: ' + str(minQty))
         print ('mulQty: ' + str(mulQty))
         return minQty

    def MultipleQty(self):
        divQuantity = self.html_Element.find("div", {"class": "pdp-buy-button"})
        if divQuantity is not None:
            result = divQuantity.findAll("div", {"class": "row"})
            if result is not None:
                result = result[0].find('div', {"class": "col-xs-8"})
                if result is not None:
                    result = result.find("div").text.strip().split(":")
                    print(result)
                    # minQty = re.sub('[^0-9.]', '', result[1])
                    # print(result[0])
                    # print(minQty)
                    # mulQty = re.sub('[^0-9.]', '', result[2])
                    # print(result[2])
                # quantity = [int(s) for s in result if s.isdigit()]
                # print(quantity[:])
                if (len(result) >= 2):
                    minQty = re.sub('[^0-9.]', '', result[1])
                    mulQty = re.sub('[^0-9.]', '', result[2])
                else:
                    minQty = ''
                    mulQty = ''
            else:
                minQty = ''
                mulQty = ''
        else:
            minQty = ''
            mulQty = ''
        print('minQty: ' + str(minQty))
        print('mulQty: ' + str(mulQty))
        return mulQty


    def rohs(self):
        list = self.html_Element.find("div", {"class": "div-table specs-table"})
        if list is not None:
        ##    parse RoHS
            RoHS = ''
            pattern = re.compile(r"RoHS:")
            chkData = list.find(text=pattern)
            print(chkData)
            if chkData is not None:
                result = list.find(text=pattern).parent.parent.parent
                if result is not None:
                    result = result.find("div", {"class": "col-xs-5"})
                    if result is not None:
                        RoHS = 'RoHS Compliant'
            print('RoHS: ' + RoHS)
        else:
            RoHS = ''
        return RoHS

    def Factorypackquantity(self):
         spanFPQ=''
         chkData = self.html_Element.find(text=re.compile(r"Factory Pack Quantity:"))
         if chkData is not None:
             result = self.html_Element.find(text=re.compile(r"Factory Pack Quantity")).parent.parent.parent.parent
             if result is not None:
                 span = result.find("div", {"class": "col-xs-5"})
                 if span is not None:
                     spanFPQ = span.text.replace(" ", "").strip()
                 else:
                     spanFPQ = ''
             else:
                 spanFPQ = ''
         else:
             chkData = self.html_Element.find(text=re.compile(r"工厂包装数量:"))
             if chkData is not None:
                 result = self.html_Element.find(text=re.compile(r"工厂包装数量:")).parent.parent.parent.parent
                 if result is not None:
                     span = result.find("div", {"class": "col-xs-5"})
                     if span is not None:
                         spanFPQ = span.text.replace(" ", "").strip()
                     else:
                         spanFPQ = ''
                 else:
                     spanFPQ = ''
             ##    parse Packaging
         print("spanFPQ :" + spanFPQ)
         return spanFPQ

    def Packaging(self):
         list = self.html_Element.find("div", {"class": "div-table specs-table"})
         if list is not None:
             strPackaging = ''
             pattern = re.compile(r"Packaging:")
             chkData = list.find(text=pattern)
             print(chkData)
             if chkData is not None:
                 result = list.find(text=pattern).parent.parent.parent
                 if result is not None:
                     span = result.find("div", {"class": "col-xs-5"})
                     if span is not None:
                         strPackaging = span.text.replace(" ", "").strip()
             else:
                 strPackaging = ''
                 pattern = re.compile(r"封装:")
                 chkData = list.find(text=pattern)
                 print(chkData)
                 if chkData is not None:
                     result = list.find(text=pattern).parent.parent.parent
                     if result is not None:
                         span = result.find("div", {"class": "col-xs-5"})
                         if span is not None:
                             strPackaging = span.text.replace(" ", "").strip()
         else:
             strPackaging = ''

         print("Packaging :" + strPackaging)
         return strPackaging

    def Weight(self):
         list = self.html_Element.find("div", {"class": "div-table specs-table"})
         if list is not None:
             spanUW = ''
             pattern = re.compile(r"Unit Weight:")
             chkData = list.find(text=pattern)
             print(chkData)
             if chkData is not None:
                 result = list.find(text=pattern).parent.parent.parent
                 if result is not None:
                     span = result.find("div", {"class": "col-xs-5"})
                     if result is not None:
                         spanUW = span.text.replace(" ", "").strip()
                         spanUW = str(float(re.sub("\D", "", span.text)) / 10000)
             else:
                 spanUW = ''
                 pattern = re.compile(r"单位重量:")
                 chkData = list.find(text=pattern)
                 print(chkData)
                 if chkData is not None:
                     result = list.find(text=pattern).parent.parent.parent
                     if result is not None:
                         span = result.find("div", {"class": "col-xs-5"})
                         if result is not None:
                             spanUW = span.text.replace(" ", "").strip()
                             spanUW = str(float(re.sub("\D", "", span.text)) / 10000)
         else:
             spanUW = ''

         print("Weight :" + spanUW)
         return spanUW




    def MultisimBlue(self):
        result = self.html_Element.find("div", {"class": "product-desc"})
        if result is not None:
            result = result.find("a", {"title": "Available in MultiSIM BLUE"})
            strMblue = result.text.strip()
        else:
            strMblue = ''
        print("MultisimBlue :" + strMblue)
        return strMblue

    def Countryoforigin(self):
        return ''

    def tariffNo(self):
        return ''

    def BreakQty(self):
        return ''

    def Availability(self):
        return ''

    def marketid(self):
         return 'CN'



