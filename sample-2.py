import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
bdd=db.test
station = []

def update_stations(ville=["lille", "paris", "lyon", "rennes"], live_data=False):
    stations = []

    if "lille" in ville:
        pprint('lille')
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records = response_json.get("records", [])
        for elem in records:
            try:
                datas = [
                    {
                    "bike_availbale": elem.get('fields', {}).get('nbvelosdispo'),
                    "stand_availbale": elem.get('fields', {}).get('nbplacesdispo'),
                    "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),
                    "station_id": get_station_id(elem.get('fields', {}).get('libelle'))
                    }
                    ]
                stations.append(datas)
            except:
                pass
        

    if "paris" in ville:
        pprint('paris')
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records =response_json.get("records", [])   
        for elem in records:
            try:
                datas = [
                    {
                    "bike_availbale": elem.get('fields', {}).get('numbikesavailable'),
                    "stand_availbale": elem.get('fields', {}).get('numdocksavailable'),
                    "date": dateutil.parser.parse(elem.get('fields', {}).get('duedate')),
                    "station_id": get_station_id(elem.get('fields', {}).get('stationcode'))
                    }
                    ]
                stations.append(datas)
            except:
                pass

    if "lyon" in ville:
        pprint('lyon')
        url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        for elem in response_json:
            try:
                datas = [
                    {
                    "bike_availbale": elem.get('mainStands', {}).get('availabilities',{}).get('bikes'),
                    "stand_availbale": elem.get('mainStands', {}).get('availabilities',{}).get('stands'),
                    "date": dateutil.parser.parse(elem.get('lastUpdate')),
                    "station_id": get_station_id(elem.get('number'))
                    }
                    ]
                stations.append(datas)
            except:
                pass
        

    if "rennes" in ville:
        pprint('rennes')
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        response_json = json.loads(response.text.encode('utf8'))
        records =response_json.get("records", []) 
        for elem in records:
            try:
                datas = [
                    {
                    "bike_availbale": elem.get('fields', {}).get('nombrevelosdisponibles'),
                    "stand_availbale": elem.get('fields', {}).get('nombreemplacementsdisponibles'),
                    "date": dateutil.parser.parse(elem.get('fields', {}).get('lastupdate')),
                    "station_id": get_station_id(elem.get('fields', {}).get('idstation'))
                    }
                    ]
                stations.append(datas)
            except:
                pass
    return stations

def get_station_id(id_ext):
    
    try:
        tps = db.mongo_record.find_one({ 'source.id_ext': id_ext }, { '_id': 1 })
        return tps['_id']
    except :
        return -1
        

while True:
    print('update')
    station=update_stations()
    for vlille in station:
        bdd.insert_many(vlille)
        
        
    time.sleep(1)