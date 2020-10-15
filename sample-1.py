import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
bdd=db.mongo_record

def get_stations(ville=["lille", "paris", "lyon", "rennes"], live_data=False):

    stations = []

    if "lille" in ville:
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records = response_json.get("records", [])
        for elem in records:
            vlilles_to_insert =[
                {
                    'name': elem.get('fields', {}).get('nom', '').title(),
                    'geometry': elem.get('geometry'),
                    'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
                    'source': {
                        'dataset': 'Lille',
                        'id_ext': elem.get('fields', {}).get('libelle')
                    },
                'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE'
                }
            ]
            stations.append(vlilles_to_insert)
            bdd.insert_many(vlilles_to_insert)

    if "paris" in ville:
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records =response_json.get("records", [])    
        for elem in records:
            velib_to_insert =[
            {
                'name': elem.get('fields', {}).get('name', '').title(),
                'geometry': elem.get('geometry'),
                'size': elem.get('fields', {}).get('capacity'),
                'source': {
                    'dataset': 'paris',
                    'id_ext': elem.get('fields', {}).get('stationcode')
                    },
                'tpe': True if elem.get('fields',{}).get('is_renting') == 'OUI' else False,
            }
            ]
            stations.append(velib_to_insert)
            bdd.insert_many(velib_to_insert)

    if "lyon" in ville:   
        key="2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
        url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        for elem in response_json:
            velov_to_insert =[
            {
                'name': elem.get('nom', '').title(),
                'geometry': {
                    "type": "Point",
                    "coordinates": [
                        elem.get('position',{}).get('longitude'),
                        elem.get('position',{}).get('latitude')
                    ]
                },
                'size': elem.get('mainStands', {}).get('availabilities',{}).get('capacity'),
                'source': {
                    'dataset': 'lyon',
                    'id_ext': elem.get('number')
                },
                'tpe': elem.get('banking', '') == 'AVEC TPE'
                }
            ]
            stations.append(velov_to_insert)
            bdd.insert_many(velov_to_insert)

    if "rennes" in ville:   
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records =response_json.get("records", []) 
        for elem in records:
            star_to_insert =[
                {
                'name': elem.get('fields', {}).get('nom', '').title(),
                'geometry': elem.get('geometry'),
                'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
                'source': {
                    'dataset': 'rennes',
                    'id_ext': elem.get('fields', {}).get('idstation')
                    },
                'tpe': 'unknown'
                }
            ]     
            stations.append(star_to_insert)
            bdd.insert_many(star_to_insert)

    

    return stations


stations = get_stations()




