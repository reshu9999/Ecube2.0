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
-- Table structure for table `tbl_RequestRunDetail`
--

DROP TABLE IF EXISTS `tbl_RequestRunDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_RequestRunDetail` (
  `RequestRunId` int(11) NOT NULL AUTO_INCREMENT,
  `FK_RequestId` int(11) DEFAULT NULL,
  `ScheduleDateId` int(11) DEFAULT NULL,
  `TotalRequests` int(11) DEFAULT NULL,
  `CompletedRequests` int(11) DEFAULT NULL,
  `InQueRequests` int(11) DEFAULT NULL,
  `PNFCounts` int(11) DEFAULT NULL,
  `ReportDownloadLink` varchar(1000) DEFAULT NULL,
  `FK_StatusId` varchar(30) DEFAULT NULL,
  `StartDatetIme` datetime DEFAULT NULL,
  `EndDateTime` datetime DEFAULT NULL,
  `ReParseStatus` varchar(100) DEFAULT NULL,
  `TotalInputs` int(11) DEFAULT NULL,
  PRIMARY KEY (`RequestRunId`),
  KEY `FK_RequestId` (`FK_RequestId`),
  CONSTRAINT `tbl_RequestRunDetail_ibfk_1` FOREIGN KEY (`FK_RequestId`) REFERENCES `tbl_RequestMaster` (`RequestId`)
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

-- Dump completed on 2018-06-28 19:06:11
