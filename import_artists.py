import csv
import json
import pymongo
from pymongo import MongoClient
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
print(dbclient)
db=dbclient.artists
data=db.allartists
columns=["artist"]
try:
# with open('safronscrape.csv') as csvfile:
	csvfile = open('artist_list.csv', 'r')
	reader=csv.DictReader(csvfile, delimiter="^")
	i=0;
	for row in reader:
		print(row)
		data.insert(row)
		# row=json.dumps(row)
		# row=json.load(row)
		# print(row)
		# row['IMAGE_LINK']="http://jlabs.co/artists/images/noimage.jpg"
		# print(data.insert(row.copy)	)
except Exception as e:
	print(str(e))
