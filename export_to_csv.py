__author__ = 'RunzeZhao'
import csv
from pymongo import MongoClient


client = MongoClient()
db = client.rental_pricing
myquery = db.partial_links.find() # I am getting everything !
output = csv.writer(open('rental_pricing.csv', 'wt')) # writng in this file

for items in myquery[0:]: # first 11 entries
    try:
        zp = items['zip_code'] # collections are importent as dictionary and I am making them as list
        price = items['price']
        size = items['size']
        tt = list()
        # for chiz in a:
        if zp != 'United States':
            if zp[0]=='9':
                print zp
                tt.append(zp.encode('utf-8', 'ignore')) #encoding
                tt.append(price.encode('utf-8', 'ignore'))
                tt.append(size.encode('utf-8', 'ignore'))
        # else:
        #     tt.append("none")
    except KeyError:
        print 'no zip code'
        # tt = list()
        # tt.append('no_zip_code_yet'.encode('utf-8','ignore'))
    if len(tt) > 2:
        output.writerow(tt)