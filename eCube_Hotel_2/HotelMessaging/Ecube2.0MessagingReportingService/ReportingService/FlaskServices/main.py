import flask
from flask import send_from_directory
from OpenSSL import SSL

context = SSL.Context(SSL.SSLv23_METHOD)

app=flask.Flask(__name__)


@app.route('/')
def hello():
    return "Test Page is ready..."

@app.route('/fetchreport/<filename>')
def send_file(filename):
    print(filename)
    #return send_from_directory('/home/tech/Ecube2.0MessagingQueueLatest/ReportingService/Reports',filename)
    return send_from_directory('/home/tech/ReportGeneration/', filename)


if __name__=='__main__':
    #app.run(host='0.0.0.0',port=5000,ssl_context = ('/home/tech/key.crt','/home/tech/key.key'))
    #app.run(host='0.0.0.0', ssl_context=('/home/tech/key.crt', '/home/tech/key.key'))
    #app.run(host='0.0.0.0', port=5000)
    app.run()