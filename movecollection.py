import csv
import json
import pymongo
from pymongo import MongoClient
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
print(dbclient)
db=dbclient.artists


cursor1=db.christie.find({"ARTIST":"Jamini Roy"})
for doc in cursor1:
    try:
        print("inserting")
        db.test.insert(doc)
    except Exception as e:
        print(str(e))
        pass
