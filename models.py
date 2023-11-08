from pydantic import BaseModel
import json
import datetime
from datetime import datetime

class Properties(BaseModel):
    injuries: int
    route_name: str
    last_updated: datetime

class Geometry(BaseModel):
    srid: int
    type: str
    #coordinates: [[]]

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
                        #coordinates=[],
                    ),
                    properties=Properties(
                        injuries=f['properties']['injuries'],
                        route_name=f['properties']['routeName'],
                        last_updated=datetime.strptime(f['properties']['lastUpdated'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                )
            )        
            except:
                print("Failed to parse a feature{}".format(f))
