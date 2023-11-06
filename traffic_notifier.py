import requests
from models import FeatureCollection
import sys
import os
import argparse

api_key: str = os.environ['CO_DOT_TRAFFIC_API_KEY']

print('Fetching Incident data for today.')

response = requests.get('https://data.cotrip.org/api/v1/incidents?apiKey={}'.format(api_key))
incident_json = response.json()

if response.status_code != 200:
    print('Failed to get incident data.')
    exit()

parser = argparse.ArgumentParser('Fetches incident data from CO\'s DOT and notifies the owner of the process.')
parser.add_argument('-i', '--injuries', help='Will return and notify any injuries', action='store_true', dest='injuries')
parser.add_argument('-tapi', '--test_api', help='Will fetch from DOT API and print results (kinda ugly)', action='store_true', dest='test_api')

args = parser.parse_args()

if args.test_api == True:
    print(incident_json)
    exit()

featureCollection = FeatureCollection() 
featureCollection.parse_from_json(incident_json)

if args.injuries == True:
    print('Getting Injuries...')

    for f in featureCollection.features:
            if (f.properties.injuries > 0):
                print("{} injuries found on route {}. Last updated on {}".format(f.properties.injuries, f.properties.route_name, f.properties.last_updated))
