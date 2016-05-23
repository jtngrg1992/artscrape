import os
import csv
import requests
import urllib
from requests import Session
from unidecode import unidecode
from bs4 import BeautifulSoup
import json
import math
import re
import sys
import pymongo
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import xmltodict

id=40000

def scurr(n):
	n=n.replace(",","")
	n=re.split(r'(\d+)',n)
	return([n[0],n[1]])

def insertToDB(dat):
    dbclient = pymongo.MongoClient("45.55.232.5:27017")
    dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
    db=dbclient.artists
    data=db.christie4
    data.insert(dat)
def get_scrape(url,soup):
    global id
    id+=1
    artist=art=sale=lot=provenance=auction_name=auction_date=auction_location=description=art=""
    header=soup.find('div', attrs={'class':'details-content-header'})
    artist=header.find('h1').text
    if(header.find('h2')):
        art=header.find('h2').text.strip()
    details=soup.find('div',attrs={'class':'details-header'}).findAll('span')
    for span in details:
        if("sale" in span['class']):
            sale=span.find('a').text[span.find('a').text.index("SALE")+4:].strip()
        if("lot" in span['class']):
            lot=span.text[span.text.index('Lot')+3:].strip()
    print("Artist: " + artist)
    print("Art: " +art)
    print("Lot: " + lot )
    print("Sale: " + sale)

    facts=soup.find('div',attrs={'class':'quick-facts'})

    # GETTING SALE PRICES#######################################
    fnlsale=list()
    if(facts.find('div',attrs={'id':'price-realized-wrapper'})):
        pr=facts.find('div',attrs={'id':'price-realized-wrapper'}).findAll('ul')[0].findAll('li')
        for i in pr:
            if('sublist-item' in i['class']):
                saleprice=i.text
                if("Set Currency" in saleprice):
                    saleprice=saleprice[:saleprice.index("Set Currency")].strip()
                curr_of_sale=scurr(saleprice)[0].strip()
                saleprice=scurr(saleprice)[1].strip()

                if(curr_of_sale=="$"):
                    curr_of_sale="USD"
                saleprice={
                    curr_of_sale:saleprice
                }
                fnlsale.append(saleprice.copy())
                # print("Sale price: " + saleprice)
            if('currency-info-item' in i['class']):
                spusd=scurr(i.text[i.text.index("("):i.text.index(")")])[1]
                spusd={
                    "USD":spusd
                    }
                fnlsale.append(spusd.copy())
                # print("Sale price in USD: " + spusd)
    print("Sale array: ")
    print(fnlsale)

    #GETTING ESTIMATE PRICES############################################################
    estsale_min=list()
    estsale_max=list()
    pe=facts.find('div',attrs={'class':'wrapper estimate-wrapper'}).findAll('ul')[0].findAll('li')
    counter=1
    for i in pe:
        if("-" not in i.text.strip()):
            break
        if(counter==1):
            estimate=i.text.strip()
            est_min=estimate[:estimate.index("-")].strip()
            if(scurr(est_min)[0]=="$"):
                curr="USD"
            else:
                curr=scurr(est_min)[0]
            est_min={
                curr:scurr(est_min)[1]
            }
            estsale_min.append(est_min.copy())
            est_max=estimate[estimate.index("-")+1:].strip()
            est_max={
                curr:scurr(est_max)[1]
            }
            estsale_max.append(est_max.copy())
            # print("Estimate: " + estimate)
        if(counter==2):
            estimateusd=i.text[i.text.index("("):i.text.index(")")].strip()
            minusd={
                "USD":scurr(estimateusd[:estimateusd.index("-")].strip())[1]
            }
            maxusd={
                "USD":scurr(estimateusd[estimateusd.index("-")+1:].strip())[1]
            }
            estsale_min.append(minusd.copy())
            estsale_max.append(maxusd.copy())
            # print("Estimate USD: " + estimateusd)
        counter+=1
    print("Estimated Min:")
    print(estsale_min)
    print("Estimated Max:")
    print(estsale_max)

    #GETTING DATE,AUCTION NAME AND LOCATION#########

    det=facts.find('div',attrs={'id':'contact-us-wrapper'}).findAll('ul')[0].findAll('li')
    counter=1
    for i in det:
        if(counter==2):
            auction_name=i.find('a').text.strip()
        if(counter==3):
            auction_date=i.text.strip()
        if(counter==4):
            auction_location=i.text.strip()
        counter+=1

    #GETTING LOT DESCRIPTION##########################################3

    desc=soup.find('div',attrs={'id':'tabWindow1'})
    h=desc.findAll('h2')
    p=desc.findAll('p',attrs={'class':'overview'})
    counter=0
    for heading in h:
        if(heading.text.strip()=="Lot Description"):
            description=p[counter].text.strip()
            print("Description: " + description)
        if(heading.text.strip()=="Provenance"):
            provenance=p[counter].text.strip()
            print("Provenance: " + provenance)
        counter+=1

    #GETTING ART TITLE#################################################

    title=soup.find('div',attrs={'class':'details-content-header'}).find('h2')
    if(title):
        art=title.text.strip()
        print("Art Title: " + art)

    #GETTING IMAGE####################################################

    img=soup.find('div',attrs={'id':'lot-images-summary'}).find('div',attrs={'class':'featured-img-wrap'}).findAll('img')[0]
    image=img['src']
    print("Image Link: " + image)
    print("Inserting into DB!!")
    #CREATING DICT TO INSERT IN MONGODB#############################

    var={}
    var['PAINTED_YEAR']=""
    var['SIGNED?']=""
    var['MEDIUM']=""
    var['AUCTION_LOCATION']=unidecode(auction_location)
    var['ORIENTATION']=""
    var['YOB']=""
    var['CURR_OF_SALE']=""
    var['IMAGE_ID']=""
    var['SIZE_H']=""
    var['PROVENANCE']=""
    var['MATERIAL']=""
    var['PROVENANCE_TEXT']=unidecode(provenance)
    var['IMAGE_LINK']=unidecode(image)
    var['LOT#']=unidecode(lot.strip())
    var['ARTIST']=unidecode(artist)
    var['MARKINGS_TEXT']=""
    var['UNIT_OF_MEASURE']=""
    var['ESTIMATE_MAX']=estsale_max
    var['ESTIMATE_MIN']=estsale_min
    var['SALE#']=sale
    var['YOD']=""
    var['NATIONALITY']=""
    var['TYPE']=""
    var['AUCTION_NAME']=unidecode(auction_name)
    var['DATED?']=""
    var['SIZE_W']=""
    var['URL']=unidecode(url)
    var['AUCTION_HOUSE']="Christie's"
    var['PRICE_SOLD']=fnlsale
    var['DIMENTIONS_TEXT']=""
    var['ID']=id
    var['ESTIMATE_MIN']=estsale_min
    var['MATERIAL_TEXT']=""
    var['SALE_DATE']=unidecode(auction_date)
    var['TITLE_OF_PAINTING']=unidecode(art)
    var['DESCRIPTION']=unidecode(description)
    insertToDB(var)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
}

