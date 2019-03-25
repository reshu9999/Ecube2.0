DELIMITER ;;

CREATE PROCEDURE `USP_Update_HotelAddress_task`()
BEGIN
Declare v_MailId Nvarchar(100);

 CALL `update_HotelAddress_weekly`();


-- set v_MailId='QA_Hotelbeds@eclerx.com;HotelMonitor_ECube@eclerx.com';
 
 
 /*
	DECLARE v_htmlBody  longtext  DEFAULT 
	 CONCAT('<p>
        Hi Team,
  <br><br>
      </p><p>'  , 
        'This is to inform you that, secondary Hotel address update task is completed' , 
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
      @subject = 'Hotelbeds-Secondary hotel address update based on newly crawled data - Completed',
      @body_format = 'HTML',
      @body = v_htmlBody
     end;
*/

END ;;
