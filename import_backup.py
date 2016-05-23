import csv
import json
import pymongo
from pymongo import MongoClient
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
print(dbclient)
db=dbclient.artists
data=db.painting_orig
columns = ["TITLE_OF_PAINTING","LOT#","ARTIST","AUCTION_NAME","BP?","PROVENANCE_TEXT","EXHIBITED","DIMENTIONS_TEXT","MATERIAL_TEXT","SIGNED_TEXT","PAINTED_YEAR","IMAGE","URL","AUCTION_HOUSE","SALE_DATE","YOD","AUCTION_LOCATION","ORIENTATION","DATED?","UNIT_OF_MEASURE","SALE#","SIZE-H","SIZE-W","IMAGE_ID","SIGNED?","TYPE","MEDIUM","CURR_OF_SALE","MARKINGS_TEXT","EST_CURR","YOB","MATERIAL","NATIONALITY" ]
try:
	# with open('safronscrape.csv') as csvfile:
		csvfile = open('safronscrape.csv', 'r')
		reader=csv.DictReader(csvfile, delimiter="^")
		i=0;
		for row in reader:
			row2={}
			row2['ID']=int(row['ID'].strip())
			estimate_min=list()
			estimate_max=list()
			if(row['ESTIMATE_MIN']):
				estimate_min.append(row['ESTIMATE_MIN'])
			if(row['ESTIMATE_MIN_INR']):
				estimate_min.append(row['ESTIMATE_MIN_INR'])
			if(row['ESTIMATE_MIN_USD']):
				estimate_min.append(row['ESTIMATE_MIN_USD'])
			if(row['ESTIMATE_MAX']):
				estimate_max.append(row['ESTIMATE_MAX'])
			if(row['ESTIMATE_MAX_INR']):
				estimate_max.append(row['ESTIMATE_MAX_INR'])
			if(row['ESTIMATE_MAX_USD']):
				estimate_max.append(row['ESTIMATE_MAX_USD'])
			row2['ESTIMATE_MIN']=estimate_min
			row2['ESTIMATE_MAX']=estimate_max
			price_sold=list()
			if(not(row['WINNING_BID_INR']) and not(row['WINNING_BID_USD'])):
				price_sold="N/A"
			else:
				price_sold.append(row['WINNING_BID_INR'])
				price_sold.append(row['WINNING_BID_USD'])
			row2['PRICE_SOLD']=price_sold
			row2['IMAGE_LINK']=""
			for head in columns:
				
				row2[head]=row[head]
			print(row2)
			data.insert(row2)	
			# row=json.dumps(row)
			# row=json.load(row)
			# print(row)
			# row['IMAGE_LINK']="http://jlabs.co/artists/images/noimage.jpg"
			# print(data.insert(row.copy)	)
except Exception as e:
	print(str(e))