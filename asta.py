import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def scurr(n):
    n=n.replace(",","")
    n=re.split(r'(\d+)',n)

    return([n[0],n[1]])
def constructBody(text):
    body={
    '__EVENTTARGET':text,
    '__EVENTARGUMENT':'',
    '__LASTFOCUS':'',
    '__VIEWSTATE':'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',
    '__EVENTVALIDATION':'/wEWWwKpy4HDDALEhKj+DQK3yOz+CwK4p8aQBwK5p8aQBwK7p8aQBwK8p8aQBwK9p8aQBwK+p8aQBwKvp8aQBwKgp8aQBwK4p4aTBwK4p4qTBwK4p46TBwK4p7KTBwK4p7aTBwK4p7qTBwK4p76TBwK4p6KTBwK4p+aQBwK4p+qQBwK5p4aTBwK5p4qTBwK5p46TBwK5p7KTBwK5p7aTBwK5p7qTBwK5p76TBwK5p6KTBwK5p+aQBwK5p+qQBwK6p4aTBwK6p4qTBwK6p46TBwK6p7KTBwK6p7aTBwK6p7qTBwK6p76TBwK6p6KTBwK6p+aQBwK6p+qQBwK7p4aTBwKXp+aXCQK7p4qTBwK7p46TBwK7p7KTBwK7p7aTBwK7p7qTBwK7p76TBwK7p+aQBwK7p+qQBwK8p4aTBwK8p4qTBwK8p46TBwK8p7KTBwK8p7aTBwK8p7qTBwK8p76TBwK8p6KTBwK8p+aQBwK8p+qQBwK9p4aTBwK9p4qTBwK9p46TBwK9p7KTBwK9p7aTBwK9p7qTBwK9p76TBwK9p6KTBwK9p+aQBwK9p+qQBwK+p4aTBwK+p4qTBwK+p46TBwK+p7KTBwK+p7aTBwK+p7qTBwK+p76TBwK+p6KTBwK+p+aQBwK+p+qQBwKvp4aTBwKzrP4HAur69fAPAtmhnrsIAtmhspYBAtmhxvEJAtmh2swCAtmh7qcLAtmhgoMEAtmhlt4MX/Btbv1oDzPm0hV/0owAlsAZ+Ts='
            }
    return body

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
        s = requests.Session()
        response = s.post(url, data=body)
        soup=BeautifulSoup(response.content,'html.parser')
        count+=1
    return
    
    # url="http://www.astaguru.com/"+url
    # print("Getting scrape from URL: " + url)
    # data=requests.get(url).content
    # soup=BeautifulSoup(data,"html.parser")
    arts=soup.find("div",attrs={'id':'content'}).find('div',attrs={'id':'column2'}).find('table').findAll('tr')[1]
    arts=arts.find("table").findAll('tr',attrs={'align':'left','valign':'middle'})
    counter=1
    print(len(arts))
    for art in arts:
        if(counter==1):
            counter+=1
        else:
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
            for a in attributes:
                if("Lot. No." in a.findAll('td')[0].text.strip()):

                    lot=a.findAll('td')[2].text.strip()
                    print("Lot: " + lot)
                    continue
                if("Artist" in a.findAll('td')[0].text.strip()):
                    artist=a.findAll('td')[2].text.strip().replace("\n","")
                    print("Artist: " + artist)
                    continue
                if("Title" in a.findAll('td')[0].text.strip()):
                    art=a.findAll('td')[2].text.strip()
                    print("Title: " + art)
                    continue
                if("Medium" in a.findAll('td')[0].text.strip()):
                    medium=a.findAll('td')[2].text.strip()
                    print("medium: " + medium)
                    continue
                if("Year" in a.findAll('td')[0].text.strip()):
                    year=a.findAll('td')[2].text.strip()
                    print("year: " + year)
                    continue
                if("Size" in a.findAll('td')[0].text.strip()):
                    size=a.findAll('td')[2].text.strip()
                    print("Size: " + size)
                ####GETTING ESTIMATES######################
                if("Estimate" in a.findAll('td')[0].text.strip()):
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
                    text=a.findAll('td')[0].text.strip().split("\n")
                    for t in text:
                        if("Exhibited" in t):
                            exhibited=t
                            print("Exhibited: " + exhibited)
                        if("Provenance" in t):
                            provenance=t
                            print("Provenance: " + provenance)
                        if("Signed" in t):
                            signed=t
                            print("Signed: " + signed)
                



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
           
            else:
                winning=attributes[attributes.index("(inclusive of")+ len("(inclusive of xx% Buyers Premium)"):]
                sale1=winning.split("\n")[0].strip()
                sale2=winning.split("\n")[len(winning.split("\n"))-1].strip()
                curr_sale1=scurr(sale1)[0]
                if("US" in curr_sale1):
                    curr_sale1="USD"
                sale1=scurr(sale1)[1]
                
                sale.append({
                    curr_sale1 : sale1
                    })
                curr_sale2=scurr(sale2)[0]
                sale2=scurr(sale2)[1]
                sale.append({
                    curr_sale2 : sale2
                    })
            print("Sale: " )
            print(sale)
            
            print("Jumping to next rec")

    # print(arts)
    

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
    
