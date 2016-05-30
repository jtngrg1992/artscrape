import os
import requests
from requests import Session
from urllib2 import urlopen, Request

from bs4 import BeautifulSoup
import json
import math
import re
import sys
import pymongo
from pymongo import MongoClient
import urllib
from unidecode import unidecode
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)    


dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
db=dbclient.artists
cursor=db.artist_list.find().sort([('id',1)])
skipped=list()
id=50000
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
def insertToDB(dat):
    dbclient = pymongo.MongoClient("45.55.232.5:27017")
    dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
    db=dbclient.artists
    data=db.sotheby
    data.insert(dat)

def get_desc(link):
    description=image=""
    exception=False
    while( not exception):
        try:
            data=requests.get(link).content
            exception=True
        except Exception as e:
            print(str(e))
            print("Retrying")
            exception=False
        
    soup=BeautifulSoup(data,'html.parser')
    if(soup.find('div',attrs={"class":"lotdetail-description-text"})):
        description=soup.find('div',attrs={"class":"lotdetail-description-text"})
    if(soup.find('div',attrs={'id':'main-image-container'})):
        text=soup.find('div',attrs={'id':'main-image-container'}).findAll('img')[0]['src']
        image="http://www.sothebys.com" + text
    return str(description),image

def get_scrape(url,artist):
        provenance=title=sale=lot=auction_name=auction_location=auction_date=description=art=material=dim=painted_year=signed=""
        exception="true"

        while(exception=="true"):
            try:
                response = requests.get(url)
                data=json.loads(response.content.decode("utf-8"))
                exception="false"

            except Exception as e:
                print(str(e))
                exception="true"
                print("Retrying")
        for result in data['searchResults']:
            print("Checking: " +  result['url'])
            if(not result.get('guaranteeLine')):
                print("Guarantee line not found!!")
                continue
            artist_strpd=artist.replace(".","").replace(" ","")
            print(artist_strpd )
            match_strpd=result['guaranteeLine'].replace(".","").replace(" ","")
            print(match_strpd)
            if(artist_strpd.upper() in match_strpd.upper()):

                global id
                id+=1
                print("FOUND MATCH!!")
                print("ID: " + str(id))
                artist2=strip_tags(result['guaranteeLine'])
                print("Artist: " + artist2)
                if(result.get('title')):
                    auction_name=result['title']
                    print("Auction Name: " + auction_name)
                if(result.get('url')):
                    link="http://www.sothebys.com" + result['url']
                    print("Art Link: " + link)
                if(result.get("saleNumber")):
                    sale=result['saleNumber']
                    print("Sale Number: " + sale)
                if(result.get('eventDateDisplay')):
                    auction_date=result['eventDateDisplay']
                    print("Auction Date: " + auction_date)
                if(result.get('locations')):
                    auction_location=result['locations'][0]
                    print("Auction Location: " + auction_location)
                if(result.get('mediumTxt')):
                    material=result['mediumTxt']
                    print("Material: " + material)
              
                if(result.get('lotNumber')):
                    lot=result['lotNumber']
                if(result.get('titleOfWork')):
                    art=strip_tags(result['titleOfWork'])
                    print("Title: " + art)
                if(result.get('currency')):
                    curr=result['currency']

                #####CONTRUCTING ESTIMATE ARRAY
                estminlst=list()
                estmaxlst=list()
                if(curr!="USD"):
                    estminlst.append({
                        curr : result['lowPrice']
                    })
                    estmaxlst.append({
                        curr : result['highPrice']
                    })
                estminlst.append({
                    "USD" : result['lowEstimateUSD']
                })


                estmaxlst.append({
                    "USD" : result['highEstimateUSD']
                })

                print("Estimate Min Array: " )
                print(estminlst)
                print("Estimate Max array: ")
                print(estmaxlst)
                ###GETTING SALE ARRAY
                pricesold=list()
                if(result.get('provenance')):
                    provenance=result['provenance']
                if(result['sold']):
                    pricesold.append(
                        {curr : result['hummerPrice']})
                else:
                    pricesold.append({"Status" : "Bought-In"})
                print("Sale Array: " )
                print(pricesold)

                ###GETTING REST OF THE DESCRIPTION
                description,image=get_desc(link)
                ####Parsing description##########
                description=description.split("<br/>")
                
                for descpt in description:
                    if ('in.' in descpt.lower() or 'cm.' in descpt.lower()):
                        dim=descpt.strip()
                        print("Dimension: " + dim)
                    if('executed' in descpt.lower()):
                        painted_year=descpt.lower()
                        painted_year=painted_year[painted_year.index('executed in')+ len('Executed in'):].strip()
                        print("Year Painted: " + painted_year)
                    if('signed' in descpt.lower()):
                        signed=strip_tags(descpt).strip()
                        print("Signed: " + signed)
                description=strip_tags(str(description))
                print("Description: " + str(description))
                print("image: " + image)
                print("Inserting into DB!!")
                #CREATING DICT TO INSERT IN MONGODB#############################

                var={}
                var['PAINTED_YEAR']=painted_year
                var['SIGNED?']=""
                var['SIGNED_TEXT']=signed
                var['MEDIUM']=""
                var['AUCTION_LOCATION']=auction_location
                var['ORIENTATION']=""
                var['YOB']=""
                var['CURR_OF_SALE']=""
                var['IMAGE_ID']=""
                var['SIZE_H']=""
                var['PROVENANCE']=""
                var['MATERIAL']=""
                var['PROVENANCE_TEXT']=provenance
                var['IMAGE_LINK']=image
                var['LOT#']=lot.strip()
                var['ARTIST']=artist2
                var['MARKINGS_TEXT']=""
                var['UNIT_OF_MEASURE']=""
                var['ESTIMATE_MAX']=estmaxlst
                var['ESTIMATE_MIN']=estminlst
                var['SALE#']=sale
                var['YOD']=""
                var['NATIONALITY']=""
                var['TYPE']=""
                var['AUCTION_NAME']=auction_name
                var['DATED?']=""
                var['SIZE_W']=""
                var['URL']=link
                var['AUCTION_HOUSE']="Sothebys"
                var['PRICE_SOLD']=pricesold
                var['DIMENTIONS_TEXT']=""
                var['ID']=id
                var['MATERIAL_TEXT']=material
                var['SALE_DATE']=auction_date
                var['TITLE_OF_PAINTING']=art
                var['DESCRIPTION']=description
                insertToDB(var)
            else:
                continue




