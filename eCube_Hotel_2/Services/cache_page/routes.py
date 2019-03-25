from flask import Flask, json, request
from ops import SaveCachePage

app = Flask(__name__)


@app.route('/api/save_cache_page', methods=['POST', 'GET'])
def save_cache_page():
    request_body = json.loads(request.data)
    # request_body = request.get_json()
    filename = request_body['filename'] + ".html"
    filecontent = request_body['filecontent']
    try:
        if filecontent is not None:
            handler = SaveCachePage(filename, filecontent)
            handler.save_file()
            return handler.file_web_path
        return ""
    except Exception as ex:
        print(ex)
        return "error"


if __name__ == '__main__':
    app.run(debug=True)
