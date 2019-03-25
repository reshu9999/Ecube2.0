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
-- Table structure for table `LastResultQACheck`
--

DROP TABLE IF EXISTS `LastResultQACheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LastResultQACheck` (
  `BIntLastResultID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Timestamp` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Company` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Dates` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Nights` int(11) DEFAULT NULL,
  `Hotel` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `HotelId` bigint(20) DEFAULT NULL,
  `PointOfSale` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `City` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `State` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Country` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `DailyRate` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Rcode` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Tax` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `RoomType` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `RoomCode` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Supplier` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `CancellationPolicy` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `StarRating` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Star` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Price` varchar(500) DEFAULT NULL,
  `Currency` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `BreakFast` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Availability` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Board` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Uniquecode` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Status` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `PageURL` longtext,
  `HotelCode` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `ContractName` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Classification` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Integration` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `B2B` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `ComOfici` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `ComCanal` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `ComNeta` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelCode` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `tintReportType` tinyint(3) unsigned DEFAULT NULL,
  `intMSTHotelId` bigint(20) DEFAULT NULL,
  `intSupplierId` int(11) DEFAULT NULL,
  `nvcrHotelName` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
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
  `nvcrEventType` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `Unq_HotelID` bigint(20) DEFAULT NULL,
  `strSupplier` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRoomAvailability` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrAdult` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrOpaqueRate` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLeadTime` longtext,
  `nvcrAccountName` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDynamicProperty` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelAddress1` longtext,
  `dtmCrawlDateTime` datetime(3) DEFAULT NULL,
  `sdtmCheckinDate` datetime DEFAULT NULL,
  `intDiPBagDynamicId` int(11) DEFAULT NULL,
  `nvcrCity` longtext,
  `nvcrSupplierHotelURL` longtext,
  `nvcrCompetitorHotelID` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrCost` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrCostCurrency` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrTaxIncluded` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrIncluded1` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrTAXNotIncluded` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrNotIncluded1` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTAX$Included` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrCurrencyIncluded` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrIncluded2` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrTAX$NotIncluded` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `NvcrCurrencyNotIncluded` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrNotincluded2` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRoomChar` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrMultipleZoneCheck` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCheckinDates` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`BIntLastResultID`)
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

-- Dump completed on 2018-06-28 19:06:09
