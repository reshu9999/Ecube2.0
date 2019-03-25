DELIMITER ;;

CREATE PROCEDURE `sp_LastResult_GeneralRules`()
BEGIN          
          
	-- Declare table variable           
	DROP TEMPORARY TABLE IF EXISTS tblTemp;
	CREATE TEMPORARY TABLE tblTemp           
	(          
	nvcrRoomType NVARCHAR(500),          
	nvcrRoomTypeMatch NVARCHAR(500),          
	intPriority INT		 
	);
     
	-- Change History Number #1 //updating all the temp value to default value        
	DROP TEMPORARY TABLE IF EXISTS tblTempExact;
	CREATE TEMPORARY TABLE tblTempExact           
	(          
	nvcrRoomType NVARCHAR(500),          
	nvcrRoomTypeMatch NVARCHAR(500)          
		
	);  


	-- Change History Number #2 //updating all the temp value to default value          
	DROP TEMPORARY TABLE IF EXISTS tblTempPrim;
	CREATE TEMPORARY TABLE tblTempPrim             
	(            
	nvcrRoomType NVARCHAR(500),            
	nvcrRoomTypeMatch NVARCHAR(500)            
		  
	);      
 -- Change History Number #2        
        
         
	UPDATE TEMP_BCD TMP  SET TMP.RoomCode  = 'X09';          
    
	-- --------------------- Start Primary match------------------  

	INSERT INTO tblTempPrim            
	SELECT RoomType as nvcrRoomType, RoomTypeMatch as nvcrRoomTypeMatch FROM vw_HotelStandardization_primarysupplier;
          
 -- updating for Primary exact mapping          
     
	
    /* Drop Temporary table If exists TEXP;
    Create Temporary table TEXP
    As*/ 
    
    
    /*
	UPDATE tblTempPrim TEXP		 
	set TEMP_BCD.RoomCode =TEXP.nvcrRoomTypeMatch    
		where TEMP_BCD.nvcrXmlroomtypecode = LTRIM(RTRIM(TEXP.nvcrRoomType))
		and TEMP_BCD.intSupplierId in (1,6,25,46,37);          
	*/
	
    
	UPDATE TEMP_BCD as t 
    inner join tblTempPrim TEXP on t.nvcrXmlroomtypecode = LTRIM(RTRIM(TEXP.nvcrRoomType))
	set t.RoomCode =TEXP.nvcrRoomTypeMatch    
		where  t.intSupplierId in (1,6,25,46,37);          
		
    
        
	INSERT INTO  tblTempExact           
	SELECT  RoomType as nvcrRoomType,RoomTypeMatch as nvcrRoomTypeMatch FROM vw_HotelStandardization;          
		
 
	UPDATE TEMP_BCD as t 
    inner join tblTempExact TEX on t.RoomType = LTRIM(RTRIM(TEX.nvcrRoomType))  
    set t.RoomCode =TEX.nvcrRoomTypeMatch  
	where t.intSupplierId not in (1,6,25,46,37);   
        
     
                  
	INSERT INTO  tblTemp           
	SELECT RoomType as nvcrRoomType, RoomTypeMatch as nvcrRoomTypeMatch, Priority as intPriority          
	FROM   vw_HotelStandardization_GeneralRules         
	ORDER BY  Priority;           
               
     
	drop temporary table if exists MainRoomType;
	create temporary table MainRoomType (  
		RoomType nvarchar(500),  
		intPriority int ,  
		RoomCode nvarchar(100),
		intSupplierId  int
		);  

	insert into MainRoomType(RoomType,intPriority,intSupplierId)  
	select  distinct TEMP_BCD.RoomType ,min(gr.intPriority) as intPriority, TEMP_BCD.intSupplierId   
	from  tblTemp gr , TEMP_BCD
	where TEMP_BCD.RoomType LIKE CONCAT('%',LTRIM(RTRIM(gr.nvcrRoomType)),'%')   
	group by  TEMP_BCD.RoomType, TEMP_BCD.intSupplierId    ;
 
 
 
	update  HotelStandardization h inner join  MainRoomType m      
    On m.intPriority=h.Priority
    set RoomCode = h.RoomTypeMatch  
    where m.intPriority = h.Priority
	and m.intSupplierId not in   
	(1,6,25,46,37); 
  
	
	update TEMP_BCD t inner join  MainRoomType a
    On t.RoomType = a.RoomType  
	set t.RoomCode = a.RoomCode  
	where t.RoomCode  =  'X09'  
	and t.intSupplierId not in  
	(1,6,25,46,37)
	and a.RoomCode is not null;   
  
           
END ;;
