#!/bin/python
import pymongo
from urllib import request
from pymongo import Connection
connection=Connection()
database=connection['bitcoin']
mycollection=database.entries
loop = mycollection.count()
count = 0
for x in range(0, loop):
        confirmed = mycollection.find()[count]
        count = count + 1
        srcurl = "https://blockchain.info/q/getreceivedbyaddress/"
        address = confirmed['Address']
        confirmations = "?confirmations=6"
        confirmedurl = srcurl+address+confirmations
        confirmedget = request.urlopen(confirmedurl)
        encoding = confirmedget.headers.get_content_charset()
        confirmedobj = confirmedget.read().decode(encoding)
        id = confirmed['_id']
        price = confirmed['Price']
        if int(confirmedobj) >= int(price):
                mycollection.update({'_id':id}, {'$set': {'Confirmed':"Yes"}})
