import requests
from models import FeatureCollection
import sys
import os

api_key: str = os.environ['CO_DOT_TRAFFIC_API_KEY']

response = requests.get('https://data.cotrip.org/api/v1/incidents?apiKey={}'.format(api_key))

if response.status_code != 200:
    print('Failed to get incident data.')
    exit()

incident_json = response.json()

featureCollection = FeatureCollection()
featureCollection.parse_from_json(incident_json)

if sys.argv[1] == '-i':
    for f in featureCollection.features:
        if (f.properties.injuries > 0):
            print("{} injuries found on route {}".format(f.properties.injuries, f.properties.route_name))
        



