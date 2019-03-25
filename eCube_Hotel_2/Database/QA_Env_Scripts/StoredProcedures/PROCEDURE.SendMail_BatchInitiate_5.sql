DELIMITER ;;

CREATE PROCEDURE `SendMail_BatchInitiate_5`(
p_intMDM_BatchesId  int,
	p_vcrStatus varchar(20))
BEGIN

 



/*





CREATE  Procedure SendMail_BatchInitiate_5  
(
	
)
BEGIN 
	BEGIN TRY
		
	 
     
	
	
	DECLARE v_Start VARCHAR (50) DEFAULT 'Start';
	DECLARE v_success VARCHAR (50) DEFAULT 'Success';
	DECLARE v_Fail VARCHAR (50) DEFAULT 'Fail';
	DECLARE v_NoData VARCHAR(50) DEFAULT 'NoData';
	DECLARE v_Error LONGTEXT DEFAULT 'ERROR';
	DECLARE v_ManualUpload varchar(50) DEFAULT 'ManualUpload';
	DECLARE v_FileName Varchar (50);
	DECLARE v_BatchName VARCHAR (50); 
	DECLARE v_intBatchId  int; 
	DECLARE v_leadtime  VARCHAR (50) DEFAULT 'leadtime'; -- --Added on 22-03-2016 for blank column check and send alert 


	SELECT    vcrBatchName ,  vcrFileName ,  intBatchId INTO v_BatchName, v_FileName, v_intBatchId from MDM_Batches WHERE intMDM_BatchesId = p_intMDM_BatchesId;-- @intMDM_BatchesId
	
	-- Declare And Set Subject
	DECLARE v_subject longtext  DEFAULT 
									(Select CASE WHEN p_vcrStatus =v_Start   THEN   CONCAT('Hotelbeds MDM_5  Report generation for batch ' , v_BatchName ,  '  "INITIATED"')
												 WHEN p_vcrStatus =v_Fail    THEN   CONCAT('Hotelbeds MDM_5  Report generation for batch ' , v_BatchName ,  ' "FAILED"')
												 WHEN p_vcrStatus =v_success THEN   CONCAT('Hotelbeds MDM_5  Report generation for batch ' , v_BatchName ,  ' "COMPLETED"') 
												 WHEN p_vcrStatus =v_NoData  THEN	  CONCAT('Hotelbeds MDM_5  Report generation for batch ', v_BatchName  ,' "FAILED"')
												 WHEN p_vcrStatus =v_Error   THEN	  CONCAT('Hotelbeds MDM_5  Report generation for batch', v_BatchName  ,' "FAILED"')	
												 WHEN p_vcrStatus =v_ManualUpload THEN 'Hotelbeds MDM_5  Report uploaded in MDM Database'
												 WHEN p_vcrStatus = v_leadtime THEN CONCAT('Hotelbeds MDM_5  Alert balnk values for LeadTime column  ', v_BatchName  ,' Batch')	-- -added on 22-03-2016 for balnk columns
												 END );							
	DECLARE v_htmlBody  longtext  DEFAULT 
	CONCAT('<style type="text/css">
      p.MsoNormal, li.MsoNormal, div.MsoNormal
      {margin:0in;
      margin-bottom:.0001pt;
      font-size:11.0pt;
      font-family:"Verdana","sans-serif";}
      a:link, span.MsoHyperlink
      {mso-style-priority:99;
      color:blue;
      text-decoration:underline;}
      a:visited, span.MsoHyperlinkFollowed
      {mso-style-priority:99;
      color:purple;
      text-decoration:underline;}
      span.EmailStyle17
      {mso-style-type:personal;
      font-family:"Verdana","sans-serif";
      color:windowtext;}
      span.EmailStyle18
      {mso-style-type:personal-reply;
      font-family:"Verdana","sans-serif";
      color:#1F497D;}
      .MsoChpDefault
      {mso-style-type:export-only;
      font-size:10.0pt;}
      @page Section1
      {size:8.5in 11.0in;
      margin:1.0in 1.0in 1.0in 1.0in;}
      div.Section1
      {page:Section1;}

      table
      {
      border-collapse:collapse;
      width : 800px;
      }
      table, td, th
      {
      border:1px solid black;
      }

    </style>
<div style="font-family: Calibri;font-size: 12pt;">
  <p>
        Dear User,

      </p><p>'  , 
        (Select Case WHEN p_vcrStatus = v_Start THEN 'Report generation for the following batch has been initiated in MDM -'
                     WHEN p_vcrStatus = v_Fail  THEN 'Report generation for the following batch in MDM could not be completed. Please contact MDM admin team for further details.'
                     WHEN p_vcrStatus = v_success THEN 'Report has been generated successfully for the following batch -'
                     WHEN p_vcrStatus = v_NoData THEN 'Report could not be generated for the following batch as batch didnt have any harvested data -'
                     WHEN p_vcrStatus = v_Error THEN 'Report could not be generated for the following batch as batch has below mentioned erroneous data -' 
                     WHEN p_vcrStatus = v_ManualUpload THEN 'Report for following batch, which was generated using old manual process (as MDM was not operational), has been uploaded in MDM target database successfully.'
                     WHEN p_vcrStatus = v_leadtime THEN 'Report Generation stopped due to balnk values for LeadTime column'  -- -added on 22-03-2016 for balnk columns
                  END)
         , 
        
        
        
        
      '</p><table>
    <tr style="border: solid black 1.0pt; background: #365F91;color:white">
      <td>Batch Name</td>
      <td>Batch Id</td> ' , 
      (Select IFNULL( Case WHEN p_vcrStatus = v_success THEN  '<td>Report Name</td>' END,'')  ) +
       (Select IFNULL( Case WHEN p_vcrStatus = v_Error THEN  '<td>Error</td>' END,'')  )
         , '
    </tr>
    <tr>
      <td>', v_BatchName  ,'</td>
      <td>', CONVERT( VARCHAR , v_intBatchId ),'</td>',
      (Select IFNULL(Case WHEN p_vcrStatus = v_success THEN  Concat('<td>',v_FileName,'</td>') END ,'') ) + 
      (Select IFNULL(Case WHEN p_vcrStatus = v_Error THEN  Concat('<td>',v_FileName,'</td>') END ,'') )
         , '
    </tr>
  </table><br><br>
  ',
  -- -(Select ISNULL( Case WHEN @vcrStatus = @success THEN  'Please visit following link to access the Report  <br/>
      -- -  ftp://192.168.7.62/TESTMDMReports/' END ,'') )
        -- InformaticaDataUpload/
        
    '
  
  <br><br><br><br>
      
        Regards,<br>
        Admin,<br>
        Hotelbeds MDM @eClerx
      <p>
        This message including attachment(s) is intended only for the personal and confidential use of the recipient(s) named above.This communication is for 
        informational purposes only.Email transmission cannot be guaranteed to be secure or error-free. All information is subject to change without notice. 
        If you are not the intended recipient of this message you are hereby notified that any review, dissemination, distribution or copying of this message 
        is strictly prohibited. If you are not the intended recipient, 
        please contact:<A href="mailto:helpdesk@eclerx.com">helpdesk@eclerx.com</A></p>
  <p>
    <font size="3pt" color="black" family="Tahoma"><STRONG> eClerx -An ISO/IEC 27001:2005 Certified Organization</STRONG></font>
  </p>
</div>');
	
	  CALL msdb.dbo
      v_profile_name; = 'Test',
      -- @recipients = 'Mayakannan.C@eclerx.com;rahul.gupta01@eclerx.com;Rajas.Sant@eclerx.com;Bhavin.Dhimmar@eclerx.com;praneeth.bathini@eclerx.com;Dharti.thakare@eclerx.com;Pallavi.Joshi@eclerx.com;Sachin.Ghule@eclerx.com;Khushboo.Priya@eclerx.com;Aditya.Rajopadhye@eclerx.com',
      -- @recipients = 'rahul.gupta01@eclerx.com',
      @recipients = 'QA_hotelbeds@eclerx.com;HotelMonitor_Ecube@eclerx.com' , -- Prachi.Chorghade@eclerx.com;Prashant.Gawade@eclerx.com
      -- 'rahul.gupta01@eclerx.comQA_hotelbeds@eclerx.com;HotelMonitor_Ecube@eclerx.com',
      v_subject = v_subject,
      @body_format = 'HTML',
      @body = v_htmlBody

     END; TRY 
	BEGIN CATCH
	/*insert into ErrorLog (vcrError ,vcrErrorNo )
	values  (ERROR_MESSAGE() , @intMDM_BatchesId)*/
    
    /*
	END; CATCH
	

-- Select * from StatusMaster		
END;	  







//

*/




END ;;
