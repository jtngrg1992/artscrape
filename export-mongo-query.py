import csv
import json
import pymongo
from pymongo import MongoClient
client=MongoClient('jlabs.co',27017)
user="artSales"
password="Jl@B$!@#"
db=client.artists
db.authenticate(user,password,mechanism='SCRAM-SHA-1')

cursor=db.paintings.distinct("AUCTION_NAME",{"AUCTION_HOUSE":"Christie's","SALE":"N/A"})
for doc in cursor:
    print(doc)
