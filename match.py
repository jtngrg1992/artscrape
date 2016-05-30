import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
db=dbclient.artists
source=db.christie4.find({},{"_id":False}).sort([('ID',1)])
exclude=['&',',',';','+','/','-',"(",")","."]
try:
	for s in source:
		print("Matchin " + str(s['ID']) + " form source")
		#converting date
		flag="false"
		sdate=s['SALE_DATE'].split(" ")
		newdate=sdate[1] + " " + sdate[0] + " " + sdate[2]
		auction=s['AUCTION_NAME']
		
		#modifying auction name
		for char in exclude:
			auction=auction.replace(char,"")
		
		print("Matching for Auction: " + auction + "\n")
		
		target=db.paintings_final.find({"AUCTION_HOUSE":"Christie's","AUCTION_NAME" : re.compile(auction, re.IGNORECASE)},{"_id":False})


		#iterating over target collection
		for t in target:
			print("ID " + str(t['ID']))
			tdate=t['SALE_DATE'].replace(",","")
			
			print("Matching" + newdate + " and  " + tdate)

			if(tdate==newdate):
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
					db.christieHits.insert(var)
					flag="true"
					break
					
			
		if(flag=="false"):
				db.christieMiss.insert(s)
except:
	pass

