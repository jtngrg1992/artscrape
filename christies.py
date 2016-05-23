import os
import csv
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import json
import math
import re
import sys

client=MongoClient('jlabs.co',27017)
user="artSales"
password="Jl@B$!@#"
db=client.artists
db.authenticate(user,password,mechanism='SCRAM-SHA-1')

csv_columns = ["Title","Lot","Artist","auction","Sale","Estimated Price Currency","Estimated_Min","Estimated_Max","Estimated_Min_INR","Estimated_Max_INR",
"Estimated_Max_USD","Estimated_Min_USD","Realized_Price_Curr","Price_Realized","Winning_Bid_INR","Winning_Bid_USD","Buyers Prem",
"Provenance","Exhibited_and_Published","Dimensions", "Material","Signed" , "Painted_Year","Image","URL","Auction_House","Auction_Date","Location","ArtID"]
currentPath = os.getcwd()
csv_file = "christie.csv"
j=0
def WriteDictToCSV(dict_data):
	global csv_columns
	global csv_file
	global j
	try:
		with open(csv_file, 'a+') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter='^', lineterminator='\r\n',quotechar = "'", fieldnames=csv_columns)
			if j == 0:
				writer.writeheader()
				j=1

			for data in dict_data:
				writer.writerow(data)

		return 1
	except Exception as e:
		print(str(e))
		return 0
def scurr(n):
	n=n.replace(",","")
	n=re.split(r'(\d+)',n)

	return([n[0],n[1]])

def get_final_scrape(link,artist,title,lot,saleno,ourid):
	print("Final Scrape")
	auction=auction_date=auction_location=image=rprice=eprice_min=eprice_max=""
	no=signed=year=dimension=material=eprice_min_usd=eprice_max_usd=provenance=""
	request=requests.get(link)
	data=request.content
	soup=BeautifulSoup(data,"html.parser")
	div=soup.find('div',attrs={'class':'lot-images-summary'})
	imagdiv=div.find('div',attrs={'class':'lot-image-area'})
	image=imagdiv.find('img',attrs={'id':'main-image'})
	image=image['src']
	div=soup.find('div',attrs={'class':'lot-summary copy'})
	div=div.find('div',attrs={'class':'quick-facts'})
	rlzd=div.find('div',attrs={'id':'price-realized-wrapper'})
	if(rlzd):
		rprice=div.find('ul',attrs={'class':'currency-list'}).findAll('li')[0]
		rprice=rprice.text.strip()
		if("Set" in rprice):
			rprice=rprice[:rprice.index("Set")].strip()
		rprice_curr=scurr(rprice)[0]
		rprice=scurr(rprice)[1]

	estmd=div.find('div',attrs={'class':'wrapper estimate-wrapper'})
	if(estmd):
		estmd=estmd.findAll('ul')[0].findAll('li')[0]
		eprice=estmd.text.strip()
		eprice_min=eprice[:eprice.index('-')].strip()
		eprice_curr=scurr(eprice_min)[0]
		eprice_min=scurr(eprice_min)[1]
		eprice_max=eprice[eprice.index('-')+1:].strip()
		if("(" in eprice_max):
			eprice_usd=eprice_max[eprice_max.index("(")+1:eprice_max.rindex(")")].strip()
			eprice_max=eprice_max[:eprice_max.index("(")].strip()
			eprice_min_usd=eprice_usd[:eprice_usd.index("-")].strip()
			eprice_min_usd=scurr(eprice_min_usd)[1]
			eprice_max_usd=eprice_usd[eprice_usd.index("-")+1:].strip()
			eprice_max_usd=scurr(eprice_max_usd)[1]
		eprice_max=scurr(eprice_max)[1]
	attr=div.find('div',attrs={'class':'wrapper sale-wrapper'})
	attr=attr.findAll('ul')[0]
	attrs=attr.findAll('li')
	auction=attrs[1].findAll('a')[0].text
	for li in attrs:
		if('date' in li['class']):
			auction_date=li.text.strip()
		if('location' in li['class']):
			auction_location=li.text.strip()
	dim=soup.find('div',attrs={'id':'tabWindow1'})
	dim=dim.findAll('p',attrs={'class':'overview'})
	c=1
	for p in dim:
		if (c==1):
			dim=str(p).strip().split('<br>')
			if(len(dim)==7):
				signed=dim[2].strip()
				material=dim[3].strip()
				dimension=dim[4].strip()
				year=dim[5].strip()
				c+=1
		elif (c==2):
			h=soup.find('div',attrs={'id':'tabWindow1'})
			h=h.findAll('h2')
			if(h[1].text=="Provenance"):
				provenance=p.text.strip()

	print("Auction Name: " + auction)
	print("Auction Date: " + auction_date)
	print("Auction Location: " + auction_location)
	print("image: ")
	print(image)
	print("Price Realized: "+ rprice)
	print("PR Currency: " + rprice_curr)
	print("Estimated Price_min: " + eprice_min)
	print("Estimated Price_max: " + eprice_max)
	print("Estimated Price_min_usd: " + eprice_min_usd)
	print("Estimated Price_max_usd: " + eprice_max_usd)
	print("Signed: " + signed)
	print("Material: " + material)
	print("dimension: " + dimension)
	print("Year: " + year)
	print("Provenance: " + provenance)

	#writing up all the shit
	data=list()
	var={}
	var['Title']=unidecode(title.strip())
	var['Artist']=unidecode(artist.strip())
	var['Estimated Price Currency']=unidecode(eprice_curr)
	var['Estimated_Min']=unidecode(eprice_min.strip())
	var['Estimated_Max']=unidecode(eprice_max.strip())
	var['Estimated_Min_INR']=""
	var['Estimated_Max_INR']=""
	var['Estimated_Min_USD']=unidecode(eprice_min_usd.strip())
	var['Estimated_Max_USD']=unidecode(eprice_max_usd.strip())
	var['Realized_Price_Curr']=unidecode(rprice_curr)
	var['Price_Realized']=unidecode(rprice.strip())
	var['Winning_Bid_INR']=""
	var['Winning_Bid_USD']=""
	var['Buyers Prem']=""
	var['Image']=unidecode(image.strip())
	var['URL']=unidecode(link.strip())
	var['Lot']=int(lot.strip())
	var['auction']=unidecode(auction)
	var['Sale']=unidecode(saleno)
	var['Provenance']=provenance
	var['Dimensions']=unidecode(dimension.strip().decode("utf8"))
	var['Material']=unidecode(material.strip())
	var['Exhibited_and_Published']=""
	var['Signed']=unidecode(signed.decode("utf8").strip())
	var['Painted_Year']=unidecode(year.strip())
	var['Auction_House']=unidecode("Christie's")
	var['Auction_Date']=unidecode(auction_date)
	var['Location']=unidecode(auction_location)
	var['ArtID']=ourid
	data.append(var.copy())
	if(lot=="" or link==""):
		return
	WriteDictToCSV(data)
