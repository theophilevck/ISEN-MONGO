import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
records=db.mongo_record


def get_vlyon():
    key="2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
    url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=2f3f00af9ce4e0959c3611b330a7be5f1af2b436"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json

vlilles = get_vlyon()

for vlille in vlilles:
    new_station={
        'name':vlille['name'],
        'ville':vlille['contractName'],
        'localisation':[vlille['position']],
        'tpe':vlille['banking']
    }
    records.insert_one(new_station)