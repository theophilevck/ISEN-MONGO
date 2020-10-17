import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser

client= MongoClient("mongodb+srv://dbUser:admin@cluster0.tpotb.mongodb.net/mongo_Test?retryWrites=true&w=majority")
db=client.get_database('mongo_Test')
bdd=db.test

def getStationNear(longitude,latitude, distance):
    stations=bdd.find(
        {
        "geometry": {
            "$near": {
                "$geometry": {
                    "type": "Point" ,
                    "coordinates": [ longitude , latitude ]
                },
                "$maxDistance": distance,
                "$minDistance": 0
                }
            }
        }
    )

    nearstation = []

    for station in stations:
        nearstation.append(station)
    return nearstation