DELIMITER ;;

CREATE PROCEDURE `sp_GetHotelCount`(
p_RequestId INT,
p_RequestRunId INT)
BEGIN
	
	Declare v_Previous_IntDipBagDynamicId INT Default 0;
    Declare rowsCount int;
	Declare rows_deleted int;
	
	Delete From HotelCount Where IntDipBagDynamicId = p_RequestRunId;	
	
	Insert Into HotelCount (BatchID, intDiPBagDynamicId,  CheckinDate, Nights, Supplier, HotelCount, MatchHotelCount)
	Select RequestId, RequestRunId, Dates, Nights, `name`, COUNT(Distinct Supplier), Sum(HotelId)
	From (
	Select  Distinct B.RequestId, D.RequestRunId, B.RequestName, BCD.Dates, 
	 Nights, MS.`name`, Supplier, Case When HotelId < 0 Then 0 Else 1 End HotelId
	    From RequestRunDetail D  Inner Join tbl_RequestMaster B  
	On D.FK_RequestId = B.RequestId Inner Join LastResultQACheck BCD  
	on D.RequestRunId = BCD.intDiPBagDynamicId And BCD.intDiPBagDynamicId = p_RequestRunId
	Inner Join tbl_Competitor MS On BCD.Company = MS.`name`
	Where BCD.intDiPBagDynamicId = p_RequestRunId
	) A 
	Group By RequestId, RequestRunId, RequestName, Dates, Nights, `name`;	
	
    
   
	Select RequestRunId Into v_Previous_IntDipBagDynamicId From RequestRunDetail   
		Where FK_RequestId = p_RequestId 
	And RequestRunId != p_RequestRunId  Order by RequestRunId desc limit 1;	 

	DELETE Trans from DisplayData_Hotel_Count Trans where intbatchid = p_RequestId;
	
     /*
	set rowsCount = 1;
	while rowsCount > 0 do
		DELETE Trans from dbo.DisplayData_Hotel_Count Trans 
			where intbatchid = p_RequestId and intdipbagdynamicid = p_RequestRunId;	
	set rowsCount = row_count();
	end while;
	*/
    
 
INSERT INTO DisplayData_Hotel_Count (Supplier,Ch_Date,Night,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount
           ,PreviousMatchCount,MatchingPercent ,intbatchid,intdipbagdynamicid,nvcrSupplier)
           
	Select Distinct  C.Supplier, C.CheckinDate, C.Nights,  C.HotelCount, Ifnull(P.HotelCount,0) HotelCount,
	Case When Ifnull(P.HotelCount,0) > 0 Then
		Cast((((Cast(C.HotelCount As Decimal(18,0)) - Cast(P.HotelCount As Decimal(18,0))) / Cast(P.HotelCount As Decimal(18,0))) *100) As decimal(10,2))  
	     Else  0
	     End Percentage 
	, C.MatchHotelCount CurrentMatchCount , Ifnull(P.MatchHotelCount,0) PreviousMatchCount,
	Ifnull(
	Case When Ifnull(P.MatchHotelCount,0) > 0 Then
	Cast((((Cast(C.MatchHotelCount As Decimal(18,0)) - Cast(P.MatchHotelCount As Decimal(18,0))) / Cast(P.MatchHotelCount As Decimal(18,0))) *100) As decimal(10,2))  
	    Else  0
	
	     End,0) MatchingPercentage,p_RequestId,p_RequestRunId,'' 
	From 
	(Select * From HotelCount Where intDiPBagDynamicId = p_RequestRunId) C Left Join 
	(Select * From HotelCount Where intDiPBagDynamicId = v_Previous_IntDipBagDynamicId) P
		On 
		C.BatchID = P.BatchID
		And Timestampdiff(DAY,C.CheckinDate, C.InsertDate) = Timestampdiff(DAY,P.CheckinDate, P.InsertDate) 
		And C.Nights = P.Nights
		And C.Supplier = P.Supplier
		Order by C.Supplier, C.CheckinDate;

	Insert into Hotel_Count_Ecube_MDM_5 (Ch_Date,Night,Supplier,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount,PreviousMatchCount,MatchingPercent)
	Select Distinct   C.CheckinDate, C.Nights, C.Supplier, C.HotelCount, Ifnull(P.HotelCount,0) HotelCount,
	Case When Ifnull(P.HotelCount,0) > 0 Then
		Cast((((Cast(C.HotelCount As Decimal(18,0)) - Cast(P.HotelCount As Decimal(18,0))) / Cast(P.HotelCount As Decimal(18,0))) *100) As decimal(10,2))  
	     Else  0
	     End Percentage 
	, C.MatchHotelCount CurrentMatchCount , Ifnull(P.MatchHotelCount,0) PreviousMatchCount,
	Ifnull(
	Case When Ifnull(P.MatchHotelCount,0) > 0 Then
	Cast((((Cast(C.MatchHotelCount As Decimal(18,0)) - Cast(P.MatchHotelCount As Decimal(18,0))) / Cast(P.MatchHotelCount As Decimal(18,0))) *100) As decimal(10,2))  
	    Else  0
	
	     End,0) MatchingPercentage 
	From 
	(Select * From HotelCount Where intDiPBagDynamicId = p_RequestRunId) C Left Join 
	(Select * From HotelCount Where intDiPBagDynamicId = v_Previous_IntDipBagDynamicId) P
		On 
		C.BatchID = P.BatchID
		And Timestampdiff(DAY,C.CheckinDate, C.InsertDate) = Timestampdiff(DAY,P.CheckinDate, P.InsertDate) 
		And C.Nights = P.Nights
		And C.Supplier = P.Supplier
		Order by C.Supplier, C.CheckinDate;
		
	-- Select * From Hotel_Count_Ecube_MDM_5;
 
	
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetInQueRequest` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
