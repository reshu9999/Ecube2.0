import re
import datetime
import numpy as np
import pandas as pd

from copy import deepcopy
from lxml import html, etree
from Parsing.scripts.Hotelbeds_Availability import ParserConfigBedsonlinePython
from Parsing.scripts.core.logs import ParsingLogger
from Parsing.scripts.core.base import ParserBase, ParamParser


class HotelbedsLogger(ParsingLogger):
    NAME = 'Hotelbeds_parsing'


HotelbedsLogger.set_logger()
ParamParser.DATA_TYPE = 'XPATH'
ParserBase.TRL = HotelbedsLogger
ParserBase.CONFIG_FILE = ParserConfigBedsonlinePython


class Hotel(ParserBase):
    PROPERTIES = [
        # ParamParser('address', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__address, 'single_obj_array'),
        ParamParser('hotelName', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__name, 'single_obj_array'),
        # ParamParser('starRating', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__starRating, 'single_obj_array'),
        ParamParser('latitude', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__Lattitude, 'single_obj_array'),
        ParamParser('longitude', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__Longitude, 'single_obj_array'),
        # ParamParser('city_zone', 'hotel_data_html', ParserBase.CONFIG_FILE.Hotel__zonename, 'single_obj_array'),
    ]

    EXTRA_FIELDS = ['city', 'index', 'page_path', 'total_hotel','adult','city_zone','hotelcode','starRating']

    def __init__(self, parser_data):
        # self.hotel_data_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['html_element'])
        # self.latitude_html = html.document_fromstring(parser_data['htmls']['hotelHTML']['latitude_html']['html_element'])
        self.hotel_data_html = etree.fromstring(parser_data['htmls']['landingPage']['hotel_html'])
        # self.latitude_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML']['latitude_html']['html_element'])

        super().__init__(parser_data)

    @classmethod
    def get_starRating(cls, star_code):

        star_rating = re.findall(r'[1-9]', star_code)
        star_rating = "".join(star_rating)
        try:
            if int(star_rating) >= 10:
                return str(int(star_rating) / 10)
            else:
                return star_rating
        except:
            return ""

    @property
    def parsed__supplier(self):
        return

    @property
    def parsed__city(self):
        return self.parser_data['city']

    @property
    def parsed__city_zone(self):
        return self.parser_data['city_zone']

    @property
    def parsed__hotelcode(self):
        hotelcode = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__hotelcode)[0]
        return hotelcode

    @property
    def parsed__starRating(self):
        star_code = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__starRating)[0]
        starRating = self.__class__.get_starRating(star_code)
        starRating=starRating.replace(".0","")
        return starRating

    @property
    def parsed__adult(self):
        return self.parser_data['adults']

    # @property
    # def parsed__website_id(self):
    #     return self.parser_data['hotel_id']

    @property
    def parsed__index(self):
        return self.parser_data['index']

    @property
    def parsed__total_hotel(self):
        return self.parser_data['hotel_count']

    @property
    def parsed__page_path(self):
        return self.parser_data['meta']['cachePageURL']


