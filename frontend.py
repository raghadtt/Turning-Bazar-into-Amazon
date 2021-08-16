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

countCatalog,countOrder = 0

class Search(Resource):

    @cache.memoize(50)
    def get(self, name, countcatalog = countCatalog):

        global count
        global arr
        global i

        data = cache.get(name)
        if data:
            return {'items from cache': data},200
        else:
            if(countcatalog):
                #catalog server A
                countcatalog = 0
                resp =requests.get('http://192.168.1.101:5000/search/'+str(name)).json() #Catalog server1 IP
                cache.set(name, resp)
            else:
                #catalog server B
                countcatalog = 1
                resp =requests.get('http://192.168.1.101:5000/search/'+str(name)).json() #Catalog server0 IP
                cache.set(name, resp)
        arr[count] = name
        count = count + 1

        if count > 6:
            cache.delete(arr[i])
            i= i+1

        return {'items':resp}


class Info(Resource):

    @cache.memoize(50)
    def get(self, num, countcatalog = countCatalog):
        global count
        global arr
        global i

        data = cache.get(str(num))
        if data:
            return {'items from cache': data},200
        else:
            if(countcatalog):
                #catalog server A
                countcatalog = 0
                resp =requests.get('http://192.168.1.101:5000/info/'+str(num)).json() #Catalog server1 IP
                cache.set(str(num), resp)
            else:
                #catalog server B
                countcatalog = 1
                resp =requests.get('http://192.168.1.101:5000/info/'+str(num)).json() #Catalog server0 IP
                cache.set(str(num), resp)

        arr[count] = str(num)
        count = count + 1

        if count > 6:
            cache.delete(arr[i])
            i= i+1

        return {'items': resp}

class Purchase(Resource):

    def put(self, num, countorder=countOrder):
        #from order server
        if(countorder):
            #catalog server A
            countorder = 0
            return requests.put('http://192.168.1.108:5000/purchase/'+str(num)).json() #Order server0 IP
        else:
            #catalog server B
            countorder = 1
            return requests.put('http://192.168.1.108:5000/purchase/'+str(num)).json() #Order server1 IP


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
