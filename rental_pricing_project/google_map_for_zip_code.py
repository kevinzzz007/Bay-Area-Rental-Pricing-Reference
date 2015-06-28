__author__ = 'RunzeZhao'
from geopy.geocoders import Nominatim
import pymongo
from pymongo import MongoClient
import urllib2
import sys
import re
import urllib2
import pprint
import json
import time
add = "Buckingham Palace, London, SW1A 1AA"
#postgresql

client = MongoClient()
db = client.rental_pricing
collection = db.partial_links
geolocator = Nominatim(timeout=10)
n = 0


for each_google_map_link in collection.find():
  try:
    print each_google_map_link['zip_code']
  except KeyError:
    if each_google_map_link['google_map_link'] != 'no_google_map_link':
        if 'q=loc' in each_google_map_link['google_map_link']:
            l = each_google_map_link['google_map_link']
            for one in re.finditer(r'q=loc%3A',l):
                add = l[one.end(0):].replace('+',' ').strip()
                add = urllib2.quote(add)
                geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=us" % add
                # print geocode_url
                req = urllib2.urlopen(geocode_url)
                jsonResponse = json.loads(req.read())
                print jsonResponse
                print int(len(jsonResponse['results'][0]['address_components'])-1)
                zip_code = jsonResponse['results'][0]['address_components']\
                    [int(len(jsonResponse['results'][0]['address_components'])-1)]['long_name']
                # pprint.pprint(jsonResponse['results'][0]['address_components'][6]['long_name'])
                n +=1
                collection.update({'_id':each_google_map_link['_id']}, {'$set': {'zip_code':zip_code}})
                # sys.exit(0)
                print n
                time.sleep(10)
        else:
            l = each_google_map_link['google_map_link']
            for one in re.finditer(r'@',l):
                for second in re.finditer(r'16z',l):
                    add = l[one.end(0):second.start(0)].rstrip(',')
                    location = geolocator.reverse(add)
                    print location.raw['address']
                    try:
                        zip_code = (location.raw['address']['postcode'])
                        collection.update({'_id':each_google_map_link['_id']}, {'$set': {'zip_code':zip_code}})
                    except KeyError:
                        collection.update({'_id':each_google_map_link['_id']}, {'$set': {'zip_code':'cant_locate_zip_code'}})
                    n +=1
                    print n
                    time.sleep(10)
                    # sys.exit(0)