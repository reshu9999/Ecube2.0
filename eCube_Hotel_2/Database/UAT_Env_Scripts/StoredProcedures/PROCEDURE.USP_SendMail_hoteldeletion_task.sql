DELIMITER ;;

CREATE PROCEDURE `USP_SendMail_hoteldeletion_task`()
BEGIN
		Declare v_MailId Nvarchar(100);

		CALL `Delete_Primary_secondary_Hotel_Weekly`() ; 
	
		-- set v_MailId='QA_Hotelbeds@eclerx.com;HotelMonitor_ECube@eclerx.com';
/*
   											 			
	DECLARE v_htmlBody  longtext  DEFAULT 
	 CONCAT('<p>
        Hi Team,
  <br><br>
      </p><p>'  , 
        ' This is to inform you that, Hotel Deletion task is completed.' , 
        '</p>               
        
        ',      
     '
  <br><br>
      
        Regards,<br>
        Admin,<br>
        Retail Monitor Team @eClerx
      <p>
        This message including attachment(s) is intended only for the personal and confidential use of the recipient(s) named above.This communication is for 
        informational purposes only.Email transmission cannot be guaranteed to be secure or error-free. All information is subject to change without notice. 
        If you are not the intended recipient of this message you are hereby notified that any review, dissemination, distribution or copying of this message 
        is strictly prohibited. If you are not the intended recipient, 
        please contact:<A href="mailto:helpdesk@eclerx.com">helpdesk@eclerx.com</A></p>
  <p>
    <font size="3pt" color="black" family="Tahoma"><STRONG> eClerx -An ISO/IEC 27001:2005 Certified Organization</STRONG></font>
  </p>');
 CALL msdb.dbo
      v_profile_name; = 'DBmail_ecxus217',
       @recipients = v_MailId,
	  -- @blind_copy_recipients ='RSComponents_L1@eclerx.com;RetailMonitor_ECube@eclerx.com',
      @subject = 'Hotelbeds-Primary (apart from masterlist) and secondary (4 weeks older) delete - Completed',
      @body_format = 'HTML',
      @body = v_htmlBody
  */
  end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `USP_Update_HotelAddress_task` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
