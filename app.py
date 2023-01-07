from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, Field, OptionField, MultiSelectField, Lookup, FunctionLookup, SetParamsButton, OutputField, Text, IntegerField, LineBreak
from viktor.result import ViktorResult, SetParamsResult
from viktor.views import GeoJSONResult, GeoJSONView, Color, PlotlyView, PlotlyResult, MapView, MapResult, MapPoint
from viktor.geometry import Arc
from viktor import Color

from geopy import distance
import plotly.graph_objects as go
import random
import numpy as np
import pandas as pd
import haversine as hs
from haversine import Unit

profiles = {}
for i in range(1,11):
    profiles[i] = []

    for x in range(24):
        profiles[i].append(random.random())

meters_df = pd.read_excel("METERS CZL.xlsx")
transformers_df = pd.read_excel("CZL TXF NEW.xlsx")

geojson2 = {'type': 'FeatureCollection', 'features':[]}

geojson = {'type': 'FeatureCollection',
 'features': [{'type': 'Feature',
   'properties': {'identifier': 'Transformer 1', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.19192510083082, 17.512122722040417],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Transformer 2', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.19105782504485, 17.512212622064297],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Transformer 3', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.19183083172318, 17.5112956397373],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Transformer 4', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.19090699447315, 17.511403520250937],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Transformer 5', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.18926671200886, 17.511520390735924],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Transformer 6', 'icon': 'circle-filled'},
   'geometry': {'coordinates': [-88.18904046615131, 17.51239242197728],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'identifier': 'Meter 1',
    'profile': [0.2890361112218778,
     0.09557570400513427,
     0.9636397557087902,
     0.46566866686700026,
     0.9873721353872178,
     0.2663934637562382,
     0.7144764639181457,
     0.23864616603035083,
     0.875735350043814,
     0.3338068831033827,
     0.7478110571667378,
     0.11251011107053521,
     0.2060989703633127,
     0.8437901930925379,
     0.2027315752405251,
     0.662711288761151,
     0.5984714808852649,
     0.1774336108184894,
     0.979645087409996,
     0.5826866237041421,
     0.6472704400493663,
     0.5548038643558296,
     0.3810504896578798,
     0.07309193086291665],
    'description': 'Meter 1'},
   'geometry': {'coordinates': [-88.19237759254527, 17.511844031685342],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.20115321678951537,
     0.4427335586995794,
     0.4105965851172545,
     0.4803429161394812,
     0.9045578552266005,
     0.7894652601841714,
     0.23343147681576237,
     0.7352071133879196,
     0.6357055980008534,
     0.11077116276549315,
     0.5999855671242185,
     0.7555746883995749,
     0.14299618651410795,
     0.09559423024810287,
     0.897173818066956,
     0.20812178146694604,
     0.5339746232439402,
     0.6106650207722182,
     0.8625791213155523,
     0.43757109589344734,
     0.7697791093286815,
     0.1359803012981844,
     0.6207775647499176,
     0.8341352966853092],
    'identifier': 'Meter 2',
    'description': 'Meter 2'},
   'geometry': {'coordinates': [-88.19205707758074, 17.511897971787263],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.9531121874442035,
     0.8111567303696734,
     0.7561422864899194,
     0.1500226090316058,
     0.2440525154851858,
     0.3041042555560963,
     0.4657318245611679,
     0.12372267901904521,
     0.3294801531249564,
     0.09989510578364835,
     0.9696394324243595,
     0.37384866724813104,
     0.7423792162937353,
     0.015846398431687336,
     0.8985342222201097,
     0.5391364980453257,
     0.7913006901068094,
     0.6291575325850982,
     0.0624354913960391,
     0.6792251177112585,
     0.36439114790188687,
     0.6891144596190246,
     0.8579704688900793,
     0.4314808019626756],
    'identifier': 'Meter 3',
    'description': 'Meter 3'},
   'geometry': {'coordinates': [-88.19167057424123, 17.511924941832234],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.753821452913151,
     0.04112542581958478,
     0.7554580982654577,
     0.39246876082700677,
     0.3862801767160142,
     0.9697850369338826,
     0.32656800418601306,
     0.7903983310807374,
     0.5872722520260593,
     0.8699855496914509,
     0.5541913326779195,
     0.9887107528738674,
     0.728075048038767,
     0.6445008141741263,
     0.32221523906418736,
     0.7745542394268883,
     0.7802455114162106,
     0.7239203251578743,
     0.8078918699277414,
     0.2350109643303787,
     0.8601021023284829,
     0.9041692117529583,
     0.9436132887708651,
     0.3799794556007273],
    'description': 'Meter 4',
    'identifier': 'Meter 4'},
   'geometry': {'coordinates': [-88.19222676197356, 17.512347472016046],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.8402909077215388,
     0.8843353018251345,
     0.5197463767678795,
     0.39332509978410146,
     0.6001391357639116,
     0.420363503522025,
     0.5763363938250133,
     0.8508394688983085,
     0.22980094419296904,
     0.028410557879762544,
     0.993074398080676,
     0.5823539349657163,
     0.9940908143303803,
     0.2991448391066346,
     0.8338528882382087,
     0.563734328358289,
     0.6990388968580513,
     0.9048505797016428,
     0.4683883458812198,
     0.46063772736787423,
     0.42757924639972444,
     0.573198432248812,
     0.86660558818435,
     0.049735760648841554],
    'identifier': 'Meter 5',
    'description': 'Meter 5'},
   'geometry': {'coordinates': [-88.19189682009812, 17.512545251763967],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.7863605840296105,
     0.836038041954217,
     0.9756382052435152,
     0.7880126942842254,
     0.35549025845466775,
     0.31951725256729846,
     0.38203937460226234,
     0.9758823711328014,
     0.37264396341962447,
     0.7476023307201437,
     0.5450539639215993,
     0.8965135240843048,
     0.33486291980543714,
     0.09079528703081607,
     0.4281620372456426,
     0.9340072427133483,
     0.9203888116913199,
     0.9296119325962336,
     0.48871908941118014,
     0.3208507750229428,
     0.6769102544478971,
     0.2077468243876779,
     0.6132996909035616,
     0.5856651708205417],
    'identifier': 'Meter 6',
    'description': 'Meter 6'},
   'geometry': {'coordinates': [-88.19178369717002, 17.51238343198628],
    'type': 'Point'}},
  {'type': 'Feature',
   'properties': {'profile': [0.13025738514662277,
     0.9106060504534297,
     0.1551278744547545,
     0.07453617408627089,
     0.7353977196100289,
     0.21833061707833012,
     0.9170735895296295,
     0.6451413670547864,
     0.01458260498690378,
     0.08562890827216951,
     0.6864032067072862,
     0.5142782309970682,
     0.5286926540631788,
     0.6170366763418499,
     0.7699508108673858,
     0.14733092028668793,
     0.17103317479963553,
     0.04362090885935488,
     0.2844605600659078,
     0.4185430956795678,
     0.4473393941532926,
     0.942872571383357,
     0.8972231175858145,
     0.007984414284945007],
    'identifier': 'Meter 7'},
   'geometry': {'coordinates': [-88.19149146293749, 17.5124104019591],
    'type': 'Point'}}]}

