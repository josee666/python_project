
import requests
import json
import xmltodict

def callWMSInfo():
    # Exemple 1 avec notre service IGO, interroge couche des sous-domaine bioclimatique
    #adresse du service
    URL = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?"

    # param
    PARAMS = {'LAYERS' : 'sh_dom_bio',
              'SERVICE':'WMS',
              'REQUEST':'GetFeatureInfo',
              'VERSION':'1.1.1',
              'SRS':'EPSG:3857',
              'BBOX': '-8062540.000868,6140794.422066,-8059506.406308,6144587.609594',
              'WIDTH':'635',
              'HEIGHT':'794',
              'QUERY_LAYERS':'sh_dom_bio',
              'X':'384',
              'Y':'234'
              }
    callWms = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=fadfe3f2&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&TRANSPARENT=true&QUERY_LAYERS=sh_reg_eco&LAYERS=sh_reg_eco&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&FEATURE_COUNT=5&I=50&J=50&CRS=EPSG%3A3857&STYLES=&WIDTH=101&HEIGHT=101&BBOX=-7862651.506788713%2C6000334.441088111%2C-7854931.366931911%2C6008054.580944913"

    # 'INFO_FORMAT': 'application/geojson'

    return requests.get(URL, PARAMS)

# lance requete http
def callWFSFeature():
    # callWfs_gml = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?service=WFS&request=GetFeature&version=1.1.0&typename=nord_photo_oblique&srsname=EPSG:3857&maxFeatures=1000&propertyName=LATITUDE,LONGITUDE,NOM_PHOTO,geometry&bbox=-7937865.542621327,5960166.782724251,-7833376.124955491,6045546.943318793,EPSG:3857"
    callWFS_geojson = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?service=WFS&request=GetFeature&info_format=geojson&version=1.1.0&typename=nord_photo_oblique&srsname=EPSG:3857&maxFeatures=1000&propertyName=LATITUDE,LONGITUDE,NOM_PHOTO,geometry&bbox=-7937865.542621327,5960166.782724251,-7833376.124955491,6045546.943318793,EPSG:3857"
    callWFS_geojson = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?service=WFS&request=GetFeature&info_format=geojson&version=1.1.0&typename=nord_photo_oblique&srsname=EPSG:3857&maxFeatures=1000&propertyName=LATITUDE,LONGITUDE,NOM_PHOTO,geometry&bbox=-7937865.542621327,5960166.782724251,-7833376.124955491,6045546.943318793,EPSG:3857"


    callMtqWfs = "https://ws.mapserver.transports.gouv.qc.ca/swtq?service=WFS&request=GetFeature&version=1.1.0&typename=aeroport_piste&outputFormat=geojson"

    # return requests.get(callWfs_gml)
    # return requests.get(callWFS_geojson)
    return requests.get(callMtqWfs)
# my_json = reponse.content.decode('utf8').replace("'", '"')
# print(my_json)
#
# data = json.loads(my_json)
# s = json.dumps(data, indent=4, sort_keys=True)
#
# print(reponse)
# print(json.dumps(reponse.content))


