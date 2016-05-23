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


id=40000
flag=0


def scurr(n):
	n=n.replace(",","")
	n=re.split(r'(\d+)',n)
	return([n[0],n[1]])

def insertToDB(dat):
    dbclient = pymongo.MongoClient("45.55.232.5:27017")
    dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
    db=dbclient.artists
    data=db.test
    data.insert(dat)


def final_scrape(url,artist,lot,sale):
    global id
    id+=1
    provenance=auction_name=auction_date=auction_location=description=art=""
    print("Artist: " + artist)
    print("Lot: " + lot )
    print("Sale: " + sale)
    print("Getting Final scrape from : " + url)
    data=requests.get(url).content
    soup=BeautifulSoup(data,"html.parser")
    facts=soup.find('div',attrs={'class':'quick-facts'})

    # GETTING SALE PRICES#######################################
    if(facts.find('div',attrs={'id':'price-realized-wrapper'})):
        pr=facts.find('div',attrs={'id':'price-realized-wrapper'}).findAll('ul')[0].findAll('li')
        for i in pr:
            if('sublist-item' in i['class']):
                saleprice=i.text
                if("Set Currency" in saleprice):
                    saleprice=saleprice[:saleprice.index("Set Currency")].strip()
                curr_of_sale=scurr(saleprice)[0].strip()
                saleprice=scurr(saleprice)[1].strip()
                fnlsale=list()
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

    pe=facts.find('div',attrs={'class':'wrapper estimate-wrapper'}).findAll('ul')[0].findAll('li')
    counter=1
    estsale_min=list()
    estsale_max=list()
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



def iterate(url,artist):

    lot=sale=""
    data=requests.get(url).content
    soup=BeautifulSoup(data,"html.parser")
    ul = soup.find("div",attrs={'class':'gridView'}).findAll('ul')[0]
    items=ul.findAll('li')
    c=1
    found=0
    for item in items:
        if item.get('class'):
            continue
        else:
            detail=item.find('div',attrs={'class':'detailscontainer'}).text.strip().split("\n")[0]

            if(artist.upper() in detail.upper()):
                print("FOUND MATCH!")
                found=1

                link=item.find('div',attrs={'class':'image-container'}).findAll('a')[0]['href']
                print("Scraping art from: " + link)
                info=item.find('div',attrs={'class':'infoContainer'}).findAll('ul')[0]
                li=info.findAll('li')
                for i in li:

                    if('lotDetails' in i['class']):
                        lot=scurr(i.findAll('a')[0].text)[1].strip()
                        sale=scurr(i.findAll('a')[1].text)[1].strip()
                        final_scrape(link,artist,lot,sale)
    global flag
    if(found==0):
        flag+=1
    else:
        flag=0


# session=Session()
# # session.head("http://jlabs.co/art/api.php?artists")
#
# response=sesn.loads(response.text)
dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
db=dbclient.artists
cursor=db.allartists.find({})
skipped=list()
for doc in cursor:


    artist=doc['artist']
    if(artist not in ['Jamini Roy']):
        continue
    # artist="Jamini Roy"
    print("Searching for artist: "+ artist)
    temp=artist
    artist=urllib.quote_plus(artist)

    url="http://www.christies.com/lotfinder/searchresults.aspx?&searchfrom=header&lid=1&entry="+artist+"&searchtype=p&action=search"
    print("Visiting: " + url)
    request=requests.get(url)
    data=request.content
    soup=BeautifulSoup(data,"html.parser")
    count=soup.find('span',attrs={'class':'count count-upcoming'})
    count=count.text[count.text.index("(")+1:count.text.index(")")].strip()
    print("Total Lots: " + count)
    pages=int(count)/18
    if(int(count)%18>0):
        pages+=1
    print("Pages: " + str(pages))
    count=1

    while(count<=pages):

        if(flag>3):
            print("DIM CHANCES OF FINDING THE ARTIST, JUMPING TO NEXT ONE")
            flag=0
            skipped.append(temp)
            break
        url="http://www.christies.com/lotfinder/searchresults.aspx?&searchfrom=header&lid=1&entry="+artist+"&searchtype=p&action=paging&pg="+str(count)

        print("Getting scrape: "+ url)
        iterate(url,temp)
        count+=1

print("Scrape Complete, artist skipped: ")
print(skipped)
