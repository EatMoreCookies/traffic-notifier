import requests
from models import FeatureCollection
import sys
import os
import argparse
from twilio_client import TwilioClient

api_key: str = os.environ['CO_DOT_TRAFFIC_API_KEY']

print('Fetching Incident data for today.')

response = requests.get('https://data.cotrip.org/api/v1/incidents?apiKey={}'.format(api_key))
incident_json = response.json()

if response.status_code != 200:
    print('Failed to get incident data.')
    exit()

parser = argparse.ArgumentParser('Fetches incident data from CO\'s DOT and notifies the owner of the process.')
parser.add_argument('-i', '--injuries', help='Will return and notify any injuries', action='store_true', dest='injuries')
parser.add_argument('-c', '--crashes', help='Will return crashes', action='store_true', dest='crashes')
parser.add_argument('-t', '--traveler_info', help='Get traveler info for incidents', action='store_true', dest='traveler_info')
parser.add_argument('-tapi', '--test_api', help='Will fetch from DOT API and print results (kinda ugly)', action='store_true', dest='test_api')
parser.add_argument('phone_number', metavar='P', type=str, nargs='+', help='Phone number to send notification to')

args = parser.parse_args()

if args.test_api == True:
    print(incident_json)
    exit()

featureCollection = FeatureCollection() 
featureCollection.parse_from_json(incident_json)

notification_message: str = ""

twilio_client: TwilioClient = TwilioClient()

if args.injuries:
    print('Getting Injuries...')

    for f in featureCollection.features:
        notification_message += "{} injuries found on route {}. Last updated on {}\n\n".format(f.properties.injuries, f.properties.route_name, f.properties.last_updated)

elif args.traveler_info:
    print('Getting Traveler info...')
    
    for f in featureCollection.features:
        notification_message += "{} traveler info on route {}. Last updated on {}\n\n".format(f.properties.traveler_information_message, f.properties.route_name, f.properties.last_updated)


if notification_message != "":
    print("Sending message to {}".format(args.phone_number))
    twilio_client.send_message(args.phone_number, notification_message)