import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser
from bson.objectid import ObjectId

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
                    "_id":station.get('_id')
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


def update_Stations_Name(id,newName):
    try:
        db.mongo_record.update(
        {"_id":id},
        {"$set": {'name':newName}})
    except :
        pprint("error update")
        pass


def delete_station_Data(id):
    db.mongo_record.delete_one(
        {"_id":id}
    )
    db.test.delete_one(
        {"station_id":id}
    )

def update_boolean_activate_station():
    {
        db.mongo_record.update_many(
            {},
            {"$set": {"activate":True}},upsert=False, array_filters=None)
    }

    
def query_polygone(x0,x1,x2,x3,state):
    db.mongo_record.update_many(
        {"geometry": {
            "$geoWithin": 
                { 
                    "$polygon": [ [ x0[0] , x0[1] ], [ x1[0] , x1[1]], [ x2[0] , x2[1] ],[x3[0] , x3[1]] ] 
                }
            }
        },
        {"$set": {"activate":state}})

def check_time_between(timest, h1, h2):
    val = time.gmtime(timest)
    if val.tm_wday < 4: 
        if val.tm_hour > h1 and val.tm_hour < h2:
            return True
    
    return False
 

def giv_stations_ratio(hour1, hour2, ratio):
    stations_list = db.mongo_record.aggregate([
        {
            '$lookup': {
                'from': 'test',
                'localField': "_id",
                'foreignField': "station_id",
                'as': "station"
                }, 
            'pipeline': [
                {
                    '$match': {  
                        '$expr': {'$eq': ['$_id', '$station_id']}  
                    }
                },
                {
                "$project":
                {
                    "name":'$name',
                    "size": [{'$sum':['$bike_availbale','$stand_availbale']}],
                    "ratio":{
                        '$cond':{
                            'if': {'$sum': ['$nbvelosdispo', '$nbplacesdispo']} == 0},  
                            'then': 0.0,
                            'else': {'$divide': ['$bike_availbale', {'$sum': ['$bike_availbale', '$stand_availbale']}]}
                        }
                    }     
                },
                {  
                        '$match': {
                            'ratio': {'$lte': ratio}
                        }
                }
            ]
         }
    ])

    return stations_list

        
 

x0=[3.048082,50.650289]
x1=[3.024833,50.621240]
x2=[3.086996,50.617326]
x3=[3.070742,50.651181]
##query_polygone(x0,x1,x2,x3,True)
##update_boolean_activate_station()
##delete_station_Data(toUpdate[0][0].get('_id'))
##update_Stations(toUpdate[0][0].get('_id'),"Seine - Flandre")
##giv_stations_ratio(18, 19, 0.2)



