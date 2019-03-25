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
-- Table structure for table `ReportData`
--

DROP TABLE IF EXISTS `ReportData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ReportData` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parseobjId` varchar(100) DEFAULT NULL,
  `intBatchCrawlID` varchar(50) DEFAULT NULL,
  `intDiPBagDynamicId` varchar(20) DEFAULT NULL,
  `intSiteID` varchar(20) DEFAULT NULL,
  `nvcrHotelName` varchar(60) DEFAULT NULL,
  `nvcrHotelAddress` varchar(60) DEFAULT NULL,
  `ncrPostCode` varchar(15) DEFAULT NULL,
  `nvcrCity` varchar(50) DEFAULT NULL,
  `intAdult` int(11) DEFAULT NULL,
  `sdtmCheckinDate` datetime NOT NULL,
  `sdtmCheckoutDate` datetime NOT NULL,
  `nvcrRoomType` varchar(100) DEFAULT NULL,
  `mnyRate` int(11) DEFAULT NULL,
  `nvcrCurrency` varchar(5) DEFAULT NULL,
  `nvcrPagePath` varchar(100) DEFAULT NULL,
  `sintBatchCrawlStatus` int(11) DEFAULT NULL,
  `intSupplierId` int(11) DEFAULT NULL,
  `nvcrBoard` varchar(100) DEFAULT NULL,
  `nvcrAvailabilty` varchar(50) DEFAULT NULL,
  `nvcrHotelStar` varchar(15) DEFAULT NULL,
  `nvcrBreakFast` varchar(15) DEFAULT NULL,
  `nvcrCrawlDescription` varchar(50) DEFAULT NULL,
  `nvcrRcode` varchar(50) DEFAULT NULL,
  `nvcrTax` varchar(50) DEFAULT NULL,
  `nvcrCancellationPolicy` varchar(100) DEFAULT NULL,
  `nvcrClassification` varchar(100) DEFAULT NULL,
  `nvcrDailyRate` varchar(50) DEFAULT NULL,
  `nvcrContractName` varchar(50) DEFAULT NULL,
  `nvcrUniqueCode` varchar(50) DEFAULT NULL,
  `nvcrHotelCode` varchar(50) DEFAULT NULL,
  `nvcrNetPrice` varchar(50) DEFAULT NULL,
  `nvcrSellingPrice` varchar(50) DEFAULT NULL,
  `nvcrCommision` varchar(50) DEFAULT NULL,
  `nvcrDirectPayment` varchar(50) DEFAULT NULL,
  `nvcrSellingPriceMandatory` varchar(50) DEFAULT NULL,
  `nvcrXmlroomtypecode` varchar(50) DEFAULT NULL,
  `nvcrPromotion` varchar(50) DEFAULT NULL,
  `nvcrPromotionDescription` varchar(100) DEFAULT NULL,
  `nvcrHotelCount` varchar(20) DEFAULT NULL,
  `nvcrTotalHotel` varchar(20) DEFAULT NULL,
  `bitReCrawl` varchar(20) DEFAULT NULL,
  `intSubDipbagDynamicId` int(11) DEFAULT NULL,
  `strbreakfast` varchar(50) DEFAULT NULL,
  `strSupplier` varchar(50) DEFAULT NULL,
  `nvcrZoneinfo` varchar(50) DEFAULT NULL,
  `nvcrRoomAvailability` varchar(10) DEFAULT NULL,
  `nvcrHotelLocation` varchar(50) DEFAULT NULL,
  `nvcrTaxdesc` varchar(50) DEFAULT NULL,
  `nvcrAdult` varchar(50) DEFAULT NULL,
  `nvcrOpaqueRate` varchar(15) DEFAULT NULL,
  `nvcrLeadTime` varchar(15) DEFAULT NULL,
  `nvcrDynamicProperty` varchar(15) DEFAULT NULL,
  `nvcrSupplierHotelURL` varchar(50) DEFAULT NULL,
  `nvcrCompetitorHotelID` varchar(15) DEFAULT NULL,
  `nvcrLongitude` varchar(50) DEFAULT NULL,
  `nvcrLatitude` varchar(50) DEFAULT NULL,
  `nvcrMultipleZoneCheck` varchar(20) DEFAULT NULL,
  `nvcrGeneralInfo` varchar(20) DEFAULT NULL,
  `NvcrCos` varchar(20) DEFAULT NULL,
  `NvcrCostCurrency` varchar(10) DEFAULT NULL,
  `NvcrTaxIncluded` varchar(20) DEFAULT NULL,
  `NvcrIncluded1` varchar(10) DEFAULT NULL,
  `NvcrTAXNotIncluded` varchar(15) DEFAULT NULL,
  `NvcrNotIncluded1` varchar(10) DEFAULT NULL,
  `nvcrTAXaIncluded` varchar(10) DEFAULT NULL,
  `NvcrCurrencyIncluded` varchar(20) DEFAULT NULL,
  `NvcrIncluded2` varchar(20) DEFAULT NULL,
  `NvcrTAXaNotIncluded` varchar(20) DEFAULT NULL,
  `NvcrCurrencyNotIncluded` varchar(20) DEFAULT NULL,
  `nvcrNotincluded2` varchar(20) DEFAULT NULL,
  `nvcrRoomChar` varchar(30) DEFAULT NULL,
  `dtmCrawlDateTime` datetime NOT NULL,
  `samId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 16:00:30