meters = ['Meter 1', 'Meter 2', 'Meter 3', 'Meter 4', 'Meter 5', 'Meter 6', 'Meter 7']
meters2 = list(meters_df['OBJECTID'].unique())

for i in geojson['features']:
  if i['properties']['identifier'] == "Transformer 1":
    i['properties']['connected_meters'] = meters          

def get_distances_meters(params, **kwargs):
  output_text = """OVERVIEW DISTANCES"""
  for i in geojson['features']:
    if i['properties']['identifier'] == "Transformer {}".format(params.option):
      transformer_location = tuple(i['geometry']['coordinates'])
      connected_meters = []
      
      for m in meters:
        for i in geojson['features']:
          if i['properties']['identifier'] == m:
            meter_location = tuple(i['geometry']['coordinates'])
            meter_distance = round(distance.distance(transformer_location, meter_location).kilometers*1000)        
            output_text = output_text + "\n Distance between Transformer {} and {}: {} meters".format(params.option, m, meter_distance)
  return output_text

class Parametrization(ViktorParametrization):
    option = OptionField('Select a transformer', options=['1','2','3','4','5','6'], default='1')
    option2 = IntegerField('Select transformer')
    range_distance = IntegerField('Distance to transformer [m]')
    set_params_btn = SetParamsButton("Connect meters", "set_param_a", longpoll=True)
    connected_meters = MultiSelectField('Connected meters', options = meters, default = [])
    
    pass
   
