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
-- Table structure for table `Temp_ProbableMatch`
--

DROP TABLE IF EXISTS `Temp_ProbableMatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Temp_ProbableMatch` (
  `intProbableMatchedHotelId` int(11) NOT NULL,
  `Secondary Supplier Company` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Secondary Supplier Hotel ID` int(11) NOT NULL,
  `Secondary Website Hotel ID` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Secondary Supplier Hotel Name` varchar(512) CHARACTER SET utf8 NOT NULL,
  `Secondary Supplier Hotel Address` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Longitude` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Latitude` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Primary Supplier Hotel ID` int(11) NOT NULL,
  `Primary Supplier Hotel Code` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Primary Supplier Hotel Name` varchar(512) CHARACTER SET utf8 NOT NULL,
  `Primary Supplier Hotel Address` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Primary Supplier Longitude` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Primary Supplier Latitude` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Hotel Status` varchar(200) NOT NULL,
  `City` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Destination Code` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Country` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Matching Type` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Added on` char(10) NOT NULL,
  `Matched on` char(10) NOT NULL,
  `Last Appearance` char(10) NOT NULL,
  `Matching Score (%)` double DEFAULT NULL,
  `Primary Matched Exist` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Secondary Match Exist` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Secondary supplier Hotel Star` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  `Primary supplier Hotel Star` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  `Primary Hotel Last Appearance` char(10) DEFAULT NULL,
  `nvcrZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL
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

-- Dump completed on 2018-06-29 16:00:33
