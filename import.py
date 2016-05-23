import csv
import json
import pymongo
from pymongo import MongoClient
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
print(dbclient)
db=dbclient.artists
data=db.testupload
columns = ["TITLE_OF_PAINTING","LOT#","ARTIST","AUCTION_NAME","ESTIMATE_MIN_INR","ESTIMATE_MAX_INR","ESTIMATE_MAX_USD","ESTIMATE_MIN_USD","BP?","PROVENANCE_TEXT","EXHIBITED","DIMENTIONS_TEXT","MATERIAL_TEXT","SIGNED_TEXT","PAINTED_YEAR","IMAGE","URL","AUCTION_HOUSE","SALE_DATE","YOD","ESTIMATE_MIN","ESTIMATE_MAX","AUCTION_LOCATION","IMAGE_LINK","ORIENTATION","DATED?","UNIT_OF_MEASURE","SALE#","SIZE-H","SIZE-W","IMAGE_ID","SIGNED?","TYPE","MEDIUM","CURR_OF_SALE","MARKINGS_TEXT","EST_CURR","YOB","MATERIAL","NATIONALITY" ]
try:
	# with open('safronscrape.csv') as csvfile:
		csvfile = open('safronscrape.csv', 'r')
		reader=csv.DictReader(csvfile, delimiter="^")
		i=0;
		for row in reader:
			print(row)
			row2={}
			row2['ID']=int(row['ID'])
			psold={}
			psold={
				"INR":row['WINNING_BID_INR'],
				"USD":row['WINNING_BID_USD']
			}
			row2['PRICE_SOLD']=psold

			for head in columns:
				row2[head]=row[head]
			data.insert(row2)
			# row=json.dumps(row)
			# row=json.load(row)
			# print(row)
			# row['IMAGE_LINK']="http://jlabs.co/artists/images/noimage.jpg"
			# print(data.insert(row.copy)	)
except Exception as e:
	print(str(e))
