from pydantic import BaseModel
import datetime
from datetime import datetime

class Properties(BaseModel):
    injuries: int
    route_name: str
    last_updated: datetime
    traveler_information_message: str

class Geometry(BaseModel):
    srid: int
    type: str

class Feature(BaseModel):
    type: str
    geometry: Geometry
    properties: Properties

class FeatureCollection:
    def __init__(self):
        self.features: [] = []

    def parse_from_json(self, json_dict: dict):
        for f in json_dict['features']:
            try:
                self.features.append(
                Feature(
                    type=f['type'], 
                    geometry=Geometry(
                        srid=f['geometry']['srid'],
                        type=f['geometry']['type'],
                    ),
                    properties=Properties(
                        injuries=f['properties']['injuries'],
                        route_name=f['properties']['routeName'],
                        last_updated=datetime.strptime(f['properties']['lastUpdated'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                        traveler_information_message=f['properties']['travelerInformationMessage']
                    )
                )
            )        
            except:
                print("Failed to parse a feature{}".format(f))
