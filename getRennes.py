import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
records=db.mongo_record


def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_vrennes()

for vlille in vlilles:
    new_station={
        'name':vlille['fields']['nom'],
        'ville':'renne',
        'localisation':vlille['fields']['coordonnees'],
        'tpe':False
    }
    records.insert_one(new_station)