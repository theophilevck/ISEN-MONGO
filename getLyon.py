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

vlilles_to_insert =[
 {
        'name': elem.get('nom', '').title(),
        'geometry': {
            "type": "Point",
            "coordinates": [
                elem.get('position',{}).get('longitude'),
                elem.get('position',{}).get('latitude')
            ]
        },
        'size': elem.get('mainStands', {}).get('availabilities',{}).get('bikes') + elem.get('mainStands', {}).get('availabilities',{}).get('stands'),
        'source': {
            'dataset': 'lyon',
            'id_ext': elem.get('number')
        },
        'tpe': elem.get('banking', '') == 'AVEC TPE'
    }
    for elem in vlilles
]

for vlille in vlilles_to_insert:
    records.insert_one(vlille)
