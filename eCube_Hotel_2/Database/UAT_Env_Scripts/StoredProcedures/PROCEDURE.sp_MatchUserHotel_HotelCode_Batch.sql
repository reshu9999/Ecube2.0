DELIMITER ;;

CREATE PROCEDURE `sp_MatchUserHotel_HotelCode_Batch`(    
	p_intbatchID int,
	p_intDipBagDynId	int
)
BEGIN  

	declare v_intUserID int; 
	
    set v_intUserID = (select CreatedBy from tbl_RequestMaster 
							where RequestId=(select FK_RequestId 
								from RequestRunDetail 
								where RequestRunId = p_intDipBagDynId
								Limit 1 )
						  Limit 1 );  

		

		DROP TEMPORARY TABLE IF EXISTS HotelWeighted;
		CREATE TEMPORARY TABLE HotelWeighted     
		(     
			intHotelId INT,     
			intHotelWeightedComHotelId INT,    
			bitHotelRelationManualMatch TINYINT,    
			intUsrId INT,    
			intAdminUsrId INT    
		);    
    
   
		INSERT INTO HotelWeighted (intHotelId,intHotelWeightedComHotelId,bitHotelRelationManualMatch,intUsrId,intAdminUsrId)            
			SELECT distinct Ps.HotelId, SS.HotelId, 0, v_intUserID, v_intUserID
			FROM vw_SecondarySupplier_HotelCode AS SS 
			inner join vw_PrimarySupplierHotels as Ps 
			ON Ps.CityId = SS.CityId  and Ps.WebSiteHotelId is not null
			AND SS.WebSiteHotelId = Ps.WebSiteHotelId
			WHERE	Ps.HotelId IS NULL  
					And SS.CompetitorId in (6,25) 
					And (SS.LastRequestRunId = p_intDipBagDynId 
                    Or Ps.LastRequestRunId = p_intDipBagDynId); 
				
			

		  

		INSERT INTO HotelRelation (HotelId, HotelRelationComHotelId, isHotelRelationManualMatch, CreatedBy, AdminUserId)    
		SELECT * FROM HotelWeighted;    
    		     
		UPDATE Hotels H inner join HotelWeighted HW
        On H.HotelId = HW.intHotelWeightedComHotelId
        SET HotelMatchStatus = 1; 
		 
 

END ;;
