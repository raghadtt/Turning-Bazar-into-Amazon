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
count = 0
arr = [None] * 50
i=0
count2=0
countcatalog = 1
countorder = 1

class Search(Resource):

    @cache.memoize(50)
    def get(self, name):

        global count
        global arr
        global i
        global countcatalog

        data = cache.get(name)
        if data:
            return {'items from cache': data},200
        else:
            if(countcatalog):
                #catalog server A
                countcatalog = 0
                resp =requests.get('http://192.168.1.110:5000/search/'+str(name)).json() #Catalog serverA IP
                cache.set(name, resp)
            else:
                #catalog server B
                countcatalog = 1
                resp =requests.get('http://192.168.1.109:5000/search/'+str(name)).json() #Catalog serverB IP
                cache.set(name, resp)
        arr[count] = name
        count = count + 1

        if count > 6:
            cache.delete(arr[i])
            i= i+1

        if(countcatalog):
           return {'items from B': resp}
        else:  
           return {'items from A': resp}


class Info(Resource):

    @cache.memoize(50)
    def get(self, num):
        global count
        global arr
        global i
        global countcatalog

        data = cache.get(str(num))
        if data:
            return {'items from cache': data},200
        else:
            if(countcatalog):
                #catalog server A
                countcatalog = 0
                resp =requests.get('http://192.168.1.110:5000/info/'+str(num)).json() #Catalog server1 IP
                cache.set(str(num), resp)
            else:
                #catalog server B
                countcatalog = 1
                resp =requests.get('http://192.168.1.109:5000/info/'+str(num)).json() #Catalog server0 IP
                cache.set(str(num), resp)

        arr[count] = str(num)
        count = count + 1

        if count > 6:
            cache.delete(arr[i])
            i= i+1
        if(countcatalog):
           return {'items from B': resp}
        else:  
           return {'items from A': resp}

class Purchase(Resource):

    def put(self, num):
        #from order server
        
        global countorder
        
        if(countorder):
            #catalog server A
            countorder = 0
            return requests.put('http://192.168.1.110:5001/purchase/'+str(num)).json() #Order server0 IP
        else:
            #catalog server B
            countorder = 1
            return requests.put('http://192.168.1.109:5001/purchase/'+str(num)).json() #Order server1 IP


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