class RoomType(ParserBase):
    PROPERTIES = []

    EXTRA_FIELDS = ['room_types']

    def __init__(self, parser_data):
        self.hotel_data_html = html.document_fromstring(parser_data['roomTypes']['roomTypeHTML'])
        super().__init__(parser_data)

    @classmethod
    def get_board_code(cls, code):
        if code in ["SA", "SC", "BM"]:
            return "RO"
        elif code in ["AD", "DB", "HD", "BB", "DE", "BF", "FF", "DA", "EB", "DI", "HA", "AP", "SB", "AB", "CB", "DC",
                      "HC", "CP", "GB", "LC", "DE", "AP", "BB", "CB", "CP", "DA", "DB", "DC", "HA", "HC", "HD", "BF",
                      "SB", "FF", "DI", "HP", "IB", "GB", "HF", "AD", "BM", "BR"]:
            return "BB"
        elif code in ["MP", "HB", "CE", "CB", "CO", "AB", "AC", "EO", "OE", "MS", "MF", "MB", "MP", "CE", "HB", "AB",
                      "CO", "AL", "OE", "BD", "DR", "LU", "BH"]:
            return "HB"
        elif code in ["PC", "FB", "CS", "EO", "PB", "PC", "FB", "FH"]:
            return "FB"
        elif code in ["SH", "RO", "SA", "SP", "RO", "SA", "SC", "SH", "AF", "X0"]:
            return "RO"
        elif code in ["TG", "TS", "MA", "NW", "UU", "TI", "SU", "AI", "AE", "TL", "T2", "UA", "AS", "PA", "TI", "T2",
                      "TL", "AE", "AP", "HA", "DA", "MA", "NW", "SU", "UA", "UU"]:
            return "AI"
        elif code in ["PF", "XX", "EB", "PQ", "FC", "EX", "RC", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"]:
            return "X1"
        else:
            return "RO"

    @classmethod
    def get_promotion(cls, priceblock):
        promotions = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__promotions)
        offers = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__offers)
        promoDesc = ""
        isPromotion = "N"
        if len(promotions):
            isPromotion = "Y"
            promoDesc = promoDesc.join(promotions)
        if len(offers):
            isPromotion = "Y"
            promoDesc = promoDesc.join(offers)
        if "Non-refundable rate" in promoDesc:
            promoDesc = "Non-refundable rate"
        return isPromotion, promoDesc

    @property
    def parsed__room_types(self):
        """
        :return:
        """
        checkIn = datetime.datetime.strptime(self.parser_data['checkIn'], "%Y-%m-%d %H:%M:%S")
        checkOut = datetime.datetime.strptime(self.parser_data['checkOut'], "%Y-%m-%d %H:%M:%S")
        no_of_days = (checkOut - checkIn).days

        roomtypes = []
        currency = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Hotel__currency)[0]
        containers = self.hotel_data_html.xpath(ParserBase.CONFIG_FILE.Roomtype__containers)
        hotelchain_chk=self.parser_data['HotelChain_value']
        if hotelchain_chk.upper()=="Accor Hotels".upper() or hotelchain_chk.upper()=="Hilton Worldwide".upper() or hotelchain_chk.upper()=="Hyatt".upper() or hotelchain_chk.upper()=="Starwood".upper():
            rota1=100
            lup_chk=1
        else:
            rota1=1
            lup_chk = 0
        for container in containers[0:1]:
            roomtype = str(container.xpath(ParserBase.CONFIG_FILE.RoomType__type)[0]).strip()
            room_code = str(container.xpath(ParserBase.CONFIG_FILE.Hotel__roomCode)[0]).strip()
            priceblocks = container.xpath(ParserBase.CONFIG_FILE.RoomType__priceblocks)
            for priceblock in priceblocks[0:rota1]:
                price = priceblock.xpath(ParserBase.CONFIG_FILE.RoomType__price)[0]
                # try:
                #     promotionDesc = priceblock.xpath(ParserBase.CONFIG_FILE.RoomType__promotion)[0]
                #     promocode = priceblock.xpath(ParserBase.CONFIG_FILE.RoomType__promotioncode)[0]
                #     promotion ='Y'
                #
                # except:
                #     promotionDesc=''
                #     promotion='N'
                #     promocode ='N'

                isPromotion, promoDesc = self.__class__.get_promotion(priceblock)

                commission = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__commission)
                if len(commission) > 0:
                    commission = commission[0]

                contractName = ""
                contractName = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__contract)[0]

                len_contractName = len(contractName.split("|"))
                Roomcharval = ""
                Roomcharval = contractName.split("|")[5]

                contractName1 = contractName.split("|")[6]  # 6th element in the list
                if len_contractName > 7:
                    contractName2 = contractName.split("|")[8]
                    if contractName2 != "":
                        contractName = contractName1 + "#" + contractName2
                    else:
                        contractName = contractName1
                else:
                    contractName2 = contractName1
                    contractName = contractName2

                Integration = ""
                Integration1 = contractName.split("B2B_")
                if len(Integration1) > 0 and contractName.rfind("B2B_") > 0:
                    Integration2 = Integration1[1]
                    Integration = Integration2.split("#")[0]
                elif contractName.rfind("_") > 0 and Integration == "":
                    posintegartion = contractName.rfind("_")
                    Integration = contractName[posintegartion:len(contractName)]
                else:
                    Integration = ""

                room_availability = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__roomAvailability)[0]

                costTaxpercent = ""
                strTaxAmount1 = ""
                strPercentageinctax = ""
                strFixedTaxCurr1 = ""
                strTaxAmount1 = ""
                strFixedIncludedTax1 = ""
                costTaxpercentnotinc = ""
                strTaxAmount2 = ""
                strFixedTaxCurr2 = ""
                strFixedNotIncludedTax1 = ""
                strPercentagenotinctax = ""

                #from pdb import set_trace; set_trace()
                tax_details=priceblock.xpath("./taxes/tax/@included")
                for strPercentageIncludedTax in tax_details:
                    if strPercentageIncludedTax=="true":
                        costTaxpercent = priceblock.xpath("*/tax[@included='true']/@percent")
                        if len(costTaxpercent)==0:
                            costTaxpercent=""
                        strTaxAmount1 = priceblock.xpath("*/tax[@included='true']/@clientamount")
                        # if len(strTaxAmount1) == 0:
                        #     strTaxAmount1 = priceblock.xpath("*/tax[@included='true']/@amount")
                        if len(strTaxAmount1)==0:
                            strTaxAmount1=""
                        if len(costTaxpercent)>0:
                            costTaxpercent = costTaxpercent[0].replace(".00", "").replace("0.00","")
                            strPercentageinctax = "Y"
                        if len(strTaxAmount1)>0:
                            strFixedTaxCurr1 = priceblock.xpath("*/tax[@included='true']/@clientcurrency")
                            if len(strFixedTaxCurr1)>0:
                                strFixedTaxCurr1=strFixedTaxCurr1[0]
                            # if len(strFixedTaxCurr1)==0:
                            #     strFixedTaxCurr1 = priceblock.xpath("*/tax[@included='true']/@currency")[0]
                            strTaxAmount1 = strTaxAmount1[0].replace(".00", "").replace("0.00", "")
                            strFixedIncludedTax1 = "Y"
                    elif strPercentageIncludedTax=="false":
                        costTaxpercentnotinc = priceblock.xpath("*/tax[@included='false']/@percent")
                        if len(costTaxpercentnotinc)==0:
                            costTaxpercentnotinc=""
                        strTaxAmount2 = priceblock.xpath("*/tax[@included='false']/@clientamount")
                        # if len(strTaxAmount2) == 0:
                        #     strTaxAmount2 = priceblock.xpath("*/tax[@included='false']/@amount")
                        if len(strTaxAmount2)==0:
                            strTaxAmount2=""
                        if len(costTaxpercentnotinc)>0:
                            costTaxpercentnotinc = costTaxpercentnotinc[0].replace(".00", "").replace("0.00","")
                            strPercentagenotinctax = "Y"
                        if len(strTaxAmount2)>0:
                            strFixedTaxCurr2 = priceblock.xpath("*/tax[@included='false']/@clientcurrency")
                            if len(strFixedTaxCurr2)>0:
                                strFixedTaxCurr2=strFixedTaxCurr2[0]
                            # if len(strFixedTaxCurr2) ==0:
                            #     strFixedTaxCurr2 = priceblock.xpath("*/tax[@included='false']/@currency")[0]
                            strTaxAmount2 = strTaxAmount2[0].replace(".00", "").replace("0.00", "")
                            strFixedNotIncludedTax1 = "Y"
                    else:
                        jj=1


                StrOpaque = ""
                StrOpaque = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__opaque)[0]
                if StrOpaque == "true":
                    OpaqueRate = "Y"
                elif StrOpaque == "false":
                    OpaqueRate = "N"

                classification = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__classification)[0]

                directPayment = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__directPayment)[0]

                costCurrency=""
                cost=""
                #from pdb import set_trace; set_trace()
                if len(priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__cost))>0:
                    cost = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__cost)[0]
                    costCurrency = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__currency)[0]
                netPrice=""
                sellingPrice=""
                if len(priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__netPrice))>0:
                    netPrice = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__netPrice)[0]
                if len(priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__sellingPrice))>0:
                    sellingPrice = priceblock.xpath(ParserBase.CONFIG_FILE.Hotel__sellingPrice)[0]

                boardtype = str(priceblock.xpath(ParserBase.CONFIG_FILE.RoomType__boardType)[0]).strip()
                boardtype = self.__class__.get_board_code(boardtype)


                roomtypes.append({"rcode":"0",
                                  'breakfast': 0,
                                  "type": roomtype,
                                  "contractName": contractName,
                                  "Opaquerate":OpaqueRate,
                                  "roomAvailability": int(room_availability),
                                  "board_code": boardtype,
                                  "price": float(sellingPrice) if sellingPrice!="" else "",
                                  "commision": float(commission) if commission!=[] else "0",
                                  "selling_price_mandatory":"N",
                                  "promotion": isPromotion,
                                  "promotionDescription": promoDesc.strip() if isPromotion else "",
                                  'availability':'Available',
                                  'currency':currency,"paymentOption": "Y" if directPayment == "AT_HOTEL" else "N",
                                  "daily_price": round(float(sellingPrice) / no_of_days, 2) if sellingPrice!="" else "",
                                  "costCurrency": costCurrency,
                                  "tax_included": costTaxpercent,
                                  "included1": strPercentageinctax,
                                  "tax_not_included": costTaxpercentnotinc,
                                  "classification": classification,
                                  "not_included": strPercentagenotinctax,
                                  "tax$included": strTaxAmount1,
                                  "currency_inlcuded": str(strFixedTaxCurr1),
                                  "included2": strFixedIncludedTax1,
                                  "tax$not_included": strTaxAmount2,
                                  "currency_not_included": str(strFixedTaxCurr2),
                                  "not_included2": strFixedNotIncludedTax1,
                                  "Integration": Integration,
                                  "Roomcharval":Roomcharval,
                                  "netPrice": float(netPrice) if netPrice!="" else "",
                                  "sellingPrice": float(sellingPrice) if sellingPrice!="" else "",
                                  "cost": cost,"costCurrency": costCurrency})

                if lup_chk==1:
                    roomtypes.append({"rcode": "0",
                                      'breakfast': 0,
                                      "type": roomtype,
                                      "contractName": contractName,
                                      "Opaquerate": OpaqueRate,
                                      "roomAvailability": int(room_availability),
                                      "board_code": boardtype,
                                      "price": float(sellingPrice) if sellingPrice != "" else "",
                                      "commision": float(commission) if commission != [] else "0",
                                      "selling_price_mandatory": "N",
                                      "promotion": isPromotion,
                                      "promotionDescription": promoDesc.strip() if isPromotion else "",
                                      'availability': 'Available',
                                      'currency': currency,
                                      "paymentOption": "Y" if directPayment == "AT_HOTEL" else "N",
                                      "daily_price": round(float(sellingPrice) / no_of_days,
                                                           2) if sellingPrice != "" else "",
                                      "costCurrency": costCurrency,
                                      "tax_included": costTaxpercent,
                                      "included1": strPercentageinctax,
                                      "tax_not_included": costTaxpercentnotinc,
                                      "classification": classification,
                                      "not_included": strPercentagenotinctax,
                                      "tax$included": strTaxAmount1,
                                      "currency_inlcuded": str(strFixedTaxCurr1),
                                      "included2": strFixedIncludedTax1,
                                      "tax$not_included": strTaxAmount2,
                                      "currency_not_included": str(strFixedTaxCurr2),
                                      "not_included2": strFixedNotIncludedTax1,
                                      "Integration": Integration,
                                      "Roomcharval": Roomcharval,
                                      "netPrice": float(netPrice) if netPrice != "" else "",
                                      "sellingPrice": float(sellingPrice) if sellingPrice != "" else "",
                                      "cost": cost, "costCurrency": costCurrency})
                    lup_chk=0
        return roomtypes


def crawl_hotels(parser_data):
    """
    :param parser_data:
    :return:
    """
    #from pdb import set_trace; set_trace()
    response = parser_data.copy()
    #response['hotels'] = [crawl_hotel(hotel_data) for hotel_data in parser_data['hotels']]
    response['hotel'] = crawl_hotel(parser_data['hotel'])
    return response


def crawl_hotel(hotel_data):
    hotel_meta = hotel_data['meta'].copy()
    hotel_payload = Hotel(hotel_data).complete_parsed_values
    room_types_payload = RoomType(hotel_data).complete_parsed_values
    mongo_data = dict()
    mongo_data.update(hotel_payload)
    mongo_data.update(room_types_payload)
    mongo_data.update({'meta': hotel_meta})
    return mongo_data
