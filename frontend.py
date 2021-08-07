from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import requests
import json

app = Flask(__name__)
api = Api(app)


def fetch_file(filename):
        # Let's try to read the file locally first
       
        file_from_cache = fetch_from_cache(filename)

        if file_from_cache:
           print('Fetched successfully from cache.')
           return file_from_cache
           
        else:
           print('Not in cache. Fetching from server.')
           return None
           
           
def fetch_from_cache(filename):
    try:
        # Check if we have this file locally
        fin = open('cache' + filename)
       
        content = fin.read()
        fin.close()
        # If we have it, let's send it
        return content
    except IOError:
        return None
      
      
def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache')
    cached_file = open('cache' + filename, 'w')
    cached_file.write(content)
    cached_file.close()
   
  
class Search(Resource):

    def get(self,name):
        filename='/'+name+'.json'
        data = fetch_file(filename)
        if data:
           return {'items from cache': data},200
        else:
           resp =requests.get('http://192.168.1.109:5000/search/'+str(name)).json()          
           save_in_cache(filename, json.dumps(resp))
           return resp
           
           
class Info(Resource):

    def get(self,num):
        filename='/'+str(num)+'.json'
        data = fetch_file(filename)
        if data:
           return {'items from cache': data},200
        else:
           resp=requests.get('http://192.168.1.109:5000/info/'+str(num)).json()
           save_in_cache(filename, json.dumps(resp))
           return resp
  
class Purchase(Resource):

    def put(self,num):
        #from order server
        return requests.put('http://192.168.1.108:5000/purchase/'+str(num)).json() 
       
api.add_resource(Search, '/search/<string:name>')
api.add_resource(Info, '/info/<int:num>')
api.add_resource(Purchase, '/purchase/<int:num>')

if __name__ == '__main__':
    app.run()
