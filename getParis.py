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


vlilles_to_insert =[
 {
        'name': elem.get('fields', {}).get('name', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('numbikesavailable') + elem.get('fields', {}).get('numdocksavailable'),
        'source': {
            'dataset': 'paris',
            'id_ext': elem.get('fields', {}).get('stationcode')
        },
        'tpe': True if elem.get('fields',{}).get('is_renting') == 'OUI' else False,
    }
    for elem in vlilles
]

for vlille in vlilles_to_insert:
    records.insert_one(vlille)
