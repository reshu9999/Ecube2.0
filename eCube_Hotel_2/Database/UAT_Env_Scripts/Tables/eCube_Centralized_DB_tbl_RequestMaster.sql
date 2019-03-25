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
-- Table structure for table `tbl_RequestMaster`
--

DROP TABLE IF EXISTS `tbl_RequestMaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_RequestMaster` (
  `RequestId` int(11) NOT NULL AUTO_INCREMENT,
  `FK_BLIId` int(11) DEFAULT NULL,
  `RequestName` varchar(100) DEFAULT NULL,
  `RequestDescription` varchar(500) DEFAULT NULL,
  `RequestFile` varchar(500) DEFAULT NULL,
  `CategoryCount` int(11) DEFAULT NULL,
  `ProductCount` int(11) DEFAULT NULL,
  `MPN_SKUCount` int(11) DEFAULT NULL,
  `FK_StatusId` int(11) DEFAULT NULL,
  `FK_GroupId` int(11) DEFAULT NULL,
  `CreatedBy` varchar(500) DEFAULT NULL,
  `CreatedDatetime` datetime DEFAULT NULL,
  `UpdatedBy` varchar(500) DEFAULT NULL,
  `UpdatedDatetime` datetime DEFAULT NULL,
  `NextScheduleDateTime` datetime DEFAULT NULL,
  `FK_ScheduleTypeId` int(11) DEFAULT NULL,
  `RequestModeId` int(11) DEFAULT NULL,
  `IsPNFStopper` tinyint(1) DEFAULT NULL,
  `ReportFlag` tinyint(1) DEFAULT NULL,
  `Email` varchar(1000) DEFAULT NULL,
  `EmailCC` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`RequestId`),
  KEY `FK_BLIId` (`FK_BLIId`),
  KEY `FK_GroupId` (`FK_GroupId`),
  KEY `FK_StatusId` (`FK_StatusId`),
  KEY `tbl_requestmaster_RequestMode_RequestModeId` (`RequestModeId`),
  CONSTRAINT `tbl_RequestMaster_ibfk_1` FOREIGN KEY (`FK_BLIId`) REFERENCES `tbl_BliMaster` (`BliId`),
  CONSTRAINT `tbl_RequestMaster_ibfk_2` FOREIGN KEY (`FK_GroupId`) REFERENCES `tbl_Field_Group_Master` (`GroupID`),
  CONSTRAINT `tbl_RequestMaster_ibfk_3` FOREIGN KEY (`FK_StatusId`) REFERENCES `tbl_StatusMaster` (`StatusId`),
  CONSTRAINT `tbl_requestmaster_RequestMode_RequestModeId` FOREIGN KEY (`RequestModeId`) REFERENCES `RequestMode` (`RequestModeId`)
) ENGINE=InnoDB AUTO_INCREMENT=1702 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 16:00:32
