from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import requests
import json
app = Flask(__name__)
api = Api(app)

class Search(Resource):

    def get(self,name):
        self.data = pd.read_csv('catalog.csv')
        data_fount=self.data.loc[self.data['topic'] == name]
        
        dataFrame = pd.DataFrame(data_fount, columns = ['id', 'title'])
        res = dataFrame.to_json(orient="records")
 
        # return data found in csv
        return json.loads(res),200 
           
class Info(Resource):

    def get(self,num):
        self.data = pd.read_csv('catalog.csv')
        data_fount=self.data.loc[self.data['id'] == num]
        
        dataFrame = pd.DataFrame(data_fount, columns = ['title','quantity', 'price'])
        res = dataFrame.to_json(orient="records")
    
        # return data found in csv
        return json.loads(res),200 
  

class Update(Resource):

    def put(self,num):
        self.data = pd.read_csv('catalog.csv')
        self.data.loc[ self.data["quantity"].loc[self.data["id"] == num].index , "quantity"] = self.data["quantity"] - 1
        self.data.to_csv("catalog.csv", index=False)
        requests.get('http://192.168.1.105:5000/invalidate/'+str(num))
        requests.put('http://192.168.1.109:5000/update/item_num/'+str(num)).json()
        return {'message from A':'You bought this book sucessfully'},200
                
        
# Add URL endpoints
api.add_resource(Search, '/search/<string:name>')
api.add_resource(Info, '/info/<int:num>')
api.add_resource(Update, '/update/item_num/<int:num>')


if __name__ == '__main__':
    app.run()
