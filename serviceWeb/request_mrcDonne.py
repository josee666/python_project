
import requests

#adresse du service
URL = "https://geoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?"

# param
PARAMS = {'LAYERS' : 'sh_dom_bio',
          'SERVICE':'WMS',
          'REQUEST':'GetFeatureInfo',
          'VERSION':'1.1.1',
          'SRS':'EPSG:3857',
          'BBOX':'-8062540.000868,6140794.422066,-8059506.406308,6144587.609594',
          'WIDTH':'635',
          'HEIGHT':'794',
          'QUERY_LAYERS':'sh_dom_bio',
          'X':'384',
          'Y':'234'}

# lance requete http
r = requests.get(url=URL, params=PARAMS)


print('pis')