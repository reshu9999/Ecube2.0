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
-- Table structure for table `BatchCrawlData_detail_Y`
--

DROP TABLE IF EXISTS `BatchCrawlData_detail_Y`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BatchCrawlData_detail_Y` (
  `ReportDelivery` varchar(500) DEFAULT NULL,
  `Hotel` varchar(2000) CHARACTER SET utf8 DEFAULT NULL,
  `HotelCode` varchar(1000) DEFAULT NULL,
  `ContractManager` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `YieldManager` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `DemandGroup` varchar(500) DEFAULT NULL,
  `Segmentation` varchar(500) DEFAULT NULL,
  `ChainName` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `Status` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `HotelContractingType` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `TPS` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `Dates` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `leadtime` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `PointOfSale` longtext,
  `Currency` longtext,
  `BedsonlinePrice` longtext,
  `BedsonlineRoomType` longtext,
  `BedsonlineBoardType` varchar(2000) CHARACTER SET utf8 DEFAULT NULL,
  `ContractName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `RoomAvailability` longtext,
  `BedsOnlinePageURL` longtext,
  `CompetitorName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorPrice` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorRoomType` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorBoardType` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorPageURL` longtext,
  `Destination` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `DestinationCode` varchar(500) CHARACTER SET utf8 DEFAULT NULL
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

-- Dump completed on 2018-06-28 19:06:12
