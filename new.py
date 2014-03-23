#!/bin/python
from urllib import request
from pymongo import Connection
import argparse
import json
import pymongo
req = request.urlopen('https://blockchain.info/no/api/receive?method=create&address=19J9J4QHDun5YgUTfEU1qb3fSHTbCwcjGj')
encoding = req.headers.get_content_charset()
obj = json.loads(req.read().decode(encoding))
print(obj['input_address'])

parser = argparse.ArgumentParser()
parser.add_argument("--price")
parser.add_argument("--name")
parser.add_argument("--description")

args = parser.parse_args()

price = float(args.price) * 100000000

connection=Connection()
database=connection['bitcoin']
mycollection=database.entries
post={"Address":(obj['input_address']), "Price":price, "Name":args.name, "Description":args.description, "Confirmed":"No"}
mycollection.insert(post)






