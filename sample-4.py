import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
bdd=db.mongo_record

def getByname(nom):
    db.mongo_record.create_index([("name", "text")])
    stations=db.mongo_record.find(
        {
            "$text":{
                "$search": nom
                }
            }
        )  
        
    nearstation = []
    for station in stations:
        datas = [
                    {
                    "name":station.get('name'),
                    "coordinates":station.get('geometry',{}).get('coordinates'),
                    "bike":get_bikebyid(station.get('_id')),
                    "stand":get_standbyid(station.get('_id')),
                    "_id":station.get('station_id')
                    }
                ]
        nearstation.append(datas)
    return nearstation

def get_bikebyid(id):
    try:
        tps = db.test.find_one({ "station_id": id }, { 'bike_availbale': 1 })
        return tps['bike_availbale']
    except :
        return -1
    

def get_standbyid(id):
    try:
        tps = db.test.find_one({ "station_id": id }, { 'stand_availbale': 1 })
        return tps['stand_availbale']
    except :
        return -1

pprint(getByname("Flandre"))