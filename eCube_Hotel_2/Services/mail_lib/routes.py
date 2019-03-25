import pandas as pd
import threading
from ops import MailHandler
from resources.responses import AetosBaseResponse
from datetime import datetime
from flask import Flask, request, Response, json, make_response, request, current_app,send_from_directory
class AetosResponse(AetosBaseResponse):
    RESPONSE = Response

app = Flask(__name__)
@app.route('/api/v1/send_email/', methods=['POST'])
def send_email():
    email_status = {
        'message': 'mail sent successfully',
        'status': 'SUCCESS'
    }
    data = request.data.decode('utf-8')
    #fo=open('/home/tech/Punit/abc.txt','w+')
    print(request.data)

    request_body = json.loads(data)    
    thread = threading.Thread(target=MailHandler.mail_to, args=(request_body,))
    thread.daemon = True
    thread.start()
    if email_status['status'] is not 'FAILURE':
        return AetosResponse.success_api_response(data=email_status['message'], message='Success')
    return AetosResponse.failure_api_response(data=email_status['message'], message='Failure')


if(__name__ == '__main__'):
    app.run(debug=True, port=5002)
