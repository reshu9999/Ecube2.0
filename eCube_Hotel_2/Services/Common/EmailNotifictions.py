import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Common.config_coordinator import config_fetcher

services_config = config_fetcher.get_services_config

class Uploaded:
    def uploadedValues(self,fileName, EmailID, flag):
        fromAddress = 'ecube2_techteam@eclerx.com;'
        toAddress = 'ecube2_techteam@eclerx.com;'

        msg = MIMEMultipart()
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg['Subject'] = "File Uploaded Successfully"
        filelenght=len(fileName)
        outputfilePath=str(fileName[8:filelenght])

        if flag == 1:
            FinalfileName = '<a href= http://' + services_config['SERVICES_IP'] + '/' + outputfilePath + '>' + ' Click Here ' + '</a>'
            body = """\
         <html>
          <head></head>
          <body>
            <p>Dear User,
               <br>
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Image Matching has been completed successfully.""" + str(FinalfileName) + """to download the output file.
                 <br />
                 <br />
                 <br />
                 <br />


               
              
              For any queries, please contact eCube2_TechTeam@eclerx.com
              
              <br/>
              <br/>
              Regards,
              <br/>
              eCube Admin Team
            </p>
          </body>
         </html>
         """
        else:
            FinalfileName = '<a href= http://' + services_config['SERVICES_IP'] + '/' + outputfilePath + '>' + ' Click Here ' + '</a>'
            body = """\
                     <html>
                      <head></head>
                      <body>
                        <p>Dear User,
                           <br>
                                     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ML Matching has been completed successfully.""" + str(FinalfileName) + """to download the output file.
                            <br />
                            <br />
                            <br />
                            <br />
                 


                           For any queries, please contact eCube2_TechTeam@eclerx.com
                           
                            <br/>
                             <br/>
                            Regards,
                            <br/>
                            eCube Admin Team
                            </p>
                        </p>
                      </body>
                     </html>
                     """




        # print(fileName)
        # print(body)ML Match File
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp1.eclerx.com',25)
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        #server.starttls()
        #server.login(fromAddress, "YOUR PASSWORD")
        text = msg.as_string()
        server.sendmail(fromAddress, toAddress, text)
        server.quit()

    def ErrorMail(self, fileName, EmailID):
        fromAddress = EmailID
        toAddress = EmailID
        msg = MIMEMultipart()
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg['Subject'] = "File Uploaded Successfully"
        # fileName = "sidd.csv"
        # body = "Dear Admin, This is to inform you that the file"+ fileName +" has been generated at mentioned path"
        body = """
                Dear Admin, 
                The Upload File for file name:""" + str(fileName) + """has some issues uploading. 

                Please visit Retail Monitor (https://lazada-contentretailmonitor.eclerx.com/) for further details.

                Regards,
                Admin, 
                Retail Monitor @ eClerx 
                """
        # print(fileName)
        # print(body)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp1.eclerx.com', 25)
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(fromAddress, "YOUR PASSWORD")
        text = msg.as_string()
        server.sendmail(fromAddress, toAddress, text)
        server.quit()

# email_body ="""
# Dear Admin,
#
# The Upload File for file name: + +has been completed successfully.
#
# Please visit Retail Monitor (https://lazada-contentretailmonitor.eclerx.com/) for further details.
#
# Regards,
# Admin,
# Retail Monitor @ eClerx
# """
# email_content = """
# <head>
#   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
#   <title>html title</title>
#   <style type="text/css" media="screen">
#     table{
#         background-color: #AAD373;
#         empty-cells:hide;
#     }
#     td.cell{
#         background-color: white;
#     }
#   </style>
# </head>
# <body>
#   <table style="border: blue 1px solid;">
#     <tr><td class="cell">Cell 1.1</td><td class="cell">Cell 1.2</td></tr>
#     <tr><td class="cell">Cell 2.1</td><td class="cell"></td></tr>
#   </table>
# </body>
# """
#
# print(email_body)
