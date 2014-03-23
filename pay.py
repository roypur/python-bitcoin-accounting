#!/bin/python
from urllib import request
from pymongo import Connection
import argparse
import json
import pymongo
parser = argparse.ArgumentParser()
parser.add_argument("--address")
args = parser.parse_args()

connection=Connection()
database=connection['bitcoin']
mycollection=database.entries
fromdatabase = mycollection.find_one({"Address":args.address})


srcurl = "https://blockchain.info/q/getreceivedbyaddress/"
address = fromdatabase['Address']
confirmations = "?confirmations=6"
confirmedurl = srcurl+address+confirmations
confirmedget = request.urlopen(confirmedurl)
encoding = confirmedget.headers.get_content_charset()
confirmedobj = confirmedget.read().decode(encoding)

sendturl = srcurl+address
sendtget = request.urlopen(sendturl)
sendtobj = sendtget.read().decode(encoding)

price = fromdatabase['Price']
id = fromdatabase['_id']
confirmed = int(confirmedobj)

sendt = int(sendtobj) / 100000000
sendtstr = str(sendt)
left = int(sendtobj) - price

leftbtc = int(left) / -100000000
sendtbtc = int(sendtobj) / 100000000

qrurl = "<IMG SRC=\"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=bitcoin:"

if int(confirmedobj) >= int(price):
        print("Payment Confirmed!")
        post={'_id':id}, {'$set': {'Confirmed':"Yes"}}
        mycollection.update({'_id':id}, {'$set': {'Confirmed':"Yes"}})
elif int(sendtobj) >= int(price):
        print("Payment discovered, waiting for Confirmations.")
elif sendt == 0.0:
        print("<html>You have not paid yet. Please pay " + str(leftbtc) + " BTC to Address " + address + "<br>" + qrurl + address + "?amount=" + str(leftbtc) + "\" WIDTH=150 HEIGHT=150>")
else:
        print("<html>You have paid " + str(sendtbtc) + "BTC. " + str(leftbtc) + "BTC left to pay.<br>" + qrurl + address + "?amount=" + str(leftbtc) + "\" WIDTH=150 HEIGHT=150>")
