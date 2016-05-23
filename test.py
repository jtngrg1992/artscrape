import os
from selenium import webdriver
import csv
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import math
import sys
import string
import re
trans=string.maketrans("\n"," ")
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
house="Saffron"

csv_columns = ["Title","Lot","Artist","auction","Estimated_Min_INR","Estimated_Max_INR",
"Estimated_Max_USD","Estimated_Min_USD","Winning_Bid_INR","Winning_Bid_USD","Buyers Prem",
"Provenance","Exhibited_and_Published","Dimensions","Material","Signed" , "Painted_Year","Image","URL","Auction_House","Auction_Date"]
currentPath = os.getcwd()
csv_file = "test.csv"
j=0
def WriteDictToCSV(dict_data):
	global csv_columns
	global csv_file
	global j
	try:
		with open(csv_file, 'a+') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter='^', lineterminator='\r\n',quotechar = "'" ,fieldnames=csv_columns)
			if j == 0:
				writer.writeheader()
				j=1
			
			for data in dict_data:
				writer.writerow(data)
				
		return 1
	except Exception as e:
		print(str(e))
		return 0


est_min_int=est_max_inr=est_min_usd=est_max_usd=incl_of_bp=""
winning_inr=winning_usd=img=artist=title=dimensions=desc=date=signed=material=year=lot=""
provenance=pub=date=""
url='http://www.saffronart.com/auctions/PostWork.aspx?l=20700'
print("On : " + url)
# request=requests.get(url)
# data=request.content
browser.get(url)
data=browser.page_source
soup=BeautifulSoup(data,'html.parser')
detail=soup.find('div',attrs={'class':'artworkDetails'})
details=detail.findAll('p')[0]
details=details.text.strip()
if('Winning Bid' in details):
	estimate=details[details.index('Estimate')+len('estimate'):details.index('Winning Bid')].strip()
	if(estimate.index("Rs")<estimate.index("$")):
		est_min_inr=estimate[estimate.index("Rs")+2:estimate.index('-')].strip()
		est_max_inr=estimate[estimate.index('-')+1:estimate.index('$')].strip()
		print("est min: " + est_min_inr)
		print("est max: " + est_max_inr)
		estimate=estimate[estimate.index('$'):]
		est_min_usd=estimate[estimate.index('$') +1:estimate.index(" ")].strip()
		est_max_usd=estimate[estimate.index('-')+1:].strip()			
		print("est min usd: " + est_min_usd)
		print("est max usd: " + est_max_usd)
	else:
		est_min_usd=estimate[estimate.index('$') +1:estimate.index("-")].strip()
		est_max_usd=estimate[estimate.index('-')+1:estimate.index("Rs")].strip()			
		print("est min usd: " + est_min_usd)
		print("est max usd: " + est_max_usd)
		estimate=estimate[estimate.index("Rs"):]
		est_min_inr=estimate[estimate.index("Rs")+2:estimate.index('-')].strip()
		est_max_inr=estimate[estimate.index('-')+1:].strip()
		print("est min: " + est_min_inr)
		print("est max: " + est_max_inr)
	estimate=details[details.index('Winning Bid')+len("winning bid"):].strip()
	# details=details[details.index('Winning Bid'):]
	if(estimate.index("Rs")<estimate.index("$")):
		winning_inr=estimate[estimate.index('Rs')+2:estimate.index('$')].strip()
		if("(Inclusive of Buyer's Premium)" in estimate):
			winning_usd=estimate[estimate.index('$') + 1:estimate.index("(Inclusive of Buyer's Premium)")].strip()
			incl_of_bp="true"
		else:
			winning_usd=estimate[estimate.index('$') + 1:estimate.index("$")+estimate.index("\n")].strip()
			incl_of_bp="false"
	else:
		winning_usd=estimate[estimate.index('$') +1 : estimate.index("Rs")].strip()
		if("(Inclusive of Buyer's Premium)" in estimate):
			winning_inr=estimate[estimate.index('Rs') + 2:estimate.index("(Inclusive of Buyer's Premium)")].strip()
			incl_of_bp="true"
		else:
			winning_inr=estimate[estimate.index('Rs') + 2:estimate.index("\n")].strip()
			incl_of_bp="false"
	print("winning inr: " + winning_inr)
	print("winning usd: " + winning_usd)
	print("BP: " + incl_of_bp)
else:
	estimate=details[details.index('Estimate'):]
	if(estimate.index("Rs")<estimate.index("$")):
		est_min_inr=estimate[estimate.index('Rs')+2: estimate.index('-')].strip()
		est_max_inr=estimate[estimate.index('-')+1:estimate.index('$')].strip()	
		print("est min: " + est_min_inr)
		print("est max: " + est_max_inr)
		estimate=estimate[estimate.index('$'):]
		est_min_usd=estimate[estimate.index('$')+1:estimate.index('-')].strip()
		if("\n" in estimate):
			est_max_usd=estimate[estimate.index('-')+1:estimate.index("\n")].strip()
		else:
			est_max_usd=estimate[estimate.index('-')+1:].strip()
		if ('Import' in est_max_usd):
			est_max_usd=est_max_usd[:est_max_usd.index('Import')-1].strip()
		print("est min usd: " + est_min_usd)
		print("est max usd: " + est_max_usd)
	else:
		est_min_usd=estimate[estimate.index('$') +1:estimate.index("-")].strip()
		est_max_usd=estimate[estimate.index('-')+1:estimate.index("Rs")].strip()			
		print("est min usd: " + est_min_usd)
		print("est max usd: " + est_max_usd)
		estimate=estimate[estimate.index("Rs"):]
		est_min_inr=estimate[estimate.index("Rs")+2:estimate.index('-')].strip()
		if("\n" in estimate):
			est_max_inr=estimate[estimate.index('-')+1:estimate.index("\n")].strip()
		else:
			est_max_inr=estimate[estimate.index('-')+1:].strip()
		if('SOLD' in est_max_inr):
			est_max_inr=est_max_inr[:est_max_inr.index("SOLD")].strip()
			winning_inr="SOLD"
			print("Winning: " + win)
		print("est min: " + est_min_inr)
		print("est max: " + est_max_inr)
	incl_of_bp="false"
