import requests
from models import FeatureCollection, IncidentType
import os
import argparse
from twilio_client import TwilioClient

api_key: str = os.environ['CO_DOT_TRAFFIC_API_KEY']

def get_incident_notification(featureCollection: FeatureCollection):
    print('Getting Injuries...')
    
    notification_message = ""
    
    for f in featureCollection.features:
        notification_message += "{} injuries found on route {}. Last updated on {}\n\n".format(f.properties.injuries, f.properties.route_name, f.properties.last_updated)

    return notification_message

def get_traveler_info_notification(featureCollection: FeatureCollection):
    print('Getting Traveler info...')
    
    notification_message = ""

    for f in featureCollection.features:
        notification_message += "{} traveler info on route {}. Last updated on {}\n\n".format(f.properties.traveler_information_message, f.properties.route_name, f.properties.last_updated)

    return notification_message

type_to_op = {
    IncidentType.INJURIES: get_traveler_info_notification,
    IncidentType.TRAVELER_INFO: get_traveler_info_notification
}

def run_logic(type: IncidentType, from_number: str):
    print('Fetching Incident data for today.')

    response = requests.get('https://data.cotrip.org/api/v1/incidents?apiKey={}'.format(api_key))
    incident_json = response.json()

    featureCollection = FeatureCollection() 
    featureCollection.parse_from_json(incident_json)

    if response.status_code != 200:
        print('Failed to get incident data.')
        exit()

    func = type_to_op[type]

    if func is None:
        print("No Op found for type {}".format(type))

    notification_message = func(featureCollection)

    twilio_client: TwilioClient = TwilioClient()

    if notification_message != "":
        print("Sending message to {}".format(from_number))
        twilio_client.send_message(from_number, notification_message[:1000])

parser = argparse.ArgumentParser('Fetches incident data from CO\'s DOT and notifies the owner of the process.')
parser.add_argument('-i', '--injuries', help='Will return and notify any injuries', action='store_true', dest='injuries')
parser.add_argument('-c', '--crashes', help='Will return crashes', action='store_true', dest='crashes')
parser.add_argument('-t', '--traveler_info', help='Get traveler info for incidents', action='store_true', dest='traveler_info')
parser.add_argument('-tapi', '--test_api', help='Will fetch from DOT API and print results (kinda ugly)', action='store_true', dest='test_api')
parser.add_argument('phone_number', metavar='P', type=str, nargs='+', help='Phone number to send notification to')

args = parser.parse_args()

type: IncidentType

if args.test_api:
    type = IncidentType.TEST_API
elif args.injuries:
    type = IncidentType.INJURIES
elif args.traveler_info:
    type = IncidentType.TRAVELER_INFO


run_logic(type, args.phone_number)