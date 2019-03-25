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
-- Table structure for table `DisplayData_Hotel_Count`
--

DROP TABLE IF EXISTS `DisplayData_Hotel_Count`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DisplayData_Hotel_Count` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Supplier` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Ch_Date` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Night` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Hotel_Count` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Previous_Crawl_Count` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Previous_Crawl_Diff` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `CurrentMatchCount` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `PreviousMatchCount` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `MatchingPercent` decimal(18,2) DEFAULT NULL,
  `intbatchid` int(11) NOT NULL,
  `intdipbagdynamicid` int(11) NOT NULL,
  `nvcrSupplier` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
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
