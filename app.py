from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Field, OptionField, MultiSelectField, Lookup, FunctionLookup, SetParamsButton, OutputField, Text, IntegerField, LineBreak, ActionButton
from viktor.result import ViktorResult, SetParamsResult
from viktor.views import GeoJSONResult, GeoJSONView, Color, PlotlyView, PlotlyResult, MapView, MapResult, MapPoint
from viktor.geometry import Arc
from viktor import Color

from geopy.distance import distance, Distance
import plotly.graph_objects as go
import random
import numpy as np
import pandas as pd
import haversine as hs
from haversine import Unit
import json

meters_df = pd.read_excel("METERS CZL.xlsx")
transformers_df = pd.read_excel("CZL TXF NEW.xlsx")

geojson2 = {'type': 'FeatureCollection', 'features':[]}

for i,x in transformers_df.iterrows():
    lon = x['X_field']
    lat = x['Y_Field']
    id = x['OBJECTID']
    feeder_id = x['Feeder ID']
    
    new_transformer = { 'type': 'Feature',
                        'properties': {
                          'identifier': str(id),
                          'description': "TRANSFORMER " + str(id),
                          'feeder-id' : feeder_id,
                          'icon': 'square-filled',
                          'marker-color': '#555555',
                          'marker-size' : 'small',
                          'connected-meters' : [],
                          },
                        'geometry': {
                          'coordinates': [lon, lat],
                          'type': 'Point'
                          }
                        }
    
    geojson2['features'].append(new_transformer)
      
for i,x in meters_df.iterrows():
  
    lon = x['longitude']
    lat = x['latitude']
    id = x['OBJECTID']
    feeder_id = x['Feeder ID']
    
    new_meter = { 'type': 'Feature',
                  'properties': {
                    'identifier': str(id),
                    'description': "METER " + str(id),
                    'feeder-id' : feeder_id, 
                    'icon': 'circle-filled',
                    'marker-color': '#FFA500',
                    'marker-size' : 'small'
                    },
                  'geometry': {
                    'coordinates': [lon, lat],
                    'type': 'Point'}
                  }
    
    geojson2['features'].append(new_meter)

with open('geojson.json', 'w') as f:
    json.dump(geojson2, f)
        
meters2 = list(meters_df['OBJECTID'].unique())
meters2 = [int(i) for i in meters2]

def check_point(point, point_north, point_east, point_south, point_west):
  point_lon = point[1]
  point_lat = point[0]
  
  if point_lon > point_west[1] and point_lon < point_east[1] and point_lat > point_south[0] and point_lat < point_north[0]:
    return True
  else:
    return False
  

class Parametrization(ViktorParametrization):
    option2 = IntegerField('Select transformer')
    range_distance = IntegerField('Distance to transformer [m]')
    set_params_btn = SetParamsButton("Connect in range", "set_param_b", longpoll=True)
    connected_meters = MultiSelectField('Connected meters', options = meters2, default = [])
    pass
   
class Controller(ViktorController):
  
    label = 'My Entity Type'
    parametrization = Parametrization
    
    def set_param_b(self, params, **kwargs):
            
      calculations = 0
      connected_meters_list = []
      
      if params.option2 is not None:
              
        for i in geojson2['features']:
          
          if i['properties']['identifier'] == str(params.option2):
            transformer_location = tuple(list(reversed(i['geometry']['coordinates'])))
            print(transformer_location)
            
            point_north   = distance(kilometers=params.range_distance/1000).destination(transformer_location, bearing=0)
            point_south   = distance(kilometers=params.range_distance/1000).destination(transformer_location, bearing=180)
            point_east    = distance(kilometers=params.range_distance/1000).destination(transformer_location, bearing=90)
            point_west    = distance(kilometers=params.range_distance/1000).destination(transformer_location, bearing=270)
            
            print(point_north[0], point_south[0], point_east[1], point_west[1])
            feeder_id_tr = i['properties']['feeder-id']

            for m in meters2:
              
              for y in geojson2['features']:
                
                if y['properties']['feeder-id'] == feeder_id_tr and y['properties']['identifier'] == str(m) :
                  meter_location = tuple(list(reversed(y['geometry']['coordinates'])))
                  
                  if check_point(meter_location, point_north, point_east, point_south, point_west):
                    calculations = calculations + 1
                    meter_distance = round(hs.haversine(transformer_location, meter_location,unit=Unit.METERS))
                    
                    if meter_distance < params.range_distance:
                      connected_meters_list.append(m)
      
            i['properties']['connected-meters'] = connected_meters_list
      
      with open('geojson.json', 'w') as f:
          json.dump(geojson2, f)
          f.close()
      
      dataParam = {"connected_meters" : connected_meters_list}
      return SetParamsResult(dataParam)
    
                      
    @GeoJSONView('New Map', duration_guess=30)
    def get_meter_map(self, params, **kwargs):
      
      with open('geojson.json') as f:
        geojson2 = json.load(f)
        f.close()        
          
      if params.option2 is not None:
        
        for y in geojson2['features']:
          if y['properties']['identifier'] == str(params.option2):
            print(y)
            meters_to_check = y['properties']['connected-meters']
            for m in meters_to_check:
              for z in geojson2['features']:
                if z['properties']['identifier'] == str(m):
                  z['properties']['marker-color'] = '#F4190B'
        
      with open('geojson.json', 'w') as f:
        json.dump(geojson2, f)
        f.close()
      
      return GeoJSONResult(geojson2)
                    
    
    # @PlotlyView("Transformer Loading", duration_guess=1)
    # def get_plotly_view(self, params, **kwargs):
              
    #     for i in geojson['features']:
          
    #       i['properties']['profile'] = [0] * 24
          
    #       if i['properties']['identifier'] == "Transformer {}".format(params.option):    
    #         i['properties']['connected_meters'] = params.connected_meters
    #         i['properties']['description'] = str(params.connected_meters)
                                           
    #         for m in i['properties']['connected_meters']:
    #           for x in geojson['features']:
    #             if x['properties']['identifier'] == m:
    #               i['properties']['profile'] = np.array(i['properties']['profile']) + np.array(x['properties']['profile'])
                   
    #         profile = list(i['properties']['profile'])
            
    #     fig = go.Figure(
    #         data=[go.Bar(x=list(range(24)), y=profile)],
    #         layout=go.Layout(title=go.layout.Title(text="Transformer {}".format(params.option)))
    #     )
    #     fig.add_hline(2, line_color = "orange", line_dash="dash", line_width=2)
    #     fig.add_hrect(1.7, 2.3, line_width=0, fillcolor = "orange", opacity=0.2)
        
    #     return PlotlyResult(fig.to_json())