import requests
import json
from pymongo import MongoClient 
from pprint import pprint

def get_wifiparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=sites-disposant-du-service-paris-wi-fi&q=&rows=100&facet=cp&facet=idpw&facet=etat2"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

client = MongoClient()
client = MongoClient('mongodb+srv://rtatin:<bgbogoss>@cluster0.ovsvo.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
db=client["worker"]
mycol = db["wifi"]
wifis = get_wifiparis()
mongo_id = mycol.insert(wifis)

for wifi in wifis:
    mycol.update_one({'_id':mongo_id}, {"$set": wifi}, upsert=False)
    pprint(wifi)