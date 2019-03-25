from core import ServiceLogger
from connectors import ProxyMySQL

from Resources.responses import AetosBaseResponse

from flask import Flask, request, Response, json, make_response, request, current_app, send_from_directory


class AetosResponse(AetosBaseResponse):
    RESPONSE = Response


app = Flask(__name__)


@app.route('/api/v2/proxy/fetch', methods=['GET'])
def get_proxy():
    # request_body = request.args.get()

    domain = request.args.get('domain')
    country = request.args.get('country') or None
    pos = request.args.get('pos') or None
    tag = request.args.get('page_type') or None

    ServiceLogger.info_log('Request Received', domain, country, pos, tag)
    proxy_data = ProxyMySQL.get_proxy_details(domain, country, pos, tag)
    ServiceLogger.info_log('Proxy Returned', domain, country, pos, tag)
    response = {
        'UserName': proxy_data['username'],
        'Password': proxy_data['password'],
        'IP': proxy_data['ip'],
        'port': proxy_data['port'],
    }

    return AetosResponse.success_api_response(
        response,
        'Proxy for %s' % ServiceLogger.prop_string(domain, country, pos, tag)
    )


@app.route('/api/v2/proxy/fetch/list', methods=['GET'])
def get_proxy_list():
    # request_body = request.args.get()

    domain = request.args.get('domain')
    country = request.args.get('country') or None
    pos = request.args.get('pos') or None
    tag = request.args.get('page_type') or None

    ServiceLogger.info_log('Request Received', domain, country, pos, tag)
    proxy_data = ProxyMySQL.get_proxy_details(domain, country, pos, tag, all_proxies=True)
    ServiceLogger.info_log('Proxy Returned', domain, country, pos, tag)
    response = [{
        'UserName': pd['username'],
        'Password': pd['password'],
        'IP': pd['ip'],
        'port': pd['port'],
    } for pd in proxy_data]

    return AetosResponse.success_api_response(
        response,
        'All Proxies for %s' % ServiceLogger.prop_string(domain, country, pos, tag)
    )

# @app.route('/media/<filename>')
# def downloadTestFile(filename):
#     return send_from_directory('/var/www/eCube_Hotel_2/Services/media/Download_excel/', filename)


if(__name__ == '__main__'):
    app.run(debug=True, port=5002)
