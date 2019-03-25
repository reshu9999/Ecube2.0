DELIMITER ;;

CREATE FUNCTION `fn_GetExcatMatchStatus`(p_HotelId INT, p_intSupplierId INT, p_FlgPriSec INT) RETURNS varchar(20) CHARSET latin1
BEGIN
	
	DECLARE v_matchstatus Varchar(20);
	DECLARE v_IntCnt int DEFAULT 0;
	SET v_matchstatus = 'N';
	If (p_FlgPriSec = 1) -- For  Primary
		Then

			Select Count(1) Into v_IntCnt
				From HotelRelation HR Inner Join Hotels MH 
				On  HR.HotelId = MH.HotelId
				 And HR.HotelId = p_HotelId 
				 Inner Join Hotels SMH 
				On  HR.HotelRelationComHotelId = SMH.HotelId				
				Where SMH.CompetitorId = p_intSupplierId;  

			If (v_IntCnt > 0) Then
				SET v_matchstatus = 'Y';
			End if; 

			Return v_matchstatus;
	Elseif (p_FlgPriSec = 2) -- For  Secondary
		Then
			Select Count(1) Into v_IntCnt
				From HotelRelation HR   
				Where HR.HotelRelationComHotelId = p_HotelId; -- And HRbitIsManualUnmatch = 0; 

			If (v_IntCnt > 0) Then
				SET v_matchstatus = 'Y';
			End if; 

			Return v_matchstatus;
	End if;

		



	

	SELECT IFNULL(HotelRelationId,0) INTO v_matchstatus 
	FROM HotelRelation  
	WHERE	HotelRelationComHotelId = p_HotelId;
	 			
	
	If v_matchstatus = 0 Then
		Set v_matchstatus = 0;
	Else
		Set v_matchstatus = 1;
	End if;

	RETURN v_matchstatus;
	
END ;;
