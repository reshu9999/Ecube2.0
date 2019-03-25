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
-- Table structure for table `HotelRelationCleared`
--

DROP TABLE IF EXISTS `HotelRelationCleared`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HotelRelationCleared` (
  `HotelRelationId` bigint(20) NOT NULL,
  `HotelId` bigint(20) NOT NULL,
  `HotelRelationComHotelId` bigint(20) NOT NULL,
  `isHotelRelationManualMatch` tinyint(1) NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `AdminUserId` int(11) NOT NULL,
  `MatchDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `MatchingRunId` int(11) DEFAULT NULL,
  `MatchedInStepNo` int(11) DEFAULT NULL,
  `MatchingScore` decimal(5,2) DEFAULT NULL,
  `HotelNamePer` decimal(5,2) DEFAULT NULL,
  `HotelAddressPer` decimal(5,2) DEFAULT NULL,
  `GeoCoordinatesPer` decimal(5,2) DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  `ModifiedDatetime` datetime DEFAULT NULL,
  `LastFlagStatus` int(11) NOT NULL DEFAULT '0',
  `LastFlagStatusDateTime` datetime DEFAULT NULL
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

-- Dump completed on 2018-06-29 15:20:33
