from flask import Response

class CustomResponse():
    def CustomResponse(data):
        return Response(response =data, status=200, mimetype="application\json", )