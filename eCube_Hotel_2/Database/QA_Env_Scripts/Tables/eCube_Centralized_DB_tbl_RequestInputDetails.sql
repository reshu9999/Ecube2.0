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
-- Table structure for table `tbl_RequestInputDetails`
--

DROP TABLE IF EXISTS `tbl_RequestInputDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_RequestInputDetails` (
  `ReqInputDetailId` int(11) NOT NULL AUTO_INCREMENT,
  `FK_RequestId` int(11) DEFAULT NULL,
  `RequestURL` varchar(500) DEFAULT NULL,
  `FK_DomainId` int(11) DEFAULT NULL,
  `RequestTypeId` int(11) DEFAULT NULL,
  `CreatedDatetime` datetime DEFAULT NULL,
  `UpdatedDatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`ReqInputDetailId`),
  KEY `FK_DomainId` (`FK_DomainId`),
  KEY `tbl_RequestInputDetails_ibfk_1_idx` (`FK_RequestId`),
  CONSTRAINT `tbl_RequestInputDetails_ibfk_1` FOREIGN KEY (`FK_RequestId`) REFERENCES `tbl_RequestMaster` (`RequestId`),
  CONSTRAINT `tbl_RequestInputDetails_ibfk_2` FOREIGN KEY (`FK_DomainId`) REFERENCES `tbl_DomainMaster` (`DomainId`)
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

-- Dump completed on 2018-06-29 15:05:55
