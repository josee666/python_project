


import requests, os, boto3, json, requests
from serviceWebService import *
from osgeo import gdal

class ErrorServiceGDAL(Exception):
    """ JM 2022-10
        Classe exception lancée lors d'un probleme avec le serviceBD.

        Exemple apel:   try:
                            ...
                            raise ErreurServiceBD("probleme xyz")
                        except ErreurServiceBD as e:
                            print (e.message)
    """
    def __init__(self, message="Error from ServiceAWSLambda", errorType="ErrorServiceAWSLambda"):
        self.message = message
        self.errorType = errorType

    def __str__(self):
        return repr(self.message)


class ServiceGDAL():
    """ 2022-10 JM
    Classe qui sert
    PARAM:


    Exemple
"""

    def __init__(self):
        self.ok = True


    def translateFormat(self, inFile, outputFile, EPSG='3857'):

        translateOptionText = "-a_srs EPSG:{}".format(EPSG)
        translateOptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))


        gdal.Translate(outputFile, inFile, options=translateOptions)

        print('file {} cree'.format(outputFile))


    def georefFile(self, inPathFile, outPathFile, ullr, epsg="3857"):
    ### Dans API python le param -a_ullr n'existe pas 😒🤦‍♂️🤔

        EPSG = "-a_srs EPSG:{}".format(epsg)  # WGS84
        a_ullr = "-a_ullr {}".format(ullr)

        # a_ullr = "-a_ullr -8002058.621, 5969600.050, -8000178.748, 5967433.538"
        # translateOptionText = EPSG+" -a_ullr " + str(WestBoundCoord) + " " + str(NorthBoundCoord) + " " + str(EastBoundCoord) + " " + str(SouthBoundCoord)

        translateOptionText = EPSG + " " + a_ullr

        translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))

        gdal.Translate(outPathFile, inPathFile, options=translateoptions)


if __name__ == '__main__':
    #
    objServGdal = ServiceGDAL()
    inFile = "D:\\python\\gitProjet\\donneeTests\\AWS\\new2\\mapEPSG_3857.tiff"
    out = "D:\\python\\gitProjet\\donneeTests\\AWS\\new2\\geoScrip.pdf"
    objServGdal.translateFormat(inFile, out)
    print('pis')

    #### ok fonctionne!!


    # utilWMS = ServiceUtilWebService()
    #
    #
    # output = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython.tiff"
    # outputPdf = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython.pdf"
    # outputPdfGeo = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\testGdalPython_georef.pdf"
    #
    # callTiff = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/tiff&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    # callPdf = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?_t=9514ce3a&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/tiff&TRANSPARENT=true&LAYERS=lidar_pentes&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi%3A96&CRS=EPSG%3A3857&STYLES=&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"
    #
    # utilWMS.saveFileFromWMSCall(callPdf, output)
    #
    #
    # dictParam = utilWMS.call2paramDict(callPdf)
    # ullr = utilWMS.BBOX2UllrString(dictParam["BBOX"])
    #
    # objServGdal.georefFile(inPathFile=outputPdf, outPathFile=outputPdfGeo, ullr=ullr)







