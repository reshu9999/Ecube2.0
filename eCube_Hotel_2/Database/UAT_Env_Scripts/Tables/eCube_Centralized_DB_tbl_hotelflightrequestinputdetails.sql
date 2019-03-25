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
-- Table structure for table `tbl_hotelflightrequestinputdetails`
--

DROP TABLE IF EXISTS `tbl_hotelflightrequestinputdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_hotelflightrequestinputdetails` (
  `hotelflightrequestinputdetailsId` bigint(20) NOT NULL AUTO_INCREMENT,
  `RequestId` int(11) NOT NULL,
  `RequestURL` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `RequestTypeId` int(11) DEFAULT NULL,
  `CreatedDatetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `UpdatedDatetime` datetime DEFAULT NULL,
  `FromDate` datetime DEFAULT NULL,
  `ToDate` datetime DEFAULT NULL,
  `BookingPeriodId` int(11) NOT NULL,
  `DaysOfWeek` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `PointOfSaleId` int(11) NOT NULL,
  `RentalLength` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `AdvanceDates` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `FromAirportCodeId` int(11) NOT NULL,
  `ToAirportCodeId` int(11) NOT NULL,
  `AdultId` int(11) NOT NULL,
  `ChildID` int(11) NOT NULL,
  `CrawlMode` int(11) DEFAULT NULL,
  `HotelId` bigint(20) DEFAULT NULL,
  `StarRating` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
  `BoardType` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
  `RoomType` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
  `CompetitorIds` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
  `FlightSearchTypeID` int(11) NOT NULL,
  `AdvanceWeeks` varchar(45) DEFAULT NULL,
  `ReportType` varchar(45) DEFAULT NULL,
  `call_func` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`hotelflightrequestinputdetailsId`),
  KEY `RequestId` (`RequestId`),
  KEY `BookingPeriodID` (`BookingPeriodId`),
  KEY `PointOfSaleId` (`PointOfSaleId`),
  KEY `AdultId` (`AdultId`),
  KEY `ChildID` (`ChildID`),
  KEY `FromAirportCodeId` (`FromAirportCodeId`),
  KEY `ToAirportCodeId` (`ToAirportCodeId`),
  KEY `FlightSearchTypeID` (`FlightSearchTypeID`),
  KEY `hotelflight_hotelid_hotels` (`HotelId`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_AirportCodes_FromAirport` FOREIGN KEY (`FromAirportCodeId`) REFERENCES `AirportCodes` (`AirportCodeId`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_AirportCodes_ToAirport` FOREIGN KEY (`ToAirportCodeId`) REFERENCES `AirportCodes` (`AirportCodeId`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_BookingPeriod_BookingPeriodID` FOREIGN KEY (`BookingPeriodId`) REFERENCES `BookingPeriod` (`BookingPeriodID`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_FlightSearchType_FlightSearch` FOREIGN KEY (`FlightSearchTypeID`) REFERENCES `FlightSearchType` (`FlightSearchTypeID`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_PointOfSales_PointOfSaleId` FOREIGN KEY (`PointOfSaleId`) REFERENCES `HotelPOS` (`PointOfSaleId`),
  CONSTRAINT `tbl_hotelflightrequestinputdetails_tbl_RequestMaster_RequestId` FOREIGN KEY (`RequestId`) REFERENCES `tbl_RequestMaster` (`RequestId`)
) ENGINE=InnoDB AUTO_INCREMENT=605 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 16:00:37
