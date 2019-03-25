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
-- Table structure for table `BatchCrawlDatafinal_Hotel_Avail_Last_R`
--

DROP TABLE IF EXISTS `BatchCrawlDatafinal_Hotel_Avail_Last_R`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BatchCrawlDatafinal_Hotel_Avail_Last_R` (
  `nvcrTimestamp` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCompany` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDates` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `Nights` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotel` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `HotelId` varchar(200) DEFAULT NULL,
  `nvcrPointOfSale` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCity` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrState` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCountry` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDailyRate` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `Rcode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTax` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRoomType` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrRoomCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSupplier` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCancellationPolicy` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `StarRating` varchar(50) DEFAULT NULL,
  `nvcrstar` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPrice` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCurrency` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrBreakFast` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrAvailability` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrBoard` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrUniquecode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrStatus` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPageURL` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `HotelCode` varchar(200) DEFAULT NULL,
  `nvcrContractName` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrClassification` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrIntegration` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrB2B` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrComOfici` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrComCanal` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrComNeta` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrnvcrHotelCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `ReportType` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrNetPrice` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSellingPrice` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrCommission` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDirectPayment` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSellingPriceMandatory` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPromotion` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrPromotionDescription` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelCount` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrEventType` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `strSupplier` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `intBatchId` int(11) DEFAULT NULL,
  `intBatchCrawlDataFinalId` int(11) NOT NULL AUTO_INCREMENT,
  `intDipBagDynamicId` int(11) DEFAULT NULL,
  `nvcrRoomAvailability` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrAdult` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrOpaqueRate` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLeadTime` longtext,
  `nvcrAccountName` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrDynamicProperty` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `HMHotelID` int(11) DEFAULT NULL,
  `HotelAddress` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrSupplierHotelURL` longtext,
  `nvcrCompetitorHotelID` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `MasterID` int(11) DEFAULT NULL,
  `Batch_Name` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrYieldManager` longtext,
  `nvcrContractManager` longtext,
  `nvcrDemandGroup` longtext,
  `nvcrSegmentation` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelChain` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelContractingType` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrTPS` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelStatus` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `intBatchCrawlDataFinalId` (`intBatchCrawlDataFinalId`)
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

-- Dump completed on 2018-06-29 16:00:35