def get_lot(url,auction,day,saleno):
	artist=title=""
	print("Visiting URL: " + url)

	cursor=db.paintings.find({"AUCTION_HOUSE":"Christie's","SALE":saleno})
	ourlots=list()
	ourdb={}
	for doc in cursor:
		ourdb['ID']=doc['ID']
		ourdb['LOT']=doc['LOT']
		ourlots.append(ourdb.copy())

	print(ourlots)
	request=requests.get(url)
	data=request.content
	soup=BeautifulSoup(data,"html.parser")
	# div=soup.findAll('div',attrs={'class':'chr-primary-content'})[0]
	div=soup.find('div',attrs={'id':'divSearchbar'})
	div=div.find('strong',attrs={'class':'chr-search-lot-results'})
	lots=div.text
	lots=int(lots[lots.index('of') +2:].strip())
	print(lots)
	lot_pages=math.ceil(lots/90)+1
	print("Number of lot pages: " + str(lot_pages) )
	p=1
	while (p<=int(lot_pages)):
		url2=url+"&action=paging&pg="+str(p)
		print("at: " + url2)
		request=requests.get(url2)
		data=request.content
		soup=BeautifulSoup(data,"html.parser")
		alllots=soup.findAll('div',attrs={'class':'chr-content-results'})
		for alot in alllots:
			link=alot.findAll('a')[0]['href']
			no=alot.find('ul',attrs={'class':'chr-sale-lot'})
			no=no.find('li')
			no=no.find('a').text
			no=no[no.index('Lot')+3:].strip()
			print("Checking lot : " + no)
			for ours in ourlots:

				if(ours['LOT']==no):
					art=alot.find('div',attrs={'class':'chr-result-info'})
					if(art.find('h3')):
						artist=art.find('h3').text.strip()
					if(art.find('h5')):
						title=art.find('h5').text.strip()
						if(title==""):
							title=artist
							artist=title[:title.index(",")]
							title=title[title.index(",")+1:]
					else:
						if("," in artist):
							temp=artist
							artist=artist[:artist.index(",")].strip()
							title=temp[temp.index(',')+1:].strip()
					print("Lot: " + no)
					print("URL:" + link)
					print("Artist: " + artist )
					print("Title: " + title)
					get_final_scrape(link,artist,title,no,saleno,ours['ID'])
					break
		p=p+1