#finding artwork details
details=detail.findAll('p')[2]
artistdetail=details.findAll('span')[0]
artist=artistdetail.find('a').text
title=artistdetail.find('i').text
for tag in details.findAll('span'):
	tag.decompose()
text=str(details)
text.replace("\n","")
text=text.strip().split('<br \="">')
print(len(text))
# print(text)
if (len(text)==4):
	year=text[0].strip('<p>').strip().translate(None,"\n")
	if(len(year)>4):
		signed=year.translate(None,";").strip("\n").translate(None,"\n")
		year=""
	material=text[1].strip('<p>').strip().translate(None,'"').translate(None,"'").translate(None,"\n")
	dimensions=text[2].strip('<p>').strip().translate(None,"\n")
else: 
	signed=text[0].strip('<p>').strip().translate(None,'"').translate(None,"'").translate(None,"\n")
	year=text[1].strip('<p>').strip().translate(None,'"').translate(None,"'").translate(None,"\n")
	material=text[2].strip('<p>').strip().translate(None,'"').translate(None,"'").translate(None,"\n")
	dimensions=text[3].strip('<p>').strip().translate(None,"\n")

print("Signed: " + signed)
print("Year: " + year)
print("Material: " + material)
print("Dimensions: " + dimensions)
#capturing artwork details now
div=soup.find('div',attrs={'class':'artwork'})
imgdiv=div.find('div',attrs={'class':'artworkImage'})
img=imgdiv.find('img')['src']
print('Img: ' + img)
lotdiv=detail.findAll('h3')[0]
lotdiv=lotdiv.text.strip()
lot=lotdiv[lotdiv.index("Lot")+3:lotdiv.index("of")].strip()
print("lot: " + lot)
#finding provenance and other stuff

details=detail.find('p',attrs={'id':'ContentPlaceHolder1_AboutWork1__Provenance'})
if(details):
	provenance=details.text.strip()
	provenance=provenance[provenance.index('PROVENANCE')+len('provenance:'):].strip()
	re.sub(r"\n"," ",provenance)
	print("Provenance: " + provenance)
details=detail.find('p',attrs={'id':'ContentPlaceHolder1_AboutWork1__PublishingDesc'})
if(details):
	pub=details.text.strip().strip()
	re.sub(r"\n"," ",pub)
	# pub=pub[pub.index('EXHIBITED AND PUBLISHED')+len('EXHIBITED AND PUBLISHED:'):]
	print("Published: " + pub)

# artitstdiv=div.find('div',attrs={'class':'artistTitle'})
# det=artitstdiv.get_text()
# lines=det.strip().split("\n")
# # print(lines)
# if (len(lines)>1):
# 	artist=lines[0]
# 	title=lines[2]
	
# else:
# 	artist=lines[0]
print("Title: " + title)
print("Artist: " + artist)
# print(div)
# if(artitstdiv.get('a')):
# 	artist=artitstdiv.find('a').text
# else:
# 	artist=artitstdiv.find('span').text
# print("artist: " + artist)
# title=artitstdiv.find('span').text
# print("Title: " + title)
var={}

datalist=list()
try:
	var['Title']=unidecode(title.strip())
	var['Artist']=unidecode(artist.strip())
	var['Estimated_Min_INR']=unidecode(est_min_inr.strip())
	var['Estimated_Max_INR']=unidecode(est_max_inr.strip())
	var['Estimated_Min_USD']=unidecode(est_min_usd.strip())
	var['Estimated_Max_USD']=unidecode(est_max_usd.strip())
	var['Winning_Bid_INR']=unidecode(winning_inr.strip())
	var['Winning_Bid_USD']=unidecode(winning_usd.strip())
	var['Buyers Prem']=unidecode(incl_of_bp.strip())
	var['Image']=unidecode(img.strip())
	var['URL']=unidecode(url.strip())
	var['Lot']=int(lot)
	var['auction']="test"
	var['Provenance']=unidecode(provenance.strip())
	var['Dimensions']=unidecode(dimensions.strip())
	var['Material']=unidecode(material.strip())
	var['Exhibited_and_Published']=unidecode(pub.strip())
	var['Signed']=unidecode(signed.strip())
	var['Painted_Year']=unidecode(year)
	var['Auction_House']="saffron"
	var['Auction_Date']="date"
	datalist.append(var.copy())
	WriteDictToCSV(datalist)
	# print(var)
except Exception as e:
	print(str(e))



