from flask import Flask
from sourceCode.DataAccessLayer.DataRepository import DataRepository
from sourceCode.Service.CustomResponse import CustomResponse



app = Flask(__name__)

@app.route('/saveData')
def SaveData(sourceHtml, sourceUrl):
    data = DataRepository.SaveData(sourceHtml, sourceUrl)
    result = CustomResponse.CustomResponse(data)
    return result

@app.route('/findById')
def FindById(Id):
    data = DataRepository.FindById(Id)
    result = CustomResponse.CustomResponse(data)
    return data

@app.route("/findAll", methods = ['GET'])
def FindAll():
    data = DataRepository.FindAll("")
    result = CustomResponse.CustomResponse(data)
    return result



if(__name__ == '__main__'):
    app.run(debug=True)

