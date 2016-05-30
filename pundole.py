import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

data=requests.get('http://pundoles.com/').content
soup=BeautifulSoup(data,"html.parser")
maindiv=soup.find('div',attrs={'class':'preimgmain'})
auctions=maindiv.findAll('div',attrs={'class':'preauctionimg-01box'})

for auction in auctions:
	details=auction.find('div', attrs={'class':'preauctionimgnew-text'})
	if(not details):
		details=auction.find('div', attrs={'class':'preauctionimg-text'})
	
	auction_date=details.findAll('span')[1].text.strip()
	[s.extract() for s in details('span')]
	[s.extract() for s in details('br')]
	auction_name=details.text.strip()
	print(auction_name)
	print(auction_date)
	url=auction.find('div',attrs={'class':'preauctionimg-thumb'}).findAll('a')[0]['href']
	print(url)
