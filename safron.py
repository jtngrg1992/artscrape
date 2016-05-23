import os
from selenium import webdriver
import csv
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import math
import sys
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
house="Saffron"
csv_columns = ["Title","Lot","Artist","auction","Estimated_Min_INR","Estimated_Max_INR",
"Estimated_Max_USD","Estimated_Min_USD","Winning_Bid_INR","Winning_Bid_USD","Buyers Prem",
"Provenance","Exhibited_and_Published","Dimensions", "Material","Signed" , "Painted_Year","Image","URL","Auction_House","Auction_Date"]
currentPath = os.getcwd()
csv_file = "safronscrape.csv"
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



browser.get('http://www.saffronart.com/auctions/allauctions.aspx')
content=browser.page_source
soup=BeautifulSoup(content, "html.parser")
div=soup.find('div',attrs={'id':'dv_html'})
# print(soup)
td=div.findAll('td')
i=1
for t in td:
	name=date=""
	if(i<82):
		i=i+1
		continue
	p=t.findAll('p')
	name=p[0].find('b').text.strip()
	print(name)
	date=p[1].text.strip()
	print("Auction Date: " + date)
	a=t.findAll('a')
	url=a[0]['href']
	url2=url[url.index('auctions')+len('auctions'):]
	furl='http://www.saffronart.com/auctions' + url2
	print("URL" + furl)
	#jumping to single painting 
	browser.get(furl)
	content=browser.page_source
	soup=BeautifulSoup(content,"html.parser")
	id=soup.findAll('div',attrs={'class':'WantThis'})
	id=id[0]['data-id']
	print("ID: " + id)
	purl='http://www.saffronart.com/auctions/PostWork.aspx?l='+id
	print("Painting url: " + purl)
	#on painting page, extracting information
	request=requests.get(purl)
	data=request.content
	soup=BeautifulSoup(data,'html.parser')
	detail=soup.find('div',attrs={'class':'artworkDetails'})
	div=detail.findAll('h3')
	lot=div[0].find('div')
	for tag in lot.findAll('a'):
		tag.decompose()
	lot=lot.text.strip()
	lot=lot[lot.index("of")+len("of"):].strip()
	tlot=int(lot)
	print("Total Lots: " + str(lot))
	count=0
	while(count<tlot):
		try:
			#initializing all variables
			est_min_int=est_max_inr=est_min_usd=est_max_usd=incl_of_bp=""
			winning_inr=winning_usd=img=artist=title=dimensions=desc=signed=material=year=lot=""
			provenance=pub=""
			id2=int(id)+int(count)
			url='http://www.saffronart.com/auctions/PostWork.aspx?l='+str(id2)
			print("On : " + url)
			# request=requests.get(url)
			# data=request.content

			browser.get(url)
			data=browser.page_source
			soup=BeautifulSoup(data,'html.parser')
			detail=soup.find('div',attrs={'class':'artworkDetails'})
			print("on lot : " + str(count))
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
			# text.replace("\n"," ")
			text=text.strip().split('<br \="">')
			# print(text)
			if (len(text)==4):
				year=text[0].strip('<p>').strip().replace("\n","")
				if(len(year)>4):
					signed=year.translate(None,";").strip().replace("\n","")
					year=""
				material=text[1].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")
				dimensions=text[2].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")
			else: 
				signed=text[0].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")
				year=text[1].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")
				material=text[2].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")
				dimensions=text[3].strip('<p>').strip().replace("'","").replace('"',"").replace("\n","")

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
				provenance=provenance[provenance.index('PROVENANCE')+len('provenance:'):].replace("'","").replace('"',"").replace("\n","")
				print("Provenance: " + provenance)
			details=detail.find('p',attrs={'id':'ContentPlaceHolder1_AboutWork1__PublishingDesc'})
			if(details):
				pub=details.text.strip().replace("'","").replace('"',"").replace("\n","")
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
				var['Lot']=int(lot.strip())
				var['auction']=unidecode(name)
				var['Provenance']=unidecode(provenance.strip())
				var['Dimensions']=unidecode(dimensions.strip())
				var['Material']=unidecode(material.strip())
				var['Exhibited_and_Published']=unidecode(pub.strip())
				var['Signed']=unidecode(signed.strip())
				var['Painted_Year']=unidecode(year)
				var['Auction_House']=unidecode(house)
				var['Auction_Date']=unidecode(date)
				datalist.append(var.copy())
				WriteDictToCSV(datalist)
				# print(var)
			except Exception as e:
				print(str(e))
			count+=1
		except:
			count+=1
			
	
