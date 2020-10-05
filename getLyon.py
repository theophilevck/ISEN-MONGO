import requests
import json
from pprint import pprint

def get_vlille():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&facet=last_upd_1"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_vlille()

for vlille in vlilles:
    pprint(vlille)