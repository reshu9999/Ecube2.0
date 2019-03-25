
import sys
# sys.path.append('/')
import config

from flask import Flask, request, Response, json, make_response, request, current_app,send_from_directory, jsonify

app = Flask(__name__)

@app.route('/api/save_cache_page', methods=['POST','GET'])
def save_cache_page():
    request_body = json.loads(request.data) # request.get_json()
    filename = request_body['filename']+ ".html"
    filecontent = request_body['filecontent']
    #filename = "abcd2" + ".html"
    #filecontent = "<html><body>Hi Linux</body></html>"
    try:
        # client = MongoClient('mongodb://localhost:27017/')
        # mongodb = client.HTMLDumps
        # objData = mongodb.HTMLRepository.find({'requestId': {'$in': [2]}})
        # count = 0
        # for data in objData:
        #     data = {'_id':data['_id'],'requestId': data['requestId'], 'html': data['html']}
            # if count == 0:
            #     header = data.keys()
            #     print(data.keys())
            #     #csvwriter.writerow(header)
            #     count += 1

            # csvwriter.writerow(data.values())
            # print (data['html'])
            # if(len(data['html']) > 10):
        if filecontent is not None:
            #print (filecontent)
            #     print(data['html'])
            #     filename = str(data['_id'])+ 'file.html'
            #     print(filename)
            #file = open("/var/www/html/savepage/" + filename,"w")
            file = open(config.BASIC_CONFIG['MEDIA_FILE_PATH'] + filename, "w")
            file.write(filecontent)
            file.close()
            # return "http://192.168.8.53/savepage/" + filename
            #return "http://38.76.27.250/savepage/" + filename
            return config.BASIC_CONFIG['SAVE_PAGE_SERVER_WEBSITE'] + filename
            # else:
            #     return "record not found"
        # report_data.close()
        return ""
    except  Exception as ex:
        print(ex)
        return "error"
    finally:
        if file:
            file.close()
        # if objData:
        #     objData.close()


if(__name__ == '__main__'):
    #app.run(debug=True, host='0.0.0.0',port=5002)
    app.run(debug=True)
# save_cache_page()
