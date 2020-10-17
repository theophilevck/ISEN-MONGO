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
    bdd.find({"name": "/.*"+nom+"*./"})



