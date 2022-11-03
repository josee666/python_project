

from serviceUtilAWSLamda import *
from serviceWebService import *
from serviceGdal import *




if __name__ == '__main__':


    file = "D:\\AWS\\accessKey\\josee666_accessKeys.csv"
    servAws = ServiceUtilAWSLambda(bucketName="josee-bucket3", local=True, awsAccesKeyCsvFile=file)

    objServGdal = ServiceGDAL()
    utilWMS = ServiceUtilWebService()

    callPdf_penteLidar = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/pdf&LAYERS=lidar_pentes&CRS=EPSG%3A3857&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"


    outputTiff = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython.tiff"
    outputPdf = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython.pdf"
    outputPdfGeo = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython_georef.pdf"

    callTiff = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/tiff&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    callPdf = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/pdf&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    utilWMS.saveFileFromWMSCall(call=callPdf, pathOutputFile=outputPdf)


    # dictParam = utilWMS.call2paramDict(callPdf)
    # ullr = utilWMS.BBOX2UllrString(dictParam["BBOX"])


    # objServGdal.translateFormat(inFile=outputTiff, outputFile=outputPdfGeo)

    httpReponse = servAws.saveLocalFileInS3Bucket(outputTiff)

    print('ok')