class Controller(ViktorController):
  
    label = 'My Entity Type'
    parametrization = Parametrization
    
    def set_param_a(self, params, **kwargs):
      for i in geojson['features']:
        if i['properties']['identifier'] == "Transformer {}".format(params.option):
          transformer_location = tuple(i['geometry']['coordinates'])

      connected_meters = []

      for m in meters:
        for i in geojson['features']:
          if i['properties']['identifier'] == m:
            meter_location = tuple(i['geometry']['coordinates'])
            meter_distance = round(distance.distance(transformer_location, meter_location).kilometers*1000)
            i['properties']['description'] = "Distance to selected transformer: " + str(int(round(meter_distance))) + " meters"
            
            if meter_distance < params.range_distance:
              connected_meters.append(m)
              
      dataParam = {"connected_meters" : connected_meters}
      #print(geojson)
      return SetParamsResult(dataParam)
    
    @GeoJSONView('Map', duration_guess=1)
    def get_geojson_view(self, params, **kwargs):
        #print(geojson)
        for i in geojson['features']:
          if i['properties']['identifier'] == "Transformer {}".format(params.option):
            i['properties']['connected_meters'] = params.connected_meters
            text = """**Connected Meters**  \n"""
            #print(params.connected_meters)
            alp_meters = sorted(params.connected_meters)
            #print(alp_meters)
            for a in alp_meters:
              new_text = """  \n """ + "- " + a
              text = text + new_text
            
            print(text)
            i['properties']['description'] = text
            i['properties']['marker-color'] = "#FFA500"
            
            for m in i['properties']['connected_meters']:
              for x in geojson['features']:
                if x['properties']['identifier'] == m:
                  x['properties']['marker-color'] = "#FFA500"

        
        return GeoJSONResult(geojson)
                  
    @GeoJSONView('New Map', duration_guess=30)
    def get_meter_map(self, params, **kwargs):     
      
      for i,x in transformers_df.iterrows():
        lon = x['X_field']
        lat = x['Y_Field']
        id = x['OBJECTID']
        
        new_transformer = { 'type': 'Feature',
                            'properties': {
                              'identifier': str(id),
                              'description': "TRANSFORMER " + str(id),
                              'icon': 'square-filled',
                              'marker-color': '#555555',
                              'marker-size' : 'small'
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
        
        new_meter = { 'type': 'Feature',
                      'properties': {
                        'identifier': str(id),
                        'description': "METER " + str(id), 
                        'icon': 'circle-filled',
                        'marker-color': '#FFA500',
                        'marker-size' : 'small'
                        },
                      'geometry': {
                        'coordinates': [lon, lat],
                        'type': 'Point'}
                      }
        
        geojson2['features'].append(new_meter)
      
      for i in geojson2['features']:
        print("TRY")
        if i['properties']['identifier'] == str(params.option2):
          transformer_location = tuple(i['geometry']['coordinates'])
          print(transformer_location)
        else:
          print('JAMMER JOH')

      connected_meters = []

      for m in meters2:
        for i in geojson2['features']:
          if i['properties']['identifier'] == str(m):
            meter_location = tuple(i['geometry']['coordinates'])
            meter_distance = round(hs.haversine(transformer_location, meter_location,unit=Unit.METERS))
            
            if meter_distance < params.range_distance:
              connected_meters.append(m)
              i['properties']['marker-color'] = '#F4190B'
      
      #print(geojson2)
      return GeoJSONResult(geojson2)
                    
    
    @PlotlyView("Transformer Loading", duration_guess=1)
    def get_plotly_view(self, params, **kwargs):
              
        for i in geojson['features']:
          
          i['properties']['profile'] = [0] * 24
          
          if i['properties']['identifier'] == "Transformer {}".format(params.option):    
            i['properties']['connected_meters'] = params.connected_meters
            i['properties']['description'] = str(params.connected_meters)
                                           
            for m in i['properties']['connected_meters']:
              for x in geojson['features']:
                if x['properties']['identifier'] == m:
                  i['properties']['profile'] = np.array(i['properties']['profile']) + np.array(x['properties']['profile'])
                   
            profile = list(i['properties']['profile'])
            
        fig = go.Figure(
            data=[go.Bar(x=list(range(24)), y=profile)],
            layout=go.Layout(title=go.layout.Title(text="Transformer {}".format(params.option)))
        )
        fig.add_hline(2, line_color = "orange", line_dash="dash", line_width=2)
        fig.add_hrect(1.7, 2.3, line_width=0, fillcolor = "orange", opacity=0.2)
        
        return PlotlyResult(fig.to_json())