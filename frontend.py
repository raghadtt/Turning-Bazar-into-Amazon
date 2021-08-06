from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import requests

app = Flask(__name__)
api = Api(app)

class Search(Resource):

    def get(self,name):
        #to catalog server
        #search by topic
        return requests.get('http://192.168.1.108:5000/search/'+str(name)).json() 
           
class Info(Resource):

    def get(self,num):
        #to catalog server
        #search by id
        return requests.get('http://192.168.1.108:5000/info/'+str(num)).json()
  
class Purchase(Resource):
    def put(self,num):
        #to order server
        #purchase by id
        return requests.put('http://192.168.1.109:5000/purchase/'+str(num)).json() 
       
api.add_resource(Search, '/search/<string:name>')
api.add_resource(Info, '/info/<int:num>')
api.add_resource(Purchase, '/purchase/<int:num>')

if __name__ == '__main__':
    app.run()
