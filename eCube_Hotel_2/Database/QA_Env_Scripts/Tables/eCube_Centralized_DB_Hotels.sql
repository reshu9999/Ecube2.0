-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
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
-- Table structure for table `Hotels`
--

DROP TABLE IF EXISTS `Hotels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Hotels` (
  `HotelId` bigint(20) NOT NULL AUTO_INCREMENT,
  `WebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `HotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
  `HotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `HotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `CityId` int(11) NOT NULL,
  `HotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `StarRatingId` int(11) DEFAULT NULL,
  `HotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorId` int(11) DEFAULT NULL,
  `HotelMatchStatus` tinyint(1) DEFAULT NULL,
  `HotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `isProceesed` tinyint(1) DEFAULT '0',
  `matchhotelname` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `DipBagSyncId` int(11) DEFAULT NULL,
  `IsMailed` tinyint(1) DEFAULT '0',
  `RequestId` int(11) DEFAULT NULL,
  `ismailed1` tinyint(1) DEFAULT NULL,
  `Active` tinyint(1) DEFAULT '1',
  `CreatedBy` int(11) NOT NULL,
  `CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `ModifiedBy` int(11) DEFAULT NULL,
  `ModifiedDatetime` datetime DEFAULT NULL,
  `MatchHotelAddress1` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `isConsiderForMatching` tinyint(1) DEFAULT NULL,
  `LastAppearnceDate` datetime DEFAULT NULL,
  `LastRequestRunId` int(11) DEFAULT NULL,
  `Longitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Latitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `YieldManager` varchar(3000) CHARACTER SET utf8 DEFAULT NULL,
  `ContractManager` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `DemandGroup` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `CrawledHotelAddress` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
  `CrawledHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  `ZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `CrawledZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `HotelStatusId` int(11) DEFAULT NULL,
  `Segmentation` longtext,
  `HotelChain` longtext,
  `HotelContractingType` longtext,
  `TPS` longtext,
  PRIMARY KEY (`HotelId`),
  KEY `CityId` (`CityId`),
  KEY `RequestId` (`RequestId`),
  KEY `Hotels_HotelStatus_HotelStatusId` (`HotelStatusId`),
  KEY `WebSiteHotelId` (`WebSiteHotelId`),
  KEY `HotelName` (`HotelName`),
  KEY `HotelAddress1` (`HotelAddress1`),
  KEY `nonix_MSTHotel` (`CompetitorId`,`CityId`,`StarRatingId`,`WebSiteHotelId`,`HotelName`,`HotelAddress1`)
) ENGINE=InnoDB AUTO_INCREMENT=7370835 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 15:20:08
