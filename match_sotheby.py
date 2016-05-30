import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
db=dbclient.artists
source=db.sothebey_2.find({},{"_id":False}).sort([('ID',1)])
target=db.paintings_final.find({"AUCTION_HOUSE":"Sotheby's"},{"_id":False})
exclude=['&',',',';','+','/','-',"(",")","."]
try:
	for s in source:

		print("Matchin " + str(s['ID']) + " form source")
		#converting date
		flag="false"
		date=s['SALE_DATE'].split(" " )
		newdate=date[1] + " " + date[0] + " " + date[2]
		#CONVERTING AUCTION
		auction=s['AUCTION_NAME']
		for char in exclude:
			auction=auction.replace(char,"")
		
		print("Matching for Auction: " + auction + "\n")
		target=db.paintings_final.find({"AUCTION_HOUSE" : "Sotheby's","AUCTION_NAME": re.compile(auction, re.IGNORECASE)},{"_id":False})

		#iterating over target collection
		for t in target:
			print("ID " + str(s['ID']))
			t['SALE_DATE']=t['SALE_DATE'].replace(",","")
			date=t['SALE_DATE'].split(" ")
			date[0]=date[0][:3]
			t['SALE_DATE']=date[0] + " " + date[1] + " " + date[2]
			
			print("Matching" + newdate + " and  " + t['SALE_DATE'])

			if(t['SALE_DATE']==newdate):
				#matching lot numbers
				print("Matching lots" + t['LOT#'] + " and " + s['LOT#'])
				if(t['LOT#']==s['LOT#']):
					print("found")
					var={}
					
					var=t
					var['DESCRIPTION']=s['DESCRIPTION']
					var['ESTIMATE_MIN']=s['ESTIMATE_MIN']
					var['ESTIMATE_MAX']=s['ESTIMATE_MAX']
					var['PRICE_SOLD']=s['PRICE_SOLD']
					db.sothebyHits.insert(var)
					flag="true"
					break
					
			
		if(flag=="false"):
				db.sothebyMiss.insert(s)
except Exception as e:
	print(str(e))
	pass

