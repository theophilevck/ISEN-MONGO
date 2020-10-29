import requests
import json
from pprint import pprint
from pymongo import MongoClient,GEOSPHERE
import time
import dateutil.parser

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
bdd=db.test

def getStationNear(longitude,latitude, distance):
    db.mongo_record.create_index([("geometry", "2dsphere")])
    stations=db.mongo_record.find(
        {
        "geometry": {
            "$near": {
                "$geometry": {
                    "type": "Point" ,
                    "coordinates": [ longitude , latitude ]
                },
                "$maxDistance": distance
                }
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
                    "stand":get_standbyid(station.get('_id'))
                    }
                ]
        nearstation.append(datas)
    return nearstation

def get_bikebyid(id):
    
    tps = db.test.find_one({ "station_id": id }, { 'bike_availbale': 1 })
    return tps['bike_availbale']
    

def get_standbyid(id):
    try:
        tps = db.test.find_one({ "station_id": id }, { 'stand_availbale': 1 })
        return tps['stand_availbale']
    except :
        return -1

stations=getStationNear(3.130853, 50.63608, 1000)
for station in stations:
    pprint(station)



        
