
import json, boto3 ,os, sys, uuid
from urllib.parse import unquote_plus
import requests

s3_client = boto3.client('s3')


def lambda_handler(event, context):

    local = True

    some_text = "test"
    bucket_name = "josee-bucket3"
    callWfs = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?service=WFS&request=GetFeature&version=1.1.0&typename=nord_photo_oblique&srsname=EPSG:3857&maxFeatures=1000&propertyName=LATITUDE,LONGITUDE,NOM_PHOTO,geometry&bbox=-7937865.542621327,5960166.782724251,-7833376.124955491,6045546.943318793,EPSG:3857"
    callPdf = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/x-pdf&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"

    # response = requests.get(callWfs)
    response = requests.get(callPdf)
    content = response.content
    # content = response.content.decode("utf-8")

    file_name = "my_test_file2.pdf"
    tmp_file = "/tmp/" + file_name

    if local:
        tmp_file = "D:\\python\\gitProjet\\python_project\\AWS\\output\\tmp\\" + file_name

    import base64
    # data = response.json()["data"]
    with open(tmp_file, 'wb') as f:
        f.write(base64.b64decode(content))


    # with open(tmp_file, "w") as file:
    #     file.write(content)

    s3_path = "output/" + file_name
    ## os.system('echo testing... >'+lambda_path)

    s3 = boto3.resource("s3")
    if local:
        s3 = boto3.resource('s3',
                       aws_access_key_id="AKIAVZJ7BGIRIDLYOIZB",
                       aws_secret_access_key="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")

    s3.meta.client.upload_file(tmp_file, bucket_name, file_name)
    ## s3.meta.client.upload_file(lambda_path, bucket_name, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('file is created in:' + s3_path)
    }

lambda_handler('test', 'local')