#get artist
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
db=dbclient.artists
cursor=db.artist_list.find({})
skipped=list()
for doc in cursor:
    skipcounter=1
    if(doc['id']<=21):
        continue
    artist=doc['artist']
    temp=artist
    print("Searching for artist: "+ artist)
    artist=urllib.quote_plus(artist)
    #getting the first page data
    pagecounter=1
    while(pagecounter<=2):
        if(pagecounter==1):
            print("Getting scrape for first page")
            pagecounter+=1
            body={
                'StrUrl':'/lotfinder/searchresults.aspx?searchfrom=header&lid=1&entry='+artist+'&searchtype=p&action=paging&pg=1',
            'GeoCountryCode':'IN',
            'LanguageID':'1',
            'IsLoadAll':'1',
            'PageSize':'18',
            'ClientGuid':''
            }
        else:
            pagecounter+=1
            print("Getting scrape from rest of the pages")
            body={
                'StrUrl':'/lotfinder/searchresults.aspx?searchfrom=header&lid=1&entry='+artist+'&searchtype=p&action=paging&pg=2',
            'GeoCountryCode':'IN',
            'LanguageID':'1',
            'IsLoadAll':'1',
            'PageSize':'18',
            'ClientGuid':''
            }
        s = requests.Session()
        response = s.post('http://www.christies.com/interfaces/LotFinderAPI/SearchResults.asmx/GetSearchResults', data=body, headers=headers)
        tree=ET.ElementTree(ET.fromstring(response.content))
        arr=list()
        root=tree.getroot()
        print(root.tag)
        for child in root:
            # print(child.tag)
            if(child.tag=='{http://www.christies.com/LotFinderAPI/Searchresults}TotalRecords'):
                print("Total records acc to API: " + child.text)
            if(child.tag=='{http://www.christies.com/LotFinderAPI/Searchresults}LotList'):
                print("iterating through lots")
                for lot in child:
                    if(lot.tag=="{http://www.christies.com/LotFinderAPI/Searchresults}LotData"):
                        for art in lot:
                            if art.tag=="{http://www.christies.com/LotFinderAPI/Searchresults}LotLink":
                                print(art.text)
                                arr.append(art.text)


        print("Total: ")
        print(len(arr))



        ref=1
        for url in arr:

            print("Checking: " + url)
            try:
                data=requests.get(url).content
            except:
                continue
            soup=BeautifulSoup(data,"html.parser")
            header=soup.find('div',attrs={'class':'details-content-header'})
            title=header.find('h1').text
            if(temp.lower() in title.lower()):
                print("REFRENCE No: " + str(ref))
                ref+=1
                get_scrape(url,soup)
            else:
                skipcounter+=1
            if(skipcounter>70):
                print("Dim chances of finding this artist further, skipping..")
                skipcounter=1
                break
