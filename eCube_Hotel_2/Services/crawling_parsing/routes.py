from core import ServiceLogger
from connectors import MySQL

from Resources.responses import AetosBaseResponse

from flask import Flask, request, Response, json, make_response, request, current_app, send_from_directory


class AetosResponse(AetosBaseResponse):
    RESPONSE = Response


app = Flask(__name__)


@app.route('/api/v2/sub-request/input/<sub_request_id>', methods=['GET'])
def get_sub_request_input(sub_request_id):
    ServiceLogger.info_log('Sub Request Received', sub_request_id)
    input_data = MySQL().get_sub_request_input(sub_request_id)
    ServiceLogger.info_log('Input Data Returned', sub_request_id)
    input_data = json.dumps(input_data)
    return AetosResponse.success_api_response(input_data, 'Input Data for %s' % sub_request_id)
