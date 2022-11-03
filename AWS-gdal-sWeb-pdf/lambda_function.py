

from serviceUtilAWSLamda import *

def lambda_handler(event, contex):
    servAws = ServiceUtilAWSLambda(bucketName="josee-bucket3", local=False, awsAccesKeyCsvFile='')

    callPdf_penteLidar = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/pdf&LAYERS=lidar_pentes&CRS=EPSG%3A3857&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    callTiff = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/tiff&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    # callPdf = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/pdf&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"


    servAws.saveWmsCallToFileInS3(call=callPdf_penteLidar,  fileNameExt="testPdf.pdf", type= "pdf", repTmp= True)

    return {
        'statusCode': 200,
        'body': json.dumps('file is created!' )
    }




