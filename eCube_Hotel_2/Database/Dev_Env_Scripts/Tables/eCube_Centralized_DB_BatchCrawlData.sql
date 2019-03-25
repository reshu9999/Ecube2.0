-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: eCube_Centralized_DB
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BatchCrawlData`
--

DROP TABLE IF EXISTS `BatchCrawlData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BatchCrawlData` (
  `intBatchCrawlID` int(11) NOT NULL AUTO_INCREMENT,
  `intDiPBagDynamicId` int(11) NOT NULL,
  `intSiteID` int(11) DEFAULT NULL,
  `nvcrHotelName` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelAddress` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `ncrPostCode` char(10) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCity` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `intAdult` int(11) DEFAULT NULL,
  `sdtmCheckinDate` datetime DEFAULT NULL,
  `sdtmCheckoutDate` datetime DEFAULT NULL,
  `nvcrRoomType` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `mnyRate` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCurrency` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPagePath` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `sintBatchCrawlStatus` smallint(6) DEFAULT NULL,
  `intSupplierId` int(11) DEFAULT NULL,
  `nvcrBoard` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrAvailabilty` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelStar` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrBreakFast` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCrawlDescription` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRcode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTax` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCancellationPolicy` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrClassification` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDailyRate` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrContractName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrUniqueCode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelCode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrNetPrice` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSellingPrice` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCommision` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDirectPayment` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSellingPriceMandatory` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrXmlroomtypecode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPromotion` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPromotionDescription` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelCount` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTotalHotel` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bitReCrawl` bit(1) DEFAULT NULL,
  `intSubDipbagDynamicId` int(11) DEFAULT NULL,
  `strbreakfast` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `strSupplier` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrZoneinfo` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRoomAvailability` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelLocation` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTaxdesc` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrAdult` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrOpaqueRate` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLeadTime` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDynamicProperty` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSupplierHotelURL` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCompetitorHotelID` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrMultipleZoneCheck` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrGeneralInfo` varchar(250) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrCost` varchar(50) DEFAULT NULL,
  `NvcrCostCurrency` varchar(50) DEFAULT NULL,
  `NvcrTaxIncluded` varchar(50) DEFAULT NULL,
  `NvcrIncluded1` varchar(50) DEFAULT NULL,
  `NvcrTAXNotIncluded` varchar(50) DEFAULT NULL,
  `NvcrNotIncluded1` varchar(50) DEFAULT NULL,
  `nvcrTAX$Included` varchar(50) DEFAULT NULL,
  `NvcrCurrencyIncluded` varchar(50) DEFAULT NULL,
  `NvcrIncluded2` varchar(50) DEFAULT NULL,
  `NvcrTAX$NotIncluded` varchar(50) DEFAULT NULL,
  `NvcrCurrencyNotIncluded` varchar(50) DEFAULT NULL,
  `nvcrNotincluded2` varchar(50) DEFAULT NULL,
  `nvcrRoomChar` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `dtmCrawlDateTime` datetime DEFAULT NULL,
  `nvcrYieldManager` varchar(1000) DEFAULT '',
  `nvcrContractManager` varchar(1000) DEFAULT '',
  `nvcrDemandGroup` varchar(1000) DEFAULT '',
  `nvcrSegmentation` varchar(1000) DEFAULT '',
  `nvcrHotelContractingType` varchar(1000) DEFAULT '',
  `nvcrTPS` varchar(1000) DEFAULT '',
  `nvcrHotelStatus` varchar(1000) DEFAULT '',
  `nvcrHotelChain` varchar(1000) DEFAULT '',
  PRIMARY KEY (`intBatchCrawlID`),
  UNIQUE KEY `intBatchCrawlID` (`intBatchCrawlID`)
) ENGINE=InnoDB AUTO_INCREMENT=942 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-28 19:06:12
