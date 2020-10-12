import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient


client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
records=db.mongo_record

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])


vlilles = get_vlille()

for vlille in vlilles:
    new_station={
        'name':vlille['fields']['nom'],
        'ville':vlille['fields']['commune'],
        'localisation':vlille['fields']['localisation'],
        'tpe':vlille['fields']['type']
    }
    records.insert_one(new_station)
    
    