def callWmsGetFeatureFilter():

    callMtqRadar = r"https://ws.mapserver.transports.gouv.qc.ca/swtq?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&TRANSPARENT=true&QUERY_LAYERS=radars_photos&LAYERS=radars_photos&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&FILTER=(%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)&INFO_FORMAT=application%2Fvnd.ogc.gml&FEATURE_COUNT=5&I=50&J=50&CRS=EPSG%3A3857&STYLES=&WIDTH=101&HEIGHT=101&BBOX=-7997104.281409148%2C5677667.427515962%2C-7750059.805991458%2C5924711.9029336525"
    # callMtqRadar = r"?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&TRANSPARENT=true&QUERY_LAYERS=radars_photos&LAYERS=radars_photos&DPI=96&
    # MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&FILTER=
    # (%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)
    # &INFO_FORMAT=application%2Fvnd.ogc.gml&FEATURE_COUNT=5&I=50&J=50&CRS=EPSG%3A3857&STYLES=&
    # WIDTH=101&HEIGHT=101&BBOX=-7997104.281409148%2C5677667.427515962%2C-7750059.805991458%2C5924711.9029336525"

    urlMtq = 'https://ws.mapserver.transports.gouv.qc.ca/swtq'

    PARAMSMtq = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetFeatureInfo',
        # 'FORMAT': 'image/png',
        'QUERY_LAYERS': 'radars_photos',
        'LAYERS': 'radars_photos',
        # 'DPI': '96',
        # 'MAP_RESOLUTION': '96',
        # 'FORMAT_OPTIONS': 'dpi:96',
        'FILTER': '(<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>typeAppareil</PropertyName><Literal>Radar photo fixe</Literal></PropertyIsEqualTo></Filter>)',
        # 'FILTER': '(%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)',
        # 'INFO_FORMAT': 'text/plain',
        # 'INFO_FORMAT': 'application/json', ## non pas dispo pour GetFeatureInfo
        'INFO_FORMAT': 'application/vnd.ogc.gml',
        'FEATURE_COUNT': '5',
        'I': '50',
        'J': '50',
        'CRS': 'EPSG:3857',
        # 'STYLES': '',
        'WIDTH': '101',
        'HEIGHT': '101',
        'BBOX': '-7997104.281409148,5677667.427515962,-7750059.805991458,5924711.9029336525'
    }


    urlDif = 'https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?'

    PARAMSDif = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetFeatureInfo',
        # 'FORMAT': 'image/png',
        'QUERY_LAYERS': 'nord_photo_oblique',
        'LAYERS': 'nord_photo_oblique',
        # 'DPI': '96',
        # 'MAP_RESOLUTION': '96',
        # 'FORMAT_OPTIONS': 'dpi:96',
        'FILTER': '(<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>NOM_PHOTO</PropertyName><Literal>_DDD2941.jpg</Literal></PropertyIsEqualTo></Filter>)',
        # 'FILTER': '(%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)',
        # 'INFO_FORMAT': 'text/plain',
        # 'INFO_FORMAT': 'application/json', ## non pas dispo pour GetFeatureInfo
        # 'INFO_FORMAT': 'application/vnd.ogc.gml',
        'FEATURE_COUNT': '5',
        'I': '50',
        'J': '50',
        'CRS': 'EPSG:3857',
        # 'STYLES': '',
        'WIDTH': '101',
        'HEIGHT': '101',
        'BBOX': '-7997104.281409148,5677667.427515962,-7750059.805991458,5924711.9029336525'
    }

    # return requests.get(callMtqRadar)
    # return requests.get(urlMtq, PARAMSMtq)
    return requests.get(urlDif, PARAMSDif)

if __name__ == '__main__':

    # reponse = callWMSInfo()
    # tes = xmltodict.parse(reponse.content)
    # my_json = reponse.content.decode('utf8').replace("'", '"')
    # print('ici')
    # data = json.loads(my_json)
    # s = json.dumps(data, indent=4, sort_keys=True)

    reponse2 = callWFSFeature()
    # tes = reponse2.json()
    # tes = xmltodict.parse(reponse2)
    namespaces = { 'http://mapserver.gis.umn.edu/mapserver': None,  # skip this namespace
                   'http://www.opengis.net/gml': None,
                   "http://www.opengis.net/wfs": None
                   }
    # tes = xmltodict.parse(reponse2.content,process_namespaces=True, namespaces=namespaces)
    my_json = reponse2.content.decode('utf8').replace("'", '"')
    my_json2 = json.loads(reponse2.content)

    ## wms filter
    response = callWmsFilter()


    print('ici')

# reponse = requests.get(url=URL, params=PARAMS)
#
# callWfs():
# import json, os, sys, uuid
# # import boto
# from urllib.parse import unquote_plus
# import requests
#
# # s3_client = boto3.client('s3')
#
#
# # def lambda_handler(event, context):
#     some_text = "test"
#     bucket_name = "josee-bucket3"
#     callWfs = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?service=WFS&request=GetFeature&version=1.1.0&typename=nord_photo_oblique&srsname=EPSG:3857&maxFeatures=1000&propertyName=LATITUDE,LONGITUDE,NOM_PHOTO,geometry&bbox=-7937865.542621327,5960166.782724251,-7833376.124955491,6045546.943318793,EPSG:3857"
#
#     response = requests.get(callWfs)
#     content = response.content
#
#     file_name = "my_test_file2.geojson"
#
#     tmp_file = "/tmp/" + file_name
#     with open(tmp_file, "w") as file:
#         file.write(content)
#
#     s3_path = "output/" + file_name
#     ## os.system('echo testing... >'+lambda_path)
#     # s3 = boto3.resource("s3")
#     # s3.meta.client.upload_file(tmp_file, bucket_name, file_name)
#     ## s3.meta.client.upload_file(lambda_path, bucket_name, file_name)
#
#     return {
#         'statusCode': 200,
#         'body': json.dumps('file is created in:' + s3_path)
#     }
#
#
# print('reponse')