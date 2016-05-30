import requests
import json
import pymongo

def getJson(url,date):
    data=requests.get(url).content
    print(data)
    var={}
    var[date]=json.loads(data)['rates']
    dbclient = pymongo.MongoClient("45.55.232.5:27017")
    dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
    db=dbclient.artists
    data=db.datelib
    data.insert(var)
###CONSTRUCTING DATE###################
year=1990
while (year<=2016):
    month=1
    while(month<=12):
        if(month in [1,3,5,7,8,10,12]):
            dayLimit=31
        elif(month in [2] and year%4==0):
            dayLimit=29
        elif(month in [2]):
            dayLimit=28
        else:
            dayLimit=30
        day=1
        while(day<=dayLimit):
           date=str(month) + "-" + str(day) + "-" + str(year) 
           print("Date: " + date)
           url='http://www.sothebys.com/en/auctions/list/_jcr_content.currencyRates.json/'+str(date)
           print(url)
           getJson(url,date)
           day+=1
        month+=1
    year+=1
        
