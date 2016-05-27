import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def scurr(n):
    n=n.replace(",","")
    n=re.split(r'(\d+)',n)

    return([n[0],n[1]])

def insertToDB(dat):
    dbclient = pymongo.MongoClient("45.55.232.5:27017")
    dbclient.artists.authenticate("artSales", "Jl@B$!@#", mechanism='MONGODB-CR')
    db=dbclient.artists
    data=db.astaguru
    data.insert(dat)
def constructBody(text):
    body={
    '__EVENTTARGET':text,
    '__EVENTARGUMENT':'',
    '__LASTFOCUS':'',
    '__VIEWSTATE':'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',
    '__EVENTVALIDATION':'/wEWDgKrsOHuDgLEhKj+DQLZobKWAQLZocbxCQLZodrMAgLZoe6nCwLZoYKDBALZoZbeDALZoeqGCgLZof7hAgKt8rzoAgKs8rzoAgLyy+W3BQLuy6m4BBNjBK+d96aA4X7Cw8vwVTwYcWoA'
            }
    return body


id=70000
def get_scrape(url,auction_name,auction_date):
    url="http://www.astaguru.com/"+url
    print("Getting scrape from URL: " + url)
    data=requests.get(url).content
    soup=BeautifulSoup(data,"html.parser")
    pages=soup.find("div",attrs={'id':'content'}).find('div',attrs={'id':'column2'}).findAll('table')[0]
    pages=pages.find('span',attrs={'id':'lblTotalPages'}).text
    pages=int(pages[pages.index("Total Pages :") + len("Total Pages :"):].strip())
    print("Total Pages: " + str(pages))
    count=1
    while(count<=pages):
        target='dgp$lkbPage'+str(count)
        body=constructBody(target)
        headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'9198',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'__utmz=133912862.1463989975.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); ASP.NET_SessionId=qk5lz2ncbmtoasnxwdmlps45; __utma=133912862.1185110546.1463989975.1464084636.1464243142.7; __utmc=133912862; __utmb=133912862; _ga=GA1.2.1304275239.1463989940; _dc_gtm_UA-69753043-1=1',
        'Host':'www.astaguru.com',
        'Origin':'http://www.astaguru.com',
        'Pragma':'no-cache',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        s = requests.Session()
        response = s.post(url, data=body,headers=headers)
        soup=BeautifulSoup(response.content,'html.parser')
        if('Validation of viewstate MAC failed' in soup.find('title').text):
            print("Cant get data for this page")
            count+=1
            continue
        arts=soup.find("div",attrs={'id':'content'}).find('div',attrs={'id':'column2'}).find('table').findAll('tr')[1]

        arts=arts.find("table").findAll('tr',attrs={'align':'left','valign':'middle'})
        counter=1
        print(len(arts))
        for art in arts:
            artist=title=provenance=signed=medium=year=size=exhibited=""
            if(counter==2):
                counter+=1
            else:
                global id
                id+=1
                print("Page: " + str(count))
                print("Auction Name: " + auction_name)
                print("Auction Date: " + auction_date)
                attribs=art.findAll('td',attrs={'valign':'top','align':'center'})
                ######GETTING IMAGE URL##########################
                image=attribs[0].findAll('a')[0]['onclick']
                if "jpg" in image:
                    image=image[image.index('javascript:window.open("')+len('javascript:window.open("'):image.index(".jpg")+4]
                else:
                    image=image[image.index('javascript:window.open("')+len('javascript:window.open("'):image.index(".png")+4]
                image="http://www.astaguru.com/" + image
                print("image: " + image)

                #GETTING ATTRIBUTES#############################
                attributes=attribs[1]
                attributes=attributes.find("table").findAll('tr')
                est_flag=0
                est_min=list()
                est_max=list()
                acounter=1
                for a in attributes:
                    if("Lot. No." in a.findAll('td')[0].text.strip() and acounter==1):
                        lot=a.findAll('td')[2].text.strip()
                        print("Lot: " + lot)
                        acounter+=1
                        continue
                    if("Artist" in a.findAll('td')[0].text.strip() and acounter==2):
                        artist=a.findAll('td')[2].text.strip().replace("\n","")
                        print("Artist: " + artist)
                        acounter+=1
                        continue
                    if("Title" in a.findAll('td')[0].text.strip() and acounter==3):
                        title=a.findAll('td')[2].text.strip()
                        print("Title: " + title)
                        acounter+=1
                        continue
                    if("Medium" in a.findAll('td')[0].text.strip() and acounter==4):
                        medium=a.findAll('td')[2].text.strip()
                        print("medium: " + medium)
                        acounter+=1
                        continue
                    if("Year" in a.findAll('td')[0].text.strip() and acounter==5):
                        year=a.findAll('td')[2].text.strip()
                        print("year: " + year)
                        acounter+=1
                        continue
                    if("Size" in a.findAll('td')[0].text.strip() and acounter==6):
                        size=a.findAll('td')[2].text.strip()
                        print("Size: " + size)
                        acounter+=1
                    ####GETTING ESTIMATES######################
                    if("Estimate" in a.findAll('td')[0].text.strip() and acounter==7):
                        estimate=a.findAll('td')[2].text.strip()
                        curr1=scurr(estimate)[0]
                        if("US in curr1"):
                            curr1="USD"
                        estimate_min=scurr(estimate)[1]
                        est_min.append({
                            curr1 : estimate_min
                            })
                        estimate_max=estimate[estimate.rindex(" "):].strip().replace(",","")
                        est_max.append({
                            curr1 : estimate_max
                            })
                        est_flag=1
                        acounter+=1
                        continue
                    if(est_flag==1):
                        est_flag=0
                        estimate=a.findAll('td')[2].text.strip()
                        curr2=scurr(estimate)[0]
                        if("Rs" in curr2):
                            curr2="INR"
                        estimate_min=scurr(estimate)[1].strip()
                        est_min.append({
                            curr2 : estimate_min
                            })
                        estimate_max=estimate[estimate.rindex(" "):].strip().replace(",","")
                        est_max.append({
                            curr2 : estimate_max
                            })
                        print("Estimate Min: ")
                        print(est_min)
                        print("Estimate Max: ")
                        print(est_max)
                        continue

                    #####GETTING PROVENANCE EXHIBITION ETC######
                    else:
                        f1=f2=f3="false"
                        text=a.findAll('td')[0].text.strip().split("\n")
                        for t in text:
                            if("Exhibited" in t and f1=="false"):
                                exhibited=t
                                print("Exhibited: " + exhibited)
                                f1="true"
                                continue
                            if("Provenance" in t and f2=="false"):
                                provenance=t
                                print("Provenance: " + provenance)
                                f2="true"
                                continue
                            if("Signed" in t and f3=="false"):
                                signed=t
                                print("Signed: " + signed)
                                f3="true"
                                continue
                    



                ###GETTING WINNING BID##########
                attributes=attribs[2].text.strip()
                sale=list()
                if(attributes.upper()=="BOUGHT IN"):
                    sale.append({
                        'Status' : 'Bought-In'
                        })
                elif (attributes.upper()=="SOLD POST AUCTION"):
                    sale.append({
                        'Status' : 'Sold Post Auction'
                        })
                elif (attributes.upper()=="PRICE ON REQUEST"):
                    sale.append({
                        'Status' : 'Price On Request'
                        })
               
                else:
                    winning=attributes[attributes.index("(inclusive of")+ len("(inclusive of xx% Buyers Premium)"):]
                    sale1=winning.split("\n")[0].strip()
                    sale2=winning.split("\n")[len(winning.split("\n"))-1].strip()
                    curr_sale1=scurr(sale1)[0]
                    if("US" in curr_sale1):
                        curr_sale1="USD"
                    elif('Rs' in curr_sale1):
                        curr_sale1="INR"
                    sale1=scurr(sale1)[1]
                    
                    sale.append({
                        curr_sale1 : sale1
                        })
                    curr_sale2=scurr(sale2)[0]
                    if("US" in curr_sale2):
                        curr_sale2="USD"
                    elif('Rs' in curr_sale2):
                        curr_sale2="INR"
                    sale2=scurr(sale2)[1]
                    sale.append({
                        curr_sale2 : sale2
                        })
                print("Sale: " )
                print(sale)
                

                ######CONSTRUCTING OBJECT TO BE INSERTED#####
                var={}
                var['SIGNED?']=""
                var['ESTIMATE_MIN']=est_min
                var['UNIT_OF_MEASURE']=""
                var['DATED?']=""
                var['PRICE_SOLD']=sale
                var['MATERIAL']=""
                var['AUCTION_HOUSE']="AstaGuru"
                var['MARKINGS_TEXT']=signed
                var['SALE#']="N/A"
                var['ORIENTATION']=""
                var['ARTIST']=artist
                var['URL']=url
                var['NATIONALITY']=""
                var['PROVENANCE_TEXT']=provenance
                var['MEDIUM']=""
                var['AUCTION_NAME']=auction_name
                var['YOD']=""
                var['TITLE_OF_PAINTING']=title
                var['YOB']=""
                var['PAINTED_YEAR']=year
                var['LOT#']=lot
                var['ID']=id
                var['AUCTION_LOCATION']=""
                var['DIMENTIONS_TEXT']=size
                var['SIZE_H']=""
                var['DESCRIPTION']=""
                var['PROVENANCE']=""
                var['IMAGE_LINK']=image
                var['IMAGE_ID']=""
                var['MATERIAL_TEXT']=medium
                var['SALE_DATE']=auction_date
                var['SIZE_W']=""
                var['TYPE']=""
                var['ESTIMATE_MAX']=est_max
                print("Inserting to DB!!")
                insertToDB(var)
                print("Jumping to next rec")

       
        count+=1
        
        
        # url="http://www.astaguru.com/"+url
        # print("Getting scrape from URL: " + url)
        # data=requests.get(url).content
        # soup=BeautifulSoup(data,"html.parser")
    
    

data=requests.get("http://www.astaguru.com/Auctionresult.aspx").content
soup=BeautifulSoup(data,"html.parser")
auctions=soup.find("div",attrs={'id':'content'}).find('div',attrs={'id':'column2'}).find('table')
auctions=auctions.findAll('tr')

for auction in auctions:
    datetext=auction.findAll('td')[0].text.strip()
    ####GETTING PROPER DATE FROM TEXT#####################
    month=datetext.split("\n")[0][:3]
    rest=datetext.split("\n")[1]
    year=rest[-4:]
    day=rest[:rest.index(year)]
    auction_date=day.strip() + "-" + month.strip() + "-" +  year.strip()
    print(auction_date)

    #####GETTING AUCTION NAME
    auctiontext=auction.findAll('td')[2].find('a')
    auction_name=auctiontext.text.strip()
    print(auction_name)
    if(auctiontext['href']=="#"):
        print("No Auction URL found!!")
        continue
    get_scrape(auctiontext['href'],auction_name,auction_date)
    
