import urllib
import csv


csvfile = open('safronscrape.csv', 'r')
reader=csv.DictReader(csvfile, delimiter="^")
try:
	count=1
	for row in reader:
		if(count<=540):
			print("Encountered")
			count+=1
			continue
			#do nothing
		else:
			image=row['IMAGE']
			image=image.replace("_big.jpg","_hires.jpg")
			print("url: " + image)
			uri="images/"+str(row['ID'])+".jpg"
			print(uri)
			urllib.urlretrieve(image, uri)



except Exception as e:
	print(str(e))
