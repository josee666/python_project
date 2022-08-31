# -*- coding: utf-8 -*-


import json

with open('E:/Web/gratuite/test_decoupe_ieqm_250K/ieqm_sortie_sud/test.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    print(feature['geometry']['type'])
    print(feature['geometry']['coordinates'])