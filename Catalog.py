from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import requests
app = Flask(__name__)
api = Api(app)

class Search(Resource):
    #search using get method
    def get(self,name):
        #read data file
        self.data = pd.read_csv('catalog.csv')
        #compare with the specified topic and store all the related entities in data_fount
        data_fount=self.data.loc[self.data['topic'] == name]
        #convert it to data frame and choose id and title columns
        dataFrame = pd.DataFrame(data_fount, columns = ['id','title'])
        json = dataFrame.to_json(orient="records")
        
        # return data
        return {'items': json},200 
           
class Info(Resource):

    def get(self,num):
        self.data = pd.read_csv('catalog.csv')
        data_fount=self.data.loc[self.data['id'] == num]
        
        dataFrame = pd.DataFrame(data_fount, columns = ['title','quantity', 'price'])
        json = dataFrame.to_json(orient="records")
    
        # return data found in csv
        return {'items': json},200 
  

class Update(Resource):

    def put(self,num):
        self.data = pd.read_csv('catalog.csv')
        #compare the entities with the specified id and decrement their quantity by one after purchasing successfully
        self.data.loc[ self.data["quantity"].loc[self.data["id"] == num].index , "quantity"] = self.data["quantity"] - 1
        self.data.to_csv("catalog.csv", index=False)
        #to invalidate cache consistency from server to frontend server that contains cache
        requests.get('http://192.168.1.105:5000/invalidate/'+str(num))
        return {'message':'You bought this book sucessfully '},200
      
    
# Add URL endpoints
api.add_resource(Search, '/search/<string:name>')
api.add_resource(Info, '/info/<int:num>')
api.add_resource(Update, '/update/item_num/<int:num>')


if __name__ == '__main__':
    app.run()
