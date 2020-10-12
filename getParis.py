import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
records=db.mongo_record

def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=2971&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_vparis()

for vlille in vlilles:
    new_station={
        'name':vlille['fields']['name'],
        'ville':vlille['fields']['nom_arrondissement_communes'],
        'localisation':vlille['fields']['coordonnees_geo'],
        'tpe':False
    }
    records.insert_one(new_station)