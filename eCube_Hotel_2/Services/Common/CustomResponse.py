from flask import Response

class CustomResponse():
    def CustomResponse(reponse):
        return Response(response =reponse.response, status=200, mimetype="application\json", )

    def CustomAPIResponse(data):
        return Response(response =data, status=200, mimetype="application\json", )