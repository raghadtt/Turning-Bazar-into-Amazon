from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import json
import requests

app = Flask(__name__)
api = Api(app)

class Purchase(Resource):
    def put(self,num):
    
        info = requests.get('http://192.168.1.105:5000/info/'+str(num)).json()
        df = pd.DataFrame(info, columns = ['quantity','title','price'])
        result = df.iloc[0]['quantity']
        title = df.iloc[0]['title']
        price = df.iloc[0]['price']
        if (result != 0):
           data = pd.read_csv('orders.csv')
           new_data = pd.DataFrame({
           'id'      : [num],
           'title'   : [title],
           'price'   : [price]
           })
           data = data.append(new_data, ignore_index = True)
           data.to_csv('orders.csv', index=False)
           return requests.put('http://192.168.1.100:5000/update/item_num/'+str(num)).json()
        else:
          return {'message':'The operation is failed, this book is over'},200
          
         
    
# Add URL endpoints
api.add_resource(Purchase, '/purchase/<int:num>')

if __name__ == '__main__':
    app.run()
    
