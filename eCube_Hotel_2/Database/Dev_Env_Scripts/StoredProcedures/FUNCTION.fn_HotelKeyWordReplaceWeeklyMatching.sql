DELIMITER ;;

CREATE FUNCTION `fn_HotelKeyWordReplaceWeeklyMatching`(
	p_Data VARCHAR(200),
    p_DipBagDynamicId int
) RETURNS varchar(200) CHARSET utf8
BEGIN      
-- -----------------------------------Replacing Provided(from Table) Keywords -----------------------    
  

Declare v_DataValue Varchar(200) Default '';

SELECT  (ROUND (   
		(
			LENGTH(p_Data)
			- LENGTH( REPLACE (p_Data, " ", "") ) 
		) / LENGTH(" ")        
	)  + 1) AS count into @Counter_Max;

	Select 1 into  @Counter;

Create Temporary Table SplitValue (WordValue Varchar(100), ReplaceWordValue Varchar(100));
    
	While(@Counter < @Counter_Max) Do
    
		Set @WordValue = SPLIT_STR(p_Data,' ',@Counter);
        
        Insert into SplitValue (WordValue, ReplaceWordValue)
			Values(@WordValue, '');
            
		Set @Counter = @Counter + 1;
        
	End While;
     

Select v_DataValue + Ltrim(Rtrim (Items))  Into v_DataValue From (
	Select Concat(Items,' ') Items From SplitValue T 
		Where Items Not In (Select Keyword From  BatchKeyword_Rule)
) A;

Set @Data =  Ltrim(Rtrim(v_DataValue));







-- ----Change history number #1 Starts-----    
-- -----------------------------------Replacing Roman Characters with Numbers---------------    
SET @Data=HotelMonitor.ReplaceRomanChars(@Data);     
    
-- -----------------------------------Replacing Acute Accent (Spanish) Characters---------------    
-- Need to do R & D
-- SET v_Data=HotelMonitor.ReplaceSpanishChars(@Data)     
-- -----------------------------------Replacing Special characters-----------------------    
SET @Data=REPLACE(@Data,'´',''); 
SET @Data=REPLACE(@Data,'''','');
SET @Data=REPLACE(@Data,'-',' ');   
SET @Data=REPLACE(@Data,'.',' ');    
SET @Data=REPLACE(@Data,',',' ');    
SET @Data=REPLACE(@Data,':',' ');    
SET @Data=REPLACE(@Data,';',' ');    
SET @Data=REPLACE(@Data,'/',' ');    
SET @Data=REPLACE(@Data,'',' ');    
Set @Data=REPLACE(@Data,'  ',' ');        
-- ----End of change. Change history number #1-----    
    
RETURN @Data;      
    
END ;;
