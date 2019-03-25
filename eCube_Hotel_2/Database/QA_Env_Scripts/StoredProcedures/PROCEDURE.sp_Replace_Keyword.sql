DELIMITER ;;

CREATE PROCEDURE `sp_Replace_Keyword`(
	IN p_DipBagDynamicId int 
)
BEGIN

	DECLARE v_bitKeywordReplaceActive TINYINT DEFAULT 0;
 
 
	if(p_DipBagDynamicId > 0)
	Then
	/*
		UPDATE (
			Select inthotelid, X.nvcrHotelName   
			from Hotels h with 
			SET nvcrMatchHotelName = HotelMonitor.fn_HotelKeyWordReplace(a.nvcrHotelName,p_DipBagDynamicId)
			inner join 
				(Select distinct intsupplierid, nvcrHotelName 
				from hotelmonitor.batchcrawldata with(nolock)
					where intDipBagDynamicId= p_DipBagDynamicId
				 
					and intSupplierId NOT IN (6,25,46,37,70,71,72,73,74,75,76)-- PMS# 
				 
				)x
				on h.intsupplierid = x.intsupplierid
				And H.nvcrHotelName = X.nvcrHotelName
			)a
		where Hotelmonitor.MstHotel.inthotelid= a.inthotelid
*/
	Set p_DipBagDynamicId = 0;
	Else

		SELECT isKeywordReplaceWeeklyMatching INTO v_bitKeywordReplaceActive FROM ProcessInfo;
			
		IF(v_bitKeywordReplaceActive = 1)
			THEN
				 
				call  sp_ClearDuplicate_Hotel();
/*				  
				UPDATE	Hotels 
					SET matchhotelname = fn_HotelKeyWordReplaceWeeklyMatching(HotelName,0)
 				WHERE CompetitorId NOT IN (6,25,46,37,70,71,72,73,74,75,76); 
 */
			END IF;

 
		
	End if;
 

END ;;
