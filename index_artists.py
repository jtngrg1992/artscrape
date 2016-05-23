import json
import pymongo
from pymongo import MongoClient
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
print(dbclient)
db=dbclient.artists


try:
    coll=db.allartists.find({})
    counter=1
    for doc in coll:
        var={}
        var['id']=counter
        var['artist']=doc['artist']
        db.artist_list.insert(var)
        counter+=1
        print(var)

except Exception as e:
	print(str(e))
