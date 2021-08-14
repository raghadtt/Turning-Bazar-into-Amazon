from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
from flask_caching import Cache
import requests
import json

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)

api = Api(app)


class Search(Resource):

    @cache.memoize(50)
    def get(self,name):
    
        global count
        global arr
        global i
        
        data = cache.get(name)
        if data:
           return {'items from cache': data},200
        else:
           resp =requests.get('http://192.168.1.101:5000/search/'+str(name)).json()          
           cache.set(name, resp)
           
           arr[count] = name
           count = count + 1
           
           if count > 6:
              cache.delete(arr[i])
              i= i+1
                
           return {'items':resp}
           
           
class Info(Resource):

    @cache.memoize(50)
    def get(self,num):
        global count
        global arr
        global i
        
        data = cache.get(str(num))
        if data:
           return {'items from cache': data},200
        else:
           resp=requests.get('http://192.168.1.101:5000/info/'+str(num)).json()
           cache.set(str(num), resp)
           
           arr[count] = str(num)
           count = count + 1
           
           if count > 6:
              cache.delete(arr[i])
              i= i+1
              
           return {'items': resp}
  
class Purchase(Resource):

    def put(self,num):
        #from order server
        return requests.put('http://192.168.1.108:5000/purchase/'+str(num)).json() 
    
#implement cache consistency after any update   
class Invalidate(Resource):
    
    @cache.cached(timeout=50)
    @cache.memoize(50)
    def get(self, item):
        data = cache.get(item)
        if data:
           cache.delete(item)

      
api.add_resource(Search, '/search/<string:name>')
api.add_resource(Info, '/info/<int:num>')
api.add_resource(Purchase, '/purchase/<int:num>')
api.add_resource(Invalidate, '/invalidate/<string:item>')

if __name__ == '__main__':
    app.run()
