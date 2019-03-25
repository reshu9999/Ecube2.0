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
-- Table structure for table `tbl_ProxyTransactionDetails`
--

DROP TABLE IF EXISTS `tbl_ProxyTransactionDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_ProxyTransactionDetails` (
  `ProxyTransactionDetailsId` int(11) NOT NULL AUTO_INCREMENT,
  `ProxyFirstUsedDate` date DEFAULT NULL,
  `ProxyLastUsedDate` date DEFAULT NULL,
  `SuccessHits` int(11) DEFAULT NULL,
  `ProxyStatus` varchar(10) DEFAULT NULL,
  `TimeZone` varchar(100) DEFAULT NULL,
  `TimeDiffinminutes` int(11) DEFAULT NULL,
  `ActiveFlag` tinyint(1) DEFAULT NULL,
  `PTD_ProxyId` int(11) DEFAULT NULL,
  `PTD_DomainId` int(11) DEFAULT NULL,
  `PTD_CountryId` int(11) DEFAULT NULL,
  `PTD_RegionId` int(11) DEFAULT NULL,
  `CreatedDate` datetime DEFAULT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  PRIMARY KEY (`ProxyTransactionDetailsId`),
  KEY `PTD_ProxyId` (`PTD_ProxyId`),
  KEY `PTD_DomainId` (`PTD_DomainId`),
  KEY `PTD_CountryId` (`PTD_CountryId`),
  KEY `PTD_RegionId` (`PTD_RegionId`)
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

-- Dump completed on 2018-06-28 19:06:10
