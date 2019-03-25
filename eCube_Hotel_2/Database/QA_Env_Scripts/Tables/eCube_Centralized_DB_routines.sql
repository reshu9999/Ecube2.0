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
-- Temporary view structure for view `vw_HotelStandardization`
--

DROP TABLE IF EXISTS `vw_HotelStandardization`;
/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_HotelStandardization` AS SELECT 
 1 AS `RoomType`,
 1 AS `RoomTypeMatch`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_SecondarySupplier_HotelCode`
--

DROP TABLE IF EXISTS `vw_SecondarySupplier_HotelCode`;
/*!50001 DROP VIEW IF EXISTS `vw_SecondarySupplier_HotelCode`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_SecondarySupplier_HotelCode` AS SELECT 
 1 AS `HotelId`,
 1 AS `HotelName`,
 1 AS `HotelAddress1`,
 1 AS `HotelPostCode`,
 1 AS `CityId`,
 1 AS `HotelBrandName`,
 1 AS `CreatedBy`,
 1 AS `isProceesed`,
 1 AS `WebSiteHotelId`,
 1 AS `CompetitorId`,
 1 AS `LastRequestRunId`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_HotelStandardization_primarysupplier`
--

DROP TABLE IF EXISTS `vw_HotelStandardization_primarysupplier`;
/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization_primarysupplier`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_HotelStandardization_primarysupplier` AS SELECT 
 1 AS `RoomType`,
 1 AS `RoomTypeMatch`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `view_RequestManagement`
--

DROP TABLE IF EXISTS `view_RequestManagement`;
/*!50001 DROP VIEW IF EXISTS `view_RequestManagement`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `view_RequestManagement` AS SELECT 
 1 AS `requestrunid`,
 1 AS `RequestId`,
 1 AS `RequestDescription`,
 1 AS `ScheduleType`,
 1 AS `userName`,
 1 AS `CreatedDatetime`,
 1 AS `EndDateTime`,
 1 AS `NextScheduleDateTime`,
 1 AS `StatusTitle`,
 1 AS `ReportDownloadLink`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_PrimarySupplierHotels`
--

DROP TABLE IF EXISTS `vw_PrimarySupplierHotels`;
/*!50001 DROP VIEW IF EXISTS `vw_PrimarySupplierHotels`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_PrimarySupplierHotels` AS SELECT 
 1 AS `HotelId`,
 1 AS `HotelName`,
 1 AS `HotelAddress1`,
 1 AS `HotelAddress2`,
 1 AS `HotelPostCode`,
 1 AS `CityId`,
 1 AS `HotelBrandName`,
 1 AS `CreatedBy`,
 1 AS `isProceesed`,
 1 AS `WebSiteHotelId`,
 1 AS `Latitude`,
 1 AS `Longitude`,
 1 AS `LastRequestRunId`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_competitor`
--

DROP TABLE IF EXISTS `vw_competitor`;
/*!50001 DROP VIEW IF EXISTS `vw_competitor`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_competitor` AS SELECT 
 1 AS `CompetitorId`,
 1 AS `Active`,
 1 AS `CreatedDate`,
 1 AS `ModifiedDate`,
 1 AS `CompetitorName`,
 1 AS `DisplayName`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dipbaghm_getcitycountry`
--

DROP TABLE IF EXISTS `vw_dipbaghm_getcitycountry`;
/*!50001 DROP VIEW IF EXISTS `vw_dipbaghm_getcitycountry`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_dipbaghm_getcitycountry` AS SELECT 
 1 AS `CityId`,
 1 AS `CityName`,
 1 AS `CityCode`,
 1 AS `CityConID`,
 1 AS `CountryId`,
 1 AS `CountryName`,
 1 AS `CountryCode`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_secondarysupplier`
--

DROP TABLE IF EXISTS `vw_secondarysupplier`;
/*!50001 DROP VIEW IF EXISTS `vw_secondarysupplier`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_secondarysupplier` AS SELECT 
 1 AS `HotelId`,
 1 AS `HotelName`,
 1 AS `HotelName_Original`,
 1 AS `HotelAddress1`,
 1 AS `HotelAddress2`,
 1 AS `HotelPostCode`,
 1 AS `CityId`,
 1 AS `HotelBrandName`,
 1 AS `CreatedBy`,
 1 AS `isProceesed`,
 1 AS `WebSiteHotelId`,
 1 AS `CompetitorId`,
 1 AS `Latitude`,
 1 AS `Longitude`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_HotelStandardization_GeneralRules`
--

DROP TABLE IF EXISTS `vw_HotelStandardization_GeneralRules`;
/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization_GeneralRules`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `vw_HotelStandardization_GeneralRules` AS SELECT 
 1 AS `RoomType`,
 1 AS `RoomTypeMatch`,
 1 AS `Priority`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_HotelStandardization`
--

/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_HotelStandardization` AS select `HotelStandardization`.`RoomType` AS `RoomType`,`HotelStandardization`.`RoomTypeMatch` AS `RoomTypeMatch` from `HotelStandardization` where (isnull(`HotelStandardization`.`RuleType`) and (`HotelStandardization`.`Priority` = 0)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_SecondarySupplier_HotelCode`
--

/*!50001 DROP VIEW IF EXISTS `vw_SecondarySupplier_HotelCode`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_SecondarySupplier_HotelCode` AS select `hotel`.`HotelId` AS `HotelId`,`hotel`.`HotelName` AS `HotelName`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelAddress1`)))) = 0) then '0' else ifnull(`hotel`.`HotelAddress1`,'0') end) AS `HotelAddress1`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelPostCode`)))) = 0) then '0' else ifnull(`hotel`.`HotelPostCode`,'0') end) AS `HotelPostCode`,`hotel`.`CityId` AS `CityId`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelBrandName`)))) = 0) then '0' else ifnull(`hotel`.`HotelBrandName`,'0') end) AS `HotelBrandName`,`hotel`.`CreatedBy` AS `CreatedBy`,`hotel`.`isProceesed` AS `isProceesed`,`hotel`.`WebSiteHotelId` AS `WebSiteHotelId`,`hotel`.`CompetitorId` AS `CompetitorId`,`hotel`.`LastRequestRunId` AS `LastRequestRunId` from `Hotels` `hotel` where ((`hotel`.`CompetitorId` <> 1) and (ltrim(rtrim(ifnull(`hotel`.`WebSiteHotelId`,''))) <> '') and (not(`hotel`.`HotelId` in (select `HotelRelation`.`HotelRelationComHotelId` from `HotelRelation`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_HotelStandardization_primarysupplier`
--

/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization_primarysupplier`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_HotelStandardization_primarysupplier` AS select `HotelStandardization`.`RoomType` AS `RoomType`,`HotelStandardization`.`RoomTypeMatch` AS `RoomTypeMatch` from `HotelStandardization` where ((`HotelStandardization`.`RuleType` = 'primary') and (`HotelStandardization`.`Priority` = 0)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `view_RequestManagement`
--

/*!50001 DROP VIEW IF EXISTS `view_RequestManagement`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_RequestManagement` AS select distinct concat('str-',`D`.`RequestRunId`) AS `requestrunid`,`A`.`RequestId` AS `RequestId`,`A`.`RequestDescription` AS `RequestDescription`,`C`.`ScheduleType` AS `ScheduleType`,'tech' AS `userName`,`A`.`CreatedDatetime` AS `CreatedDatetime`,`D`.`EndDateTime` AS `EndDateTime`,`A`.`NextScheduleDateTime` AS `NextScheduleDateTime`,(case when ((`D`.`FK_StatusId` = 1) or (`D`.`FK_StatusId` = 5)) then 'Running' when (`D`.`FK_StatusId` = 2) then 'Completed' when (`D`.`FK_StatusId` = 3) then 'InQue' end) AS `StatusTitle`,`D`.`ReportDownloadLink` AS `ReportDownloadLink` from ((((`tbl_RequestMaster` `A` join `tbl_RequestRunDetail` `D` on((`D`.`FK_RequestId` = `A`.`RequestId`))) left join `tbl_ScheduleMaster` `B` on((`A`.`RequestId` = `B`.`SM_RequestId`))) left join `tbl_ScheduleTypeMaster` `C` on((`C`.`ShedulId` = `B`.`SM_ScheduleTypeId`))) left join `tbl_StatusMaster` `E` on((`E`.`StatusId` = `D`.`FK_StatusId`))) where (`E`.`StatusId` in (1,2,3,5)) order by `A`.`RequestId` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_PrimarySupplierHotels`
--

/*!50001 DROP VIEW IF EXISTS `vw_PrimarySupplierHotels`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_PrimarySupplierHotels` AS select distinct `hotel`.`HotelId` AS `HotelId`,(case when (char_length(rtrim(ltrim(rtrim(ifnull(`hotel`.`matchhotelname`,''))))) > 0) then `hotel`.`matchhotelname` else `hotel`.`HotelName` end) AS `HotelName`,`hotel`.`HotelAddress1` AS `HotelAddress1`,`hotel`.`HotelAddress2` AS `HotelAddress2`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelPostCode`)))) = 0) then '0' else ifnull(`hotel`.`HotelPostCode`,'0') end) AS `HotelPostCode`,`hotel`.`CityId` AS `CityId`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelPostCode`)))) = 0) then '0' else ifnull(`hotel`.`HotelBrandName`,'0') end) AS `HotelBrandName`,`hotel`.`CreatedBy` AS `CreatedBy`,`hotel`.`isProceesed` AS `isProceesed`,`hotel`.`WebSiteHotelId` AS `WebSiteHotelId`,`hotel`.`Latitude` AS `Latitude`,`hotel`.`Longitude` AS `Longitude`,`hotel`.`LastRequestRunId` AS `LastRequestRunId` from `Hotels` `hotel` where (`hotel`.`CompetitorId` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_competitor`
--

/*!50001 DROP VIEW IF EXISTS `vw_competitor`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_competitor` AS select `tbl_Competitor`.`Id` AS `CompetitorId`,`tbl_Competitor`.`active` AS `Active`,`tbl_Competitor`.`createdDate` AS `CreatedDate`,`tbl_Competitor`.`updatedDate` AS `ModifiedDate`,`tbl_Competitor`.`name` AS `CompetitorName`,`tbl_Competitor`.`DisplayName` AS `DisplayName` from `tbl_Competitor` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dipbaghm_getcitycountry`
--

/*!50001 DROP VIEW IF EXISTS `vw_dipbaghm_getcitycountry`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dipbaghm_getcitycountry` AS select `CITY`.`CityId` AS `CityId`,`CITY`.`CityName` AS `CityName`,`CITY`.`CityCode` AS `CityCode`,`CITY`.`CountryId` AS `CityConID`,`COUNTRY`.`CountryID` AS `CountryId`,`COUNTRY`.`CountryName` AS `CountryName`,`COUNTRY`.`CountryCode` AS `CountryCode` from (`Cities` `CITY` join `tbl_CountryMaster` `COUNTRY` on((`CITY`.`CountryId` = `COUNTRY`.`CountryID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_secondarysupplier`
--

/*!50001 DROP VIEW IF EXISTS `vw_secondarysupplier`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_secondarysupplier` AS select `hotel`.`HotelId` AS `HotelId`,`hotel`.`matchhotelname` AS `HotelName`,`hotel`.`HotelName` AS `HotelName_Original`,`hotel`.`HotelAddress1` AS `HotelAddress1`,`hotel`.`HotelAddress2` AS `HotelAddress2`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelPostCode`)))) = 0) then '0' else ifnull(`hotel`.`HotelPostCode`,'0') end) AS `HotelPostCode`,`hotel`.`CityId` AS `CityId`,(case when (char_length(rtrim(ltrim(rtrim(`hotel`.`HotelBrandName`)))) = 0) then '0' else ifnull(`hotel`.`HotelBrandName`,'0') end) AS `HotelBrandName`,`hotel`.`CreatedBy` AS `CreatedBy`,`hotel`.`isProceesed` AS `isProceesed`,`hotel`.`WebSiteHotelId` AS `WebSiteHotelId`,`hotel`.`CompetitorId` AS `CompetitorId`,`hotel`.`Latitude` AS `Latitude`,`hotel`.`Longitude` AS `Longitude` from `Hotels` `hotel` where ((`hotel`.`CompetitorId` <> 1) and (char_length(rtrim(ltrim(rtrim(ifnull(`hotel`.`matchhotelname`,''))))) > 0)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_HotelStandardization_GeneralRules`
--

/*!50001 DROP VIEW IF EXISTS `vw_HotelStandardization_GeneralRules`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_HotelStandardization_GeneralRules` AS select `HotelStandardization`.`RoomType` AS `RoomType`,`HotelStandardization`.`RoomTypeMatch` AS `RoomTypeMatch`,`HotelStandardization`.`Priority` AS `Priority` from `HotelStandardization` where ((`HotelStandardization`.`RuleType` = 'general') and (`HotelStandardization`.`Priority` <> 0)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-29 15:25:05
