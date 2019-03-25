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
-- Table structure for table `TempHotelMaster`
--

DROP TABLE IF EXISTS `TempHotelMaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TempHotelMaster` (
  `Websitehotelcode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Hotelname` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `Starrating` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `Address1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `Countrycode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Countryname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `ZipCode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Longitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Latitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Citycode` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Cityname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrHotelStatus` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `nvcrYieldManager` longtext,
  `nvcrContractManager` longtext,
  `nvcrDemandGroup` longtext,
  `Countryid` int(11) DEFAULT NULL,
  `Cityid` int(11) DEFAULT NULL,
  `Hotelid` int(11) DEFAULT NULL,
  `ErrorStatus` longtext,
  `ErrorFlag` int(11) DEFAULT NULL,
  `OrignalCityName` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `OrignalCountryName` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `RecRowId` int(11) NOT NULL AUTO_INCREMENT,
  `IntHotelStatusID` int(11) DEFAULT NULL,
  UNIQUE KEY `RecRowId` (`RecRowId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 15:13:44