for doc in cursor:
    
    artist=doc['artist']
    # artist="Om Prakash Sharma"

    temp=artist
    artist=urllib.quote_plus(artist)

    print("Searching for artist: "+ artist)
    ##GETTING DATA FROM API#########

    url='http://www.sothebys.com/en/search?keyword='+artist+'&pageSize=11&offset=1&filters[0]=scontent_type_f|("LOT")&filters[1]=speriod_f|("Past")&currentFilter=scontent_type_f'
    print(url)
    exception="true"

    while(exception=="true"):
        try:
            response = requests.get(url)
        #   data=response.json()
            data=json.loads(response.content.decode("utf-8"))
            exception="false"

        except Exception as e:
            exception="true"
            print(str(e))
            print("retrying")
    # print(text)
    #   data = json.load(text)
    lots=data['numFound']
    print("Total Lots: " + str(lots))
    if(int(lots)<100):
        pages=1
    else:
        pages=int(lots)/100
        if(int(lots)%100>0):
            pages+=1
    print("Pages: " + str(pages))
    count=0
    while count<pages:
        offset=count*100
        url='http://www.sothebys.com/en/search?keyword='+artist+'&pageSize=100&offset='+str(offset)+'&filters[0]=scontent_type_f|("LOT")&filters[1]=speriod_f|("Past")&currentFilter=scontent_type_f'
        print("Scraping from: " + url)
        get_scrape(url,temp)
        count+=1
        
    