def get_scrape(auction,day,sale,url):
	print("Getting from : ")
	print(url)
	request=requests.get(url)
	data=request.content
	soup=BeautifulSoup(data,"html.parser")
	div=soup.find('div',attrs={'id':'results'})
	items=div.find('ul',attrs={'id':'list-items'})
	items=items.findAll('li')
	for li in items:
		if li.get('id'):

			if("day" in li['id']):

				info=li.find('div',attrs={'class':"auction-info"})
				saleno=info.find('span',attrs={'class':"sale"})
				if(saleno and sale != "N/A"):
					saleno=saleno.findAll('a')[0].text.strip()
					print("got sale no: " + saleno)
					if(int(saleno)==int(sale)):
						print("FOUND MATCH")
						location=info.find('span',attrs={'class':"location"})
						if(location):
							location=location.text
						else:
							location="N/A"
						dec=info.find('p',attrs={'class': "description"})
						a=dec.find('a',attrs={'class':"description"})['href']
						try:
							saleid=a[a.rindex('-')+1:a.rindex('.')].strip()
							url='http://www.christies.com/lotfinder/salebrowse.aspx?intsaleid='+ saleid + '&viewType=list&num=90'
							get_lot(url,auction,day,saleno)
						except Exception as e:
							print(str(e))




				else:
					dec=info.find('p',attrs={'class': "description"})
					desc=dec.find('a',attrs={'class':"description"}).text.strip()
					print("Christie: " + desc)
					print("Ours: " + auction)
					if(auction.upper() == desc.upper()):
						print("FOUND MATCH BY NAME!")
						a=dec.find('a',attrs={'class':"description"})['href']
						saleid=a[a.rindex('-')+1:a.rindex('.')].strip()
						url='http://www.christies.com/lotfinder/salebrowse.aspx?intsaleid='+ saleid + '&viewType=list&num=90'
						get_lot(url,auction,day,"")

def get_page(month,year,day,sale,auction):
	try:
		print("getting url")
		url="http://www.christies.com/results/?month=" + str(month)+"&year=" + str(year) + "&locations=&scids=&action=paging&initialpageload=false&pg=1"
		print(url)
		request=requests.get(url)
		data=request.content
		soup=BeautifulSoup(data,"html.parser")
		div=soup.find('div',attrs={'id':'results-nav'})
		if(div):
			p=div.findAll('p')[0]
			results=p.text
			if(results==""):
				print("No auctions found")
				return
			results=results[results.index('of')+2:].strip()
			results=int(results)
			print(results)
			page_count=math.ceil(results/30)
			page_count=int(page_count)+1
			print("Page Count: " + str(page_count))
			count=1
			while(count<=page_count):
				url="http://www.christies.com/results/?month=" + str(month)+"&year=" + str(year) + "&locations=&scids=&action=paging&initialpageload=false&pg="+str(count)
				get_scrape(auction,day,sale,url)
				count+=1
	except Exception as e:
		print(str(e))



	# print(div)
cursor=db.paintings.aggregate([{"$match":{"AUCTION_HOUSE":"Christie's"}},{"$group":{"_id":{"AUCTION_NAME":"$AUCTION_NAME","SALE_DATE":"$SALE_DATE","SALE":"$SALE"}}}])
datetime=list()
datetime=[{"mon":"Jan","val":1},{"mon":"Feb","val":2},{"mon":"Mar","val":3},{"mon":"Apr","val":4},{"mon":"May","val":5},{"mon":"Jun","val":6},
{"mon":"Jul","val":7},{"mon":"Aug","val":8},{"mon":"Sep","val":9},{"mon":"Oct","val":10},
{"mon":"Nov","val":11},{"mon":"Dec","val":12}]
for document in cursor:

	date=document['_id']['SALE_DATE'].strip()
	name=document['_id']['AUCTION_NAME'].strip()
	sale=document['_id']['SALE'].strip()
	print(name)
	print(date)
	print(sale)
	month=date[date.index('-')+1:date.rindex("-")].strip()
	#finding month number
	for d in datetime:
		if (month==d['mon']):
			month=d['val']
			break
	#finding year

	year=date[date.rindex("-")+1:].strip()
	if(int(year)>0 and int(year)<17):
		year="20" + year
	else:
		year="19" + year
	#finding date
	day=date[:date.index("-")].strip()
	print(month)
	print(year)
	print(day)
	get_page(month,year,day,sale,name)
