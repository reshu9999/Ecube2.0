from flask import Flask,request
from pymongo import MongoClient
from pdb import set_trace as st

app=Flask(__name__)

client=MongoClient('192.168.8.69',27017)

@app.route('/')
def hello():
    return ("Hi")

@app.route('/api/v1/service/SaveResponseHotelData',methods=['GET','POST'])
def SaveResponseHotelData():
    data=eval(request.data.decode('utf-8'))
    if len(data)>1:
        db=client.HotelData
        hotelParseData=db.HotelParseData
        rec=hotelParseData.insert(data)
        return ("Success")
    else:
        return ("Failed")


if __name__=='__main__':
    app.run(host='0.0.0.0')
